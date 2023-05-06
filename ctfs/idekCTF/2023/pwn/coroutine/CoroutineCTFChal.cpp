#include <iostream>
#include <coroutine>
#include <span>
#include <optional>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <cassert>
#include <vector>


void load_flag()
{
    char flag[400];
    FILE* fp = fopen("flag", "rt");
    fscanf(fp, "%s", flag);
    fclose(fp);
}

struct io_context
{
    struct entry
    {
        int fd;
        std::coroutine_handle<> coroutine;
    };
    std::vector<entry> reads_;
    std::vector<entry> writes_;

    void run_until_done()
    {
        while (!reads_.empty() || !writes_.empty())
        {
            load_flag();

            fd_set readfds;
            FD_ZERO(&readfds);

            fd_set writefds;
            FD_ZERO(&writefds);

            fd_set exceptfds;
            FD_ZERO(&exceptfds);

            int maxfd = 0;
            for (auto& read : reads_)
            {
                maxfd = std::max(maxfd, read.fd);
                FD_SET(read.fd, &readfds);
                FD_SET(read.fd, &exceptfds);
            }

            for (auto& write : writes_)
            {
                maxfd = std::max(maxfd, write.fd);
                FD_SET(write.fd, &writefds);
                FD_SET(write.fd, &exceptfds);
            }

            int donefds = ::select(maxfd + 1, &readfds, &writefds, &exceptfds, /*timeout*/nullptr);
            if (donefds == -1)
            {
                std::cerr << "Error performing select() errno: " << errno << '\n';
                return;
            }

            // Take a copy as this may change
            auto reads = reads_;
            auto writes = writes_;

            for (auto & read : reads)
            {
                if (FD_ISSET(read.fd, &readfds) || FD_ISSET(read.fd, &exceptfds))
                {
                    auto coroutine = std::move(read.coroutine);
                    reads_.erase(std::remove_if(reads_.begin(), reads_.end(), [fd = read.fd](auto& item) { return item.fd == fd; }));
                    coroutine.resume();
                    continue;
                }
            }

            for (auto& write : writes)
            {
                if (FD_ISSET(write.fd, &writefds) || FD_ISSET(write.fd, &exceptfds))
                {
                    auto coroutine = std::move(write.coroutine);
                    writes_.erase(std::remove_if(writes_.begin(), writes_.end(), [fd = write.fd](auto& item) { return item.fd == fd; }));
                    coroutine.resume();
                    continue;
                }
            }
        }
    }

    void add_read(int fd, std::coroutine_handle<> coroutine)
    {
#ifdef _DEBUG
        for (auto& read : reads_)
        {
            assert(read.fd != fd);
        }
#endif
        reads_.push_back({ fd, std::move(coroutine) });
    }


    void add_write(int fd, std::coroutine_handle<> coroutine)
    {
#ifdef _DEBUG
        for (auto& write: writes_)
        {
            assert(write.fd != fd);
        }
#endif
        writes_.push_back({ fd, std::move(coroutine) });
    }

    void cancel(int fd)
    {
        auto rit = reads_.begin();
        while (rit != reads_.end())
        {
            if (rit->fd == fd)
            {
                reads_.erase(rit);
                break;
            }
        }

        auto wit = writes_.begin();
        while (wit != writes_.end())
        {
            if (wit->fd == fd)
            {
                writes_.erase(wit);
                break;
            }
        }
    }
};


template<typename Result>
class Task {
public:
    struct promise_type {
        std::optional<Result> result_;

        Task get_return_object() {
            return Task{ this };
        }

        void unhandled_exception() noexcept {}

        void return_value(Result result) noexcept { result_ = std::move(result); }
        std::suspend_never initial_suspend() { return {}; }

        struct FinalAwaiter {
            constexpr bool await_ready() noexcept { return false; }

            std::coroutine_handle<>
                await_suspend(std::coroutine_handle<promise_type> coroutine) noexcept {
                auto& promise = coroutine.promise();
                return promise.continuation_ != nullptr ? promise.continuation_ : std::noop_coroutine();
            }

            // nothing to do, the coroutine will no longer be executed
            void await_resume() noexcept { }
        };

        FinalAwaiter final_suspend() noexcept { return {}; }

        void set_continuation(std::coroutine_handle<> continuation) {
            continuation_ = continuation;
        }

        std::coroutine_handle<> continuation_;
    };

    explicit Task(promise_type* promise)
        : handle_{ HandleT::from_promise(*promise) } {}
    Task(Task&& other) : handle_{ std::exchange(other.handle_, nullptr) } { }

    ~Task() {
        if (handle_) {
            handle_.destroy();
        }
    }

    Task & operator=(const Task&) = delete;

    auto operator co_await() {
        struct Awaiter {
            std::coroutine_handle<promise_type> this_handle;

            constexpr bool await_ready() {
                assert(this_handle);
                return this_handle.done();
            }

            void await_suspend(std::coroutine_handle<> awaiting_coroutine) {
                this_handle.promise().set_continuation(awaiting_coroutine);
            }

            Result await_resume() {
                return *this_handle.promise().result_;
            }
        };

        return Awaiter{ handle_ };
    }

    using HandleT = std::coroutine_handle<promise_type>;
    HandleT handle_;
};


struct NonCopyable
{
    NonCopyable() = default;
    NonCopyable(const NonCopyable&) = delete;
    NonCopyable& operator=(const NonCopyable&) = delete;
};


int MakeNonBlocking(int fd)
{
    int flags = fcntl(fd, F_GETFL, 0);
    flags |= O_NONBLOCK;
    return fcntl(fd, F_SETFL, flags);
}


