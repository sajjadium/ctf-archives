#include <emmintrin.h>
#include <fcntl.h>
#include <inttypes.h>
#include <malloc.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <algorithm>
#include <atomic>
#include <condition_variable>
#include <functional>
#include <limits>
#include <list>
#include <map>
#include <memory>
#include <mutex>
#include <optional>
#include <set>
#include <shared_mutex>
#include <span>
#include <string>
#include <string_view>
#include <thread>
#include <tuple>
#include <variant>
#include <vector>

#define CHECK(condition)                                              \
  do {                                                                \
    if (!(condition)) {                                               \
      CheckFailure("Check failed at %s:%d: %s\n", __FILE__, __LINE__, \
                   #condition);                                       \
    }                                                                 \
  } while (0);

#define PCHECK(condition)                                                  \
  do {                                                                     \
    if (!(condition)) {                                                    \
      CheckFailure("Check failed at %s:%d (%m): %s\n", __FILE__, __LINE__, \
                   #condition);                                            \
    }                                                                      \
  } while (0);

void CheckFailure(const char* format, ...) {
  // asm("int3");
  va_list ap;
  va_start(ap, format);
  vfprintf(stderr, format, ap);
  va_end(ap);
  abort();
}

template <typename Fn, typename... Args>
auto HandleEINTR(Fn fn, Args... args) -> decltype(fn(args...)) {
  decltype(fn(args...)) result;
  errno = 0;
  do {
    result = fn(args...);
  } while (result == -1 && errno == EINTR);
  return result;
}

ssize_t ReadLen(int fd, void* buf, size_t n) {
  uint8_t* ptr = reinterpret_cast<uint8_t*>(buf);
  ssize_t nread = 0;
  while (nread < n) {
    const ssize_t rc = HandleEINTR(read, fd, ptr + nread, n - nread);
    if (rc < 0) {
      return rc;
    }
    if (rc == 0) {
      break;
    }
    nread += rc;
  }
  return nread;
}

ssize_t WriteLen(int fd, const void* buf, size_t n) {
  const uint8_t* ptr = reinterpret_cast<const uint8_t*>(buf);
  ssize_t nwritten = 0;
  while (nwritten < n) {
    const ssize_t rc = HandleEINTR(write, fd, ptr + nwritten, n - nwritten);
    if (rc < 0) {
      return rc;
    }
    nwritten += rc;
  }
  return nwritten;
}

using SequenceNumber = uint64_t;
constexpr SequenceNumber kMaxSequenceNumber =
    std::numeric_limits<SequenceNumber>::max();

template <typename T>
class Pool {
 public:
  class Deleter {
   public:
    void operator()(T* obj) const { pool_.Release(obj); }
  };

  static Pool<T>& Get() { return pool_; }

  using Ptr = std::unique_ptr<T, Deleter>;

  Ptr Allocate() {
    if (size_ > 0) {
      CHECK(size_ < kMaxSize);
      --size_;
      T* obj = items_[size_];
      CHECK(obj != nullptr);
      return Ptr(obj, Deleter());
    }
    return Ptr(new T, Deleter());
  }

 private:
  void Release(T* obj) { items_[size_++] = obj; }

  static thread_local Pool<T> pool_;
  static constexpr size_t kMaxSize = 256;

  size_t size_ = 0;
  T* items_[kMaxSize] = {nullptr};
};

struct Vec2 {
  double x;
  double y;
};

struct Vec3 {
  double x;
  double y;
  double z;
};

struct Quaternion {
  double a;
  double b;
  double c;
  double d;
};

template <class... Ts>
struct overloaded : Ts... {
  using Ts::operator()...;
};
template <class... Ts>
overloaded(Ts...) -> overloaded<Ts...>;

using Value = std::variant<std::monostate, std::string_view, uint32_t, uint64_t,
                           Vec2, Vec3, Quaternion>;
using OwnedValue = std::variant<std::monostate, std::string, uint32_t, uint64_t,
                                Vec2, Vec3, Quaternion>;

OwnedValue ToOwned(const Value& value) {
  return std::visit(overloaded{[](std::string_view v) -> OwnedValue {
                                 return std::string(v);
                               },
                               [](const auto& v) -> OwnedValue { return v; }},
                    value);
}

Value ToUnowned(const OwnedValue& value) {
  return std::visit(overloaded{[](const auto& v) -> Value { return v; }},
                    value);
}

std::string VStrFormat(const char* format, va_list ap) {
  char* buf = nullptr;
  CHECK(vasprintf(&buf, format, ap) != -1);

  std::unique_ptr<char, decltype(free)*> deleter(buf, free);
  return std::string(buf);
}

std::string StrFormat(const char* format, ...) {
  va_list ap;
  va_start(ap, format);
  std::string result = VStrFormat(format, ap);
  va_end(ap);
  return result;
}

std::string DebugString(const Value& value) {
  return std::visit(
      overloaded{
          [](std::monostate) -> std::string { return "(null)"; },
          [](std::string_view v) { return StrFormat("\"%s\"", v.data()); },
          [](uint32_t v) { return StrFormat("u32(%" PRIu32 ")", v); },
          [](uint64_t v) { return StrFormat("u64(%" PRIu64 ")", v); },
          [](const Vec2 v) { return StrFormat("Vec2(%g, %g)", v.x, v.y); },
          [](const Vec3 v) {
            return StrFormat("Vec2(%g, %g, %g)", v.x, v.y, v.z);
          },
          [](const Quaternion v) {
            return StrFormat("Quaternion(%g, %g, %g, %g)", v.a, v.b, v.c, v.d);
          },
      },
      value);
}

struct Version {
  Value value;
  SequenceNumber seq = 0;
};

template <typename T>
thread_local Pool<T> Pool<T>::pool_;

using VersionPtr = Pool<Version>::Ptr;
using VersionList = std::vector<VersionPtr>;

class Arena {
 public:
  char* Allocate(size_t n) {
    char* ptr = nullptr;
    if (n > kDefaultBlockSize) {
      blocks_.emplace_back(n);
      ptr = blocks_.back().Allocate(n);
      CHECK(ptr != nullptr);
      return ptr;
    }

    if (!blocks_.empty()) {
      ptr = blocks_.front().Allocate(n);
      if (ptr != nullptr) {
        return ptr;
      }
    }

    blocks_.emplace_front(kDefaultBlockSize);
    ptr = blocks_.front().Allocate(n);
    CHECK(ptr != nullptr);
    return ptr;
  }

 private:
  static constexpr size_t kDefaultBlockSize = 4096;

  class Block {
   public:
    explicit Block(size_t size)
        : data_(new char[size]), ptr_(data_.get()), remaining_(size) {}

    Block(Block&&) = default;
    Block& operator=(Block&&) = default;

    char* Allocate(size_t n) {
      if (remaining_ < n) {
        return nullptr;
      }
      char* ptr = ptr_;
      ptr_ += n;
      remaining_ -= n;
      return ptr;
    }

   private:
    std::unique_ptr<char[]> data_;
    char* ptr_;
    size_t remaining_;
  };

  std::list<Block> blocks_;
};

class Layer {
 public:
  using Id = uint64_t;
  explicit Layer(Id id) : id_(id) {}

  void Set(std::string_view key, Value value, SequenceNumber seq) {
    std::unique_lock l(mu_);
    CHECK(!sealed_);
    VersionList* version_list;
    auto it = map_.find(key);
    if (it != map_.end()) {
      version_list = &it->second;
    } else {
      version_list = &map_[ArenaString(key)];
    }

    auto version = Pool<Version>::Get().Allocate();
    version->seq = seq;
    version->value = std::visit(
        overloaded{
            [&](std::string_view v) -> Value { return ArenaString(v); },
            [](const auto& v) -> Value { return v; },
        },
        value);

    version_list->push_back(std::move(version));
  }

  const Version* Read(std::string_view key, SequenceNumber seq) {
    std::shared_lock l(mu_);
    const auto it = map_.find(key);
    if (it == map_.end()) {
      return nullptr;
    }
    const auto& versions = it->second;
    auto version_it =
        std::upper_bound(versions.begin(), versions.end(), seq,
                         [](SequenceNumber seq, const VersionPtr& version) {
                           return seq < version->seq;
                         });
    if (version_it == versions.begin()) {
      return nullptr;
    }
    --version_it;
    return version_it->get();
  }

  using Iterator = std::map<std::string_view, VersionList>::const_iterator;

  Iterator begin() const {
    std::shared_lock l(mu_);
    CHECK(sealed_);
    return map_.cbegin();
  }

  Iterator end() const {
    std::shared_lock l(mu_);
    CHECK(sealed_);
    return map_.cend();
  }

  bool empty() const {
    std::shared_lock l(mu_);
    CHECK(sealed_);
    return map_.empty();
  }

  void Seal() {
    std::unique_lock l(mu_);
    CHECK(!sealed_);
    sealed_ = true;
  }

  Id id() const { return id_; }

 private:
  std::string_view ArenaString(std::string_view str) {
    char* ptr = arena_.Allocate(str.size() + 1);
    memcpy(ptr, str.data(), str.size());
    return std::string_view(ptr, str.size());
  }

  const Id id_;

  mutable std::shared_mutex mu_;
  bool sealed_ = false;
  Arena arena_;
  std::map<std::string_view, VersionList> map_;
};

class LayerStack {
 public:
  LayerStack() {}
  ~LayerStack() {}

  void AddLayer(std::shared_ptr<Layer> layer) {
    layers_.push_back(std::move(layer));
  }

  const Version* Read(std::string_view key, SequenceNumber seq) {
    const Version* result = nullptr;
    for (const auto& layer : layers_) {
      const Version* version = layer->Read(key, seq);
      if (version == nullptr) {
        continue;
      }
      if (version->seq > seq) {
        break;
      }
      result = std::move(version);
    }
    return result;
  }

  void Iterate(const std::function<void(
                   std::string_view, std::span<const Version*> versions)>& fn) {
    std::vector<Layer::Iterator> iterators;
    std::vector<size_t> min_heap;
    for (size_t i = 0; i < layers_.size(); ++i) {
      const auto& layer = *layers_[i];
      if (layer.begin() == layer.end()) {
        continue;
      }
      iterators.push_back(layer.begin());
      min_heap.push_back(i);
    }

    const auto comparator_gt = [&](size_t a, size_t b) {
      const auto it_a = iterators[a];
      const auto it_b = iterators[b];
      return std::tie(it_a->first, a) > std::tie(it_b->first, b);
    };

    std::make_heap(min_heap.begin(), min_heap.end(), comparator_gt);

    while (!min_heap.empty()) {
      std::string_view key;
      std::vector<const Version*> versions;

      while (true) {
        const size_t idx = min_heap.front();
        auto& it = iterators[idx];
        key = it->first;
        const auto& version_list = it->second;
        for (const auto& version : version_list) {
          versions.push_back(version.get());
        }

        std::pop_heap(min_heap.begin(), min_heap.end(), comparator_gt);

        ++it;
        if (it == layers_[idx]->end()) {
          if (min_heap.size() == 1) {
            return;
          }
          min_heap.pop_back();
        } else {
          std::push_heap(min_heap.begin(), min_heap.end(), comparator_gt);
        }

        if (iterators[min_heap.front()]->first != key) {
          break;
        }
      }

      fn(key, {versions.begin(), versions.end()});
    }
  }

  Layer* mutable_layer() const {
    return layers_.empty() ? nullptr : layers_.back().get();
  }
  std::span<const std::shared_ptr<Layer>> layers() const {
    return {layers_.begin(), layers_.end()};
  }

 private:
  std::vector<std::shared_ptr<Layer>> layers_;
};

class Transaction;
class LockManager {
 private:
  struct LockState {
    // Protected by `LockManager::mu_`.
    size_t num_waiters = 0;
    Transaction* holder = nullptr;
    std::condition_variable cond_var;
  };
  using LockMap =
      std::map<std::string, std::unique_ptr<LockState>, std::less<>>;

 public:
  using LockHandle = LockMap::iterator;

  std::optional<LockHandle> Lock(Transaction* transaction,
                                 std::string_view key) {
    std::unique_lock l(mu_);
    auto it = map_.find(key);
    if (it == map_.end()) {
      it = map_.try_emplace(std::string(key), std::make_unique<LockState>())
               .first;
    }

    auto& state = it->second;
    if (state->holder == transaction) {
      return std::nullopt;
    }
    ++state->num_waiters;
    state->cond_var.wait(l, [&] { return state->holder == nullptr; });
    state->holder = transaction;
    --state->num_waiters;
    return it;
  }

  void Unlock(Transaction* transaction, LockHandle handle) {
    std::unique_lock l(mu_);
    auto& state = handle->second;
    CHECK(state->holder == transaction);
    if (state->num_waiters == 0) {
      map_.erase(handle);
      return;
    }

    state->holder = nullptr;
    l.unlock();
    state->cond_var.notify_one();
  }

  std::mutex mu_;
  LockMap map_;
};

using MutationList = std::map<std::string, OwnedValue, std::less<>>;

enum LogLevel : uint8_t {
  kDebug,
  kInfo,
  kError,
};

class Table {
 public:
  static constexpr std::string_view kInternalKeyPrefix = "_";
  static constexpr std::string_view kGcWatermarkKey = "_gc_watermark";

  Table() : layer_stack_(std::make_shared<LayerStack>()) { NewMutableLayer(); }

  std::shared_ptr<LayerStack> layer_stack() const {
    std::shared_lock l(mu_);
    return layer_stack_;
  }

  LockManager* lock_manager() { return &lock_manager_; }

  struct ReadResult {
    const Version* version = nullptr;
    std::shared_ptr<LayerStack> layer_stack;
    std::string_view error;
  };
  ReadResult Read(std::string_view key,
                  SequenceNumber seq = kMaxSequenceNumber) const {
    std::shared_ptr<LayerStack> layer_stack;
    {
      std::shared_lock l(mu_);
      if (seq < gc_watermark_) {
        return {.error = "Requested sequence below GC watermark"};
      }
      layer_stack = layer_stack_;
    }

    return ReadResult{
        .version = layer_stack->Read(key, seq),
        .layer_stack = std::move(layer_stack),
    };
  }

  SequenceNumber Apply(const MutationList& mutations) {
    std::unique_lock l(mu_);
    const SequenceNumber seq = next_seq_++;
    for (const auto& [key, value] : mutations) {
      if (key == kGcWatermarkKey) {
        CHECK(std::holds_alternative<SequenceNumber>(value));
        gc_watermark_ = std::clamp(std::get<SequenceNumber>(value),
                                   gc_watermark_, next_seq_ - 1);
      }
      layer_stack_->mutable_layer()->Set(key, ToUnowned(value), seq);
    }
    return seq;
  }

  Layer::Id NewMutableLayer() {
    std::unique_lock l(mu_);
    if (layer_stack_->mutable_layer() != nullptr) {
      layer_stack_->mutable_layer()->Seal();
    }
    auto new_stack = std::make_shared<LayerStack>();
    for (const auto& layer : layer_stack_->layers()) {
      new_stack->AddLayer(layer);
    }
    const Layer::Id id = next_layer_id_++;
    new_stack->AddLayer(std::make_shared<Layer>(id));
    layer_stack_ = std::move(new_stack);
    return id;
  }

  void Compact(Layer::Id start, Layer::Id limit) {
    std::unique_lock l(mu_);
    limit = std::min(limit, layer_stack_->mutable_layer()->id());
    if (start >= limit) {
      return;
    }

    auto it = compacting_.lower_bound(start);
    if (it != compacting_.end() && *it < limit) {
      return;
    }

    const SequenceNumber gc_watermark = start == 0 ? gc_watermark_ : 0;

    LayerStack compaction_stack;
    for (const auto& layer : layer_stack_->layers()) {
      if (layer->id() >= start && layer->id() < limit) {
        CHECK(layer.get() != layer_stack_->mutable_layer());
        compaction_stack.AddLayer(layer);
        compacting_.insert(layer->id());
      }
    }

    l.unlock();

    auto new_layer = std::make_shared<Layer>(start);
    compaction_stack.Iterate(
        [&](std::string_view key, std::span<const Version*> versions) {
          size_t first_live = 0;
          for (size_t i = 0; i < versions.size(); ++i) {
            const auto& version = *versions[i];
            if (std::holds_alternative<std::monostate>(version.value) &&
                version.seq <= gc_watermark) {
              first_live = i + 1;
            }
          }
          versions = versions.subspan(first_live);

          SequenceNumber prev_seq = 0;
          for (const Version* version : versions) {
            new_layer->Set(key, version->value, version->seq);
            CHECK(prev_seq <= version->seq);
            prev_seq = version->seq;
          }
        });
    new_layer->Seal();

    if (new_layer->empty()) {
      new_layer = nullptr;
    }

    l.lock();

    auto new_stack = std::make_shared<LayerStack>();
    for (const auto& layer : layer_stack_->layers()) {
      if (layer->id() < start || layer->id() >= limit) {
        new_stack->AddLayer(layer);
      } else if (new_layer != nullptr) {
        new_stack->AddLayer(std::move(new_layer));
      }
    }

    it = compacting_.lower_bound(start);
    while (it != compacting_.end() && *it < limit) {
      it = compacting_.erase(it);
    }
    layer_stack_ = std::move(new_stack);
  }

 private:
  mutable std::shared_mutex mu_;
  Layer::Id next_layer_id_ = 0;

  SequenceNumber next_seq_ = 1;
  SequenceNumber gc_watermark_ = 0;

  std::shared_ptr<LayerStack> layer_stack_;
  std::set<Layer::Id> compacting_;

  LockManager lock_manager_;
};

class SpinLock {
 public:
  void lock() {
    while (true) {
      if (!lock_.exchange(true, std::memory_order_acquire)) {
        return;
      }
      while (lock_.load(std::memory_order_relaxed)) {
        _mm_pause();
      }
    }
  }

  bool try_lock() {
    return !lock_.load(std::memory_order_relaxed) &&
           !lock_.exchange(true, std::memory_order_acquire);
  }

  void unlock() { lock_.store(false, std::memory_order_release); }

 private:
  std::atomic<bool> lock_{false};
};

class Tracer {
 public:
  void Trace(const char* format, ...) {
    std::unique_lock l(mu_);
    if (!enabled_) {
      return;
    }

    va_list ap;
    va_start(ap, format);
    buffer_.append(VStrFormat(format, ap));
    va_end(ap);

    buffer_.append("\n");
  }

  void set_enabled(bool value) {
    std::unique_lock l(mu_);
    enabled_ = value;
    if (!enabled_) {
      buffer_.clear();
    }
  }

  std::string Flush() {
    std::unique_lock l(mu_);
    std::string trace;
    trace.swap(buffer_);
    return trace;
  }

 private:
  SpinLock mu_;
  bool enabled_ = false;
  std::string buffer_;
};

class Transaction {
 public:
  using Id = uint64_t;
  static constexpr Id kInvalidId = 0;
  static constexpr Id kSystemId = std::numeric_limits<Id>::max();

  Transaction(Id id, Table* table, Tracer* tracer)
      : id_(id), table_(table), tracer_(tracer) {}
  ~Transaction() { CHECK(locks_.empty()); }

  Table::ReadResult Read(std::string_view key) {
    {
      std::unique_lock l(mu_);
      if (finished_) {
        return {.error = "Transaction finished"};
      }
      ++num_active_requests_;
    }

    Trace("Locking %s", key.data());
    Lock(key);
    Table::ReadResult result = table_->Read(key, kMaxSequenceNumber);

    bool notify = false;
    {
      std::unique_lock l(mu_);
      CHECK(!finished_);
      --num_active_requests_;
      notify = num_active_requests_ == 0;
    }

    if (notify) {
      cond_var_.notify_all();
    }

    return result;
  }

  void BufferMutation(std::string_view key, OwnedValue value) {
    if (auto it = mutations_.find(key); it != mutations_.end()) {
      it->second = std::move(value);
    } else {
      mutations_[std::string(key)] = std::move(value);
    }
  }

  SequenceNumber Commit() {
    Trace("Commiting %" PRIu64, id_);
    {
      std::unique_lock l(mu_);
      if (finished_) {
        return kMaxSequenceNumber;
      }

      cond_var_.wait(l, [&] { return num_active_requests_ == 0; });
      finished_ = true;
    }

    for (const auto& [key, _] : mutations_) {
      Lock(key);
    }
    const SequenceNumber seq = table_->Apply(mutations_);
    UnlockAll();
    return seq;
  }

  bool Abort() {
    {
      std::unique_lock l(mu_);
      if (finished_) {
        return false;
      }

      cond_var_.wait(l, [&] { return num_active_requests_ == 0; });
      finished_ = true;
    }

    UnlockAll();
    return true;
  }

  template <typename... Args>
  void Trace(Args&&... args) {
    tracer_->Trace(std::forward<Args>(args)...);
  }

 private:
  void Lock(std::string_view key) {
    auto lock_handle = table_->lock_manager()->Lock(this, key);
    if (lock_handle.has_value()) {
      locks_.push_back(*lock_handle);
    }
  }

  void UnlockAll() {
    for (const auto& lock_handle : locks_) {
      table_->lock_manager()->Unlock(this, lock_handle);
    }
    locks_.clear();
  }

  const Id id_;
  Table* const table_;
  MutationList mutations_;
  std::vector<LockManager::LockHandle> locks_;

  std::mutex mu_;
  std::condition_variable cond_var_;
  bool finished_ = false;
  size_t num_active_requests_ = 0;

  Tracer* const tracer_;
};

class Session {
 public:
  Session(Table* table) : table_(table) {}
  template <typename T, std::enable_if_t<
                            std::is_arithmetic_v<std::conditional_t<
                                std::is_enum_v<T>, std::underlying_type<T>, T>>,
                            bool> = true>
  void Read(T* value) {
    CHECK(ReadLen(0, value, sizeof(*value)) == sizeof(*value));
  }

  void Read(std::string* str) {
    uint16_t size;
    Read(&size);
    str->resize(size);
    if (size > 0) {
      CHECK(ReadLen(0, str->data(), size) == size);
    }
  }

  void Read(Vec2* v) {
    Read(&v->x);
    Read(&v->y);
  }

  void Read(Vec3* v) {
    Read(&v->x);
    Read(&v->y);
    Read(&v->z);
  }

  void Read(Quaternion* v) {
    Read(&v->a);
    Read(&v->b);
    Read(&v->c);
    Read(&v->d);
  }

  void Read(OwnedValue* value) {
    uint8_t tag;
    Read(&tag);
    CHECK(tag < std::variant_size_v<Value>);
    switch (tag) {
      case 0: {
        *value = OwnedValue();
        return;
      }
#define HANDLE(tag)               \
  case tag: {                     \
    Read(&value->emplace<tag>()); \
    return;                       \
  }
        HANDLE(1)
        HANDLE(2)
        HANDLE(3)
        HANDLE(4)
        HANDLE(5)
        HANDLE(6)
        static_assert(std::variant_size_v<Value> == 7);
#undef HANDLE
    }
  }

  class IOLock {
   public:
    explicit IOLock(Session* session) : lock_(session->io_mu_) {}

   private:
    std::unique_lock<std::mutex> lock_;
  };

  template <typename T, std::enable_if_t<
                            std::is_arithmetic_v<std::conditional_t<
                                std::is_enum_v<T>, std::underlying_type<T>, T>>,
                            bool> = true>
  void Write(T value) {
    CHECK(WriteLen(1, &value, sizeof(value)) == sizeof(value));
  }

  void Write(std::string_view value) {
    CHECK(value.size() <= std::numeric_limits<uint16_t>::max());
    Write<uint16_t>(value.size());
    if (!value.empty()) {
      CHECK(WriteLen(1, value.data(), value.size()) == value.size());
    }
  }

  void Write(const Vec2& v) {
    Write(v.x);
    Write(v.y);
  }

  void Write(const Vec3& v) {
    Write(v.x);
    Write(v.y);
    Write(v.z);
  }

  void Write(const Quaternion& v) {
    Write(v.a);
    Write(v.b);
    Write(v.c);
    Write(v.d);
  }

  void Write(const Value& value) {
    static_assert(std::variant_size_v<Value> <=
                  std::numeric_limits<uint8_t>::max());
    Write<uint8_t>(value.index());
    std::visit(overloaded{
                   [](std::monostate) {},
                   [&](const auto& v) { Write(v); },
               },
               value);
  }

  Table* table() const { return table_; }

  std::shared_ptr<Transaction> FindTransaction(Transaction::Id tid) {
    if (tid == Transaction::kSystemId) {
      return nullptr;
    }

    std::shared_lock l(transactions_mu_);
    auto it = transactions_.find(tid);
    if (it == transactions_.end()) {
      return nullptr;
    }
    return it->second;
  }

  Transaction::Id CreateTransaction() {
    std::unique_lock l(transactions_mu_);
    const Transaction::Id tid = next_tid_++;
    auto transaction = std::make_shared<Transaction>(tid, table_, &tracer_);
    transactions_[tid] = std::move(transaction);
    return tid;
  }

  void RemoveTransaction(Transaction::Id tid) {
    std::unique_lock l(transactions_mu_);
    transactions_.erase(tid);
  }

  Tracer* tracer() { return &tracer_; }

 private:
  // Serializes socket reads/writes.
  std::mutex io_mu_;

  Table* const table_;

  std::shared_mutex transactions_mu_;
  Transaction::Id next_tid_ = 1;
  std::map<Transaction::Id, std::shared_ptr<Transaction>> transactions_;

  Tracer tracer_;
};

class CommandHandler {
 public:
  explicit CommandHandler(Session* session) : session_(session) {}
  virtual ~CommandHandler() {}
  virtual void ReadRequest() = 0;
  virtual void Run() = 0;

  template <typename... Args>
  void Trace(Args&&... args) {
    session_->tracer()->Trace(std::forward<Args>(args)...);
  }

  using RequestId = uint64_t;

 protected:
  Session* session_;
};

class ReadHandler : public CommandHandler {
 public:
  explicit ReadHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override {
    session_->Read(&request_id_);
    session_->Read(&tid_);
    session_->Read(&seq_);
    session_->Read(&key_);
  }

  void Run() override {
    if (tid_ != Transaction::kInvalidId) {
      transaction_ = session_->FindTransaction(tid_);
      if (transaction_ == nullptr) {
        ReturnError("Transaction not found");
        return;
      }

      if (seq_ != kMaxSequenceNumber) {
        ReturnError("Invalid sequence number for transactional read");
        return;
      }

      const Table::ReadResult result = transaction_->Read(key_);
      TraceResult(result);
      ReturnResult(result);
      return;
    }

    const Table::ReadResult result = session_->table()->Read(key_);
    TraceResult(result);
    ReturnResult(result);
  }

 private:
  void TraceResult(const Table::ReadResult& result) {
    if (!result.error.empty()) {
      Trace("Read %s failed: %s", key_.c_str(), result.error.data());
      return;
    }
    Trace(
        "Read %s -> %s", key_.c_str(),
        DebugString(result.version == nullptr ? Value() : result.version->value)
            .c_str());
  }

  void ReturnResult(const Table::ReadResult& result) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(result.error);
    session_->Write(result.version == nullptr ? Value()
                                              : result.version->value);
  }

  void ReturnError(std::string_view error) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(error);
    session_->Write(Value());
  }

 private:
  RequestId request_id_;
  Transaction::Id tid_;
  SequenceNumber seq_;
  std::string key_;

  std::shared_ptr<Transaction> transaction_;
};

