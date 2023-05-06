
/*
 * RACHELL
 *  Really Abnormal Crazy sHELL
 *
 */

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<stdbool.h>

//commands
// ls, mkdir, echo, cat, rm, cd, exit, touch

#define NAMELEN 0x20
#define MAXPATH_LEN 0x100
#define MAXCHILD 0x10
#define SYSBUF 0x5000

typedef enum{       // type of node
    DIR,            // directory
    FIL,            // file
} NTYPE;

struct node{
    NTYPE type;                 // node type 
    struct node *p;             // parent pointer
    struct node *c[MAXCHILD];   // child pointers
    char *name;                 // node name <= NAMELEN
    char *buf;                  // node content
    unsigned int size;          // node content size
};

struct node root;               // root directory
char *sysbuf;                   // buffer which receives command
char username[] = "tsg";        // username
char hostname[] = "ut";         // hostname
struct node *cwd = &root;       // current working directory


void panic(void)
{
    write(1,"exit...\n",7);
    while(true)
        sleep(100);
}

// Read n bytes from stdin and return the num of read.
// "\n" at the end of input would be NULL terminated. 
unsigned long readn(char *buf, unsigned size) {
    unsigned cnt = 0;
    for (unsigned i = 0; i < size; i++) {
        unsigned x = read(0, buf + i, 1);
        cnt += x;
        if (x != 1 || buf[cnt - 1] == '\n') break;
    }
    if (cnt == 0) exit(-1);
    if (buf[cnt - 1] == '\n'){
      buf[cnt - 1] = '\x00';
      --cnt;
    }

    return cnt;
}

// Get a node in the current directory specified by a node name.
struct node *get_node_cur(struct node *parent, const char *name)
{
    if(strcmp(name,".") == 0)
        return parent;
    if(strcmp(name,"..") == 0)
        return parent->p;
    for(int ix=0; ix!=MAXCHILD; ++ix){
        if(parent->c[ix] != NULL && strcmp(parent->c[ix]->name,name) == 0){
            return parent->c[ix];
        }
    }
    return NULL;
}

// Submodule of get_node()
struct node* sub_get_node(char *p, char *c, struct node* start_dir)
{
    struct node* tmp = start_dir;

    while(1==1){
        p = strchr(++c,'/');
        if(p == NULL)
            return get_node_cur(tmp,c);
        else
            *p = '\x00';
        if((tmp = get_node_cur(tmp,c)) == NULL)
            return NULL;
        c = p;
        if(*(++p) == '\x00')
            return tmp;
    }
}

// Get a node specified by a relative path and return its pointer.
// If the node doesn't exist, return NULL.
struct node* get_node(const char *target_path)
{
  char path[MAXPATH_LEN]; 
  if(strlen(target_path) >= MAXPATH_LEN){
      write(1,"too long path\n",14);
      panic();
  }
  strncpy(path,target_path,strlen(target_path));
  path[strlen(target_path)] = '\x00';
  char *c = path;                         // pos
  char *p = strchr(path,'/');             // slash right after c

  if(p == NULL)                           // relative path (cur)
      return get_node_cur(cwd,path);
  
  if(c == p){                             // absolute path
    write(1,"relative path only\n",19);
    return NULL;
  }else if(strncmp(c,"..",2) == 0){       // relative path (parent)
      c += 2;
      if(*c == '\x00' || *(c+1) == '\x00')
          return cwd->p;
      return sub_get_node(p,c,cwd->p);
  }else if(strncmp(c,".",1) == 0){        // relative path (cur)
      c += 1;
      if(*c == '\x00' || *(c+1) == '\x00')
          return cwd;
      return sub_get_node(p,c,cwd);
  }else{                                  // relative path (cur) 
      return sub_get_node(p,c-1,cwd);
  }
  return NULL;
}

// Return the index of empty child entry.
// If the node has MAXCHILD children, returns -1.
char find_first_empty(struct node *n)
{
    for(int ix=0;ix!=MAXCHILD;++ix)
        if(n->c[ix]==NULL)
            return ix;
    return -1;
}

// Check if the name consists only of allowed ASCII chars.
// Return 1 if the name contains only allowed ASCII chars.
// Return 0 otherwise.
// Allowed chars are [\n,-,@,0-9,a-z,A-Z,_,.]
unsigned char ascii_check(const char *name, unsigned int size)
{
    char c;
    for(int ix=0;ix!=size;++ix){
        c = name[ix];
        if(c=='\n' || c=='-' || (0x30<=c && c<=0x39) || (0x40<=c && c<=0x5a) || (0x61<=c && c<=0x7a) || c=='_' || c=='.')
            continue;
        return 0;
    }
    return 1;
}

