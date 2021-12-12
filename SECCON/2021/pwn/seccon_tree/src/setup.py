from distutils.core import setup, Extension
setup(name='seccon_tree',
        version='1.0',
        ext_modules=[Extension('seccon_tree', ['lib.c'])]
)
