// g++ -fcoroutines -std=c++20 -o multitool chall.cpp -lcrypto -lcryptopp

#include <iostream>
#include <coroutine>
#include <future>
#include <cstring>
#include <chrono>
#include <stdexcept>
#include <thread>
#include <unistd.h> 
#include <vector> 

#include <cryptopp/cryptlib.h>
#include <cryptopp/rijndael.h>
#include <cryptopp/modes.h>
#include <cryptopp/files.h>
#include <cryptopp/osrng.h>
#include <cryptopp/hex.h>


void init() {
    setvbuf(stdout,0,2,0);
}

void menu() {
    std::cout << "1. Create new task" << std::endl;
    std::cout << "2. Resume task" << std::endl;
    std::cout << "3. Delete task" << std::endl;
}

void algorithm_menu() {
    std::cout << std::endl;
    std::cout << "Slow algorithms (Resume twice): " << std::endl;
    std::cout << "1. AES CBC" << std::endl;
    std::cout << "2. Bubble Sort" << std::endl;
    std::cout << "3. Coin Change" << std::endl;
    std::cout << "4. Substring Search" << std::endl;
    std::cout << std::endl;

    std::cout << "Fast algorithms (Resume once): " << std::endl;
    std::cout << "5. GCD" << std::endl;
    std::cout << "6. Linear Search" << std::endl;
    std::cout << "7. Binary Search" << std::endl;
    std::cout << "8. Fibonacci" << std::endl;
    std::cout << std::endl;

}

class Algo 
{
    public:
        Algo() {
            this->name = "Algo";
        }
        virtual ~Algo() {}

        virtual void get_algo_params() {}
        virtual bool do_algo() { return true; }

        std::string get_name() {
            return this->name;
        }

        std::string get_result() {
            return this->result;
        }

        void set_result(std::string result) {
            this->result = result;
        }

    protected:
        std::string name;
        std::string type;
        std::string result;
};

class FastAlgo : public Algo
{
    public:
        FastAlgo() {
            this->type = "Fast Algorithm";
        }
        ~FastAlgo() {}
};

class SlowAlgo : public Algo
{
    public:
        SlowAlgo() {
            this->type = "Slow Algorithm";
        }
        ~SlowAlgo() {}
};

class AES_CBC : public SlowAlgo
{
    public:
        AES_CBC() {
            this->name = "AES CBC";
            this->key = new CryptoPP::byte[CryptoPP::AES::DEFAULT_KEYLENGTH];
            this->iv = new CryptoPP::byte[CryptoPP::AES::DEFAULT_KEYLENGTH];   
        }
        ~AES_CBC() {
            delete[] this->key;
            delete[] this->iv;
        }

        void get_algo_params() override {
            CryptoPP::AutoSeededRandomPool prng;
            prng.GenerateBlock(this->key, CryptoPP::AES::DEFAULT_KEYLENGTH);
            prng.GenerateBlock(this->iv, CryptoPP::AES::DEFAULT_KEYLENGTH);
            std::cout << "Enter plaintext: ";
            std::cin >> this->plaintext;
        }

        bool do_algo() override {

            try
            {
                CryptoPP::CBC_Mode< CryptoPP::AES >::Encryption e;
                e.SetKeyWithIV(this->key, CryptoPP::AES::DEFAULT_KEYLENGTH, this->iv);

                CryptoPP::StringSource s(this->plaintext, true, 
                    new CryptoPP::StreamTransformationFilter(e,
                        new CryptoPP::StringSink(this->ciphertext)
                    )
                );
            }
            catch (const std::exception& e) {
                std::cerr << e.what() << std::endl;
                return false;
            }
            this->set_result(this->ciphertext);
            return true;
        }

    private:
        std::string plaintext;
        std::string ciphertext;
        CryptoPP::byte *key;
        CryptoPP::byte *iv;
};

class BubbleSort : public SlowAlgo
{
    public:
        BubbleSort() {
            this->name = "Bubble Sort";
        }
        ~BubbleSort() {
            delete[] this->numbers;
        }