class BeginTransactionHandler : public CommandHandler {
 public:
  explicit BeginTransactionHandler(Session* session)
      : CommandHandler(session) {}

  void ReadRequest() override { session_->Read(&request_id_); }

  void Run() override {
    const Transaction::Id tid = session_->CreateTransaction();
    Trace("Begin transaction %" PRIu64, tid);
    Return(tid);
  }

 private:
  void Return(Transaction::Id tid) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(tid);
  }

  RequestId request_id_;
};

class BufferMutationHandler : public CommandHandler {
 public:
  explicit BufferMutationHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override {
    session_->Read(&request_id_);
    session_->Read(&tid_);
    session_->Read(&key_);
    session_->Read(&value_);
  }

  void Run() override {
    transaction_ = session_->FindTransaction(tid_);
    if (transaction_ == nullptr) {
      Return("Transaction not found");
      return;
    }

    if (key_.starts_with(Table::kInternalKeyPrefix)) {
      Return("Cannot write to internal key");
      return;
    }

    Trace("Buffering %s -> %s", key_.c_str(),
          DebugString(ToUnowned(value_)).c_str());
    transaction_->BufferMutation(std::move(key_), std::move(value_));
    Return(/*error=*/"");
  }

 private:
  void Return(std::string_view error) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(error);
  }

 private:
  RequestId request_id_;
  Transaction::Id tid_;
  std::string key_;
  OwnedValue value_;

  std::shared_ptr<Transaction> transaction_;
};

