#pragma once
#include "param.h"
#include "inode.h"

// this is the directory and path name layer

// Write a new direcotry entry (name, inum) to the directory dp
// return 0 on success, return -1 on failed
// called inside op and ip->lock locked
int dirlink(struct inode* dp, const char* name, uint inum);

// Look for a directory entry in a directory.
// If found, set *poff to byte offset of entry.
// called inside op and ip->lock locked
struct inode* dirlookup(struct inode* dp, const char* name, uint* poff);

struct inode* path2inode(const char* path);

struct inode* path2parentinode(const char* path, char* name);

void dirnamencpy(char* a, const char* b);

void dirnamecpy(char* a, const char* b);

const char* skiptoend(const char* path);
