#include <string>
#include <iostream>
#include <cstdlib>
#include <iomanip>
#include <sstream>
#include <string>
#include <algorithm>
#include <cstdio>
#include <vector>
#include <cstring>
#include <fstream>
#include <sstream>
#include <climits>
#include <regex>
#include <mutex>

#include <sys/ptrace.h> // ptrace
#include <unistd.h> // fork
#include <sys/types.h> // wait
#include <sys/wait.h> //wait
#include <err.h> //err
#include <sys/user.h>
#include <sys/time.h> // getrlimit
#include <sys/resource.h> // setrlimit
#include <unistd.h> // sleep
#include <fcntl.h> 
#include <pwd.h> // getpwnam
#include <grp.h> // setgroups
#include <dirent.h> // opendir
#include <sys/stat.h> // mkdir

// g++ ptrace_64.cpp -O3 -o ptrace_64 -std=c++11 -pthread
// ./ptrace_64 ./call32 gift 1 60 50 blacklist.conf



#define EXIT_CODE_VIOLATION 10
#define EXIT_CODE_REAL_TIME 2
#define EXIT_CODE_MEMORY 11
#define EXIT_CODE_UNHANDLED_SIGNAL 9
#define EXIT_CODE_CPU_TIME 4
#define EXIT_CODE_RUN_TIME_ERROR 3

#define MEM_FOR_LIB 10 // MB

#define DEBUG false
#define ENABLE_LOG 1

// syscall 64
#define SYSCALL_BRK 12
#define SYSCALL_OPEN 2
#define SYSCALL_OPENAT 257

using namespace std;
/*
tam thoi hieu lai cach ptrace hoat dong, de co the giam sat chuong trinh con
    http://eli.thegreenplace.net/2011/01/23/how-debuggers-work-part-1
	https://www.gnu.org/software/libc/manual/html_node/Process-Completion-Status.html
	su dung RLIMIT_DATA khong duoc, ma phai dung RLIMIT_AS

khi TRACEME xong và gọi exec, parent bắt buộc phải attach vào
bản chất của thread_create là clone, nên chỉ có main_thread mới có thể getrusage, hay là waitpid được thôi
Do đó, có thể thử cách sau:
	Cho main_thread tạo ra thread1 -> thread1 tạo ra debuggee
	Như vậy, main_thread có thể waitpid của debuggee, còn thread1 có thể getrusage của debuggee
// sd getrusage không được, vì nó chỉ đưa ra 

mã nguồn get_usage: https://github.com/fho/code_snippets/blob/master/c/getusage.c
*/

struct pstat {
    double utime; // seconds
    double stime; // seconds
    //long unsigned int vsize; // virtual memory size in bytes
};

int global_child_id;
vector<int> global_syscalls;
vector<string> global_black_files;
double global_cpu_time_limit; // seconds
double global_real_time_limit; // seconds
bool global_check_limit_continue = true;
int global_check_limit_rc = -1;
pthread_t global_thread1;
double global_cpu_used = 0;
double global_real_time_elapsed = 0;

void run_target(const string& programname, const char* user, int memLimit);
void run_debugger(const string& pathSyscallList);
char** parseArgs(const string& args);
string hexToString(string mHex);
double getSecs(struct timeval* t);
void mKillChild();
int get_usage(const pid_t pid, struct pstat* result);
string getCString(pid_t child, long addr);

class FileLog {
public:
	FileLog(const char* dir, const char* prefix) {
		if (ENABLE_LOG) {
            // make dir if not exists
            DIR* d = opendir(dir);
            if (d) {
                /* Directory exists. */
                closedir(d);
            } else {
                /* Directory does not exist. */
                if (mkdir(dir, 0750) == -1) {
                    std::cerr << "Error: creating log dir\n";
                    exit(1);
                }
            }

			// get time
			time_t rawtime;
			struct tm * timeinfo;
			char timeBuf[80];

			time (&rawtime);
			timeinfo = localtime(&rawtime);

			strftime(timeBuf,sizeof(timeBuf),".%d-%m-%Y_%I-%M-%S.log",timeinfo);
			std::string file = dir; file += "/"; file += prefix; file += timeBuf;
            // create file with permissions
            int fd = open(file.c_str(), O_RDWR|O_CREAT, 0640);
            if (fd) {
                close(fd);
            } else {
                std::cerr << "Error: creating log file\n";
                exit(1);
            }
			f.open(file.c_str());
		}
	}
	~FileLog() {
		if (ENABLE_LOG) {
			std::lock_guard<std::mutex> lock(mtx);
			f.close();
		}
	}
	template<typename T>
	void log(const T& obj, bool el = true) {
		if (ENABLE_LOG) {
			std::lock_guard<std::mutex> lock(mtx);
			f << obj;
			if (el) f << '\n';
			f.flush();
		}
	}
private:
	std::ofstream f;
	std::mutex mtx;
};