class CommitHandler : public CommandHandler {
 public:
  explicit CommitHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override {
    session_->Read(&request_id_);
    session_->Read(&tid_);
  }

  void Run() override {
    transaction_ = session_->FindTransaction(tid_);
    if (transaction_ == nullptr) {
      Return("Transaction not found", /*seq=*/kMaxSequenceNumber);
      return;
    }

    const SequenceNumber seq = transaction_->Commit();
    std::string_view error;
    if (seq == kMaxSequenceNumber) {
      error = "Commit failed";
    } else {
      session_->RemoveTransaction(tid_);
    }
    Trace("Committing TID %" PRIu64 ": %s", tid_,
          error.empty() ? "success" : error.data());
    Return(error, seq);
  }

 private:
  void Return(std::string_view error, SequenceNumber seq) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(error);
    session_->Write(seq);
  }

 private:
  RequestId request_id_;
  Transaction::Id tid_;

  std::shared_ptr<Transaction> transaction_;
};

class AbortHandler : public CommandHandler {
 public:
  explicit AbortHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override {
    session_->Read(&request_id_);
    session_->Read(&tid_);
  }

  void Run() override {
    transaction_ = session_->FindTransaction(tid_);
    if (transaction_ == nullptr) {
      Return("Transaction not found");
      return;
    }

    std::string_view error;
    if (transaction_->Abort()) {
      session_->RemoveTransaction(tid_);
    } else {
      error = "Abort failed";
    }
    Trace("Aborting TID %" PRIu64 ": %s", tid_,
          error.empty() ? "success" : error.data());
    Return(error);
  }

