Crack my virtual machine :D

Sample command of running the machine:

qemu-system-x86_64 \
  -enable-kvm \
  -machine q35 \
  -m 3024 \
  -smp sockets=1,cores=2,threads=2 \
  -cpu host \
  -drive file=crackme.qcow2,if=virtio,format=qcow2,discard=unmap \
  -device virtio-scsi-pci \
  -netdev user,id=net0 \
  -device virtio-net-pci,netdev=net0 \
  -vga qxl \
  -boot c

Author: UmmIt

 https://drive.proton.me/urls/CE30SCFGDC#UWjKvfJUZRFi

