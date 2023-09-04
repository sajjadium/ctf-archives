/*
 * Author: peter
 * Balanced Tree Implemenation
 */
#include "bltree.h"
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#define max(a, b) (a > b ? a : b)

void BLTNodeInit(BLNode_t a_node)
{
	a_node->height = 1;
	a_node->left = NULL;
	a_node->right = NULL;
}

BLNode_t BLTRotateRight(BLNode_t parent, BLNode_t a_node)
{
	if(!a_node)
		return parent;

	/*
			 parent                    a_node
			/	   \        ->       /         \
		a_node	    Y               X          parent
		/ 	\                                 /      \
		X	 Z	                             Z        Y
	*/
	parent->left = a_node->right;
	a_node->right = parent;

	parent->height = 1 + max(BLNHEIGHT(parent->left), BLNHEIGHT(parent->right));
	a_node->height = 1 + max(BLNHEIGHT(a_node->left), BLNHEIGHT(a_node->right));
	
	return a_node;
}

BLNode_t BLTRotateLeft(BLNode_t parent, BLNode_t a_node)
{
	if(!a_node)
		return parent;
	/*
			parent                          a_node
		/      \                          /      \
		X       a_node         ->       parent    Z
				/    \                  /     \
				Y     Z                X     Y
	*/
	parent->right = a_node->left;
	a_node->left = parent;


	parent->height = 1 + max(BLNHEIGHT(parent->left), BLNHEIGHT(parent->right));
	a_node->height = 1 + max(BLNHEIGHT(a_node->left), BLNHEIGHT(a_node->right));

	return a_node;
}

BLNode_t BLTInsert(BLNode_t root, BLNode_t a_node, int (*cmp)(BLNode_t, BLNode_t))
{
	int64_t balance;
    int res;

	if(!root || !a_node){
		// empty tree
		return a_node;
	}

	res = cmp(a_node, root);
	if(res < 0){
		root->left = BLTInsert(root->left, a_node, cmp);
	} else if(res > 0){
		root->right = BLTInsert(root->right, a_node, cmp);
	} else {
		// don't insert equal node to this tree
		return root;
	}

	// update root
	root->height = 1 + max(BLNHEIGHT(root->left), BLNHEIGHT(root->right));
	balance = BLNBALANCE(root);

	res = cmp(a_node, root->left);
	if(balance > 1 && res < 0){
		// case 1: left's height > right's height and root->left's value > a_node's value
		root = BLTRotateRight(root, root->left);
	}

	if(balance > 1 && res >= 0){
		// case 3: left's height > right's height and root->left's value <= a_node's value
		root->left = BLTRotateLeft(root->left, root->left->right);
		root = BLTRotateRight(root, root->left);
	}
    
	res = cmp(a_node, root->right);
	if(balance < -1 && res > 0) {
		// case 2: left's height < right's height and root->right's value < a_node's value
		root = BLTRotateLeft(root, root->right);
	}

	if(balance < -1 && res <= 0){
		// case 4: left's height < right's height and root->right's value >= a_node's value
		root->right = BLTRotateRight(root->right, root->right->left);
		root = BLTRotateLeft(root, root->right);
	}

	return root;
}

BLNode_t findMinValueNode(BLNode_t node)
{
	BLNode_t cur = node;

	while(cur->left != NULL)
		cur = cur->left;
	
	return cur;
}

BLNode_t BLTDelete(BLNode_t root, BLNode_t a_node, 
		int (*cmp)(BLNode_t, BLNode_t), void (*deallocObject)(BLNode_t),
		void (*swap)(BLNode_t, BLNode_t))
{
	BLNode_t select_node;
	int64_t balance;
    int res;

	if(!root)
		return NULL;
	
	if(!a_node)
		return root;

    res = cmp(a_node, root);
	if(res < 0){
		root->left = BLTDelete(root->left, a_node, cmp, deallocObject, swap);
	}else if(res > 0){
		root->right = BLTDelete(root->right, a_node, cmp, deallocObject, swap);
	} else {
		// found node
		if(!root->left && !root->right){
			// this node is the bottom node
			deallocObject(root);
			return NULL;
		}

		if(root->left && root->right){
			// delete a node has 2 childs
			select_node = findMinValueNode(root->right);
			swap(select_node, root);
			root->right = BLTDelete(root->right, select_node, cmp, deallocObject, swap);
		} else {
			// delete a node only has one child
			select_node = root->left != NULL ? root->left : root->right;
			deallocObject(root);
			return select_node;
		}
	}
	
	// re-balance the tree after delete a node
	root->height = 1 + max(BLNHEIGHT(root->left), BLNHEIGHT(root->right));
	balance = BLNBALANCE(root);

	if(balance < -1 && BLNBALANCE(root->right) < 0){
		// case 1: balance root < -1 and BLNBALANCE(root->right) > 0
		root = BLTRotateLeft(root, root->right);
	}

	if(balance > 1 && BLNBALANCE(root->left) > 0){
		// case 2: balance root > 1 and BLNBALANCE(root->left) > 0
		root = BLTRotateRight(root, root->left);
	}

	if(balance < -1 && BLNBALANCE(root->right) > 0){
		// case 3: balance root < -1 and BLNBALANCE(root->right) < 0
		root->right = BLTRotateRight(root->right, root->right->left);
		root = BLTRotateLeft(root, root->right);
	}

	if(balance > 1 && BLNBALANCE(root->left) < 0){
		// case 4: balance root > 1 and BLNBALANCE(root->left) < 0
		root->left = BLTRotateLeft(root->left, root->left->right);
		root = BLTRotateRight(root, root->left);
	}

	return root;
}

BLNode_t BLTSearch(BLNode_t root, BLNode_t a_node, int (*cmp)(BLNode_t, BLNode_t))
{
	int res = 0;

	if(!a_node || !root)
		return NULL;
    
    res = cmp(a_node, root);
	if(res < 0){
		return BLTSearch(root->left, a_node, cmp);
	}else if(res > 0){
		return BLTSearch(root->right, a_node, cmp);
	} else {
		return root;
	}
}

void BLTWalk(BLNode_t root, void (*callback)(BLNode_t))
{
	if(!root){
		return;
	}
	
	callback(root);

	if(root->left)
		BLTWalk(root->left, callback);
	
	if(root->right)
		BLTWalk(root->right, callback);
}

uint32_t BLTIsBalance(BLNode_t root)
{
	int64_t balance;
	if(!root)
		return 0;

	if(!root->left && !root->right){
		return 0;
	}

	balance = BLTIsBalance(root->left);
	if(balance)
		return balance;

	balance = BLTIsBalance(root->right);
	if(balance)
		return balance;

	balance = BLNHEIGHT(root->left) - BLNHEIGHT(root->right);
	if(balance > 1 && balance < -1)
		return balance;
	
	return 0;
}

BLNode_t BLTDestroy(BLNode_t root, void (*deallocObject)(BLNode_t))
{
	if(!root)
		return NULL;
	
	if(root->left)
		root->left = BLTDestroy(root->left, deallocObject);
	
	if(root->right)
		root->right = BLTDestroy(root->right, deallocObject);

	deallocObject(root);
	return NULL;
}
