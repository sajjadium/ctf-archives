/**
 * Santa's Database
 * Well, we should have started working on this months before December
 * but here we are, another damn crunch time. I hope Santa won't be
 * very disappointed (again).
 * 
 * There are a lot of missing features and pieces of code to refactor,
 * but let's do it next Christmas.
 * 
 * Missing features:
 * - arrays?
 * - joins?
 * - result piping?
 * - delete tables?
 * - floats?
 * - primary keys? constraints?
 * - save to file?
 * 
 * The databse uses our custom query language: GTL
 * Example:
 * CREATE TABLE _name=skrr; col1=STRING; col2=NUMBER;
 * READ TABLE _name=skr;
 * CREATE ROW _table=skrr; col1=something; col2=123;
 * UPDATE ROW _table=skrr; _id=1; col1=otherthing;
 * READ ROW _table=skrr;
 * 
 * LATER EDIT: THERE IS A DAMN BUG SOMEWHERE, I DON'T THINK THE SOFTWARE
 * WILL BE ABLE TO SUPPORT THE LOAD AROUND THE CHRISTMAS!!!!!!!
 * 
 * EVEN LATER EDIT: well, it's not that bad, it occurs in very specific situations
 * i think we are safe. anyway, who would try to hack Santa?
 * 
 * ANOTHER EDIT: there are HUGE memory leaks, but Santa has a super computer, 
 * he won't even notice
 * 
 * Made by Elf Development LTD
 */

#include <iostream>
#include <map>
#include <thread>
#include <mutex>
#include <vector>
#include <set>
#include <stdexcept>
#include <sstream>
#include <unistd.h>
#include <malloc.h>
#include <signal.h>

#include "types.h"
#include "helpers.h"

using namespace std;

// TODO: use a proper language parser
Command parseCommand(const string line) {
    Command cmd;
    for (const auto& instr: instructions) {
        if (line.compare(0, instr.size(), instr) == 0) {
            for (const auto& targ: targets) {
                if (line.compare(instr.size() + 1, targ.size(), targ) == 0) {
                    cmd.instruction = instr;
                    cmd.target = targ;

                    size_t pos = instr.size() + targ.size() + 2;
                    if (pos >= line.size()) break;

                    size_t newpos;
                    vector<string> parts;
                    while ((newpos = line.find('=', pos)) != string::npos) {
                        string part = line.substr(pos, newpos - pos);
                        parts.push_back(part);
                       
                        size_t end_pos = line.find(';', newpos);
                        if (end_pos != string::npos) {
                            parts.push_back(line.substr(newpos + 1, end_pos - newpos - 1));
                            pos = end_pos + 1;
                        } else {
                            pos = newpos + 1;
                        }
                    }

                    if (line[line.size() - 1] == pipe_sym) {
                        cmd.output = REDIRECT;
                        parts.push_back(line.substr(pos, line.size()-1));
                    } else if (line[line.size() - 1] == print_sym) {
                        cmd.output = FLUSH;
                        parts.push_back(line.substr(pos, line.size()-1));
                    } else if (line[line.size() - 1] == print_pipe_sym) {
                        cmd.output = FLUSH_REDIRECT;
                        parts.push_back(line.substr(pos, line.size()-1));
                    } else {
                        cmd.output = FLUSH;
                        parts.push_back(line.substr(pos));
                    }

                    for (size_t i = 0; i + 1 < parts.size(); i += 2) {
                        cmd.arguments[trim(parts[i])] = trim(parts[i+1]);
                    }

                    return cmd;
                }
            }
        }
    }

    // TODO: proper error handling
    cmd.instruction = "UNKNOWN";
    return cmd;
}

// TODO: use classes, it's C++ btw
struct Result {
    bool hasRows = false;
    string message;
    string tableName;
    vector<Column> columns;
    vector<set<Row>::iterator> rows;
};

// TODO: don't use globals!!!
mutex mtx;
map<string, Table> database;

