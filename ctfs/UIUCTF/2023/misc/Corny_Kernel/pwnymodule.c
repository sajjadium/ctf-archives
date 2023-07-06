// SPDX-License-Identifier: GPL-2.0-only

#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt

#include <linux/module.h>
#include <linux/init.h>
#include <linux/kernel.h>

extern const char *flag1, *flag2;

static int __init pwny_init(void)
{
	pr_alert("%s\n", flag1);
	return 0;
}

static void __exit pwny_exit(void)
{
	pr_info("%s\n", flag2);
}

module_init(pwny_init);
module_exit(pwny_exit);

MODULE_AUTHOR("Nitya");
MODULE_DESCRIPTION("UIUCTF23");
MODULE_LICENSE("GPL");
MODULE_VERSION("0.1");
