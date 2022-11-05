#include <gtest/gtest.h>
#include "test_def.h"

TestEnvironment* env;

std::array<bool, MAX_BLOCK_NO> wrote;

void* test_write_worker(void* _range) {
  auto range = (struct start_to_end*)_range;
  begin_op();
  int in_op = 1;
  for (uint i = range->start; i < range->end; i++) {
    int blockno = content_blockno[i];
    if (blockno < nmeta_blocks) {
      // don't write meta block
      continue;
    }
    if (in_op == 0) {
      begin_op();
      in_op = 1;
    }
    auto b = logged_read(blockno);
    memcpy(b->data, contents[blockno], BSIZE);
    logged_write(b);
    EXPECT_EQ(0, memcmp(b->data, contents[blockno], BSIZE));
    EXPECT_EQ(blockno, b->blockno);
    logged_relse(b);
    if (n_log_wrote >= MAXOPBLOCKS - 1) {
      in_op = 0;
      end_op();
    }
    EXPECT_EQ(wrote[blockno], false);
    wrote[blockno] = true;
  }
  if (in_op) {
    end_op();
  }
  return nullptr;
}

void* test_read_worker(void*) {
  int read_times = content_sum;
  for (int i = 0; i < read_times; i++) {
    int blockno = content_blockno[rand() % content_sum];
    if (blockno < nmeta_blocks) {
      continue;
    }
    auto b = logged_read(blockno);
    int eq = memcmp(b->data, contents[blockno], BSIZE);
    EXPECT_EQ(eq, 0);
    logged_relse(b);
  }
  return nullptr;
}

TEST(log_test, begin_end_op_test) {
  for (int i = 0; i < 10; i++) {
    begin_op();
    end_op();
  }
}

TEST(log_test, parallel_read_write_test) {
  generate_block_test_data();
  start_worker(test_write_worker, 10);

  int failed = 0;
  // check the write
  for (int& i : content_blockno) {
    if (i < nmeta_blocks) {
      ASSERT_FALSE(wrote[i]);
      continue;
    }
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