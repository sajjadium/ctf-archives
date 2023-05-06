#include "pza999.h"
#include <linux/io.h>

char pza999_driver_name[] = "pza999";
static char pza999_driver_string[] = "PZA 999 Network Driver";
static const char pza999_copyright[] = "Copyright (c) 2021 OOO Corp.";

// prototypes
static int pza999_init_rings(struct pza999_adapter *adapter);
static void pza999_configure_rings(struct pza999_adapter *adapter);
static void pza999_clean_rx_descriptors(struct pza999_adapter *adapter);
static void pza999_clean_tx_descriptors(struct pza999_adapter *adapter);
static int pza999_alloc_rx_descriptors(struct pza999_adapter *adapter);
static int pza999_alloc_tx_descriptors(struct pza999_adapter *adapter, size_t incr);

/* pza999_pci_tbl - PCI Device ID table
 *
 * Just one entry for now
 *
 */
static const struct pci_device_id pza999_pci_tbl[] = {
	{PCI_DEVICE(PCI_VENDOR_ID_PZA, 0x0999)},
	{0,}
};

MODULE_DEVICE_TABLE(pci, pza999_pci_tbl);

static int pza999_probe(struct pci_dev *pdev, const struct pci_device_id *ent);
static void pza999_remove(struct pci_dev *pdev);
static irqreturn_t pza999_interrupt(int irq, void *d);

static struct pci_driver pza999_driver = {
	.name     = pza999_driver_name,
	.id_table = pza999_pci_tbl,
	.probe    = pza999_probe,
	.remove   = pza999_remove
};

u16 pza999_io_read16(struct pza999_adapter *a, unsigned long port)
{
  return inw(a->io_base + port);
}

u32 pza999_io_read32(struct pza999_adapter *a, unsigned long port)
{
  return inl(a->io_base + port);
}

void pza999_io_write16(struct pza999_adapter *a, unsigned long port, uint16_t val)
{
  outw(val, a->io_base + port);
}

void pza999_io_write32(struct pza999_adapter *a, unsigned long port, uint32_t val)
{
  outl(val, a->io_base + port);
}

void pza999_rx_write32(struct pza999_adapter *a,
		       unsigned long offset,
		       unsigned long val) {
  writel(val, a->rx_addr + offset);
}

unsigned long pza999_rx_read32(struct pza999_adapter *a,
		      unsigned long offset) {
  return readl(a->rx_addr + offset);
}

void pza999_tx_write32(struct pza999_adapter *a,
		       unsigned long offset,
		       unsigned long val) {
  writel(val, a->tx_addr + offset);
}

unsigned long pza999_tx_read32(struct pza999_adapter *a,
			       unsigned long offset) {
  return readl(a->tx_addr + offset);
}


void pza999_read_mac_addr(struct pza999_adapter *a) {
  *(u16 *)&a->mac_addr[0] = pza999_io_read16(a, MAC_ADDR1);
  *(u16 *)&a->mac_addr[2] = pza999_io_read16(a, MAC_ADDR2);
  *(u16 *)&a->mac_addr[4] = pza999_io_read16(a, MAC_ADDR3);
}

#define ALIGN_SKB_ADDR(addr) \
  ((((unsigned long)(addr) + (64 - 1)) & ~(64 - 1)) - (unsigned long)(addr))

static inline struct sk_buff *pza999_alloc_skb(unsigned int length,
					       gfp_t gfp_flags)
{
  struct sk_buff *skb;

  skb = alloc_skb(length + 64, gfp_flags);
  if (skb) {
    int offset = ALIGN_SKB_ADDR(skb->data);

    if (offset)
      skb_reserve(skb, offset);
  }

  return skb;
}

// ---------------------------------------------------------
// netdev
// ---------------------------------------------------------

/**
 * pza999_open - called when network interface is made active
 */
