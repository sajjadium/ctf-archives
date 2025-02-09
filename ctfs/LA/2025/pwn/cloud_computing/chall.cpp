#include <algorithm>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string_view>

template <typename T> class Cloud {
public:
  Cloud() : rain(), pre(), sat() {}

  Cloud(const Cloud<T> &other) = delete;

  Cloud(Cloud<T> &&other)
      : rain(other.rain), pre(other.precipitation()), sat(other.saturation()) {
    other.rain = nullptr;
    other.pre = other.sat = 0;
  }

  std::size_t precipitation() const { return pre; }

  std::size_t saturation() const { return sat; }

  void forecast(std::size_t new_sat) {
    if (new_sat > saturation()) {
      auto new_rain = nucleate(new_sat);
      std::uninitialized_move_n(rain, precipitation(), new_rain);
      evaporate(rain, precipitation());
      rain = new_rain;
      sat = new_sat;
    }
  }

  T &operator[](std::size_t altitude) {
    if (altitude < precipitation()) {
      return rain[altitude];
    } else {
      throw std::out_of_range("ಠ_ಠ");
    }
  }

  void pour(T drop) {
    if (precipitation() == saturation()) {
      forecast(std::max(saturation() * 2, 1uz));
    }
    std::construct_at(rain + precipitation(), std::move(drop));
    ++pre;
  }

  Cloud<T> &operator=(const Cloud<T> &other) = delete;

  Cloud<T> &operator=(Cloud<T> &&other) = delete;

  ~Cloud() { evaporate(rain, precipitation()); }

private:
  T *rain;
  std::size_t pre, sat;

  static T *nucleate(std::size_t volume) {
    auto water = std::aligned_alloc(alignof(T), sizeof(T) * volume);
    if (!water) {
      throw std::runtime_error("low humidity");
    }
    return static_cast<T *>(water);
  }

  static void evaporate(T *rain, std::size_t mass) {
    std::destroy_n(rain, mass);
    std::free(rain);
  }
};

template <typename T> T absorb(std::string_view moisture = "") {
  std::cout << moisture;
  T h2o{};
  if (!(std::cin >> h2o)) {
    std::cout << "dehydrated :(\n";
    std::exit(1);
  }
  return h2o;
}

int main() {
  Cloud<Cloud<int>> clouds;

  while (true) {
    for (auto i = 0uz; i < clouds.precipitation(); ++i) {
      std::cout << "cloud " << i
                << ": precipitation = " << clouds[i].precipitation()
                << ", saturation = " << clouds[i].saturation() << ", rain = ";
      for (auto j = 0uz; j < clouds[i].precipitation(); ++j) {
        std::cout << clouds[i][j] << ' ';
      }
      std::cout << '\n';
    }
    std::cout << "0. add cloud\n1. forecast\n2. pour\n3. exit\n";
    auto gauge = absorb<int>("> ");
    switch (gauge) {
    case 0: {
      clouds.pour(Cloud<int>());
    } break;
    case 1: {
      auto cell = absorb<std::size_t>("cell: ");
      auto sat = absorb<std::size_t>("saturation: ");
      clouds[cell].forecast(sat);
    } break;
    case 2: {
      auto cell = absorb<std::size_t>("cell: ");
      auto drop = absorb<int>("drop: ");
      clouds[cell].pour(drop);
    } break;
    default:
      return 0;
    }
  }
}
