//
// Created by lukec on 22/04/18.
//

#include <iostream>
#include "parser.h"

using namespace parser;

Parser::Parser(lexer::Lexer* lex) : lex(lex) {
    current_token = lex->next_token();
    next_token    = lex->next_token();
}

Parser::Parser(lexer::Lexer* lex, unsigned int tokens) : lex(lex) {
    next_token = lex->next_token();
    for(unsigned int i = 0; i < tokens; i++)
        consume_token();
}

void Parser::consume_token() {
    current_token = next_token;
    next_token = lex->next_token();
}

ASTProgramNode* Parser::parse_program() {

    auto statements = new std::vector<ASTNode*>;

    while(current_token.type != lexer::TOK_EOF){
        statements->push_back(parse_statement());
        consume_token();
    }

    return new ASTProgramNode(*statements);
}

ASTStatementNode* Parser::parse_statement() {

    switch(current_token.type){

        case lexer::TOK_VAR:
            return parse_declaration_statement();

        case lexer::TOK_SET:
            return parse_assignment_statement();

        case lexer::TOK_PRINT:
            return parse_print_statement();

        case lexer::TOK_IF:
            return parse_if_statement();

        case lexer::TOK_WHILE:
            return parse_while_statement();

        case lexer::TOK_RETURN:
            return parse_return_statement();

        case lexer::TOK_DEF:
            return parse_function_definition();

        case lexer::TOK_LEFT_CURLY:
            return parse_block();

        default:
            throw std::runtime_error("Invalid statement starting with '" +
                                     current_token.value
                                     + "' encountered on line " +
                                     std::to_string(current_token.line_number) + ".");
    }
}

ASTDeclarationNode* Parser::parse_declaration_statement() {

    // Node attributes
    TYPE type;
    std::string identifier;
    ASTExprNode* expr;
    unsigned int line_number;

    // Determine line number
    line_number = current_token.line_number;

    // Consume identifier
    consume_token();
    if(current_token.type != lexer::TOK_IDENTIFIER)
        throw std::runtime_error("Expected variable name after 'var' on line "
                                 + std::to_string(current_token.line_number) + ".");
    identifier = current_token.value;

    consume_token();
    if(current_token.type != lexer::TOK_COLON)
        throw std::runtime_error("Expected ':' after " + identifier + " on line "
                                 + std::to_string(current_token.line_number) + ".");

    consume_token();
    type = parse_type(identifier);

    consume_token();
    if(current_token.type != lexer::TOK_EQUALS)
        throw std::runtime_error("Expected assignment operator '=' for " + identifier + " on line "
                                 + std::to_string(current_token.line_number) + ".");

    // Parse the right hand side
    expr = parse_expression();

    consume_token();
    if(current_token.type != lexer::TOK_SEMICOLON)
        throw std::runtime_error("Expected ';' after assignment of " + identifier + " on line "
                                 + std::to_string(current_token.line_number) + ".");

    // Create ASTExpressionNode to return
    return new ASTDeclarationNode(type, identifier, expr, line_number);
}

ASTAssignmentNode* Parser::parse_assignment_statement() {

    // Node attributes
    std::string identifier;
    ASTExprNode* expr;

    // Determine line number
    unsigned int line_number = current_token.line_number;

    consume_token();
    if(current_token.type != lexer::TOK_IDENTIFIER)
        throw std::runtime_error("Expected variable name after 'set' on line "
                                 + std::to_string(current_token.line_number) + ".");
    identifier = current_token.value;

    consume_token();
    if(current_token.type != lexer::TOK_EQUALS)
        throw std::runtime_error("Expected assignment operator '=' after " + identifier + " on line "
                                 + std::to_string(current_token.line_number) + ".");

    // Parse the right hand side
    expr = parse_expression();

    consume_token();
    if(current_token.type != lexer::TOK_SEMICOLON)
        throw std::runtime_error("Expected ';' after assignment of " + identifier + " on line "
                                 + std::to_string(current_token.line_number) + ".");

    return new ASTAssignmentNode(identifier, expr, line_number);
}

ASTPrintNode* Parser::parse_print_statement() {

    // Determine line number
    unsigned int line_number = current_token.line_number;

    // Get expression to print
    ASTExprNode* expr = parse_expression();

    // Consume ';' token
    consume_token();

    // Make sure it's a ';'
    if(current_token.type != lexer::TOK_SEMICOLON)
        throw std::runtime_error("Expected ';' after print statement on line "
                                 + std::to_string(current_token.line_number) + ".");

    // Return return node
    return new ASTPrintNode(expr, line_number);
}

