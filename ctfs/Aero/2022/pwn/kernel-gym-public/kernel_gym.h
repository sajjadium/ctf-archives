#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/miscdevice.h> 
#include <linux/random.h>
#include <linux/types.h>

MODULE_AUTHOR("ker@localhost");                    
MODULE_DESCRIPTION("Kernel GYM");
MODULE_LICENSE("GPL");

#define DEFAULT_MONEY_COUNT 4096
#define USERNAME_SIZE 64
#define PASSWORD_SIZE 64
#define MCH_BUF_SIZE 256
#define MCH_NAME_SIZE 128
#define COOKIE_SIZE 128
#define INFO_SIZE 256
#define BARB_DEFAULT_WEIGHT 20
#define SUBSCRIPTION_TIME 30 
#define NULLPTR NULL
#define TRUE 1
#define FALSE 0

typedef unsigned char uint8_t; 
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;
typedef unsigned long long uint64_t;


static enum IOCTL_ACTIONS {
    A_REGISTRATION = 0x0101,
    A_LOGIN = 0x0102,
    A_EXIT = 0x0103,
    A_SUB_FREEZE = 0x0201,
    A_SUB_CLOSE = 0x0202,
    A_GYM_GET_MCH_LIST = 0x0301,
    A_GYM_CHOOSE_MCH = 0x0302,
    A_GYM_RELEASE_MCH = 0x0303,
    A_GYM_TAKE_BARB = 0x0304,
    A_GYM_RELEASE_BARB = 0x0305,
    A_GYM_TAKE_DUMBL = 0x0306,
    A_GYM_RELEASE_DUMBL = 0x0307,
    A_GYM_DO_CARDIO = 0x0308,
    A_GYM_RELEASE_CARDIO = 0x0309
};

static enum ERORR_CODES {
    E_USERSPACE_POINTERS_INVL = 0x0e01,
    E_REQUEST_POINTER_IS_NULL = 0x0e02,
    E_INCORRECT_REQ_OPTION = 0x0e03,
    E_USER_ALREADY_BUSY = 0x0e04,
    E_COPY_FROM_USER = 0x0e05,
    E_NOTHING_TO_RELEASE = 0x0e06,
    E_MCH_IS_BUSY = 0x0e07,
    E_USER_ALREADY_ON_MCH = 0x0e08,
    E_USER_ISNT_ON_MCH = 0x0e09,
    E_MCH_ISNT_BUSY = 0x0e0a,
    E_MCH_ISNT_YOURS = 0x0e0b,
    E_USER_ISNT_LOGINED = 0x0e0c,
    E_COPY_TO_USER = 0x0e0d,
    E_USER_ISNT_EXIST = 0x0e0e,
    E_INVALID_PASSWORD = 0x0e0f,
    E_USER_ALREADY_EXIST = 0x0e10,
    E_KMALLOC_NULLPTR = 0x0e11,
    E_USER_NULLPTR = 0x0e12,
    E_MCH_ISNT_EXIST = 0x0e13
};

static enum SUBSCRIPTION_COST {
    SC_Default = 128, 
    SC_Premium = 256, 
    SC_Pro = 512, 
    SC_Elite = 1024, 
    SC_Gold = 2048, 
    SC_Platinum = 4096
};

static enum SUBSCRIPTION_TYPE {
    ST_Default, 
    ST_Premium, 
    ST_Pro, 
    ST_Elite, 
    ST_Gold, 
    ST_Platinum
};

typedef struct {
    uint64_t speed;
    uint64_t seconds;
    uint8_t is_busy;
} cardio_t;

typedef struct {
    uint64_t weight;
    uint8_t is_busy;
} dumbbells_t;

typedef struct {
    uint64_t default_weight;
    uint64_t left_weight;
    uint64_t right_weight;
    uint8_t is_busy;
} barbell_t;

