#include "text_decorator.h"


text_block user_text_block = {{0}, 0};


char* red_decorator(char * text)
{
	char* decorated_text = (char*)malloc(strlen(text) + 8);
	sprintf(decorated_text, "\033[0;31m%s\033[0m", text);
	return decorated_text;
}


char* green_decorator(char * text)
{
	char* decorated_text = (char*)malloc(strlen(text) + 8);
	sprintf(decorated_text, "\033[0;32m%s\033[0m", text);
	return decorated_text;
}


char* blue_decorator(char * text)
{
	char* decorated_text = (char*)malloc(strlen(text) + 8);
	sprintf(decorated_text, "\033[0;34m%s\033[0m", text);
	return decorated_text;
}   


char get_char()
{
	char t, c = getchar();
	while((t = getchar()) != '\n' && t != EOF);
	return c;
}


decorator_ptr get_decorator_ptr(char decorator_symbol)
{
	switch (decorator_symbol)
	{
	case 'r':
		return red_decorator;
	case 'g':
		return green_decorator;
	case 'b':
		return blue_decorator;
	default:
		printf("Invalid choice, no decorator will be used.\n");
		return NULL;
	}
}


char get_decorator_symbol(decorator_ptr ptr)
{
	if (ptr == red_decorator)
		return 'r';
	if (ptr == green_decorator)
		return 'g';
	if (ptr == blue_decorator)
		return 'b';
	return DECORATOR_FLAG_ERROR;
}


decorator_ptr choose_decorator_menu()
{
	char decorator_choice = 0;

	printf("Which decorator would you like to use?\n");
	printf("[R]ed / [G]reen / [B]lue\nYour choice: ");
	decorator_choice = tolower(get_char());

	return get_decorator_ptr(decorator_choice);
}


bool add_line(char * line_content, int is_decorator, decorator_ptr decorator)
{
	text_block* block = &user_text_block;
	text_line *line = &block->text_lines[block->current_line_count];
	
	if (block->current_line_count < MAX_LINE_AMOUNT)
	{
		if (is_decorator)
		{
			line->type = DECORATOR;
			if(decorator)
				line->content.decorated.decorator = decorator;
			memcpy(line->content.decorated.text, line_content, MAX_LINE_LENGTH);
		}
		else
		{
			line->type = RAW_TEXT;
			memcpy(line->content.raw_text, line_content, MAX_LINE_LENGTH);
		}
		block->current_line_count++;
		return TRUE;
	}

	return FALSE;
}


void add_line_menu()
{
	text_block* block = &user_text_block;
	char* temp_text = (char*)malloc(MAX_LINE_LENGTH);
	bool is_decorated = FALSE, success = FALSE;

	printf("Enter the text for this line [%d characters max]:\n", MAX_LINE_LENGTH);
	fgets(temp_text, MAX_LINE_LENGTH, stdin);

	printf("Would you like to decorate it [Y/n]? ");
	is_decorated = (tolower(get_char()) == 'y');

	success = add_line(temp_text, is_decorated, ((is_decorated) ? choose_decorator_menu() : NULL));

	if (!success)
		puts("Sorry, you've reached the max line amount.\n");

	free(temp_text);
}


void print_text()
{
	text_block* block = &user_text_block;
	char* decorated_text = NULL;
	int i;

	for (i = 0; i < block->current_line_count; i++)
	{
		text_line* line = &block->text_lines[i];

		if(line->type == DECORATOR)
		{
			if (line->content.decorated.decorator)
			{
				decorated_text = line->content.decorated.decorator(line->content.decorated.text);
				printf("%s", decorated_text);
				free(decorated_text);
			}
			else
			{
				printf("%s", line->content.decorated.text);
			}
		}
		else
		{
			printf("%s", line->content.raw_text);
		}
	}
}


void remove_line()
{
	text_block* block = &user_text_block;

	if(block->current_line_count)
		block->current_line_count--;
	else
		puts("You've nothing to remove.");
}


void load_from_file(char * file_name)
{
	text_block* block = &user_text_block;
	char* content = (char*)malloc(MAX_LINE_LENGTH);
	FILE* file = fopen(file_name, "r");
	bool success = TRUE, is_decorated = FALSE;
	decorator_ptr ptr;
	int length = 0, offset, read_count;

	if (file == NULL)
	{
		puts("Error: file opening error.");
		free(content);
		return;
	}
	
	while (fgets(content, MAX_LINE_LENGTH, file) && success)
	{
		length = strlen(content);

		if (length > 1)
		{
			is_decorated = (length > 2 && content[0] == DECORATOR_FLAG);
			ptr = (is_decorated) ? get_decorator_ptr(content[1]) : NULL;
			offset = (is_decorated) ? 2 : 0;
			content[MAX_LINE_LENGTH - 1] = 0;
			
			success = add_line(content + offset, is_decorated, ptr);
		}
	}

	free(content);
}


void print_banner()
{
	printf("\
  ______          __     ____                             __            \n\
 /_  __/__  _  __/ /_   / __ \\___  _________  _________ _/ /_____  _____\n\
  / / / _ \\| |/_/ __/  / / / / _ \\/ ___/ __ \\/ ___/ __ `/ __/ __ \\/ ___/\n\
 / / /  __/>  </ /_   / /_/ /  __/ /__/ /_/ / /  / /_/ / /_/ /_/ / /    \n\
/_/  \\___/_/|_|\\__/  /_____/\\___/\\___/\\____/_/   \\__,_/\\__/\\____/_/     \n\
                                                                        \n\
			\rNote: this program supports up to %d lines of text.\n\n", MAX_LINE_AMOUNT);
	putchar('\n');
}


void print_menu()
{
	puts("1. Add line");
	puts("2. Print text");
	puts("3. Remove line");
	puts("4. Load example");
	puts("5. Exit");
}


void main_menu()
{
	menu_option user_choice = NONE;

	while (user_choice != EXIT)
	{
		print_menu();
		printf("Your choice: ");
		user_choice = get_char();

		switch (user_choice)
		{
		case ADD_LINE:
			add_line_menu();
			break;
		
		case PRINT_TEXT:
			print_text();
		break;
		
		case REMOVE_LINE:
			remove_line();
			break;

		case EXIT:
			puts("Quiting...");
			break;
		
		case LOAD_EXAMPLE:
			load_from_file("example.bin");
			break;
		
		case EOF:
			return;

		default:
			puts("Invalid choice, please try again.\n");
			break;
		}
	}
}


int main()
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	setuid(geteuid());
	seteuid(geteuid());

	print_banner();
	main_menu();
	return 0;
}

