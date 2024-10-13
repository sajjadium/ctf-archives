#include <cstdlib>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <unistd.h>
#include <pthread.h>
#include <vector>
#include <memory>

// Lock-free, thread-safe FIFO.
template<typename T, unsigned int buffer_size=256>
class RingBuffer
{
    T backing_buf[buffer_size];
    volatile unsigned int head = 0;
    volatile unsigned int tail = 0;

public:
    RingBuffer()
    {
        memset((void*) backing_buf, 0, sizeof(backing_buf));
        head = 0;
        tail = 0;
        __sync_synchronize();
    }

    // Reader-side functions
    bool empty(const unsigned int& tail_local) const
    {
        return head == tail_local;
    }

    T read(unsigned int& tail_local)
    {
        while (empty(tail_local)); // Buffer is empty, block.

        T data = std::move(backing_buf[tail_local]);
        tail_local = (tail_local + 1) % buffer_size;
        tail = tail_local;
        return std::move(data);
    }

    // Writer-side functions
    bool full(const unsigned int& head_local) const
    {
        return (head_local + 1) % buffer_size == tail;
    }

    void write(T data, unsigned int& head_local)
    {
        while (full(head_local)); // Buffer is full, block.

        backing_buf[head_local] = std::move(data);
        head_local = (head_local + 1) % buffer_size;
        head = head_local;
    }
};

struct Request
{
    char *str;
    uint64_t result;

    Request(char *str, int result) : str(strdup(str)), result(result) {}
    ~Request() { free(str); }
};

// Work queue
RingBuffer<Request*> wq;
// Results queue
RingBuffer<std::unique_ptr<Request>, 65536*2> rq;

void* thread_consumer(void* arg)
{
    uint64_t i = 0;
    unsigned int wq_tail = 0;
    unsigned int rq_head = 0;

    while (1) {
        auto data = wq.read(wq_tail);
        data->result = strlen(data->str);
        rq.write(std::unique_ptr<Request>(data), rq_head);
    }
}

unsigned int get_number(bool prompt=true)
{
    unsigned int num;
    if (prompt) {
        printf("> ");
        fflush(stdout);
    }
    scanf("%u", &num);
    int c;
    do {
        c = getchar();
    } while(c != EOF && c != '\n');
    return num;
}

void manage_results(std::vector<std::unique_ptr<Request>>& results)
{
    printf("%lu results:\n", results.size());
    if (!results.size())
        return;
    for (int i = 0; i < results.size(); i++) {
        auto& result = results[i];
        printf("#%d: %s", i, result.get() ? result->str : "<deleted>");
    }
    printf("Choose a result: #");
    fflush(stdout);
    unsigned int i = get_number(false);
    if (i >= results.size())
        exit(1);
    auto& result = results[i];
    printf("Result #%d selected\n", i);
    if (!result) {
        puts("<deleted>");
        return;
    }
    switch (get_number()) {
        // View result
        case 1: {
            printf("Input: %s\n", result->str);
            printf("Result: %ld\n", result->result);
            return;
        }

        // Delete result
        case 2:
        puts("Result deleted");
        result.reset();
        return;

        default:
        exit(1);
    }
    return;
}

void thread_producer()
{
    char buf[64];
    memset(buf, 0, sizeof(buf));

    unsigned int wq_head = 0;
    unsigned int rq_tail = 0;

    std::vector<std::unique_ptr<Request>> results;

    while (1) {
        switch (get_number()) {
            // New request
            case 1: {
                puts("How many requests in this job?");
                unsigned int count = get_number();
                if (count > 100000) {
                    puts("Too many!");
                    exit(1);
                }
                for (unsigned int i = 0; i < count; i++) {
                    if (!fgets_unlocked(buf, sizeof(buf), stdin))
                        exit(0);
                
                    wq.write(new Request{buf, 0}, wq_head);
                }
                break;
            }
            
            // Receive results
            case 2: {
                unsigned int n = 0;
                while (!rq.empty(rq_tail)) {
                    results.push_back(std::unique_ptr<Request>(rq.read(rq_tail))), n++;
                }
                printf("Received %u results\n", n);
                break;
            }

            // Manage results
            case 3:
            manage_results(results);
            break;

            // Clear results
            case 4:
            puts("All saved results cleared");
            results.clear();
            break;

            // Exit
            case 5:
            puts("Bye");

            default:
            exit(1);
        }
        
    }
}

int main()
{
    alarm(60);

    puts("hihgly scalable strlen() service");
    puts("1. New job");
    puts("2. Receive results");
    puts("3. Manage results");
    puts("3.1. View result");
    puts("3.2. Delete result");
    puts("4. Clear results history");
    puts("5. Exit");

    pthread_t pt_C;   
    pthread_create(&pt_C, 0, thread_consumer, 0);

    thread_producer();
}