        void get_algo_params() override {
            std::cout << "N: ";
            std::cin >> this->n;
            this->numbers = new long long[n];
            std::cout << "Numbers: ";
            for(int i = 0; i < this->n; i++ ) {
                std::cin >> this->numbers[i];
            }
        }

        bool do_algo() override {
            long long tmp;
            for(int i = 0; i < this->n-1; i++) {
                for(int j = i+1; j < this->n; j++) {
                    if(this->numbers[i] > this->numbers[j]) {
                        tmp = this->numbers[i];
                        this->numbers[i] = this->numbers[j];
                        this->numbers[j] = tmp;
                    }
                }
            }
            std::string result = "";
            for(int i = 0; i < this->n; i++) {
                result += std::to_string(this->numbers[i]);
                result += " ";
            }
            this->set_result(result);
            return true;
        }

    private:
        long long *numbers;
        long long n;
};

class CoinChange : public SlowAlgo
{
    public:
        CoinChange() {
            this->name = "Coin Change";
        }
        ~CoinChange() {
            delete[] this->coins;
        }

        void get_algo_params() override {
            std::cout << "N: ";
            std::cin >> this->n;
            this->coins = new long long[n];
            std::cout << "Coins: ";
            for(int i = 0; i < this->n; i++ ) {
                std::cin >> this->coins[i];
            }
            std::cout << "Amount to calculate: ";
            std::cin >> this->amount;
        }

        bool do_algo() override {
            long long dp[this->amount + 1];
            for (long long i = 1; i <= this->amount; i++)
                dp[i] = 99999999999;
            dp[0] = 0;
            for (long long i = 1; i <= this->amount; i++) {
                for (long long j = 0; j < this->n; j++) {
                    if(this->coins[j] <= i) {
                        dp[i] = std::min(dp[i], dp[i-this->coins[j]] + 1);
                    }
                }
            }
            if(dp[this->amount] == 99999999999) {
                dp[this->amount] = -1;
            }
            this->set_result(std::to_string(dp[this->amount]));
            return true;
        }

    private:
        long long *coins;
        long long n;
        long long amount;
};

class SubstringSearch : public SlowAlgo
{
    public:
        SubstringSearch() {
            this->name = "Substring Search";
        }
        ~SubstringSearch() {}

        void get_algo_params() override {
            std::cout << "Haystack: ";
            std::cin >> this->haystack;
            std::cout << "Needle: ";
            std::cin >> this->needle;
        }

        bool do_algo() override {
            int res = -1;
            for (int i = 0; i <= this->haystack.length() - this->needle.length(); i++) {
                int j;
                for (j = 0; j < this->needle.length(); j++)
                    if (this->haystack[i + j] != this->needle[j])
                        break;
                if (j == this->needle.length())
                    res = j;
            }
            this->set_result(std::to_string(res));
            return true;
        }

    private:
        std::string haystack;
        std::string needle;
};

class GCD : public FastAlgo
{
    public:
        GCD() {
            this->name = "GCD";
        }
        ~GCD() {}

        void get_algo_params() override {
            std::cout << "First number: ";
            std::cin >> this->first;
            std::cout << "Second number: ";
            std::cin >> this->second;
        }

        bool do_algo() override {
            this->set_result(std::to_string(gcd(this->first, this->second)));
            return true;
        }

        long long gcd(long long a, long long b) {
            if (b == 0)
                return a;
            return gcd(b, a%b);
        }

    private:
        long long first, second;
};

class LinearSearch : public FastAlgo
{
    public:
        LinearSearch() {
            this->name = "Linear Search";
        }
        ~LinearSearch() {
            delete[] this->numbers;
        }

        void get_algo_params() override {
            std::cout << "N: ";
            std::cin >> this->n;
            this->numbers = new long long[n];
            std::cout << "Numbers: ";
            for(int i = 0; i < this->n; i++ ) {
                std::cin >> this->numbers[i];
            }
            std::cout << "Search number: ";
            std::cin >> this->to_search;
        }

