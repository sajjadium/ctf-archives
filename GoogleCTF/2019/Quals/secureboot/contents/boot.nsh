echo "If Secure Boot is enabled it will verify kernel's integrity and"
echo "return 'Security Violation' in case of inconsistency."

echo "Booting..."
bzImage console=ttyS0 -initrd=rootfs.cpio.gz
