#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/mutex.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/miscdevice.h>
#include <linux/uaccess.h>
#include <linux/random.h>
#include <crypto/hash.h>
#include <linux/types.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/net.h>
#include <linux/in.h>
#include <linux/skbuff.h>
#include <linux/ip.h>
#include <linux/inet.h>
#include <linux/tcp.h>
#include <linux/udp.h>


MODULE_AUTHOR("FizzBuzz and D3v17");
#ifdef EASY_MODE
MODULE_DESCRIPTION("Fire of Salvation");
#endif
#ifndef EASY_MODE
MODULE_DESCRIPTION("Wall of Perdition");
#endif
MODULE_LICENSE("GPL");



#define DEVICE_NAME "firewall"
#define CLASS_NAME  "firewall"

#define ADD_RULE 0x1337babe
#define DELETE_RULE 0xdeadbabe
#define EDIT_RULE 0x1337beef
#define SHOW_RULE 0xdeadbeef
#define DUP_RULE 0xbaad5aad

#define ERROR -1
#define SUCCESS 0
#define MAX_RULES 0x80

#define INBOUND 0
#define OUTBOUND 1
#define SKIP -1

#ifdef EASY_MODE
#define DESC_MAX 0x800
#endif

typedef struct
{
    char iface[16];
    char name[16];
    char ip[16];
    char netmask[16];
    uint8_t idx;
    uint8_t type;
    uint16_t proto;
    uint16_t port;
    uint8_t action;
    #ifdef EASY_MODE
    char desc[DESC_MAX];
    #endif
} user_rule_t;

typedef struct
{
    char iface[16];
    char name[16];
    uint32_t ip;
    uint32_t netmask;
    uint16_t proto;
    uint16_t port;
    uint8_t action;
    uint8_t is_duplicated;
    #ifdef EASY_MODE
    char desc[DESC_MAX];
    #endif
} rule_t;

rule_t **firewall_rules_in;
rule_t **firewall_rules_out;

static DEFINE_MUTEX(firewall_lock);

static long firewall_ioctl(struct file *file, unsigned int cmd, unsigned long arg);
static uint32_t firewall_inbound_hook(void *priv, struct sk_buff *skb, const struct nf_hook_state *state);
static uint32_t firewall_outbound_hook(void *priv, struct sk_buff *skb, const struct nf_hook_state *state);
static uint32_t process_rule(struct sk_buff *skb, rule_t *rule, uint8_t type, int i);
static long firewall_add_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx);
static long firewall_delete_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx);
static long firewall_edit_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx);
static long firewall_show_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx);
static long firewall_dup_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx);

static struct miscdevice firewall_device;
static struct file_operations firewall_fops = {.unlocked_ioctl = firewall_ioctl};

static struct nf_hook_ops in_hook = {
  .hook        = firewall_inbound_hook,
  .hooknum     = NF_INET_PRE_ROUTING,
  .pf          = PF_INET,
  .priority    = NF_IP_PRI_FIRST
};

static struct nf_hook_ops out_hook = {
  .hook        = firewall_outbound_hook,
  .hooknum     = NF_INET_POST_ROUTING,
  .pf          = PF_INET,
  .priority    = NF_IP_PRI_FIRST
};


static long firewall_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
    int ret;
    user_rule_t user_rule;
    rule_t **firewall_rules;

    mutex_lock(&firewall_lock);
    memset(&user_rule, 0, sizeof(user_rule_t));

    if (copy_from_user((void *)&user_rule, (void *)arg, sizeof(user_rule_t)))
    {
        printk(KERN_INFO "[Firewall::Error] firewall_ioctl() cannot copy user request!\n");
        mutex_unlock(&firewall_lock);
        return ERROR;
    }

    if (user_rule.idx >= MAX_RULES)
    {
        printk(KERN_INFO "[Firewall::Info] firewall_ioctl() invalid index!\n");
        mutex_unlock(&firewall_lock);
        return ERROR;
    }

    if ((user_rule.type != INBOUND) && (user_rule.type != OUTBOUND))
    {
        printk(KERN_INFO "[Firewall::Error] firewall_ioctl() invalid rule type!\n");
        mutex_unlock(&firewall_lock);
        return ERROR;
    }

    firewall_rules = (user_rule.type == INBOUND) ? firewall_rules_in : firewall_rules_out;

    switch (cmd)
    {
        case ADD_RULE:
            ret = firewall_add_rule(user_rule, firewall_rules, user_rule.idx);
            break;

        case DELETE_RULE:
            ret = firewall_delete_rule(user_rule, firewall_rules, user_rule.idx);
            break;

        case SHOW_RULE:
            ret = firewall_show_rule(user_rule, firewall_rules, user_rule.idx);
            break;

        case EDIT_RULE:
            ret = firewall_edit_rule(user_rule, firewall_rules, user_rule.idx);
            break;

        case DUP_RULE:
            ret = firewall_dup_rule(user_rule, firewall_rules, user_rule.idx);
            break;

        default:
            ret = ERROR;
            break;
    }

    mutex_unlock(&firewall_lock);

    return ret;
}


