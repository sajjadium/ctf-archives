#include <iostream>
#include <vector>
#include <cstring>

using namespace std;

template <typename T>
class Vector {
private:
    T* ptr;
    int len;
    int cap;
public:
    Vector(int sz) {
        ptr = new T[sz];
        cap = sz;
        len = 0;
    }

    void push_back(T val) {
        if (len == cap) {
            reallocate();
        }
        *(ptr + len) = val;
        len++;
    }

    void reallocate() {
        auto ncap = cap * 2;
        auto nptr = new T[ncap];
        memcpy(nptr, ptr, len * sizeof(T));
        delete []ptr;
        ptr = nptr;
        cap = ncap;
    }

    T& operator[](int index)
    {
        if (index >= len) {
            cout << "index out of bounds";
            exit(0);
        }
        return ptr[index];
    }

    void for_each() {
        for (int i = 0; i < len; i++) {
            cout << ptr[i];
        }
    }
};

void print_stats(string& str) {
    printf("Stats for string: %s\n", str.c_str());
    printf("size: %ld\n", sizeof(string));
    printf("0x00: %p\n", (void*) *(size_t*)((void*)&str));
    printf("0x08: %p\n", (void*) *(1 + (size_t*)((void*)&str)));
    printf("0x10: %p\n", (void*) *(2 + (size_t*)((void*)&str)));
    printf("0x18: %p\n", (void*) *(3 + (size_t*)((void*)&str)));
}

int get_index() {
    int idx;
    cout << "enter index: ";
    cin >> idx;
    return idx;
}

int main() {
    Vector<string> v(4);
    int opt;
    while (true) {
        cout << "1. add" << endl;
        cout << "2. read" << endl;
        cout << "3. edit" << endl;

        cout << ">";
        cin >> opt;

        switch (opt) {
            case 1:
                {
                    string str;
                    cout << "enter string: ";
                    cin >> str;
                    v.push_back(str);
                    break;
                }
            case 2:
                {
                    int idx = get_index();
                    cout << "v[" << idx << "]: ";
                    cout << v[idx] << endl;
                    break;
                }
            case 3:
                {
                    int idx = get_index();
                    cout << "enter string: ";
                    cin >> v[idx];
                    break;
                }
            case 1337:
                {
                    print_stats(v[get_index()]);
                    break;
                }
        }
    }
}