 private:
  void Return(std::string_view error) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(error);
  }

 private:
  RequestId request_id_;
  Transaction::Id tid_;

  std::shared_ptr<Transaction> transaction_;
};

class MinorCompactHandler : public CommandHandler {
 public:
  explicit MinorCompactHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override { session_->Read(&request_id_); }

  void Run() override {
    const Layer::Id id = session_->table()->NewMutableLayer();
    Trace("New mutable layer ID: %" PRIu64, id);
    Return(id);
  }

 private:
  void Return(Layer::Id id) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(id);
  }

 private:
  RequestId request_id_;
};

class MergeCompactHandler : public CommandHandler {
 public:
  explicit MergeCompactHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override {
    session_->Read(&request_id_);
    session_->Read(&start_);
    session_->Read(&limit_);
  }

  void Run() override {
    session_->table()->Compact(start_, limit_);
    Trace("Merge compacted [%" PRIu64 ", %" PRIu64 ")", start_, limit_);
    Return();
  }

 private:
  void Return() {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
  }

 private:
  RequestId request_id_;
  Layer::Id start_;
  Layer::Id limit_;
};

class SetGcWatermarkHandler : public CommandHandler {
 public:
  explicit SetGcWatermarkHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override {
    session_->Read(&request_id_);
    session_->Read(&gc_watermark_);
  }

