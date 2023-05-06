from distutils.core import setup, Extension

module = Extension('auditor', sources = ['auditor.c'])
setup(name = 'auditor', version = '1.0', description = 'More auditing!', ext_modules = [module])