static long firewall_add_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx)
{
    printk(KERN_INFO "[Firewall::Info] firewall_add_rule() adding new rule!\n");

    if (firewall_rules[idx] != NULL)
    {
        printk(KERN_INFO "[Firewall::Error] firewall_add_rule() invalid rule slot!\n");
        return ERROR;
    }

    firewall_rules[idx] = (rule_t *)kzalloc(sizeof(rule_t), GFP_KERNEL);

    if (!firewall_rules[idx])
    {
        printk(KERN_INFO "[Firewall::Error] firewall_add_rule() allocation error!\n");
        return ERROR;
    }

    memcpy(firewall_rules[idx]->iface, user_rule.iface, 16);
    memcpy(firewall_rules[idx]->name, user_rule.name, 16);

    #ifdef EASY_MODE
    strncpy(firewall_rules[idx]->desc, user_rule.desc, DESC_MAX);
    #endif

    if (in4_pton(user_rule.ip, strnlen(user_rule.ip, 16), (u8 *)&(firewall_rules[idx]->ip), -1, NULL) == 0)
    {
        printk(KERN_ERR "[Firewall::Error] firewall_add_rule() invalid IP format!\n");
        kfree(firewall_rules[idx]);
        firewall_rules[idx] = NULL;
        return ERROR;
    }

    if (in4_pton(user_rule.netmask, strnlen(user_rule.netmask, 16), (u8 *)&(firewall_rules[idx]->netmask), -1, NULL) == 0)
    {
        printk(KERN_ERR "[Firewall::Error] firewall_add_rule() invalid Netmask format!\n");
        kfree(firewall_rules[idx]);
        firewall_rules[idx] = NULL;
        return ERROR;
    }

    firewall_rules[idx]->proto = user_rule.proto;
    firewall_rules[idx]->port = ntohs(user_rule.port);
    firewall_rules[idx]->action = user_rule.action;
    firewall_rules[idx]->is_duplicated = 0;

    printk(KERN_ERR "[Firewall::Info] firewall_add_rule() new rule added!\n");

    return SUCCESS;
}


static long firewall_delete_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx)
{
    printk(KERN_INFO "[Firewall::Info] firewall_delete_rule() deleting rule!\n");

    if (firewall_rules[idx] == NULL)
    {
        printk(KERN_INFO "[Firewall::Error] firewall_delete_rule() invalid rule slot!\n");
        return ERROR;
    }

    kfree(firewall_rules[idx]);
    firewall_rules[idx] = NULL;

    return SUCCESS;
}


static long firewall_edit_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx)
{
    printk(KERN_INFO "[Firewall::Info] firewall_edit_rule() editing rule!\n");

    #ifdef EASY_MODE
    printk(KERN_INFO "[Firewall::Error] Note that description editing is not implemented.\n");
    #endif

    if (firewall_rules[idx] == NULL)
    {
        printk(KERN_INFO "[Firewall::Error] firewall_edit_rule() invalid idx!\n");
        return ERROR;
    }

    memcpy(firewall_rules[idx]->iface, user_rule.iface, 16);
    memcpy(firewall_rules[idx]->name, user_rule.name, 16);

    if (in4_pton(user_rule.ip, strnlen(user_rule.ip, 16), (u8 *)&(firewall_rules[idx]->ip), -1, NULL) == 0)
    {
        printk(KERN_ERR "[Firewall::Error] firewall_edit_rule() invalid IP format!\n");
        return ERROR;
    }

    if (in4_pton(user_rule.netmask, strnlen(user_rule.netmask, 16), (u8 *)&(firewall_rules[idx]->netmask), -1, NULL) == 0)
    {
        printk(KERN_ERR "[Firewall::Error] firewall_edit_rule() invalid Netmask format!\n");
        return ERROR;
    }

    firewall_rules[idx]->proto = user_rule.proto;
    firewall_rules[idx]->port = ntohs(user_rule.port);
    firewall_rules[idx]->action = user_rule.action;

    printk(KERN_ERR "[Firewall::Info] firewall_edit_rule() rule edited!\n");

    return SUCCESS;
}