Result readTable(const map<string, string>& args) {
    Result result;
    
    // TODO: get rid of magic strings
    if (database.find(args.at("_name")) == database.end()) {
        result.message = "Table not found.";
        return result;
    }
    result.tableName = args.at("_name");

    auto tbl = database[args.at("_name")];
    result.hasRows = true;
    result.columns.push_back({"name", STRING});
    result.columns.push_back({"type", STRING});

    unsigned int id = 0;
    set<Row> metaRows;
    for (auto& col: tbl.columns) {
        string typeName = ColTypeToStr(col.second.type);
        metaRows.insert({id++, {
            Value(STRING, &col.second.name),
            Value(STRING, &typeName),
        }});
    }
    for (set<Row>::iterator it = metaRows.begin(); it != metaRows.end(); it++) {
        result.rows.push_back(it);
    }

    // TODO: Logic and output is pretty mixed
    ostringstream stringStream;
    stringStream << "Read " << result.rows.size() << " rows.";
    result.message = stringStream.str();
    return result;
}

Result createTable(const map<string, string>& args) {
    Result result;

    mtx.lock();
    if (database.find(args.at("_name")) != database.end()) {
        result.message = "[ERROR] Table already exists";
        return result;
    }
    result.tableName = args.at("_name");
    mtx.unlock();

    // TODO: add proper logging

    Table newTable;
    for (auto& arg: args) {
        if (arg.first[0] == '_') continue;
        Column c;
        c.name = arg.first;
        if (arg.second == "NUMBER") c.type = NUMBER;
        else if (arg.second == "STRING") c.type = STRING;
        else if (arg.second == "BOOLEAN") c.type = BOOLEAN;
        // TODO: array
        newTable.columns[c.name] = c;
        newTable.indexes[c.name] = {};
    }


    mtx.lock();
    database[args.at("_name")] = newTable;
    result.message = "Table created.";
    mtx.unlock();


    return result;
}

Result updateTable(const map<string, string>& args) {
    Result result;

    mtx.lock();
    if (database.find(args.at("_name")) == database.end()) {
        result.message = "[ERROR] Table does not exist";
        return result;
    }
    result.tableName = args.at("_name");
    mtx.unlock();

    mtx.lock();
    auto& newTable = database[args.at("_name")];
    for (auto& arg: args) {
        if (arg.first[0] == '_') continue;
        Column c;
        c.name = arg.first;
        // TODO: remove code duplication
        if (arg.second == "NUMBER") c.type = NUMBER;
        else if (arg.second == "STRING") c.type = STRING;
        else if (arg.second == "BOOLEAN") c.type = BOOLEAN;
        // TODO: array
        newTable.columns[c.name] = c;
        newTable.indexes[c.name] = {};

        set<Row> newRows;
        for (auto it: newTable.rows) {
            it.values.push_back({});
            newRows.insert(it);
        }
        newTable.rows = newRows;
    }
    mtx.unlock();

    result.message = "Updated table.";
    return result;
}

Result createRow(const map<string, string>& args) {
    Result result;

    mtx.lock();
    const auto tableName = args.at("_table");
    if (database.find(tableName) == database.end()) {
        result.message = "[ERROR] Table not found";
        return result;
    }
    auto& tbl = database[tableName];
    result.tableName = args.at("_table");
    mtx.unlock();


    Row newRow;
    for (auto& col: tbl.columns) {
        auto name = col.second.name;
        auto type = col.second.type;

        if (args.find(name) == args.end()) {
            result.message = "[ERROR] Missing column.";
            return result;
        }
        auto strVal = args.at(name);

        if (type == NUMBER) {
            auto v = stoll(strVal);
            newRow.values.push_back(Value(NUMBER, &v));
        } else if (type == BOOLEAN) {
            auto i = stoll(strVal);
            bool v = i ? true : false;
            newRow.values.push_back(Value(BOOLEAN, &v));
        } else if (type == STRING) {
            newRow.values.push_back(Value(STRING, &strVal));
        }
    }
    
    result.message = "Added 1 row.";


    mtx.lock();
    newRow.id = tbl.rowIdSeq++;
    tbl.rows.insert(newRow);
    unsigned int i = 0;
    for (auto& col: tbl.columns) {
        auto name = col.second.name;
        //auto type = col.second.type;

        // indexes could be more efficinet?
        tbl.indexes[name].valueToId.insert({newRow.values[i], newRow.id});
        i++;
    }
    mtx.unlock();


    return result;
}

