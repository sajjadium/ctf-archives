#include <linux/errno.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/module.h>
#include <linux/miscdevice.h>
#include <linux/slab.h>
#include"../include/lkgit.h"

hash_object *objects[HISTORY_MAXSZ] = {0};

static int find_by_hash(char *hash) {
	int ix;
	for (ix = 0; ix != HISTORY_MAXSZ; ++ix) {
		if (objects[ix] != NULL && memcmp(hash, objects[ix]->hash, HASH_SIZE) == 0)
			return ix;
	}
	return -1;
}

static void get_hash(char *content, char *buf) {
	int ix,jx;
	unsigned unit = FILE_MAXSZ / HASH_SIZE;
	char c;
	for (ix = 0; ix != HASH_SIZE; ++ix) {
		c = 0;
		for(jx = 0; jx != unit; ++jx) {
			c ^= content[ix * unit + jx];
		}
		buf[ix] = c;
	}
}

static long save_object(hash_object *obj) {
	int ix;
	int dup_ix;
	// first, find conflict of hash
	if((dup_ix = find_by_hash(obj->hash)) != -1) {
		kfree(objects[dup_ix]);
		objects[dup_ix] = NULL;
	}
	// assign object
	for (ix = 0; ix != HISTORY_MAXSZ; ++ix) {
		if (objects[ix] == NULL) {
			objects[ix] = obj;
			return 0;
		}
	}
	return -LKGIT_ERR_UNKNOWN;
}

static long lkgit_hash_object(hash_object *reqptr) {
	long ret = -LKGIT_ERR_UNKNOWN;
	char *content_buf = kzalloc(FILE_MAXSZ, GFP_KERNEL);
	char *message_buf = kzalloc(MESSAGE_MAXSZ, GFP_KERNEL);
	hash_object *req = kzalloc(sizeof(hash_object), GFP_KERNEL);
	if (IS_ERR_OR_NULL(content_buf) || IS_ERR_OR_NULL(message_buf) || IS_ERR_OR_NULL(req))
		goto end;

	if (copy_from_user(req, reqptr, sizeof(hash_object)))
		goto end;

	if (copy_from_user(content_buf, req->content, FILE_MAXSZ)
		|| copy_from_user(message_buf, req->message, MESSAGE_MAXSZ))
		goto end;

	req->content = content_buf;
	req->message = message_buf;
	get_hash(content_buf, req->hash);

	if (copy_to_user(reqptr->hash, req->hash, HASH_SIZE)) {
		goto end;
	}

	ret = save_object(req);

end:
  return ret;
}

static long lkgit_get_object(log_object *req) {
	long ret = -LKGIT_ERR_OBJECT_NOTFOUND;
	char hash_other[HASH_SIZE] = {0};
	char hash[HASH_SIZE];
	int target_ix;
	hash_object *target;
	if (copy_from_user(hash, req->hash, HASH_SIZE))
		goto end;

	if ((target_ix = find_by_hash(hash)) != -1) {
		target = objects[target_ix];
		if (copy_to_user(req->content, target->content, FILE_MAXSZ))
			goto end;

		// validity check of hash
		get_hash(target->content, hash_other);
		if (memcmp(hash, hash_other, HASH_SIZE) != 0)
			goto end;

		if (copy_to_user(req->message, target->message, MESSAGE_MAXSZ))
			goto end;
		if (copy_to_user(req->hash, target->hash, HASH_SIZE)) 
			goto end;
		ret = 0;
	}

end:
	return ret;
}

static long lkgit_amend_message(log_object *reqptr) {
	long ret = -LKGIT_ERR_OBJECT_NOTFOUND;
	char buf[MESSAGE_MAXSZ];
	log_object req = {0};
	int target_ix;
	hash_object *target;
	if(copy_from_user(&req, reqptr->hash, HASH_SIZE))
		goto end;

	if ((target_ix = find_by_hash(req.hash)) != -1) {
		target = objects[target_ix];
		// save message temporarily
		if (copy_from_user(buf, reqptr->message, MESSAGE_MAXSZ))
			goto end;
		// return old information of object
		ret = lkgit_get_object(reqptr);
		// amend message
		memcpy(target->message, buf, MESSAGE_MAXSZ);
	}

	end:
		return ret;
}

static long lkgit_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
	switch(cmd){
		case LKGIT_HASH_OBJECT:
			return lkgit_hash_object((hash_object *)arg);
		case LKGIT_GET_OBJECT:
			return lkgit_get_object((log_object*)arg);
		case LKGIT_AMEND_MESSAGE:
			return lkgit_amend_message((log_object*)arg);
		default:
			return -LKGIT_ERR_UNIMPLEMENTED;
		};
}

static const struct file_operations lkgit_fops = {
	.owner = THIS_MODULE,
	.unlocked_ioctl = lkgit_ioctl,
};

static struct miscdevice lkgit_device = {
	.minor = MISC_DYNAMIC_MINOR,
	.name = "lkgit",
	.fops = &lkgit_fops,
};

static int __init lkgit_init(void) {
	return misc_register(&lkgit_device);
}

static void __exit lkgit_exit(void) {
	misc_deregister(&lkgit_device);
}

module_init(lkgit_init);
module_exit(lkgit_exit);
MODULE_AUTHOR("TSGCTF");
MODULE_LICENSE("GPL");