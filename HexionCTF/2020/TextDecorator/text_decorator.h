#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <sys/types.h>
#include <unistd.h>

#define MAX_LINE_AMOUNT 10
#define MAX_LINE_LENGTH 256

#define bool int
#define TRUE 1
#define FALSE 0

#define DECORATOR_FLAG 6
#define DECORATOR_FLAG_ERROR 21


typedef char* (*decorator_ptr)(char*);


typedef enum text_line_type {
	RAW_TEXT,
	DECORATOR
} text_line_type;


typedef enum menu_options {
	NONE = '0',
	ADD_LINE,
	PRINT_TEXT,
	REMOVE_LINE,
	LOAD_EXAMPLE,
	EXIT
} menu_option;


typedef struct text_line {						 
		union {									
				struct {
						decorator_ptr decorator;
						char text[MAX_LINE_LENGTH];
				} decorated;
				char raw_text[MAX_LINE_LENGTH];
		} content;
		text_line_type type;
} text_line;


typedef struct text_block {
	text_line text_lines[MAX_LINE_AMOUNT];
	int current_line_count;
} text_block;


char* red_decorator(char * text);
char* green_decorator(char * text);
char* blue_decorator(char * text);
char get_char();
decorator_ptr get_decorator_ptr(char decorator_symbol);
char get_decorator_symbol(decorator_ptr ptr);
decorator_ptr choose_decorator_menu();
bool add_line(char * line_content, int is_decorator, decorator_ptr decorator);
void add_line_menu();
void print_text();
void remove_line();
void load_from_file(char * file_name);
void save_to_file(char * file_name);
void print_banner();
void print_menu();
void main_menu();

