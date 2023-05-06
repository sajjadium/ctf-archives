/**
 * @file lexer.cpp
 * Implements the functions in lexer.h
 * @author Luke Collins
 * @date 5/3/2018
 */
#include <stack>
#include <stdexcept>
#include <iostream>
#include "lexer.h"

using namespace lexer;

Lexer::Lexer(std::string& program) {
    unsigned int current_index = 0;

    // Tokenise the program, ignoring comments
    Token t;
    while(current_index <= program.length()) {
        t = next_token(program, current_index);
        if(t.type != TOK_COMMENT)
            tokens.push_back(t);
    }
}

Token Lexer::next_token() {
    if(current_token < tokens.size())
        return tokens[current_token++];
    else{
        std::string error = "Final token surpassed.";
        return Token(TOK_ERROR, error);
    }
}

int Lexer::transition_delta(int s, char sigma) {

    /*
     * Check which transition type we have, and then refer to the
     * transition table.
     */
    switch(sigma){
        case '0':
        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
        case '6':
        case '7':
        case '8':
        case '9':
            return transitions[DIGIT][s];

        case '.':
            return transitions[PERIOD][s];

        case '+':
        case '-':
            return transitions[ADDITIVE_OP][s];

        case '*':
            return transitions[ASTERISK][s];

        case '!':
            return transitions[EXCL_MARK][s];

        case '>':
        case '<':
            return transitions[ORDER_REL][s];

        case '=':
            return transitions[EQUALS][s];

        case '_':
            return transitions[UNDERSCORE][s];

        case '/':
            return transitions[FORWARDSLASH][s];

        case '\\':
            return transitions[BACKSLASH][s];

        case '\"':
            return transitions[QUOTATION_MARK][s];

        case ':':
        case ';':
        case ',':
        case '(':
        case ')':
        case '{':
        case '}':
            return transitions[PUNCTUATION][s];

        case '\n':
            return transitions[NEWLINE][s];

        case EOF:
            return transitions[ENDOFFILE][s];

        default:
            auto ascii = (int) sigma;

            // If alpha is in [A-Z] or [a-z]
            if (((0x41 <= ascii) && (ascii <= 0x5A)) ||
                ((0x61 <= ascii) && (ascii <= 0x7A)))
                return transitions[LETTER][s];

            // If other
            return transitions[PRINTABLE][s];
    }


}

Token Lexer::next_token(std::string &program, unsigned int &current_index) {

    // Setup stack and lexeme
    int current_state = 0;
    std::stack<int> state_stack;
    char current_symbol;
    std::string lexeme;

    // Push 'BAD' state on the stack
    state_stack.push(-1);

    // Ignore whitespaces or newlines in front of lexeme
    while(current_index < program.length() &&
          (program[current_index] == ' ' || program[current_index] == '\n'))
        current_index++;

    // Check if EOF
    if(current_index == program.length()){
        lexeme = (char) EOF;
        current_index++;
        return Token(22, lexeme, get_line_number(program, current_index));
    }

    // While current state is not error state
    while(current_state != e){
        current_symbol = program[current_index];
        lexeme += current_symbol;

        // If current state is final, remove previously recorded final states
        if (is_final[current_state])
            while(!state_stack.empty())
                state_stack.pop();

        // and push current one on the stack
        state_stack.push(current_state);

        // Go to next state using delta function in DFA
        current_state = transition_delta(current_state, current_symbol);

        // Update current index for next iteration
        current_index++;
    }

    // Rollback loop
    while(!is_final[current_state] && current_state != -1){
        current_state = state_stack.top();
        state_stack.pop();
        lexeme.pop_back();
        current_index--;
    }

    if(current_state == -1)
        throw std::runtime_error("Lexical error.");


    if(is_final[current_state])
        return Token(current_state, std::move(lexeme), get_line_number(program, current_index));
    else throw std::runtime_error("Lexical error on line " + std::to_string(get_line_number(program, current_index)) + ".");
}

unsigned int Lexer::get_line_number(std::string &program, unsigned int index) {
    unsigned int line = 1;
    for(int i = 0; i < index; i++)
        if(program[i] == '\n')
            line++;
    return line;
}

Lexer::~Lexer() = default;
