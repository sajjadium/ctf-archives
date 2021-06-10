// #include "global.h"

void op_add() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("ADD: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data += temp->data;
  }
  sp++;
}

void op_sub() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("ADD: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = temp->data - ax.data;
  }
  sp++;
}

void op_mul() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("ADD: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = temp->data * ax.data;
  }
  sp++;
}

void op_div() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("ADD: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = temp->data / ax.data;
  }
  sp++;
}

void op_mod() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("ADD: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = temp->data % ax.data;
  }
  sp++;
}

void op_equal() {
  val *temp = sp;
  if (ax.type != sp->type) {
    ax.type = INT;
    ax.data = 0;
    return;
  }
  if (ax.type == INT) {
    ax.data = (temp->data == ax.data);
  }
  sp++;
}

void op_notequal() {
  val *temp = sp;
  if (ax.type != sp->type) {
    ax.type = INT;
    ax.data = 1;
    return;
  }
  if (ax.type == INT) {
    ax.data = (temp->data != ax.data);
  }
  sp++;
}

void op_or() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("OR: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = (temp->data | ax.data);
  }
  sp++;
}

void op_xor() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("OR: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = (temp->data ^ ax.data);
  }
  sp++;
}

void op_and() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("OR: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = (temp->data & ax.data);
  }
  sp++;
}

void op_lt() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("LT: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = (temp->data < ax.data);
  }
  sp++;
}

void op_le() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("LT: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = (temp->data <= ax.data);
  }
  sp++;
}

void op_gt() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("GT: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = (temp->data > ax.data);
  }
  sp++;
}

void op_ge() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("GT: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = (temp->data >= ax.data);
  }
  sp++;
}

void op_shl() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("SHL: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = (temp->data << ax.data);
  }
  sp++;
}

void op_shr() {
  val *temp = sp;
  if (ax.type != sp->type) {
    puts("SHR: Different types of operands");
    exit(-1);
  }
  if (ax.type == INT) {
    ax.data = (temp->data >> ax.data);
  }
  sp++;
}

void op_getelem() {
  val *id = sp;
  if (id->type != PTR) {
    puts("Invalid varible");
    exit(-1);
  }
  if (ax.type != INT) {
    puts("Invalid index");
    exit(-1);
  }
  st *e = (st *)id->data;
  long idx = ax.data;
  if (e->value->type == STR) {
    str *elem = (str *)e->value->data;
    if (idx >= elem->size || idx < 0) {
      puts("OOB Detected!");
      exit(-1);
    }
    // printf("size = %d\n",elem->size );
    ax.type = INT;
    ax.data = (long)elem->data[idx];
    sp++;
  } else if (e->value->type == LIST) {
    list *elem = (list *)e->value->data;
    if (idx >= elem->size || idx < 0) {
      puts("OOB Detected!");
      exit(-1);
    }
    ax.type = elem->elements[idx]->type;
    ax.data = (long)elem->elements[idx]->data;
    sp++;
  } else {
  }
}

void op_setelem() {
  /*  a[i] = b
      sp[0] = i
      sp[1] = a
      ax = b    */

  val *tmp = sp;
  if (tmp->type != INT) {
    puts("Invalid index");
    exit(-1);
  }
  long idx = tmp->data;
  sp++;
  tmp = sp;

  st *ptr = (st *)tmp->data;
  val *v = (val *)ptr->value;

  /* String */
  if (v->type == STR) {
    str *elem = (str *)v->data;
    if (idx >= elem->size || idx < 0) {
      puts("OOB Detected!");
      exit(-1);
    }
    elem->data[idx] = (char)ax.data;
    sp++;
  }
  /* List */
  else if (v->type == LIST) {
    list *elem = (list *)v->data;
    if (idx >= elem->size || idx < 0) {
      puts("OOB Detected!");
      exit(-1);
    }
    elem->elements[idx]->type = ax.type;
    elem->elements[idx]->data = ax.data;
    sp++;
  }
  else
  {
    puts("Invalid array setter");
    exit(-1);
  }
}

void op_addelem()
{
  val *lstval = sp;
  if (lstval->type != LIST) {
    puts("Invalid List assignment");
    exit(-1);
  }
  list *lst = (list *)lstval->data;

  if (lst->size == 0 && lst->capacity == 0) {
    lst->elements = (val **)calloc(10 * sizeof(val *), 1);
    lst->capacity = 10;
  }

  lst->size += 1;

  if (lst->size >= lst->capacity) {
    lst->elements =
        (val **)realloc(lst->elements, (2 * lst->capacity * sizeof(val *)));
    lst->capacity = lst->capacity * 2;
  }

  val *value = (val *)calloc(sizeof(val), 1);
  value->type = ax.type;
  value->data = ax.data;

  lst->elements[lst->size - 1] = value;

  sp++;
}

void op_push()
{
  --sp;
  val* tmp = sp;
  tmp->type = ax.type;
  tmp->data= ax.data;
}

void op_imm()
{
  ax.type = (long)*pc++;
  ax.data= (long)*pc++;
}


void op_get()
{
  if (ax.type != PTR)
  {
    puts("ERROR: Invalid Access!");
    exit(-1);
  }
  st* temp = (st*)ax.data;
  ax.type = temp->value->type;
  ax.data = temp->value->data;
}

void op_set()
{
  val* temp = (val*)sp;
  if (temp->type != PTR)
  {
    puts("ERROR: Invalid Access!");
    exit(-1);
  }
  st* target = (st*)temp->data;
  sp++;
  target->value->type = ax.type;
  target->value->data = ax.data;
}

void op_call()
{

  func* callee = (func*)*pc++;

  --cs_sp;
  *cs_sp = (long)pc;
  --cs_sp;
  *cs_sp = (long)scope;

  pc = (long*)callee->code;
}

void op_ret()
{
  scope = (st**)*cs_sp;
  ++cs_sp;
  pc = (long*)*cs_sp;
  ++cs_sp;
}
