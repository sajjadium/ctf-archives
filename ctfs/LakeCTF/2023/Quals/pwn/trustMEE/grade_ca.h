#define NR_STUDENTS 0x10
#define NAME_LEN 0x10
#define SIG_LEN 0x10

#define HASH_UPDATE	0x00000001
#define HASH_DO_FINAL	0x00000002
#define HASH_RESET	0x00000003

#define SIGN_CLASS	0x00000001
#define SIGN_STUDENT	0x00000002
#define SIGN_CLASS_STUDENT 0x00000003

/* Hash algorithm identifier */
#define HASH_MD5	0x00000001

struct student{
	char firstname[NAME_LEN];
	char lastname[NAME_LEN];
	int grade;
    int sciper;
};

struct signedStudent{
    char firstname[NAME_LEN];
	char lastname[NAME_LEN];
	int grade;
    int sciper;
    char signature[SIG_LEN];
};

struct studentclass{
	struct student students[NR_STUDENTS];
};

struct signedStudentclass{
    struct signedStudent sigsStudents[NR_STUDENTS];
};