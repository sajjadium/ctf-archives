author:ptr-yudai
They say that when an object is well loved it is eventually imbued with a soul, then what about the array, the trash that resizes a lot? What is that imbued with?

NOTE: We accidentally distributed an older build of the binary. It prints size in place of capacity, but this does not affect the intended solution, so we won’t be updating the attachment.

-printf("Initialized: size=%d capacity=%d\n", pkt->size, pkt->capacity);
+printf("Initialized: size=%d capacity=%d\n", pkt->size, pkt->size);
