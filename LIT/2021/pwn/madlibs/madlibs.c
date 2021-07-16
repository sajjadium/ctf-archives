#include <stdio.h>
#include <stdlib.h>                                                                                             
                                                                                                                
void win(){                                                                                                     
	char flag[0x30];                                                                                        
	FILE *f = fopen("flag.txt", "r");                                                                       
	if(f == NULL){                                                                                         
 		puts("Something is wrong. Please contact Rythm.");                                              
 		exit(1);                                                                                        	}                                                                                                      
	fgets(flag, 0x30, f);                                                                                          
	puts("Huh, I guess you did win. How does that even work? Well, here's the flag:");                    
	puts(flag);                                                                                             }                                                                                                               
                                                                                                                
void game(){                                                                                                    
	puts("First, enter a proper noun.");                                                                                                                                                                              
	char noun[0x40];                                                                                       
	scanf("%63s", noun);                                                                                           	puts("");                                                                                                      
        puts("Now, enter an adjective.");                                                                       
                                                                                                                
	char adj[0x40];                                                                                         
	scanf("%63s", adj);                                                                                    
	puts("");                                                                                                                                                                                                           
	puts("Now, I'll combine them into a great sentence!\n");                                                       
        char buf[0x80];                                                                                         	sprintf(buf, "%s is so %s at deepspacewaifu! I wish I were %s like %s", noun, adj, adj, noun);          
                                                                                                        
	puts("The final sentence is:");                                                                         
	printf("\"%s\"\n", buf);                                                                                       	puts("");                                                                                               }                                                                                                               
                                                                                                                
int main(){                                                                                                     
	setbuf(stdout, 0x0);                                                                                   
	setbuf(stderr, 0x0);                                                                                                                                                                                                 
	puts("I made a quick mad libs game!\n");                                                                                                                                                                             
	game();                                                                                                                                                                                                               
	puts("Did you win? Oh wait, I guess it's not really that kind of game.");                                                                                                                                             
	return 0;                                                                                              
}    
