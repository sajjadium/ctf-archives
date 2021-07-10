#include <iostream>
#include <string>
#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>


class Food {
 public:
  Food(std::string name) : name_(std::move(name)) {}

  virtual void Eat() {
    std::cout << "om nom nom" << std::endl; 
  }

  void PrintName() {
    std::cout << "name: " << name_ << std::endl;
  }
 //private:
  std::string name_;
};

class Bamboo : public Food {
 public:
  Bamboo(const std::string&& name) : Food(std::move(name)) {}

  virtual void Eat() {
    std::cout << "crunch crunch" << std::endl;
  }
};

inline size_t get_idx() {
  size_t idx;

  std::cout << "idx: " << std::endl;
  std::cin >> idx;
  return idx;
}

uint64_t rand64() {
  uint64_t var = 0;
  static int ufd = open("/dev/urandom", O_RDONLY);

  if (read(ufd, &var, sizeof(var)) != sizeof(var)) {
    perror("ufd read");
    exit(1);
  }

  return var;
}

int main() {
  std::map<size_t, std::unique_ptr<Food>> foods;
  Food* favorite = nullptr;

  int choice;
  while (true) {
    std::cout << "choice: " << std::endl;
    std::cin >> choice;

    switch (choice) {
      case 0: {
        size_t idx = get_idx();

        std::unique_ptr<Food> tmp;
        std::string name;


        std::cout << "name: " << std::endl;
        std::cin >> name;

        if (name.length() > 0x1000) {
          std::cout << "too big :/" << std::endl;
          _Exit(1);
        } else {
          if (rand64() % 2 == 1) {
            tmp = std::make_unique<Bamboo>(std::move(name));
          } else {
            tmp = std::make_unique<Food>(std::move(name));
          }


          foods[idx] = std::move(tmp);
        }
        break;
      }
      case 1: {
        size_t idx = get_idx();

        favorite = foods[idx].get();
        break;
      }
      case 2: {
        if (favorite) favorite->PrintName();
        else std::cout << "set a favorite first!" << std::endl;
        break;
      }
      case 3: {
        char one_gadget_padding[0x100];
        memset(one_gadget_padding, 0, sizeof(one_gadget_padding));

        if (favorite) favorite->Eat();
        else std::cout << "set a favorite first!" << std::endl;
        break;
      }
      case 4: {
        _Exit(0);
        break;
      }
        
    }
  }
  
  return 0;
}