typedef struct {
    unsigned long long id;
    int (*pDestructor)(void*);
    size_t type;
    size_t days_cnt;
    size_t is_forzen;
    size_t is_expired;
    size_t is_closed;
} subscription_t;

typedef struct {
    char * username;
    char * password;
    
    char is_loginned;
    char * cookie;
    
    size_t has_active_sub;
    subscription_t * current_sub;
    size_t money;
    
    uint8_t on_mch;
    uint8_t is_barb;
    uint8_t is_dumb;
    uint8_t is_cardio;
    
    barbell_t * barb;
    dumbbells_t * dumb;
    cardio_t * cardio;
} user_t;

typedef struct {
    char * name;
    uint64_t min_weight;
    uint64_t max_weight;
    uint64_t weight_step;
    uint8_t is_busy;
    user_t * pCurUser;
} machine_t;

typedef struct {
    char * username;
    char * password;
    char * cookie;
} u_login_req_t;

typedef struct {
    char * username;
    char * password;
    size_t type;
    size_t days_cnt;
} u_reg_req_t;

typedef struct {
    char * cookie;
} u_exit_req_t;

typedef struct {
    char * cookie;
    uint8_t freeze;
    uint8_t close;
    uint8_t update;
    char * info;    
} u_sub_req_t;

typedef struct {
    char * cookie;
    uint8_t get_mch_list;
    uint8_t choose_mch;
    uint8_t release_mch;
    uint8_t take_barb;
    uint8_t release_barb;
    uint8_t take_dumbl;
    uint8_t release_dumbl;
    uint8_t do_cradio;
    uint8_t release_cardio;
    void * args;
    size_t args_size;
} u_gym_req_t;

typedef struct user_list_elem {
    user_t * cur;
    struct user_list_elem * next;
} user_list_elem_t;

typedef struct machine_list_elem {
    machine_t * cur;
    struct machine_list_elem * next;
} mch_list_elem_t;

user_list_elem_t * pUsersList = NULLPTR;
user_list_elem_t * pLoginedUsers = NULLPTR;
mch_list_elem_t * pMchList = NULLPTR;
char * secret = NULLPTR;

static noinline long ioctl_handler(struct file *, unsigned int, unsigned long);
static struct file_operations kernel_gym_fops = {.unlocked_ioctl = ioctl_handler}; 

static noinline size_t registration(unsigned long);
static noinline size_t login(unsigned long);
static noinline char * generate_cookie(void);
static noinline size_t user_exit(unsigned long);

static noinline size_t freeze_subscription(unsigned long);
static noinline size_t close_subscription(unsigned long);
static noinline size_t update_info(unsigned long);

static noinline size_t get_machines_list(unsigned long);
static noinline size_t choose_machine(unsigned long);
static noinline size_t release_machine(unsigned long);
static noinline size_t take_barbell(unsigned long);
static noinline size_t release_barbell(unsigned long);
static noinline size_t take_dumbbells(unsigned long);
static noinline size_t release_dumbbells(unsigned long);
static noinline size_t do_cardio(unsigned long);
static noinline size_t release_cardio(unsigned long);

static noinline u_gym_req_t * get_gym_request(unsigned long);
static noinline machine_t * get_mch_by_name(const char*);

static noinline size_t add_user(user_t *, user_list_elem_t **);
static noinline size_t remove_user(user_t* , user_list_elem_t **);
static noinline user_t * find_user_by_name(const char *);
static noinline user_t * find_user_by_cookie(const char *, user_list_elem_t *);

static noinline size_t get_subs_cost_by_type(size_t);
static noinline u_sub_req_t * get_subs_request(unsigned long);
static noinline size_t destroy_user_obj(user_t *);
static noinline size_t destroy_sub_obj(subscription_t *);
static noinline size_t destroy_platinum_sub_obj(subscription_t *);

static noinline size_t add_mch(machine_t*);

struct miscdevice kernel_gym_dev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "kernel_gym",
    .fops = &kernel_gym_fops,
};