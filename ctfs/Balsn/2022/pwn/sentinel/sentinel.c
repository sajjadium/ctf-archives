#define _GNU_SOURCE
#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<fcntl.h>
#include<string.h>
#include<unistd.h>
#include<stddef.h>
#include<sys/prctl.h>
#include<linux/seccomp.h>
#include<linux/filter.h>
#include<linux/unistd.h>
#include<linux/audit.h>
#include<linux/openat2.h>
#include<sys/syscall.h>
#include<sys/socket.h>
#include<errno.h>
#include<sys/ioctl.h>
#include<limits.h>
#include<sys/stat.h>
#include<sys/wait.h>
#include<pthread.h>

#ifdef DO_LOG
  #define LOGPATH "/tmp/log"
#endif

#define REALFLAGPATH "./flag"
#define FAKEFLAGPATH "./fakeFlag"

#define SETSECCOMPRESP(_resp,_err,_val,_flag) {(_resp)->error = (_err);\
                                                 (_resp)->val = (_val);\
                                                 (_resp)->flags = (_flag);}

enum ARGTYPE{
  SIZET,
  CHARPTR
};

void printError(char *msg){
  puts(msg);
  exit(0);
}

void printErrorChild(char *msg){
  puts(msg);
  exit(0);
}

//used to abort hypervisor early in the process in case setup fails
//this must only be called when hypervisor has no more than 1 decendant
void printErrorHypervisor(pid_t pid,char *msg){
  puts(msg);
  fflush(stdout);
  kill(pid,SIGKILL);
  while(true){
    //since it is unsafe to resume after this, just wait until reaper realizes all decendants are gone and commit suicide
    pause();
  }
}

#ifdef DO_LOG
void hypervisorLog(int length,enum ARGTYPE *types,void **args){
  int fd = open(LOGPATH,O_CREAT|O_APPEND|O_RDWR,S_IRUSR|S_IWUSR);
  if(fd==-1) return;
  write(fd,"LOGENTRY >> ",12);
  for(int i=0;i<length;i++){
    switch(types[i]){
      case SIZET:
        dprintf(fd,"%lld",(size_t)args[i]);
        break;
      case CHARPTR:
        write(fd,(char*)args[i],strlen((char*)args[i]));
        break;
      default:
        break;
    }
  }
  write(fd,"\n",1);
  close(fd);
  return;
}
#endif

void *reaper(void *tid){
  *((pid_t*)tid) = gettid();
  pid_t pid;
  while(1){
    pid = wait(NULL);
    if(pid==-1 && errno==ECHILD) break;
  }
  exit(0);
  return NULL;
}

int configureSeccomp() {
  int ret;
  struct sock_filter filter[] = {BPF_STMT(BPF_LD | BPF_W | BPF_ABS,offsetof(struct seccomp_data,arch)),
                                 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,AUDIT_ARCH_X86_64,0,12),
                                 BPF_STMT(BPF_LD | BPF_W | BPF_ABS,offsetof(struct seccomp_data,nr)),
                                 BPF_JUMP(BPF_JMP | BPF_JGE | BPF_K,0x40000000,10,0),
                                 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,__NR_kill,7,0),
                                 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,__NR_tkill,6,0),
                                 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,__NR_tgkill,5,0),
                                 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,__NR_open,4,0),
                                 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,__NR_openat,3,0),
                                 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,__NR_openat2,2,0),
                                 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,__NR_pidfd_open,1,0),
                                 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K,__NR_open_by_handle_at,0,1),
                                 BPF_STMT(BPF_RET | BPF_K,SECCOMP_RET_USER_NOTIF),
                                 BPF_STMT(BPF_RET | BPF_K,SECCOMP_RET_ALLOW),
                                 BPF_STMT(BPF_RET | BPF_K,SECCOMP_RET_KILL)};
  struct sock_fprog prog = {.len = (unsigned short)(sizeof(filter)/sizeof(filter[0])),
                            .filter = filter};
  if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0))
    printError("prctl PR_SET_NO_NEW_PRIVS failed");
  if((ret = syscall(SYS_seccomp,SECCOMP_SET_MODE_FILTER,SECCOMP_FILTER_FLAG_NEW_LISTENER,&prog))==-1)
    printError("seccomp failed");
  return ret;
}

