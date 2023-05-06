#include <stdlib.h>
#include <stdio.h>

#define NB_PAGE 20

typedef struct quote_t quote_t;
struct quote_t
{
    char * content;
    unsigned int content_size;
    char * title;
    unsigned int title_size;
    void (*write)(quote_t *);
    void (*read)(quote_t *);
};

quote_t * book[NB_PAGE];
unsigned int book_ctr;

void quote_write(quote_t * quote)
{
    printf("Content > ");
    fgets(quote->content, quote->content_size, stdin);
    quote->content[quote->content_size - 2] = '\n';
}

void quote_read(quote_t * quote)
{
    printf("[+] %s", quote->title);
    printf("[>] %s", quote->content);
}

int get_choice(const char * question)
{
    char buffer[100];
    int choice = -1;
    printf("%s > ", question);
    fgets(buffer, 100, stdin);
    if(sscanf(buffer, "%d", &choice) != 1)
    {
        return -1;
    }
    return choice;
}

int menu()
{
    int choice = -1;
    puts("\n-:: Menu ::-");
    puts("1- List quotes");
    puts("2- Add a quote");
    puts("3- Display a quote");
    puts("4- Edit a quote");
    puts("5- Delete a quote");
    puts("6- Exit");
    return get_choice("Choice number");
}

void list_quotes()
{
    for(int i = 0; i < book_ctr; i++)
    {
        printf("[%d] - %s", i + 1, book[i]->title);
    }   
}

void add_quote()
{
    int choice1 = -1;
    int choice2 = -1;
    if(book_ctr >= NB_PAGE)
    {
        puts("[!] Error : too much quotes !");
    }
    else
    {
        quote_t * quote = malloc(sizeof(quote_t));
        choice1 = get_choice("Title size");
        choice2 = get_choice("Content size");
        if(choice1 <= 0 || choice2 <= 0)
        {
            puts("[!] Error : bad size !");
            free(quote);
        }
        else
        {
            quote->title_size = choice1 + 2;
            quote->content_size = choice2 + 2;
            quote->content = malloc(quote->content_size);
            quote->title = malloc(quote->title_size);
            quote->read = quote_read;
            quote->write = quote_write;

            printf("Title > ");
            fgets(quote->title, quote->title_size, stdin);
            quote->title[quote->title_size - 2] = '\n';
            printf("Content > ");
            fgets(quote->content, quote->content_size, stdin);
            quote->content[quote->content_size - 2] = '\n';

            book[book_ctr] = quote;
            book_ctr++;
        }
    }
}

void display_quote()
{
    int choice = get_choice("Quote number");
    if(choice < 1 || choice >= book_ctr + 1)
    {
        puts("[!] Error : wrong quote number !");
    }
    else
    {
        book[choice - 1]->read(book[choice - 1]);
    }
}

void edit_quote()
{
    int choice = get_choice("Quote number");
    if(choice < 1 || choice >= book_ctr + 1)
    {
        puts("[!] Error : wrong quote number !");
    }
    else
    {
        book[choice - 1]->write(book[choice - 1]);
    }
}

void delete_quote()
{
    int choice = get_choice("Quote number");
    if(choice < 1 || choice >= book_ctr + 1)
    {
        puts("[!] Error : wrong quote number !");
    }
    else
    {
        free(book[choice - 1]);
        book_ctr--;
    }
}

int main()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    book_ctr = 0;

    puts("Welcome to your wonderful quotebook !");
    puts("Here, you can write down the quotes that inspire you so that they are with you forever :3");
    while(1)
    {
        switch(menu())
        {
            case 1:
                list_quotes();
                break;
            case 2:
                add_quote();
                break;
            case 3:
                display_quote();
                break;
            case 4:
                edit_quote();
                break;
            case 5:
                delete_quote();
                break;
            case 6:
                puts("[+] Exiting ...");
                exit(0);
                break;
            default:
                puts("[!] Error : wrong choice !");
                break;
        }
    }

    return 0;
}
