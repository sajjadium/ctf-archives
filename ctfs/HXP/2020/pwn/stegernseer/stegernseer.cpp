#include <algorithm>
#include <array>
#include <atomic>
#include <charconv>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <future>
#include <iomanip>
#include <iostream>
#include <limits>
#include <list>
#include <memory>
#include <mutex>
#include <string_view>
#include <thread>
#include <queue>

#include <x86intrin.h> // This should pull in all the various intrinsics headers (immintrin.h, xmmintrin.h, ...).

using namespace std::literals;

#define PRODUCT_NAME "stegernseer"
#define PRODUCT_URL "https://stegernseer.hxp.io/"
constexpr static std::size_t DEFAULT_THREADS = 64;

constexpr static std::size_t MAX_CONCURRENT_IMAGES = 4;
constexpr static std::size_t MAX_WIDTH = 32;
constexpr static std::size_t MAX_HEIGHT = 32;
constexpr static std::size_t MAX_ANNOTATION_LENGTH = 100;

[[noreturn]] inline void fail(std::string_view message) {
    std::cout << message << std::endl;
    std::exit(1);
}

template <typename T> inline void check(T&& value, std::string_view message) {
    if (!std::forward<T>(value))
        fail(std::move(message));
}

// The compiler is allowed to remove std::memset sometimes, so we roll our own
namespace {
    enum class block_alignment { NOT_ALIGNED, ALIGNED_AT_START, ALIGNED_AT_END };
    template <block_alignment Alignment> [[gnu::always_inline]] inline void zero_memory_block(std::uintptr_t from, std::size_t size) {
        // We have size < 32, the rest should be handled by zero_array.
        if constexpr (Alignment == block_alignment::ALIGNED_AT_START) {
            if (size & 16) {
                _mm_stream_si128(reinterpret_cast<__m128i *>(from), _mm_setzero_si128());
                from += 16;
                size -= 16;
            }
        } else if constexpr (Alignment == block_alignment::ALIGNED_AT_END) {
            if (size & 16) {
                _mm_stream_si128(reinterpret_cast<__m128i *>(from + size - 16), _mm_setzero_si128());
                size -= 16;
            }
        } else {
            if (size & 16) {
                *reinterpret_cast<std::uint64_t *>(from)     = static_cast<std::uint64_t>(0);
                *reinterpret_cast<std::uint64_t *>(from + 8) = static_cast<std::uint64_t>(0);
                from += 16;
                size -= 16;
            }
        }

        // Now size < 16, and we don't have to deal with alignments anymore
        switch (size) {
            case 15: *reinterpret_cast<std::uint64_t *>(from) = static_cast<std::uint64_t>(0); *reinterpret_cast<std::uint32_t *>(from + 8) = static_cast<std::uint32_t>(0); *reinterpret_cast<std::uint16_t *>(from + 12) = static_cast<std::uint16_t>(0); *reinterpret_cast<std::uint8_t *>(from + 14) = static_cast<std::uint8_t>(0);  break;
            case 14: *reinterpret_cast<std::uint64_t *>(from) = static_cast<std::uint64_t>(0); *reinterpret_cast<std::uint32_t *>(from + 8) = static_cast<std::uint32_t>(0); *reinterpret_cast<std::uint16_t *>(from + 12) = static_cast<std::uint16_t>(0); break;
            case 13: *reinterpret_cast<std::uint64_t *>(from) = static_cast<std::uint64_t>(0); *reinterpret_cast<std::uint32_t *>(from + 8) = static_cast<std::uint32_t>(0); *reinterpret_cast<std::uint8_t *>(from + 12)  = static_cast<std::uint8_t>(0);  break;
            case 12: *reinterpret_cast<std::uint64_t *>(from) = static_cast<std::uint64_t>(0); *reinterpret_cast<std::uint32_t *>(from + 8) = static_cast<std::uint32_t>(0); break;
            case 11: *reinterpret_cast<std::uint64_t *>(from) = static_cast<std::uint64_t>(0); *reinterpret_cast<std::uint16_t *>(from + 8) = static_cast<std::uint16_t>(0); *reinterpret_cast<std::uint8_t *>(from + 10)  = static_cast<std::uint8_t>(0);  break;
            case 10: *reinterpret_cast<std::uint64_t *>(from) = static_cast<std::uint64_t>(0); *reinterpret_cast<std::uint16_t *>(from + 8) = static_cast<std::uint16_t>(0);  break;
            case 9:  *reinterpret_cast<std::uint64_t *>(from) = static_cast<std::uint64_t>(0); *reinterpret_cast<std::uint8_t *>(from + 8)  = static_cast<std::uint8_t>(0);  break;
            case 8:  *reinterpret_cast<std::uint64_t *>(from) = static_cast<std::uint64_t>(0); break;
            case 7:  *reinterpret_cast<std::uint32_t *>(from) = static_cast<std::uint32_t>(0); *reinterpret_cast<std::uint16_t *>(from + 4) = static_cast<std::uint16_t>(0); *reinterpret_cast<std::uint8_t *>(from + 6)   = static_cast<std::uint8_t>(0);  break;
            case 6:  *reinterpret_cast<std::uint32_t *>(from) = static_cast<std::uint32_t>(0); *reinterpret_cast<std::uint16_t *>(from + 4) = static_cast<std::uint16_t>(0); break;
            case 5:  *reinterpret_cast<std::uint32_t *>(from) = static_cast<std::uint32_t>(0); *reinterpret_cast<std::uint8_t *>(from + 4)  = static_cast<std::uint8_t>(0);  break;
            case 4:  *reinterpret_cast<std::uint32_t *>(from) = static_cast<std::uint32_t>(0); break;
            case 3:  *reinterpret_cast<std::uint16_t *>(from) = static_cast<std::uint16_t>(0); *reinterpret_cast<std::uint8_t *>(from + 2)  = static_cast<std::uint8_t>(0);  break;
            case 2:  *reinterpret_cast<std::uint8_t *>(from)  = static_cast<std::uint8_t>(0);  break;
            case 1:  *reinterpret_cast<std::uint8_t *>(from)  = static_cast<std::uint8_t>(0);  break;
            case 0:   break;
        }
    }
}

