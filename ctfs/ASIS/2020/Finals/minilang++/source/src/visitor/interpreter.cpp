//
// Created by lukec on 04/05/18.
//

#include <iostream>
#include "interpreter.h"
#include "../optimizer/optimizer.h"

using namespace visitor;

bool InterpreterScope::already_declared(std::string identifier) {
    return variable_symbol_table.find(identifier) != variable_symbol_table.end();
}

bool InterpreterScope::already_declared(std::string identifier, std::vector<parser::TYPE> signature) {

    auto funcs = function_symbol_table.equal_range(identifier);

    // If key is not present in multimap
    if(std::distance(funcs.first, funcs.second) == 0)
        return false;

    // Check signature for each function in multimap
    for (auto i = funcs.first; i != funcs.second; i++)
        if(std::get<0>(i->second) == signature)
            return true;

    // Function with matching signature not found
    return false;
}

void InterpreterScope::declare(std::string identifier, int int_value) {
    value_t value;
    value.i = int_value;
    variable_symbol_table[identifier] = std::make_pair(parser::INT, value);
}

void InterpreterScope::declare(std::string identifier, float real_value) {
    value_t value;
    value.r = real_value;
    variable_symbol_table[identifier] = std::make_pair(parser::REAL, value);
}

void InterpreterScope::declare(std::string identifier, bool bool_value) {
    value_t value;
    value.b = bool_value;
    variable_symbol_table[identifier] = std::make_pair(parser::BOOL, value);
}

void InterpreterScope::declare(std::string identifier, std::string string_value) {
    value_t value;
    value.s = string_value;
    variable_symbol_table[identifier] = std::make_pair(parser::STRING, value);
}

void InterpreterScope::declare(std::string identifier, std::vector<parser::TYPE> signature,
                               std::vector<std::string> variable_names, parser::ASTBlockNode* block) {

    function_symbol_table
            .insert(std::make_pair(identifier, std::make_tuple(signature,
                                                               variable_names,
                                                               block)));
}

parser::TYPE InterpreterScope::type_of(std::string identifier) {
    return variable_symbol_table[identifier].first;
}

value_t InterpreterScope::value_of(std::string identifier) {
    return variable_symbol_table[identifier].second;
}

std::vector<std::string> InterpreterScope::variable_names_of(std::string identifier,
                                                             std::vector<parser::TYPE> signature) {

    auto funcs = function_symbol_table.equal_range(identifier);

    // Match given signature to function in multimap
    for (auto i = funcs.first; i != funcs.second; i++)
        if(std::get<0>(i->second) == signature)
            return std::get<1>(i->second);

}

parser::ASTBlockNode* InterpreterScope::block_of(std::string identifier, std::vector<parser::TYPE> signature) {

    auto funcs = function_symbol_table.equal_range(identifier);

    // Match given signature to function in multimap
    for (auto i = funcs.first; i != funcs.second; i++)
        if(std::get<0>(i->second) == signature) {
            return std::get<2>(i->second);
        }

    return nullptr;
}

std::vector<std::tuple<std::string, std::string, std::string>> InterpreterScope::variable_list() {

    std::vector<std::tuple<std::string, std::string, std::string>> list;

    for(auto const &var : variable_symbol_table)
        switch(var.second.first){
            case parser::INT:
                list.emplace_back(std::make_tuple(
                        var.first, "int", std::to_string(var.second.second.i)));
                break;
            case parser::REAL:
                list.emplace_back(std::make_tuple(
                        var.first, "real", std::to_string(var.second.second.r)));
                break;
            case parser::BOOL:
                list.emplace_back(std::make_tuple(
                        var.first, "bool",  (var.second.second.b) ? "true" : "false"));
                break;
            case parser::STRING:
                list.emplace_back(std::make_tuple(
                        var.first, "string",  var.second.second.s));
                break;
        }

    return std::move(list);
}


Interpreter::Interpreter(){
    // Add global scope
    scopes.push_back(new InterpreterScope());
}

Interpreter::Interpreter(InterpreterScope* global_scope) {
    // Add global scope
    scopes.push_back(global_scope);
}

Interpreter::~Interpreter() = default;


void visitor::Interpreter::visit(parser::ASTProgramNode *prog) {

    // For each statement, accept
    for(auto &statement : prog -> statements)
        statement -> accept(this);
}

void visitor::Interpreter::visit(parser::ASTDeclarationNode *decl) {

    // Visit expression to update current value/type
    decl -> expr -> accept(this);

    // Declare variable, depending on type
    switch(decl -> type){
        case parser::INT:
            scopes.back()->declare(decl->identifier,
                                   current_expression_value.i);
            break;
        case parser::REAL:
            if(current_expression_type == parser::INT)
                scopes.back()->declare(decl->identifier,
                                       (float)current_expression_value.i);
            else
                scopes.back()->declare(decl->identifier,
                                        current_expression_value.r);
            break;
        case parser::BOOL:
            scopes.back()->declare(decl->identifier,
                                   current_expression_value.b);
            break;
        case parser::STRING:
            scopes.back()->declare(decl->identifier,
                                   current_expression_value.s);
            break;
    }
}