Result readRow(const map<string, string>& args, Result& InputSet, bool piped) {
    Result result;

    mtx.lock();
    const auto tableName = args.at("_table");
    if (database.find(tableName) == database.end() && !piped) {
        result.message = "[ERROR] Table not found";
        return result;
    }
    result.tableName = args.at("_table");
    auto& tbl = database[tableName];
    mtx.unlock();
    
    // unfortunately joins are very slow
    // TODO: use indexes on joins
    if (piped && InputSet.hasRows) {
        vector<set<Row>::iterator> newRows;
        for (auto& arg: args) {
            if (arg.first == "_id") {
                auto id = (unsigned int)stoll(arg.second);
                vector<set<Row>::iterator> newRow;
                for (auto it: InputSet.rows) {
                    if (it->id == id) {
                        newRow.push_back(it);
                        break;
                    }
                }
                result.columns = InputSet.columns;
                result.hasRows = true;
                result.message = "Read 1 row.";
                result.rows = newRow;
                return result;
            } else if (arg.first[0] == '_') continue;
            else {
                auto& colName = arg.first;
                string strVal  = arg.second;

                if (tbl.columns.find(colName) == tbl.columns.end()) {
                    result.message = "[ERROR] Column does not exist";
                    return result;
                }

                auto type = tbl.columns[colName].type;
                Value val;
                if (type == NUMBER) {
                    auto v = stoll(strVal);
                    val = Value(NUMBER, &v);
                } else if (type == BOOLEAN) {
                    auto i = stoll(strVal);
                    bool v = i ? true : false;
                    val = Value(BOOLEAN, &v);
                } else if (type == STRING) {
                    val = Value(STRING, &strVal);
                }

                unsigned int i = 0;
                for (auto& col: tbl.columns) {
                    for (auto& row_it: InputSet.rows) {
                        if (i < row_it->values.size() && val == row_it->values[i]) {
                            newRows.push_back(row_it);
                        }
                    }
                    i++;
                }
            }
        }

        // no filtering
        if (args.size() == 1) {
            newRows = InputSet.rows;
        }

        result.columns = InputSet.columns;
        result.hasRows = true;
        result.rows = newRows;
        ostringstream stringStream;
        stringStream << "Read " << newRows.size() << " rows.";
        result.message = stringStream.str();

        return result;
    } else if (piped && !InputSet.hasRows) {
        result.message = "[ERROR] Something is broken";
        return result;
    }

    mtx.lock();

   
    set<unsigned int> found;
    set<unsigned int> curr_found;
    set<unsigned int> output;

    for (auto& it: tbl.rows) {
        found.insert(it.id);
    }

    
    for (auto& arg: args) {
        if (arg.first == "_id") {
            auto r = Row{(unsigned int)stoll(arg.second)};
            if (tbl.rows.find(r) != tbl.rows.end()) { curr_found.insert(r.id); }
        } else if (arg.first[0] == '_') continue;
        else {
            auto& colName = arg.first;
            string strVal  = arg.second;

            if (tbl.columns.find(colName) == tbl.columns.end()) {
                result.message = "[ERROR] Column does not exist";
                return result;
            }

            auto type = tbl.columns[colName].type;
            Value val;
            if (type == NUMBER) {
                auto v = stoll(strVal);
                val = Value(NUMBER, &v);
            } else if (type == BOOLEAN) {
                auto i = stoll(strVal);
                bool v = i ? true : false;
                val = Value(BOOLEAN, &v);
            } else if (type == STRING) {
                val = Value(STRING, &strVal);
            }

            auto it = tbl.indexes[colName].valueToId.find(val);
            for (; it != tbl.indexes[colName].valueToId.end(); ++it) {
                if (it->first == val) curr_found.insert(it->second);
                else break;
            }
        }

        // i think that it's damn slow
        set_intersection(found.begin(), found.end(),
            curr_found.begin(), curr_found.end(),
            inserter(output,output.begin()));

        found = output;
        curr_found.clear();
        output.clear();
    }
    
    result.hasRows = true;
    for (auto& col: tbl.columns) {
        result.columns.push_back(col.second);
    }

    for (auto id: found) {
        Row r = {id};
        auto row_it = tbl.rows.find(r);
        result.rows.push_back(row_it);
    }
    mtx.unlock();

    ostringstream stringStream;
    stringStream << "Read " << found.size() << " rows.";
    result.message = stringStream.str();

    return result;
}

