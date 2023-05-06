#include "kernel_gym.h"

static noinline long ioctl_handler(struct file * file, unsigned int cmd, 
    unsigned long arg) 
{
    long ret = -1;

    switch (cmd) {
        case A_REGISTRATION:
            ret = registration(arg);
            break;
        case A_LOGIN:
            ret = login(arg);
            break;
        case A_EXIT:
            ret = user_exit(arg);
            break;
        case A_SUB_FREEZE:
            ret = freeze_subscription(arg);
            break;
        case A_SUB_CLOSE:
            ret = close_subscription(arg);
            break;
        case A_GYM_GET_MCH_LIST:
            ret = get_machines_list(arg);
            break;
        case A_GYM_CHOOSE_MCH:
            ret = choose_machine(arg);
            break;
        case A_GYM_RELEASE_MCH:
            ret = release_machine(arg);
            break;
        case A_GYM_TAKE_BARB:
            ret = take_barbell(arg);
            break;
        case A_GYM_RELEASE_BARB:
            ret = release_barbell(arg);
            break;
        case A_GYM_TAKE_DUMBL:
            ret = take_dumbbells(arg);
            break;
        case A_GYM_RELEASE_DUMBL:
            ret = release_dumbbells(arg);
            break;
        case A_GYM_DO_CARDIO:
            ret = do_cardio(arg);
            break;
        case A_GYM_RELEASE_CARDIO:
            ret = release_cardio(arg);
            break;
    }

    return ret;
}

static noinline size_t take_dumbbells(unsigned long arg) {
    u_gym_req_t * u_req = get_gym_request(arg);
    dumbbells_t * dumb = NULLPTR;
    user_t * pUser = NULLPTR;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!u_req->take_dumbl) {
        return E_INCORRECT_REQ_OPTION;
    }

    if (!access_ok(u_req->args, 1)) {
        printk(KERN_INFO "{-} Userspace pointer is invalid!");
        kfree(u_req);
        return E_USERSPACE_POINTERS_INVL;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);

    if (pUser->is_cardio || pUser->is_dumb || pUser->barb) {
        kfree(u_req);
        return E_USER_ALREADY_BUSY;
    }

    dumb = (dumbbells_t*) kmalloc(sizeof(dumbbells_t), GFP_KERNEL);

    if (copy_from_user(&dumb->weight, u_req->args, 
        sizeof(dumb->weight)))
    {
        printk(KERN_INFO "{-} Error in copy from user (take_dumbbells)!");
        kfree(u_req);
        kfree(dumb);
        return E_COPY_FROM_USER;
    }

    dumb->is_busy = TRUE;
    pUser->is_dumb = TRUE;
    pUser->dumb = dumb;

    return 0;
}

static noinline size_t release_dumbbells(unsigned long arg) {
    u_gym_req_t * u_req = get_gym_request(arg);
    user_t * pUser = NULLPTR;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!u_req->release_dumbl) {
        return E_INCORRECT_REQ_OPTION;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);

    if (pUser->dumb == NULLPTR) {
        kfree(u_req);
        return E_NOTHING_TO_RELEASE;
    }

    kfree(pUser->dumb);
    pUser->dumb = NULLPTR;
    pUser->is_dumb = FALSE;
    kfree(u_req);

    return 0;
}

static noinline size_t do_cardio(unsigned long arg) {
    u_gym_req_t * u_req = get_gym_request(arg);
    cardio_t * cardio = NULLPTR;
    user_t * pUser = NULLPTR;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!u_req->do_cradio) {
        return E_INCORRECT_REQ_OPTION;
    }

    if (!access_ok(u_req->args, 1)) {
        printk(KERN_INFO "{-} Userspace pointer is invalid!");
        kfree(u_req);
        return E_USERSPACE_POINTERS_INVL;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);

    if (pUser->is_cardio || pUser->is_dumb || pUser->barb) {
        kfree(u_req);
        return E_USER_ALREADY_BUSY;
    }

    cardio = (cardio_t*) kmalloc(sizeof(cardio_t), GFP_KERNEL);

    if (copy_from_user(&cardio->speed, u_req->args, 
        sizeof(cardio->speed)))
    {
        printk(KERN_INFO "{-} Error in copy from user (do_cradio)!");
        kfree(u_req);
        kfree(cardio);
        return E_COPY_FROM_USER;
    }

    if (copy_from_user(&cardio->seconds, 
        u_req->args + sizeof(cardio->speed), 
        sizeof(cardio->seconds)))
    {
        printk(KERN_INFO "{-} Error in copy from user (do_cradio)!");
        kfree(u_req);
        kfree(cardio);
        return E_COPY_FROM_USER;
    }

    cardio->is_busy = TRUE;
    pUser->is_cardio = TRUE;
    pUser->cardio = cardio;

    return 0;
}