void visitor::Interpreter::visit(parser::ASTAssignmentNode *assign) {

    // Determine innermost scope in which variable is declared
    unsigned long i;
    for (i = scopes.size() - 1; !scopes[i] -> already_declared(assign->identifier); i--);

    // Visit expression node to update current value/type
    assign -> expr -> accept(this);

    // Redeclare variable, depending on type
    switch(scopes[i]->type_of(assign->identifier)){
        case parser::INT:
            scopes[i]->declare(assign->identifier,
                               current_expression_value.i);
            break;
        case parser::REAL:
            if(current_expression_type == parser::INT)
                scopes[i]->declare(assign->identifier,
                                   (float) current_expression_value.i);
            else
                scopes[i]->declare(assign->identifier,
                                   current_expression_value.r);
            break;
        case parser::BOOL:
            scopes[i]->declare(assign->identifier,
                               current_expression_value.b);
            break;
        case parser::STRING:
            scopes[i]->declare(assign->identifier,
                               current_expression_value.s);
            break;
    }
}

void visitor::Interpreter::visit(parser::ASTPrintNode *print){

    // Visit expression node to update current value/type
    print -> expr -> accept(this);

    // Print, depending on type
    switch(current_expression_type){
        case parser::INT:
            std::cout << current_expression_value.i;
            break;
        case parser::REAL:
            std::cout << current_expression_value.r;
            break;
        case parser::BOOL:
            std::cout << ((current_expression_value.b) ? "true" : "false");
            break;
        case parser::STRING:
            std::cout << current_expression_value.s;
            break;
    }
}

void visitor::Interpreter::visit(parser::ASTReturnNode *ret) {
    // Update current expression
    ret -> expr -> accept(this);
}

void visitor::Interpreter::visit(parser::ASTBlockNode *block) {

    // Create new scope
    scopes.push_back(new InterpreterScope());

    // Check whether this is a function block by seeing if we have any current function
    // parameters. If we do, then add them to the current scope.
    for(unsigned int i = 0; i < current_function_arguments.size(); i++){
        switch(current_function_arguments[i].first){
            case parser::INT:
                scopes.back() -> declare(current_function_parameters[i],
                                         current_function_arguments[i].second.i);
                break;
            case parser::REAL:
                scopes.back() -> declare(current_function_parameters[i],
                                         current_function_arguments[i].second.r);
                break;
            case parser::BOOL:
                scopes.back() -> declare(current_function_parameters[i],
                                         current_function_arguments[i].second.b);
                break;
            case parser::STRING:
                scopes.back() -> declare(current_function_parameters[i],
                                         current_function_arguments[i].second.s);
                break;
        }
    }

    // Clear the global function parameter/argument vectors
    current_function_parameters.clear();
    current_function_arguments.clear();

    // Visit each statement in the block
    for(auto &stmt : block -> statements)
        stmt -> accept(this);

    // Close scope
    scopes.pop_back();
}

void visitor::Interpreter::visit(parser::ASTIfNode *ifNode) {

    // Evaluate if condition
    ifNode -> condition -> accept(this);

    // Execute appropriate blocks
    if(current_expression_value.b)
        ifNode -> if_block -> accept(this);
    else{
        if(ifNode -> else_block)
            ifNode -> else_block -> accept(this);
    }

}

void visitor::Interpreter::visit(parser::ASTWhileNode *whileNode) {

    // Evaluate while condition
    whileNode -> condition -> accept(this);

    while(current_expression_value.b){
        // Execute block
        whileNode -> block -> accept(this);

        // Re-evaluate while condition
        whileNode -> condition -> accept(this);
    }
}

void visitor::Interpreter::visit(parser::ASTFunctionDefinitionNode *func) {

    // Add function to symbol table
    scopes.back() -> declare(func->identifier, func->signature,
                             func->variable_names, func->block);


}

void visitor::Interpreter::visit(parser::ASTLiteralNode<int> *lit) {
    value_t v;
    v.i = lit->val;
    current_expression_type = parser::INT;
    current_expression_value = std::move(v);
}

void visitor::Interpreter::visit(parser::ASTLiteralNode<float> *lit) {
    value_t v;
    v.r = lit->val;
    current_expression_type = parser::REAL;
    current_expression_value = std::move(v);
}

void visitor::Interpreter::visit(parser::ASTLiteralNode<bool> *lit) {
    value_t v;
    v.b = lit->val;
    current_expression_type = parser::BOOL;
    current_expression_value = std::move(v);
}

void visitor::Interpreter::visit(parser::ASTLiteralNode<std::string> *lit) {
    value_t v;
    v.s = lit->val;
    current_expression_type = parser::STRING;
    current_expression_value = std::move(v);
}