FileLog gLog("/tmp/ptrace", "ptrace");

// Remember to check return values carefully in this function.
// Don't want to accidentally give people root :-)
int drop_privs(const char *username) {
    struct passwd *pw = getpwnam(username);
    if (pw == NULL) {
        gLog.log("Error: User ", false); gLog.log(username, false); gLog.log(" not found");
        return 1;
    }

    if (chdir(pw->pw_dir) != 0) {
        gLog.log("Error: chdir");
        return 1;
    }

    // Don't forget to drop supplemental groups. Forgetting this
    // has led to people escalating to root in some past CTFs :-)
    if (setgroups(0, NULL) != 0) {
        gLog.log("Error: setgroups");
        return 1;
    }

    if (setgid(pw->pw_gid) != 0) {
        gLog.log("Error: setgid");
        return 1;
    }

    if (setuid(pw->pw_uid) != 0) {
        gLog.log("Error: setuid");
        return 1;
    }

    return 0;
}


bool syscallBlackList(int syscall)
{
	for (int i = 0; i < global_syscalls.size(); ++i) {
		if (global_syscalls[i] == syscall) {
			return true;
		}
	}
	return false;
}
bool fileInBlackList(const string& fname) 
{
    // Simple regular expression matching
	char actualpath[PATH_MAX+1];
	if(realpath(fname.c_str(), actualpath)) {
		gLog.log("Open file: ", false); gLog.log(actualpath);
		for(int i = 0; i < global_black_files.size(); ++i) {
			regex txt_regex(global_black_files[i], regex_constants::basic);
			if(regex_match(actualpath, txt_regex)) {
				return true;
			}
		}
	}
	return false;
}

int main(int argc, char** argv)
{
    if (argc != 7) {
        gLog.log("Usage: ", false);
		gLog.log(argv[0], false);
		gLog.log(" exec_path_n_args user cpu_time_limit(seconds - double) real_time_limit(seconds) memory_limit(MB) blacklist_path");
        exit(1);
    }
    string pathNArgs = argv[1];
    char* user = argv[2];
    global_cpu_time_limit = atof(argv[3]);
    int memLimit = atoi(argv[5]);
    global_real_time_limit = atof(argv[4]);
    string pathSyscallList = argv[6];
    global_child_id = fork();
    if (global_child_id == 0)
		// this is the child
        run_target(pathNArgs, user, memLimit);
    else if (global_child_id > 0) {
        run_debugger(pathSyscallList);
    }
    else {
        gLog.log("Error: fork");
        return -1;
    }

    return 0;
}


void run_target(const string& pathNArgs, const char* user, int memLimit)
{
    gLog.log("Target started, will run ", false); gLog.log(pathNArgs);
    /* Allow parent to trace */
    int status = ptrace(PTRACE_TRACEME, 0, 0, 0);
    if (status < 0) {
		gLog.log("Error: cannot be traced");
        exit(1);
    }

    rlimit r;
    
    r.rlim_cur = (memLimit+MEM_FOR_LIB)*1024*1024;
    r.rlim_max = (memLimit+MEM_FOR_LIB)*1024*1024;
    int ret = setrlimit(RLIMIT_AS, &r);
	if (ret) {
		gLog.log("Error: setrlimit");
		exit(1);
    }
    /* Replace this process's image with the given program */
    char** args = parseArgs(pathNArgs);
    int rc = drop_privs(user);
    if (rc == 0) {
	    gLog.log("About to run execv");
	    execv(args[0], args);
	    std::cerr << "Error in execv\n";
    }
}


void mKillChild()
{
	// give child a chance to exit normally
	kill(global_child_id, SIGINT);
	sleep(0);
	kill(global_child_id, 9);
}

double getSecs(struct timeval* t)
{
	return t->tv_sec+t->tv_usec*1.0/1000000;
}

