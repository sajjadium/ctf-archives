#ifndef _PZA999_H_
#define _PZA999_H_

#include <asm/io.h>
#include <linux/stddef.h>
#include <linux/module.h>
#include <linux/string.h>
#include <linux/types.h>
#include <linux/pci.h>
#include <linux/netdevice.h>
#include <linux/etherdevice.h>
#include <linux/ioport.h>
#include <linux/dma-mapping.h>
#include <linux/mm.h>
#include <linux/gfp.h>

#define PCI_VENDOR_ID_PZA 0x505a

#define MAX_JUMBO_FRAME_SIZE 0x3f00

#define RXRING_DESC_CNT 64
#define TXRING_DESC_CNT 64

#define RX_SKB_SIZE (64 * 3)

// IRQ enablement
#define RXIRQ 1

// Descriptor flags
#define RXPOPD 1
#define TXPOPD 2
#define RXEOPK 4

// PIO registers
#define MAC_ADDR1 0
#define MAC_ADDR2 2
#define MAC_ADDR3 4
#define LNKSTATUS 8
#define IRSN      12
#define IMSK      16

// RX registers
#define RXDAL 0 // Rx Desc Address Lo
#define RXDAH 1 // Rx Desc Address Hi
#define RXCNT 2 // Rx Desc Length
#define RXHDP 3 // Rx Head Pointer
#define RXTLP 4 // Rx Tail Pointer

// TX registers
#define TXDAL 0 // Tx Desc Address Lo
#define TXDAH 1 // Tx Desc Address Hi
#define TXCNT 2 // Tx Desc Length
#define TXHDP 3 // Tx Head Pointer
#define TXTLP 4 // Tx Tail Pointer

#define io_rd32(R)    pza999_io_read32(adapter, R)
#define io_wr32(R, V) pza999_io_write32(adapter, R, V)
#define rx_wr32(R, V) pza999_rx_write32(adapter, R * 4, V)
#define tx_wr32(R, V) pza999_tx_write32(adapter, R * 4, V)
#define rx_rd32(R)    pza999_rx_read32(adapter, R * 4)
#define tx_rd32(R)    pza999_tx_read32(adapter, R * 4)

#undef pr_fmt
#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt

extern char pza999_driver_name[];

// contains the vaddr and dma addr of a descriptor
// without this there isn't a good descriptor vbase to pbase mapping
struct descriptor_base {
  void *virt;
  dma_addr_t dma;
  size_t len;
};

struct tx_ring {
  void *virt_base;
  dma_addr_t dma_base;

  // book keeping list of descriptor bases
  struct descriptor_base *dbases;

  size_t len;
  size_t cnt;

  uint32_t head;
  uint32_t tail;
  uint32_t next; // next to drain
};

struct rx_ring {
  void *virt_base;
  dma_addr_t dma_base;

  struct sk_buff **skbs;

  size_t len;
  size_t cnt;

  uint32_t head;
  uint32_t tail;
  uint32_t next;
};

struct rx_descriptor {
  dma_addr_t base;
  uint32_t len;
  uint8_t flags;
  uint8_t pad[3];
};

struct tx_descriptor {
  dma_addr_t base;
  uint32_t len;
  uint8_t flags;
  uint8_t pad[3];
};

struct pza999_adapter {
  // Parent
  struct pci_dev *pci;

  // IO regions
  unsigned long io_base;
  u8 __iomem *tx_addr;
  u8 __iomem *rx_addr;

  // MAC
  u8 mac_addr[6];

  // Ring buffers
  struct rx_ring rx_r;
  struct tx_ring tx_r;
};

#endif