// Print the name of the node, with ascii_check().
void print_name_with_check(struct node *n){
  if(ascii_check(n->name,strlen(n->name))==1){
    write(1,n->name,strlen(n->name));
  }else{
    panic();
  }
}

// Print the name of children, with ascii_check().
void print_children(struct node *p)
{
  for(int ix=0; ix!=MAXCHILD; ++ix){
    if(p->c[ix]!=NULL){
      print_name_with_check(p->c[ix]);
      write(1,"\n",1);
    }
  }
}

void sub_pwd(struct node *d)
{
    if(d->p == &root){
        write(1,"/",1);
        print_name_with_check(d);
        return;
    }
    sub_pwd(d->p);
    write(1,"/",1);
    write(1,d->name,strlen(d->name));
}

// Show the absolute path of a current directory.
void pwd(void)
{
    sub_pwd(cwd);
}

// "cd" command.
// Absolute path is not supported.
void cd(void)
{
  struct node *target;
  unsigned rs = 0;
  write(1,"path> ",6);
  if((rs = readn(sysbuf,MAXPATH_LEN)) <= 0)
      panic();

  if((target=get_node(sysbuf))==NULL || target->type!=DIR){
    write(1,"no such dir\n",12);
    return;
  }

  cwd = target;
}

// "ls" command.
// Absolute path is not supported.
void ls(void)
{
  struct node *target;
  unsigned rs = 0;
  write(1,"path> ",6);
  if((rs = readn(sysbuf,MAXPATH_LEN)) <= 0)
      panic();

  if((target=get_node(sysbuf))==NULL){
    write(1,"no such file or dir\n",20);
    return;
  }

  if(target->type == DIR)
    print_children(target);
  else{
    print_name_with_check(target);
    write(1,"\n",1);
  }
}

// Create a node in a current directory.
struct node* mk(const char *name, NTYPE type)
{
  int empty = find_first_empty(cwd);

  if(empty == -1){
    write(1,"too many children\n",18);
    return NULL;
  }
  if(get_node_cur(cwd,name)!=NULL){
    write(1,"already exists\n",15);
    return NULL;
  }

  struct node *new = malloc(sizeof(struct node));
  new->name = malloc(NAMELEN+1); 
  strncpy(new->name,name,NAMELEN);
  new->name[strlen(name)] = '\x00';
  new->p = cwd;
  for(int ix=0;ix!=MAXCHILD;++ix)
      new->c[ix] = NULL;
  new->type = type;
  new->buf = NULL;
  new->size = 0;

  cwd->c[find_first_empty(cwd)] = new;
  return new;
}

// Create a dir in a current dir
struct node* mkdir(const char *name)
{
  return mk(name,DIR);
}

// "mkdir" command.
// Absolute path is not supported.
void mkdir_handler(void)
{
  struct node *target;
  unsigned rs = 0;
  write(1,"name> ",6);
  if((rs = readn(sysbuf,NAMELEN)) <= 0)
      panic();

  if(ascii_check(sysbuf,sizeof(sysbuf))==1){
    write(1,"non-ASCII found\n",15);
    panic();
  }

  mkdir(sysbuf);
}

// "cat" command.
// TODO: I have to implement it until the CTF. Otherwise, impossible to solve.
void cat(void)
{
  write(1,"not implemented\n",16);
}

// "touch" command.
// Initiate a node structure, but not its buffer.
void touch(void)
{
  struct node *target;
  struct node *new;
  unsigned rs = 0;
  write(1,"filename> ",10);
  if((rs = readn(sysbuf,NAMELEN)) <= 0)
      panic();

  mk(sysbuf,FIL);
}

// Unlink a specified child from its parent.
void unlink_child(struct node *target)
{
  for(int ix=0;ix!=MAXCHILD;++ix){
    if(target->p->c[ix] == target){
      target->p->c[ix] = NULL;
      return;
    }
  }
  write(1,"unlink failed\n",14);
  panic();
}