ASTReturnNode* Parser::parse_return_statement() {

    // Determine line number
    unsigned int line_number = current_token.line_number;

    // Get expression to return
    ASTExprNode* expr = parse_expression();

    // Consume ';' token
    consume_token();

    // Make sure it's a ';'
    if(current_token.type != lexer::TOK_SEMICOLON)
        throw std::runtime_error("Expected ';' after return statement on line "
                                 + std::to_string(current_token.line_number) + ".");

    // Return return node
    return new ASTReturnNode(expr, line_number);
}

ASTBlockNode* Parser::parse_block() {

    auto statements = new std::vector<ASTStatementNode*>;

    // Determine line number
    unsigned int line_number = current_token.line_number;

    // Current token is '{', consume first token of statement
    consume_token();

    // While not reached end of block or end of file
    while(current_token.type != lexer::TOK_RIGHT_CURLY &&
          current_token.type != lexer::TOK_ERROR &&
          current_token.type != lexer::TOK_EOF){

        // Parse the statement
        statements->push_back(parse_statement());

        // Consume first token of next statement
        consume_token();
    }

    // If block ended by '}', return block
    if(current_token.type == lexer::TOK_RIGHT_CURLY)
        return new ASTBlockNode(*statements, line_number);

    // Otherwise the user left the block open
    else throw std::runtime_error("Reached end of file while parsing."
                                  " Mismatched scopes.");
}

ASTIfNode* Parser::parse_if_statement() {

    //Node attributes
    ASTExprNode* condition;
    ASTBlockNode* if_block;
    unsigned int line_number = current_token.line_number;

    // Consume '('
    consume_token();
    if(current_token.type != lexer::TOK_LEFT_BRACKET)
        throw std::runtime_error("Expected '(' after 'if' on line " +
                                 std::to_string(current_token.line_number) + ".");

    // Parse the expression
    condition = parse_expression();

    // Consume ')'
    consume_token();
    if(current_token.type != lexer::TOK_RIGHT_BRACKET)
        throw std::runtime_error("Expected ')' after if-condition on line " +
                                 std::to_string(current_token.line_number) + ".");

    // Consume '{'
    consume_token();
    if(current_token.type != lexer::TOK_LEFT_CURLY)
        throw std::runtime_error("Expected '{' after if-condition on line " +
                                 std::to_string(current_token.line_number) + ".");

    // Consume if-block and '}'
    if_block = parse_block();

    // Lookahead whether there is an else
    if(next_token.type != lexer::TOK_ELSE)
        return new ASTIfNode(condition, if_block, line_number);

    // Otherwise, consume the else
    consume_token();

    // Consume '{' after else
    consume_token();
    if(current_token.type != lexer::TOK_LEFT_CURLY)
        throw std::runtime_error("Expected '{' after else on line " +
                                 std::to_string(current_token.line_number) + ".");

    // Parse else-block and '}'
    ASTBlockNode* else_block = parse_block();

    // Return if node
    return new ASTIfNode(condition, if_block, line_number, else_block);
}

ASTWhileNode* Parser::parse_while_statement() {

    //Node attributes
    ASTExprNode* condition;
    ASTBlockNode* block;
    unsigned int line_number = current_token.line_number;

    // Consume '('
    consume_token();
    if(current_token.type != lexer::TOK_LEFT_BRACKET)
        throw std::runtime_error("Expected '(' after 'while' on line " +
                                 std::to_string(current_token.line_number) + ".");

    // Parse the expression
    condition = parse_expression();

    // Consume ')'
    consume_token();
    if(current_token.type != lexer::TOK_RIGHT_BRACKET)
        throw std::runtime_error("Expected ')' after while-condition on line " +
                                 std::to_string(current_token.line_number) + ".");

    // Consume '{'
    consume_token();
    if(current_token.type != lexer::TOK_LEFT_CURLY)
        throw std::runtime_error("Expected '{' after while-condition on line " +
                                 std::to_string(current_token.line_number) + ".");

    // Consume while-block and '}'
    block = parse_block();

    // Return while node
    return new ASTWhileNode(condition, block, line_number);
}

