typedef unsigned char byte;
struct listnode {
    byte data;
    struct listnode *ptr;
};

struct list {
    int len;
    struct listnode *head;
}(list);

void list_init(struct list *list, byte *data, int len);
void list_mix(struct list *list);