template <typename T> void zero_array(T *pointer, std::size_t size) {
    std::uintptr_t location = reinterpret_cast<std::uintptr_t>(pointer);
    size *= sizeof(T);
    if (size < sizeof(__m256i))
        return zero_memory_block<block_alignment::NOT_ALIGNED>(location, size);

    std::uintptr_t mask = sizeof(__m256i) - 1;
    __m256i zero = _mm256_setzero_si256();

    std::uintptr_t prev_aligned = location & (~mask);
    std::ptrdiff_t unaligned = (sizeof(__m256i) - (location - prev_aligned)) & mask;
    zero_memory_block<block_alignment::ALIGNED_AT_END>(location, unaligned);
    location += unaligned;
    size -= unaligned;

    std::uintptr_t aligned_size = size & (~mask);
    std::uintptr_t aligned_end = location + aligned_size - sizeof(__m256i);
    for (; location <= aligned_end; location += sizeof(__m256i))
        _mm256_stream_si256(reinterpret_cast<__m256i *>(location), zero);

    size -= aligned_size;
    zero_memory_block<block_alignment::ALIGNED_AT_START>(location, size);
    _mm_sfence();
}

// If std::underlying_type_t is char / unsigned char, the streaming operators do unexpected things, so pick an unsigned int instead.
template <typename Enum> using underlying_streamable_t = std::conditional_t<std::numeric_limits<std::underlying_type_t<Enum>>::digits <= 8, unsigned int, std::underlying_type_t<Enum>>;
#define make_enum_streamable(type) \
    std::istream& operator>>(std::istream& stream, type& value) { underlying_streamable_t<type> underlying; stream >> underlying; value = static_cast<type>(underlying); return stream; } \
    std::ostream& operator<<(std::ostream& stream, const type& value) { return stream << static_cast<underlying_streamable_t<type>>(value); }

