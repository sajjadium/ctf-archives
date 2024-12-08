#include <iostream>
#include <cstring>
#include <map>

#define MAX_LOG_SIZE 10

class Log {
    private:
        int size;
        char logs[MAX_LOG_SIZE];

    public:
        Log() {
            size = 0;
            memset(logs, 0, MAX_LOG_SIZE);
        }

        int get_size() {
            return size;
        }

        void increase_size() {
            size++;
        }

        void add_cmd_to_log(const char* cmd) {
            strcat(logs, cmd);
        }

        void reset_log() {
            memset(logs, 0, MAX_LOG_SIZE);
            size = 0;
        }
};

enum TYPE {
    LONG,
    STRING
};

class Variable {
    public:
        TYPE type;
        union {
            long l;
            char* s;
        } value;
        
        Variable(long l) : type(LONG) {
            value.l = l;
        }

        Variable(const char* s) : type(STRING) {
            value.s = strdup(s);
        }

        virtual void print() {
            std::cout << "Default print" << std::endl;
        }
};

class longVariable : public Variable {
    public:
        longVariable(long l) : Variable(l) {}
        void print() override {
            std::cout << value.l << std::endl;
        }
};

class stringVariable : public Variable {
    public:
        stringVariable(const char* s) : Variable(s) {}
        void print() override {
            std::cout << value.s << std::endl;
        }
};

std::map<std::string, Variable*> variables;

void setvar(const char* name, const char* p) {
    char *strval;
    long longval = std::strtol(p + 1, &strval, 10);

    if (*strval) {
        variables[name] = new stringVariable(strval);
    } else {
        variables[name] = new longVariable(longval);
    }

    variables[name]->print();
}

Variable* getvarbyname(const char* name) {
    if (variables.find(name) != variables.end()) {
        return variables[name];
    } else {
        std::cout << "Variable not found" << std::endl;
        return 0;
    }
}

long getLongVar(const char* name) {
    Variable* v = getvarbyname(name);
    if (v->type == LONG) {
        return v->value.l;
    } else {
        std::cout << "Invalid variable " << name << ": " << v->value.s << std::endl;
        return 0;
    }
}

void process_arithmetic(char* cmd) {
    char *p = std::strchr(cmd, ')');

    if (!p) {
        std::cout << "Invalid command" << std::endl;
        return;
    }

    *p = 0;

    char *op = std::strchr(cmd, '+');
    long a, b;
    if (op) {
        *op = 0;
        a = getLongVar(cmd+1);
        b = getLongVar(op + 2);
        std::cout << a + b << std::endl;
    } else {
        op = std::strchr(cmd, '-');
        if (op) {
            *op = 0;
            a = getLongVar(cmd+1);
            b = getLongVar(op + 2);
            std::cout << a - b << std::endl;
        } else {
            op = std::strchr(cmd, '*');
            if (op) {
                *op = 0;
                a = getLongVar(cmd+1);
                b = getLongVar(op + 2);
                std::cout << a * b << std::endl;
            } else {
                op = std::strchr(cmd+1, '/');
                if (op) {
                    *op = 0;
                    a = getLongVar(cmd+1);
                    b = getLongVar(op + 2);
                    std::cout << a / b << std::endl;
                } else {
                    std::cout << "Invalid operation" << std::endl;
                }
            }
        }
    }
}

void win() {
    system("cat flag.txt");
    exit(0);
}

int main() {
    Log *log = new Log();
    log -> reset_log();
    variables = std::map<std::string, Variable*>();
    while (true) {
        std::cout << "> ";
        char cmd[20];
        std::cin >> cmd;

        if (cmd[0] == '$') {
            if (cmd[1] == '(' && cmd[2] == '(') {
                process_arithmetic(cmd + 3);
            } else {
                char* p = std::strchr(cmd, '=');
                if (p) {
                    *p = 0;
                    setvar(cmd + 1, p);
                } else {
                    Variable* c_v = getvarbyname(cmd + 1);
                    c_v -> print();
                }
            }
        } else if (!strcmp(cmd, "log")) {
            std::cout << "Creating new log" << std::endl;
            log = new Log();
        } else {
            std::cout << cmd << std::endl;
        }

        if (log->get_size() >= MAX_LOG_SIZE) {
            log->reset_log();
        }
        log->add_cmd_to_log(cmd);
        log->increase_size();
    }

    return 0;
}
