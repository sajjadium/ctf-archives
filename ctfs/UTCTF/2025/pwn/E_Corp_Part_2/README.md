Last year, your internship at E-Corp (Evil Corp) ended with a working router RCE exploit. Leadership was very impressed. As a result, we chose to extend a return offer. We used your exploit to get a MiTM position on routers around the world. Now, we want to be able to use that MiTM position to exploit browsers to further our world domination plans! This summer, you will need to exploit Chrome!

One of our vulnerability researchers has discovered a new type confusion bug in Chrome. It turns out, a type confusion can be evoked by calling .confuse() on a PACKED_DOUBLE_ELEMENTS or PACKED_ELEMENTS array. The attached poc.js illustrates an example. You can run it with ./d8 ./poc.js. Once you have an RCE exploit, you will find a file with the flag in the current directory. Good luck and have fun!

By Aadhithya (@aadhi0319 on discord)
