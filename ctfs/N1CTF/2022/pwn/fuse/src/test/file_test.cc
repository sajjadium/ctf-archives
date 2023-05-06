#include "test_def.h"

TestEnvironment* env;

std::string gen_random(const int len) {
  std::string alphanum =
      "0123456789_."
      "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
      "abcdefghijklmnopqrstuvwxyz";
  std::string tmp_s;
  tmp_s.reserve(len);

  for (int i = 0; i < len; ++i) {
    tmp_s += alphanum[rand() % (alphanum.length() - 1)];
  }

  return tmp_s;
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
std::map<std::string, File*> name2file;
std::vector<std::string> paths;
std::map<std::string, file*> path2file;

void* file_write_worker(void* _range) {
  auto range = (struct start_to_end*)_range;
  struct fuse_file_info fi;

  for (uint i = range->start; i < range->end; i++) {
    auto path = paths[i];
    fi.flags  = 0;
    fi.flags |= O_CREAT | O_RDWR;
    myfuse_open(("/" + path).c_str(), &fi);
    auto file = (struct file*)fi.fh;
    EXPECT_NE(file, nullptr);
    EXPECT_EQ(file->type, FD_INODE);
    EXPECT_NE(file->ip, nullptr);
    path2file[path] = file;
  }

  return nullptr;
}

void* file_read_worker(void* _range) {
  auto range = (struct start_to_end*)_range;
  struct fuse_file_info fi;

  for (uint i = range->start; i < range->end; i++) {
    auto path = paths[i];
    fi.fh     = (uint64_t)path2file[path];
    myfuse_release(nullptr, &fi);
  }

  return nullptr;
}

TEST(file, file_open_close) {
  const int total_files = 100;

  files.reserve(total_files);
  // create ${total_files} files
  for (int i = 0; i < total_files / 2; i++) {
    files.push_back(File::GenRandomFile());
  }
  for (int i = 0; i < total_files / 2; i++) {
    files.push_back(File::GenRandomFile(MAXOPBLOCKS * BSIZE * 4, MAXOPBLOCKS));
  }

  // second, generate lots of names
  const int name_sum = total_files;
  std::set<std::string> names_set;
  while (names_set.size() < name_sum) {
    auto name = gen_random((rand() % (DIRSIZE - 1)) + 1);
    if (name != "." && name != "..") {
      names_set.insert(name);
    }
  }
  const std::vector<std::string> names(names_set.begin(), names_set.end());
  paths = names;

  // TODO: finish the test
  for (int i = 0; i < total_files; i++) {
    name2file[names[rand() % names.size()]] = files[i];
  }

  start_worker(file_write_worker, MAX_WORKER, files.size());

  start_worker(file_read_worker, MAX_WORKER, files.size());
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