static long firewall_show_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx)
{
    printk(KERN_INFO "[Firewall::Error] Function not implemented.\n");
    return ERROR;
}


static long firewall_dup_rule(user_rule_t user_rule, rule_t **firewall_rules, uint8_t idx)
{
    uint8_t i;
    rule_t **dup;

    printk(KERN_INFO "[Firewall::Info] firewall_dup_rule() duplicating rule!\n");

    dup = (user_rule.type == INBOUND) ? firewall_rules_out : firewall_rules_in;

    if (firewall_rules[idx] == NULL)
    {
        printk(KERN_INFO "[Firewall::Error] firewall_dup_rule() nothing to duplicate!\n");
        return ERROR;
    }

    if (firewall_rules[idx]->is_duplicated)
    {
        printk(KERN_INFO "[Firewall::Info] firewall_dup_rule() rule already duplicated before!\n");
        return ERROR;
    }

    for (i = 0; i < MAX_RULES; i++)
    {
        if (dup[i] == NULL)
        {
            dup[i] = firewall_rules[idx];
            firewall_rules[idx]->is_duplicated = 1;
            printk(KERN_INFO "[Firewall::Info] firewall_dup_rule() rule duplicated!\n");
            return SUCCESS;
        }
    }

    printk(KERN_INFO "[Firewall::Error] firewall_dup_rule() nowhere to duplicate!\n");

    return ERROR;
}


static uint32_t process_rule(struct sk_buff *skb, rule_t *rule, uint8_t type, int i)
{
    struct iphdr *iph;
    struct tcphdr *tcph;
    struct udphdr *udph;

    printk(KERN_INFO "[Firewall::Info] rule->iface: %s...\n", rule->iface);
    printk(KERN_INFO "[Firewall::Info] skb->dev->name: %s...\n", skb->dev->name);

    if (strncmp(rule->iface, skb->dev->name, 16) != 0)
    {
        printk(KERN_INFO "[Firewall::Error] Rule[%d], inferface doesn't match, skipping!\n", i);
        return SKIP;
    }

    iph = ip_hdr(skb);

    if (type == INBOUND)
    {
        if ((rule->ip & rule->netmask) != (iph->saddr & rule->netmask))
        {
            printk(KERN_INFO "[Firewall::Error] Rule[%d], ip->saddr doesn't belong to the provided subnet, skipping!\n", i);
            return SKIP;
        }
    }
    else
    {
        if ((rule->ip & rule->netmask) != (iph->daddr & rule->netmask))
        {
            printk(KERN_INFO "[Firewall::Error] Rule[%d], ip->daddr doesn't belong to the provided subnet, skipping!\n", i);
            return SKIP;
        }
    }

    if ((rule->proto == IPPROTO_TCP) && (iph->protocol == IPPROTO_TCP))
    {
        printk(KERN_INFO "[Firewall::Info] Rule[%d], protocol is TCP\n", i);

        tcph = tcp_hdr(skb);

        if ((rule->port != 0) && (rule->port != tcph->dest))
        {
            printk(KERN_INFO "[Firewall::Error] Rule[%d], rule->port (%d) != tcph->dest (%d), skipping!\n", i, ntohs(rule->port), ntohs(tcph->dest));
            return SKIP;
        }

        if ((rule->action != NF_DROP) && (rule->action != NF_ACCEPT))
        {
            printk(KERN_INFO "[Firewall::Error] Rule[%d], invalid action (%d), skipping!\n", i, rule->action);
            return SKIP;
        }

        printk(KERN_INFO "[Firewall::Info] %s Rule[%d], action %d\n", (type == INBOUND) ? "Inbound" : "Outbound", i, rule->action);

        return rule->action;
    }

    else if ((rule->proto == IPPROTO_UDP) && (iph->protocol == IPPROTO_UDP))
    {
        printk(KERN_INFO "[Firewall::Info] Rule[%d], protocol is UDP\n", i);

        udph = udp_hdr(skb);

        if ((rule->port != 0) && (rule->port != udph->dest))
        {
            printk(KERN_INFO "[Firewall::Error] Rule[%d], rule->port (%d) != udph->dest (%d), skipping!\n", i, ntohs(rule->port), ntohs(udph->dest));
            return SKIP;
        }

        if ((rule->action != NF_DROP) && (rule->action != NF_ACCEPT))
        {
            printk(KERN_INFO "[Firewall::Error] Rule[%d], invalid action (%d), skipping!\n", i, rule->action);
            return SKIP;
        }

        printk(KERN_INFO "[Firewall::Info] %s Rule[%d], action %d\n", (type == INBOUND) ? "Inbound" : "Outbound", i, rule->action);

        return rule->action;
    }

    return SKIP;
}


