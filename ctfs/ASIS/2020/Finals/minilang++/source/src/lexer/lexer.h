/**
 * @file lexer.h
 * Contains the implementation of the table-driven lexer.
 * @author Luke Collins
 * @date 5/3/2018
 */
#ifndef MINILANG_LEXER_H
#define MINILANG_LEXER_H


#include <string>
#include <vector>
#include "token.h"

/**
 * This namespace contains all the functions and attributes pertaining to the
 * functionality of the lexer.
 */
namespace lexer {

    /**
     * An enum containing tranistion types.
     * This enum encodes the equivalence classes of admissable transitions in
     * the automaton for the lexer, as described in table 1.1 in the report.
     */
    enum TRANSITION_TYPE {
        DIGIT           =  0,
        PERIOD          =  1,
        ADDITIVE_OP     =  2,
        ASTERISK        =  3,
        EXCL_MARK       =  4,
        ORDER_REL       =  5,
        EQUALS          =  6,
        UNDERSCORE      =  7,
        FORWARDSLASH    =  8,
        BACKSLASH       =  9,
        QUOTATION_MARK  = 10,
        PUNCTUATION     = 11,
        NEWLINE         = 12,
        ENDOFFILE       = 13,
        LETTER          = 14,
        PRINTABLE       = 15,
        OTHER           = 16
    };

    /**
     * Implementation of a table-driven lexer.
     * This class performs tokenisation of the program string by looking up the
     * appropriate DFA transitions in a transition table.
     */
    class Lexer {

        public:
            /**
             * Constructor for Lexer class with the input program string as a
             * parameter.
             * This constructor generates the tokens by successively executing
             * the function next_token(std::string&, unsigned int&), until
             * the end of the string is encountered. This process populates the
             * global vector #tokens.
             *
             * @param &program The memory address of the @c std::string containing the program
             * @see   Lexer::next_token(std::string&, unsigned int&)
             */
            Lexer(std::string&);

            /**
             * Returns the next token.
             * This function returns the object in the global vector #tokens at the
             * position specified by the global unsigned integer #current_token,
             * which is then incremented.
             *
             * @return The next token in the program string.
             */
            Token next_token();

            /**
             * Default destructor.
             */
            ~Lexer();


        private:

            /**
             * The error state.
             * This value represents the state S<SUB>e</SUB> in the DFA.
             */
            const unsigned int e = 23;

            /**
             * Encodes in location i whether or not the state S<SUB>i</SUB>
             * in the DFA is a final state.
             */                       /* S0  S1  S2  S3  S4  S5  S6  S7  S8  S9 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 Se */
            const bool is_final[24] = {   0,  1,  0,  1,  1,  1,  0,  1,  1,  1,  1,  1,  0,  0,  1,  0,  1,  0,  0,  0,  1,  1,  1, 0};

            /**
             * Encodes the transition function of the DFA.
             * The value of <tt>transitions[i][j]</tt> is the state to go to from
             * S<SUB>j</SUB> when receiving input i, that is, <tt>transitions[i][j]</tt>
             * \f$=\delta(j, i)\f$.
             * @see Lexer::transition_delta(int, char)
             */
            const unsigned int transitions[17][23] = {
                                     /* S0  S1  S2  S3  S4  S5  S6  S7  S8  S9 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 */
                /* DIGIT          */ {   1,  1,  3,  3,  e,  e,  e,  e,  e,  e, 10,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* PERIOD         */ {   2,  3,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* ADDITIVE_OP    */ {   4,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* ASTERISK       */ {   5,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 13, 12, 15,  e, 15,  e, 17, 17, 17,  e,  e,  e},
                /* EXCL_MARK      */ {   6,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* ORDER_REL      */ {   7,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* EQUALS         */ {   8,  e,  e,  e,  e,  e,  9,  9,  9,  e,  e,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* UNDERSCORE     */ {  10,  e,  e,  e,  e,  e,  e,  e,  e,  e, 10,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* FORWARDSLASH   */ {  11,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 12, 12, 13,  e, 16,  e, 17, 17, 17,  e,  e,  e},
                /* BACKSLASH      */ {   e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 12, 13,  e, 13,  e, 18, 18, 18,  e,  e,  e},
                /* QUOTATION_MARK */ {  17,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 12, 13,  e, 13,  e, 20, 19, 20,  e,  e,  e},
                /* PUNCTUATION    */ {  21,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* NEWLINE        */ {   e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 14, 13,  e, 13,  e,  e,  e,  e,  e,  e,  e},
                /* ENDOFFILE      */ {  22,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e},
                /* LETTER         */ {  10,  e,  e,  e,  e,  e,  e,  e,  e,  e, 10,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* PRINTABLE      */ {   e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e, 12, 13,  e, 13,  e, 17, 17, 17,  e,  e,  e},
                /* OTHER          */ {   e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e,  e}
            };

            /**
             * Stores the current token in the program string.
             * @see tokens
             * @see Lexer::next_token()
             */
            unsigned int current_token = 0;

            /**
             * Stores the individual Token objects generated by the constructor
             * Lexer().
             * @see current_token
             * @see next_token(std::string&, unsigned int&)
             */
            std::vector<Token> tokens;

            /**
             * Returns the state number to go to from state S<SUB>s</SUB> in the DFA
             * when encountering the character \f$\sigma\f$.
             * @param s The state number in the DFA
             * @param sigma The character encountered
             * @return int The value of \f$\delta(S_s, \sigma)\f$.
             */
            int transition_delta(int, char);

            /**
             * Returns the next token from a given position in the program string.
             * @param &program The memory address of the @c std::string containing the program
             * @param &current_index The memory address of an unsigned int referring to an index
             *                       in the program string
             * @return The next token from position @c current_index.
             */
            Token next_token(std::string&, unsigned int&);

            /**
             * Determines the line number of a position in the program string.
             * This function traverses the program string and increments a counter
             * whenever a newline character (<tt>\n</tt>) is encountered.
             * @return The line number of a given index in the program string.
             */
            unsigned int get_line_number(std::string&, unsigned int);
    };

};


#endif //MINILANG_LEXER_H
