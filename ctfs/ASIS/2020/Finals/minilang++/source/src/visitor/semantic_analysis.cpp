//
// Created by lukec on 30/04/18.
//

#include "semantic_analysis.h"
#include <utility>
#include <iostream>

using namespace visitor;

bool SemanticScope::already_declared(std::string identifier) {
    return variable_symbol_table.find(identifier) != variable_symbol_table.end();
}

bool SemanticScope::already_declared(std::string identifier, std::vector<parser::TYPE> signature) {

    auto funcs = function_symbol_table.equal_range(identifier);

    // If key is not present in multimap
    if(std::distance(funcs.first, funcs.second) == 0)
        return false;

    // Check signature for each function in multimap
    for (auto i = funcs.first; i != funcs.second; i++)
        if(std::get<1>(i->second) == signature)
            return true;

    // Function with matching signature not found
    return false;
}

void SemanticScope::declare(std::string identifier, parser::TYPE type, unsigned int line_number) {
    variable_symbol_table[identifier] = std::make_pair(type, line_number);
}

void SemanticScope::declare(std::string identifier, parser::TYPE type, std::vector<parser::TYPE> signature,
                    unsigned int line_number) {

    function_symbol_table
            .insert(std::make_pair(identifier, std::make_tuple(type,
                                                               signature,
                                                               line_number)));
}

parser::TYPE SemanticScope::type(std::string identifier) {

    if(already_declared(identifier))
        return variable_symbol_table[identifier].first;

    throw std::runtime_error("Something went wrong when determining the type of '" + identifier + "'.");
}

parser::TYPE SemanticScope::type(std::string identifier, std::vector<parser::TYPE> signature) {

    auto funcs = function_symbol_table.equal_range(identifier);

    // If key is not present in multimap
    if(std::distance(funcs.first, funcs.second) == 0)
        throw std::runtime_error("Something went wrong when determining the type of '" + identifier + "'.");

    // Check signature for each
    for (auto i = funcs.first; i != funcs.second; i++)
        if(std::get<1>(i->second) == signature)
            return std::get<0>(i->second);

    // Function with matching signature not found
    throw std::runtime_error("Something went wrong when determining the type of '" + identifier + "'.");
}

unsigned int SemanticScope::declaration_line(std::string identifier) {

    if(already_declared(identifier))
        return variable_symbol_table[std::move(identifier)].second;

    throw std::runtime_error("Something went wrong when determining the line number of '" + identifier + "'.");
}

unsigned int SemanticScope::declaration_line(std::string identifier, std::vector<parser::TYPE> signature) {

    auto funcs = function_symbol_table.equal_range(identifier);

    // If key is not present in multimap
    if(std::distance(funcs.first, funcs.second) == 0)
        throw std::runtime_error("Something went wrong when determining the line number of '" + identifier + "'.");

    // Check signature for each
    for (auto i = funcs.first; i != funcs.second; i++)
        if(std::get<1>(i->second) == signature)
            return std::get<2>(i->second);

    // Function with matching signature not found
    throw std::runtime_error("Something went wrong when determining the line number of '" + identifier + "'.");
}


std::vector<std::pair<std::string, std::string>> SemanticScope::function_list() {

    std::vector<std::pair<std::string, std::string>> list;

    for(auto func = function_symbol_table.begin(), last = function_symbol_table.end();
        func != last; func = function_symbol_table.upper_bound(func -> first)){

        std::string func_name = func->first + "(";
        bool has_params = false;
        for(auto param : std::get<1>(func -> second)) {
            has_params = true;
            func_name += type_str(param) + ", ";
        }
        func_name.pop_back();   // remove last whitespace
        func_name.pop_back();   // remove last comma
        func_name += ")";

        list.emplace_back(std::make_pair(func_name, type_str(std::get<0>(func->second))));
    }

    return std::move(list);
}


SemanticAnalyser::SemanticAnalyser() {
    // Add global scope
    scopes.push_back(new SemanticScope());
};

SemanticAnalyser::SemanticAnalyser(SemanticScope* global_scope) {
    // Add global scope
    scopes.push_back(global_scope);
};

SemanticAnalyser::~SemanticAnalyser() = default;

void SemanticAnalyser::visit(parser::ASTProgramNode *prog) {

    // For each statement, accept
    for(auto &statement : prog -> statements)
        statement -> accept(this);
}