void visitor::Interpreter::visit(parser::ASTBinaryExprNode *bin) {
    // Operator
    std::string op = bin -> op;

    // Visit left node first
    bin -> left -> accept(this);
    parser::TYPE l_type = current_expression_type;
    value_t l_value = current_expression_value;

    // Then right node
    bin -> right -> accept(this);
    parser::TYPE r_type = current_expression_type;
    value_t r_value = current_expression_value;

    if (bin -> is_optimized()) {
        // Call optimized function
        bin -> call(l_value, r_value);
        return;
    } else {
        bin -> use();
        if (bin -> is_marked())
            optimizer::Optimize(this, bin, l_type, r_type);
    }

    // Expression struct
    value_t v;

    // Arithmetic operators for now
    if(op == "+" || op == "-" || op == "*" || op == "/") {
        // Two ints
        if(l_type == parser::INT && r_type == parser::INT){
            current_expression_type = parser::INT;
            if(op == "+")
                v.i = l_value.i + r_value.i;
            else if(op == "-")
                v.i = l_value.i - r_value.i;
            else if(op == "*")
                v.i = l_value.i * r_value.i;
            else if(op == "/") {
                if(r_value.i == 0)
                    throw std::runtime_error("Division by zero encountered on line "
                                             + std::to_string(bin->line_number) + ".");
                v.i = l_value.i / r_value.i;
            }
        }
        // At least one real
        else if(l_type == parser::REAL || r_type == parser::REAL) {
            current_expression_type = parser::REAL;
            float l = l_value.r, r = r_value.r;
            if(l_type == parser::INT)
                l = l_value.i;
            if(r_type == parser::INT)
                r = r_value.i;
            if(op == "+")
                v.r = l+r;
            else if(op == "-")
                v.r = l-r;
            else if(op == "*")
                v.r = l*r;
            else if(op == "/") {
                if(r == 0)
                    throw std::runtime_error("Division by zero encountered on line "
                                             + std::to_string(bin->line_number) + ".");
                v.r = l / r;
            }
        }
        // Remaining case is for strings
        else {
            current_expression_type = parser::STRING;
            v.s = l_value.s + r_value.s;
        }
    }
    // Now bool
    else if(op == "and" || op == "or"){
        current_expression_type = parser::BOOL;
        if(op == "and")
            v.b = l_value.b && r_value.b;
        else if(op == "or")
            v.b = l_value.b || r_value.b;
    }

    // Now Comparator Operators
    else {
        current_expression_type = parser::BOOL;
        if(l_type == parser::BOOL)
                v.b = (op == "==") ? l_value.b == r_value.b : l_value.b != r_value.b;

        else if (l_type == parser::STRING)
                v.b = (op == "==") ? l_value.s == r_value.s : l_value.s != r_value.s;

        else{
            float l = l_value.r, r = r_value.r;
            if(l_type == parser::INT)
                l = l_value.i;
            if(r_type == parser::INT)
                r = r_value.i;
            if(op == "==")
                v.b = l == r;
            else if(op == "!=")
                v.b = l != r;
            else if(op == "<")
                v.b = l < r;
            else if(op == ">")
                v.b = l > r;
            else if(op == ">=")
                v.b = l >= r;
            else if(op == "<=")
                v.b = l <= r;
        }
    }


    // Update current expression
    current_expression_value = v;

}

void visitor::Interpreter::visit(parser::ASTIdentifierNode *id) {

    // Determine innermost scope in which variable is declared
    unsigned long i;
    for (i = scopes.size() - 1; !scopes[i] -> already_declared(id->identifier); i--);

    // Update current expression
    current_expression_type = scopes[i] -> type_of(id->identifier);
    current_expression_value = scopes[i] -> value_of(id->identifier);

}

void visitor::Interpreter::visit(parser::ASTUnaryExprNode *un) {

    // Update current expression
    un -> expr -> accept(this);

    switch(current_expression_type){
        case parser::INT:
            if(un->unary_op == "-")
            current_expression_value.i *= -1;
            break;
        case parser::REAL:
            if(un->unary_op == "-")
                current_expression_value.r *= -1;
            break;
        case parser::BOOL:
            current_expression_value.b ^= 1;
    }
}

void visitor::Interpreter::visit(parser::ASTFunctionCallNode *func) {

    // Determine the signature of the function
    std::vector<parser::TYPE> signature;
    std::vector<std::pair<parser::TYPE, value_t>> current_function_arguments;

    // For each parameter,
    for (auto param : func -> parameters) {

        // visit to update current expr type
        param->accept(this);

        // add the type of current expr to signature
        signature.push_back(current_expression_type);

        // add the current expr to the local vector of function arguments, to be
        // used in the creation of the function scope
        current_function_arguments.emplace_back(current_expression_type, current_expression_value);
    }

    // Update the global vector current_function_arguments
    for(auto arg : current_function_arguments)
        this -> current_function_arguments.push_back(arg);

    // Determine in which scope the function is declared
    unsigned long i;
    for (i = scopes.size() - 1;
         !scopes[i]->already_declared(func->identifier, signature);
         i--);

    // Populate the global vector of function parameter names, to be used in creation of
    // function scope
    current_function_parameters = scopes[i] -> variable_names_of(func->identifier, signature);

    // Visit the corresponding function block
    scopes[i] -> block_of(func->identifier, signature) -> accept(this);
}


std::pair<parser::TYPE, value_t> Interpreter::current_expr(){
    return std::move(std::make_pair(current_expression_type,
                                    current_expression_value));
};


std::string visitor::type_str(parser::TYPE t) {

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

