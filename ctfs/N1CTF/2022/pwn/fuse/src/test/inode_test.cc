#include <gtest/gtest.h>
#include "test_def.h"
#include <cassert>
#include <vector>
#include <map>

TestEnvironment* env;

struct inode* single_inode;

const int nwriter             = 10;
const int nblock_reader_check = 1000;
const uint big_file_block = nwriter * ((uint)((NINDIRECT1 * 40) / nwriter) + 1);
const uint64_t big_file_size = (uint64_t)big_file_block * BSIZE;
std::array<char, big_file_size> big_file_content;
std::array<char, big_file_size> big_file_buf;

static_assert(big_file_block < NDIRECT + NINDIRECT, "file too big!");
static_assert(big_file_block < MAX_BLOCK_NO, "file too big!");

void* block_aligned_write_worker(void* _range) {
  auto range = (start_to_end*)_range;
  for (uint i = range->start; i < range->end; i++) {
    auto nbytes = inode_write_nbytes_unlocked(
        single_inode, &big_file_content[i * BSIZE], BSIZE, i * BSIZE);
    EXPECT_EQ(nbytes, BSIZE);
  }
  return nullptr;
}

void* block_aligned_read_worker(void*) {
  std::array<char, BSIZE> read_buf;
  for (int i = 0; i < nblock_reader_check; i++) {
    int blockno = rand() % big_file_block;
    auto nbytes = inode_read_nbytes_unlocked(single_inode, read_buf.data(),
                                             BSIZE, blockno * BSIZE);
    int eq = memcmp(read_buf.data(), &big_file_content[blockno * BSIZE], BSIZE);
    EXPECT_EQ(eq, 0);
    EXPECT_EQ(nbytes, BSIZE);
  }
  return nullptr;
}

int write_max_size = MAXOPBLOCKS * BSIZE;
int read_max_size  = MAXOPBLOCKS * BSIZE;

void* unaligned_random_write_worker(void* _range) {
  auto range = (struct start_to_end*)_range;
  for (uint i = range->start; i < range->end;) {
    uint size = rand() % write_max_size;
    size      = std::min(range->end - i, size);

    auto nbytes = inode_write_nbytes_unlocked(single_inode,
                                              &big_file_content[i], size, i);
    i += size;
    EXPECT_EQ(nbytes, size);
  }
  return nullptr;
}

void* unaligned_random_read_worker(void* _range) {
  auto range     = (struct start_to_end*)_range;
  char* read_buf = new char[read_max_size];
  for (uint i = range->start; i < range->end;) {
    uint size = rand() % write_max_size;
    size      = std::min(range->end - i, size);

    auto nbytes = inode_read_nbytes_unlocked(single_inode, read_buf, size, i);

    int eq = memcmp(read_buf, &big_file_content[i], size);
    EXPECT_EQ(eq, 0);
    EXPECT_EQ(nbytes, size);
    i += size;
  }
  delete[] read_buf;
  return nullptr;
}

struct File {
  struct FilePiece {
    std::string content;
    size_t start;
    size_t size;

    static FilePiece* GenRandomPiece(size_t start, size_t size) {
      auto piece   = new FilePiece;
      piece->start = start;
      piece->size  = size;
      piece->content.resize(size);
      for (char& c : piece->content) {
        c = rand() % 0x100;
      }
      return piece;
    }
  };

  std::vector<FilePiece*> pieces;
  size_t file_tatol_size;

  ~File() {
    for (auto piece : pieces) {
      delete piece;
    }
  }

  static File* GenRandomFile(size_t max_size   = MAXOPBLOCKS * BSIZE,
                             size_t max_pieces = MAXOPBLOCKS) {
    auto file    = new File;
    size_t start = 0;

    size_t piece_size;
    size_t piece_hole_size;
    size_t max_per_pieces_size      = (max_size / max_pieces) * 1.5;
    size_t max_per_pieces_hole_size = (max_size / max_pieces) * 1;
    while (start < max_size) {
      piece_hole_size =
          ((size_t)rand() << 32 | rand()) % max_per_pieces_hole_size + 1;
      if (start + piece_hole_size > max_size) {
        break;
      }
      start += piece_hole_size;
      piece_size = ((size_t)rand() << 32 | rand()) % max_per_pieces_size + 1;
      if (start + piece_size > max_size) {
        start -= piece_hole_size;
        break;
      }
      file->pieces.push_back(FilePiece::GenRandomPiece(start, piece_size));
      start += piece_size;
    }

    file->file_tatol_size = start;

    return file;
  }
};

std::vector<File*> files;
std::map<File*, uint> file_to_inum;
std::map<uint, File*> inum_to_file;
std::set<uint> inum_got;
pthread_mutex_t mapping_lock;