class RecvAsync : NonCopyable {
public:
    RecvAsync(io_context& ctx, int fd, std::span<std::byte> buffer) : NonCopyable(),
        ctx_{ ctx },
        fd_{ fd },
        buffer_{ buffer }
    {
    }

    auto operator co_await() {
        struct Awaiter {
            io_context& ctx_;
            int fd_;
            std::optional<int> result_;
            std::span<std::byte> buffer_;

            Awaiter(io_context& ctx, int fd, std::span<std::byte> buffer) :
                ctx_{ ctx }, fd_{ fd }, buffer_{ buffer } {
            }

            bool await_ready() {
                int result = ::recv(fd_, buffer_.data(), buffer_.size(), 0);
                if (result == -1 && (errno == EAGAIN || errno == EWOULDBLOCK) )
                {
                    return false;
                }

                result_ = result;
                return true;
            }
            void await_suspend(std::coroutine_handle<> handle) noexcept {
                ctx_.add_read(fd_, std::move(handle));
            }
            int await_resume() {
                if (result_.has_value())
                {
                    return result_.value();
                }

                int result = ::recv(fd_, buffer_.data(), buffer_.size(), 0);
                if (result == -1)
                {
                    assert(errno != EAGAIN && errno != EWOULDBLOCK);
                }

                return result;
            }
        };
        return Awaiter{ ctx_, fd_, buffer_ };
    }

private:
    io_context& ctx_;
    int fd_;
    std::span<std::byte> buffer_;
};




class SendAsync : NonCopyable {
public:
    SendAsync(io_context& ctx, int fd, std::span<std::byte> buffer) : NonCopyable(),
        ctx_{ ctx },
        fd_{ fd },
        buffer_{ buffer }
    {
    }

    auto operator co_await() {
        struct Awaiter {
            io_context& ctx_;
            int fd_;
            std::optional<int> result_;
            std::span<std::byte> buffer_;

            Awaiter(io_context& ctx, int fd, std::span<std::byte> buffer) :
                ctx_{ ctx }, fd_{ fd }, buffer_{ buffer } {
            }

            bool await_ready() {
                int result = ::send(fd_, buffer_.data(), buffer_.size(), 0);
                if (result == -1 && (errno == EAGAIN || errno == EWOULDBLOCK))
                {
                    return false;
                }

                result_ = result;
                return true;
            }
            void await_suspend(std::coroutine_handle<> handle) noexcept {
                ctx_.add_write(fd_, std::move(handle));
            }

            int await_resume() {
                if (result_.has_value())
                {
                    return result_.value();
                }

                int result = ::send(fd_, buffer_.data(), buffer_.size(), 0);
                if (result == -1)
                {
                    assert(errno != EAGAIN && errno != EWOULDBLOCK);
                }

                return result;
            }
        };
        return Awaiter{ ctx_, fd_, buffer_ };
    }

private:
    io_context& ctx_;
    int fd_;
    std::span<std::byte> buffer_;
};

Task<bool> SendAllAsync(io_context& ctx, int socket, std::span<std::byte> buffer)
{
    int offset = 0;
    while (offset < buffer.size())
    {
        int result = co_await SendAsync(ctx, socket, std::span(buffer.data() + offset, buffer.size() - offset));
        if (result == -1)
        {
            co_return false;
        }

        offset += result;
    }
    co_return true;
}

Task<bool> SendAllAsyncNewline(io_context& ctx, int socket, std::span<std::byte> buffer)
{
    std::byte buffer2[513];
    std::copy(buffer.begin(), buffer.end(), buffer2);
    buffer2[buffer.size()] = (std::byte)'\n';
    return SendAllAsync(ctx, socket, std::span(buffer2, buffer.size()+1));
}

Task<bool> client_loop(io_context& ctx, int socket)
{
    while (true)
    {
        std::byte buffer[512];
        int recved = co_await RecvAsync(ctx, socket, buffer);
        if (recved == 0)
        {
            std::cout << "Disconnected\n";
            co_return true;
        }
        if (recved == -1)
        {
            std::cout << "Could not receive\n";
            co_return false;
        }
        
        bool send_result = co_await SendAllAsyncNewline(ctx, socket, std::span(buffer, recved));
        if (!send_result)
        {
            std::cout << "Could not send: " << errno << "\n";
            co_return false;
        }
    }
}

Task<bool> server(io_context & ctx)
{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    assert(sock != -1);


    int listen_result = listen(sock, 1);
    assert(listen_result != -1);

    struct sockaddr_in sin;
    socklen_t len = sizeof(sin);
    int getsockname_result = ::getsockname(sock, (sockaddr*)&sin, &len);
    assert(getsockname_result != -1);
    std::cout << "port number " << ntohs(sin.sin_port) << "\n";


    int client_size;
    struct sockaddr_in client_addr;
    socklen_t client_addr_size = sizeof(client_addr);

    int accept_result = accept(sock, (sockaddr*)&client_addr, &client_addr_size);
    assert(accept_result != -1);

    MakeNonBlocking(accept_result);

    int sendbuff = 128;
    setsockopt(accept_result, SOL_SOCKET, SO_SNDBUF, &sendbuff, sizeof(sendbuff));

    co_await client_loop(ctx, accept_result);

    co_return true;
}


int main(int argc, char* argv[])
{
    setbuf(stdout, nullptr);

    io_context ctx;

    auto s = server(ctx);

    ctx.run_until_done();

    return EXIT_SUCCESS;
}


