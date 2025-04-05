class File:
    def __init__(self, filename, content=""):
        self.filename = filename
        self.content = content


class Directory:
    def __init__(self):
        self.entries = {}


class Symlink:
    def __init__(self, target):
        self.target = target


class VirtualShell:
    MAX_ENTRIES = 100
    MAX_SYMLINK_DEPTH = 10

    def __init__(self):
        self.fs = {"/": Directory()}
        self.current_path = ["/"]
        self.fs["/"].entries["flag.txt"] = File("flag.txt", "[REDACTED]")
        self.fs["/"].entries["shell.history"] = File("shell.history", "")
        self.fs["/"].entries[".Trash"] = Directory()
        self.commit_history = {}

    def _get_cwd(self):
        return "/".join(self.current_path)[1:] if self.current_path != ["/"] else "/"

    def _normalize_path(self, path_list):
        """Normalize path parts by handling '.' and '..'."""
        result = []
        for part in path_list:
            if part == "" or part == ".":
                continue
            elif part == "..":
                if result:
                    result.pop()
            else:
                result.append(part)
        return result

    def _get_current_dir(self):
        """Return the current directory, resolving symlinks along the way."""
        ref = self.fs["/"]
        for folder in self.current_path[1:]:
            if folder not in ref.entries:
                print(f"Error: Directory '{folder}' not found.")
                return None
            entry = ref.entries[folder]
            if isinstance(entry, Symlink):
                resolved = self._resolve_path(entry.target.strip("/").split("/"))
                if resolved is None:
                    print(f"Error: Unable to resolve symlink for '{folder}'.")
                    return None
                ref = resolved
            elif isinstance(entry, Directory):
                ref = entry
            else:
                print(f"Error: '{folder}' is not a directory.")
                return None
        return ref

    def _resolve_path(self, path_list, visited=None, depth=0):
        """Resolve a path list, following symlinks, with loop detection and depth limit."""
        if depth > self.MAX_SYMLINK_DEPTH:
            print("Error: Maximum symlink resolution depth exceeded.")
            return None

        if visited is None:
            visited = set()
        normalized = self._normalize_path(path_list)
        ref = self.fs["/"]

        for folder in normalized:
            if folder not in ref.entries:
                print(f"Error: Directory entry '{folder}' does not exist.")
                return None
            entry = ref.entries[folder]

            if isinstance(entry, Symlink):
                if entry.target in visited:
                    print("Error: Symlink loop detected.")
                    return None
                visited.add(entry.target)
                target_path = self._normalize_path(entry.target.strip("/").split("/"))
                resolved = self._resolve_path(target_path, visited, depth + 1)
                if resolved is None:
                    return None
                ref = resolved
            elif isinstance(entry, Directory):
                ref = entry
            else:
                return entry
        return ref

    def _load_history(self):
        history_file = self.fs["/"].entries.get("shell.history")
        return (
            history_file.content.split("\n")
            if history_file and history_file.content
            else []
        )

    def _save_history(self):
        history_file = self.fs["/"].entries.get("shell.history")
        if history_file:
            history_file.content = "\n".join(self.history)

    def _validate_name(self, name):
        """Ensure the name is valid (no slashes)."""
        if "/" in name:
            print("Invalid name: cannot contain '/'.")
            return False
        return True

    def _check_directory_space(self, directory):
        if len(directory.entries) >= self.MAX_ENTRIES:
            print("Error: Directory is full.")
            return False
        return True

    def _ln(self, args):
        if len(args) != 2:
            print("Usage: ln <target> <link_name>")
            return
        target, link_name = args
        if not self._validate_name(link_name):
            return
        current_dir = self._get_current_dir()
        if current_dir is None or link_name in current_dir.entries:
            print("Link name already exists.")
            return
        resolved_target = self._resolve_path(target.strip("/").split("/"))
        if resolved_target is None:
            print("Target does not exist. Ensure to give absolute paths only")
            return
        current_dir.entries[link_name] = Symlink(target)

    def _rm(self, args):
        if len(args) != 1:
            print("Usage: rm <filename>")
            return

        filename = args[0]
        current_dir = self._get_current_dir()

        if current_dir is None:
            return

        if filename not in current_dir.entries:
            print("File not found.")
            return

        if filename == ".Trash":
            print(f"Cannot remove {filename}.")
            return

        trash_dir = self.fs["/"].entries[".Trash"]
        if filename in trash_dir.entries:
            print(f"File {filename} already exists in .Trash. Overwriting.")
        try:
            trash_dir.entries[filename] = current_dir.entries.pop(filename)
            print(f"Moved {filename} to .Trash/")
        except Exception as e:
            print(f"Error moving {filename} to .Trash: {e}")

    def _clear(self, args):
        if args:
            print("Usage: clear")
            return
        print("\033c", end="")

    def _git_commit(self, args):
        if args:
            print("Usage: git commit")
            return

        import time, random, hashlib

        commit_time = int(time.time())
        rand_val = random.randint(1, 10000)
        hash_val = hashlib.sha256(str(rand_val).encode()).hexdigest()[:6]
        commit_id = f"{commit_time}-{hash_val}"

        def snapshot(directory):
            data = {}
            for name, entry in directory.entries.items():
                if isinstance(entry, File):
                    data[name] = (entry.content, "file")
                elif isinstance(entry, Directory):
                    data[name] = snapshot(entry)
                elif isinstance(entry, Symlink):
                    data[name] = (
                        entry.target,
                        "symlink",
                    )
            return data

        commit_snapshot = snapshot(self.fs["/"])
        self.commit_history[commit_id] = commit_snapshot
        print(f"Committed.")

    def _git_status(self, args):
        if args:
            print("Usage: git status")
            return

        if not self.commit_history:
            print("No commits found.")
            return

        latest_commit_id = sorted(self.commit_history.keys())[-1]
        latest_snapshot = self.commit_history[latest_commit_id]

        def compare_snapshots(current, committed, path=""):
            changes = {"new": [], "modified": [], "deleted": []}

            for name, entry in current.entries.items():
                full_path = f"{path}/{name}".lstrip("/")
                if isinstance(entry, File):
                    if name not in committed:
                        changes["new"].append(full_path)
                    elif entry.content != committed[name][0]:
                        changes["modified"].append(full_path)
                elif isinstance(entry, Directory):
                    if name not in committed:
                        changes["new"].append(full_path)
                    else:
                        sub_changes = compare_snapshots(
                            entry, committed[name], full_path
                        )
                        for key in changes:
                            changes[key].extend(sub_changes[key])

            for name in committed.keys():
                full_path = f"{path}/{name}".lstrip("/")
                if name not in current.entries:
                    changes["deleted"].append(full_path)

            return changes

        changes = compare_snapshots(self.fs["/"], latest_snapshot)

        if not any(changes.values()):
            print("No changes.")
        else:
            for key in changes:
                if changes[key]:
                    print(f"{key.capitalize()} files:\n" + "\n".join(changes[key]))

    def _git_snapshot(self, args):
        if len(args) != 1:
            print("Usage: git snapshot <commit_id>")
            return

        commit_id = args[0]

        if commit_id not in self.commit_history:
            print("Error: Commit ID not found.")
            return

        def print_snapshot(snapshot, indent=0):
            for name, entry in snapshot.items():
                prefix = " " * indent
                if isinstance(entry, tuple):
                    if entry[1] == "symlink":
                        print(f"{prefix}{name} -> {entry[0]} (Symlink)")
                    else:
                        print(f"{prefix}{name} (File)")
                        print(
                            f"{prefix}---\n{prefix}Content:\n{prefix}{entry[0]}\n{prefix}---"
                        )
                else:
                    print(f"{prefix}{name}/ (Directory)")
                    print_snapshot(entry, indent + 4)

        print(f"Snapshot of commit {commit_id}:")
        print_snapshot(self.commit_history[commit_id])

    def _git_restore(self, args):
        if len(args) != 1:
            print("Usage: git restore <filename>")
            return

        if not self.commit_history:
            print("Error: No commits available to restore from.")
            return

        latest_commit_id = sorted(self.commit_history.keys())[-1]
        latest_snapshot = self.commit_history[latest_commit_id]

        def restore_entry(snapshot, current_dir, filename):
            if filename not in snapshot:
                print(f"Error: '{filename}' not found in latest commit.")
                return False

            if filename in [".Trash"]:
                print(f"Error: Cannot restore protected file '{filename}'.")
                return False

            entry = snapshot[filename]
            if isinstance(entry, tuple):
                if entry[1] == "symlink":
                    current_dir.entries[filename] = Symlink(entry[0])
                else:
                    current_dir.entries[filename] = File(filename, entry[0])
            else:
                current_dir.entries[filename] = Directory()
                for name in entry:
                    restore_entry(entry, current_dir.entries[filename], name)
            return True

        current_dir = self._get_current_dir()
        if current_dir is None:
            return

        if restore_entry(latest_snapshot, current_dir, args[0]):
            print(f"Restored '{args[0]}' from latest commit.")

    def run(self):
        self.history = self._load_history()

        try:
            while True:
                command = input(f"{self._get_cwd()}$ ").strip()
                if not command:
                    continue

                self.history.append(command)
                self._save_history()

                parts = self._parse_command(command)
                if not parts:
                    continue
                cmd, args = parts[0], parts[1:]

                if cmd == "history":
                    self._history()
                elif cmd == "ls":
                    self._ls(args)
                elif cmd == "cd":
                    self._cd(args)
                elif cmd == "mkdir":
                    self._mkdir(args)
                elif cmd == "touch":
                    self._touch(args)
                elif cmd == "cat":
                    self._cat(args)
                elif cmd == "echo":
                    self._echo(args)
                elif cmd == "write":
                    self._write(args)
                elif cmd == "ln":
                    self._ln(args)
                elif cmd == "rm":
                    self._rm(args)
                elif cmd == "clear":
                    self._clear(args)
                elif cmd == "git":
                    if args:
                        if args[0] == "commit":
                            self._git_commit(args[1:])
                        elif args[0] == "status":
                            self._git_status(args[1:])
                        elif args[0] == "snapshot":
                            self._git_snapshot(args[1:])
                        elif args[0] == "restore":
                            self._git_restore(args[1:])
                        else:
                            print("Unknown git command.")
                    else:
                        print("Unknown git command.")
                elif cmd == "exit":
                    print("Exiting...")
                    break
                else:
                    print(f"Unknown command: {cmd}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _parse_command(self, command):
        result, current, in_quotes = [], "", False
        for char in command:
            if char == '"':
                in_quotes = not in_quotes
            elif char == " " and not in_quotes:
                if current:
                    result.append(current)
                    current = ""
            else:
                current += char

        if in_quotes:
            print("Error: Unbalanced quotes detected.")
            return []

        if current:
            result.append(current)

        return result

    def _cd(self, args):
        if len(args) != 1:
            print("Usage: cd <directory>")
            return
        path = args[0]
        if path == "..":
            if len(self.current_path) > 1:
                self.current_path.pop()
            return
        current_dir = self._get_current_dir()
        if current_dir is None:
            return
        entry = current_dir.entries.get(path)
        if isinstance(entry, Symlink):
            entry = self._resolve_path(entry.target.strip("/").split("/"))
            if entry is None:
                print(f"Error: Cannot navigate to symlink target '{path}'.")
                return
        if isinstance(entry, Directory):
            self.current_path.append(path)
        else:
            print(f"Error: '{path}' is not a directory or does not exist.")

    def _mkdir(self, args):
        if len(args) != 1:
            print("Usage: mkdir <directory>")
            return
        dirname = args[0]
        if not self._validate_name(dirname):
            return
        current_dir = self._get_current_dir()
        if current_dir is None or not self._check_directory_space(current_dir):
            return
        if dirname not in current_dir.entries:
            current_dir.entries[dirname] = Directory()
        else:
            print("Directory already exists.")

    def _touch(self, args):
        if len(args) != 1:
            print("Usage: touch <filename>")
            return
        filename = args[0]
        if not self._validate_name(filename):
            return
        current_dir = self._get_current_dir()
        if current_dir is None or not self._check_directory_space(current_dir):
            return
        if filename not in current_dir.entries:
            current_dir.entries[filename] = File(filename)
        else:
            print("File already exists.")

    def _cat(self, args):
        if len(args) != 1:
            print("Usage: cat <filename>")
            return
        filename = args[0]
        current_dir = self._get_current_dir()
        if current_dir is None:
            return
        entry = current_dir.entries.get(filename)
        if isinstance(entry, Symlink):
            entry = self._resolve_path(entry.target.strip("/").split("/"))
        if isinstance(entry, File):
            if entry.filename != "flag.txt":
                print(entry.content)
            else:
                print("Permission denied.")
        else:
            print("File not found.")

    def _echo(self, args):
        if not args:
            print("Usage: echo <text>")
            return
        print(" ".join(args))

    def _write(self, args):
        if len(args) < 2:
            print("Usage: write <filename> <text>")
            return

        filename, text = args[0], " ".join(args[1:])

        current_dir = self._get_current_dir()
        if current_dir is None:
            return

        if filename in current_dir.entries:
            file = current_dir.entries[filename]
            if isinstance(file, File):
                file.content = text
            else:
                print("Not a file.")
        else:
            current_dir.entries[filename] = File(filename, text)

    def _ls(self, args):
        if args:
            print("Usage: ls")
            return
        directory = self._get_current_dir()
        if directory:
            print(" ".join(directory.entries.keys()) or "(empty)")
        else:
            print("Error: Cannot access directory.")

    def _history(self):
        if not self.history:
            print("No history available.")
            return
        for i, cmd in enumerate(self.history, start=1):
            print(f"{i}  {cmd}")


if __name__ == "__main__":
    VirtualShell().run()