int pza999_open(struct net_device *netdev)
{
  struct pza999_adapter *adapter = netdev_priv(netdev);
  struct pci_dev *pdev = adapter->pci;
  int err = 0;

  err = pza999_init_rings(adapter);
  if (err < 0)
    return err;

  // cannot fail
  pza999_configure_rings(adapter);

  // set up recv descriptor lists
  err = pza999_alloc_rx_descriptors(adapter);
  if (err)
    goto init_descriptors_failed;

  // set up interrupt handler
  err = request_irq(adapter->pci->irq, pza999_interrupt, IRQF_SHARED,
		    netdev->name, netdev);

  if (err) {
    goto request_irq_failed;
  }

  // enable interrupt handler
  io_wr32(IMSK, 0);

  // enable packet reception
  netif_start_queue(netdev);

  // signal the link is up
  io_wr32(LNKSTATUS, 1);

  return err;

 request_irq_failed:
  pza999_clean_rx_descriptors(adapter);

 init_descriptors_failed:
  kfree(adapter->rx_r.skbs);
  dma_free_coherent(&pdev->dev,
		    adapter->rx_r.len,
		    adapter->rx_r.virt_base,
		    adapter->rx_r.dma_base);

  kfree(adapter->tx_r.dbases);
  dma_free_coherent(&pdev->dev,
		    adapter->tx_r.len,
		    adapter->tx_r.virt_base,
		    adapter->tx_r.dma_base);

  return err;
}

int pza999_close(struct net_device *netdev)
{
  struct pza999_adapter *adapter = netdev_priv(netdev);
  struct pci_dev *pdev = adapter->pci;

  netif_tx_disable(netdev);

  // disable interrupts
  io_wr32(IMSK, ~0);

  // signal we're going down
  io_wr32(LNKSTATUS, 0);

  free_irq(pdev->irq, netdev);

  pza999_clean_rx_descriptors(adapter);
  pza999_clean_tx_descriptors(adapter);

  kfree(adapter->rx_r.skbs);
  dma_free_coherent(&pdev->dev,
		    adapter->rx_r.len,
		    adapter->rx_r.virt_base,
		    adapter->rx_r.dma_base);

  kfree(adapter->tx_r.dbases);
  dma_free_coherent(&pdev->dev,
		    adapter->tx_r.len,
		    adapter->tx_r.virt_base,
		    adapter->tx_r.dma_base);

  io_wr32(LNKSTATUS, 0);

  return 0;
}

static netdev_tx_t pza999_xmit_frame(struct sk_buff *skb,
				     struct net_device *netdev)
{
  struct pza999_adapter *adapter = netdev_priv(netdev);
  struct pci_dev *pdev = adapter->pci;
  struct tx_ring *tx_r = &adapter->tx_r;
  size_t elem = tx_r->next;
  struct tx_descriptor *tx_d = (struct tx_descriptor *)tx_r->virt_base;
  struct descriptor_base *dbase = &tx_r->dbases[elem];
  size_t new_tail = 0;

  // if the tail is equal to the length we need to clean
  // some bufs and set the tail to 0
  if (tx_r->next == tx_r->cnt) {
    pza999_clean_tx_descriptors(adapter);
    tx_r->next = 0;
    tx_r->tail = 0;
  }

  // we need to allocate more descriptors if the next
  // descriptor to use points to the limit described
  // by the tail
  if (tx_r->next == tx_r->tail) {
    if (pza999_alloc_tx_descriptors(adapter, 1) < 0) {
      pr_err("TX FAILED TO EXPAND DESC CNT\n");
      return NETDEV_TX_OK;
    }
  }

  // now that we have the descriptors, sanity check the skb and
  // write it to the descriptor

  if (skb->len > dbase->len) {
    return NETDEV_TX_OK;
  }

  // copy the skb into the descriptor, update the length and flags
  memcpy(dbase->virt, skb->data, skb->len);

  // sync the dma to the device
  dma_sync_single_for_device(&pdev->dev,
			     dbase->dma,
			     dbase->len,
			     DMA_TO_DEVICE);

