mkdir /tmp/build
cd /tmp/build
wget 'https://github.com/jerryscript-project/jerryscript/archive/refs/tags/v2.4.0.tar.gz'
# sha256: 5850947c23db6fbce032d15560551408ab155b16a94a7ac4412dc3bb85762d2d  /tmp/build/v2.4.0.tar.gz
# ping admin if the hash doesn't match.
tar xf v2.4.0.tar.gz
cd jerryscript-2.4.0
python3 ./tools/build.py --clean
ls -al ./build/bin/jerry
