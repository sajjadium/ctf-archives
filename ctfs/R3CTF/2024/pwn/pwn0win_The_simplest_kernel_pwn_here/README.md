This must be the simplest kernel pwn challenge here, I promise you.

Please pack your exploit into a regular and installable IPA file. And open a ticket to start challenge. You will have 10 minutes to pwn the challenge. During the attempt, you can request any form of restart or environment reset.

Note: Flag is in /var/jb/var/root/flag with -r-------- 1 root wheel.

    We use an iPhone 8 with iOS 16.0 for this challenge.
    Several well-known 1-days have been patched.
    We highly recommend you test your exploitation on jailbroken devices or Corellium or any emulators like t8030-qemu / D22-QEMU first.
    Feel free to ask admin for debug device in case you want to test your proof-of-concept.


Download kernelcache:
```
pzb -g kernelcache.release.iphone10 https://updates.cdn-apple.com/2022FallFCS/fullrestores/012-65931/BD2515B7-7802-4EB4-9377-98E3238EA5A8/iPhone_4.7_P3_16.0_20A362_Restore.ipsw
```

Extract kernelcache:
```
ipsw kernel dec kernelcache.release.iphone10
```

Patches:
```
Vulnerabilities: 
    IOSurfaceRootUserClient::lookup_surface_from_port()
        0xFFFFFFF005B27844: 0xF90002B4
        0xFFFFFFF005B27848: 0xD2800013
    IOSurface::setIndexedTimestamp()
        0xFFFFFFF005B1B83C: 0xF9000022
        0xFFFFFFF005B1B840: 0x52800000
```
