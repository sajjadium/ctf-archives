#include "test_def.h"
#include <random>
#include <algorithm>

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

TEST(directory, dir_link_lookup_test) {
  // first, get the root
  auto rootdp = path2inode("/");
  ASSERT_EQ(rootdp->inum, ROOTINO);
  iput(rootdp);

  // second, generate lots of paths
  const int name_sum       = 100;
  const int max_paths      = 2000;
  const int max_path_depth = MAXOPBLOCKS / 6 + 5;
  std::set<std::string> names_set;
  while (names_set.size() < name_sum) {
    auto name = gen_random((rand() % (DIRSIZE - 1)) + 1);
    if (name != "." && name != "..") {
      names_set.insert(name);
    }
  }
  const std::vector<std::string> names(names_set.begin(), names_set.end());
  using Path = std::vector<std::string>;
  std::set<Path> paths_set;

  while (paths_set.size() < max_paths) {
    Path path;
    for (int j = 0; j <= std::rand() % max_path_depth; j++) {
      path.push_back(names[rand() % names.size()]);
    }
    paths_set.insert(path);
  }
  const std::vector<Path> paths(paths_set.begin(), paths_set.end());

  std::map<Path, uint> path2inum;
  std::map<Path, uint> path2parentinum;

  for (const auto& path : paths) {
    std::string cwd       = "/";
    uint last_inum        = ROOTINO;
    uint last_parent_inum = ROOTINO;
    for (const auto& name : path) {
      std::string next_cwd = (cwd + "/").append(name);
      begin_op();
      auto ip = path2inode(next_cwd.c_str());
      if (ip == nullptr) {
        ip = ialloc(T_DIR_INODE_MYFUSE);
        ilock(ip);
        ip->nlink++;
        iupdate(ip);
        auto dp = path2inode(cwd.c_str());
        ASSERT_NE(dp, nullptr);
        EXPECT_EQ(last_inum, dp->inum);
        ilock(dp);
        dirlink(dp, name.c_str(), ip->inum);
        last_parent_inum = dp->inum;
        iunlockput(dp);
        iunlock(ip);
      }
      ASSERT_NE(ip, nullptr);
      last_inum = ip->inum;
      iput(ip);
      end_op();
      cwd = next_cwd;
    }
    ASSERT_NE(last_inum, 0);
    path2inum[path]       = last_inum;
    path2parentinum[path] = last_parent_inum;
    begin_op();
    end_op();
  }

  // validate
  for (const Path& path : paths) {
    std::string lasT_DIR_INODE_MYFUSE = "";
    for (const auto& name : path) {
      lasT_DIR_INODE_MYFUSE += "/";
      lasT_DIR_INODE_MYFUSE += name;
    }

    begin_op();
    auto found_dp = path2inode(lasT_DIR_INODE_MYFUSE.c_str());
    std::array<char, DIRSIZE> last_name;
    auto found_pdp =
        path2parentinode(lasT_DIR_INODE_MYFUSE.c_str(), last_name.data());
    ASSERT_NE(found_dp, nullptr);
    ASSERT_NE(found_pdp, nullptr);
    EXPECT_EQ(found_dp->inum, path2inum[path]);
    EXPECT_EQ(found_pdp->inum, path2parentinum[path]);
    EXPECT_EQ(strncmp(last_name.data(), path[path.size() - 1].c_str(), DIRSIZE),
              0);
    iput(found_dp);
    iput(found_pdp);
    end_op();
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
