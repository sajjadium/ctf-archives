#define ELECTIVE_CLASS_CODE 0
#define MANDATORY_CLASS_CODE 1

typedef struct {
  char name[10];
  int studentNumber;
  int EnglishScore;
} student;
typedef struct {
  char *name;
  int type;
  void *detail;
} comma;

typedef struct {
  char *name;
  int time[2];
  char *target[4];
  char memo[32];
  char *professor;
} mandatory_subject;

typedef struct {
  char *name;
  int time[2];
  char memo[32];
  char *professor;
  int (*IsAvailable)(student *);
} elective_subject;

const mandatory_subject computer_system = {
    "Computer_System",
    {3, 2},
    {"Engineering", "Electricity&Information", "Information", "Info-system"},
    "",
    "Matsumura Kaoru"};
const mandatory_subject digital_circuit = {
    "Digital_Circuit",
    {2, 4},
    {"Engineering", "Electricity&Information", "Electricity", "Circuit-system"},
    "",
    "Kawamura Takeshi"};
const mandatory_subject system_control = {
    "System Control",
    {1, 1},
    {"Engineering", "Machine&Material", "Machine", "machine-system"},
    "",
    "Nakano Ami"};

mandatory_subject mandatory_list[3] = {computer_system, digital_circuit,
                                       system_control};

int IsAvailableWorldAffairs(student *stu) {
  printf("Name : %s, EnglishScore: %d, studentNumber: %d", stu->name,
         stu->EnglishScore, stu->studentNumber);
  if (stu->EnglishScore >= 60 && stu->studentNumber >= 1000) {
    return 1;
  }
  return 0;
}

const elective_subject world = {
    "World Affairs", {3, 2}, "", "Nomura Kameyo", IsAvailableWorldAffairs};

int IsAvailableTWI(student *stu) {
  if (stu->EnglishScore >= 80 && stu->studentNumber >= 1500) {
    return 1;
  }
  return 0;
}
const elective_subject intellect = {
    "The World of Intellect", {2, 4}, "", "Kataoka Izanami", IsAvailableTWI};

elective_subject elective_list[2] = {world, intellect};