template <typename T, std::size_t Capacity = 10>
class threadsafe_queue
{
public:
    threadsafe_queue() { m_inner.reserve(Capacity); }
    void push(T&& value) {
        std::lock_guard<std::mutex> lock(m_mutex);
        m_inner.insert(m_inner.begin(), std::move(value)); // If you expect the queue to be empty most of the time (which we do), pushing to the front of a std::vector is more efficient than messing around with deques.
    }
    bool pop(T& into) {
        std::lock_guard<std::mutex> lock(m_mutex);
        if (m_inner.empty())
            return false;
        into = std::move(m_inner.back());
        m_inner.pop_back();
        return true;
    }

private:
    std::vector<T> m_inner;
    std::mutex m_mutex;
};

class synchronization_point // Synchronizes with waiting threads twice so that no thread can re-enter the synchronization prior to all others passing it (something with semaphores might be nicer here, but those are not in the standard...)
{
public:
    [[nodiscard]] std::unique_lock<std::mutex> enter() {
        std::unique_lock<std::mutex> lock(m_mutex);
        wait(lock);
        return lock;
    }
    void leave(std::unique_lock<std::mutex>&& lock) {
        wait(lock);
    }
    template <typename Duration> bool step(std::size_t expected, Duration timeout) {
        std::unique_lock<std::mutex> lock(m_mutex);
        if (!m_cv.wait_for(lock, timeout, [this, expected] { return m_ready >= expected; }))
            return false;
        ++m_index;
        m_cv.notify_all(); // Wait for all to acknowledge receipt
        if (!m_cv.wait_for(lock, timeout, [this, expected] { return m_ready == 0; }))
            return false;
        ++m_index;
        m_cv.notify_all();
        return true;
    }

private:
    void wait(std::unique_lock<std::mutex>& lock) {
        ++m_ready;
        m_cv.notify_all();
        m_cv.wait(lock, [this, index = m_index.load()] { return index < m_index; });
        --m_ready;
        m_cv.notify_all();
        m_cv.wait(lock, [this, index = m_index.load()] { return index < m_index; });
    }

    std::atomic<std::size_t> m_ready = 0;
    std::atomic<std::size_t> m_index = 0;
    std::mutex m_mutex;
    std::condition_variable m_cv;
};

class threadpool
{
    using task_t = std::function<void()>;
    template <typename T> static std::reference_wrapper<T> wrap_ref(T& val) { return std::ref(val); } // std::bind does not like lvalue references otherwise
    template <typename T> static T&& wrap_ref(T&& val) { return std::forward<T>(val); }

public:
    threadpool(std::size_t size) : m_threads(size), m_stop(false) {
        auto sync = std::make_shared<synchronization_point>();
        std::generate(m_threads.begin(), m_threads.end(), [this, sync] {
            return std::thread([this, sync]() mutable {
                auto lock = sync->enter();
                auto tasks = std::make_shared<std::list<task_t>>();
                task_t current;
                sync->leave(std::move(lock));
                while (!m_stop) {
                    if (m_tasks.pop(current)) {
                        tasks->push_back(std::move(current)); // Store the task so that we don't accidentally discard shared state before the future is fetched.
                        tasks->back()();
                    } else {
                        std::this_thread::sleep_for(std::chrono::milliseconds { 100 }); // Don't completely eat up the CPU
                    }
                }
                return tasks;
            });
        });
        if (!sync->step(size, std::chrono::milliseconds { 500 })) // Wait for thread creation
            fail("Failed to create threadpool threads!");
        if (!sync->step(size, std::chrono::milliseconds { 500 })) // Wait for threads to start processing
            fail("Failed to start threadpool!");
    }
    ~threadpool() {
        m_stop = true;
        for (auto& thread : m_threads)
            thread.join();
    }
    template <typename Fn, typename... Args>
    auto push(Fn&& fn, Args&&... args) {
        using Result = std::invoke_result_t<Fn, Args...>;
        auto promise = std::make_shared<std::promise<Result>>();
        auto future = promise->get_future().share();
        auto bound = std::bind(std::forward<Fn>(fn), wrap_ref(std::forward<Args>(args))...);
        auto target = std::make_shared<decltype(bound)>(std::move(bound));
        auto packaged = [promise = std::move(promise), target = std::move(target)]() mutable {
            if constexpr (std::is_same_v<Result, void>) { (*target)(); promise->set_value(); }
            else { promise->set_value((*target)()); }
        };
        m_tasks.push(std::move(packaged));
        return future;
    }

private:
    std::vector<std::thread> m_threads;
    threadsafe_queue<task_t> m_tasks;
    std::atomic<bool> m_stop;
};

