#include <stdlib.h>
#include <vector>
#include <memory>
#include <iostream>
#include <cstring>
#include <unistd.h>
#define BUF_SIZE 1024

using namespace std;

enum Command {
  ADD = 1,
  DELETE,
  EDIT,
  VIEW,
  EXIT
};

class Note {
  public:
    char* name;
    char* content;

    Note() {
      this->name = NULL;
      this->content = NULL;
    }

    ~Note() {
      if (this->name) {
        delete this->name;
      }
      if (this->content) {
        delete this->content;
      }
    }

    void view() {
      if (name) {
        cout << "Name > ";
        cout << name << endl;
      }
      if (content) {
        cout << "Content > ";
        cout << content << endl;
      }
    }
};

class NoteMgr {
  public:
    unique_ptr<Note> ptr;
    Note* raw_ptr;
    bool use_up;

    NoteMgr() = default;
    ~NoteMgr() = default;
};

vector<unique_ptr<NoteMgr>> Notes;

uint32_t read_str(char* buf) {
  memset(buf, 0, BUF_SIZE);
  int32_t len = read(0, buf, BUF_SIZE - 1);

  if (len < 0 ) {
    exit(-1);
  }

  if (buf[len - 1] == '\n') {
    buf[len - 1] = '\0';
    return len - 1;
  }

  return len;
}

int32_t FindNote(char* s, uint32_t s_size, bool off_inc) {
  Note* note = NULL;
  int32_t find_idx = -1;

  for (int32_t i = 0; i < Notes.size(); i++) {
    if (Notes[i] && Notes[i]->use_up) {
      note = Notes[i]->ptr.get();
      if (strlen(note->name) == s_size && (!strcmp(note->name, s))) {
        find_idx = i;
      }
    }
  }

  if (find_idx == -1 && off_inc) {
    for(int32_t i = 0; i < Notes.size(); i++) {
      if (Notes[i] && !Notes[i]->use_up) {
        note = Notes[i]->raw_ptr;
        if (strlen(note->name) == s_size && !strcmp(note->name, s)) {
          find_idx = i;
        }
      }
    }
  }

  return find_idx;
}

NoteMgr* getNoteMgr(int32_t idx) {
  NoteMgr* mgr = NULL;

  if (idx == -1) {
    Notes.push_back(make_unique<NoteMgr>());
    mgr = Notes.back().get();
  } else {
    mgr = Notes[idx].get();
  }

  mgr->use_up = 1;
  mgr->ptr = NULL;
  mgr->raw_ptr = NULL;

  return mgr;
}

void addHandler() {
  char* name = NULL;
  char* content = NULL;

  Note* note = NULL;
  NoteMgr* mgr = NULL;

  char s[2][BUF_SIZE];
  bool contentFind = false;

  int32_t find_idx = -1;
  uint32_t s_size[2] = {0, };

  cout << "Input Name > ";

  s_size[0] = read_str(s[0]);
  find_idx = FindNote(s[0], s_size[0], 0);

  if (find_idx != -1) {
    note = Notes[find_idx]->ptr.get();
  }

  cout << "Input Content > ";
  s_size[1] = read_str(s[1]);

  if (find_idx != -1) {
    if (strlen(note->content) == s_size[1] && !strcmp(Notes[find_idx]->ptr->content, s[1])) {
      contentFind = true;
    }
  }

  if (find_idx != -1 && contentFind) {
    mgr = getNoteMgr(-1);
    mgr->use_up = 0;
    mgr->raw_ptr = Notes[find_idx]->ptr.get();
  } else {
    name = new char[s_size[0] + 1];
    content = new char[s_size[1] + 1];

    memset(name, 0, s_size[0] + 1);
    memcpy(name, s[0], s_size[0]);

    memset(content, 0, s_size[1] + 1);
    memcpy(content, s[1], s_size[1]);

    mgr = getNoteMgr(find_idx);
    mgr->ptr = make_unique<Note>();
    note = mgr->ptr.get();
    note->name = name;
    note->content = content;
  }

  cout << "Add Success" << endl;
}


void deleteHandler() {
  char s[BUF_SIZE];
  uint32_t s_size;
  int32_t unique_idx = -1;

  Note* note = NULL;

  cout << "Input Name > ";
  s_size = read_str(s);

  for (int32_t i = 0; i < Notes.size(); i++) {
    if (Notes[i] && Notes[i]->use_up) {
      note = Notes[i]->ptr.get();
    } else if (Notes[i]) {
      note = Notes[i]->raw_ptr;
    }

    if (note && strlen(note->name) == s_size && (!strcmp(s, note->name))) {
      if (Notes[i]->use_up)
        unique_idx = i;
      else if (!Notes[i]->use_up)
        Notes[i].reset(nullptr);
    }
  }
  if (unique_idx == -1) {
    cout << "Not Found" << endl;
  } else {
    Notes[unique_idx].reset(nullptr);
    cout << "Delete Success" << endl;
  }
}

void editHandler() {
  Note* note = NULL;
  char s[BUF_SIZE];

  int32_t s_size;
  int32_t find_idx;

  cout << "Input Name > ";

  s_size = read_str(s);
  find_idx = FindNote(s, s_size, 1);

  if (find_idx == -1) {
    cout << "Not Found" << endl;
    return;
  }

  if (Notes[find_idx] && Notes[find_idx]->use_up) {
    note = Notes[find_idx]->ptr.get();
  }
  else if (Notes[find_idx]) {
    note = Notes[find_idx]->raw_ptr;
  }

  if (note && strlen(note->name) == s_size && (!strcmp(note->name, s))) {
    cout << "Input New Content > ";
    s_size = read_str(s);

    if (strlen(note->content) >= s_size) {
      memcpy(note->content, s, s_size);
    } else {
      note->content = (char*)realloc(note->content, s_size + 1);

      memset(note->content, 0, s_size + 1);
      memcpy(note->content, s, s_size);
    }
  }
}

void viewHandler() {
  for (int i = 0; i < Notes.size(); i++) {
    if (Notes[i] && Notes[i]->use_up) {
      Notes[i]->ptr->view();
    } else if (Notes[i]) {
      Notes[i]->raw_ptr->view();
    }
  }
}

void handler() {
  int cmd;

  cin >> cmd;
  cin.ignore();

  switch (cmd) {
    case Command::ADD:
      addHandler();
      break;
    case Command::DELETE:
      deleteHandler();
      break;
    case Command::EDIT:
      editHandler();
      break;
    case Command::VIEW:
      viewHandler();
      break;
    case Command::EXIT:
      exit(0);
  }
}

void printMenu() {
  cout << "1. Add" << endl;
  cout << "2. Delete" << endl;
  cout << "3. Edit" << endl;
  cout << "4. View" << endl;
  cout << "5. Exit" << endl;
  cout << "> ";
}

void init() {
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stderr, 0, 2, 0);
}

int main(void) {
  init();

  while (1) {
    printMenu();
    handler();
  }
}
