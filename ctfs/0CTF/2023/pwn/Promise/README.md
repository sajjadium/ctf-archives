Try the RCE challenge!


## Build

```
cd v8
git pull
git checkout 68d1f7534f616977e386dfa5041206bed2ec213a
gclient sync -D
patch -p1 < ../CVE-2023-4355_tctf.patch
gn gen out/tctf_d8 --args='is_debug=false dcheck_always_on=false v8_static_library=true target_cpu="x64" v8_enable_sandbox=true v8_enable_object_print=true'
autoninja -C out/tctf_d8 d8
```
