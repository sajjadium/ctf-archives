#include "test_def.h"
#include "block_allocator.h"
#include <random>
#include <algorithm>

TestEnvironment* env;

void random_bmap_get_set() {
  uint end_of_bmap = ROUNDUP(MYFUSE_STATE->sb.size, BPB);
  std::vector<bool> bmap_status;
  std::vector<std::pair<uint, bool>> random_bmap;
  bmap_status.resize(end_of_bmap, true);
  random_bmap.resize(MYFUSE_STATE->sb.nblocks);
  for (uint i = nmeta_blocks; i < MYFUSE_STATE->sb.nblocks + nmeta_blocks;
       i++) {
    bmap_status[i]                       = rand() % 2;
    random_bmap[i - nmeta_blocks].first  = i;
    random_bmap[i - nmeta_blocks].second = bmap_status[i];
  }

  std::random_device rd;
  std::mt19937 g(rd());
  std::shuffle(random_bmap.begin(), random_bmap.end(), g);

  for (auto pair : random_bmap) {
    int i = pair.first;
    begin_op();
    for (int random = rand() % 10; random > 0; random--) {
      bmap_block_statue_set(i, rand() % 2);
    }
    bmap_block_statue_set(i, pair.second);
    if (rand() % 2) {
      bmap_block_statue_set(i, pair.second);
    }
    end_op();
  }

  for (uint i = 0; i < end_of_bmap; i++) {
    EXPECT_EQ(bmap_block_statue_get(i), bmap_status[i]);
  }

  // persistent test
  block_allocator_refresh(&MYFUSE_STATE->sb);
  uint n_alloced              = 0;
  int first_unalloced         = -1;
  int first_unalloced_blockno = -1;
  for (uint i = 0; i < end_of_bmap; i++) {
    EXPECT_EQ(bmap_block_statue_get(i), bmap_status[i]);
    if (bmap_status[i] == 1) {
      n_alloced++;
    } else {
      if (first_unalloced < 0) {
        first_unalloced         = i % BPB;
        first_unalloced_blockno = i;
      }
    }

    if ((i + 1) % BPB == 0) {
      // test the meta of the last bitmap block
      EXPECT_EQ(n_alloced, bmap_cache.n_alloced[(i / BPB)]);
      EXPECT_EQ(first_unalloced, bmap_cache.first_unalloced[(i / BPB)]);
      EXPECT_EQ(first_unalloced + (i / BPB) * BPB, first_unalloced_blockno);
      n_alloced               = 0;
      first_unalloced         = -1;
      first_unalloced_blockno = -1;
    }
  }

  for (uint i = 0; i < end_of_bmap; i++) {
    begin_op();
    bmap_block_statue_set(i, 1);
    end_op();
  }
  block_allocator_refresh(&MYFUSE_STATE->sb);
  for (uint i = 0; i < bmap_cache.n_cache; i++) {
    EXPECT_EQ(bmap_cache.n_alloced[i], BPB);
    EXPECT_EQ(bmap_cache.first_unalloced[i], -1);
  }
}

TEST(block_allocator, bmap_block_statue_get_set_test) {
  // a. test the meta blocks
  for (int i = 0; i < nmeta_blocks; i++) {
    EXPECT_EQ(bmap_block_statue_get(i), 1);
  }
  uint end_of_bmap = ROUNDUP(MYFUSE_STATE->sb.size, BPB);
  for (uint i = MYFUSE_STATE->sb.size; i < end_of_bmap; i++) {
    EXPECT_EQ(bmap_block_statue_get(i), 1);
  }
  // reinit to set the set's persistent
  block_allocator_refresh(&MYFUSE_STATE->sb);
  for (int i = 0; i < nmeta_blocks; i++) {
    EXPECT_EQ(bmap_block_statue_get(i), 1);
  }
  for (uint i = MYFUSE_STATE->sb.size; i < end_of_bmap; i++) {
    EXPECT_EQ(bmap_block_statue_get(i), 1);
  }

  for (int test_times = 0; test_times < 5; test_times++) {
    // b. randomly set status
    random_bmap_get_set();
  }
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