class image_note
{
public:
    image_note() : m_data(nullptr), m_size(0) {}
    explicit image_note(std::size_t size) : m_data(new char[size]), m_size(size) { zero_array(m_data, m_size); }
    void read() {
        // std::cin.getline() reads n - 1 characters or overflows, which is not what we want, but we also cannot tell std::cin.read() to stop on a newline.
        // Also, we want to know whether we actually stopped reading based on size alone or because we encountered the delimiter...
        for (std::size_t i = 0; i < m_size; ++i) { char read; check(std::cin.get(read), "Failed to read annotation!"); if (read == '\n') return; else m_data[i] = read; }
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << static_cast<std::string_view>(*this) << ": Annotation reached size limit, it may be truncated!\n";
    }
    explicit operator bool() const { return !!m_data; }
    operator const std::string_view() const { return m_data ? std::string_view { m_data, m_size } : "[no annotation]"sv; }
    std::size_t size() const { return m_size; }

private:
    char *m_data;
    std::size_t m_size;
};

class image
{
public:
    using transform_t = void (*)(image& out, const image& in, const image *mask);

    image() : m_data(nullptr), m_line(0), m_blocks(0), m_width(0), m_height(0) {}
    image(std::size_t width, std::size_t height) : m_width(width), m_height(height) {
        m_line = (m_width + sizeof(__m256i) - 1) / sizeof(__m256i);
        m_blocks = m_line * m_height;
        m_data = new __m256i[m_blocks];
        zero_array(m_data, m_blocks);
    }
    explicit operator bool() const { return !!m_data; }
    void read() {
        char input[2];
        std::uint8_t *pointer;
        std::cin >> std::ws;
        for (std::size_t row = 0; row < m_height; ++row) {
            pointer = reinterpret_cast<std::uint8_t *>(m_data) + row * m_line * sizeof(__m256i);
            for (std::size_t col = 0; col < m_width; ++col, ++pointer) {
                check(std::cin.read(input, 2), "Image incomplete!");
                auto [ptr, ec] = std::from_chars(&input[0], &input[2], *pointer, 16);
                check(ptr == &input[2] && ec == std::errc(), "Invalid input!");
            }
        }
    }
    void transform(threadpool& pool, transform_t tf, image& other, image *mask) {
        block();
        other.block();
        if (mask) mask->block();
        m_background = other.m_background = pool.push(tf, *this, const_cast<const image&>(other), const_cast<const image *>(mask));
        if (mask) mask->m_background = m_background;
    }
    void block() {
        if (m_background.valid()) {
            if (m_background.wait_for(std::chrono::milliseconds(0)) != std::future_status::ready)
                std::cout << "Waiting for background operation to complete..." << std::endl;
            m_background.get();
            m_background = std::shared_future<void>();
        }
    }
    std::pair<__m256i *, std::size_t> get() { return { m_data, m_blocks }; }
    std::pair<const __m256i *, std::size_t> get() const { return { m_data, m_blocks }; }
    image_note& note() { return m_note; }
    const image_note& note() const { return m_note; }
    std::pair<std::size_t, std::size_t> size() const { return { m_width, m_height }; }

private:
    __m256i *m_data;
    std::shared_future<void> m_background;
    image_note m_note;
    std::size_t m_line; // Blocks per line
    std::size_t m_blocks; // Total blocks
    std::size_t m_width; // Pixel width
    std::size_t m_height; // Pixel height
};

