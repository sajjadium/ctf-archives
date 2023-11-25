#include "BDDriver.h"
#include "BDManager.h"
#include "BDRequest.h"
#include "BDVirtualDevice.h"
#include "IDEDriver.h"
#include "kprintf.h"
#include "debug.h"
#include "kstring.h"

BDManager *BDManager::getInstance()
{
  if (!instance_)
    instance_ = new BDManager();
  return instance_;
}


BDManager::BDManager() :
    probeIRQ(false)
{
}

void BDManager::doDeviceDetection(void)
{
  debug(BD_MANAGER, "doDeviceDetection: Detecting BD devices\n");
  IDEDriver id;
  // insert other device detectors here
  debug(BD_MANAGER, "doDeviceDetection:Detection done\n");
}

void BDManager::addRequest(BDRequest* bdr)
{
  if (bdr->getDevID() < getNumberOfDevices())
    getDeviceByNumber(bdr->getDevID())->addRequest(bdr);
  else
    bdr->setStatus(BDRequest::BD_ERROR);
}

void BDManager::addVirtualDevice(BDVirtualDevice* dev)
{
  debug(BD_MANAGER, "addVirtualDevice:Adding device\n");
  dev->setDeviceNumber(device_list_.size());
  device_list_.push_back(dev);
  debug(BD_MANAGER, "addVirtualDevice:Device added\n");
}

void BDManager::serviceIRQ(uint32 irq_num)
{
  debug(BD_MANAGER, "serviceIRQ:Servicing IRQ\n");
  probeIRQ = false;

  for (BDVirtualDevice* dev : device_list_)
    if (dev->getDriver()->irq == irq_num)
    {
      dev->getDriver()->serviceIRQ();
      return;
    }

  debug(BD_MANAGER, "serviceIRQ:End servicing IRQ\n");
}

BDVirtualDevice* BDManager::getDeviceByNumber(uint32 dev_num)
{
  return device_list_[dev_num];
}

BDVirtualDevice* BDManager::getDeviceByName(const char * dev_name)
{
  if(!dev_name)
  {
      return 0;
  }

  debug(BD_MANAGER, "getDeviceByName: %s", dev_name);
  for (BDVirtualDevice* dev : device_list_)
  {
    if (strcmp(dev->getName(), dev_name) == 0)
    {
      debug(BD_MANAGER, "getDeviceByName: %s with id: %d\n", dev->getName(), dev->getDeviceNumber());
      return dev;
    }
  }
  return 0;
}

uint32 BDManager::getNumberOfDevices(void)
{
  return device_list_.size();
}

BDManager* BDManager::instance_ = 0;
