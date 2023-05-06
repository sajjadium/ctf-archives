#include <cstddef>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <vector>
#include <string.h>

class Note {
public:
    Note(const std::string& name, const std::string& content)
        : name_(name), content_(content) {}
    
    virtual std::string& getName() {
        return name_;
    }

    virtual std::string& getContent() {
        return content_;
    }

    virtual void printContents() const {
        char buf[32];
        char const* noteStart = "     _______________________  \n"
                                "   =(__    ___      __     _)=\n";
        char const* noteEnd   = "   =(_______________________)=\n";
        char const* line      = "     | %-19s |\n";

        std::string output(noteStart);
        for (size_t i = 0; i < content_.length(); i += 19) {
            std::memset(buf, 0, sizeof(buf));
            auto part = content_.substr(i, 19);
            std::snprintf(buf, sizeof(buf), line, part.data());
            output += std::string(buf);
        }
        output += noteEnd;
        std::cout << output << std::endl;
    }

    virtual void lockNote(const char *key, size_t key_size) {
        // Overwrite and discard
        auto key_index = 0;
        for (auto &c: content_) {
            c ^= *key;
            key_index = (key_index + 1) % key_size;
        }
        content_ = "=== LOCKED ===";
    }

    void setName(const std::string& name) {
        name_ = name;
    }

    void setContent(const std::string& content) {
        content_ = content;
    }

private:
    std::string name_;
    std::string content_;
};


class Notepad {
public:
    Notepad() {
        notes_.reserve(5);
    }

    void createNote(const std::string& name, const std::string& content) {
        notes_.emplace_back(name, content);
    }

    auto getNote(size_t idx) {
        return notes_.at(idx);
    }

    void editNote(const std::string& name, const std::string& content) {
        currentNote_->setName(name);
        currentNote_->setContent(content);
    }

    bool selectNoteByName(const std::string& search) {
        auto note = findNoteByName(search);
        if (note != nullptr) {
            currentNote_ = note;
            return true;
        }
        return false;
    }

    void printCurrentNote() const {
        currentNote_->printContents();
    }
    
    void lockCurrentNote(std::string key, size_t key_size) {
        currentNote_->lockNote(key.c_str(), *(size_t *)key_size);
    }


private:
    Note* findNoteByName(const std::string& search) {
        auto result = std::find_if(
            notes_.begin(), 
            notes_.end(), 
            [&](Note& note){
                if (std::strstr(note.getName().data(), search.data())) {
                    return true;
                }
                return false;
            }
        );
        if (result != notes_.end()) {
            return &*result;
        }
        return nullptr;
    }

    std::vector<Note> notes_;
    Note* currentNote_;
};