  tx_d[tx_r->next].len = skb->len;
  tx_d[tx_r->next].flags = TXPOPD;

  new_tail = ++tx_r->next;
  if (tx_r->next == tx_r->cnt)
    new_tail = 0;

  // tricky thing here, we actually want to report our ->next as the
  // tail pointer to the device, for the tx descriptor our internal ->tail
  // is more like 'allocated up to'
  tx_wr32(TXTLP, new_tail);

  netdev->stats.tx_packets++;
  netdev->stats.tx_bytes += skb->len;

  return NETDEV_TX_OK;
}

static void pza999_set_rx_mode(struct net_device *netdev)
{
  // TODO
  return;
}

static int pza999_set_mac_addr(struct net_device *netdev, void *p)
{
  struct pza999_adapter *adapter = netdev_priv(netdev);
  struct sockaddr *addr = p;

  if (!is_valid_ether_addr(addr->sa_data))
    return -EADDRNOTAVAIL;

  io_wr32(MAC_ADDR1, *(u16 *)&addr->sa_data[0]);
  io_wr32(MAC_ADDR2, *(u16 *)&addr->sa_data[2]);
  io_wr32(MAC_ADDR3, *(u16 *)&addr->sa_data[4]);

  return 0;
}

static void pza999_tx_timeout(struct net_device *netdev,
			     unsigned int __always_unused txqueue)
{
  return;
}

static int pza999_change_mtu(struct net_device *netdev, int new_mtu)
{
  netdev->mtu = new_mtu;
  return 0;
}

static int pza999_ioctl(struct net_device *netdev, struct ifreq *ifr, int cmd)
{
  return -EOPNOTSUPP;
}

static netdev_features_t pza999_fix_features(struct net_device *netdev,
	netdev_features_t features)
{
  // No filter
  return features;
}

static int pza999_set_features(struct net_device *netdev,
			       netdev_features_t features)
{
  netdev_features_t changed = features ^ netdev->features;

  if (!(changed & (NETIF_F_RXCSUM | NETIF_F_RXCSUM)))
    return 0;

  netdev->features = features;

  return 1;
}

static const struct net_device_ops pza999_netdev_ops = {
	.ndo_open = pza999_open,
	.ndo_stop = pza999_close,
	.ndo_start_xmit = pza999_xmit_frame,
	.ndo_set_rx_mode = pza999_set_rx_mode,
	.ndo_set_mac_address = pza999_set_mac_addr,
	.ndo_tx_timeout = pza999_tx_timeout,
	.ndo_change_mtu = pza999_change_mtu,
	.ndo_do_ioctl = pza999_ioctl,
	.ndo_validate_addr = eth_validate_addr,
	.ndo_fix_features = pza999_fix_features,
	.ndo_set_features = pza999_set_features
};

// ---------------------------------------------------------
// software
// ---------------------------------------------------------

