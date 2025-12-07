#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define unreachable() do { printf("\nUnreachable code reached at code line [%d]\n", __LINE__); exit(EXIT_FAILURE); } while(0)

typedef char * variable_name_t;

typedef struct expression_t expression_t;

typedef struct {
    variable_name_t name;
} variable_t;

typedef struct {
    variable_name_t bound_name;
    expression_t *body;
} abstraction_t;

typedef struct {
    expression_t *function;
    expression_t *argument;
} application_t;

typedef enum {
    VAR, ABS, APP
} expression_type_t;

struct expression_t {
    expression_type_t type;
    union {
        variable_t var;
        abstraction_t abs;
        application_t app;
    } data;
};

void print_expression(expression_t *token) {
    switch (token->type) {
        case ABS:
            printf("(µ%s.", token->data.abs.bound_name);
            print_expression(token->data.abs.body);
            printf(")");
            break;
        case APP:
            printf("(");
            print_expression(token->data.app.function);
            printf(" ");
            print_expression(token->data.app.argument);
            printf(")");
            break;
        case VAR:
            printf("%s", token->data.var.name);
            break;
        default:
            printf("UNKNOWN_DATA[");
            for (size_t i = 0; i < sizeof(expression_t); i++) {
                printf("%c", ((unsigned char *)token)[i]);
            }
            printf("]");
    }
}

void free_expression(expression_t *expr);
void free_expression_body(expression_t *expr); // free only the body, not the expr itself

void free_expression(expression_t *expr) {
    free_expression_body(expr);
    free(expr);
}

// don't free strings; they are globally shared
// all expression pointers are uniquely owned
void free_expression_body(expression_t *expr) {
    if (expr->type == ABS) {
        free_expression(expr->data.abs.body);
        // do not free bound_name, as it is shared
    } else if (expr->type == APP) {
        free_expression(expr->data.app.function);
        free_expression(expr->data.app.argument);
    } else {
        // var, nothing to free
    }
}

/// makes a full copy of the expression tree while using the same original bound variable names
void dup_expression(expression_t *dest, expression_t *src) {
    switch (src->type) {
        case VAR:
            free_expression_body(dest);
            dest->type = src->type;
            dest->data.var.name = src->data.var.name; // shallow copy name
            break;
        case ABS:
            free_expression_body(dest); // free existing body if any
            dest->type = src->type;
            dest->data.abs.bound_name = src->data.abs.bound_name; // shallow copy name
            dest->data.abs.body = malloc(sizeof(expression_t));
            dup_expression(dest->data.abs.body, src->data.abs.body);
            break;
        case APP:
            free_expression_body(dest); // free existing body if any
            dest->type = src->type;
            dest->data.app.function = malloc(sizeof(expression_t));
            dup_expression(dest->data.app.function, src->data.app.function);
            dest->data.app.argument = malloc(sizeof(expression_t));
            dup_expression(dest->data.app.argument, src->data.app.argument);
            break;
        default:
            unreachable();
    }
}

// treats the dest as uninitialized, and consumes the src
void init_move_from_expression(expression_t *dest, expression_t *src) {
    switch (src->type) {
        case VAR:
            dest->type = src->type;
            dest->data.var.name = src->data.var.name; // shallow copy name
            break;
        case ABS:
            dest->type = src->type;
            dest->data.abs.bound_name = src->data.abs.bound_name; // shallow copy name
            dest->data.abs.body = src->data.abs.body;
            break;
        case APP:
            dest->type = src->type;
            dest->data.app.function = src->data.app.function;
            dest->data.app.argument = src->data.app.argument;
            break;
    }
}

void substitute(expression_t *expr, variable_name_t old_name, expression_t *replacement_expr) {
    if (expr->type == ABS) {
        substitute(expr->data.abs.body, old_name, replacement_expr);
    } else if (expr->type == APP) {
        substitute(expr->data.app.function, old_name, replacement_expr);
        substitute(expr->data.app.argument, old_name, replacement_expr);
    } else if (expr->type == VAR) {
        // base case: var substitution
        if (expr->data.var.name == old_name) {
            // assign it the variable
            dup_expression(expr, replacement_expr);
        }
    }
}