Result updateRow(const map<string, string>& args, Result& InputSet, bool piped) {
    Result result;

    mtx.lock();
    const auto tableName = args.at("_table");
    if (database.find(tableName) == database.end()) {
        result.message = "[ERROR] Table not found";
        return result;
    }
    auto& tbl = database[tableName];
    result.tableName = args.at("_table");
    mtx.unlock();

    if (piped && !InputSet.hasRows) {
        result.message = "[ERROR] Something is broken";
        return result;
    } else if (piped && InputSet.hasRows) {
        mtx.lock();
        unsigned int i = 0;
        for (auto& col: tbl.columns) {
            auto name = col.second.name;
            auto type = col.second.type;

            if (args.find(name) == args.end()) {
                i++;
                continue;
            }
            auto strVal = args.at(name);
            Value newVal;

            if (type == NUMBER) {
                auto v = stoll(strVal);
                newVal = Value(NUMBER, &v);
            } else if (type == BOOLEAN) {
                auto i = stoll(strVal);
                bool v = i ? true : false;
                newVal = Value(BOOLEAN, &v);
            } else if (type == STRING) {
                newVal = Value(STRING, &strVal);
            }

            // clear the index for current column
            tbl.indexes[name].valueToId.clear();

            // update rows
            for (auto& row_it: InputSet.rows) {
                if (i < row_it->values.size()) {
                    if (type == NUMBER) {
                        *static_cast<long long int*>(row_it->values[i].data) = *static_cast<long long int*>(newVal.data);
                    } else if (type == STRING) {
                         *static_cast<string*>(row_it->values[i].data) = *static_cast<string*>(newVal.data);
                    } else {
                        row_it->values[i] = newVal;
                    }
                }
            }

            // reinsert into the index 
            for (auto& rit: tbl.rows) {
                tbl.indexes[name].valueToId.insert({rit.values[i], rit.id});
            }
        }
        mtx.unlock();

        result.message = "Updated rows.";
        result.hasRows = true;
        result.columns = InputSet.columns;
        result.rows = InputSet.rows;
        return result;
    }

    mtx.lock();
    const auto id = (unsigned int)stoul(args.at("_id"));
    Row r = {id};
    if (tbl.rows.find(r) == tbl.rows.end()) {
        result.message = "[ERROR] Row not found";
        return result;
    }


    auto it = tbl.rows.find(r);
    auto newRow = *it;
    tbl.rows.erase(it);
    mtx.unlock();

    // CODE DUPLICATION AGAIN
    unsigned int i = 0;
    for (auto& col: tbl.columns) {
        auto name = col.second.name;
        auto type = col.second.type;

        if (args.find(name) == args.end()) {
            i++;
            continue;
        }
        auto strVal = args.at(name);

        if (type == NUMBER) {
            auto v = stoll(strVal);
            newRow.values[i] = Value(NUMBER, &v);
        } else if (type == BOOLEAN) {
            auto i = stoll(strVal);
            bool v = i ? true : false;
            newRow.values[i] = Value(BOOLEAN, &v);
        } else if (type == STRING) {
            newRow.values[i] = Value(STRING, &strVal);
        }

        mtx.lock();
        tbl.indexes[name].valueToId.clear();
        tbl.indexes[name].valueToId.insert({newRow.values[i], newRow.id});
        for (auto& rit: tbl.rows) {
            tbl.indexes[name].valueToId.insert({rit.values[i], rit.id});
        }
        
        mtx.unlock();

        i++;
    }


    mtx.lock();
    result.hasRows = true;
    for (auto& col: tbl.columns) {
        result.columns.push_back(col.second);
    }
    result.rows.push_back(tbl.rows.insert(newRow).first);
    mtx.unlock();


    result.message = "Updated 1 row.";
    return result;
}

