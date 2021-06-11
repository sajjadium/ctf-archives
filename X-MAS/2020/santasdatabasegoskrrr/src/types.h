#pragma once

#include <string>
#include <stdexcept>
#include <vector>
#include <map>
#include <set>
#include <iostream>

enum ColumnType {
    NUMBER = 0xfffbeba, 
    STRING = 0xfffbebb, 
    BOOLEAN = 0xfffbebc, 
    ARRAY = 0xfffbebd, 
    CNULL = 0xfffbebe};

std::string ColTypeToStr(const ColumnType type) {
    switch (type) {
        case NUMBER:
            return "NUMBER";
            break;
        case STRING:
            return "STRING";
            break;
        case BOOLEAN:
            return "BOOLEAN";
            break;
        case ARRAY:
            return "ARRAY";
            break;
        case CNULL:
            return "CNULL";
            break;
    }
    return "UNKNOWN";
}

struct Column {
    std::string name;
    ColumnType type;
};

struct Value {
    void *data;
    ColumnType type;

    Value() {
        data=nullptr;
        type=CNULL;
    }

    Value(const Value& other) {
        *this = other;
        //std::cout << "copy " << data << std::endl;
    }

    Value& operator=(const Value& other) {
        type = other.type;
        if (type == NUMBER) {
            auto ptr = new long long int;
            *ptr = *static_cast<long long int*>(other.data);
            data = ptr;
        } else if (type == STRING) {
            auto ptr = new std::string;
            *ptr = *static_cast<std::string*>(other.data);
            data = ptr;
        } else if (type == BOOLEAN) {
            auto ptr = new bool;
            *ptr = *static_cast<bool*>(other.data);
            data = ptr;
        } else if (type == ARRAY) {

        }
        //std::cout << "copy " << data << std::endl;
        return *this;
    }

    Value(const ColumnType _type, void* _data) {
        type = _type;
        
        if (type == NUMBER) {
            auto ptr = new long long int;
            *ptr = *static_cast<long long int*>(_data);
            data = ptr;
        } else if (type == STRING) {
            auto ptr = new std::string;
            *ptr = *static_cast<std::string*>(_data);
            data = ptr;
        } else if (type == BOOLEAN) {
            auto ptr = new bool;
            *ptr = *static_cast<bool*>(_data);
            data = ptr;
        } else if (type == ARRAY) {

        }
        //std::cout << "alloc " << data << std::endl;
    }

    ~Value() {
        if (data==nullptr) return;
        //std::cout << "delete " << data << std::endl;
        if (type == NUMBER) {
            auto ptr = static_cast<long long int*>(data);
            delete ptr;
        } else if (type == STRING) {
            auto ptr = static_cast<std::string*>(data);
            delete ptr;
        } else if (type == BOOLEAN) {
            auto ptr = static_cast<bool*>(data);
            delete ptr;
        } else if (type == ARRAY) {

        };
    }

    bool operator<(const Value& rhs) const {
        if (type == CNULL || rhs.type == CNULL) return false;
        if (type != rhs.type) {
            throw std::logic_error("[Value] Invalid RHS value.");
        }

        if (data == NULL || rhs.data == NULL) {
            throw std::logic_error("[Value] NULL data pointer");
        }

        long long int num1, num2;
        std::string s1, s2;
        bool b1, b2;

        switch (type) {
            case NUMBER:
                {
                    num1 = *static_cast<long long int*>(data);
                    num2 = *static_cast<long long int*>(rhs.data);
                    return num1 < num2;
                    break;
                }
            case STRING:
                {
                    s1 = *static_cast<std::string*>(data);
                    s2 = *static_cast<std::string*>(rhs.data);
                    return s1 < s2;
                    break;
                }
            case BOOLEAN:
                {
                    b1 = *static_cast<bool*>(data);
                    b2 = *static_cast<bool*>(rhs.data);
                    return b1 < b2;
                    break;
                }
            case ARRAY:
                {
                    throw std::logic_error("[Value] Can't index on array.");
                    break;
                }
            default:
                throw std::logic_error("[Value] Unkown type.");
        }
        return false;
    }

    bool operator==(const Value& rhs) const {
        if (type == CNULL || rhs.type == CNULL) return false;
        if (type != rhs.type) {
            throw std::logic_error("[Value] Invalid RHS value.");
        }

        if (data == NULL || rhs.data == NULL) {
            throw std::logic_error("[Value] NULL data pointer");
        }

        long long int num1, num2;
        std::string s1, s2;
        bool b1, b2;

        switch (type) {
            case NUMBER:
                {
                    num1 = *static_cast<long long int*>(data);
                    num2 = *static_cast<long long int*>(rhs.data);
                    return num1 == num2;
                    break;
                }
            case STRING:
                {
                    s1 = *static_cast<std::string*>(data);
                    s2 = *static_cast<std::string*>(rhs.data);
                    return s1 == s2;
                    break;
                }
            case BOOLEAN:
                {
                    b1 = *static_cast<bool*>(data);
                    b2 = *static_cast<bool*>(rhs.data);
                    return b1 == b2;
                    break;
                }
            case ARRAY:
                {
                    throw std::logic_error("[Value] Can't index on array.");
                    break;
                }
            default:
                throw std::logic_error("[Value] Unkown type.");
        }
        return false;
    }
};

    std::ostream& operator<<(std::ostream& out, const Value& val) {
    if (val.type == NUMBER) {
        auto ptr = static_cast<long long int*>(val.data);
        out << (*ptr);
    } else if (val.type == STRING) {
        auto ptr = static_cast<std::string*>(val.data);
        out << (*ptr);
    } else if (val.type == BOOLEAN) {
        auto ptr = static_cast<bool*>(val.data);
        out << (*ptr);
    } else if (val.type == ARRAY) {

    };
    
    return out;
}

struct Row {
    unsigned int id;
    mutable std::vector<Value> values;

    bool operator<(const Row& rhs) const {
        return id < rhs.id;
    }
};

struct Index {
    std::multimap<Value, unsigned int> valueToId;    
};

struct Table {
    std::map<std::string, Column> columns;
    unsigned int rowIdSeq = 0;
    std::set<Row> rows;
    std::map<std::string, Index> indexes;
};

// CREATE TABLE ...
// CREATE ROW ...
// READ TABLE ...
// READ ROW ...
// UPDATE TABLE ...
// UPDATE ROW ...
// DELETE TABLE ...
// DELETE ROW ...

const std::string instructions[] = {"CREATE", "READ", "UPDATE", "DELETE", "SLEEP"};
const std::string targets[]  = {"TABLE", "ROW"};
const char pipe_sym = '|';
const char print_sym = '.';
const char print_pipe_sym = '&';
enum OutputType {FLUSH, REDIRECT, FLUSH_REDIRECT};

struct Command {
    std::string instruction;
    std::string target;
    std::map<std::string, std::string> arguments;
    OutputType output;
};