        bool do_algo() override {
            int index = -1;
            for(int i = 0; i < this->n; i++ ) {
                if(this->numbers[i] == this->to_search) {
                    index = i;
                    break;
                }
            }
            this->set_result(std::to_string(index));
            return true;
        }

    private:
        long long *numbers;
        long long n;
        long long to_search;
};

class BinarySearch : public FastAlgo
{
    public:
        BinarySearch() {
            this->name = "Binary Search";
        }
        ~BinarySearch() {
            delete[] this->numbers;
        }

        void get_algo_params() override {
            std::cout << "N: ";
            std::cin >> this->n;
            this->numbers = new long long[n];
            std::cout << "Numbers: ";
            for(int i = 0; i < this->n; i++ ) {
                std::cin >> this->numbers[i];
            }
            std::cout << "Search number: ";
            std::cin >> this->to_search;
        }

        bool do_algo() override {\
            int lo = 0;
            int hi = this->n-1;
            int index = -1;
            while (lo <= hi) {
                int mid = lo + (hi - lo) / 2;
                if (this->numbers[mid] == this->to_search)
                    index = mid;
                if (this->numbers[mid] < this->to_search)
                    lo = mid + 1;
                else
                    hi = lo - 1;
            }

            this->set_result(std::to_string(index));
            return true;
        }

    private:
        long long *numbers;
        long long n;
        long long to_search;
};

class Fibonacci : public FastAlgo
{
    public:
        Fibonacci() {
            this->name = "Fibonacci";
        }
        ~Fibonacci() {
        }

        void get_algo_params() override {
            std::cout << "N: ";
            std::cin >> this->n;
        }

        bool do_algo() override {\
            long long next, curr, prev;
            curr = 0;
            prev = 1;
            for(int i = 1; i < this->n; i++ ) {
                next = (curr + prev) % 1000000007; // the numbers can get big, so we modulo it
                prev = curr;
                curr = next;
            }
            this->set_result(std::to_string(curr));
            return true;
        }

    private:
        long long n;
};

auto run_algo_async(Algo* algo)
{
    struct awaitable
    {
        Algo* algo;;
        bool await_ready() { return false; }
        void await_suspend(std::coroutine_handle<> h)
        {
            std::jthread([i = algo] {
                bool res = i->do_algo();
                if(!res) {
                    std::cerr << "Error" << std::endl;
                    exit(-1);
                }
            });
        }
        void await_resume() {}
    };
    return awaitable{algo};
}

auto do_nothing()
{
    struct awaitable
    {
        bool await_ready() { return false; }
        void await_suspend(std::coroutine_handle<> h){}
        void await_resume() {}
    };
    return awaitable{};
}

struct promise;

struct Task : std::coroutine_handle<promise>
{
    using promise_type = ::promise;
};
 
struct promise
{
    Task get_return_object() { return {Task::from_promise(*this)}; }
    std::suspend_always initial_suspend() noexcept {  return std::suspend_always{}; }
    std::suspend_always final_suspend() noexcept {  return std::suspend_always{}; }
    void return_void() {}
    void unhandled_exception() noexcept {}
};

struct SavedTask {
    Task task;
    Algo* algo;
    std::string name;
    long long call_count;
    SavedTask() {}
    SavedTask(Task task, Algo* algo, std::string name) {
        this->task = task;
        this->algo = algo;
        this->name = name;
    }
    ~SavedTask() {
        delete this->algo;
    }
};
 
auto fast_algo_factory(FastAlgo* algo)
{
    algo->get_algo_params();
    algo->do_algo();
    auto h = [result = algo->get_result()]() -> Task
    {
        std::cout << "Result: " << result << std::endl;
        co_return;
    };
    return h;
}

auto slow_algo_factory(SlowAlgo* algo)
{
    algo->get_algo_params();
    auto h = [algo_l = algo]() -> Task
    {
        co_await run_algo_async(algo_l);
        std::cout << "Result: " << algo_l->get_result() << std::endl;
        co_return;
    };
    return h;
}