void* file_write_worker(void* _range) {
  auto range = (struct start_to_end*)_range;

  for (uint i = range->start; i < range->end; i++) {
    auto file = files[i];
    begin_op();
    auto inode = ialloc(T_FILE_INODE_MYFUSE);
    pthread_mutex_lock(&mapping_lock);
    if (inum_got.find(inode->inum) != inum_got.end()) {
      myfuse_debug_log("inode %d realloced", inode->inum);
    }
    inum_got.insert(inode->inum);
    file_to_inum[file] = inode->inum;
    EXPECT_EQ(inum_to_file[inode->inum], nullptr);
    inum_to_file[inode->inum] = file;
    pthread_mutex_unlock(&mapping_lock);
    ilock(inode);
    EXPECT_EQ(inode->ref, 1);
    // manully link
    inode->nlink++;
    iupdate(inode);
    iunlock(inode);
    end_op();
    for (auto piece : file->pieces) {
      EXPECT_EQ(inode_write_nbytes_unlocked(inode, piece->content.c_str(),
                                            piece->size, piece->start),
                piece->size);
    }
    begin_op();
    EXPECT_EQ(inode->size, file->file_tatol_size);
    iput(inode);
    end_op();
  }
  return nullptr;
}

void* file_read_worker(void* _range) {
  auto range = (struct start_to_end*)_range;

  std::array<char, MAXOPBLOCKS * BSIZE * 4> read_buf;

  for (uint i = range->start; i < range->end; i++) {
    pthread_mutex_lock(&mapping_lock);
    auto file = files[i];
    auto inum = file_to_inum[file];
    EXPECT_EQ(inum_to_file[inum], file);
    pthread_mutex_unlock(&mapping_lock);
    auto inode_by_iget = iget(inum);
    EXPECT_EQ(inum, inode_by_iget->inum);
    for (auto piece : file->pieces) {
      if (piece->start > file->file_tatol_size) {
        continue;
      }
      size_t read_size = piece->size;
      if (piece->size + piece->start > file->file_tatol_size) {
        read_size = file->file_tatol_size - piece->start;
      }
      EXPECT_EQ(inode_read_nbytes_unlocked(inode_by_iget, read_buf.data(),
                                           piece->size, piece->start),
                read_size);

      int eq = memcmp(read_buf.data(), piece->content.c_str(), read_size);
      EXPECT_EQ(eq, 0);
    }

    struct stat st;
    begin_op();
    ilock(inode_by_iget);
    stat_inode(inode_by_iget, &st);
    iunlock(inode_by_iget);
    end_op();
    EXPECT_EQ(st.st_size, inode_by_iget->size);
    EXPECT_EQ(st.st_nlink, inode_by_iget->nlink);
    stat_inum(inode_by_iget->inum, &st);
    EXPECT_EQ(st.st_size, inode_by_iget->size);
    EXPECT_EQ(st.st_nlink, inode_by_iget->nlink);
    EXPECT_EQ(inode_by_iget->type, T_FILE_INODE_MYFUSE);
    EXPECT_EQ(inode_by_iget->size, file->file_tatol_size);

    begin_op();
    ilock(inode_by_iget);
    EXPECT_EQ(inode_by_iget->nlink, 1);
    // inode_by_iget->nlink--;
    iupdate(inode_by_iget);
    iunlockput(inode_by_iget);
    end_op();
  }
  return nullptr;
}

void* file_truncate_worker(void* _range) {
  auto range = (struct start_to_end*)_range;
  for (uint i = range->start; i < range->end; i++) {
    pthread_mutex_lock(&mapping_lock);
    auto file = files[i];
    auto inum = file_to_inum[file];
    EXPECT_EQ(inum_to_file[inum], file);
    pthread_mutex_unlock(&mapping_lock);
    auto inode_by_iget = iget(inum);
    EXPECT_EQ(inum, inode_by_iget->inum);
    size_t random_size =
        (((uint64_t)rand() << 32) | rand()) % file->file_tatol_size;

    begin_op();
    ilock(inode_by_iget);

    itrunc2size(inode_by_iget, random_size);

    iupdate(inode_by_iget);

    EXPECT_EQ(inode_by_iget->size, random_size);
    file->file_tatol_size = random_size;

    iunlockput(inode_by_iget);
    end_op();
  }
  return nullptr;
}

void exceedTheDisk() {
  for (int i = 0; i < 5; i++) {
    begin_op();
    auto fill_all_disk_file = ialloc(T_FILE_INODE_MYFUSE);
    ilock(fill_all_disk_file);
    itrunc2size(fill_all_disk_file, big_file_size);
    iunlock(fill_all_disk_file);
    end_op();
  }
}

TEST(inode, truncate2big_test) {
  EXPECT_EXIT(exceedTheDisk(); exit(0), testing::ExitedWithCode(1), "");
}

TEST(inode, truncate_test) {
  // this test mayno failed it self, but may fail other test by filling all disk
  // with junk
  // NOTE: change the 2 to larger can help test better
  for (uint i = 0; i < 2; i++) {
    std::array<char, BSIZE> ones;
    ones.fill(1);
    begin_op();
    auto fill_all_disk_file = ialloc(T_FILE_INODE_MYFUSE);
    end_op();
    for (uint i = 0; i < (uint)((MAX_BLOCK_NO - nmeta_blocks) * 0.9); i++) {
      inode_write_nbytes_unlocked(fill_all_disk_file, ones.data(), BSIZE,
                                  i * BSIZE);
    }
    begin_op();
    fill_all_disk_file->nlink = 1;
    iupdate(fill_all_disk_file);
    itrunc2size(fill_all_disk_file, 1);
    iput(fill_all_disk_file);
    // iput(fill_all_disk_file);
    end_op();
  }
}