int simplify_normal_order(expression_t *expr) {
    // Simplification logic goes here
    // simplify lambda calculus normal order (leftmost)
    // returns 1 if there is more to simplify
    
    // normal order: apply outermost function immediately
    if (expr->type == APP) {
        if (expr->data.app.function->type == APP) {
            simplify_normal_order(expr->data.app.function); // must go down; this is not an immediately reducible lambda
            return 1; // there is more to reduce
        }
        // substitute the function application
        expr->data.app.function->type = ABS;
        substitute(expr->data.app.function->data.abs.body, expr->data.app.function->data.abs.bound_name, expr->data.app.argument);
        free_expression(expr->data.app.argument); // discard argument expression
        init_move_from_expression(expr, expr->data.app.function->data.abs.body); // move function body up
        return 1;
    } else if (expr->type == ABS) {
        return simplify_normal_order(expr->data.abs.body);
    } else if (expr->type == VAR) {
        return 0; // can't do any beta reduction here
    }

    unreachable();
}

struct parse_stack_t {
    variable_name_t *buf;
    size_t used;
    size_t capacity;
} parse_stack;

void initialize_parse_stack() {
    parse_stack.used = 0;
    parse_stack.capacity = 128;
    parse_stack.buf = calloc(parse_stack.capacity, sizeof(variable_name_t));
    if (!parse_stack.buf) {
        printf("Failed to allocate required data\n");
        printf("1\n");
        exit(EXIT_FAILURE);
    }
}

void free_parse_stack() {
    free(parse_stack.buf);
    parse_stack.buf = NULL;
    parse_stack.used = 0;
    parse_stack.capacity = 0;
}

void parse_stack_push(variable_name_t name) {
    // printf("Pushing variable: [%s]\n", name);
    if (parse_stack.used == parse_stack.capacity) {
        printf("Stack overflow\n");
        exit(EXIT_FAILURE);
    }
    parse_stack.buf[parse_stack.used++] = name;
}

variable_name_t parse_stack_pop() {
    // printf("Popping variable: [%s]\n", parse_stack.buf[parse_stack.used - 1]);
    if (parse_stack.used == 0) {
        printf("Parse stack underflow\n");
        exit(EXIT_FAILURE);
    }
    return parse_stack.buf[--parse_stack.used];
}

