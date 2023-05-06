//
// Created by lukec on 29/04/18.
//

#include "xml_visitor.h"

using namespace visitor;

XMLVisitor::XMLVisitor() : indentation_level(0) {
    xmlfile.open("program.xml");
};

std::string XMLVisitor::indentation() {

    std::string tabs;

    // Tab character for each indentation level
    for(unsigned int i = 0; i < indentation_level; i++)
        tabs += TAB;

    return tabs;
}

void XMLVisitor::visit(parser::ASTProgramNode *program) {

    // Add initial <program> tag
    xmlfile << indentation() << "<program>" << std::endl;

    // Indent
    indentation_level++;

    // For each statement, accept
    for(auto &statement : program -> statements)
        statement -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</program>" << std::endl;
}

void XMLVisitor::visit(parser::ASTDeclarationNode *decl) {

    // Add initial <decl> tag
    xmlfile << indentation() << "<decl>" << std::endl;

    // Indent
    indentation_level++;

    // Add identifier
    xmlfile << indentation() << "<id type = \"" + type_str(decl -> type) + "\">"
                             << decl -> identifier << "</id>" << std::endl;

    // Expression tags
    decl -> expr -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</decl>" << std::endl;
}

void XMLVisitor::visit(parser::ASTAssignmentNode *assign) {

    // Add initial <assign> tag
    xmlfile << indentation() << "<assign>" << std::endl;

    // Indent
    indentation_level++;

    // Add identifier
    xmlfile << indentation() << "<id>" << assign -> identifier << "</id>" << std::endl;

    // Expression tags
    assign -> expr -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</assign>" << std::endl;
}

void XMLVisitor::visit(parser::ASTPrintNode *print){

    // Add initial <print> tag
    xmlfile << indentation() << "<print>" << std::endl;

    // Indent
    indentation_level++;

    // Expression tags
    print -> expr -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</print>" << std::endl;
}

void XMLVisitor::visit(parser::ASTReturnNode *ret) {

    // Add initial <return> tag
    xmlfile << indentation() << "<return>" << std::endl;

    // Indent
    indentation_level++;

    // Expression tags
    ret -> expr -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</return>" << std::endl;
}

void XMLVisitor::visit(parser::ASTBlockNode *block) {

    // Add initial <block> tag
    xmlfile << indentation() << "<block>" << std::endl;

    // Indent
    indentation_level++;

    // For each statement, accept
    for(auto &statement : block -> statements)
        statement -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</block>" << std::endl;
}

void XMLVisitor::visit(parser::ASTIfNode *ifnode) {

    // Add initial <if> tag
    xmlfile << indentation() << "<if>" << std::endl;

    // Indent
    indentation_level++;

    // Add <condition> tag
    xmlfile << indentation() << "<condition>" << std::endl;

    // Indent
    indentation_level++;

    // Expression
    ifnode -> condition -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</condition>" << std::endl;

    // Add <if-block> tag
    xmlfile << indentation() << "<if-block>" << std::endl;

    // Indent
    indentation_level++;

    // If-block
    ifnode -> if_block -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</if-block>" << std::endl;

    // Unindent
    indentation_level--;

    // If there is an else-block
    if(ifnode->else_block){

        // Add <else-block> tag
        xmlfile << indentation() << "<else-block>" << std::endl;

        // Indent
        indentation_level++;

        // Else-block
        ifnode -> else_block -> accept(this);

        // Unindent
        indentation_level--;

        // Add closing tag
        xmlfile << indentation() << "</else-block>" << std::endl;
    }

    // Add closing tag
    xmlfile << indentation() << "</if>" << std::endl;
}

void XMLVisitor::visit(parser::ASTWhileNode *whilenode) {

    // Add initial <while> tag
    xmlfile << indentation() << "<while>" << std::endl;

    // Indent
    indentation_level++;

    // Add <condition> tag
    xmlfile << indentation() << "<condition>" << std::endl;

    // Indent
    indentation_level++;

    // Expression
    whilenode -> condition -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</condition>" << std::endl;

    // while-block
    whilenode -> block -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</while>" << std::endl;
}