static int pza999_init_rings(struct pza999_adapter *adapter)
{
  int err = 0;
  struct pci_dev *pdev = adapter->pci;
  struct rx_ring *rx_r = &adapter->rx_r;
  struct tx_ring *tx_r = &adapter->tx_r;

  rx_r->cnt = RXRING_DESC_CNT;
  rx_r->len = rx_r->cnt * sizeof(struct rx_descriptor);
  rx_r->len = ALIGN(rx_r->len, 4096);

  rx_r->virt_base = dma_alloc_coherent(&pdev->dev,
				       rx_r->len,
				       &rx_r->dma_base,
				       GFP_KERNEL);

  if (!rx_r->virt_base) {
    return -ENOMEM;
  }

  memset(rx_r->virt_base, 0, rx_r->len);
  rx_r->head = rx_r->tail = rx_r->next = 0;

  rx_r->skbs = kcalloc(rx_r->cnt,
		       sizeof(struct sk_buff *),
		       GFP_KERNEL);

  if (!rx_r->skbs) {
    err = -ENOMEM;
    goto cleanup_rx_r;
  }

  pr_info("rx_r.virt_base %p, rx_r.dma_base %llx, rx_r.len %zx\n",
	  rx_r->virt_base,
	  rx_r->dma_base,
	  rx_r->len);

  tx_r->cnt = TXRING_DESC_CNT;
  tx_r->len = tx_r->cnt * sizeof(struct tx_descriptor);
  tx_r->len = ALIGN(tx_r->len, 4096);

  tx_r->virt_base = dma_alloc_coherent(&pdev->dev,
				       tx_r->len,
				       &tx_r->dma_base,
				       GFP_KERNEL);

  if (!tx_r->virt_base) {
    err = -ENOMEM;
    goto cleanup_rx_r_dbases;
  }

  memset(tx_r->virt_base, 0, tx_r->len);
  tx_r->head = tx_r->tail = tx_r->next = 0;

  tx_r->dbases = kcalloc(tx_r->cnt,
			 sizeof(struct descriptor_base),
			 GFP_KERNEL);

  if (!tx_r->dbases) {
    err = -ENOMEM;
    goto cleanup_tx_r;
  }

  pr_info("tx_r.virt_base %p, tx_r.dma_base %llx, tx_r.len %zx\n",
	  tx_r->virt_base,
	  tx_r->dma_base,
	  tx_r->len);

 cleanup_tx_r:
  if (err < 0) {
    dma_free_coherent(&pdev->dev,
		      tx_r->len,
		      tx_r->virt_base,
		      tx_r->dma_base);
  }
 cleanup_rx_r_dbases:
  if (err < 0) {
    kfree(rx_r->skbs);
    rx_r->skbs = NULL;
  }
 cleanup_rx_r:
  if (err < 0) {
    dma_free_coherent(&pdev->dev,
		      rx_r->len,
		      rx_r->virt_base,
		      rx_r->dma_base);
  }

  return err;
}

static void pza999_configure_rings(struct pza999_adapter *adapter)
{
  rx_wr32(RXDAL, ((uint64_t)adapter->rx_r.dma_base & 0xffffffff));
  rx_wr32(RXDAH, ((uint64_t)adapter->rx_r.dma_base >> 32) & 0xffffffff);
  rx_wr32(RXCNT, adapter->rx_r.cnt);
  rx_wr32(RXHDP, adapter->rx_r.head);
  rx_wr32(RXTLP, adapter->rx_r.tail);

  tx_wr32(TXDAL, ((uint64_t)adapter->tx_r.dma_base & 0xffffffff));
  tx_wr32(TXDAH, ((uint64_t)adapter->tx_r.dma_base >> 32) & 0xffffffff);
  tx_wr32(TXCNT, adapter->tx_r.cnt);
  tx_wr32(TXHDP, adapter->tx_r.head);
  tx_wr32(TXTLP, adapter->tx_r.tail);
}

static void pza999_clean_tx_descriptors(struct pza999_adapter *adapter)
{
  struct pci_dev *pdev = adapter->pci;
  struct tx_ring *tx_r = &adapter->tx_r;
  struct descriptor_base *base = &tx_r->dbases[0];
  int i = 0;
  // iterate over all of cnt and free the buffers
  for (i=0;i<tx_r->cnt;i++) {
    dma_unmap_single(&pdev->dev,
		     base->dma,
		     base->len,
		     DMA_TO_DEVICE);
    free_page((unsigned long) base->virt);
    base++;
  }
}

static void pza999_clean_rx_descriptors(struct pza999_adapter *adapter)
{
  struct pci_dev *pdev = adapter->pci;
  struct rx_ring *rx_r = &adapter->rx_r;
  struct rx_descriptor *rx_d = NULL;

  int i = 0;
  for (i=0;i<rx_r->tail;i++) {
    rx_d = rx_r->virt_base + (sizeof(struct rx_descriptor) * i);

    dma_unmap_single(&pdev->dev,
		     rx_d->base,
		     rx_d->len,
		     DMA_FROM_DEVICE);

    kfree_skb(rx_r->skbs[i]);
  }
}