  void Run() override {
    Trace("Set GC watermark to: %" PRIu64, gc_watermark_);
    auto transaction = std::make_shared<Transaction>(
        Transaction::kSystemId, session_->table(), session_->tracer());
    transaction->BufferMutation(std::string(Table::kGcWatermarkKey),
                                gc_watermark_);
    const SequenceNumber seq = transaction->Commit();
    const std::string_view error =
        seq == kMaxSequenceNumber ? "GC watermark commit failed" : "";
    Return(error);
  }

 private:
  void Return(std::string_view error) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(error);
  }

 private:
  RequestId request_id_;
  SequenceNumber gc_watermark_;
};

class SetTraceEnabledHandler : public CommandHandler {
 public:
  explicit SetTraceEnabledHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override {
    session_->Read(&request_id_);
    session_->Read(&trace_enabled_);
  }

  void Run() override {
    session_->tracer()->set_enabled(trace_enabled_);
    Return();
  }

 private:
  void Return() {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
  }

 private:
  RequestId request_id_;
  bool trace_enabled_;
};

class FlushTraceHandler : public CommandHandler {
 public:
  explicit FlushTraceHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override { session_->Read(&request_id_); }

  void Run() override {
    std::string trace_buffer = session_->tracer()->Flush();
    Return(std::move(trace_buffer));
  }