static noinline size_t release_cardio(unsigned long arg) {
    u_gym_req_t * u_req = get_gym_request(arg);
    user_t * pUser = NULLPTR;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!u_req->release_cardio) {
        return E_INCORRECT_REQ_OPTION;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);

    if (pUser->cardio == NULLPTR) {
        kfree(u_req);
        return E_NOTHING_TO_RELEASE;
    }

    kfree(pUser->cardio);
    pUser->cardio = NULLPTR;
    pUser->is_cardio = FALSE;
    kfree(u_req);

    return 0;
}

static noinline size_t release_barbell(unsigned long arg) {
    u_gym_req_t * u_req = get_gym_request(arg);
    user_t * pUser = NULLPTR;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!u_req->release_barb) {
        return E_INCORRECT_REQ_OPTION;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);

    if (pUser->barb == NULLPTR) {
        kfree(u_req);
        return E_NOTHING_TO_RELEASE;
    }

    kfree(pUser->barb);
    pUser->barb = NULLPTR;
    pUser->is_barb = FALSE;
    kfree(u_req);

    return 0;
}

static noinline size_t take_barbell(unsigned long arg) {
    u_gym_req_t * u_req = get_gym_request(arg);
    barbell_t * barb = NULLPTR;
    user_t * pUser = NULLPTR;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!u_req->take_barb) {
        return E_INCORRECT_REQ_OPTION;
    }

    if (!access_ok(u_req->args, 1)) {
        printk(KERN_INFO "{-} Userspace pointer is invalid!");
        kfree(u_req);
        return E_USERSPACE_POINTERS_INVL;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);

    if (pUser->is_cardio || pUser->is_dumb || pUser->barb) {
        kfree(u_req);
        return E_USER_ALREADY_BUSY;
    }

    barb = (barbell_t*) kmalloc(sizeof(barbell_t), GFP_KERNEL);
    barb->default_weight = BARB_DEFAULT_WEIGHT;

    if (copy_from_user(&barb->left_weight, u_req->args, 
        sizeof(barb->left_weight)))
    {
        printk(KERN_INFO "{-} Error in copy from user (take_barbell)!");
        kfree(u_req);
        kfree(barb);
        return E_COPY_FROM_USER;
    }

    if (copy_from_user(&barb->right_weight, 
        u_req->args + sizeof(barb->left_weight), 
        sizeof(barb->left_weight)))
    {
        printk(KERN_INFO "{-} Error in copy from user (take_barbell)!");
        kfree(u_req);
        kfree(barb);
        return E_COPY_FROM_USER;
    }

    barb->is_busy = TRUE;
    pUser->is_barb = TRUE;
    pUser->barb = barb;

    return 0;
}

static noinline size_t get_machines_list(unsigned long arg) {
    u_gym_req_t * u_req = get_gym_request(arg);
    mch_list_elem_t * pCur = pMchList;
    machine_t * pMch = NULLPTR;
    size_t copy_offset = 0;
    size_t realBufSize = 0;

    char mch_buf[MCH_BUF_SIZE];

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!u_req->get_mch_list) {
        return E_INCORRECT_REQ_OPTION;
    }

    if (!access_ok(u_req->args, 1)) {
        printk(KERN_INFO "{-} Userspace pointer is invalid!");
        kfree(u_req);
        return E_USERSPACE_POINTERS_INVL;
    }

    while (pCur != NULLPTR) {
        pMch = pCur->cur;
        
        memset(mch_buf, 0, MCH_BUF_SIZE);

        if (pMch != NULLPTR) {
            if (pMch->is_busy) {
                realBufSize = snprintf(mch_buf, MCH_BUF_SIZE, "|%s|%lld|%lld|%lld|%d|%s|\n",
                pMch->name, pMch->min_weight, pMch->max_weight,
                pMch->weight_step, pMch->is_busy, pMch->pCurUser->username);
            } else {
                realBufSize = snprintf(mch_buf, MCH_BUF_SIZE, "|%s|%lld|%lld|%lld|%d|NULL|\n",
                pMch->name, pMch->min_weight, pMch->max_weight,
                pMch->weight_step, pMch->is_busy);
            }
            
            if (copy_to_user((void*)u_req->args + copy_offset, 
                (void*)mch_buf, realBufSize)) {
                printk(KERN_INFO "{-} Error in copy to user (get_machines_list)!");
                kfree(u_req);
                return E_COPY_TO_USER;
            }
        }

        if (realBufSize > 0) {
            copy_offset += realBufSize;
        }
        pCur = pCur->next;
    }
    
    kfree(u_req);    
    return 0;   
}