void allocSeccompNotifBuffers(struct seccomp_notif **req,struct seccomp_notif_resp **resp,struct seccomp_notif_sizes *sizes,pid_t pid){
  if(syscall(SYS_seccomp,SECCOMP_GET_NOTIF_SIZES,0,sizes)==-1)
    printErrorHypervisor(pid,"seccomp SECCOMP_GET_NOTIF_SIZES failed");
  *req = malloc(sizes->seccomp_notif);
  if(*req==NULL)
    printErrorHypervisor(pid,"malloc failed");
  size_t resp_size = sizes->seccomp_notif_resp;
  if(sizeof(struct seccomp_notif_resp)>resp_size)
    resp_size = sizeof(struct seccomp_notif_resp);
  *resp = malloc(resp_size);
  if(resp==NULL)
    printErrorHypervisor(pid,"malloc failed");
  return;
}

size_t safeRead(int fd,char *buf,size_t size){
  int res;
  size_t idx = 0;
  while(idx<size){
    int res = read(fd,&buf[idx],size-idx);
    if(res<=0)
      return idx;
    idx+=res;
  }
  return idx;
}

bool fetchMem(pid_t pid,size_t addr,char *buf,size_t size,size_t minSize){
  if(size>PATH_MAX) return false;
  char fname[PATH_MAX+1];
  memset(buf,0,size);
  snprintf(fname,PATH_MAX+1,"/proc/%d/mem",pid);
  int memFd = open(fname,O_RDONLY);
  if(memFd==-1 ||
     lseek(memFd,addr,SEEK_SET)==-1 ||
     safeRead(memFd,buf,size)<minSize){
    perror("fetchMem");
    close(memFd);
    return false;
  }
  close(memFd);
  buf[size] = '\x00';
  return true;
}

bool fetchDirFd(pid_t pid,int *dirFd){
  char procFname[PATH_MAX+1];
  char fname[PATH_MAX+1];
  if((*dirFd-(int)AT_FDCWD)==0){
    sprintf(procFname,"/proc/%d/cwd",pid);
    memset(fname,0,PATH_MAX+1);
    readlink(procFname,fname,PATH_MAX);
    *dirFd = open(fname,O_DIRECTORY|O_RDONLY);
  }
  else{
    sprintf(procFname,"/proc/%d/fd/%d",pid,*dirFd);
    *dirFd = open(procFname,O_RDONLY);
  }
  if(*dirFd==-1)
    return false;
  return true;
}

bool fetchFlagStat(dev_t *flagDev, ino_t *flagIno){
  struct stat fileStat;
  int tmpFd = open(REALFLAGPATH,O_RDONLY);
  if(tmpFd==-1)
    return false;
  if(fstat(tmpFd,&fileStat)==-1)
    return false;
  close(tmpFd);
  *flagDev = fileStat.st_dev;
  *flagIno = fileStat.st_ino;
  return true;
}