static int pza999_alloc_rx_descriptors(struct pza999_adapter *adapter)
{
  // allocate rx descriptors and assign them bus addresses
  int i = 0;
  int err = 0;
  struct pci_dev *pdev = adapter->pci;
  struct rx_ring *rx_r = &adapter->rx_r;
  struct rx_descriptor *rx_d = NULL;

  // assume all skbs are unfulfilled
  for (i=0;i<rx_r->cnt;i++) {
    // allocate the dest buffer into our book-keeping struct
    struct sk_buff *skb;

    skb = pza999_alloc_skb(RX_SKB_SIZE, GFP_KERNEL);

    if (!skb)
      continue;

    rx_r->skbs[i] = skb;

    skb_put(skb, RX_SKB_SIZE);

    // now write to the descriptor pointed to be tail
    rx_d = rx_r->virt_base +\
      (sizeof(struct rx_descriptor) * rx_r->tail);

    rx_d->base = dma_map_single(&pdev->dev,
				skb->data,
				RX_SKB_SIZE,
				DMA_FROM_DEVICE);

    if (dma_mapping_error(&pdev->dev, rx_d->base)) {
      err = -ENOMEM;
      goto cleanup_descriptors;
    }

    rx_d->len = RX_SKB_SIZE;
    rx_d->flags = 0;

    pr_info("[New Descriptor] %p -> %llx (%x)\n",
	    skb->data,
	    rx_d->base,
	    rx_d->len);

    rx_r->tail++;
  }

  // writeout the new tail
  rx_wr32(RXTLP, rx_r->tail);


 cleanup_descriptors:
  if (err < 0) {
    pr_err("Failed to allocate RX descriptors\n");
    for (i=0;i<rx_r->tail;i++) {
      rx_d = rx_r->virt_base + (sizeof(struct rx_descriptor) * i);

      dma_unmap_single(&pdev->dev,
		       rx_d->base,
		       rx_d->len,
		       DMA_FROM_DEVICE);

      kfree_skb(rx_r->skbs[i]);
    }
  }
  return err;
}

static int pza999_alloc_tx_descriptors(struct pza999_adapter *adapter, size_t incr)
{
  struct pci_dev *pdev = adapter->pci;
  struct tx_ring *tx_r = &adapter->tx_r;
  int elem = tx_r->tail;
  struct tx_descriptor *tx_d = (struct tx_descriptor *)tx_r->virt_base;
  struct tx_descriptor *cur = &tx_d[elem];
  struct descriptor_base *base = &tx_r->dbases[elem];
  int err = 0;
  int i = 0;

  // any calls that attempt to increment past the count we drop
  if (tx_r->tail + incr > tx_r->cnt) {
    return -ENOMEM;
  }

  for(i=0;i<incr;i++) {
    base->len = PAGE_SIZE;
    base->virt = (void *)get_zeroed_page(GFP_KERNEL);
    base->dma = dma_map_single(&pdev->dev,
			       base->virt,
			       base->len,
			       DMA_TO_DEVICE);

    if (dma_mapping_error(&pdev->dev, base->dma)) {
      err = -ENOMEM;
      goto cleanup_descriptors;
    }

    cur->base = base->dma;
    cur->len = PAGE_SIZE;
    cur->flags = 0;

    pr_info("[TX Desc] %p -> %llx (%lx)\n",
	    base->virt,
	    base->dma,
	    base->len);

    base++;
    cur++;
    tx_r->tail++;
  }

 cleanup_descriptors:
  if (err < 0) {
    base = &tx_r->dbases[elem];
    for(i=0;i<incr;i++) {
      dma_unmap_single(&pdev->dev,
		       base->dma,
		       base->len,
		       DMA_TO_DEVICE);
      free_page((unsigned long)base->virt);
      base++;
    }
  }
  return err;
}

