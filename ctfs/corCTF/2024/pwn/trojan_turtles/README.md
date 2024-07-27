FizzBuzz101

A mysterious person who goes by Tia Jan recently replaced our nested hypervisor's Intel KVM driver with a new driver. Can you take a look at this and see if our systems have been compromised?

Note that the goal of this challenge is to escape from the L2 guest to the root user on the L1 guest. You will need an Intel system with modern VMX extensions to debug this challenge.

The L1 guest is running a 6.9.0 kernel with the provided kconfig below. The L2 guest is running a 5.15.0-107 Ubuntu HWE kernel. You can retrieve the necessary headers from the following links: - https://packages.ubuntu.com/focal/linux-headers-5.15.0-107-generic - https://packages.ubuntu.com/focal-updates/linux-hwe-5.15-headers-5.15.0-107

You can download the 6.9.0 kernel source at https://cdn.kernel.org/pub/linux/kernel/v6.x/patch-6.0.1.xz
