#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

typedef enum {
	TYPE_EMPTY = 0,
	TYPE_ARRAY = 0xfeed0001,
	TYPE_STRING,
	TYPE_UINT,
	TYPE_FLOAT,
} type_t;

typedef struct {
	type_t type;

	union {
		struct Array *p_arr;
		struct String *p_str;
		uint64_t v_uint;
		double v_float;
	};
} data_t;

typedef struct Array {
	size_t count;
	data_t data[];
} arr_t;

typedef struct String {
	size_t size;
	char *content;
} str_t;

static int create(data_t *data);
static int edit(data_t *data);
static int show(data_t *data, unsigned level, bool recur);
static int remove_recursive(data_t *data);
static int getnline(char *buf, int size);
static int getint(void);
static double getfloat(void);

__attribute__((constructor))
static int init(){
	alarm(60);
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	return 0;
}

int main(void){
	data_t *root = (data_t*)calloc(1, sizeof(data_t));

	for(;;){
		printf("\nMENU\n"
				"1. Edit\n"
				"2. List\n"
				"0. Exit\n"
				"> ");

		switch(getint()){
			case 1:
				edit(root);
				break;
			case 2:
				puts("\nList Data");
				show(root, 0, true);
				break;
			default:
				goto end;
		}
	}

end:
	puts("Bye.");
	return 0;
}

static int create(data_t *data){
	if(!data || data->type != TYPE_EMPTY)
		return -1;

	printf("Select type: [a]rray/[v]alue\n"
		   "> ");

	char t;
	scanf("%c%*c", &t);
	if(t == 'a') {
		printf("input size: ");
		size_t count = getint();
		if(count > 0x10){
			puts("too big!");
			return -1;
		}

		arr_t *arr = (arr_t*)calloc(1, sizeof(arr_t)+sizeof(data_t)*count);
		if(!arr)
			return -1;
		arr->count = count;

		data->type = TYPE_ARRAY;
		data->p_arr = arr;
	}
	else {
		char *buf, *endptr;

		printf("input value: ");
		scanf("%70m[^\n]%*c", &buf);
		if(!buf){
			getchar();
			return -1;
		}

		uint64_t v_uint = strtoull(buf, &endptr, 0);
		if(!endptr || !*endptr){
			data->type = TYPE_UINT;
			data->v_uint = v_uint;
			goto fin;
		}

		double v_float = strtod(buf, &endptr);
		if(!endptr || !*endptr){
			data->type = TYPE_FLOAT;
			data->v_float = v_float;
			goto fin;
		}

		str_t *str = (str_t*)malloc(sizeof(str_t));
		if(!str){
			free(buf);
			return -1;
		}
		str->size = strlen(buf);
		str->content = buf;
		buf = NULL;

		data->type = TYPE_STRING;
		data->p_str = str;

fin:
		free(buf);
	}

	return 0;
}

static int edit(data_t *data){
	if(!data)
		return -1;

	printf("\nCurrent: ");
	show(data, 0, false);

	switch(data->type){
		case TYPE_ARRAY:
			{
				arr_t *arr = data->p_arr;

				printf("index: ");
				unsigned idx = getint();
				if(idx > arr->count)
					return -1;

				printf("\n"
						"1. Update\n"
						"2. Delete\n"
						"> ");

				switch(getint()){
					case 1:
						edit(&arr->data[idx]);
						break;
					case 2:
						remove_recursive(&arr->data[idx]);
						break;
				}
			}
			break;
		case TYPE_STRING:
			{
				str_t *str = data->p_str;
				printf("new string (max:%ld bytes): ", str->size);
				getnline(str->content, str->size+1);
			}
			break;
		case TYPE_UINT:
		case TYPE_FLOAT:
			remove_recursive(data);
		default:
			create(data);
			break;
	}

	return 0;
}

static int remove_recursive(data_t *data){
	if(!data)
		return -1;

	switch(data->type){
		case TYPE_ARRAY:
			{
				arr_t *arr = data->p_arr;
				for(int i=0; i<arr->count; i++)
					if(remove_recursive(&arr->data[i]))
						return -1;
				free(arr);
			}
			break;
		case TYPE_STRING:
			{
				str_t *str = data->p_str;
				free(str->content);
				free(str);
			}
			break;
	}
	data->type = TYPE_EMPTY;

	return 0;
}

static int show(data_t *data, unsigned level, bool recur){
	if(!data)
		return -1;

	switch(data->type){
		case TYPE_EMPTY:
			puts("<EMPTY>");
			break;
		case TYPE_ARRAY:
			{
				arr_t *arr = data->p_arr;
				printf("<ARRAY(%ld)>\n", arr->count);
				if(recur || !level)
					for(int i=0; i<arr->count; i++){
						printf("%*s", level*4, "");
						printf("[%02d] ", i);
						if(show(&arr->data[i], level+1, recur))
							return -1;
					}
			}
			break;
		case TYPE_STRING:
			{
				str_t *str = data->p_str;
				printf("<S> %.*s\n", (int)str->size, str->content);
			}
			break;
		case TYPE_UINT:
			printf("<I> %ld\n", data->v_uint);
			break;
		case TYPE_FLOAT:
			printf("<F> %lf\n", data->v_float);
			break;
		default:
			puts("<UNKNOWN>");
			exit(1);
	}

	return 0;
}

static int getnline(char *buf, int size){
	int len;

	if(size <= 0 || (len = read(STDIN_FILENO, buf, size-1)) <= 0)
		return -1;

	if(buf[len-1]=='\n')
		len--;
	buf[len] = '\0';

	return len;
}

static int getint(void){
	char buf[0x10] = {};

	getnline(buf, sizeof(buf));
	return atoi(buf);
}

static double getfloat(void){
	char buf[0x10] = {};

	getnline(buf, sizeof(buf));
	return atof(buf);
}