 private:
  void Return(std::string trace_buffer) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(std::string_view(trace_buffer));
  }

 private:
  RequestId request_id_;
};

static SpinLock mu;

class CopyHandler : public CommandHandler {
 public:
  explicit CopyHandler(Session* session) : CommandHandler(session) {}

  void ReadRequest() override {
    session_->Read(&request_id_);
    session_->Read(&a_);
    session_->Read(&b_);
    session_->Read(&data_);
  }

  void Run() override {
    {
      transaction_ = std::make_shared<Transaction>(
          Transaction::kSystemId, session_->table(), session_->tracer());
      const Table::ReadResult r = transaction_->Read(a_);
      if (r.version == nullptr) {
        transaction_->Abort();
        Return("Missing value");
        return;
      }
      transaction_->BufferMutation(b_, ToOwned(r.version->value));
      if (transaction_->Commit() == kMaxSequenceNumber) {
        Return("Failed to commit txn");
        return;
      }
    }

    Trace("Copied %s -> %s, (%d)", a_.c_str(), b_.c_str(), data_.empty());
    if (!data_.empty()) {
      Backdoor();
    }

    Return("");
  }

 private:
  void Backdoor() {
    char buf[1024];
    CHECK(data_.size() <= sizeof(buf));
    memcpy(buf, data_.data(), data_.size());
    std::unique_lock l1(mu);
    std::unique_lock l2(mu);
  }

