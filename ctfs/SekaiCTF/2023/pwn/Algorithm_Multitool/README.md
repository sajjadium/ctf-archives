C++20 introduced coroutines, I cant wait to abuse them!
To get a leak, look into c++ Small String Optimization.
Lambda capture variable is stored in the stack, you can overwrite it somehow. if you figure out what its overwritten with, solving this is straightforward.