void SemanticAnalyser::visit(parser::ASTDeclarationNode *decl){

    // Current scope is the scope at the back
    SemanticScope *current_scope = scopes.back();

    // If variable already declared, throw error
    if(current_scope->already_declared(decl->identifier))
        throw std::runtime_error("Variable redeclaration on line " + std::to_string(decl->line_number) + ". '" +
                                  decl->identifier + "' was already declared in this scope on line " +
                                  std::to_string(current_scope->declaration_line(decl->identifier)) + ".");

    // Visit the expression to update current type
    decl -> expr -> accept(this);

    // allow mismatched type in the case of declaration of int to real
    if(decl -> type == parser::REAL && current_expression_type == parser::INT)
        current_scope->declare(decl->identifier, parser::REAL, decl->line_number);

    // types match
    else if (decl -> type == current_expression_type)
        current_scope->declare(decl->identifier, decl->type, decl->line_number);

    // types don't match
    else
        throw std::runtime_error("Found " + type_str(current_expression_type) + " on line " +
                                 std::to_string(decl->line_number) + " in definition of '" +
                                 decl -> identifier + "', expected " + type_str(decl->type) + ".");
}

void SemanticAnalyser::visit(parser::ASTAssignmentNode *assign) {

    // Determine the inner-most scope in which the value is declared
    unsigned long i;
    for (i = scopes.size() - 1; !scopes[i] -> already_declared(assign->identifier); i--)
        if(i <= 0)
            throw std::runtime_error("Identifier '" + assign->identifier + "' being reassigned on line " +
                                     std::to_string(assign->line_number) + " was never declared " +
                                     ((scopes.size() == 1) ? "globally." : "in this scope."));


    // Get the type of the originally declared variable
    parser::TYPE type = scopes[i]->type(assign->identifier);

    // Visit the expression to update current type
    assign->expr->accept(this);

    // allow mismatched type in the case of declaration of int to real
    if (type == parser::REAL && current_expression_type == parser::INT) {}

    // otherwise throw error
    else if (current_expression_type != type)
        throw std::runtime_error("Mismatched type for '" + assign->identifier + "' on line " +
                                 std::to_string(assign->line_number) + ". Expected " + type_str(type) +
                                 ", found " + type_str(current_expression_type) + ".");
}

void SemanticAnalyser::visit(parser::ASTPrintNode *print) {

    // Update current expression
    print -> expr -> accept(this);
}

void SemanticAnalyser::visit(parser::ASTReturnNode *ret) {

    // Update current expression
    ret -> expr -> accept(this);

    // If we are not global, check that we return current function return type
    if(!functions.empty() && current_expression_type != functions.top())
        throw std::runtime_error("Invalid return type on line " + std::to_string(ret->line_number) +
                                 ". Expected " + type_str(functions.top()) + ", found " +
                                 type_str(current_expression_type) + ".");
}

void SemanticAnalyser::visit(parser::ASTBlockNode *block) {

    // Create new scope
    scopes.push_back(new SemanticScope());

    // Check whether this is a function block by seeing if we have any current function
    // parameters. If we do, then add them to the current scope.
    for(auto param : current_function_parameters)
        scopes.back() -> declare(param.first, param.second, block->line_number);

    // Clear the global function parameters vector
    current_function_parameters.clear();

    // Visit each statement in the block
    for(auto &stmt : block -> statements)
        stmt -> accept(this);

    // Close scope
    scopes.pop_back();
}

void SemanticAnalyser::visit(parser::ASTIfNode *ifnode) {

    // Set current type to while expression
    ifnode -> condition -> accept(this);

    // Make sure it is boolean
    if(current_expression_type != parser::BOOL)
        throw std::runtime_error("Invalid if-condition on line " + std::to_string(ifnode -> line_number)
                                 + ", expected boolean expression.");

    // Check the if block
    ifnode -> if_block -> accept(this);

    // If there is an else block, check it too
    if(ifnode -> else_block)
        ifnode -> else_block -> accept(this);

}

void SemanticAnalyser::visit(parser::ASTWhileNode *whilenode) {

    // Set current type to while expression
    whilenode -> condition -> accept(this);

    // Make sure it is boolean
    if(current_expression_type != parser::BOOL)
        throw std::runtime_error("Invalid while-condition on line " + std::to_string(whilenode -> line_number)
                                 + ", expected boolean expression.");

    // Check the while block
    whilenode -> block -> accept(this);
}

