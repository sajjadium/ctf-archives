//
// Created by lukec on 22/04/18.
//

#include "ast.h"
#include <utility>
#include <iostream>

using namespace parser;

// Program Node
ASTProgramNode::ASTProgramNode(std::vector<ASTNode*> statements) :
        statements(std::move(statements))
{}


// Statement Nodes
ASTDeclarationNode::ASTDeclarationNode(TYPE type, std::string identifier, ASTExprNode *expr,
                                       unsigned int line_number) :
    type(type),
    identifier(std::move(identifier)),
    expr(expr),
    line_number(line_number)
{}

ASTAssignmentNode::ASTAssignmentNode(std::string identifier, ASTExprNode *expr, unsigned int line_number) :
        identifier(std::move(identifier)),
        expr(expr),
        line_number(line_number)
{}

ASTPrintNode::ASTPrintNode(ASTExprNode *expr, unsigned int line_number) :
        expr(expr),
        line_number(line_number)
{}

ASTReturnNode::ASTReturnNode(ASTExprNode *expr, unsigned int line_number) :
        expr(expr),
        line_number(line_number)
{}

ASTBlockNode::ASTBlockNode(std::vector<ASTStatementNode*> statements, unsigned int line_number) :
        statements(std::move(statements)),
        line_number(line_number)
{}

ASTIfNode::ASTIfNode(ASTExprNode* condition, ASTBlockNode *if_block, unsigned int line_number,
                     ASTBlockNode *else_block) :
        condition(condition),
        if_block(if_block),
        line_number(line_number),
        else_block(else_block)
{}

ASTWhileNode::ASTWhileNode(ASTExprNode *condition, ASTBlockNode *block, unsigned int line_number) :
        condition(condition),
        block(block),
        line_number(line_number)
{}

ASTFunctionDefinitionNode::ASTFunctionDefinitionNode(std::string identifier,
                                                     std::vector<std::pair<std::string, TYPE>> parameters,
                                                     TYPE type, ASTBlockNode* block, unsigned int line_number) :
        identifier(std::move(identifier)),
        parameters(std::move(parameters)),
        type(type),
        block(block),
        line_number(line_number)
{
    // Generate signature
    this->signature = std::vector<TYPE>();
    for(auto param : this->parameters) {
        variable_names.push_back(param.first);
        signature.push_back(param.second);
    }
}


// Expression Nodes
ASTBinaryExprNode::ASTBinaryExprNode(std::string op, ASTExprNode *left, ASTExprNode *right,
                                     unsigned int line_number) :
        op(std::move(op)),
        left(left),
        right(right),
        line_number(line_number),
        _optimized(false),
        _marked(false),
        _use_cnt(0),
        _code(NULL)
{}

ASTIdentifierNode::ASTIdentifierNode(std::string identifier, unsigned int line_number) :
        identifier(std::move(identifier)),
        line_number(line_number)
{}

ASTUnaryExprNode::ASTUnaryExprNode(std::string unary_op, ASTExprNode *expr, unsigned int line_number) :
    unary_op(std::move(unary_op)),
    expr(expr),
    line_number(line_number)
{}

ASTFunctionCallNode::ASTFunctionCallNode(std::string identifier, std::vector<ASTExprNode*> parameters,
                                         unsigned int line_number) :
    identifier(std::move(identifier)),
    parameters(std::move(parameters)),
    line_number(line_number)
{}


// Accept functions for visitors
void ASTBinaryExprNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

namespace parser {

    template<>
    void ASTLiteralNode<int>::accept(visitor::Visitor *v) {
        v->visit(this);
    }

    template<>
    void ASTLiteralNode<float>::accept(visitor::Visitor *v) {
        v->visit(this);
    }

    template<>
    void ASTLiteralNode<bool>::accept(visitor::Visitor *v) {
        v->visit(this);
    }

    template<>
    void ASTLiteralNode<std::string>::accept(visitor::Visitor *v) {
        v->visit(this);
    }
}

void ASTFunctionCallNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTIdentifierNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTUnaryExprNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTDeclarationNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTAssignmentNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTPrintNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTReturnNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTBlockNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTIfNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTWhileNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTFunctionDefinitionNode::accept(visitor::Visitor *v){
    v -> visit(this);
}

void ASTProgramNode::accept(visitor::Visitor *v){
    v -> visit(this);
}