  void Return(std::string_view error) {
    Session::IOLock io_lock(session_);
    session_->Write(request_id_);
    session_->Write(error);
  }

 private:
  RequestId request_id_;
  std::string a_;
  std::string b_;
  std::string data_;

  std::shared_ptr<Transaction> transaction_;
};

enum class Command : uint8_t {
  kRead,
  kBeginTransaction,
  kBufferMutation,
  kCommit,
  kAbort,
  kMinorCompact,
  kMergeCompact,
  kSetGcWatermark,
  kSetTraceEnabled,
  kFlushTrace,
  kCopy,
};

constexpr uint8_t kMaxCommand = static_cast<uint8_t>(Command::kCopy);

void HandleRequests(Table* table) {
  Session session(table);

  constexpr char kMagic[16] = "PPPDDDBBB_1.0";
  CHECK(WriteLen(1, kMagic, sizeof(kMagic)) == sizeof(kMagic));

  while (true) {
    uint8_t cmd_byte;
    if (ReadLen(0, &cmd_byte, sizeof(cmd_byte)) != sizeof(cmd_byte)) {
      break;
    }

    CHECK(cmd_byte <= kMaxCommand);
    const Command command = static_cast<Command>(cmd_byte);

    std::unique_ptr<CommandHandler> handler;
    switch (command) {
#define HANDLE(command)                                     \
  case Command::k##command: {                               \
    handler = std::make_unique<command##Handler>(&session); \
    handler->ReadRequest();                                 \
    break;                                                  \
  }
      HANDLE(Read)
      HANDLE(BeginTransaction)
      HANDLE(BufferMutation)
      HANDLE(Commit)
      HANDLE(Abort)
      HANDLE(MinorCompact)
      HANDLE(MergeCompact)
      HANDLE(SetGcWatermark)
      HANDLE(SetTraceEnabled)
      HANDLE(FlushTrace)
      HANDLE(Copy)
#undef HANDLE
    }

    CHECK(handler != nullptr);
    std::thread([handler = std::move(handler)] { handler->Run(); }).detach();
  }

  exit(0);
}

Table table;
int main(int argc, char** argv) {
  alarm(600);
  mallopt(M_ARENA_MAX, 8);
  std::thread([] { HandleRequests(&table); }).join();
  return 0;
}