void SemanticAnalyser::visit(parser::ASTFunctionDefinitionNode *func) {

    // First check that all enclosing scopes have not already defined the function
    for(auto &scope : scopes)
        if(scope->already_declared(func->identifier, func->signature)) {

            // Determine line number of error and the corresponding function signature
            int line = scope -> declaration_line(func -> identifier, func -> signature);
            std::string signature = "(";
            bool has_params = false;
            for(auto param : func -> signature) {
                has_params = true;
                signature += type_str(param) + ", ";
            }
            signature.pop_back();   // remove last whitespace
            signature.pop_back();   // remove last comma
            signature += ")";


            throw std::runtime_error("Error on line " + std::to_string(func->line_number) +
                                     ". Function " + func->identifier + signature +
                                     " already defined on line "+ std::to_string(line) + ".");
        }

    // Add function to symbol table
    scopes.back() -> declare(func->identifier, func->type, func->signature, func->line_number);

    // Push current function type onto function stack
    functions.push(func->type);

    // Empty and update current function parameters vector
    current_function_parameters.clear();
    current_function_parameters = func->parameters;

    // Check semantics of function block by visiting nodes
    func -> block -> accept(this);

    // Check that the function body returns
    if(!returns(func -> block))
        throw std::runtime_error("Function " + func->identifier + " defined on line " +
                                 std::to_string(func->line_number) + " is not guaranteed to "+
                                 "return a value.");

    // End the current function
    functions.pop();
}

void SemanticAnalyser::visit(parser::ASTLiteralNode<int>*) {
    current_expression_type = parser::INT;
}

void SemanticAnalyser::visit(parser::ASTLiteralNode<float>*) {
    current_expression_type = parser::REAL;
}

void SemanticAnalyser::visit(parser::ASTLiteralNode<bool>*) {
    current_expression_type = parser::BOOL;
}

void SemanticAnalyser::visit(parser::ASTLiteralNode<std::string>*) {
    current_expression_type = parser::STRING;
}

void SemanticAnalyser::visit(parser::ASTBinaryExprNode* bin) {

    // Operator
    std::string op = bin -> op;

    // Visit left node first
    bin -> left -> accept(this);
    parser::TYPE l_type = current_expression_type;

    // Then right node
    bin -> right -> accept(this);
    parser::TYPE r_type = current_expression_type;

    // These only work for int/real
    if(op == "*" || op == "/" || op == "-"){
        if((l_type != parser::INT && l_type != parser::REAL) ||
           (r_type != parser::INT && r_type != parser::REAL))
            throw std::runtime_error("Expected numerical operands for '" + op +
                                     "' operator on line " + std::to_string(bin->line_number) + ".");

        // If both int, then expression is int, otherwise real
        current_expression_type = (l_type == parser::INT && r_type == parser::INT) ?
                                  parser::INT : parser::REAL;
    }

    // + works for all types except bool
    else if(op == "+") {
        if(l_type == parser::BOOL || r_type == parser::BOOL)
            throw std::runtime_error("Invalid operand for '+' operator, expected numerical or string"
                                     " operand on line " + std::to_string(bin->line_number) + ".");

        // If both string, no error
        if(l_type == parser::STRING && r_type == parser::STRING)
            current_expression_type = parser::STRING;

        // only one is string, error
        else if(l_type == parser::STRING || r_type == parser::STRING)
            throw std::runtime_error("Mismatched operands for '+' operator, found " + type_str(l_type) +
                                     " on the left, but " + type_str(r_type) + " on the right (line " +
                                      std::to_string(bin->line_number) + ").");

        // real/int possibilities remain. If both int, then result is int, otherwise result is real
        else
            current_expression_type = (l_type == parser::INT && r_type == parser::INT) ?
                                      parser::INT : parser::REAL;
    }

    // and/or only work for bool
    else if(op == "and" || op == "or") {
        if (l_type == parser::BOOL && r_type == parser::BOOL)
            current_expression_type = parser::BOOL;
        else throw std::runtime_error("Expected two boolean-type operands for '" + op + "' operator " +
                                      "on line " + std::to_string(bin->line_number) + ".");
    }

    // rel-ops only work for numeric types
    else if(op == "<" || op == ">" || op == "<=" || op == ">=") {
        if ((l_type != parser::REAL && l_type != parser::INT) ||
            (r_type != parser::REAL && r_type != parser::INT))
            throw std::runtime_error("Expected two numerical operands for '" + op + "' operator " +
                                     "on line " + std::to_string(bin->line_number) + ".");
        current_expression_type = parser::BOOL;
    }

    // == and != only work for like types
    else if(op == "==" || op == "!=") {
        if (l_type != r_type && (l_type != parser::REAL || r_type != parser::INT) &&
            (l_type != parser::INT || r_type != parser::REAL))
            throw std::runtime_error("Expected arguments of the same type '" + op + "' operator " +
                                     "on line " + std::to_string(bin->line_number) + ".");
        current_expression_type = parser::BOOL;
    }

    else
        throw std::runtime_error("Unhandled semantic error in binary operator.");
}

