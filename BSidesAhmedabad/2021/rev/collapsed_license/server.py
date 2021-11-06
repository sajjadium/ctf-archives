import os
import base64
import tempfile
import subprocess
import requests

if __name__ == '__main__':
    try:
        url = input("License URL: ")
        assert url.startswith("http")
        lic = requests.get(url).content
        assert len(lic) < 1000*1000 # 1MB limit
        with tempfile.NamedTemporaryFile('w+b') as f:
            f.write(lic)
            f.flush()
            subprocess.run(["./y05h1k1ng50f7", f.name])
    except Exception as e:
        print("[-] Error", e)
