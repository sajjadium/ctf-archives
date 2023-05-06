#include "mkfs.myfuse-util.h"

#include <cassert>
#include <string>
#include <set>

std::set<int> block_used;

struct myfuse_state* get_myfuse_state() {
  static struct myfuse_state state;
  return &state;
}

static void disk_init(std::string& disk_name) {
  block_device_init(disk_name.c_str());

  MYFUSE_STATE->sb.size = 1;
  if (read_block_raw_nbytes(SUPERBLOCK_ID, (u_char*)&MYFUSE_STATE->sb,
                            sizeof(struct superblock)) !=
      sizeof(struct superblock)) {
    err_exit("failed to read super block");
  }

  if (MYFUSE_STATE->sb.magic != FSMAGIC) {
    err_exit("disk magic not match! read %x", MYFUSE_STATE->sb.magic);
  }

  bcache_init();
  log_init(&MYFUSE_STATE->sb);
  inode_init(&MYFUSE_STATE->sb);
  file_init();
}

void print_direct_map(uint* addrs, size_t n) {
  char comma = ' ';
  printf("[");
  for (int i = 0; i < n; i++) {
    if (addrs[i]) {
      putchar(comma);
      comma = ',';
      printf(R"({"index":%d,"blockno": %u})", i, addrs[i]);
      block_used.insert(addrs[i]);
    }
  }
  printf("]");
}

void print_indirect1_map(uint* addrs, size_t n) {
  char comma = ' ';
  for (int i = 0; i < n; i++) {
    if (addrs[i] != 0) {
      block_used.insert(addrs[i]);

      putchar(comma);
      comma = ',';
      printf("{");

      printf(R"("index_page": %u,)", addrs[i]);
      printf(R"("map_page": )");
      struct bcache_buf* bp = logged_read(addrs[i]);
      print_direct_map((uint*)bp->data, NINDIRECT1);
      logged_relse(bp);
      printf("}");
    }
  }
}

void print_indirect2_map(uint* addrs, size_t n) {
  char comma = ' ';
  for (int i = 0; i < n; i++) {
    if (addrs[i] != 0) {
      block_used.insert(addrs[i]);

      putchar(comma);
      comma = ',';
      printf("{");

      printf(R"("index_page": %u,)", addrs[i]);
      printf(R"("map_pages": [)");
      struct bcache_buf* bp = logged_read(addrs[i]);
      print_indirect1_map((uint*)bp->data, NINDIRECT1);
      logged_relse(bp);

      printf("]");
      printf("}");
    }
  }
}

void print_indirect3_map(uint* addrs, size_t n) {
  char comma = ' ';
  for (int i = 0; i < n; i++) {
    if (addrs[i] != 0) {
      block_used.insert(addrs[i]);

      putchar(comma);
      comma = ',';
      printf("{");

      printf(R"("index_page": %u,)", addrs[i]);
      printf(R"("map_pages": [)");
      struct bcache_buf* bp = logged_read(addrs[i]);
      print_indirect2_map((uint*)bp->data, NINDIRECT1);
      logged_relse(bp);

      printf("]");
      printf("}");
    }
  }
}

void output_dinode(struct dinode* dip, uint inum) {
  printf("{");
  // inum

  printf(R"("inum": %d)", inum);

  // type
  printf(R"(,"type": %d)", dip->type);

  // size
  printf(R"(,"used_size": %lu)", dip->size);

  // block index uses
  printf(R"(,"direct": )");
  print_direct_map(dip->addrs, NDIRECT);

  if (dip->addrs[NDIRECT]) {
    printf(R"(,"indirect1": )");
    print_indirect1_map(&dip->addrs[NDIRECT], 1);
  }

  if (dip->addrs[NDIRECT + 1]) {
    printf(R"(,"indirect2": )");
    print_indirect2_map(&dip->addrs[NDIRECT + 1], 1);
  }

  if (dip->addrs[NDIRECT + 2]) {
    printf(R"(,"indirect3": )");
    print_indirect3_map(&dip->addrs[NDIRECT + 2], 1);
  }
  printf("}");
}

static void count_leakblock() {
  printf(R"("leak": [)");
  char comma = ' ';
  for (int i = MYFUSE_STATE->sb.size - MYFUSE_STATE->sb.nblocks;
       i < MYFUSE_STATE->sb.size; i++) {
    if (bmap_block_statue_get(i)) {
      if (!block_used.count(i)) {
        putchar(comma);
        comma = ',';
        printf("%d", i);
      }
    }
  }
  printf("]");
}

static void count_inodes(void (*filler)(struct dinode*, uint)) {
  struct bcache_buf* bp;
  struct dinode* dip;

  char comma = ' ';
  printf(R"("files": [)");

  for (int inum = 1; inum < MYFUSE_STATE->sb.ninodes; inum++) {
    bp  = logged_read(IBLOCK(inum));
    dip = (struct dinode*)bp->data + inum % IPB;
    if (dip->type != T_UNUSE_INODE_MYFUSE) {
      putchar(comma);
      comma = ',';
      filler(dip, inum);
    }
    logged_relse(bp);
  }

  printf("]");
}

void print_superblock() {
  printf(R"("superblock":{)");
  printf(R"("size_in_blocks": %u,)", MYFUSE_STATE->sb.size);
  printf(R"("block_size": %lu,)", BSIZE);
  printf(R"("ndata_blocks": %u,)", MYFUSE_STATE->sb.nblocks);
  printf(R"("nlog_blocks": %u,)", MYFUSE_STATE->sb.nlog);
  printf(R"("ninode_blocks": %u,)", MYFUSE_STATE->sb.ninodes);
  printf(R"("logstart": %u,)", MYFUSE_STATE->sb.logstart);
  printf(R"("inodestart": %u,)", MYFUSE_STATE->sb.inodestart);
  printf(R"("bmapstart": %u)", MYFUSE_STATE->sb.bmapstart);
  printf("}");
}

int main(int argc, char* argv[]) {
  std::string disk_name;

  if (argc != 2) {
    err_exit("Usage: %s <path to your disk>", argv[0]);
  }

  disk_name = argv[1];
  disk_init(disk_name);

  printf("{");

  print_superblock();

  printf(",");
  count_inodes(output_dinode);

  printf(",");
  count_leakblock();

  printf("}");
}