ASTFunctionDefinitionNode* Parser::parse_function_definition() {

    // Node attributes
    std::string identifier;
    std::vector<std::pair<std::string, TYPE>> parameters;
    TYPE type;
    ASTBlockNode* block;
    unsigned int line_number = current_token.line_number;

    // Consume identifier
    consume_token();

    // Make sure it is an identifier
    if(current_token.type != lexer::TOK_IDENTIFIER)
        throw std::runtime_error("Expected function identifier after keyword 'def' on line "
                                 + std::to_string(current_token.line_number) + ".");

    identifier = current_token.value;

    // Consume '('
    consume_token();
    if(current_token.type != lexer::TOK_LEFT_BRACKET)
        throw std::runtime_error("Expected '(' after '" + identifier + "' on line "
                                 + std::to_string(current_token.line_number) + ".");

    // Consume ')' or parameters
    consume_token();

    if(current_token.type != lexer::TOK_RIGHT_BRACKET){

        // Parse first parameter
        parameters.push_back(*parse_formal_param());

        // Consume ',' or ')'
        consume_token();

        while(current_token.type == lexer::TOK_COMMA){

            // Consume identifier
            consume_token();

            // Parse parameter
            parameters.push_back(*parse_formal_param());

            // Consume ',' or ')'
            consume_token();
        }

        // Exited while-loop, so token must be ')'
        if(current_token.type != lexer::TOK_RIGHT_BRACKET)
            throw std::runtime_error("Expected ')' or more parameters on line "
                                     + std::to_string(current_token.line_number) + ".");
    }

    // Consume ':'
    consume_token();

    if(current_token.type != lexer::TOK_COLON)
        throw std::runtime_error("Expected ':' after ')' on line "
                                 + std::to_string(current_token.line_number) + ".");


    // Consume type
    consume_token();
    type = parse_type(identifier);

    // Consume '{'
    consume_token();

    if(current_token.type != lexer::TOK_LEFT_CURLY)
        throw std::runtime_error("Expected '{' after function '" + identifier +
                                 "' definition on line "
                                 + std::to_string(current_token.line_number) + ".");

    // Parse block
    block = parse_block();

    // Return function definition node
    return new ASTFunctionDefinitionNode(identifier, parameters, type, block, line_number);

}

std::pair<std::string, TYPE>* Parser::parse_formal_param() {

    std::string identifier;
    TYPE type;

    // Make sure current token is identifier
    if(current_token.type != lexer::TOK_IDENTIFIER)
        throw std::runtime_error("Expected variable name in function definition on line "
                                 + std::to_string(current_token.line_number) + ".");
    identifier = current_token.value;

    // Consume ':'
    consume_token();

    if(current_token.type != lexer::TOK_COLON)
        throw std::runtime_error("Expected ':' after '" + identifier + "' on line "
                                 + std::to_string(current_token.line_number) + ".");

    // Consume type
    consume_token();
    type = parse_type(identifier);

    return new std::pair<std::string, TYPE>(identifier, type);

};

ASTExprNode* Parser::parse_expression() {
    ASTExprNode *simple_expr = parse_simple_expression();
    unsigned int line_number = current_token.line_number;

    if(next_token.type == lexer::TOK_RELATIONAL_OP) {
        consume_token();
        return new ASTBinaryExprNode(current_token.value, simple_expr, parse_expression(), line_number);
    }

    return simple_expr;
}

ASTExprNode* Parser::parse_simple_expression() {

    ASTExprNode *term = parse_term();
    unsigned int line_number = current_token.line_number;

    if(next_token.type == lexer::TOK_ADDITIVE_OP) {
        consume_token();
        return new ASTBinaryExprNode(current_token.value, term, parse_simple_expression(), line_number);
    }

    return term;
}

ASTExprNode* Parser::parse_term() {

    ASTExprNode *factor = parse_factor();
    unsigned int line_number = current_token.line_number;

    if(next_token.type == lexer::TOK_MULTIPLICATIVE_OP) {
        consume_token();
        return new ASTBinaryExprNode(current_token.value, factor, parse_term(), line_number);
    }

    return factor;
}

