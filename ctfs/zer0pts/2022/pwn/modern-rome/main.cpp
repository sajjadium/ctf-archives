#include <string>
#include <iostream>

short buf[10];

void win() {
  std::system("/bin/sh");
}

short readroman(){
  short res = 0;
  std::string s;

  std::cin >> s;
  auto it = s.crbegin();

  int b = 1;
  for (auto c: "IXCM") {
    int cnt = 0;
    while (cnt < 9 && it != s.crend() && *it == c) {
      it++;
      cnt++;
    }
    res += b * cnt;
    b *= 10;
  }

  return res;
}

int main() {
  std::setbuf(stdin, NULL);
  std::setbuf(stdout, NULL);

  std::cout << "ind: ";
  int ind = readroman();
  std::cout << "val: ";
  int val = readroman();

  std::cout << "buf[" << ind << "] = " << val << std::endl;
  buf[ind] = val;

  std::exit(0);
}