void* checkLimits(void* params)
{
	timeval tvalNow, tvalStart;
	pstat mStat;
	// /*set up real time*/
    gettimeofday(&tvalStart, NULL);
	while(global_check_limit_continue) {
		// /*cpu time*/
		if (get_usage(global_child_id, &mStat) == 0) {
			global_cpu_used = mStat.utime+mStat.stime;
			if (global_cpu_used > global_cpu_time_limit) {
				gLog.log("Timeout cpu time!");
				mKillChild();
				global_check_limit_rc = EXIT_CODE_CPU_TIME;
				break;
			}
		} else {
			// /*file closed => exited*/
			break;
		}
		// /*real time*/
		gettimeofday(&tvalNow, NULL);
		global_real_time_elapsed = getSecs(&tvalNow)-getSecs(&tvalStart);
		// /*<< "elapsed: " << elapsed << "\n";*/
		if (global_real_time_elapsed > global_real_time_limit) {
			gLog.log("Timeout real time!");
			mKillChild();
			global_check_limit_rc = EXIT_CODE_REAL_TIME;
			break;
		}
		sleep(0);
	}
} 

void run_debugger(const string& pathSyscallList)
{
	gLog.log("Debugger started");
	int inSyscall = 0;
	user_regs_struct regs;
	int status;
	/* Wait for child to stop on its first instruction */
	gLog.log("Waiting for debugee");
    pid_t ret;
	// setup
	ret = waitpid(global_child_id, &status, 0); // wait for result iamge of execve
	if (ret == -1 || WIFSTOPPED(status) == 0) {
		gLog.log("Error: waitpid");
		mKillChild();
		exit(1);
	}
	int rc = ptrace(PTRACE_SETOPTIONS, global_child_id, NULL, PTRACE_O_TRACESYSGOOD);
	if (rc) {
		gLog.log("Error: ptrace");
		mKillChild();
		exit(1);
	}
    // get in syscall blacklist
    ifstream ifs (pathSyscallList.c_str(), ifstream::in);
	if (ifs.fail()) {
		gLog.log("Error open log file ", false); gLog.log(pathSyscallList);
		mKillChild();
		exit(1);
	}
	
    int nSyscall, sc;
    ifs >> nSyscall;
	gLog.log("nSyscall = ", false); gLog.log(nSyscall);
    for(int i = 0; i < nSyscall; ++i) {
    	ifs >> sc;
    	global_syscalls.push_back(sc);
		gLog.log(sc, false); gLog.log(" ", false);
    }
	gLog.log("\n", false);
	int nFile, filePath;
	// get in file blacklist
	ifs >> nFile;
	string file;
	ifs.ignore();
	for(int i = 0; i < nFile; ++i) {
		getline(ifs, file);
		global_black_files.push_back(file);
		gLog.log(file);
	}
	
	/* create checkLimits*/
	pthread_t hThread;
	rc = pthread_create(&hThread, NULL, checkLimits, NULL);
	if (rc) {
		gLog.log("Error: creating thread checkLimits");
		mKillChild();
		exit(1);
	}
	
	gLog.log("While loop");
	int exitCode;
    int count = 0;
    int timeToBreak = 0;
    while (true) {
		ptrace(PTRACE_SYSCALL, global_child_id, 0, 0);// continue
		ret = waitpid(global_child_id, &status, 0);
		if (ret == -1 || ret == 0) {
			gLog.log("Error: waitpid");
			mKillChild();
			exit(1);
		}
		if (WIFEXITED(status)) {
			gLog.log("\nNormal termination with exit code ", false);
			gLog.log(WEXITSTATUS(status));
			exitCode = 0;
			break;
		}
		if (WIFSIGNALED(status)) {
			gLog.log("\nTerminated by unhandled signal ", false);
			gLog.log(WTERMSIG(status));
			exitCode = EXIT_CODE_UNHANDLED_SIGNAL;
			break;
		}
		if (WCOREDUMP(status)) {
			gLog.log("\nRuntime Error");
			exitCode = (EXIT_CODE_RUN_TIME_ERROR);
			break;
		}
		if (WIFSTOPPED(status)) {
			if (WSTOPSIG(status) == 11) // SIGSEGV
			{
				gLog.log("\nSegmentation Fault");
				exitCode = (EXIT_CODE_MEMORY);
				break;
			}
			
			ptrace(PTRACE_GETREGS, global_child_id, 0, &regs);
            if (inSyscall) {
                gLog.log("returned ", false); gLog.log(regs.rax);
                inSyscall = 0;
                if (timeToBreak) break;
            } else {
                inSyscall = 1;
                gLog.log("count=", false); gLog.log(count, false); gLog.log("\t", false);
                count += 1;
		        int sysCall = regs.orig_rax;
		        gLog.log("syscall=", false); gLog.log(sysCall, false); gLog.log("\t", false);
                if (sysCall == SYSCALL_OPEN) { // open
	                string filePath = getCString(global_child_id, regs.rdi);
	                if (fileInBlackList(filePath)) {
		                gLog.log("Violation detected: opening file ", false); gLog.log(filePath);
		                mKillChild();
		                exitCode = EXIT_CODE_VIOLATION;
		                break; // do not allow syscall to finish
	                }
                } else if (sysCall == SYSCALL_OPENAT) { // openat
	                int dfd = regs.rdi;
	                char actualpath[PATH_MAX+1];
	                string fdPath = "/proc/";
	                fdPath += to_string(global_child_id);
	                fdPath += "/fd/";
	                fdPath += to_string(dfd);
	                memset(actualpath, 0, sizeof(actualpath));
	                if (-1 != readlink(fdPath.c_str(), actualpath, sizeof(actualpath))) {
		                string path = actualpath;
		                path += "/";
		                path += getCString(global_child_id, regs.rsi);
		                if (fileInBlackList(path)) {
			                gLog.log("Violation detected: opening file ", false); gLog.log(path);
			                mKillChild();
			                exitCode = EXIT_CODE_VIOLATION;
			                break; // do not allow syscall to finish
		                }
	                } else {
		                // false dfd
	                }
                } else if (syscallBlackList(sysCall)) {
	                gLog.log("Violation detected with syscall: ", false); gLog.log(sysCall);
	                mKillChild();
	                exitCode = EXIT_CODE_VIOLATION;
	                break; // do not allow syscall to finish
                }
            }
		}
    }
	global_check_limit_continue = false;
	pthread_join(hThread, NULL);
	gLog.log("Cpu used: ", false); gLog.log(global_cpu_used);
	gLog.log("Real time elapsed: ", false); gLog.log(global_real_time_elapsed);
	if (global_check_limit_rc != -1)
		exit(global_check_limit_rc);
	exit(exitCode);
}

