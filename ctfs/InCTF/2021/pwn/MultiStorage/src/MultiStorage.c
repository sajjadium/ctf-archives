#include "MultiStorage.h"

int Add(char *buf){

    int type1_cnt = 0, type2_cnt = 0, i;
    char * t1 = NULL;
    char * t2 = NULL;
    char * cp = buf;

    Header * head = (Header*)buf;
    unsigned int length = head->length;

    buf+= sizeof(Header);
    cp+= sizeof(Header);


    /*  Count Type1 and Type2 */
    for(i=0;i<length;i++){
        /*  Since both have type, we can use this.*/
        input1 * tmp = (input1 *)buf;
        unsigned int curType = tmp->type;

        switch(curType){
            case TYPE1: type1_cnt++;
                        break;
            case TYPE2: type2_cnt++;
                        break;
                        /*  Can't allow anything else  */
            default: Info("Undefined behaviour\n");
                     goto err;
        }
        buf+= sizeof(input1);

        /*  Only 10 of each allowed */
        if(type1_cnt > 10 || type2_cnt > 10){
            Info("Too many Type1 or Type2 requests\n");
            goto err;
        }
    }

    if(t1Ptr || t2Ptr){
        Info("Already exist\n");
        goto err;
    }


    /*  Allocate space for both types */
    if(type1_cnt)
        t1 = kmalloc(sizeof(Type1)*type1_cnt, GFP_KERNEL);

    if(type2_cnt)
        t2 = kmalloc(sizeof(Type2)*type2_cnt, GFP_KERNEL);

    t1Ptr = t1;
    t2Ptr = t2;

    Info("Copying data\n");

    /*  Now we copy the actual data */
    for(i=0; i<length; i++){
        /*  If it is type1 */
        input1 * temp = (input1 *)cp;
        /*  If it is type2 */
        input2 * in = (input2*)cp;

        unsigned int curType = temp->type;

        /*  We copy to its respective place */
        switch(curType){
            case TYPE1:
                if(t1){
                    Type1 * tmp = (Type1 *)t1;
                    tmp->id = i;
                    memcpy(tmp->data, temp->buf, 28);
                    t1 += sizeof(Type1);
                }
                else{
                    Info("Undefined behaviour\n");
                    goto err;
                }
                break;
            case TYPE2:
                /*  Once we know it is type2, we make it input2 type */
                if(t2){
                    int j;
                    Type2 * tmp = (Type2 *)t2;
                    tmp->id = i;
                    for(j=0; j<7; j++){
                        tmp->arr[j] = in->arr[j];
                    }
                    t2+= sizeof(Type2);
                }
                else{
                    Info("Undefined behaviour\n");
                    goto err;
                }
                break;
            default: Info("Undefined behaviour\n");
                     goto err;
        }
        /*  Will work since input1 and input2 are of same size */
        cp += sizeof(input1);
    }

    /*  Later used in view */
    t1_len = type1_cnt;
    t2_len = type2_cnt;
    Info("Add comepleted\n");

    return 0;

    /*  Cleanup */
err:
    if(t1)
        kfree(t1);
    if(t2)
        kfree(t2);
    t1Ptr = NULL;
    t2Ptr = NULL;
    return -EINVAL;
}

/*  A small function to delete stuff */
int Del(void){
    if(t1Ptr)
        kfree(t1Ptr);
    if(t2Ptr)
        kfree(t2Ptr);

    t1Ptr = NULL;
    t2Ptr = NULL;
    Info("Delete comepleted\n");
    return 0;
}

/*  User can ask for type1 or type2 */
int View(char * buf, int type){
    if(type == TYPE1){
        if(t1Ptr){
            if(copy_to_user(buf, t1Ptr,t1_len*sizeof(Type1))){
                Info("Error");
            }
        }

    }
    if(type == TYPE2){
        if(t2Ptr){
            if(copy_to_user(buf, t2Ptr,t2_len*sizeof(Type2))){
                Info("Error");
            }
        }
    }
    Info("View comepleted\n");
    return 0;

}

long int handle_ioctl(struct file* fd, unsigned int type, unsigned long arg){

    req * temp;
    char * usr_buf = NULL;
    unsigned int p_type=0;

    temp = kmalloc(sizeof(req), GFP_KERNEL);

    mutex_lock(&lock);
    if(copy_from_user((void *)temp, (const void * )arg, sizeof(req))){
        Info("Error");
        mutex_unlock(&lock);
        return -EINVAL;
    }
    usr_buf = temp->buf;
    p_type = temp->type;

    switch(type){
        case ADD: Add(usr_buf); break;
        case DELETE: Del(); break;
        case VIEW: View(usr_buf, p_type); break;
        default: 
                   if(temp)
                       kfree(temp);
                   mutex_unlock(&lock); 
                   return -EINVAL;
    }
    if(temp)
        kfree(temp);
    mutex_unlock(&lock);
    return 0;
}


static const struct file_operations file_ops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = handle_ioctl,
};

static struct miscdevice device = {
    MISC_DYNAMIC_MINOR, "MultiStorage" , &file_ops
};


static int __init init(void)
{
    int ret;
    mutex_init(&lock);
    ret = misc_register(&device);
    if(ret < 0){
        mutex_destroy(&lock);
        Info("Failed\n");
    }
    Info("Init\n");
    return 0;
}

static void __exit cleanup(void)
{
    Info("Fini\n");
    misc_deregister(&device);
}


module_init(init);
module_exit(cleanup);

