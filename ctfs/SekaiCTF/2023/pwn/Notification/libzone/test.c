#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "libzone.h"

#define PERSON "Person"

struct Person;
typedef struct Person* person_t;

struct RefPtr {
	uint32_t ref_count;
	void (*do_rel)(void *object);
	void (*do_ref)(void *object);
};

typedef struct RefPtr RefPtr_t;

struct Person {
	char *name;
	uint32_t age;
	void (*sayhello)(person_t person);
	struct RefPtr ref;
};

void person_ref(person_t person)
{
	person->ref.ref_count++;
}

void sayHello(person_t person)
{
	printf("[%p]Hello %s\n", (void *)person, person->name);
}

void person_rel(person_t person);

person_t person_alloc(const char *name, uint32_t age)
{
	person_t person = (person_t)zone_alloc(PERSON);
	person->name = strdup(name);
	person->age = age;
	person->sayhello = sayHello;
	person->ref.ref_count = 0;
	person->ref.do_ref = (void (*)(void *))person_ref;
	person->ref.do_rel = (void (*)(void *))person_rel;

	return person;
}

void person_rel(person_t person)
{
	if(person->ref.ref_count) return;

	printf("[%p] \"%s\" was freed\n", (void *)person, person->name);
	free(person->name);
	zone_free(PERSON, person);
	// zone_list();
}

int main(int argc, char **argv)
{
	zone_create(PERSON, sizeof(struct Person));

	// person_t new_person = person_alloc("Peter", 23);
	person_t my_class[16];
	person_t my_class2[85*4];
	char name[256];
	int i;

	for(i = 0 ; i < 64 * 3 - 3; i++){
		snprintf(name, sizeof(name), "robot_%d", i);
		my_class2[i] = person_alloc(name, 10);
		my_class2[i]->sayhello(my_class2[i]);
	}

	for(i = 60*2 ; i < 64*3 - 3; i++){
		my_class2[i]->sayhello(my_class2[i]);
		// if(i%2)continue;
		my_class2[i]->ref.do_rel(my_class2[i]);
		my_class2[i] = NULL;
	}

	// new_person->sayhello(new_person);

	for(i = 0 ; i < 16; i++){
		snprintf(name, sizeof(name), "robot_%d", i);
		my_class[i] = person_alloc(name, 10);
		my_class[i]->sayhello(my_class[i]);
	}

#ifdef USEZMALLOC
	char *pbuffer;

	pbuffer = zmalloc(3000);
	printf("zmalloc pbuffer = 0x%lx\n", pbuffer);
	memset(pbuffer, 'A', 3000);
	zfree(pbuffer, 3000);
	printf("zfree pbuffer ok\n");

	zone_list2();
#endif

	// new_person->ref.do_rel(new_person);

	// for(i = 0 ; i < 16; i++){
	// 	my_class[i]->sayhello(my_class[i]);
	// 	// if(i%2)continue;
	// 	my_class[i]->ref.do_rel(my_class[i]);
	// 	my_class[i] = NULL;
	// }

	// zone_list();

	// new_person = person_alloc("Peter", 23);
	// new_person->sayhello(new_person);
	
	// for(i = 0 ; i < 3; i++){
	// 	snprintf(name, sizeof(name), "robot_%d", i);
	// 	my_class[i] = person_alloc(name, 10);
	// 	my_class[i]->sayhello(my_class[i]);
	// }

	// for(i = 0 ; i < 86; i++){
	// 	snprintf(name, sizeof(name), "robot_%d", i);
	// 	my_class2[i] = person_alloc(name, 10);
	// 	my_class2[i]->sayhello(my_class2[i]);
	// }

	// for(i = 0 ; i < 85; i++){
	// 	my_class2[i]->ref.do_rel(my_class2[i]);
	// }

	// zone_list();

	// for(i = 0 ; i < 160; i++){
	// 	snprintf(name, sizeof(name), "Peter_%d", i);
	// 	my_class2[i] = person_alloc(name, 10);
	// 	my_class2[i]->sayhello(my_class2[i]);
	// }

	// zone_list();

	// for(i = 160 - 32 ; i < 160; i++){
	// 	my_class2[i]->ref.do_rel(my_class2[i]);
	// }

	// zone_list();

	// for(i = 160 - 32 ; i < 160; i++){
	// 	snprintf(name, sizeof(name), "Peter_%d", i);
	// 	my_class2[i] = person_alloc(name, 10);
	// 	my_class2[i]->sayhello(my_class2[i]);
	// }

	// zone_list();
	return 0;
}
