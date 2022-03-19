import std.stdio;
import std.format;
import std.range;
import std.typecons;
import std.algorithm;

// @safe ensures memory safety, yay!
// https://dlang.org/spec/memory-safe-d.html
@safe:

/* Polygon struct */
alias vertex = Tuple!(int, int);
struct Polygon
{
private:
  vertex[] _vertices; // List of vertex

public:
  this(ulong n) {
    if (n <= 2) // Dots and lines are not polygon
      throw new Exception("Invalid number of vertices");
    _vertices = new vertex[n];
  }
  ~this() {}

  /* Convert this structure into string (@trusted for sink) */
  void toString(scope void delegate(const(char)[]) sink,
                FormatSpec!char fmt) const @trusted {
    if (fmt.spec != 's')
      throw new Exception("Unknown format specifier: %" ~ fmt.spec);

    sink("[ Polygon: ");
    foreach (vertex v; _vertices) {
      sink(format("(%d,%d) ", v[0], v[1]));
    }
    sink("]");
  }

  /* Set the position of a vertex */
  void set_vertex(ulong index, vertex v) {
    if (index > _vertices.length - 1)
      throw new Exception("Invalid index");

    _vertices[index] = v;
  }
}

/* We need to wrap `readf` in a trusted function
   because it's @system and not thread safe */
vertex read_vertex(string msg) @trusted {
  int x, y;
  write(msg);
  readf("(%d, %d)\n", x, y);
  return tuple(x, y);
}

ulong read_ul(string msg) @trusted {
  ulong i;
  write(msg);
  readf("%d\n", i);
  return i;
}

string read_str(string msg) @trusted {
  string s;
  write(msg);
  readf("%s\n", s);
  return s;
}

/* Create a new polygon */
void polygon_new(ref Polygon[string] ps) {
  string name = read_str("Name: ");

  ulong n = read_ul("Number of vertices: ");

  Polygon p = Polygon(n);
  for (ulong i = 0; i < n; i++) {
    vertex v = read_vertex(format("vertices[%d] = ", i));
    p.set_vertex(i, v);
  }

  ps[name] = p;
}

/* Show a polygon */
void polygon_show(ref Polygon[string] ps) {
  string name = read_str("Name: ");

  if (!(name in ps)) // Not found
    throw new Exception("No such polygon: " ~ name);

  writeln(ps[name]);
}

/* Rename a polygon */
void polygon_rename(ref Polygon[string] ps) {
  string old_name = read_str("(old) Name: ");
  string new_name = read_str("(new) Name: ");

  if (!(old_name in ps)) // Not found
    throw new Exception("No such polygon: " ~ old_name);

  Polygon p;
  move(ps[old_name], p); // Make a copy

  if (new_name in ps) {
    // Ask when new name already exists
    writeln("Do you want to overwrite the existing polygon?");
    writeln(new_name, " --> ", ps[new_name]);

    string answer = read_str("[y/N]: ");
    if (answer[0] != 'Y' && answer[0] != 'y')
      return;
  }

  // Remove original polygon and move to target
  ps.remove(old_name);
  ps[new_name] = p;
}

/* Edit a vertex in a polygon */
void polygon_edit(ref Polygon[string] ps) {
  string name = read_str("Name: ");

  if (!(name in ps)) // Not found
    throw new Exception("No such polygon: " ~ name);

  ulong index = read_ul("Index: ");
  vertex v = read_vertex(format("vertices[%d] = ", index));
  ps[name].set_vertex(index, v);
}

/* Delete a polygon */
void polygon_delete(ref Polygon[string] ps) {
  string name = read_str("Name: ");

  if (!(name in ps)) // Not found
    throw new Exception("No such polygon: " ~ name);

  ps.remove(name);
}

/* Entry point! (@trusted for setvbuf) */
void main() @trusted
{
  Polygon[string] ps;

  stdin.setvbuf(0, _IONBF);
  stdout.setvbuf(0, _IONBF);

  writeln("  o  o");
  writeln(" / __ \\");
  writeln(" \\|@@\\/");
  writeln("  || \\\\");
  writeln("  ||_//");
  writeln("  |__/");
  writeln("  / \\");
  writeln("  `o b");
  writeln("1. New");
  writeln("2. Show");
  writeln("3. Rename");
  writeln("4. Edit");
  writeln("5. Delete");

  while (true) {
    ulong choice;
    try {
      choice = read_ul("> ");
    } catch (Exception e) {
      break;
    }

    try {
      switch (choice) {
      case 1: polygon_new(ps); break;
      case 2: polygon_show(ps); break;
      case 3: polygon_rename(ps); break;
      case 4: polygon_edit(ps); break;
      case 5: polygon_delete(ps); break;
      default: return;
      }
    } catch (Exception e) {
      writeln("[ERROR] ", e);
    }
  }
}