static noinline size_t choose_machine(unsigned long arg) {
    u_gym_req_t * u_req = get_gym_request(arg);
    char * mch_name = NULLPTR;
    machine_t * mch = NULLPTR;
    user_t * pUser = NULLPTR;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!u_req->choose_mch) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!access_ok(u_req->args, 1)) {
        printk(KERN_INFO "{-} Userspace pointer is invalid!");
        kfree(u_req);
        return E_USERSPACE_POINTERS_INVL;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);

    if (pUser->is_cardio || pUser->is_dumb || pUser->is_barb) {
        kfree(u_req);
        return E_USER_ALREADY_BUSY;
    }

    mch_name = (char*) kmalloc(MCH_NAME_SIZE, GFP_KERNEL);

    if (u_req->args_size > MCH_NAME_SIZE) {
        printk(KERN_INFO "{-} Error args size!");
        kfree(mch_name);
        kfree(u_req);
        return E_INCORRECT_REQ_OPTION;
    }

    if (copy_from_user((void*)mch_name, (void*)u_req->args, MCH_NAME_SIZE)) {
        printk(KERN_INFO "{-} Error in copy from user (choose_machine)!");
        kfree(mch_name);
        kfree(u_req);
        return E_COPY_FROM_USER;
    }

    mch = get_mch_by_name(mch_name);

    if (mch == NULLPTR) {
        printk(KERN_INFO "{-} No such machine!");
        kfree(mch_name);
        kfree(u_req);
        return E_MCH_ISNT_EXIST;
    }

    if (mch->is_busy) {
        printk(KERN_INFO "{-} Machine is busy!");
        kfree(mch_name);
        kfree(u_req);
        return E_MCH_IS_BUSY;
    }

    if (pUser->on_mch) {
        printk(KERN_INFO "{-} User already on machine!");
        kfree(mch_name);
        kfree(u_req);
        return E_USER_ALREADY_ON_MCH;
    }

    mch->is_busy = TRUE;
    mch->pCurUser = pUser;
    pUser->on_mch = TRUE;

    return 0;
}

static noinline size_t release_machine(unsigned long arg) {
    u_gym_req_t * u_req = get_gym_request(arg);
    char * mch_name = NULLPTR;
    machine_t * mch = NULLPTR;
    user_t * pUser = NULLPTR;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (!u_req->release_mch) {
        return E_INCORRECT_REQ_OPTION;
    }

    if (!access_ok(u_req->args, 1)) {
        printk(KERN_INFO "{-} Userspace pointer is invalid!");
        kfree(u_req);
        return E_USERSPACE_POINTERS_INVL;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);
    
    if (!pUser->on_mch) {
        printk(KERN_INFO "{-} User isn't on machine!");
        kfree(u_req);
        return E_USER_ISNT_ON_MCH;
    }

    mch_name = (char*) kmalloc(MCH_NAME_SIZE, GFP_KERNEL);

    if (copy_from_user((void*)mch_name, (void*)u_req->args, MCH_NAME_SIZE)) {
        printk(KERN_INFO "{-} Error in copy from user (release_machine)!");
        kfree(mch_name);
        kfree(u_req);
        return E_COPY_FROM_USER;
    }

    mch = get_mch_by_name(mch_name);

    if (!mch->is_busy) {
        printk(KERN_INFO "{-} Machine isn't busy!");
        kfree(mch_name);
        kfree(u_req);
        return E_MCH_ISNT_BUSY;
    }

    if (mch->pCurUser != pUser) {
        printk(KERN_INFO "{-} Machine isn't yours!");
        kfree(mch_name);
        kfree(u_req);
        return E_MCH_ISNT_YOURS;
    }

    mch->is_busy = FALSE;
    mch->pCurUser = NULLPTR;
    pUser->on_mch = FALSE;

    return 0;
}

