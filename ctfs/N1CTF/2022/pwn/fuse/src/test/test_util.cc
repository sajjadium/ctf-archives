#include "random"
#include <algorithm>
#include "test_def.h"

// map blockno to it's expected content
std::map<int, const u_char*> contents;
// this array contains [0, MAX_BLOCK_NO), and then shuffled
std::array<int, MAX_BLOCK_NO> total_blockno;
// this array contains {content_sum} uniq random nums in range [0, MAX_BLOCK_NO)
std::array<int, content_sum> content_blockno;

int nmeta_blocks = 0;

void generate_block_test_data() {
  // init the global contents
  for (int i = 0; i < nmeta_blocks; i++) {
    // write 0 in test is safe (fs do not use the boot section)
    total_blockno[i] = 0;
  }
  for (int i = nmeta_blocks; i < MAX_BLOCK_NO; i++) {
    total_blockno[i] = i;
  }

  static_assert(content_sum <= MAX_BLOCK_NO,
                "content_sum must lower then MAX_BLOCK_NO");

  std::random_device rd;
  std::mt19937 g(rd());
  std::shuffle(total_blockno.begin(), total_blockno.end(), g);
  std::copy(total_blockno.begin(),
            total_blockno.begin() + content_blockno.size(),
            content_blockno.begin());

  for (int& i : content_blockno) {
    auto buf = new u_char[BSIZE];
    for (unsigned long i = 0; i < BSIZE; i++) {
      buf[i] = rand() % 0x100;
    }
    contents[i] = buf;
  }
}

void start_worker(void* (*pthread_worker)(void*), uint MAX_WORKER,
                  uint64_t end) {
  auto workers = new pthread_t[MAX_WORKER];
  auto ranges  = new struct start_to_end[MAX_WORKER];
  for (uint i = 0; i < MAX_WORKER; i++) {
    auto range   = &ranges[i];
    range->start = i * (end / MAX_WORKER);
    range->end   = (i + 1) * (end / MAX_WORKER);
    pthread_create(&workers[i], nullptr, pthread_worker, range);
  }
  for (uint i = 0; i < MAX_WORKER; i++) {
    pthread_join(workers[i], nullptr);
  }

  delete[] workers;
  delete[] ranges;
}
