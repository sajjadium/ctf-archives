Try the half RCE challenge!


## Build

```
cd v8
git pull
git checkout 68d1f7534f616977e386dfa5041206bed2ec213a
gclient sync -D
patch -p1 < ../tctf.patch
gn gen out/tctf_d8_2 --args='is_debug=false dcheck_always_on=false v8_static_library=true target_cpu="x64" v8_enable_sandbox=true v8_enable_object_print=true v8_expose_memory_corruption_api=true'
autoninja -C out/tctf_d8_2 d8
```