namespace alg {
    [[gnu::always_inline]] inline void stream_masked(__m256i *into, __m256i value, const __m256i *mask) {
        _mm256_stream_si256(into, _mm256_blendv_epi8(value, _mm256_load_si256(into), _mm256_cmpeq_epi64(_mm256_load_si256(mask), _mm256_setzero_si256())));
    }
    void xor_(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_xor_si256(_mm256_load_si256(i_data), _mm256_load_si256(o_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                _mm256_stream_si256(o_data, _mm256_xor_si256(_mm256_load_si256(i_data), _mm256_load_si256(o_data)));
        _mm_sfence();
    }
    void and_(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_and_si256(_mm256_load_si256(i_data), _mm256_load_si256(o_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_and_si256(_mm256_load_si256(i_data), _mm256_load_si256(o_data)));
        _mm_sfence();
    }
    void or_(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_or_si256(_mm256_load_si256(i_data), _mm256_load_si256(o_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_or_si256(_mm256_load_si256(i_data), _mm256_load_si256(o_data)));
        _mm_sfence();
    }
    void add(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_add_epi8(_mm256_load_si256(i_data), _mm256_load_si256(o_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_add_epi8(_mm256_load_si256(i_data), _mm256_load_si256(o_data)));
        _mm_sfence();
    }
    void adds(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_adds_epu8(_mm256_load_si256(i_data), _mm256_load_si256(o_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_adds_epu8(_mm256_load_si256(i_data), _mm256_load_si256(o_data)));
        _mm_sfence();
    }
    void sub(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_sub_epi8(_mm256_load_si256(o_data), _mm256_load_si256(i_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_sub_epi8(_mm256_load_si256(o_data), _mm256_load_si256(i_data)));
        _mm_sfence();
    }
    void subs(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_subs_epu8(_mm256_load_si256(o_data), _mm256_load_si256(i_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_subs_epu8(_mm256_load_si256(o_data), _mm256_load_si256(i_data)));
        _mm_sfence();
    }
    void rsub(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_sub_epi8(_mm256_load_si256(i_data), _mm256_load_si256(o_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_sub_epi8(_mm256_load_si256(i_data), _mm256_load_si256(o_data)));
        _mm_sfence();
    }
    void rsubs(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_subs_epu8(_mm256_load_si256(i_data), _mm256_load_si256(o_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_subs_epu8(_mm256_load_si256(i_data), _mm256_load_si256(o_data)));
        _mm_sfence();
    }
    void invert(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : std::pair<const __m256i *, std::size_t> { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        const __m256i full = _mm256_set1_epi8(0xff);
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_xor_si256(full, _mm256_load_si256(i_data)), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_xor_si256(full, _mm256_load_si256(i_data)));
        _mm_sfence();
    }
    void copy(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        if (!!mask)
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data, ++m_data)
                stream_masked(o_data, _mm256_load_si256(i_data), m_data);
        else
            for (std::size_t i = 0; i < i_count; ++i, ++i_data, ++o_data)
                _mm256_stream_si256(o_data, _mm256_load_si256(i_data));
        _mm_sfence();
    }
    void reverse(image& out, const image& in, const image *mask) {
        auto [o_data, o_count] = out.get();
        auto [i_data, i_count] = in.get();
        auto [m_data, m_count] = !!mask ? mask->get() : decltype(mask->get()) { nullptr, i_count };
        check(o_count >= i_count, "Output image is too small!");
        check(m_count >= i_count, "Mask image is too small!");
        const __m256i shuffle = _mm256_setr_epi8(15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0);
        if (!!mask)
            for (auto o_back = o_data + o_count; o_back > o_data; ++i_data, --o_back, ++m_data)
                stream_masked(o_back, _mm256_shuffle_epi8(_mm256_permute4x64_epi64(_mm256_load_si256(i_data), 0b01001110), shuffle), m_data);
        else
            for (auto o_back = o_data + o_count; o_back > o_data; ++i_data, --o_back)
                _mm256_stream_si256(o_back, _mm256_shuffle_epi8(_mm256_permute4x64_epi64(_mm256_load_si256(i_data), 0b01001110), shuffle));
        _mm_sfence();
    }

    enum class operation {
        XOR,
        AND,
        OR,
        ADD,
        ADDS,
        SUB,
        SUBS,
        RSUB,
        RSUBS,
        INVERT,
        COPY,
        REVERSE,
    };
    make_enum_streamable(operation)

    image::transform_t select(operation op) {
        switch (op) {
            case operation::XOR: return xor_;
            case operation::AND: return and_;
            case operation::OR: return or_;
            case operation::ADD: return add;
            case operation::ADDS: return adds;
            case operation::SUB: return sub;
            case operation::SUBS: return subs;
            case operation::RSUB: return rsub;
            case operation::RSUBS: return rsubs;
            case operation::INVERT: return invert;
            case operation::COPY: return copy;
            case operation::REVERSE: return reverse;
            default: fail("Invalid operation!");
        }
    }
}

enum class command {
    LOAD,
    ANNOTATE,
    LIST,
    TRANSFORM,
    QUIT,
};
make_enum_streamable(command)

int main() {
    std::cin.rdbuf()->pubsetbuf(0, 0); // setvbuf, but in C++
    std::cin.setf(std::ios::unitbuf);
    std::cout.rdbuf()->pubsetbuf(0, 0);
    std::cout.setf(std::ios::unitbuf);
    std::cerr.rdbuf()->pubsetbuf(0, 0);
    std::cerr.setf(std::ios::unitbuf);

    std::cout << "Welcome to " PRODUCT_NAME ", hxp's premier anti-stego image analysis toolkit!\n\n"
              << "This evaluation version is limited to working on images no larger than " << MAX_WIDTH << "x" << MAX_HEIGHT << " pixels.\n"
              << "To remove the limitations of this evaluation version, please purchase the full version at " PRODUCT_URL "\n";

    threadpool pool(DEFAULT_THREADS);
    std::array<image, MAX_CONCURRENT_IMAGES> images;

    while (true) {
        command cmd;
        std::cout << "\nPress [" << command::LOAD << "] to load an image, "
                             "[" << command::ANNOTATE << "] to annotate an image, "
                             "[" << command::LIST << "] to list all images, "
                             "[" << command::TRANSFORM << "] to transform images, and "
                             "[" << command::QUIT << "] to quit.\n"
                             "> " << std::flush;
        check(std::cin >> cmd, "Failed to read command!");

        switch (cmd) {
            case command::LOAD: {
                std::size_t image_index;
                std::cout << "Select an image slot [0 - " << images.size() - 1 << "]: " << std::flush;
                check(std::cin >> image_index, "Failed to read image slot!");
                check(0 <= image_index && image_index < images.size(), "Invalid image slot!");
                if (!!images[image_index]) {
                    std::cout << "This image slot is already occupied. Are you sure you want to overwrite the current image? [y/N]: " << std::flush;
                    std::cin >> std::ws;
                    char confirmation = std::cin.get();
                    if (confirmation != '\n')
                        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                    if (confirmation != 'y' && confirmation != 'Y')
                        continue;
                }

                std::size_t width, height;
                std::cout << "Enter image width: " << std::flush;
                check(std::cin >> width, "Failed to read image width");
                check(0 < width && width <= MAX_WIDTH, "Image is too large!");

                std::cout << "Enter image height: " << std::flush;
                check(std::cin >> height, "Failed to read image height");
                check(0 < height && height <= MAX_HEIGHT, "Image is too large!");

                images[image_index] = image(width, height);

                std::cout << "Enter hex-encoded image data: " << std::flush;
                images[image_index].read();
                break;
            }
            case command::ANNOTATE: {
                std::size_t image_index;
                std::cout << "Select an image slot [0 - " << images.size() - 1 << "]: " << std::flush;
                check(std::cin >> image_index, "Failed to read image slot!");
                check(0 <= image_index && image_index < images.size(), "Invalid image slot!");
                check(!!images[image_index], "This image slot is empty!");

                std::size_t annotation_length;
                std::cout << "Enter annotation length: " << std::flush;
                check(std::cin >> annotation_length, "Failed to read annotation length!");
                check(annotation_length <= MAX_ANNOTATION_LENGTH, "Annotation is too long!");

                if (annotation_length == 0)
                    images[image_index].note() = image_note();
                else if (!images[image_index].note() || images[image_index].note().size() != annotation_length)
                    images[image_index].note() = image_note(annotation_length);

                if (annotation_length) {
                    std::cout << "Enter annotation: " << std::flush;
                    std::cout.clear();
                    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Drop newline from earlier input
                    images[image_index].note().read();
                }
                break;
            }
            case command::LIST: {
                std::cout << "Images:\n";
                for (std::size_t index = 0; index < images.size(); ++index) {
                    std::cout << "  [" << index << "]: ";
                    if (!!images[index]) {
                        auto [width, height] = images[index].size();
                        std::cout << static_cast<std::string_view>(images[index].note()) << " (" << width << "x" << height << " pixels)\n";
                    } else {
                        std::cout << "[empty]\n";
                    }
                }
                std::cout << std::flush;
                break;
            }
            case command::TRANSFORM: {
                std::cout << "Operations:\n"
                             "  [" << std::setw(2) << alg::operation::XOR     << "]: out = out ^ in\n"
                             "  [" << std::setw(2) << alg::operation::AND     << "]: out = out & in\n"
                             "  [" << std::setw(2) << alg::operation::OR      << "]: out = out | in\n"
                             "  [" << std::setw(2) << alg::operation::ADD     << "]: out = out + in  (wrapping)\n"
                             "  [" << std::setw(2) << alg::operation::ADDS    << "]: out = out + in  (saturating)\n"
                             "  [" << std::setw(2) << alg::operation::SUB     << "]: out = out - in  (wrapping)\n"
                             "  [" << std::setw(2) << alg::operation::SUBS    << "]: out = out - in  (saturating)\n"
                             "  [" << std::setw(2) << alg::operation::RSUB    << "]: out = in  - out (wrapping)\n"
                             "  [" << std::setw(2) << alg::operation::RSUBS   << "]: out = in  - out (saturating)\n"
                             "  [" << std::setw(2) << alg::operation::INVERT  << "]: out =     ~ in\n"
                             "  [" << std::setw(2) << alg::operation::COPY    << "]: out =       in\n"
                             "  [" << std::setw(2) << alg::operation::REVERSE << "]: out =       in  (reversed, with the last pixel first)\n"
                             "\nSelect an operation: " << std::flush;
                alg::operation op;
                check(std::cin >> op, "Failed to read operation!");

                std::size_t output_index;
                std::cout << "Select an output image slot [0 - " << images.size() - 1 << "]: " << std::flush;
                check(std::cin >> output_index, "Failed to read image slot!");
                check(0 <= output_index && output_index < images.size(), "Invalid image slot!");
                check(!!images[output_index], "This image slot is empty!");

                std::cout << "Select an input image slot [0 - " << images.size() - 1 << "]: " << std::flush;
                std::size_t input_index;
                check(std::cin >> input_index, "Failed to read image slot!");
                check(0 <= input_index && input_index < images.size(), "Invalid image slot!");
                check(!!images[input_index], "This image slot is empty!");

                std::cout << "Select a mask image slot [0 - " << images.size() - 1 << "], or -1 to apply the operation to the whole image: " << std::flush;
                std::ptrdiff_t mask_index; // No std::ssize_t, for some reason.
                check(std::cin >> mask_index, "Failed to read mask slot!");
                check(mask_index == -1 || static_cast<std::size_t>(mask_index) < images.size(), "Invalid mask slot!");
                check(mask_index == -1 || !!images[mask_index], "This image slot is empty!");
                check(mask_index == -1 || static_cast<std::size_t>(mask_index) != output_index, "Cannot use output image as mask image!");

                images[output_index].transform(pool, alg::select(op), images[input_index], mask_index >= 0 ? &images[mask_index] : nullptr);
                break;
            }
            case command::QUIT: {
                std::cout << "\nThank you for trying " PRODUCT_NAME "!\n";
                std::exit(0);
                break;
            }
            default: fail("Invalid command!");
        }
    }
}