ASTExprNode* Parser::parse_factor() {

    consume_token();

    // Determine line number
    unsigned int line_number = current_token.line_number;

    switch(current_token.type){

        // Literal Cases
        case lexer::TOK_INT:
            return new ASTLiteralNode<int>(std::stoi(current_token.value), line_number);

        case lexer::TOK_REAL:
            return new ASTLiteralNode<float>(std::stof(current_token.value), line_number);

        case lexer::TOK_BOOL:
            return new ASTLiteralNode<bool>(current_token.value == "true", line_number);

        case lexer::TOK_STRING: {
            // Remove " character from front and end of lexeme
            std::string str = current_token.value.substr(1, current_token.value.size() - 2);

            // Replace \" with quote
            size_t pos = str.find("\\\"");
            while (pos != std::string::npos) {
                // Replace
                str.replace(pos, 2, "\"");
                // Get next occurrence from current position
                pos = str.find("\\\"", pos + 2);
            }

            // Replace \n with newline
            pos = str.find("\\n");
            while (pos != std::string::npos) {
                // Replace
                str.replace(pos, 2, "\n");
                // Get next occurrence from current position
                pos = str.find("\\n", pos + 2);
            }

            // Replace \t with tab
            pos = str.find("\\t");
            while (pos != std::string::npos) {
                // Replace
                str.replace(pos, 2, "\t");
                // Get next occurrence from current position
                pos = str.find("\\t", pos + 2);
            }

            // Replace \b with backslash
            pos = str.find("\\b");
            while (pos != std::string::npos) {
                // Replace
                str.replace(pos, 2, "\\");
                // Get next occurrence from current position
                pos = str.find("\\b", pos + 2);
            }

            return new ASTLiteralNode<std::string>(std::move(str), line_number);
        }

        // Identifier or function call case
        case lexer::TOK_IDENTIFIER:
            if(next_token.type == lexer::TOK_LEFT_BRACKET)
                return parse_function_call();
            else return new ASTIdentifierNode(current_token.value, line_number);

        // Subexpression case
        case lexer::TOK_LEFT_BRACKET: {
            ASTExprNode *sub_expr = parse_expression();
            consume_token();
            if (current_token.type != lexer::TOK_RIGHT_BRACKET)
                throw std::runtime_error("Expected ')' after expression on line "
                                         + std::to_string(current_token.line_number) + ".");
            return sub_expr;
        }

        // Unary expression case
        case lexer::TOK_ADDITIVE_OP:
        case lexer::TOK_NOT:
            return new ASTUnaryExprNode(current_token.value, parse_expression(), line_number);

        default:
            throw std::runtime_error("Expected expression on line "
                                     + std::to_string(current_token.line_number) + ".");

    }

}

ASTFunctionCallNode* Parser::parse_function_call() {
    // current token is the function identifier
    std::string identifier = current_token.value;
    auto *parameters = new std::vector<ASTExprNode*>;
    unsigned int line_number = current_token.line_number;

    consume_token();
    if(current_token.type != lexer::TOK_LEFT_BRACKET)
        throw std::runtime_error("Expected '(' on line "
                                 + std::to_string(current_token.line_number) + ".");

    // If next token is not right bracket, we have parameters
    if(next_token.type != lexer::TOK_RIGHT_BRACKET) {
        parameters = parse_actual_params();
    } else
        // Consume ')'
        consume_token();

    // Ensure right close bracket after fetching parameters
    if(current_token.type != lexer::TOK_RIGHT_BRACKET)
        throw std::runtime_error("Expected ')' on line "
                                 + std::to_string(current_token.line_number)
                                 + " after function parameters.");

    return new ASTFunctionCallNode(identifier, *parameters, line_number);
}

std::vector<ASTExprNode*>* Parser::parse_actual_params() {

    auto parameters = new std::vector<ASTExprNode*>;

    parameters->push_back(parse_expression());
    consume_token();

    // If there are more
    while(current_token.type == lexer::TOK_COMMA) {
        parameters->push_back(parse_expression());
        consume_token();
    }

    return parameters;
}

TYPE Parser::parse_type(std::string& identifier) {
    switch(current_token.type){
        case lexer::TOK_INT_TYPE:
            return INT;

        case lexer::TOK_REAL_TYPE:
            return REAL;

        case lexer::TOK_BOOL_TYPE:
            return BOOL;

        case lexer ::TOK_STRING_TYPE:
            return STRING;

        default:
            throw std::runtime_error("Expected type for " + identifier + " after ':' on line "
                                     + std::to_string(current_token.line_number) + ".");
    }
}