static struct sk_buff *pza999_reset_skb(struct pza999_adapter *adapter)
{
  struct rx_ring *rx_r = &adapter->rx_r;
  struct pci_dev *pdev = adapter->pci;
  struct rx_descriptor *desc = (struct rx_descriptor *)rx_r->virt_base;
  struct rx_descriptor *cur = &desc[rx_r->next];
  struct sk_buff *orig_skb = rx_r->skbs[rx_r->next];

  struct sk_buff *reset_skb = pza999_alloc_skb(RX_SKB_SIZE, GFP_ATOMIC);
  if (reset_skb == NULL) {
    return NULL;
  }

  skb_put(reset_skb, RX_SKB_SIZE);
  skb_copy_to_linear_data(reset_skb,
			  (unsigned char *)orig_skb->data,
			  orig_skb->len > RX_SKB_SIZE ? RX_SKB_SIZE : orig_skb->len);

  dma_unmap_single(&pdev->dev,
		   cur->base,
		   orig_skb->len,
		   DMA_FROM_DEVICE);

  cur->base = dma_map_single(&pdev->dev,
			     reset_skb->data,
			     reset_skb->len,
			     DMA_FROM_DEVICE);

  if (dma_mapping_error(&pdev->dev, cur->base)) {
    kfree_skb(reset_skb);
    return NULL;
  }

  kfree_skb(orig_skb);
  rx_r->skbs[rx_r->next++] = reset_skb;

  return reset_skb;
}

static struct sk_buff *pza999_reassemble_skb(struct pza999_adapter *adapter,
					     size_t *len)
{
  struct rx_ring *rx_r = &adapter->rx_r;
  struct pci_dev *pdev = adapter->pci;  
  struct rx_descriptor *desc = (struct rx_descriptor *)rx_r->virt_base;
  unsigned int n = rx_r->next;
  struct rx_descriptor *cur = &desc[n];
  struct sk_buff *orig_skb = rx_r->skbs[n];
  struct sk_buff *reass_skb = NULL;
  size_t offset, l;

  // first count from rx_next until we hit EOPK
  size_t new_length = 0;
  do {
    cur = &desc[n];
    new_length += cur->len;
    if (++n >= rx_r->tail) {
      n = 0;
    }
  } while (!(cur->flags & RXEOPK));

  reass_skb = pza999_alloc_skb(new_length, GFP_ATOMIC);
  if (reass_skb == NULL) {
    new_length = RX_SKB_SIZE;
    reass_skb = pza999_reset_skb(adapter);
    if (reass_skb == NULL) {
      return NULL;
    }

    goto clear_descriptors;
  }

  n = rx_r->next;
  offset = 0;
  do {
    cur = &desc[n];
    l = cur->len;
    if (offset >= new_length) {
      break;
    }
    
    if (offset + l > new_length) {
      l = new_length - offset;
    }

    skb_put(reass_skb, l);
    skb_copy_to_linear_data_offset(reass_skb,
				   offset,
				   (unsigned char *)rx_r->skbs[n]->data,
				   l);

    offset += l;
    if (++n >= rx_r->tail) {
      n = 0;
    }
  } while (!(cur->flags & RXEOPK));

  // now remove traces of the old skb
  cur = &desc[rx_r->next];

  // unmap descriptor point
  dma_unmap_single(&pdev->dev,
		   cur->base,
		   orig_skb->len,
		   DMA_FROM_DEVICE);

  // map in new backing to descriptor
  cur->base = dma_map_single(&pdev->dev,
			     reass_skb->data,
			     reass_skb->len,
			     DMA_FROM_DEVICE);

  if (dma_mapping_error(&pdev->dev, cur->base)) {
    kfree_skb(reass_skb);
    return NULL;
  }

  kfree_skb(orig_skb);

  rx_r->skbs[rx_r->next] = reass_skb;

 clear_descriptors:
  // clean up the descriptors we slirped up
  for (cur = &desc[rx_r->next];
       !(cur->flags & RXEOPK);
       cur = &desc[rx_r->next]) {
    cur->flags = 0;
    cur->len = rx_r->skbs[rx_r->next]->len;
    if (++rx_r->next >= rx_r->tail)
      rx_r->next = 0;
  }

  // finally update the EOPK
  cur->flags = 0;
  cur->len = rx_r->skbs[rx_r->next]->len;

  // we don't want to reprocess those we've already assimilated
  *len = new_length;

  return reass_skb;
}

