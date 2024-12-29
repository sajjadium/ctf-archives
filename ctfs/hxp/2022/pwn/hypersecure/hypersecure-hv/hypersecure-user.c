// Copyright (C) 2022? 2023? hxp. License expires after HXP CTF 2022
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#include "hypersecure-user.h"
#include "hypersecure.h"
#include "hypersecure-debug.h"

#include <linux/miscdevice.h>
#include <linux/fs.h>
#include <linux/mm.h>

#include <asm/io.h>

static int hypersecure_user_open(struct inode *node, struct file *f) {
	return 0;
}

static int hypersecure_user_release(struct inode *node, struct file *f) {
	return 0;
}

static long hypersecure_user_ioctl(struct file *f, unsigned int cmd, unsigned long arg) {
	int r;

	// One page should be enough for everybody.
	void *page = kzalloc(0x1000, GFP_KERNEL);
	if (!page) {
		return -ENOMEM;
	}
	if (copy_from_user(page, (void *)arg, 0x1000)) {
		hypersecure_log_msg("Failed to read\n");
		kfree(page);
		return -EFAULT;
	}
	r = hypersecure_write_memory(page, 0x1000);
	if (r != 0) {
		hypersecure_log_msg("Failed to write memory\n");
		kfree(page);
		return -EFAULT;
	}
	kfree(page);

	r = hypersecure_init_and_run();
	if (r < 0) {
		hypersecure_log_msg("Failed to init and run\n");
		return r;
	}

	return 0;
}

static const struct file_operations hypersecure_user_ops = {
	.owner          = THIS_MODULE,
	.release        = hypersecure_user_release,
	.open           = hypersecure_user_open,
	.unlocked_ioctl = hypersecure_user_ioctl,
};

static struct miscdevice hypersecure_user_misc = {
	.minor = MISC_DYNAMIC_MINOR,
	.name = "hypersecure",
	.fops = &hypersecure_user_ops,
};

int hypersecure_register_user_node(void) {
	int r;

	r = misc_register(&hypersecure_user_misc);
	if (r) {
		return r;
	}

	return 0;
}

void hypersecure_deregister_user_node(void) {
	misc_deregister(&hypersecure_user_misc);
}
