My operating systems professor is teaching us using xv6. At the end of the lecture, he pointed us to section 6.10 exercise 1 of the book, which states:

    Comment out the calls to acquire and release in kalloc (kernel/kalloc.c:69). This seems like it should cause problems for kernel code that calls kalloc; what symptoms do you expect to see? When you run xv6, do you see these symptoms? How about when running usertests? If you don’t see a problem, why not? See if you can provoke a problem by inserting dummy loops into the critical section of kalloc.

Can you help me write a decent answer before the next lecture?