char** parseArgs(const string& args)
{
    int s = 0, e = 0;
    vector<string> passed;
    for(int i = 0; i < args.length(); ++i) {
        if (args[i] == ' ') {
            e = i;
            if (e != s) {
                passed.push_back(args.substr(s, e-s));
            }
            s = i+1;
        }
    }
    if (s != args.length()) passed.push_back(args.substr(s, args.length()-s));
    char** rets = new char*[passed.size()+1];
    for(int i = 0; i < passed.size(); ++i) {
        char* ret = new char[passed[i].length()+1];
        strcpy(ret, passed[i].c_str());
        rets[i] = ret;
    }
    rets[passed.size()] = NULL;
    return rets;
}

string hexToString(string mHex)
{
    int len = mHex.length();
    string newString;
    for(int i=0; i < len; i+=2)
    {
        string byte = mHex.substr(i,2);
        char chr = (char) (int)strtol(byte.c_str(), NULL, 16);
        newString.push_back(chr);
    }
    reverse(newString.begin(), newString.end());
    return newString;
}

int get_usage(const pid_t pid, struct pstat* result) {
    //convert  pid to string
    char pid_s[20];
    snprintf(pid_s, sizeof(pid_s), "%d", pid);
    char stat_filepath[30] = "/proc/"; strncat(stat_filepath, pid_s,
            sizeof(stat_filepath) - strlen(stat_filepath) -1);
    strncat(stat_filepath, "/stat", sizeof(stat_filepath) -
            strlen(stat_filepath) -1);

    FILE *fpstat = fopen(stat_filepath, "r");
    if (fpstat == NULL) {
        gLog.log("Error: get_usage:fpstat");
        return -1;
    }

    //read values from /proc/pid/stat
    bzero(result, sizeof(struct pstat));
	unsigned long int u, s;
    if (fscanf(fpstat, "%*d %*s %*c %*d %*d %*d %*d %*d %*u %*u %*u %*u %*u %lu %lu",
                &u, &s) == EOF) {
        fclose(fpstat);
        return -1;
    }
    fclose(fpstat);
	result->utime = u*1.0/sysconf(_SC_CLK_TCK);
	result->stime = s*1.0/sysconf(_SC_CLK_TCK);
    return 0;
}

const int long_size = sizeof(long);
string getCString(pid_t child, long addr)
{
	string ret = "";
    int i;
    union u {
            long val;
            char chars[long_size+1];
    } data;
    i = 0;
    while(true) {
		memset(data.chars, 0, sizeof(data.chars));
        data.val = ptrace(PTRACE_PEEKDATA, child,
                          addr + i * long_size, NULL);
		ret += data.chars;
		if (strlen(data.chars) != long_size) break; // found null
        ++i;
    }
	return ret;
}
