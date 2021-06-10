//
// Created by lukec on 04/05/18.
//

#ifndef MINILANG_INTERPRETER_H
#define MINILANG_INTERPRETER_H

#include <map>
#include <stack>
#include "visitor.h"
#include "../parser/ast.h"

namespace visitor {

    typedef struct vT {
        vT() : i(0), r(0), b(0), s("") {};
        int i;
        float r;
        bool b;
        std::string s;
    } value_t;


    class InterpreterScope {
    public:

        bool already_declared(std::string);
        bool already_declared(std::string, std::vector<parser::TYPE>);
        void declare(std::string, int);
        void declare(std::string, float);
        void declare(std::string, bool);
        void declare(std::string, std::string);
        void declare(std::string, std::vector<parser::TYPE>, std::vector<std::string>,
                parser::ASTBlockNode*);

        parser::TYPE type_of(std::string);
        value_t value_of(std::string);
        std::vector<std::string> variable_names_of(std::string, std::vector<parser::TYPE>);
        parser::ASTBlockNode* block_of(std::string, std::vector<parser::TYPE>);

        std::vector<std::tuple<std::string, std::string, std::string>>  variable_list();

    private:
        std::map<std::string,
                 std::pair<parser::TYPE,
                           value_t>> variable_symbol_table;

        std::multimap<std::string,
                      std::tuple<std::vector<parser::TYPE>,
                                 std::vector<std::string>,
                                 parser::ASTBlockNode*>> function_symbol_table;
    };

    class Interpreter : public Visitor {
    public:

        Interpreter();
        Interpreter(InterpreterScope*);
        ~Interpreter();

        void visit(parser::ASTProgramNode*) override;
        void visit(parser::ASTDeclarationNode*) override;
        void visit(parser::ASTAssignmentNode*) override;
        void visit(parser::ASTPrintNode*) override;
        void visit(parser::ASTReturnNode*) override;
        void visit(parser::ASTBlockNode*) override;
        void visit(parser::ASTIfNode*) override;
        void visit(parser::ASTWhileNode*) override;
        void visit(parser::ASTFunctionDefinitionNode*) override;
        void visit(parser::ASTLiteralNode<int>*) override;
        void visit(parser::ASTLiteralNode<float>*) override;
        void visit(parser::ASTLiteralNode<bool>*) override;
        void visit(parser::ASTLiteralNode<std::string>*) override;
        void visit(parser::ASTBinaryExprNode*) override;
        void visit(parser::ASTIdentifierNode*) override;
        void visit(parser::ASTUnaryExprNode*) override;
        void visit(parser::ASTFunctionCallNode*) override;

        std::pair<parser::TYPE, value_t> current_expr();
        parser::TYPE current_expression_type;
        value_t current_expression_value;

    private:
        std::vector<InterpreterScope*> scopes;
        std::vector<std::string> current_function_parameters;
        std::vector<std::pair<parser::TYPE, value_t>> current_function_arguments;
    };

    std::string type_str(parser::TYPE);
}

#endif //MINILANG_INTERPRETER_H