// Submodule of rm().
void sub_rm(struct node *target)
{
  if(target == &root){
    write(1,"not allowed\n",12);
    return;
  }
  if(target->p == cwd){
    switch(target->type){
      case FIL:
        if(target->buf != NULL)
          free(target->buf);
        unlink_child(target);
        break;
      case DIR:
        unlink_child(target);
        free(target);
        break;
      default:
        panic();
    }
  }else{
    switch(target->type){
      case FIL:
        if(target->buf != NULL)
          free(target->buf);
        break;
      case DIR:
        unlink_child(target);
        free(target);
        break;
      default:
        panic();
    }
  }
}

// "rm" command.
// Absolute path is not supported.
void rm(void)
{
  struct node *target;
  unsigned rs = 0;
  write(1,"filename> ",10);
  if((rs = readn(sysbuf,MAXPATH_LEN)) <= 0)
      panic();

  if((target = get_node(sysbuf)) == NULL){
    write(1,"no such file or dir\n",20);
    return;
  }

  sub_rm(target);
}

// Write content at buffer of the specified node.
void write2file(struct node *target, const char *content, unsigned size)
{
  if(target->buf == NULL){
    target->buf = malloc(size);
    // find newline
    for(int ix=0; ix!=size; ++ix){
      if(content[ix] == '\r'){
        size = ix;
        break;
      }
    }
    memcpy(target->buf,content,size);
    target->size = size;
  }else{
    if(size > target->size){ // re-allocation
      free(target->buf);
      target->buf = malloc(size+1);
      // find newline
      for(int ix=0; ix!=size; ++ix){
        if(content[ix] == '\r'){
          size = ix;
          break;
        }
      }
      memcpy(target->buf,content,size);
      target->size = size;
    }else{                              // use same buffer
      memcpy(target->buf,content,size);
    }
  }
}

// "echo" command.
// Only this command can be redirected to a file.
//    e.g ) echo Hello,World > memo.txt
void echo(void)
{
  char path[MAXPATH_LEN];
  struct node *target;
  unsigned rs = 0, ss = 0;

  write(1,"arg> ",5);
  if((ss=readn(sysbuf,SYSBUF)) <= 0)
    panic();

  write(1,"redirect?> ",11);
  if((rs = readn(path,MAXPATH_LEN-1)) <= 0)
    panic();

  if(path[0] == 'y' || path[0] == 'Y'){
    write(1,"path> ",6);
    if((rs = readn(path,MAXPATH_LEN-1)) <= 0) 
      panic();

    if((target = get_node(path))!=NULL && target->type==FIL){
      write2file(target,sysbuf,ss);
    }else{
      write(1,"invalid path\n",13);
    }
  }else{
    write(1,sysbuf,strlen(sysbuf));
  }
}

// Show a prompt and read a command.
void prompt(void)
{
    unsigned rs = 0;
    
    write(1,"\n",1);
    write(1,username,strlen(username));
    write(1,"@",1);
    write(1,hostname,strlen(hostname));
    write(1,":",1);
    pwd();
    write(1,"$\n",2);

    // read command
    write(1,"command> ",9);
    if((rs = readn(sysbuf,NAMELEN)) <= 0)
        panic();

    if(strcmp(sysbuf,"pwd")==0){
      pwd();
      write(1,"\n",1);
    }else if(strcmp(sysbuf,"ls")==0){
      ls();
    }else if(strcmp(sysbuf,"mkdir")==0){
      mkdir_handler();
    }else if(strcmp(sysbuf,"cd")==0){
      cd();
    }else if(strcmp(sysbuf,"cat")==0){
      cat();
    }else if(strcmp(sysbuf,"touch")==0){
      touch();
    }else if(strcmp(sysbuf,"exit")==0){
      panic();
    }else if(strcmp(sysbuf,"rm")==0){
      rm();
    }else if(strcmp(sysbuf,"echo")==0){
      echo();
    }else{
      write(1,"unknown command\n",16);
    }
}

// Initiate some files and buffer.
void init(void)
{
    // set sysbuf
    sysbuf = malloc(SYSBUF);

    // create root directory
    root.name = malloc(NAMELEN);
    *(root.name) = '\x00';
    root.p = &root; // the parent of root is root
    root.type = DIR;
    
    char hoge[] = "home";
    char fuga[] = "tmp";
    mkdir(hoge);
    mkdir(fuga);
}

int main(int argc,char *argv[])
{
    init();

    while(1==1){
        prompt();
    }
    return 0;
}
