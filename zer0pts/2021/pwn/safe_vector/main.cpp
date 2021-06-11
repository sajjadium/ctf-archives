#include <iostream>
#include <vector>

template<typename T>
class safe_vector: public std::vector<T> {
public:
  void wipe() {
    std::vector<T>::resize(0);
    std::vector<T>::shrink_to_fit();
  }

  T& operator[](int index) {
    int size = std::vector<T>::size();
    if (size == 0) {
      throw "index out of bounds";
    }
    return std::vector<T>::operator[](index % size);
  }
};

using namespace std;

int menu() {
  int choice;
  cout << "1. push_back" << endl
       << "2. pop_back" << endl
       << "3. store" << endl
       << "4. load" << endl
       << "5. wipe" << endl
       << ">> ";
  cin >> choice;
  return choice;
}

int main() {
  safe_vector<uint32_t> arr;

  do {
    switch(menu()) {
    case 1:
      {
        int v;
        cout << "value: ";
        cin >> v;
        arr.push_back(v);
        break;
      }
    case 2:
      {
        arr.pop_back();
        cout << "popped" << endl;
        break;
      }
    case 3:
      {
        int i, v;
        cout << "index: ";
        cin >> i;
        cout << "value: ";
        cin >> v;
        arr[i] = v;
        break;
      }
    case 4:
      {
        int i;
        cout << "index: ";
        cin >> i;
        cout << "value: " << arr[i] << endl;
        break;
      }
    case 5:
      {
        arr.wipe();
        cout << "wiped" << endl;
        break;
      }
    default:
      return 0;
    }
  } while (cin.good());
  return 0;
}

__attribute__((constructor))
void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}