expression_t *parse_text(char **parse_location, char expected_terminator) {
    // Simple parser implementation of lambda calculus
    expression_t *expr = malloc(sizeof(expression_t));
    if (!expr) {
        printf("Failed to allocate required data\n");
        printf("3\n");
        exit(EXIT_FAILURE);
    }
    
    // parses the exact format used in print_expression
    // This is a very naive parser and only works for the specific format used in print_expression
    if (strncmp(*parse_location, "(µ", 2) == 0) { // abstraction
        expr->type = ABS; // parse abstraction(µParameter.Body)
        // find end of var name '.'
        *parse_location += strlen("(µ");
        char *terminator = memchr(*parse_location, '.', 64);
        if (!terminator) {
            printf("Variable name too long\n");
            exit(EXIT_FAILURE);
        }
        size_t var_name_len = terminator - *parse_location;
        expr->data.abs.bound_name = calloc(var_name_len + 1, sizeof(char));
        if (!expr->data.abs.bound_name) {
            printf("Failed to allocate required data\n");
            printf("4\n");
            exit(EXIT_FAILURE);
        }
        memcpy(expr->data.abs.bound_name, *parse_location, var_name_len);
        printf("Bound variable: [%s]\n", expr->data.abs.bound_name);
        *parse_location += var_name_len;
        (*parse_location)++; // skip past '.'
        parse_stack_push(expr->data.abs.bound_name);
        expr->data.abs.body = parse_text(parse_location, ')'); // parse until close paren
        char *removed = parse_stack_pop();
        printf("Unbound variable: [%s]\n", removed);
    } else if (strncmp(*parse_location, "(", 1) == 0) { // application
        expr->type = APP;
        (*parse_location)++;
        expr->data.app.function = parse_text(parse_location, ' '); // parse until space
        expr->data.app.argument = parse_text(parse_location, ')'); // parse until closeparen
    } else { // variable
        expr->type = VAR;
        // parse until our terminator
        char other_terminators[] = { ' ', ')', '\n', '\0' };
        char *terminator = memchr(*parse_location, expected_terminator, 64);
        for (size_t i = 0; i < sizeof(other_terminators); i++) {
            char *other_terminator = memchr(*parse_location, other_terminators[i], 64);
            if (other_terminator && (!terminator || other_terminator < terminator)) {
                terminator = other_terminator;
            }
        }
        if (!terminator) {
            printf("Variable name too long\n");
            exit(EXIT_FAILURE);
        }
        size_t var_name_len = terminator - *parse_location;
        // search thru var stack for match
        size_t i = parse_stack.used;
        int found = 0;
        while (i-- > 0) {
            if (strlen(parse_stack.buf[i]) == var_name_len && strncmp(parse_stack.buf[i], *parse_location, var_name_len) == 0) {
                expr->data.var.name = parse_stack.buf[i]; // they point to the same shared loc
                found = 1;
                break;
            }
        }
        if (!found) {
            printf("No bound variable name found: [%.*s]\n", (int)var_name_len, *parse_location);
            exit(EXIT_FAILURE);
        }
        *parse_location += var_name_len;
    }
    // next char must be our terminator
    if (**parse_location != expected_terminator) {
        printf("Unexpected character '%c', expected '%c'\n", **parse_location, expected_terminator);
        exit(EXIT_FAILURE);
    }
    (*parse_location)++;
    return expr;
}

char *flag = NULL;

void read_flag() {
    printf("Reading flag...\n");

    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        printf("Failed to open flag file\n");
        exit(EXIT_FAILURE);
    }
    flag = malloc(24);
    if (!flag) {
        printf("Failed to allocate required data\n");
        printf("5\n");
        exit(EXIT_FAILURE);
    }
    if (!fgets(flag, 24, f)) {
        printf("Failed to read flag\n");
        exit(EXIT_FAILURE);
    }
    fclose(f);
}

void free_flag() {
    printf("free(%p)\n", flag);
    free(flag);
    flag = NULL;
}

// char *EXAMPLE_TEXT = "((µx.x) (µx.((µy.y) x)))";
// char *EXAMPLE_TEXT = "(µh.((((µf.(µg.(µh.((f g) (h h))))) (µx.(µy.x))) h) (µx.(x x))))";

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("Welcome to the Idempotence Lambda Calculus Interpreter!\n");
    printf("Enter your lambda expression:\n");

    char *text = malloc(1024);
    if (fgets(text, 1024, stdin) == NULL) {
        printf("Failed to read input\n");
        exit(EXIT_FAILURE);
    }

    initialize_parse_stack();
    expression_t *parsed_lambda = parse_text(&text, '\n');
    free_parse_stack();
    print_expression(parsed_lambda);
    printf("\n");

    int continue_reducing;
    do {
        printf("======================\n");
        continue_reducing = simplify_normal_order(parsed_lambda);
        print_expression(parsed_lambda);
        printf("\n");
        while (1) {
            printf("Press r to read the flag, f to free the flag, n to rename a variable, or any other letter to continue:\n");

            char choice;
            char inputted;
            while ((choice = (inputted = getchar())) == '\n');
            do {
                inputted = getchar(); // flush rest of line
            } while (inputted != '\n' && inputted != EOF);

            if (choice == 'r') {
                read_flag();
                printf("Flag read into memory at %p\n", flag);
            } else if (choice == 'f') {
                free_flag();
                printf("Flag freed from memory\n");
            } else {
                break; // next cycle
            }
            printf("Continuing reduction!\n");
        }
    } while (continue_reducing);

    printf("Reached beta-normal form\n");

    return 0;
}
