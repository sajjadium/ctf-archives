from secret import flag
import os, subprocess, tempfile
from base64 import b64decode

hash_mod = 1 << 32
hash_mask = hash_mod - 1
def sign_ext(val):
    if val >= 0x80:
        return val - 256 + hash_mod
    return val

def calc_hash(data):
    assert len(data) == 0x33b, "Bad length"
    base_hash = 1
    for v in data:
        base_hash = (base_hash * 31 + sign_ext(v)) & hash_mask
    return base_hash

wanted_hash = 868400328
print('Wanted hash:', hex(wanted_hash))
print('Please input your apk file(base64-encoded, <10MB, ends with EOF in new line):', end=' ')
apk = ''
while True:
    line = input().strip()
    if line == 'EOF':
        break
    apk += line
    if len(apk) > 20 * 1024 * 1024:
        print('Too long!')
        exit()

cwd = os.getcwd()

apk_data = b64decode(apk)
with tempfile.TemporaryDirectory(prefix="MAnaGerfAker") as dir:
    os.chdir(dir)
    with open('test.apk', 'wb') as f:
        f.write(apk_data)
    ret = subprocess.run(['java', '-jar', os.path.join(cwd, "apksigner.jar"), "verify", "--verbose", "--max-sdk-version", "33", "--min-sdk-version", "27", "test.apk"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ret.returncode != 0 or len(ret.stderr.strip()) > 0:
        print('Error(%d):' % (ret.returncode, ), ret.stderr.decode())
        exit()
    ret :str= ret.stdout.decode().strip().replace('\r', '')
    lower_ret = ret.lower()
    if 'warning' in lower_ret or 'error' in lower_ret or 'does not verify' in lower_ret or '\nVerifies\n' not in ret or ret.count('Verified using v3 scheme (APK Signature Scheme v3):') != 1 or ret.count('Verified using v2 scheme (APK Signature Scheme v2):') != 1 or '\nVerified using v2 scheme (APK Signature Scheme v2): true\n' not in ret or '\nVerified using v3 scheme (APK Signature Scheme v3): true\n' not in ret:
        print('Bad apk!')
        exit()
    exported_cer = [calc_hash(open(file, 'rb').read()) for file in os.listdir(".") if file.endswith(".cer") and file.startswith("x509_exported_")]
    if len(exported_cer) == 0 or any([x != wanted_hash for x in exported_cer]):
        print('No exported cer!')
        exit()
    print('Good! You prove it.')
    print(flag)
