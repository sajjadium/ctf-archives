#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

struct entry {
	char valid;
	uint32_t hash;
	uint32_t size;
	char *key;
	char *data;
	struct entry *next;
};

struct mpool {
	void *base;
	size_t cap;
	size_t inuse;
} mp;

struct entry *htb[0x100];

static struct entry *ent_lookup(const char *key);
static uint32_t new_hash (const char *s);
static void htb_link(struct entry *e);
static void init_mpool(struct mpool *p, size_t cap);
static void *alloc(struct mpool *p, size_t size);
static size_t gc(struct mpool *p, size_t ensure);
static size_t estimate_inuse(void);
static void migrate(struct mpool *p);

__attribute__((noreturn))
static void panic (const char *s){
	printf("PANIC : %s\n", s);
	_exit(0);
}

int db_reg(const char *key, const char *data, size_t size){
	struct entry *e;

	if(!(e = ent_lookup(key))){
		if(!(e = (struct entry*)calloc(1, sizeof(struct entry))))
			panic("allocate entry");
		e->hash = new_hash(key);
		e->key = alloc(&mp, strlen(key)+1);
		strcpy(e->key, key);
		htb_link(e);
	}
	e->valid = 1;

	if(e->size < size || (void*)e->data < mp.base || (void*)e->data > mp.base + mp.inuse){
		e->size = 0;
		e->data = alloc(&mp, size);
	}
	e->size = size;
	memcpy(e->data, data, size);

	return 1;
}

char *db_get(const char *key, size_t *size){
	struct entry *e;

	if(!(e = ent_lookup(key)) || !e->valid)
		return NULL;

	if((void*)e->data < mp.base || (void*)e->data > mp.base + mp.inuse)
		panic("Out of memory pool");

	if(size)
		*size = e->size;
	return e->data;
}

int db_del(const char *key){
	struct entry *e;

	if(!(e = ent_lookup(key)) || !e->valid)
		return 0;

	e->valid = 0;
	return 1;
}

static struct entry *ent_lookup(const char *key){
	struct entry *e;
	uint32_t hash;

	hash = new_hash(key);
	for(e = htb[hash & 0xff]; e; e = e->next)
		if(e->hash == hash && !strcmp(e->key, key))
			return e;

	return NULL;
}

static uint32_t new_hash (const char *s){
	uint32_t h = 5381;
	for (uint8_t c = *s; c != '\0'; c = *++s)
		h = h * 33 + c;
	return h & 0xffffffff;
}

static void htb_link(struct entry *e){
	uint32_t idx;

	idx = e->hash & 0xff;
	e->next = htb[idx];
	htb[idx] = e;
}

static void init_mpool(struct mpool *p, size_t cap){
	if(!p || !(p->base = malloc(cap)))
		panic("allocate memory pool");
	p->cap = cap;
	p->inuse = 0;
}

static void *alloc(struct mpool *p, size_t size){
	void *mem;

	if(p->inuse + size > p->cap && gc(p, size) < size)
		return NULL;

	mem = p->base + p->inuse;
	p->inuse += size;

	return mem;
}

static size_t gc(struct mpool *p, size_t ensure){
	struct mpool new;
	size_t inuse, new_size;

	new_size = p->cap ?: 0x80;
	inuse = estimate_inuse();

	if(new_size > 0x80 && inuse + ensure < new_size/4)
		new_size /= 2;
	while(new_size < inuse + ensure)
		new_size *= 2;

	init_mpool(&new, new_size);
	migrate(&new);
	
	free(p->base);
	*p = new;

	return p->cap - p->inuse;
}

static size_t estimate_inuse(void){
	size_t total = 0;

	for(int i=0; i<0x100; i++)
		for(struct entry *e = htb[i]; e; e = e->next)
			total += strlen(e->key)+1 + (e->valid ? e->size : 0);

	return total;
}

static void migrate(struct mpool *p){
	for(int i=0; i<0x100; i++)
		for(struct entry *e = htb[i]; e; e = e->next){
			char *key, *data;

			key = alloc(p, strlen(e->key)+1);
			strcpy(key, e->key);
			e->key = key;

			if(e->valid && e->size > 0){
				data = alloc(p, e->size);
				memcpy(data, e->data, e->size);
				e->data = data;
			}
		}
}