void SemanticAnalyser::visit(parser::ASTIdentifierNode* id) {

    // Determine the inner-most scope in which the value is declared
    unsigned long i;
    for (i = scopes.size() - 1; !scopes[i] -> already_declared(id->identifier); i--)
        if(i <= 0)
            throw std::runtime_error("Identifier '" + id->identifier + "' appearing on line " +
                                     std::to_string(id->line_number) + " was never declared " +
                                     ((scopes.size() == 1) ? "globally." : "in this scope."));

    // Update current expression type
    current_expression_type = scopes[i]->type(id->identifier);
}

void SemanticAnalyser::visit(parser::ASTUnaryExprNode* un) {

    // Determine expression type
    un -> expr -> accept(this);

    // Handle different cases
    switch(current_expression_type){
        case parser::INT:
        case parser::REAL:
            if(un -> unary_op != "+" && un -> unary_op != "-")
                throw std::runtime_error("Operator '" + un -> unary_op + "' in front of numerical " +
                                         "expression on line " + std::to_string(un->line_number) + ".");
            break;
        case parser::BOOL:
            if(un -> unary_op != "not")
                throw std::runtime_error("Operator '" + un -> unary_op + "' in front of boolean " +
                                         "expression on line " + std::to_string(un->line_number) + ".");
            break;
        default:
            throw std::runtime_error("Incompatible unary operator '" + un -> unary_op + "' in front of " +
                                     "expression on line " + std::to_string(un->line_number) + ".");
    }
}

void SemanticAnalyser::visit(parser::ASTFunctionCallNode *func) {

    // Determine the signature of the function
    std::vector<parser::TYPE> signature;

    // For each parameter,
    for(auto param : func -> parameters) {

        // visit to update current expr type
        param -> accept(this);

        // add the type of current expr to signature
        signature.push_back(current_expression_type);
    }

    // Make sure the function exists in some scope i
    unsigned long i;
    for (i = scopes.size() - 1;
         !scopes[i] -> already_declared(func->identifier, signature);
         i--)
        if(i <= 0) {
            std::string func_name = func->identifier + "(";
            bool has_params = false;
            for(auto param : signature) {
                has_params = true;
                func_name += type_str(param) + ", ";
            }
            func_name.pop_back();   // remove last whitespace
            func_name.pop_back();   // remove last comma
            func_name += ")";
            throw std::runtime_error("Function '" + func_name + "' appearing on line " +
                                     std::to_string(func->line_number) + " was never declared " +
                                     ((scopes.size() == 1) ? "globally." : "in this scope."));
        }

    // Set current expression type to the return value of the function
    current_expression_type = scopes[i]->type(func->identifier, std::move(signature));
}


std::string type_str(parser::TYPE t) {

    switch(t){
        case parser::INT:
            return "int";
        case parser::REAL:
            return "real";
        case parser::BOOL:
            return "bool";
        case parser::STRING:
            return "string";
        default:
            throw std::runtime_error("Invalid type encountered.");
    }
}


// Determines whether a statement definitely returns or not
bool SemanticAnalyser::returns(parser::ASTStatementNode* stmt){

    // Base case: if the statement is a return statement, then it definitely returns
    if(dynamic_cast<parser::ASTReturnNode*>(stmt))
        return true;

    // For a block, if at least one statement returns, then the block returns
    if(auto block = dynamic_cast<parser::ASTBlockNode*>(stmt))
        for(auto &blk_stmt : block->statements)
            if(returns(blk_stmt))
                return true;

    // An if-(else) block returns only if both the if and the else statement return.
    if(auto ifstmt = dynamic_cast<parser::ASTIfNode*>(stmt))
        if(ifstmt -> else_block)
            return (returns(ifstmt->if_block) && returns(ifstmt->else_block));

    // A while block returns if its block returns
    if(auto whilestmt = dynamic_cast<parser::ASTWhileNode*>(stmt))
        return returns(whilestmt -> block);

    // Other statements do not return
    else return false;
}