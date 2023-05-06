The challenge is to exploit V8 9.1.269.36 with these two changes:

------------------------------------------------------------------------------------
diff --git a/src/compiler/js-create-lowering.cc b/src/compiler/js-create-lowering.cc
index 899922a27f..aea23fe7ea 100644
--- a/src/compiler/js-create-lowering.cc
+++ b/src/compiler/js-create-lowering.cc
@@ -681,7 +681,7 @@ Reduction JSCreateLowering::ReduceJSCreateArray(Node* node) {
       int capacity = static_cast<int>(length_type.Max());
       // Replace length with a constant in order to protect against a potential
       // typer bug leading to length > capacity.
-      length = jsgraph()->Constant(capacity);
+      //length = jsgraph()->Constant(capacity);
       return ReduceNewArray(node, length, capacity, *initial_map, elements_kind,
                             allocation, slack_tracking_prediction);
     }
diff --git a/src/compiler/typer.cc b/src/compiler/typer.cc
index 0f18222236..0f76ad896e 100644
--- a/src/compiler/typer.cc
+++ b/src/compiler/typer.cc
@@ -2073,7 +2073,7 @@ Type Typer::Visitor::TypeStringFromCodePointAt(Node* node) {
 }

 Type Typer::Visitor::TypeStringIndexOf(Node* node) {
-  return Type::Range(-1.0, String::kMaxLength, zone());
+  return Type::Range(0, String::kMaxLength, zone());
 }

 Type Typer::Visitor::TypeStringLength(Node* node) {
------------------------------------------------------------------------------------



For your convenience we have provided you a few things:

1) exploit.js - This is a template to build your exploit around. Feel free to use it or not. It
   contains code to turn arbitrary read, write and get object address primitives into arbitrary
   code execution. It also contains the shellcode to print `flag.txt`, which is what you need to
   print to solve the challenge.

2) v8-binary - Contains the v8 binary we will test your exploit against.

3) Download the built v8 source here:
     https://drive.google.com/file/d/1DQiqnyvEWJNtmpZ-oIPRCTzKaZgx5xlP/view?usp=sharing

   This is the source code built with our changes. You should be able to make changes and quickly
   rebuild (without rebuilding the whole thing) by using the provided docker container. We also
   had the V8 build system output a `compile_commands.json`. This should make it easier to import
   the code into an IDE so you can more precisely navigate and get cross references.

4) Download depot_tools here:
     https://drive.google.com/file/d/1aZBtZHSk5iC34lFmgFtZgghJG0koULQj/view?usp=sharing

   You can also just get it from git, we haven't made any changes to this.

5) build-challenge.sh - This shows exactly how we built the challenge. You alternatively could build
   V8 for testing this way, instead of downloading the prebuilt sources from above. This may take
   longer though since you will have to wait for an entire V8 build.



How to test locally, and then remotely:

1) Run the following to test locally:
    ./v8-binary/v8_hello_world < exploit.js

2) Run the following to test remotely.
    cat exploit.js | nc <challenge server> <port>
   Make sure your exploit ends with "// END" otherwise this may hang.


Building the source with changes.

1) Launch the docker container.
    enter-docker-container.sh

2) Add depot_tools to your path.
    export PATH=`pwd`/depot_tools:$PATH

3) Rebuild.
    ninja -C v8/v8/out/x64.release v8_hello_world

   This should only rebuild object files that need rebuilding based on the files you modified.