static uint32_t firewall_inbound_hook(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
    int i;
    uint32_t ret;

    for (i = 0; i < MAX_RULES; i++)
    {
        if (firewall_rules_in[i])
        {
            ret = process_rule(skb, firewall_rules_in[i], INBOUND, i);

            if (ret != SKIP)
                return ret;
        }
    }

    return NF_ACCEPT;
}


static uint32_t firewall_outbound_hook(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
    int i;
    uint32_t ret;

    for (i = 0; i < MAX_RULES; i++)
    {
        if (firewall_rules_out[i])
        {
            ret = process_rule(skb, firewall_rules_out[i], OUTBOUND, i);

            if (ret != SKIP)
                return ret;
        }
    }

    return NF_ACCEPT;
}


static int init_firewall(void)
{
    mutex_init(&firewall_lock);

    firewall_device.minor = MISC_DYNAMIC_MINOR;
    firewall_device.name = DEVICE_NAME;
    firewall_device.fops = &firewall_fops;

    if (misc_register(&firewall_device))
    {
        printk(KERN_INFO "[Firewall::Error] Device registration failed!\n");
        return ERROR;
    }

    printk(KERN_INFO "[Firewall::Init] Initializing firewall...\n");

    firewall_rules_in = kzalloc(sizeof(void *) * MAX_RULES, GFP_KERNEL);
    firewall_rules_out = kzalloc(sizeof(void *) * MAX_RULES, GFP_KERNEL);

    if (nf_register_net_hook(&init_net, &in_hook) < 0)
    {
        printk(KERN_INFO "[Firewall::Error] Cannot register nf hook!\n");
        return ERROR;
    }

    if (nf_register_net_hook(&init_net, &out_hook) < 0)
    {
        printk(KERN_INFO "[Firewall::Error] Cannot register nf hook!\n");
        return ERROR;
    }

    printk(KERN_INFO "[Firewall::Init] Firewall initialized!\n");
    #ifdef EASY_MODE
    printk(KERN_INFO "[Firewall::Init] 👼 Welcome to Easy Mode 👼\n");
    #else
    printk(KERN_INFO "[Firewall::Init] 😈 Welcome to Hard Mode 😈\n");
    #endif
    return SUCCESS;
}


static void cleanup_firewall(void)
{
    int i;

    printk(KERN_INFO "[Firewall::Exit] Cleaning up...\n");

    for (i = 0; i < MAX_RULES; i++)
    {
        if (firewall_rules_in[i] != NULL)
        {
            kfree(firewall_rules_in[i]);
        }

        if (firewall_rules_out[i] != NULL)
        {
            kfree(firewall_rules_out[i]);
        }
    }

    memset(firewall_rules_in, 0, sizeof(void *) * MAX_RULES);
    memset(firewall_rules_out, 0, sizeof(void *) * MAX_RULES);

    kfree(firewall_rules_in);
    firewall_rules_in = NULL;

    kfree(firewall_rules_out);
    firewall_rules_out = NULL;

    nf_unregister_net_hook(&init_net, &in_hook);
    nf_unregister_net_hook(&init_net, &out_hook);

    misc_deregister(&firewall_device);
    mutex_destroy(&firewall_lock);

    printk(KERN_INFO "[Firewall::Exit] Cleanup done, bye!\n");
}


module_init(init_firewall);
module_exit(cleanup_firewall);
