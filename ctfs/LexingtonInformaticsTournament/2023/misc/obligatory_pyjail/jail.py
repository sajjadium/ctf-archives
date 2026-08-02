# python3.10 jail.py build
import os
from distutils.core import Extension, setup
if not os.path.exists("./audit_sandbox.so"):
  setup(name='audit_sandbox', ext_modules=[
        Extension('audit_sandbox', ['audit_sandbox.c'])],)
  os.popen("cp build/lib*/audit_sandbox* audit_sandbox.so")
del os
import sys
cod = input(">>> ")
import audit_sandbox
audit_sandbox.install_hook()
del audit_sandbox
del sys.modules['audit_sandbox']
del sys
print(eval(cod))