void XMLVisitor::visit(parser::ASTFunctionDefinitionNode *func) {

    // Add initial <func-def> tag
    xmlfile << indentation() << "<func-def type = \"" + type_str(func->type) +
                                "\">" << std::endl;

    // Indent
    indentation_level++;

    // Function identifier
    xmlfile << indentation() << "<id>" + func->identifier + "</id>" << std::endl;

    // For each parameter
    for(auto &param : func -> parameters){
        xmlfile << indentation() << "<param type = \"" + type_str(param.second) +
                                    "\">" + param.first + "</param>" << std::endl;
    }

    // Function body
    func -> block -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</func-def>" << std::endl;

}

void XMLVisitor::visit(parser::ASTLiteralNode<int> *lit) {

    // Add initial <int> tag
    xmlfile << indentation() << "<int>";

    // Add value
    xmlfile << std::to_string(lit->val);

    // Add closing tag
    xmlfile << "</int>" << std::endl;
}

void XMLVisitor::visit(parser::ASTLiteralNode<float> *lit) {

    // Add initial <real> tag
    xmlfile << indentation() << "<real>";

    // Add value
    xmlfile << std::to_string(lit->val);

    // Add closing tag
    xmlfile << "</real>" << std::endl;
}

void XMLVisitor::visit(parser::ASTLiteralNode<bool> *lit) {

    // Add initial <bool> tag
    xmlfile << indentation() << "<bool>";

    // Add value
    xmlfile << ((lit->val) ? "true" : "false");

    // Add closing tag
    xmlfile << "</bool>" << std::endl;
}

void XMLVisitor::visit(parser::ASTLiteralNode<std::string> *lit) {

    // Add initial <string> tag
    xmlfile << indentation() << "<string>";

    // Add value
    xmlfile << lit->val;

    // Add closing tag
    xmlfile << "</string>" << std::endl;
}

void XMLVisitor::visit(parser::ASTBinaryExprNode *bin) {

    // Add initial <bin> tag
    xmlfile << indentation() << "<bin op = \"" + xml_safe_op(bin->op) +
                                "\">" << std::endl;

    // Indent
    indentation_level++;

    // Left node
    bin -> left -> accept(this);

    // Right node
    bin -> right -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</bin>" << std::endl;
}

void XMLVisitor::visit(parser::ASTIdentifierNode *id) {

    // Add initial <id> tag
    xmlfile << indentation() << "<id>";

    // Add value
    xmlfile << id -> identifier;

    // Add closing tag
    xmlfile << "</id>" << std::endl;

}

void XMLVisitor::visit(parser::ASTUnaryExprNode *un) {

    // Add initial <unary> tag
    xmlfile << indentation() << "<unary op = \"" + un -> unary_op + "\">"
                             << std::endl;

    // Indent
    indentation_level++;

    // Value
    un -> expr -> accept(this);

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</unary>" << std::endl;
}

void XMLVisitor::visit(parser::ASTFunctionCallNode *func) {

    // Add initial <func-call> tag
    xmlfile << indentation() << "<func-call>" << std::endl;

    // Indent
    indentation_level++;

    // Function identifier
    xmlfile << indentation() << "<id>" + func->identifier + "</id>" << std::endl;

    // For each parameter
    for(auto &param : func -> parameters){
        xmlfile << indentation() << "<arg>" << std::endl;

        // Indent
        indentation_level++;

        // Parameter
        param->accept(this);

        // Unindent
        indentation_level++;

        xmlfile << indentation() << "</arg>" << std::endl;
    }

    // Unindent
    indentation_level--;

    // Add closing tag
    xmlfile << indentation() << "</func-call>" << std::endl;
}

std::string XMLVisitor::type_str(parser::TYPE t) {

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
            throw std::runtime_error("Invalid type encountered in syntax tree when generating XML.");
    }
}

std::string XMLVisitor::xml_safe_op(std::string op) {

    if(op == "<")
        return "&lt;";
    if(op == ">")
        return "&gt;";
    if(op == "<=")
        return "&lt;=";
    if(op == ">=")
        return "&gt;=";
    return op;
}

XMLVisitor::~XMLVisitor(){
    xmlfile.close();
}