static noinline size_t freeze_subscription(unsigned long arg) {
    u_sub_req_t * u_req = get_subs_request(arg);
    user_t * pUser = NULLPTR;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);

    if (u_req->freeze != 0 && pUser->has_active_sub) {
        pUser->current_sub->is_forzen = TRUE;
    }

    kfree(u_req);
    return 0;
}

static noinline size_t close_subscription(unsigned long arg) {
    u_sub_req_t * u_req = get_subs_request(arg);
    user_t * pUser = NULLPTR;
    size_t cashback = 0;

    if (u_req == NULLPTR) {
        return E_REQUEST_POINTER_IS_NULL;
    }

    pUser = find_user_by_cookie(u_req->cookie, pLoginedUsers);
    
    if (u_req->close != 0 && pUser->has_active_sub) {
        if (pUser->current_sub->pDestructor == NULLPTR) {
            kfree(pUser->current_sub);
        }
        else {
            cashback = pUser->current_sub->pDestructor(pUser->current_sub);
        }

        pUser->has_active_sub = FALSE;
        pUser->current_sub = NULLPTR; 
    }

    pUser->money += cashback;
    kfree(u_req);
    return 0;
}

static noinline size_t user_exit(unsigned long arg) {
    u_exit_req_t * u_req = (u_exit_req_t*) kmalloc(sizeof(u_exit_req_t),
        GFP_KERNEL);
    user_t * pUser = NULLPTR;
    char * cookie = NULLPTR;

    if (u_req == NULLPTR) {
        printk(KERN_INFO "{-} Error in create user exit request struct!");
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (copy_from_user((void *)u_req, (void *)arg, sizeof(u_exit_req_t))) {
        printk(KERN_INFO "{-} Error in copy user request (exit)!");
        kfree(u_req);
        return E_COPY_FROM_USER;
    }

    if (!access_ok(u_req->cookie, 1)) {
        printk(KERN_INFO "{-} Userspace pointers is invalid!");
        kfree(u_req);
        return E_USERSPACE_POINTERS_INVL;
    }

    cookie = (char*) kmalloc(COOKIE_SIZE, GFP_KERNEL);

    if (copy_from_user((void*)cookie, (void*)u_req->cookie, COOKIE_SIZE)) {
        printk(KERN_INFO "{-} Error in copy user cookie (exit)!");
        kfree(u_req);
        kfree(cookie);
        return E_COPY_FROM_USER;
    }

    pUser = find_user_by_cookie(cookie, pLoginedUsers);

    if (pUser == NULLPTR) {
        printk(KERN_INFO "{-} User isn't logined!");
        return E_USER_ISNT_LOGINED;
    }

    remove_user(pUser, &pLoginedUsers);

    if (pUser->cookie != NULLPTR) {
        kfree(pUser->cookie);
        pUser->cookie = NULLPTR;
    }

    pUser->is_loginned = FALSE;
    kfree(pUser);

    return 0;
}

static noinline size_t login(unsigned long arg) {
    u_login_req_t * u_req = (u_login_req_t*) kmalloc(sizeof(u_login_req_t),
        GFP_KERNEL);
    char * pTmpUsername = NULLPTR;
    char * pTmpPassword = NULLPTR;
    user_t * pTmpUser = NULLPTR;
    user_t * pLoginedUser = NULLPTR;
    
    if (u_req == NULLPTR) {
        printk(KERN_INFO "{-} Error in create user login request struct!");
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (copy_from_user((void *)u_req, (void *)arg, sizeof(u_login_req_t))) {
        printk(KERN_INFO "{-} Error in copy user request (login)!");
        kfree(u_req);
        return E_COPY_FROM_USER;
    }

    if (!access_ok(u_req->username, 1) || !access_ok(u_req->password, 1) ||
        !access_ok(u_req->cookie, 1)) {
        printk(KERN_INFO "{-} Userspace pointers is invalid!");
        kfree(u_req);
        return E_USERSPACE_POINTERS_INVL;
    }

    pTmpUsername = (char*) kmalloc(USERNAME_SIZE, GFP_KERNEL);
    pTmpPassword = (char*) kmalloc(PASSWORD_SIZE, GFP_KERNEL);
    
    if (copy_from_user(pTmpUsername, u_req->username, USERNAME_SIZE)) {
        printk(KERN_INFO "{-} Error in copy username (registration)");
        kfree(u_req);
        kfree(pTmpUsername);
        kfree(pTmpPassword);
        return E_COPY_FROM_USER;
    }

    if (copy_from_user(pTmpPassword, u_req->password, PASSWORD_SIZE)) {
        printk(KERN_INFO "{-} Error in copy password (registration)");
        kfree(u_req);
        kfree(pTmpUsername);
        kfree(pTmpPassword);
        return E_COPY_FROM_USER;
    }

    pTmpUser = find_user_by_name(pTmpUsername);

    if (pTmpUser == NULLPTR) {
        printk(KERN_INFO "{-} User isn't exist!");
        kfree(u_req);
        kfree(pTmpUsername);
        kfree(pTmpPassword);
        return E_USER_ISNT_EXIST;
    }

    if (strlen(pTmpUser->password) == strlen(pTmpPassword) &&
        !strncmp(pTmpUser->password, pTmpPassword, strlen(pTmpPassword))) {
        pTmpUser->is_loginned = TRUE;
    } else {
        printk(KERN_INFO "{-} Invalid password!");
        kfree(u_req);
        kfree(pTmpUsername);
        kfree(pTmpPassword);
        return E_INVALID_PASSWORD;
    }

    pLoginedUser = (user_t*) kmalloc(sizeof(user_t), GFP_KERNEL);
    memcpy((void*)pLoginedUser, (void*)pTmpUser, sizeof(user_t));

    pLoginedUser->cookie = generate_cookie();
    
    if (pLoginedUser->cookie == NULLPTR) {
        kfree(u_req);
        kfree(pTmpUsername);
        kfree(pTmpPassword);
        kfree(pLoginedUser);
        return E_KMALLOC_NULLPTR;
    }

    if (copy_to_user(u_req->cookie, pLoginedUser->cookie, COOKIE_SIZE)) {
        printk(KERN_INFO "{-} Error in copy cookie to userspace!");
        kfree(u_req);
        kfree(pLoginedUser->cookie);
        kfree(pTmpUsername);
        kfree(pTmpPassword);
        pLoginedUser->cookie = NULLPTR;
        return E_COPY_TO_USER;
    }

    pLoginedUser->is_loginned = TRUE;
    add_user(pLoginedUser, &pLoginedUsers);

    kfree(u_req);
    kfree(pTmpUsername);
    kfree(pTmpPassword);
    return 0;  
}

static noinline size_t registration(unsigned long arg) {
    u_reg_req_t * u_req = (u_reg_req_t*) kmalloc(sizeof(u_reg_req_t),
        GFP_KERNEL);
    user_t * pNewUser = NULLPTR;
    subscription_t * pUserSub = NULLPTR;
    size_t subs_cost = 0;
    size_t real_days_cnt = 0;

    if (u_req == NULLPTR) {
        printk(KERN_INFO "{-} Error in create user registration request struct!");
        return E_REQUEST_POINTER_IS_NULL;
    }

    if (copy_from_user((void *)u_req, (void *)arg, sizeof(u_reg_req_t))) {
        printk(KERN_INFO "{-} Error in copy user request (registration)!");
        kfree(u_req);
        return E_COPY_FROM_USER;
    }

    if (!access_ok(u_req->username, 1) || !access_ok(u_req->password, 1)) {
        printk(KERN_INFO "{-} Userspace pointers is invalid!");
        kfree(u_req);
        return E_USERSPACE_POINTERS_INVL;
    }

    pNewUser = (user_t*) kmalloc(sizeof(user_t), GFP_KERNEL);

    if (pNewUser == NULLPTR) {
        printk(KERN_INFO "{-} Error in create user_t struct (registration)!");
        kfree(u_req);
        return E_KMALLOC_NULLPTR;
    }

    pNewUser->current_sub = NULLPTR;
    pNewUser->has_active_sub = FALSE;
    pNewUser->is_loginned = FALSE;
    pNewUser->money = DEFAULT_MONEY_COUNT;
    pNewUser->username = (char*) kmalloc(USERNAME_SIZE, GFP_KERNEL);
    pNewUser->password = (char*) kmalloc(PASSWORD_SIZE, GFP_KERNEL);
    pNewUser->cookie = NULLPTR;

    if (copy_from_user(pNewUser->username, u_req->username, USERNAME_SIZE)) {
        printk(KERN_INFO "{-} Error in copy username (registration)");
        destroy_user_obj(pNewUser);
        kfree(u_req);
        return E_COPY_FROM_USER;
    }

    if (copy_from_user(pNewUser->password, u_req->password, PASSWORD_SIZE)) {
        printk(KERN_INFO "{-} Error in copy password (registration)");
        destroy_user_obj(pNewUser);
        kfree(u_req);
        return E_COPY_FROM_USER;
    }

    if (find_user_by_name(pNewUser->username) != NULLPTR) {
        printk(KERN_INFO "{-} User already exist!");
        destroy_user_obj(pNewUser);
        kfree(u_req);
        return E_USER_ALREADY_EXIST;
    }

    subs_cost = get_subs_cost_by_type(u_req->type) * (u_req->days_cnt/SUBSCRIPTION_TIME);
    
    if (subs_cost > pNewUser->money) {
        real_days_cnt = pNewUser->money / (get_subs_cost_by_type(u_req->type) / SUBSCRIPTION_TIME);
        pNewUser->money = 0;
    } else {
        real_days_cnt = u_req->days_cnt;
        pNewUser->money -= subs_cost;
    }

    pUserSub = (subscription_t*) kmalloc(sizeof(subscription_t), GFP_KERNEL);

    if (pUserSub == NULLPTR) {
        printk(KERN_INFO "{-} Error in create user subscription struct!");
        return E_KMALLOC_NULLPTR;
    }

    pUserSub->type = u_req->type;
    pUserSub->days_cnt = real_days_cnt;
    pUserSub->is_forzen = FALSE;
    pUserSub->is_expired = FALSE;
    pUserSub->is_closed = FALSE;

    if (pUserSub->type == ST_Platinum) {
        pUserSub->pDestructor = (int(*)(void*))&destroy_platinum_sub_obj;
    } else {
        pUserSub->pDestructor = (int(*)(void*))&destroy_sub_obj;
    }

    get_random_bytes(&pUserSub->id, sizeof(pUserSub->id));
    pNewUser->current_sub = pUserSub;
    pNewUser->has_active_sub = TRUE;

    add_user(pNewUser, &pUsersList);
    return 0;
}

static noinline size_t add_user(user_t * pNewUser, user_list_elem_t ** pList) {
    user_list_elem_t * pNewUserEntry = NULLPTR;
    
    if (pNewUser == NULLPTR) {
        return E_USER_NULLPTR;
    }

    pNewUserEntry = (user_list_elem_t*) kmalloc(sizeof(user_list_elem_t),
         GFP_KERNEL);

    pNewUserEntry->next = NULLPTR;
    pNewUserEntry->cur = pNewUser;
    
    if (pList == NULLPTR) {
        *pList = pNewUserEntry;    
    } else {
        pNewUserEntry->next = *pList;
        *pList = pNewUserEntry;
    }

    return 0;
}

static noinline size_t remove_user(user_t * pUser, user_list_elem_t ** pList) {
    user_list_elem_t * pCur = *pList;
    user_list_elem_t * pPrev = NULLPTR;

    while (pCur != NULLPTR) {
        if (pCur->cur == pUser)
            break;
        pPrev = pCur;
        pCur = pCur->next;
    }

    if (pCur == NULLPTR) {
        return E_USER_ISNT_EXIST;
    }

    if (pPrev == NULLPTR) {
       *pList = pCur->next;
       return 0; 
    }

    pPrev->next = pCur->next;
    return 0;
}

static noinline user_t * find_user_by_name(const char * name) {
    user_list_elem_t * pCur = pUsersList;

    while (pCur != NULLPTR) {
        if (strlen(pCur->cur->username) == strlen(name)) {
            if (!strncmp(pCur->cur->username, name, strlen(name)))
                return pCur->cur;
        }

        pCur = pCur->next;
    }

    return NULLPTR;
}

static noinline user_t * find_user_by_cookie(const char * cookie, 
    user_list_elem_t * pList) {
    user_list_elem_t * pCur = pList;

    while (pCur != NULLPTR) {
        if (pCur->cur->cookie != NULLPTR) {
            if (!strncmp(pCur->cur->cookie, cookie, COOKIE_SIZE))
                return pCur->cur;
        }
        pCur = pCur->next;
    }

    return NULLPTR;
}

static noinline size_t get_subs_cost_by_type(size_t t) {
    switch(t) {
        case ST_Default:
            return SC_Default;
        case ST_Premium:
            return SC_Premium;
        case ST_Pro:
            return SC_Pro;
        case ST_Elite:
            return SC_Elite;
        case ST_Gold:
            return SC_Gold;
        case ST_Platinum:
            return SC_Platinum;
        default:
            break;
    }
    return INT_MAX;
}

static noinline u_sub_req_t * get_subs_request(unsigned long arg) {
    u_sub_req_t * u_req = (u_sub_req_t*) kmalloc(sizeof(u_sub_req_t),
        GFP_KERNEL);
    user_t * pUser = NULLPTR;
    char * cookie = NULLPTR;

    if (u_req == NULLPTR) {
        printk(KERN_INFO "{-} Error in create user subscription request struct!");
        return NULLPTR;
    }

    if (copy_from_user((void *)u_req, (void *)arg, sizeof(u_sub_req_t))) {
        printk(KERN_INFO "{-} Error in copy user request (check_subs_request)!");
        kfree(u_req);
        return NULLPTR;
    }

    if (!access_ok(u_req->cookie, 1)) {
        printk(KERN_INFO "{-} Userspace pointers is invalid!");
        kfree(u_req);
        return NULLPTR;
    }

    cookie = (char*) kmalloc(COOKIE_SIZE, GFP_KERNEL);

    if (copy_from_user((void*)cookie, (void*)u_req->cookie, COOKIE_SIZE)) {
        printk(KERN_INFO "{-} Error in copy user cookie (get_subs_request)!");
        kfree(u_req);
        kfree(cookie);
        return NULLPTR;
    }

    pUser = find_user_by_cookie(cookie, pLoginedUsers);

    if (pUser == NULLPTR) {
        printk(KERN_INFO "{-} User isn't logined!");
        kfree(u_req);
        kfree(cookie);
        return NULLPTR;
    }

    u_req->cookie = cookie;

    return u_req;
};

static noinline u_gym_req_t * get_gym_request(unsigned long arg) {
    u_gym_req_t * u_req = (u_gym_req_t*) kmalloc(sizeof(u_gym_req_t),
        GFP_KERNEL);
    user_t * pUser = NULLPTR;
    char * cookie = NULLPTR;

    if (u_req == NULLPTR) {
        printk(KERN_INFO "{-} Error in create user gym request struct!");
        return NULLPTR;
    }

    if (copy_from_user((void *)u_req, (void *)arg, sizeof(u_gym_req_t))) {
        printk(KERN_INFO "{-} Error in copy user request (get_gym_request)!");
        kfree(u_req);
        return NULLPTR;
    }

    if (!access_ok(u_req->cookie, 1)) {
        printk(KERN_INFO "{-} Userspace pointers is invalid!");
        kfree(u_req);
        return NULLPTR;
    }

    cookie = (char*) kmalloc(COOKIE_SIZE, GFP_KERNEL);

    if (copy_from_user((void*) cookie, (void*)u_req->cookie, COOKIE_SIZE)) {
        printk(KERN_INFO "{-} Error in copy user cookie (get_gym_request)!");
        kfree(u_req);
        kfree(cookie);
        return NULLPTR;
    }

    pUser = find_user_by_cookie(cookie, pLoginedUsers);

    if (pUser == NULLPTR) {
        printk(KERN_INFO "{-} User isn't logined!");
        kfree(u_req);
        kfree(cookie);
        return NULLPTR;
    }

    u_req->cookie = cookie;

    return u_req;
};

static noinline machine_t * get_mch_by_name(const char * name) {
    mch_list_elem_t * pCur = pMchList;

    while (pCur != NULLPTR) {
        if (strlen(name) == strlen(pCur->cur->name)) {
            if (!strncmp(name, pCur->cur->name, strlen(name))) {
                return pCur->cur;
            }
        }
        pCur = pCur->next;
    }

    return NULLPTR;
};

static noinline size_t destroy_user_obj(user_t * pUser) {
    if (pUser == NULLPTR)
        return 0;
    
    if (pUser->username != NULLPTR)
        kfree(pUser->username);
    
    if (pUser->password != NULLPTR)
        kfree(pUser->password);

    if (pUser->current_sub != NULLPTR)
        destroy_sub_obj(pUser->current_sub);
    
    if (pUser->cookie != NULLPTR)
        kfree(pUser->cookie);
    
    if (pUser->barb != NULLPTR)
        kfree(pUser->barb);

    if (pUser->dumb != NULLPTR)
        kfree(pUser->dumb);

    if (pUser->cardio != NULLPTR)
        kfree(pUser->cardio);

    kfree(pUser);
    return 1;
}

static noinline size_t destroy_sub_obj(subscription_t * pSub) {
    if (pSub == NULLPTR)
        return 0;

    pSub->id = 0;
    pSub->type = SC_Default;
    pSub->days_cnt = 0;
    pSub->is_forzen = FALSE;
    pSub->is_expired = FALSE;
    pSub->is_closed = TRUE;

    kfree(pSub);
    return 0;
}

static noinline size_t destroy_platinum_sub_obj(subscription_t * pSub) {
    if (pSub == NULLPTR)
        return 0;

    pSub->id = 0;
    pSub->type = SC_Default;
    pSub->days_cnt = 0;
    pSub->is_forzen = FALSE;
    pSub->is_expired = FALSE;
    pSub->is_closed = TRUE;

    kfree(pSub);
    return SC_Gold;
}

static noinline size_t add_mch(machine_t * pMch) {
    mch_list_elem_t * pNewMchEntry = NULLPTR;
    
    if (pMch == NULLPTR) {
        return 1;
    }

    pNewMchEntry = (mch_list_elem_t*) kmalloc(sizeof(mch_list_elem_t),
         GFP_KERNEL);

    pNewMchEntry->next = NULLPTR;
    pNewMchEntry->cur = pMch;
    
    if (pMchList == NULLPTR) {
        pMchList = pNewMchEntry;    
    } else {
        pNewMchEntry->next = pMchList;
        pMchList = pNewMchEntry;
    }

    return 0;
}

static noinline char * generate_cookie(void) {
    char alph[] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int i = 0;
    char * cookie = NULLPTR;

    cookie = (char*) kmalloc(COOKIE_SIZE, GFP_KERNEL);

    if (cookie == NULLPTR) {
        printk(KERN_INFO "{-} Error in create cookie!");
        return cookie;
    }

    get_random_bytes(cookie, COOKIE_SIZE);

    for (i = 0; i < COOKIE_SIZE; i++) {
        cookie[i] = alph[cookie[i] % strlen(alph)];
    }

    return cookie;
}

static int __init init_dev(void) {
    int dev_reg = misc_register(&kernel_gym_dev);
    machine_t * mch[10];
    int i = 0;

    if (dev_reg < 0){
        printk(KERN_INFO "{-} Failed to register kernel GYM!");
    }

    for (i = 0; i < 10; i++) {
        mch[i] = (machine_t*) kmalloc(sizeof(machine_t), GFP_KERNEL);
        mch[i]->name = (char*) kmalloc(MCH_NAME_SIZE, GFP_KERNEL);
        snprintf(mch[i]->name, MCH_NAME_SIZE, "machine{%d}", i);
        mch[i]->max_weight = 10;
        mch[i]->max_weight = 100;
        mch[i]->weight_step = 10;
        mch[i]->is_busy = FALSE;
        mch[i]->pCurUser = NULLPTR;
        add_mch(mch[i]);
    }

    secret = (char*) kmalloc(128, GFP_KERNEL);
    strcpy(secret, "Aero{fakeflag}");

    return 0;
}

static void __exit exit_dev(void) {
    misc_deregister(&kernel_gym_dev);
}

module_init(init_dev);
module_exit(exit_dev);