static void pza999_rx(struct net_device *netdev)
{
  struct pza999_adapter *adapter = netdev_priv(netdev);
  struct rx_ring *rx_r = &adapter->rx_r;
  struct rx_descriptor *desc = (struct rx_descriptor *)rx_r->virt_base;
  struct rx_descriptor *cur = &desc[rx_r->next];
  size_t queue_len, len;

  while(cur->flags & RXPOPD) {
    struct sk_buff *skb, *orig_skb;

    orig_skb = rx_r->skbs[rx_r->next];
    if (orig_skb == NULL) {
      goto next;
    }

    dma_rmb();

    queue_len = 0;
    len = cur->len;

    if (abs(rx_r->next - rx_rd32(RXHDP)) > rx_rd32(RXCNT) / 16) {
      queue_len = abs(rx_rd32(RXHDP) - rx_r->next);
      pr_err("SATURATED QUEUE (%zX desc)\n", queue_len);
    }

    if (!(cur->flags & RXEOPK)) {
      // reassembly is required
      // we have a new 'original' skb
      orig_skb = pza999_reassemble_skb(adapter, &len);
      if (orig_skb == NULL) {
	goto next;
      }
    } else {
      // clear the RXPOPD flag
      cur->flags = 0;
      // update the length to original skb to avoid truncating incoming packets
      cur->len = orig_skb->len;
    }

    skb = skb_clone(orig_skb, GFP_ATOMIC);

    if (skb == NULL) {
      goto next;
    }

    skb_trim(skb, len);

    // send it up
    skb->protocol = eth_type_trans(skb, netdev);
    netif_rx(skb);

    // update the descriptor length
    netdev->stats.rx_packets++;
    netdev->stats.rx_bytes += skb->len;

  next:
    if (++rx_r->next >= rx_r->tail) {
      rx_r->next = 0;
    }

    if (queue_len) {
      if (abs(rx_rd32(RXHDP) - rx_r->next) > queue_len) {
	pr_err("DRAIN (%zX desc push)\n", abs(rx_rd32(RXHDP) - rx_r->next) - queue_len);
      } else {
	pr_err("DRAIN (%zX desc pop)\n", queue_len - abs(rx_rd32(RXHDP) - rx_r->next));
      }
    }
    
    cur = &desc[rx_r->next];
  }

  // re-enable interrupts
  io_wr32(IMSK, 0);
}

static irqreturn_t pza999_interrupt(int irq, void *d)
{
  struct net_device *netdev = d;
  struct pza999_adapter *adapter = netdev_priv(netdev);

  uint32_t irsn = io_rd32(IRSN);

  if (unlikely(!irsn))
    return IRQ_NONE;

  io_wr32(IRSN, 0);
  io_wr32(IMSK, ~0);

  if (irsn & RXIRQ)
    pza999_rx(netdev);

  return IRQ_HANDLED;
}

/**
 * pza999_probe - device initialization
 */
