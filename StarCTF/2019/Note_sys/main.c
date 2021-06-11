#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <string.h>

char *notes[36];
int count = 0;
char **note_to_write = notes;
void *malloc_func(void *arg)
{
	note_to_write ++;
	int tmp = count;
	char *to_copy = (char *)arg;
	tmp += 1;
	//usleep(100000);
	count = tmp;
	if(count > 34)
	{
		printf("too many notes!!\n");
		note_to_write --;
		return 0;
	}
	else
	{
		printf("logged successfully!\n");
		*note_to_write = malloc(256 * sizeof(char));
		memset(*note_to_write, 0, 256);
		memcpy(*note_to_write, to_copy, 250);
		return 0;
	}
}
void *delete_func(void *arg)
{
	char **note_to_delete = note_to_write;
	note_to_write --;
	int tmp = count;
	tmp -= 1;
	usleep(2000000);
	if(count > 0)
	{
		free(*note_to_delete);
		count = tmp;
		printf("delete successfully!\n");
	}
	else
	{
		printf("too less notes!!\n");
		note_to_write ++;
		return 0;
	}
	return 0;
}

int make_note()
{
	int cnt = 250;
	char inputs[256];
	char *ptr = inputs;
	memset(inputs, 0, 256);
	printf("input your note, no more than 250 characters\n");
	while(cnt)
	{
		char tmp;
		tmp = getchar();
		if(tmp != '\n' && tmp!= '\x00' && tmp != '\x90' && tmp )
		{
			*ptr = tmp;
			*ptr ++;
		}
		else
		{
			ptr = NULL;
			break;
		}
		cnt --;
	}
	pthread_t thread_tmp;
	pthread_create(&thread_tmp, NULL, malloc_func, (void*)inputs );
	return 0;
}
int get_total()
{
	printf("the total of notes is %ld\n",count);
	//printf("real : %ld\n",note_to_write - notes);
}
int delete_note()
{
	printf("the last one will be deleted!\n");
	pthread_t thread_tmp;
	pthread_create(&thread_tmp, NULL, delete_func, NULL);
	return 0;
}

int welcome()
{
	char choice = '3';
	printf("welcome to flappypig's note system!\n");
	printf("enter 0 to make a new note\n");
	printf("enter 1 to get the total of notes\n");
	printf("enter 2 to delete a note\n");
	printf("enter 3 to exit\n");
	printf("choice:\n");
	while(1)
	{
		while(1)
		{
			char tmp = getchar();
			if(tmp == '\n')
			{
				break;
			}
			else if(tmp == EOF)
			{
				return 0;
			}
			else
			{
				choice = tmp;
			}
		}
		switch (choice)
		{
			case '0':
				make_note();
				break;
			case '1':
				get_total();
				break;
			case '2':
				delete_note();
				break;
			case '3':
				return 0;
				break;
			default :
				printf("please enter the right choice!\n");
				break;
		}
		printf("choice:\n");
	}
}

int main()
{
	memset(&notes,0,36 * sizeof(char *));
	welcome();
	return 0;
}



/*
int main()
{
	srand(time(0));
	pthread_t id;
	printf("Main thread id is %ld \n",pthread_self());
	while(1)
	{	
		if(!pthread_create(&id,NULL,(void *)thread,NULL))
		{
			printf("succeed!\n");
			//return 0;
		}
		else
		{
			printf("Fail to Create Thread");
			//return -1;
		}
		usleep((rand()%5000));
	}
	return 0;
}
*/
