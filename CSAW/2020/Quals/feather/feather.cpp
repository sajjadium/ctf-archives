#include <map>
#include <memory>
#include <span>
#include <stdint.h>
#include <stdio.h>
#include <string>
#include <unistd.h>
#include <variant>
#include <vector>

using u8 = uint8_t;
using u16 = uint16_t;
using u32 = uint32_t;
using u64 = uint64_t;

// https://stackoverflow.com/a/34571089
std::vector<u8> base64_decode(const std::string &encoded) {
  std::vector<int> T(256, -1);
  for (int i = 0; i < 64; i++) {
    T["ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[i]] =
        i;
  }

  std::vector<u8> out{};

  int val = 0, valb = -8;
  for (auto c : encoded) {
    if (T[c] == -1)
      break;
    val = (val << 6) + T[c];
    valb += 6;
    if (valb >= 0) {
      out.push_back(char((val >> valb) & 0xFF));
      valb -= 8;
    }
  }

  return out;
}

static std::string encoded{};
std::vector<u8> read_base64_from_stdin() {
  char buffer[256] = {0};

  encoded = "";

  ssize_t read_amount = 0;
  while ((read_amount = read(STDIN_FILENO, buffer, sizeof(buffer))) > 0) {
    encoded += std::string(buffer, read_amount);

    if (encoded.size() > 2 && encoded[encoded.size() - 1] == '\n' &&
        encoded[encoded.size() - 2] == '\n') {
      break;
    }
  }

  return base64_decode(encoded);
}

std::vector<std::string_view> split_by(const std::string &input,
                                       const char splitter) {
  std::vector<std::string_view> result{};

  u64 last = 0;
  u64 curr = 0;
  for (; curr < input.size(); curr++) {
    if (input[curr] == splitter) {
      result.push_back(std::string_view(input).substr(last, curr - last));
      last = curr + 1;
    }
  }

  if (curr != last) {
    result.push_back(std::string_view(input).substr(last, curr - last));
  }

  return result;
}

struct Entry;
struct Feather {
  std::map<u32, Entry *> loaded_segments{};
  std::string label{""};
  Entry *root{nullptr};

  void print_tree(Entry *entry, u64 depth);
  void print_tree() {
    printf("Tree with label %s:", label.c_str());
    print_tree(root, 0);
  }
};

enum class Segment_Type {
  Directory = 0,
  File = 1,
  File_Clone = 2,
  Symlink = 3,
  Hardlink = 4,
  Label = 5,
};

struct Entry {
  struct Directory {
    std::vector<Entry *> entries;
  };
  struct File {
    std::vector<u8> contents;
  };
  struct File_Clone {
    u32 source_inode;
    std::vector<u8> cached_file_contents;
  };
  struct Symlink {
    std::string target;
    Entry *target_inode_cache;
  };
  struct Hardlink {
    u32 target;
    Entry *target_inode_cache;
  };
  using Value = std::variant<Directory, File, File_Clone, Symlink, Hardlink>;

  static Entry *make_directory(const std::string_view name,
                               const std::vector<Entry *> &entries) {
    return new Entry{Segment_Type::Directory, std::string(name),
                     Directory{entries}};
  }
  static Entry *make_file(const std::string_view name,
                          const std::vector<u8> &contents) {
    return new Entry{Segment_Type::File, std::string(name), File{contents}};
  }
  static Entry *make_file_clone(const std::string_view name, u32 source) {
    return new Entry{Segment_Type::File_Clone, std::string(name),
                     File_Clone{source, {}}};
  }
  static Entry *make_symlink(const std::string_view name,
                             const std::string_view target) {
    return new Entry{Segment_Type::Symlink, std::string(name),
                     Symlink{std::string(target), nullptr}};
  }
  static Entry *make_hardlink(const std::string_view name, u32 target) {
    return new Entry{Segment_Type::Hardlink, std::string(name),
                     Hardlink{target, nullptr}};
  }

  Directory &directory() { return std::get<Directory>(value); }
  File &file() { return std::get<File>(value); }
  File_Clone &file_clone(Feather &fs) {
    auto &result = std::get<File_Clone>(value);
    if (result.cached_file_contents.empty()) {
      result.cached_file_contents =
          fs.loaded_segments.find(result.source_inode)->second->file().contents;
    }
    return result;
  }
  Symlink &symlink(Feather &fs) {
    auto &result = std::get<Symlink>(value);
    if (result.target_inode_cache == nullptr) {
      const auto components = split_by(result.target, '/');
      Entry *curr = fs.root;
      for (u64 i = 0; i < components.size() - 1; i++) {
        const auto &component = components[i];
        const auto &next_component = components[i + 1];
        if (curr->name != component) {
          goto end;
        }
        switch (curr->type) {
        case Segment_Type::Directory: {
          const auto &directory = curr->directory();
          const auto it = std::find_if(
              directory.entries.begin(), directory.entries.end(),
              [&](Entry *entry) { return entry->name == next_component; });
          if (it == directory.entries.end()) {
            goto end;
          }
          curr = *it;
          break;
        }
        case Segment_Type::File: {
          goto end;
        }
        case Segment_Type::File_Clone: {
          goto end;
        }
        case Segment_Type::Symlink: {
          curr = curr->symlink(fs).target_inode_cache;
          break;
        }
        case Segment_Type::Hardlink: {
          curr = curr->hardlink(fs).target_inode_cache;
          break;
        }
        }
      }
      result.target_inode_cache = curr;
    }
  end:
    return result;
  }
  Hardlink &hardlink(Feather &fs) {
    auto &result = std::get<Hardlink>(value);
    if (result.target_inode_cache == nullptr) {
      result.target_inode_cache =
          fs.loaded_segments.find(result.target)->second;
    }
    return result;
  }

  Segment_Type type;
  std::string name;
  Value value;
};

namespace layout {
struct Header {
  u64 magic;
  u32 num_segments;
} __attribute__((packed));

struct Segment {
  u32 type;
  u32 id;
  u32 offset;
  u32 length;
} __attribute__((packed));

struct Directory {
  u32 name_length;
  u32 num_entries;
  /* u8 name[] */
  /* u32 entries[] */
} __attribute__((packed));

struct File {
  u32 name_length;
  u32 contents_length;
  /* u8 name[] */
  /* u8 contents[] */
} __attribute__((packed));

struct File_Clone {
  u32 name_length;
  u32 target_inode;
  /* u8 name[] */
} __attribute__((packed));

struct Symlink {
  u32 name_length;
  u32 target_length;
  /* u8 name[] */
  /* u8 target[] */
} __attribute__((packed));

struct Hardlink {
  u32 name_length;
  u32 target;
  /* u8 name[] */
} __attribute__((packed));
} // namespace layout

template <typename T>
std::span<T> checked_subspan(const std::span<T> span, u64 offset, u64 length) {
  if (offset <= span.size() && offset + length <= span.size() &&
      offset <= offset + length) {
    return span.subspan(offset, length);
  }
  printf("Invalid subspan for span of size %zu: offset: %zu, length: %zu\n",
         span.size(), offset, length);
  abort();
}

Feather load_feather_fs(const std::vector<u8> &blob) {
  if (blob.size() < sizeof(layout::Header)) {
    printf("Filesystem blob too small!\n");
    abort();
  }

  const auto &header = *(const layout::Header *)(blob.data());

  if (header.magic != 0x52454854414546) {
    printf("Invalid magic: %llx\n", header.magic);
    abort();
  }
  if (header.num_segments > 100000) {
    printf("Too many segments: %zu (max: 100000)\n", header.num_segments);
    abort();
  }
  if (sizeof(layout::Header) + header.num_segments * sizeof(layout::Segment) >
      blob.size()) {
    printf("Segment table size is larger than size of blob\n");
    abort();
  }

  const auto *segment_region =
      (const layout::Segment *)(blob.data() + sizeof(layout::Header));
  std::span<const layout::Segment> segments(segment_region,
                                            header.num_segments);

  const auto *data_region = (const u8 *)&segment_region[header.num_segments];
  std::span<const u8> data(data_region, blob.data() + blob.size());

  u64 total_segments = std::count_if(
      segments.begin(), segments.end(), [](layout::Segment segment) {
        return segment.type != u32(Segment_Type::Label);
      });

  Feather feather{};
  while (feather.loaded_segments.size() != total_segments) {
    for (const auto &segment : segments) {
      if (feather.loaded_segments.contains(segment.id)) {
        continue;
      }

      auto contents = checked_subspan(data, segment.offset, segment.length);

      switch (segment.type) {
      case u32(Segment_Type::Directory): {
        if (segment.length < sizeof(layout::Directory)) {
          printf("Directory segment too small (%u vs %u)\n", segment.length,
                 sizeof(layout::Directory));
          abort();
        }

        const auto &directory_header =
            *(const layout::Directory *)(contents.data());
        std::span<const u8> name = checked_subspan(
            contents, sizeof(layout::Directory), directory_header.name_length);
        std::span<const u8> children_bytes = checked_subspan(
            contents, sizeof(layout::Directory) + directory_header.name_length,
            directory_header.num_entries * sizeof(u32));
        std::span<const u32> children((const u32 *)children_bytes.data(),
                                      children_bytes.size() / sizeof(u32));

        std::vector<Entry *> child_entries{};
        child_entries.reserve(children.size());
        bool missing_children = false;
        for (const auto child : children) {
          if (!feather.loaded_segments.contains(child)) {
            missing_children = true;
            break;
          }
          child_entries.push_back(feather.loaded_segments[child]);
        }
        if (missing_children) {
          continue;
        }

        feather.loaded_segments[segment.id] = Entry::make_directory(
            std::string_view((const char *)name.data(), name.size()),
            child_entries);
        if (name.empty()) {
          feather.root = feather.loaded_segments[segment.id];
        }
        break;
      }
      case u32(Segment_Type::File): {
        if (segment.length < sizeof(layout::File)) {
          printf("File segment too small (%u vs %u)\n", segment.length,
                 sizeof(layout::File));
          abort();
        }

        const auto &file_header = *(const layout::File *)(contents.data());
        std::span<const u8> name = checked_subspan(
            contents, sizeof(layout::File), file_header.name_length);
        std::span<const u8> file_contents = checked_subspan(
            contents, sizeof(layout::File) + file_header.name_length,
            file_header.contents_length);

        feather.loaded_segments[segment.id] = Entry::make_file(
            std::string_view((const char *)name.data(), name.size()),
            std::vector<u8>(file_contents.data(),
                            file_contents.data() + file_contents.size()));
        break;
      }
      case u32(Segment_Type::File_Clone): {
        if (segment.length < sizeof(layout::File_Clone)) {
          printf("File_Clone segment too small (%u vs %u)\n", segment.length,
                 sizeof(layout::File_Clone));
          abort();
        }

        const auto &file_clone_header =
            *(const layout::File_Clone *)(contents.data());
        std::span<const u8> name =
            checked_subspan(contents, sizeof(layout::File_Clone),
                            file_clone_header.name_length);
        auto target = file_clone_header.target_inode;

        if (!feather.loaded_segments.contains(target)) {
          continue;
        }

        feather.loaded_segments[segment.id] = Entry::make_file_clone(
            std::string_view((const char *)name.data(), name.size()), target);
        break;
      }
      case u32(Segment_Type::Symlink): {
        if (segment.length < sizeof(layout::Symlink)) {
          printf("Symlink segment too small (%u vs %u)\n", segment.length,
                 sizeof(layout::Symlink));
          abort();
        }

        const auto &symlink_header =
            *(const layout::Symlink *)(contents.data());
        std::span<const u8> name = checked_subspan(
            contents, sizeof(layout::Symlink), symlink_header.name_length);
        std::span<const u8> target = checked_subspan(
            contents, sizeof(layout::Symlink) + symlink_header.name_length,
            symlink_header.target_length);

        feather.loaded_segments[segment.id] = Entry::make_symlink(
            std::string_view((const char *)name.data(), name.size()),
            std::string_view((const char *)target.data(), target.size()));
        break;
      }
      case u32(Segment_Type::Hardlink): {
        if (segment.length < sizeof(layout::Hardlink)) {
          printf("Hardlink segment too small (%u vs %u)\n", segment.length,
                 sizeof(layout::Hardlink));
          abort();
        }

        const auto &hardlink_header =
            *(const layout::Hardlink *)(contents.data());
        std::span<const u8> name = checked_subspan(
            contents, sizeof(layout::Hardlink), hardlink_header.name_length);

        feather.loaded_segments[segment.id] = Entry::make_hardlink(
            std::string_view((const char *)name.data(), name.size()),
            hardlink_header.target);
        break;
      }
      case u32(Segment_Type::Label): {
        feather.label.assign(
            std::string_view((const char *)contents.data(), contents.size()));
        break;
      }
      default: {
        printf("Error: Invalid segment type: %u\n", segment.type);
        abort();
      }
      }
    }
  }

  for (const auto [id, entry] : feather.loaded_segments) {
    if (entry->name.empty()) {
      feather.root = entry;
      return feather;
    }
  }

  printf("Error: No filesystem root found\n");
  abort();
}

void Feather::print_tree(Entry *entry, u64 depth) {
  auto print_indent = [depth]() {
    for (u64 i = 0; i < depth; i++) {
      printf("  ");
    }
  };

  switch (entry->type) {
  case Segment_Type::Directory: {
    print_indent();
    printf("%s/\n", entry->name.c_str());
    for (auto child : entry->directory().entries) {
      print_tree(child, depth + 1);
    }
    break;
  }
  case Segment_Type::File: {
    print_indent();
    printf("%s: File, %zu bytes\n", entry->name.c_str(),
           entry->file().contents.size());
    break;
  }
  case Segment_Type::File_Clone: {
    print_indent();
    printf("%s: File, %zu bytes\n", entry->name.c_str(),
           entry->file_clone(*this).cached_file_contents.size());
    break;
  }
  case Segment_Type::Symlink: {
    print_indent();
    auto &symlink = entry->symlink(*this);
    std::string target_name = symlink.target;
    if (symlink.target_inode_cache == nullptr) {
      target_name += " (broken)";
    }
    printf("%s: Symlink to %s\n", entry->name.c_str(), target_name.c_str());
    break;
  }
  case Segment_Type::Hardlink: {
    auto &hardlink = entry->hardlink(*this);
    print_tree(hardlink.target_inode_cache, depth);
    break;
  }
  default: {
    printf("Error: Unhandled segment type in print_tree: %#x\n",
           u32(entry->type));
    abort();
  }
  }
}
int main() {
  setvbuf(stdout, NULL, _IONBF, 0);

  puts("Please send a base64-encoded feather file, followed by two newlines:");
  auto file = read_base64_from_stdin();
  puts("Loading Feather Filesystem...");
  auto feather = load_feather_fs(file);
  puts("Filesystem dump:");
  feather.print_tree();
}
