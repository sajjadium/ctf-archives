#include "test_def.h"
#include <array>
#include <algorithm>
#include <random>

TestEnvironment* env;

// test:
// 1. read block
// 2. write block
// 3. random read write
TEST(block_device, read_write_test) {
  std::array<u_char, BSIZE> write_buf;
  std::array<u_char, BSIZE> read_buf;

  for (int i = 0; i < 1000; i++) {
    for (auto& c : write_buf) {
      c = rand() % 0x100;
    }
    int blockno = rand() % MAX_BLOCK_NO;
    int n_write = write_block_raw(blockno, write_buf.data());
    EXPECT_EQ(n_write, BSIZE);
    int n_read = read_block_raw(blockno, read_buf.data());
    EXPECT_EQ(n_write, n_read);
    EXPECT_EQ(write_buf, read_buf);
  }
}

TEST(block_device, random_read_write_test) {
  // write all the disk here
  nmeta_blocks = 0;
  generate_block_test_data();

  for (int& i : content_blockno) {
    int n_write = write_block_raw(i, contents[i]);
    EXPECT_EQ(n_write, BSIZE);
  }

  std::random_device rd;
  std::mt19937 g(rd());
  std::shuffle(content_blockno.begin(), content_blockno.end(), g);

  for (int& i : content_blockno) {
    std::array<u_char, BSIZE> buf;
    int n_read = read_block_raw(i, buf.data());
    EXPECT_EQ(n_read, BSIZE);
    int eq = memcmp(buf.data(), contents[i], BSIZE);
    EXPECT_EQ(eq, 0);
  }
}

// this array denotes {blockno}-th block has been wrote
std::array<bool, MAX_BLOCK_NO> wrote;

void* test_write_worker(void* _range) {
  auto range = (struct start_to_end*)_range;
  for (uint i = range->start; i < range->end; i++) {
    int blockno  = content_blockno[i];
    auto n_write = write_block_raw(blockno, contents[blockno]);
    EXPECT_EQ(n_write, BSIZE);
    EXPECT_EQ(wrote[blockno], false);
    wrote[blockno] = true;
  }
  return nullptr;
}

TEST(block_device, parrallel_write_test) {
  int failed = 0;

  // write all the disk here
  nmeta_blocks = 0;
  generate_block_test_data();

  wrote.fill(false);
  start_worker(test_write_worker);

  std::array<u_char, BSIZE> read_buf;

  // check the write
  for (int& i : content_blockno) {
    ASSERT_TRUE(wrote[i]);
    auto n_read = read_block_raw(i, read_buf.data());
    EXPECT_EQ(n_read, BSIZE);
    int eq = memcmp(read_buf.data(), contents[i], BSIZE);
    if (eq != 0) {
      failed++;
    }
  }

  myfuse_debug_log("failed on %d blocks", failed);
  myfuse_debug_log("%.3lf memory successfully read and write",
                   (content_sum - failed) / (content_sum * 1.0));
  ASSERT_EQ(failed, 0);
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
