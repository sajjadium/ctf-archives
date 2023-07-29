Provided is everything necessary to solve the challenge, including
the necessary Linux header files for the relevant kernel. If you would
like to pull the headers manually, you will need headers for
linux-hwe-5.15-headers-5.15.0-73.

If you would like to build EDK2 or QEMU for your own debugging
purposes, you can clone the repos to each build folder, and use
(or modify) the provided build scripts.

For EDK2, use commit: 16779ede2d366bfc6b702e817356ccf43425bcc8 (tag edk2-stable202205)

For QEMU, use commit: f7f686b61cf7ee142c9264d2e04ac2c6a96d37f8 (tag v8.0.2, branch stable-8.0)

Some older versions of QEMU (such as the ones in Ubuntu repos) have
weird behavior in features required for this challenge that might make
it unsolvable.

Anyways, good luck and have fun pwning ring -2!