Result deleteRow(const map<string, string>& args) {
    Result result;

    mtx.lock();
    const auto tableName = args.at("_table");
    if (database.find(tableName) == database.end()) {
        result.message = "[ERROR] Table not found";
        return result;
    }
    result.tableName = args.at("_table");
    mtx.unlock();


    mtx.lock();
    auto& tbl = database[tableName];
    const auto id = (unsigned int)stoul(args.at("_id"));
    Row r = {id};
    if (tbl.rows.find(r) == tbl.rows.end()) {
        result.message = "[ERROR] Row not found";
        return result;
    }

    tbl.rows.erase(tbl.rows.find(r));
    mtx.unlock();

    unsigned int i = 0;
    for (auto& col: tbl.columns) {
        auto name = col.first;
        // TODO: find a better way than clearing the entire index
        tbl.indexes[name].valueToId.clear();
        for (auto& rit: tbl.rows) {
            tbl.indexes[name].valueToId.insert({rit.values[i], rit.id});
        }
        i++;
    }


    result.message = "Deleted 1 row.";
    return result;
}

// TODO: use a proper command interpreter
// TODO: support output piping
Result runCommand(Command& cmd, Result& InputSet, bool piped) {
    const string& instr = cmd.instruction;
    const map<string, string>& args = cmd.arguments;

    if (cmd.instruction == "SLEEP") {
        usleep(stoul(args.at("time")));
        Result result = InputSet;
        result.message += " (slept)";
        return result;
    }

    // TABLE commands ignore piped input
    if (cmd.target == "TABLE") {
        if (instr == "CREATE") {
            return createTable(args);
        } else if (instr == "READ") {
            Result result;
            auto table = database.find(args.at("_name"));
            if (table == database.end()) {
                result.message = "[ERROR] Table does not exist";
                return result;
            }
            return readTable(args);
        } else if (instr == "UPDATE") {
            return updateTable(args);
        } else if (instr == "DELETE") {

        }
    } else if (cmd.target == "ROW") {
        if (instr == "CREATE") {
            return createRow(args);
        } else if (instr == "READ") {
            return readRow(args, InputSet, piped);
        } else if (instr == "UPDATE") {
            return updateRow(args, InputSet, piped);
        } else if (instr == "DELETE") {
            return deleteRow(args);
        } 
    }
    return {};
}