void sandbox(int seccompFd,pid_t childPid,pid_t reaperTid){
  enum ARGTYPE logArgType[100];
  void *logArg[100];
  struct seccomp_notif_sizes sizes;
  struct seccomp_notif *req;
  struct seccomp_notif_resp *resp;
  int tmpFd;
  struct stat fileStat;
  dev_t flagDev;
  ino_t flagIno;
  char fname[PATH_MAX+1];
  struct seccomp_notif_addfd addFd;
  pid_t selfPid = getpid();
  allocSeccompNotifBuffers(&req,&resp,&sizes,childPid);

  //up till this point, it is guaranteed that only one child is present, so if anything fails, we can just kill child and call it a day
  //once we enter the while loop, it is point of no return, we can no longer exit hypervisor safely unless all decendants are dead
  while (1){
    memset(req,0,sizes.seccomp_notif);
    //if error occurs here, we have nothing to handle, and since another thread acts as reaper, no point in doing any checks either
    if(ioctl(seccompFd,SECCOMP_IOCTL_NOTIF_RECV,req)==-1)
      continue;
    resp->id = req->id;
    switch(req->data.nr){
      case __NR_kill:
      case __NR_tkill:
      case __NR_tgkill:
      case __NR_pidfd_open:
#ifdef DO_LOG
        {
          logArgType[0] = CHARPTR;
          logArgType[1] = SIZET;
          logArg[0] = (void*)"preparing to check (t/tg)kill/pidfd_open on pid ";
          logArg[1] = (void*)req->data.args[0];
          hypervisorLog(2,logArgType,logArg);
        }
#endif
        if(req->data.args[0]==selfPid || req->data.args[0]==reaperTid){
          SETSECCOMPRESP(resp,-EPERM,-1,0);
#ifdef DO_LOG
          {
            logArgType[0] = CHARPTR;
            logArgType[1] = SIZET;
            logArg[0] = (void*)"blocked (t/tg)kill/pidfd_open on pid ";
            logArg[1] = (void*)req->data.args[0];
            hypervisorLog(2,logArgType,logArg);
          }
#endif
        }
        else{
          SETSECCOMPRESP(resp,0,0,SECCOMP_USER_NOTIF_FLAG_CONTINUE);
        }
        break;
      case __NR_open:
      case __NR_openat:
      case __NR_openat2:
        struct open_how *openHow;
        tmpFd = -1;
        if(fetchMem(req->pid,req->data.args[req->data.nr==__NR_open?0:1],fname,PATH_MAX,1)==false){
          SETSECCOMPRESP(resp,-EACCES,-1,0);
          break;
        }
        //we have to get a local version of dir fd in child
        if(req->data.nr==__NR_openat || req->data.nr==__NR_openat2){
          int dirFd = req->data.args[0];
          if(fetchDirFd(req->pid,&dirFd)==false){
            SETSECCOMPRESP(resp,-EACCES,-1,0);
            break;
          }
          req->data.args[0] = dirFd;
        }
        if(req->data.nr==__NR_openat2){
          openHow = malloc(req->data.args[3]);
          if(openHow==NULL){
            close(req->data.args[0]);
            SETSECCOMPRESP(resp,-EACCES,-1,0);
            break;
          }
          if(fetchMem(req->pid,req->data.args[2],(char*)openHow,req->data.args[3],req->data.args[3])==false){
            close(req->data.args[0]);
            free(openHow);
            SETSECCOMPRESP(resp,-EACCES,-1,0);
            break;
          }
        }
        if((req->data.nr==__NR_open && (tmpFd = open(fname,req->data.args[1],req->data.args[2]))==-1) ||
           (req->data.nr==__NR_openat && (tmpFd = openat(req->data.args[0],fname,req->data.args[2],req->data.args[3]))==-1) ||
           (req->data.nr==__NR_openat2 && (tmpFd = syscall(__NR_openat2,req->data.args[0],fname,openHow,req->data.args[3]))==-1)){
          if(req->data.nr==__NR_openat || req->data.nr==__NR_openat2)
            close(req->data.args[0]);
          if(req->data.nr==__NR_openat2)
            free(openHow);
          SETSECCOMPRESP(resp,-errno,-1,0);
          break;
        }
        if(req->data.nr==__NR_openat || req->data.nr==__NR_openat2)
          close(req->data.args[0]);
        if(fstat(tmpFd,&fileStat)==-1){
          close(tmpFd);
          if(req->data.nr==__NR_openat2)
            free(openHow);
          SETSECCOMPRESP(resp,-EACCES,-1,0);
          break;
        }
#ifdef DO_LOG
        {
          logArgType[0] = CHARPTR;
          logArgType[1] = CHARPTR;
          logArgType[2] = CHARPTR;
          logArg[0] = (void*)"opened file ";
          logArg[1] = (void*)fname;
          logArg[2] = (void*)", preparing to check stat";
          hypervisorLog(3,logArgType,logArg);
        }
#endif
        if(fetchFlagStat(&flagDev,&flagIno)==false){
          SETSECCOMPRESP(resp,-EACCES,-1,0);
          break;
        }
        if(fileStat.st_dev==flagDev && fileStat.st_ino==flagIno){
#ifdef DO_LOG
          {
            logArgType[0] = CHARPTR;
            logArgType[1] = CHARPTR;
            logArgType[2] = CHARPTR;
            logArg[0] = (void*)"blacklisted file ";
            logArg[1] = (void*)fname;
            logArg[2] = (void*)" detected, sabotaging fd";
            hypervisorLog(3,logArgType,logArg);
          }
#endif
          close(tmpFd);
          if((req->data.nr==__NR_open && (tmpFd = open(FAKEFLAGPATH,req->data.args[1],req->data.args[2]))==-1) ||
             (req->data.nr==__NR_openat && (tmpFd = openat(AT_FDCWD,FAKEFLAGPATH,req->data.args[2],req->data.args[3]))==-1) ||
             (req->data.nr==__NR_openat2 && (tmpFd = syscall(__NR_openat2,AT_FDCWD,FAKEFLAGPATH,openHow,req->data.args[3]))==-1)){
            if(req->data.nr==__NR_openat2)
              free(openHow);
            SETSECCOMPRESP(resp,-errno,-1,0);
            break;
          }
        }
        addFd.id = req->id;
        addFd.flags = SECCOMP_ADDFD_FLAG_SEND;
        addFd.srcfd = tmpFd;
        addFd.newfd = 0;
        if(req->data.nr==__NR_openat2){
          addFd.newfd_flags = openHow->flags&O_CLOEXEC;
          free(openHow);
        }
        else
          addFd.newfd_flags = req->data.args[req->data.nr==__NR_open?1:2]&O_CLOEXEC;
        if(ioctl(seccompFd,SECCOMP_IOCTL_NOTIF_ADDFD,&addFd)==-1){
          close(tmpFd);
          if(errno == ENOENT)
            continue;
          else{
            //in case addFd+notif_send failed, we have to explicitly inform the child that the syscall somehow failed  
            SETSECCOMPRESP(resp,-EACCES,-1,0);
            break;
          }
        }
        close(tmpFd);
        continue;
      case __NR_open_by_handle_at:
        struct file_handle *fHandleTmp,*fHandle;
        if((fHandleTmp = malloc(sizeof(struct file_handle)))==NULL){
          SETSECCOMPRESP(resp,-EACCES,-1,0);
          break;
        }
        if(fetchMem(req->pid,req->data.args[1],(char*)fHandleTmp,offsetof(struct file_handle,f_handle),offsetof(struct file_handle,f_handle))==false ||
           offsetof(struct file_handle,f_handle)+fHandleTmp->handle_bytes<offsetof(struct file_handle,f_handle) ||
           (fHandle = realloc(fHandleTmp,offsetof(struct file_handle,f_handle)+fHandleTmp->handle_bytes))==NULL){
          free(fHandleTmp);
          SETSECCOMPRESP(resp,-EACCES,-1,0);
          break;
        }
        if(fetchMem(req->pid,req->data.args[1]+offsetof(struct file_handle,f_handle),(char*)(&(fHandle->f_handle)),fHandle->handle_bytes,fHandle->handle_bytes)==false){
          free(fHandle);
          SETSECCOMPRESP(resp,-EACCES,-1,0);
          break;
        }
        int dirFd = req->data.args[0];
        if(fetchDirFd(req->pid,&dirFd)==false){
          free(fHandle);
          SETSECCOMPRESP(resp,-EACCES,-1,0);
          break;
        }
        req->data.args[0] = dirFd;
        if((tmpFd = open_by_handle_at(req->data.args[0],fHandle,req->data.args[2]))==-1){
          close(req->data.args[0]);
          free(fHandle);
          SETSECCOMPRESP(resp,-errno,-1,0);
          break;
        }
#ifdef DO_LOG
        {
          logArgType[0] = CHARPTR;
          logArg[0] = (void*)"opened handle, preparing to check stat";
          hypervisorLog(1,logArgType,logArg);
        }
#endif
        close(req->data.args[0]);
        free(fHandle);
        if(fstat(tmpFd,&fileStat)==-1){
          close(tmpFd);
          SETSECCOMPRESP(resp,-EACCES,-1,0);
          break;
        }
        if(fetchFlagStat(&flagDev,&flagIno)==false){
          SETSECCOMPRESP(resp,-EACCES,-1,0);
          break;
        }
        if(fileStat.st_dev==flagDev && fileStat.st_ino==flagIno){
#ifdef DO_LOG
          {
            logArgType[0] = CHARPTR;
            logArg[0] = (void*)"blacklisted file detected, sabotaging fd";
            hypervisorLog(1,logArgType,logArg);
          }
#endif
          close(tmpFd);
          if((tmpFd = open(FAKEFLAGPATH,req->data.args[2]))==-1){
            SETSECCOMPRESP(resp,-errno,-1,0);
            break;
          }
        }
        addFd.id = req->id;
        addFd.flags = SECCOMP_ADDFD_FLAG_SEND;
        addFd.srcfd = tmpFd;
        addFd.newfd = 0;
        addFd.newfd_flags = req->data.args[2]&O_CLOEXEC;
        if(ioctl(seccompFd,SECCOMP_IOCTL_NOTIF_ADDFD,&addFd)==-1){
          close(tmpFd);
          if(errno == ENOENT)
            continue;
          else{
            //in case addFd+notif_send failed, we have to explicitly inform the child that the syscall somehow failed  
            SETSECCOMPRESP(resp,-EACCES,-1,0);
            break;
          }
        }
        close(tmpFd);
        continue;
      default:
        //shouldn't reach here
        SETSECCOMPRESP(resp,-1,-1,0);
        break;
    }
    //if ioctl fails, there's not much we can/have to do, so no point in checking ret value
    ioctl(seccompFd,SECCOMP_IOCTL_NOTIF_SEND,resp);
  }
}

