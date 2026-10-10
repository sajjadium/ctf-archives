SR

A three drive NAS lost power partway through writing a sealed report, and nobody had saved the RAID settings. The three drives were pulled and imaged raw before anyone touched the box. The report holds a custody token for a piece of evidence that cannot be reissued, and the write job never finished. Rebuild enough of the array to recover the token. The token is the flag.

You are given three raw drive images, bay0.img, bay1.img, and bay2.img. The flag is in isfcr{...} format.