// so many couts that i don't understand a line
void execute(const vector<string> commands, ostream& real_out, mutex& output_mtx) {
    ostringstream out;

    Result result;
    bool redirect = false;
    for (const auto line: commands) {
        auto cmd = parseCommand(line);
        out << "[COMMAND] " << line << endl;
        //cout << "Do " << line << endl;

        auto curr_result = runCommand(cmd, result, redirect);
        if (cmd.output == FLUSH || curr_result.rows.size() == 0) {
            out << "[RESULT] " << curr_result.message << endl;
            if (curr_result.hasRows) {
                out << "| _id | ";
                for (auto& col: curr_result.columns) {
                    out << col.name << " | ";
                }
                out << endl;
                for (auto& row: curr_result.rows) {
                    out << "| " << row->id << " | ";
                    unsigned int i = 0;
                    for (auto& val: row->values) {
                        if (val.type == CNULL) { 
                            out << "(null) | ";
                        } else if (val.type != curr_result.columns[i].type || i >= curr_result.columns.size()) {
                            out << "invalid | ";
                        } else {
                            out << val << " | ";
                        }
                        i++;
                    }
                    out << endl;
                }
            }

            result.hasRows = false;
            result.columns.clear();
            result.rows.clear();
        } else if (cmd.output == REDIRECT) {
            redirect = true;
            result = curr_result;
        } else if (cmd.output == FLUSH_REDIRECT) {
            out << "[RESULT] " << curr_result.message << endl;
            if (curr_result.hasRows) {
                out << "| _id | ";
                for (auto& col: curr_result.columns) {
                    out << col.name << " | ";
                }
                out << endl;
                for (auto& row: curr_result.rows) {
                    out << "| " << row->id << " | ";
                    unsigned int i = 0;
                    for (auto& val: row->values) {
                        if (val.type == CNULL) { 
                            out << "(null) | ";
                        } else if (val.type != curr_result.columns[i].type || i >= curr_result.columns.size()) {
                            out << "invalid | ";
                        } else {
                            out << val << " | ";
                        }
                        i++;
                    }
                    out << endl;
                }
            }

            redirect = true;
            result = curr_result;
        }
    }

    output_mtx.lock();
    real_out << out.str();
    output_mtx.unlock();
}

int main() {
    //setbuf(stdin, nullptr);
    //setbuf(stdout, nullptr);

    mallopt(M_ARENA_MAX, 4);

    cout << "Santa's database" << endl;
    cout << endl;
    cout << "RUN <newline> ... <newline> END -> execute a query on a new thread" << endl;
    cout << "LIST -> list all threads" << endl;
    cout << "OUTPUT <newline> <n> -> display the output of thread n" << endl; 
    cout << "OUTPUT_ALL -> display all outputs" << endl;
    cout << "EXIT -> well..." << endl;
    cout << endl;

    string* word = new string;
    mutex output_mtx;
    map<unsigned int, ostringstream> outputs;
    unsigned int id = 0;
    vector<thread> threads;

    // TODO: use a socket interface for communication

    while (true) {
        getline(cin, *word);
        if (*word == "WAIT") {
            for (auto& t: threads) {
                t.join();
            }
            threads.clear();
        } else if (*word == "EXIT") {
            for (auto& t: threads) {
                t.join();
            }
            threads.clear();

            /*output_mtx.lock();
            for (auto& it: outputs) {
                cout << endl;
                cout << it.second.str() << endl;
                cout << endl;
            }
            output_mtx.unlock();*/
            return 0;
        } else if (*word == "RUN") {
            string line;
            getline(cin, line);
            vector<string> lines;
            while (line != "END") {
                //cout << "got: " << line << endl;
                lines.push_back(line);
                getline(cin, line);
            }

            //cout << "Starting thread " << id << endl;
            threads.emplace_back(thread{
                [&output_mtx, &outputs, &id, lines]() {
                    output_mtx.lock();
                    auto tid = id++;
                    outputs[tid] = {};
                    outputs[tid] << "Thread " << tid << endl;
                    output_mtx.unlock();
                    execute(lines, outputs[tid], output_mtx);
                    cout << "Ended thread " << tid << endl;
                }
            });
        } else if (*word == "LIST") {
            output_mtx.lock();
            for (auto& it: outputs) {
                cout << it.first << " ";
            }
            cout << endl;
            output_mtx.unlock();
        } else if (*word == "OUTPUT_ALL") {
            output_mtx.lock();
            for (auto& it: outputs) {
                cout << endl;
                cout << it.second.str() << endl;
                cout << endl;
            }
            output_mtx.unlock();
        } else if (*word == "OUTPUT") {
            output_mtx.lock();
            string sid;
            getline(cin, sid);
            unsigned int tid = (unsigned int)stoul(sid);
            cout << endl;
            cout << outputs[tid].str() << endl;
            cout << endl;
            output_mtx.unlock();
        }
    }

    return 0;
}
