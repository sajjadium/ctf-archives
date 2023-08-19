from distutils.core import setup, Extension

def main():
    setup(name="spy",
          version="1.0.0",
          description="Spy Game Module",
          author="Louis Burda",
          author_email="quent.burda@gmail.com",
          ext_modules=[Extension("spy", ["spymodule.c"])])

if __name__ == "__main__":
    main()