int main(int argc, char* argv[]) {
  int socketfd;
  int serverSd,workerSd,pairSd[2];
  //this is required for hypervisor to check if any descendant process is still alive
  if(prctl(PR_SET_CHILD_SUBREAPER,1,0,0,0)==-1)
    printError("prctl PR_SET_CHILD_SUBREAPER failed");
  if(socketpair(AF_UNIX,SOCK_DGRAM,0,pairSd)<0)
    printError("socket AF_UNIX failed");
  serverSd = pairSd[0];
  workerSd = pairSd[1];

  int pid = fork();
  if(pid<0)
    printError("fork failed");
  if(pid>0){
    //prevent access to parent proc directories, as well as ptracing parent
    if(prctl(PR_SET_DUMPABLE,0)==-1)
      printErrorHypervisor(pid,"prctl PR_SET_DUMPABLE failed");
    //setup reaper to ensure parent commits suicide after no decendants are left
    pthread_t T;
    pid_t reaperTid;
    pthread_create(&T,NULL,reaper,&reaperTid);
    struct msghdr childMsg;
    memset(&childMsg,0,sizeof(childMsg));
    char cmsgbuf[CMSG_SPACE(sizeof(int))];
    childMsg.msg_control = cmsgbuf; // make place for the ancillary message to be received
    childMsg.msg_controllen = sizeof(cmsgbuf);

    int rc = recvmsg(workerSd,&childMsg,0);
    struct cmsghdr *cmsg = CMSG_FIRSTHDR(&childMsg);
    if(cmsg==NULL || cmsg->cmsg_type!=SCM_RIGHTS){
      printErrorHypervisor(pid,"recvmsg received seccompFd corrupted");
      exit(0);
    }
    int seccompFd;
    memcpy(&seccompFd,CMSG_DATA(cmsg),sizeof(seccompFd));
    sandbox(seccompFd,pid,reaperTid);
  }
  else if(pid==0){
    struct msghdr parentMsg;
    struct cmsghdr *cmsg;
    char cmsgbuf[CMSG_SPACE(sizeof(int))];
    int seccompFd = configureSeccomp();

    memset(&parentMsg,0,sizeof(parentMsg));
    parentMsg.msg_control = cmsgbuf;
    parentMsg.msg_controllen = sizeof(cmsgbuf); // necessary for CMSG_FIRSTHDR to return the correct value
    cmsg = CMSG_FIRSTHDR(&parentMsg);
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type = SCM_RIGHTS;
    cmsg->cmsg_len = CMSG_LEN(sizeof(seccompFd));
    memcpy(CMSG_DATA(cmsg),&seccompFd,sizeof(seccompFd));
    parentMsg.msg_controllen = cmsg->cmsg_len; // total size of all control blocks
    if((sendmsg(serverSd,&parentMsg,0))<0)
      printErrorChild("child sendmsg failed");
    char *argv[2] = {"/bin/bash",NULL};
    execve(argv[0],argv,NULL);
  }
  return 0;
}