TEST(inode, unaligned_random_read_write_test) {
  write_max_size = MAXOPBLOCKS * BSIZE;
  read_max_size  = MAXOPBLOCKS * BSIZE;
  begin_op();
  single_inode = ialloc(T_FILE_INODE_MYFUSE);
  end_op();

  for (char& c : big_file_content) {
    c = rand();
  }

  start_worker(unaligned_random_write_worker, MAX_WORKER, big_file_size);

  start_worker(unaligned_random_read_worker, MAX_WORKER, big_file_size);

  begin_op();
  iput(single_inode);
  end_op();
}

TEST(inode, big_unaligned_random_read_write_test) {
  write_max_size = MAXOPBLOCKS * 10 * BSIZE;
  read_max_size  = MAXOPBLOCKS * 10 * BSIZE;
  begin_op();
  single_inode = ialloc(T_FILE_INODE_MYFUSE);
  end_op();

  for (char& c : big_file_content) {
    c = rand();
  }

  start_worker(unaligned_random_write_worker, MAX_WORKER, big_file_size);

  start_worker(unaligned_random_read_worker, MAX_WORKER, big_file_size);

  begin_op();
  iput(single_inode);
  end_op();
}

TEST(inode, parallel_big_unaligned_random_read_write_test) {
  write_max_size = MAXOPBLOCKS * 10 * BSIZE;
  read_max_size  = MAXOPBLOCKS * 10 * BSIZE;

  begin_op();
  single_inode = ialloc(T_FILE_INODE_MYFUSE);
  end_op();

  for (char& c : big_file_content) {
    c = rand();
  }

  start_worker(unaligned_random_write_worker, MAX_WORKER, big_file_size);

  start_worker(unaligned_random_read_worker, MAX_WORKER, big_file_size);

  begin_op();
  iput(single_inode);
  end_op();
}

TEST(inode, single_big_read_write_test) {
  begin_op();
  single_inode = ialloc(T_FILE_INODE_MYFUSE);
  end_op();

  for (char& c : big_file_content) {
    c = rand() % 0x100;
  }

  long nbytes;

  nbytes = inode_write_nbytes_unlocked(single_inode, big_file_content.data(),
                                       big_file_content.size(), 0);
  EXPECT_EQ(nbytes, big_file_content.size());

  nbytes = inode_read_nbytes_unlocked(single_inode, big_file_buf.data(),
                                      big_file_content.size(), 0);
  EXPECT_EQ(nbytes, big_file_content.size());

  EXPECT_EQ(big_file_content, big_file_buf);
}

TEST(inode, parrallel_block_aligned_read_write_test) {
  begin_op();
  single_inode = ialloc(T_FILE_INODE_MYFUSE);
  end_op();

  for (char& c : big_file_content) {
    c = rand() % 0x100;
  }

  start_worker(block_aligned_write_worker, nwriter, big_file_block);

  std::array<char, BSIZE> read_buf;

  int failed = 0;
  // check the write
  for (uint i = 0; i < big_file_block; i++) {
    inode_read_nbytes_unlocked(single_inode, read_buf.data(), BSIZE, i * BSIZE);
    int eq = memcmp(read_buf.data(), &big_file_content[i * BSIZE], BSIZE);
    if (eq != 0) {
      failed++;
    }
  }

  myfuse_debug_log("failed on %d blocks", failed);
  myfuse_debug_log("%.3lf memory successfully read and write",
                   (big_file_block - failed) / (big_file_block * 1.0));
  ASSERT_EQ(failed, 0);

  start_worker(block_aligned_read_worker, nwriter, big_file_block);

  begin_op();
  iput(single_inode);
  end_op();
}

TEST(inode, mutil_file_read_write_test) {
  const int total_files = 100;

  files.reserve(total_files);
  // create ${total_files} files
  for (int i = 0; i < total_files / 2; i++) {
    files.push_back(File::GenRandomFile());
  }
  for (int i = 0; i < total_files / 2; i++) {
    files.push_back(File::GenRandomFile(MAXOPBLOCKS * BSIZE * 2, MAXOPBLOCKS));
  }

  start_worker(file_write_worker, MAX_WORKER, files.size());

  start_worker(file_read_worker, MAX_WORKER, files.size());

  start_worker(file_truncate_worker, MAX_WORKER, files.size());

  start_worker(file_read_worker, MAX_WORKER, files.size());
}

int main(int argc, char* argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  env = reinterpret_cast<TestEnvironment*>(
      ::testing::AddGlobalTestEnvironment(new TestEnvironment()));
  if (env == nullptr) {
    err_exit("failed to init testing env!");
  }
  pthread_mutex_init(&mapping_lock, nullptr);
  return RUN_ALL_TESTS();
}
