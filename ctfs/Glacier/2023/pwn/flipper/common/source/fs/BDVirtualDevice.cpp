#include "ArchInterrupts.h"
#include "BDDriver.h"
#include "BDRequest.h"
#include "BDVirtualDevice.h"
#include "kstring.h"
#include "debug.h"
#include "kprintf.h"

BDVirtualDevice::BDVirtualDevice(BDDriver * driver, uint32 offset, uint32 num_sectors, uint32 sector_size,
                                 const char *name, bool writable) :
    offset_(offset), num_sectors_(num_sectors), sector_size_(sector_size), block_size_(sector_size),
    writable_(writable), driver_(driver), partition_type_(0), name_(name)
{

  debug(BD_VIRT_DEVICE, "ctor: offset = %d, num_sectors = %d,\n  sector_size = %d, "
        "name = %s \n",
        offset, num_sectors, sector_size, name);
  dev_number_ = 0;
}

void BDVirtualDevice::addRequest(BDRequest * command)
{
  command->setResult(5);
  switch (command->getCmd())
  {
    case BDRequest::BD_GET_BLK_SIZE:
      command->setResult(block_size_);
      command->setStatus(BDRequest::BD_DONE);
      break;
    case BDRequest::BD_GET_NUM_BLOCKS:
      command->setResult(getNumBlocks());
      command->setStatus(BDRequest::BD_DONE);
      break;
    case BDRequest::BD_READ:
    case BDRequest::BD_WRITE:
      //start block and num blocks will be interpreted as start sector and num sectors
      command->setStartBlock(command->getStartBlock() * (block_size_ / sector_size_) + offset_);
      command->setNumBlocks(command->getNumBlocks() * (block_size_ / sector_size_));
      // fall-through
    default:
      command->setResult(driver_->addRequest(command));
      break;
  }
  return;
}


int32 BDVirtualDevice::readData(uint32 offset, uint32 size, char *buffer)
{
  assert(buffer);
  assert(offset % block_size_ == 0 && "we can only read multiples of block_size_ from the device");
  assert(size % block_size_ == 0 && "we can only read multiples of block_size_ from the device");

  assert((offset + size <= getNumBlocks() * block_size_) && "tried reading out of range");

  debug(BD_VIRT_DEVICE, "readData\n");
  uint32 blocks2read = size / block_size_, jiffies = 0;
  uint32 blockoffset = offset / block_size_;

  debug(BD_VIRT_DEVICE, "blocks2read %d\n", blocks2read);
  BDRequest bd(dev_number_, BDRequest::BD_READ, blockoffset, blocks2read, buffer);
  addRequest(&bd);

  if (driver_->irq != 0)
  {
    bool interrupt_context = ArchInterrupts::disableInterrupts();
    ArchInterrupts::enableInterrupts();

    while (bd.getStatus() == BDRequest::BD_QUEUED && jiffies++ < IO_TIMEOUT)
      ArchInterrupts::yieldIfIFSet();

    if (!interrupt_context)
      ArchInterrupts::disableInterrupts();
  }

  if (bd.getStatus() != BDRequest::BD_DONE)
  {
    return -1;
  }
  return size;
}


int32 BDVirtualDevice::writeData(uint32 offset, uint32 size, char *buffer)
{
  assert(offset % block_size_ == 0 && "we can only write multiples of block_size_ to the device");
  assert(size % block_size_ == 0 && "we can only write multiples of block_size_ to the device");

  assert((offset + size <= getNumBlocks() * block_size_) && "tried writing out of range");

  debug(BD_VIRT_DEVICE, "writeData\n");
  uint32 blocks2write = size / block_size_, jiffies = 0;
  uint32 blockoffset = offset / block_size_;

  BDRequest bd(dev_number_, BDRequest::BD_WRITE, blockoffset, blocks2write, buffer);
  addRequest(&bd);

  if (driver_->irq != 0)
  {
    bool interrupt_context = ArchInterrupts::disableInterrupts();
    ArchInterrupts::enableInterrupts();

    while (bd.getStatus() == BDRequest::BD_QUEUED && jiffies++ < IO_TIMEOUT)
      ArchInterrupts::yieldIfIFSet();

    if (!interrupt_context)
      ArchInterrupts::disableInterrupts();
  }

  if (bd.getStatus() != BDRequest::BD_DONE)
    return -1;
  else
    return size;
}


void BDVirtualDevice::setPartitionType(uint8 part_type)
{
  partition_type_ = part_type;
}

uint8 BDVirtualDevice::getPartitionType(void) const
{
  return partition_type_;
}
