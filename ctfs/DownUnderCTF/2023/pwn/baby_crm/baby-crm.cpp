#include <vector>
#include <string>
#include <iostream>
#include <unistd.h>
#include <stdio.h>

#define DESCRIPTION_SIZE 0x50


using namespace std;

void fill_buf(char * buf, int len) {

    int i = 0;
    int c;
    for(int i = 0; i<len; i++) {
        buf[i] = c = getchar();
        if (c == '\n') {
            break; 
        }
    }
}

class Order {
  public:
  
    Order(): value_(0){};

    Order(double value) {
      value_ = value;
    }

    ~Order() {
      delete description_;
    }
    
    void print_order() {
      cout << "Value: " << value_ << endl;
      cout << "Description: " << endl;
      print_description();

    }

    double value() {
      return value_;
    }
    char * description() {
      return description_;
    }

    void print_description() {
      fwrite(description_, DESCRIPTION_SIZE, 1, stdout);
    }

    void edit_description() {
      cout << "New description: ";
      if (description_ == nullptr) {
        cout << "Description not yet set" << endl;
        return;
      }
      fill_buf(description_, DESCRIPTION_SIZE);
    }

    void set_description() {

      cout << "> ";
      char * desc_buf = (char*)malloc(DESCRIPTION_SIZE);
      fill_buf(desc_buf, DESCRIPTION_SIZE);

      description_ = desc_buf;
    }

  void help() {
    cout << "Use an order to track the value and details \
of a single order. A Customer may hold several orders." << endl;
  }

  private:

    char* description_;
    double value_;
     
};

class Customer {
  public:

    Customer() {
      revenue_ = 0;
      orders_ = new vector<Order*>();
    }

    string name() {
      return name_;
    }

    void set_name(string name) {
      name_ = name;
    }

    void set_description(string description) {
      description_ = description; 
    }

    vector<Order*> * orders() {
      return orders_;
    }
   
    void print() {
      cout << "Name: " << name_ << endl;
      cout << "Description: " << description_ << endl;
      cout << "Orders: " << endl;
      for (auto o : *orders_) {
        o->print_order();
      }
    }

    void help() {
      cout << "Use Customer to track a single customer, including their name\
, description, and their current open orders." << endl;
    }

  private:
    string name_;
    float revenue_; 
    string description_;
    vector<Order*> * orders_;
};

vector<Customer*> customers;

void help() {
  
  Order o;
  Customer c;
  size_t option;

  cout << "1. Order Help" << endl;
  cout << "2. Customer Help" << endl;
  cout << "> ";
  cin >> option;
  switch (option) {
    case 1:
      o.help();
      break;
    case 2:
      c.help();
      break;
  }
}                               

int menu(){
  char buf[0x100];
  cout << "1. New Customer" << endl;
  cout << "2. Alter Customer" << endl;
  cout << "3. Show Customer" << endl;
  cout << "4. Help" << endl;
  cout << "> ";
  int choice;
  scanf("%d", &choice);
  return choice;
}
                                       
void new_customer() {

  Customer * customer = new Customer();
  cout << "Customer name: ";
  string name;
  cin >> name;
  customer->set_name(name);
  customers.push_back(customer);
}

Order * new_order() {
  cout << "Order value: ";
  float value;
  cin >> value;
  Order * order = new Order(value);
  order->set_description();
  return order;
}

void alter_customer(){

  char buf [0x10];
  size_t choice;
  size_t option;

  cout << "Customer to alter: ";
  cin >> choice;

  if (choice >= customers.size()) {
    cout << "No such customer" << endl;
    return;
  } 
  Customer * customer = customers[choice];
  cout << "1. Change name" << endl;
  cout << "2. Change description" << endl;
  cout << "3. Add Order" << endl;
  cout << "4. Edit Order" << endl;
  cout << "5. Mark Order complete" << endl;
  cout << "> ";
  cin >> option;

  switch(option) {
    case 1: {
      cout << "New name: ";
      string name;
      cin >> name;
      customer->set_name(name);
      break;
    }
    case 2: {
      cout << "New description: ";
      string description;
      cin >> description;
      customer->set_description(description);
      break;
    }
    case 3: {
      Order * order = new_order();
      customer->orders()->push_back(order); 
      break;
    }
      
    case 4: {
      cout << "Order to edit: ";
      size_t idx;
      cin >> idx;
      getchar();
      if (idx >= customer->orders()->size()){
        cout << "No such order" << endl;
        return;
      }
      Order * order = customer->orders()->at(idx);
      order->edit_description();
      break;
    }
    default:
      cout << "No such option" << endl;

  }
}  

void show_customer() {
  Customer * customer;

  size_t choice;
  cout << "Customer to show: " << endl;
  cin >> choice;
  customer = customers[choice];
  customer->print();
}
void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main()                             
{      
  init();
  int option;     
  while (true) {
    option = menu();
    switch(option) {
      case 1:
        new_customer();
        break;
      case 2:
        alter_customer();
        break;
      case 3:
        show_customer();
        break;
      case 4:
        help();
        break;
      default:
        goto exit;
    }
  }                                     
exit:                                   
  return 0;                            
}  
