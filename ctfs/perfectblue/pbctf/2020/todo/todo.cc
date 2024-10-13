//Name:  theKidOfArcrania
//Class: 7331 (It's a very l33t class :3 )
//Date:  29 April 2018
//         ^^ yes this is the actual date when I started writing this.

// NOTE: I *TOTALLY* DID NOT PAY MY FRIEND $13.37 TO WRITE THIS CODE FOR A FINAL
// PROJECT IN MY CS PROGRAMMING CLASS. Please do not give me a zero, because you
// can see I totally spent a whole lot of time commenting (and writing) this
// code out for you to grade. Please give me a 100 because I know I deserve
// that, u the best thx!

#define _GNU_SOURCE
#include <errno.h>
#include <iostream>

#include "string2.h"

#define fudge(x) std::cout << x << std::endl

// This to-do list manager the string class. We implement a simple to-do list
// manager. This is not fully implemented, please bear with it!
//
// I heard of a student that got docked points for not commenting enough. So he
// decided to write a comment on every single line :D . I did not go inasmuch so
// far, but here's a bit of comment(ary) for my code.

const int MAX_TASKS = 10000;
const int NUM_CATEGORIES = 6;
const char* names[NUM_CATEGORIES] = {"Calculus", "Economics", "English (yuck)", 
  "History", "Computer Science :D", "Physics"};

int      taskCount[NUM_CATEGORIES];
String*  tasks[NUM_CATEGORIES];
bool     changed = false;

// Used to eat newlines.
std::string xx;

// Function prototypes (because I have to put them)
int promptCategories();
int promptChoices();

void addTask(int categ);
void viewTodos(int categ);
void finishTasks(int categ);
void save(); 
void eatNewline();

// Main function
int main() {

  setbuf(stdout, nullptr);
  setbuf(stdin, nullptr);

  fudge("To-do list manager PRO v0.95");
  fudge("We manage your daily tasks!\n");

  //TODO: load from tasks.dat
  fudge(program_invocation_short_name << ": ./tasks.dat: Permission denied");
  fudge("WARNING: data is corrupted! Cannot access tasks.dat\n");

  while (true) {
    
    // Take strings and pipe it to cout
    fudge("Please select a choice: ");
    fudge("  1 - Add new task.");
    fudge("  2 - View to-dos.");
    fudge("  3 - Finish tasks.");
    fudge("  4 - Save to disk.");
    fudge("  5 - Exit.");
    std::cout << ">>> ";

    int resp = 42; // the (default) answer/response to the world is 42.
    std::cin >> resp;
    eatNewline();

    // Process response.
    switch (resp) {
      case 1: // Add
        addTask(promptCategories());
        break;
      case 2: // View
        viewTodos(promptCategories());
        break;
      case 3: // Finish
        finishTasks(promptCategories());
        break;
      case 4: // Save
        save();
        break;
      case 5: // Exit
        if (changed) {
          std::cout << "Do you want to save? (y/n) ";
          if (std::cin.get() == 'y') {
            save();
          }
        }
        exit(0);
        break;
      default:
        fudge("Invalid choice!");
    }

  }
}

int promptCategories() {
  fudge("Please select a category: ");      // Print a select category
  for (int i = 0; i < NUM_CATEGORIES; i++) {  // From 0 to NUM_CATEGORIES
    std::cout << "  " << i << " - " << names[i] << std::endl; //print a line and name
  }

  int resp = -1; //why is this -1? (I forgot)
  while (resp == -1) { // oh wait! while user gives -1 as a response
    std::cout << ">>> ";
    std::cin >> resp;
    eatNewline();
    if (resp < 0 || resp >= NUM_CATEGORIES) { // if resp is less than zero or greater than NUM_CATEGORIES
      fudge("Invalid choice!");
      resp = -1;
    }
  } 
  return resp;
}

void addTask(int categ) {
  int count;
  std::cout << "Input number of tasks to add: ";
  std::cin >> count;
  eatNewline();

  if (count <= 0) {
    // What are you trying to do?
    fudge("What are you trying to do? This ain't a CTF problem!");
    // what's a CTF problem? :confused:
    exit(3);
  } else if (count > MAX_TASKS || count + taskCount[categ] > MAX_TASKS) {
    //Okay bummer... maybe something else should happen?
    fudge("You have exceeded the max task count!");
    exit(3);
  }

  changed = true; // changed is now true

  String *arr;
  if (taskCount[categ] == 0) { // if the category is zero
    tasks[categ] = arr = new String[count]; //it becomes arr...
  } else {
    String* old = tasks[categ]; // old pointer?
    arr = tasks[categ] = new String[count + taskCount[categ]]; //new array?
    for (int i = 0; i < taskCount[categ]; i++) {
      tasks[categ][i] = old[i]; 
      arr++; // wait why does this get incremented again?
    }
    delete old;
  }

  // Read each task
  for (int i = 0 ; i < count; i++) {
    std::cin >> arr[i];
  }

  taskCount[categ] += count; 
  
  fudge("Successfully added some new tasks.");
}

void viewTodos(int categ) {
  if (taskCount[categ] == 0) {
    // No pending tasks
    fudge("You have no pending tasks in " << names[categ] << ".");
    return;
  }

  //current tasks
  std::cout << "Current tasks for " << names[categ] << ": " << std::endl;
  for (int i = 0; i < taskCount[categ]; i++) {
    std::cout << "  " << tasks[categ][i] << std::endl;
  }
}

void finishTasks(int categ) {
  // Check if we have any tasks first.
  if (taskCount[categ] == 0) {
    std::cout << "You have no pending tasks in " << names[categ] << "." << 
      std::endl;
    return;
  }

  while (taskCount[categ] != 0) {
    std::cout << "Please select a task to complete (or -1 to go back): " 
      << std::endl;  //    tell user to select a task
    for (int i = 0; i < taskCount[categ]; i++) { //   and what to select
      std::cout << "  " << (i + 1) << " - " << tasks[categ][i] << std::endl;
    }

    //Okay wait, now resp is set to 0? what's with all these changes?
    int resp = 0;
    while (resp == 0) {
      std::cout << ">>> ";
      std::cin >> resp;
      eatNewline();
      if (resp != -1 && (resp < 1 || resp > taskCount[categ])) {
        std::cout << "Invalid choice!" << std::endl;
        resp = 0;
      }
    }

    if (resp == -1) // -1???
      break;

    changed = true; //changed is set to true


    taskCount[categ]--;
    int ind = resp - 1;
    while (ind < taskCount[categ]) {
      tasks[categ][ind] = std::move(tasks[categ][ind + 1]);// like a moving van from one home to the next
      ind++;
    }
  }

  if (taskCount[categ] == 0) {
    std::cout << "You have no more pending tasks!" << std::endl;
    
    //Free the array since we already sent all the messages.
        //SCREW THAT MEMORY LEAK. WHY THE HECK IS THIS CAUSING AN ERROR?
  // delete tasks[categ]; // <-- im just gonna comment out this line.
     
    tasks[categ] = nullptr; // no uaf for you!
  }
}

void save() {
  // TODO: actually save it to tasks.dat?
  changed = false;
  std::cout << program_invocation_short_name << ": ./tasks.dat: Permission denied" << std::endl;
}

void eatNewline() {
  int c;
  while ((c = std::cin.get()) != '\n') {
    if (c == -1)
      exit(1);
  }
}



