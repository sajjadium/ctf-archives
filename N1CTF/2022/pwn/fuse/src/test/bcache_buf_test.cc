#include <gtest/gtest.h>
#include "test_def.h"

TestEnvironment* env;

// map blockno to it's expected content
// this array denotes {blockno}-th block has been wrote
std::array<bool, MAX_BLOCK_NO> wrote;

void* test_write_worker(void* _range) {
  auto range = (struct start_to_end*)_range;
  for (uint i = range->start; i < range->end; i++) {
    int blockno = content_blockno[i];
    auto b      = bread(blockno);
    memcpy(b->data, contents[blockno], BSIZE);
    auto n_write = bwrite(b);
    EXPECT_EQ(0, memcmp(b->data, contents[blockno], BSIZE));
    EXPECT_EQ(blockno, b->blockno);
    EXPECT_EQ(n_write, BSIZE);
    brelse(b);
    EXPECT_EQ(wrote[blockno], false);
    wrote[blockno] = true;
  }
  return nullptr;
}

void* test_read_worker(void*) {
  int read_times = content_sum / MAX_WORKER;
  for (int i = 0; i < read_times; i++) {
    int blockno = content_blockno[rand() % content_sum];
    auto b      = bread(blockno);
    int eq      = memcmp(b->data, contents[blockno], BSIZE);
    EXPECT_EQ(eq, 0);
    brelse(b);
  }
  return nullptr;
}

// test:
// random read write block with mutiple threads
// this test is not `unit' at all...
TEST(bcache_buf, parallel_read_write_test) {
  int failed = 0;

  // no need to avoid the meta blocks;
  nmeta_blocks = 0;
  generate_block_test_data();

  start_worker(test_write_worker);

  // check the write
  for (int& i : content_blockno) {
    ASSERT_TRUE(wrote[i]);
    auto b = bread(i);
    int eq = memcmp(b->data, contents[i], BSIZE);
    brelse(b);
    if (eq != 0) {
      failed++;
    }
  }

  myfuse_debug_log("failed on %d blocks", failed);
  myfuse_debug_log("%.3lf memory successfully read and write",
                   (content_sum - failed) / (content_sum * 1.0));
  ASSERT_EQ(failed, 0);

  start_worker(test_read_worker);
}

int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  env = reinterpret_cast<TestEnvironment*>(
      ::testing::AddGlobalTestEnvironment(new TestEnvironment()));
  if (env == nullptr) {
    err_exit("failed to init testing env!");
  }
  return RUN_ALL_TESTS();
}