#include <cstdlib>
#include <variant>
#include <cstring>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fstream>
#include <memory>
#include "base64.h"

using namespace std;

#define MAX_DATA_SIZE 2000
#define T_INT 1
#define T_STR 2
#define H2C "env/connector/h2c"
#define C2H "env/connector/c2h"
#define N_MESSAGE MAX_DATA_SIZE
#define MESSAGE_FMT "%1999s"

typedef unsigned long long u64;

class StringData {
    private:
        char *str = nullptr;
        u64 length = 0;
    public:
        static void validate(char *line) {
            if (strlen(line) == 0) throw "empty";
            if (strlen(line) > MAX_DATA_SIZE) throw "too long";
        }
        explicit StringData(char *line) {
            str = line;
            length = strlen(str);
        }
        StringData(ifstream &ifs) {
            ifs >> length;
            char *b64_buf = (char *)malloc( 1 + (length+2)*2);
            ifs >> b64_buf;
            char *buf = (char *)malloc(length + 1);
            Base64decode(buf, b64_buf);
            buf[length] = 0;
            str = buf;
            free(b64_buf);
        }
        StringData (const StringData& data) = delete;
        StringData& operator=(const StringData& data) = delete;
        StringData (StringData&& data) {
            this->str = data.str;
            this->length = data.length;
            data.str = nullptr;
            data.length = 0;
        }
        StringData& operator=(StringData&& data) {
            char *tmp = this->str;
            this->str = data.str;
            this->length = data.length;
            data.str = nullptr;
            data.length = 0;
            free(tmp);
            return *this;
        }
        ~StringData() {
            free(str);
        }
        void encode_packet(ofstream &ofs) {
            ofs << T_STR << endl;
            ofs << length << endl;
            char *buf = (char *)malloc(1 + (length+2)*2);
            Base64encode(buf, str, length);
            ofs << buf << endl;
            free(buf);
        }
        void print_data() {
            printf("string: %s", str);
        }
};

class IntData {
    private:
        u64 val = 0;
    public:
        static void validate(char *line) {
            if (strlen(line) == 0) throw "empty";
            if (strlen(line) > MAX_DATA_SIZE) throw "too long";
            u64 idx = 0;
            while (line[idx]) {
                char c = line[idx++];
                if ('0' > c || '9' < c) throw "invalid data";
            }
        }
        IntData(u64 x) {
            val = x;
        }
        IntData(char *line) {
            val = stoull(line);
            free(line);
        }
        IntData(ifstream &ifs) {
            ifs >> val;
        }
        IntData (const IntData&) = default;
        IntData& operator=(char *line) {
            val = stoull(line);
            free(line);
            return *this;
        }
        IntData& operator=(const IntData& x) {
            this->val = x.val;
            return *this;
        }
        IntData (IntData&& x) {
            this->val = x.val;
        }
        void encode_packet(ofstream &ofs) {
            ofs << T_INT << endl;
            ofs << val << endl;
        }
        void print_data() {
            printf("number: %llu", val);
        }
};

class Client {
    protected:
        ifstream reader;
        ofstream writer;
    public:
        variant<IntData, StringData> data {0xcafe};
        Client() {
            mkfifo(H2C, 0666);
            mkfifo(C2H, 0666);
            writer.rdbuf()->pubsetbuf(0, 0);
            reader.rdbuf()->pubsetbuf(0, 0);
        }
        ~Client(){
            // remove named pipe
            remove(H2C);
            remove(C2H);
        }
        bool receive_data() {
            int type;

            reader >> type;

            if (type == T_INT) {
                data = IntData(reader);
            } else if (type == T_STR) {
                data = StringData(reader);
            } else {
                return false;
            }
            return true;
        }
        void send_data() {
            visit([&](auto &v) {
                    v.encode_packet(writer);
                    }, data);
        }
        void set_int_data(char *line) {
            IntData::validate(line);
            data = line;
        }
        void set_str_data(char *line) {
            StringData::validate(line);
            data = StringData(line);
        }
        virtual char *initialize(char message_to_be_sent[N_MESSAGE]) {
            char message[N_MESSAGE] = {};
            reader.open(H2C, ios::in);
            writer.open(C2H, ios::out);
            writer.rdbuf()->pubsetbuf(0, 0);
            reader.rdbuf()->pubsetbuf(0, 0);
            if (!reader || !writer) return NULL;
            puts("connected...");
            reader >> message;
            writer << message_to_be_sent << endl;
            return strdup(message);
        }
};

class Host : public Client {
    public:
        char *initialize(char message_to_be_sent[N_MESSAGE]) override {
            char message[N_MESSAGE] = {};
            writer.open(H2C, ios::out);
            reader.open(C2H, ios::in);
            if (!reader || !writer) return NULL;
            puts("connected...");
            writer << message_to_be_sent << endl;
            reader >> message;
            return strdup(message);
        }
};

void set_handler(unique_ptr<Client>& c) {
    char type[8] = {};
    char *data = nullptr;
    printf("type[int/str] >");
    if (scanf("%4s", type) != 1) {
        puts("invalid type");
        return;
    }
    printf("data >");
    if (scanf("%2000ms", &data) != 1) {
        puts("invalid data");
        return;
    }
    try {
        if (strcmp(type, "int") == 0) {
            c->set_int_data(data);
        } else if (strcmp(type, "str") == 0) {
            c->set_str_data(data);
        } else {
            puts("wrong type");
            free(data);
        }
    } catch (...) {
        puts("invalid data");
    }
}

void send_handler(unique_ptr<Client>& c) {
    puts("transferring your message...");
    c->send_data();
}

void receive_handler(unique_ptr<Client>& c) {
    puts("waiting...");
    auto ret = c->receive_data();
    if (ret) {
        visit([&](auto &v) {
                printf("> ");
                v.print_data();
                }, c->data);
        puts("");
    } else {
        puts("connection broken");
    }
}

void main_loop(unique_ptr<Client> client) {
    char name[N_MESSAGE] = {};

    printf("what's your name? >");
    if (scanf(MESSAGE_FMT, name) != 1) return;

    char *opponent_name = client->initialize(name);
    if (opponent_name == NULL) {
        puts("failed to initalize the connection");
        return;
    }
    printf("The opponent is %s\n", opponent_name);

    int x = 0;
    while (1) {
        puts("Menu");
        puts("1. set data");
        puts("2. send data");
        puts("3. receive data");
        puts("4. bye");
        printf("> ");
        if (scanf("%d", &x) != 1) return;
        switch (x) {
            case 1:
                set_handler(client);
                break;
            case 2:
                send_handler(client);
                break;
            case 3:
                receive_handler(client);
                break;
            default:
                puts("bye");
                return;
        }
    }
}