int main() { 

    unsigned int choice, index;
    std::vector<SavedTask*> tasks;
    SavedTask* temp;

    init();
    while(1){
		menu();
        std::cout << "Choice: ";
        std::cin >> choice;
        if(choice == 1) {
            algorithm_menu();
            std::cout << "Choice: ";
            std::cin >> choice;
            if(choice == 1) {
                AES_CBC *cbc = new AES_CBC();
                temp = new SavedTask(slow_algo_factory(cbc)(), cbc, cbc->get_name());
                temp->call_count = 0;
            }

            else if(choice == 2) {
                BubbleSort *bubblesort = new BubbleSort();
                temp = new SavedTask(slow_algo_factory(bubblesort)(), bubblesort, bubblesort->get_name());
                temp->call_count = 0;
            }

            else if(choice == 3) {
                CoinChange *coinchange = new CoinChange();
                temp = new SavedTask(slow_algo_factory(coinchange)(), coinchange, coinchange->get_name());
                temp->call_count = 0;
            }

            else if(choice == 4) {
                SubstringSearch *substringsearch = new SubstringSearch();
                temp = new SavedTask(slow_algo_factory(substringsearch)(), substringsearch, substringsearch->get_name());
                temp->call_count = 0;
            }

            else if(choice == 5) {
                GCD *gcd = new GCD();
                temp = new SavedTask(fast_algo_factory(gcd)(), gcd, gcd->get_name());
                temp->call_count = 1; // Fast algo, we skip a call count
            }

            else if(choice == 6) {
                LinearSearch *linearsearch = new LinearSearch();
                temp = new SavedTask(fast_algo_factory(linearsearch)(), linearsearch, linearsearch->get_name());
                temp->call_count = 1; // Fast algo, we skip a call count
            }

            else if(choice == 7) {
                BinarySearch *binarysearch = new BinarySearch();
                temp = new SavedTask(fast_algo_factory(binarysearch)(), binarysearch, binarysearch->get_name());
                temp->call_count = 1; // Fast algo, we skip a call count
            }

            else if(choice == 8) {
                Fibonacci *fibonacci = new Fibonacci();
                temp = new SavedTask(fast_algo_factory(fibonacci)(), fibonacci, fibonacci->get_name());
                temp->call_count = 1; // Fast algo, we skip a call count
            }

            else {
                std::cout << "Invalid" << std::endl;
                continue;
            }

            tasks.push_back(temp);
            std::cout << "Task saved" << std::endl;
        }

        else if(choice == 2) {
            if(tasks.size() == 0) {
                std::cout << "Invalid" << std::endl;
                continue;
            }
            std::cout << "Tasks: " << tasks.size() << std::endl;
            for(int i = 0; i < tasks.size(); i++) {
                std::cout << i << ". " << tasks[i]->name << std::endl;
            }
            std::cout << "Resume task #: ";
            std::cin >> index;
            if(index >= tasks.size() || tasks[index]->call_count >= 2) {
                std::cout << "Invalid" << std::endl;
                continue;
            }
            tasks[index]->call_count++;
            tasks[index]->task.resume();
            std::cout << "Done!" << std::endl;
        }

        else if(choice == 3) {
            if(tasks.size() == 0) {
                std::cout << "Invalid" << std::endl;
                continue;
            }
            std::cout << "Tasks: " << tasks.size() << std::endl;
            for(int i = 0; i < tasks.size(); i++) {
                std::cout << i << ". " << tasks[i]->name << std::endl;
            }
            std::cout << "Destroy task #: ";
            std::cin >> index;
            if(index >= tasks.size()) {
                std::cout << "Invalid" << std::endl;
                continue;
            }
            tasks[index]->task.destroy();
            delete tasks[index];
            tasks.erase(tasks.begin()+index);
            std::cout << "Done!" << std::endl;
        }
    }

    return 0;
} 