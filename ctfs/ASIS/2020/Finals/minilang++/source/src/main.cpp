#include <iostream>
#include <fstream>
#include <regex>
#include <iomanip>

#include "lexer/lexer.h"
#include "parser/parser.h"
#include "visitor/xml_visitor.h"
#include "visitor/semantic_analysis.h"
#include "visitor/interpreter.h"
#include "table/table.h"

/**
 * The main function implements the REPL interface.
 * The
 * @return 0
 */

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    // REPL Greeting
    std::cout << "\e[1mMiniLang\e[0m 1.0.0  [6th May, 2018]" << std::endl;
    std::cout << "Type \"#help\" for more information." << std::endl;

    // Create Global Scopes
    visitor::SemanticScope semantic_global_scope;
    visitor::InterpreterScope interpreter_global_scope;

    // Indefinite User input
    for(;;){

        // Variables for user input
        std::string input_line;
        std::string program;
        bool file_load = false;
        bool expr = false;

        // User prompt
        std::cout << "\n>>> _\b";
        std::getline(std::cin, input_line);
        if(!std::cin.good()) {
            break;
        }

        // Remove leading/trailing whitespaces
        input_line = std::regex_replace(input_line, std::regex("^ +| +$"), "$1");

        // Quit
        if(input_line == "#quit"){
            break;
        }

        // Help
        else if(input_line == "#help"){

            std::cout << "\n" << "Welcome to MiniLang 1.0.0! \n\n";

            std::cout << "To use this interactive REPL, just type in regular MiniLang commands and hit\n";
            std::cout << "enter. You can also make use of the following commands: \n\n";

            std::cout << " #load \e[1;3;4mfile-path\e[0m  ";
            std::cout << "Loads variable and function declarations from a specified\n";
            std::cout << std::setw(18);
            std::cout << "" << "file into memory, e.g.\n";
            std::cout << std::setw(18);
            std::cout << "" << ">>> #load ~/hello_world.prog\n\n";
            std::cout << " #quit            Exits the MiniLang REPL.\n\n";
            std::cout << " #st              Displays the symbol table, a list of currently declared \n";
            std::cout << std::setw(18);
            std::cout << "" << "functions and variables in the global scope.\n\n";
            std::cout << " #clear           Clears the terminal window." << std::endl;
        }

        // Load File
        else if(input_line.substr(0, 5) == "#load"){
            std::cout << input_line << std::endl;

            // If length <= 6, then the user specified no file
            if(input_line.size() <= 6){
                std::cout << "File path expected after '#load'." << std::endl;
            }

            else{

                // Get file directory
                std::string file_dir = input_line.substr(6);

                // Remove any whitespaces from that
                file_dir = std::regex_replace(file_dir, std::regex("^ +| +$"), "$1");

                // Read the file
                std::ifstream file;
                file.open(file_dir);

                if(!file)
                    std::cout << "Could not load file from \"" + file_dir + "\"." << std::endl;

                else {
                    // Convert whole program to std::string
                    std::string line;
                    while(std::getline(file, line))
                        program.append(line + "\n");

                    // Flag to indicate that this statement is for file loading
                    file_load = true;
                }

                file.close();
            }
        }

        // Symbol Table
        else if(input_line == "#st"){
            std::cout << "\e[1mCurrently Declared Variables and Functions\e[0m" << std::endl;
            TextTable vt('-', '|', '+');
            vt.add("Name");
            vt.add("Type");
            vt.add("Current Value");
            vt.endOfRow();
            for(auto var : interpreter_global_scope.variable_list()) {
                vt.add(std::get<0>(var));
                vt.add(std::get<1>(var));
                vt.add(std::get<2>(var));
                vt.endOfRow();
            }
            vt.setAlignment(2, TextTable::Alignment::RIGHT);
            std::cout << vt << std::endl;

            TextTable ft('-', '|', '+');
            ft.add("Name/Signature");
            ft.add("Return Type");
            ft.endOfRow();

            for(auto func : semantic_global_scope.function_list()) {
                ft.add(func.first);
                ft.add(func.second);
                ft.endOfRow();
            }
            std::cout << ft << std::endl;
        }

        // Clear Screen
        else if(input_line == "#clear"){
            std::cout << std::string(50, '\n');
        }

        // Parse as program
        else {

            // Add line to program
            program += input_line;

            // Count number of open scopes
            unsigned int open_scopes = 0;
            open_scopes += std::count(input_line.begin(), input_line.end(), '{');
            open_scopes -= std::count(input_line.begin(), input_line.end(), '}');

            while(open_scopes){
                std::cout << "... _\b";

                // Read next line
                input_line.clear();
                getline(std::cin, input_line);

                // Update scope count
                open_scopes += std::count(input_line.begin(), input_line.end(), '{');
                open_scopes -= std::count(input_line.begin(), input_line.end(), '}');

                // Add line to program
                program += input_line + "\n";
            }
        }

        try {

            // Tokenise and initialise parser
            lexer::Lexer lexer(program);
            parser::Parser parser(&lexer);
            parser::ASTProgramNode *prog;

            // Try to parse as program
            try {
                prog = parser.parse_program();
            }

            // Catch by trying to parse as expression
            catch(const std::exception &e) {

                try {
                    // If expression ends with ';', get rid of it
                    if (program.back() == ';')
                        program.pop_back();

                    // Parse again, create program node manually
                    lexer::Lexer expr_lexer(program);
                    parser = parser::Parser(&expr_lexer, 0);  // do not consume first token
                    prog = new parser::ASTProgramNode(
                            std::vector<parser::ASTNode *>({parser.parse_expression()}));

                    expr = true;
                } catch(const std::exception &expr_e) {

                    // Throw original error
                    throw std::runtime_error(e.what());
                }
            }

            // Generate XML
            /*
            visitor::XMLVisitor xml_generator;
            xml_generator.visit(prog);
            */

            // Try to analyse in a temporary copy of the global scope (just in case
            // the program is invalid)
            visitor::SemanticScope temp = semantic_global_scope;
            visitor::SemanticAnalyser temp_semantic_analyser(&temp);
            temp_semantic_analyser.visit(prog);

            // If this succeeds, perform semantic analysis modifying global scope
            visitor::SemanticAnalyser semantic_analyser(&semantic_global_scope);
            semantic_analyser.visit(prog);

            // Interpreter
            visitor::Interpreter interpreter(&interpreter_global_scope);
            interpreter.visit(prog);

            // If loading file, show user that everything went well
            if (file_load)
                std::cout << "File loaded successfully." << std::endl;

            // If expression, show user output
            else if(expr){
                auto current = interpreter.current_expr();
                switch(current.first){
                    case parser::INT:
                        std::cout << current.second.i;
                        break;
                    case parser::REAL:
                        std::cout << current.second.r;
                        break;
                    case parser::BOOL:
                        std::cout << ((current.second.b) ? "true" : "false");
                        break;
                    case parser::STRING:
                        std::cout << current.second.s;
                        break;
                }
            }
        }

        // Catch exception and print error
        catch(const std::exception &e) {
            std::cerr << e.what() << std::endl;
        }
    }

    return 0;
}