static int pza999_probe(struct pci_dev *pdev, const struct pci_device_id *ent)
{
  int err;
  struct net_device *netdev;
  struct pza999_adapter *adapter = NULL;
  int bars;

  bars = pci_select_bars(pdev, IORESOURCE_IO | IORESOURCE_MEM);
  err = pci_enable_device(pdev);

  if (err)
    return err;

  err = pci_request_selected_regions(pdev, bars, pza999_driver_name);
  if (err)
    goto err_pci_reg;

  // allow the device to bus master, aka control DMA
  pci_set_master(pdev);

  err = -ENOMEM;
  netdev = alloc_etherdev(sizeof(struct pza999_adapter));
  if (!netdev)
    goto err_alloc_etherdev;

  // hook up the underlying netdev to the pci structure
  SET_NETDEV_DEV(netdev, &pdev->dev);

  pci_set_drvdata(pdev, netdev);
  adapter = netdev_priv(netdev);
  adapter->pci = pdev;

  err = -EIO;
  if (pci_resource_flags(pdev, 0) & IORESOURCE_IO) {
    adapter->io_base = pci_resource_start(pdev, 0);
  } else {
    goto err_ioremap;
  }

  adapter->tx_addr = pci_ioremap_bar(pdev, 1);
  if (!adapter->tx_addr)
    goto err_ioremap;

  adapter->rx_addr = pci_ioremap_bar(pdev, 2);
  if (!adapter->rx_addr)
    goto err_ioremap;

  pr_info("%s probed and loaded\n", pza999_driver_string);
  pr_info("PIO @ 0x%lx\n", adapter->io_base);
  pr_info("TXMMIO @ %p\n", adapter->tx_addr);
  pr_info("RXMMIO @ %p\n", adapter->rx_addr);

  // configure netdev, linux stuff ripped from e1000
  netdev->netdev_ops = &pza999_netdev_ops;

  strncpy(netdev->name, pci_name(pdev), sizeof(netdev->name) - 1);
  pr_info("PCI Name %s\n", pci_name(pdev));

  // feature flags
  // TODO are these needed?
  netdev->priv_flags |= IFF_SUPP_NOFCS;       // device supports sending custom FCS

  netdev->hw_features |= (NETIF_F_RXCSUM |    // receive checksumming offload
			  NETIF_F_RXALL |     // receive errored frames
			  NETIF_F_RXFCS);     // append fcs to skb pkt data

  netdev->vlan_features |= (NETIF_F_TSO |     // tcpv4 segmentation
			    NETIF_F_HW_CSUM | // checksum all packets
			    NETIF_F_SG);      // scatter/gather io

  // mtu range: 46 - 16110
  netdev->min_mtu = ETH_ZLEN - ETH_HLEN;
  netdev->max_mtu = MAX_JUMBO_FRAME_SIZE - (ETH_HLEN + ETH_FCS_LEN);

  pza999_read_mac_addr(adapter);
  pr_info("MAC %02x%02x%02x%02x%02x%02x\n",
	  adapter->mac_addr[0],
	  adapter->mac_addr[1],
	  adapter->mac_addr[2],
	  adapter->mac_addr[3],
	  adapter->mac_addr[4],
	  adapter->mac_addr[5]);

  memcpy(netdev->dev_addr, adapter->mac_addr, netdev->addr_len);
  if (!is_valid_ether_addr(netdev->dev_addr))
    pr_err("Invalid MAC addr\n");

  strcpy(netdev->name, "eth%d");
  err = register_netdev(netdev);
  if (err)
    goto err_register;

  pr_info("Device done %pM\n", netdev->dev_addr);

  return 0;

err_register:
err_ioremap:
  if (adapter->tx_addr)
    iounmap(adapter->tx_addr);
  if (adapter->rx_addr)
    iounmap(adapter->rx_addr);
  free_netdev(netdev);
err_alloc_etherdev:
  pci_release_selected_regions(pdev, bars);
err_pci_reg:
  if (!adapter)
    pci_disable_device(pdev);
  return err;
}

/**
 * pza999_remove - Device removal
 */
static void pza999_remove(struct pci_dev *pdev)
{
  return;
}

/**
 * pza999_init_module - Driver registration
 *
 * All it does is register with the PCI subsystem
 * 
 */
static int __init pza999_init_module(void)
{
  pr_info("%s\n", pza999_driver_string);

  pr_info("%s\n", pza999_copyright);

  return pci_register_driver(&pza999_driver);
}

module_init(pza999_init_module);

static void __exit pza999_exit_module(void)
{
  ;
}

module_exit(pza999_exit_module);

MODULE_LICENSE("GPL");
