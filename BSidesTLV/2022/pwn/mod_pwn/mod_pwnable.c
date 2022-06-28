#include "httpd.h"
#include "http_config.h"
#include "http_protocol.h"
#include "ap_config.h"

#define ERR_NAME_TOO_LONG -1
#define MAX_NAME_SIZE 128 
const char flag[] = "BSidesTLV2022{TEST_FLAG_TEST_FLAG_TEST_FLAG_TEST_FLAG_TES}";
const char footer[] = "\n<hr /> can u pwn me?\n\n";

typedef struct _welcome_msg_obj {
    char name[MAX_NAME_SIZE];
    char *suffix;
    char color[32];
} welcome_msg_obj;

static void raise_error(int error_code, char *out, char *msg_fmt, ...) {
    va_list args;
    if(error_code == ERR_NAME_TOO_LONG) {
        va_start(args, msg_fmt);
        vsprintf(out, msg_fmt, args);
        va_end(args); 
    }
    else {
        sprintf(out, "Internal error: unknown reason");
    }
}

// Fetches the value of the `name` query parameter
static void fetch_name_param(request_rec *r, char *out) {
    char *name = &r->args[5]; // skipping the "?name=" prefix
    if(strlen(name) > sizeof(welcome_msg_obj)) {
        char *msg = apr_palloc(r->pool, MAX_NAME_SIZE); // CTF Note: The way `apr_palloc` works should NOT be a concern when trying to solve this challenge. Treat it as if it was a traditional `malloc` call.
        sprintf(msg, "Error, name too long: %.16s...", name);
        raise_error(ERR_NAME_TOO_LONG, out, msg); 
    } else {
        memcpy(out, name, strlen(name));
    }
    ap_unescape_urlencoded(out);
}


/* The Apache content handler */
static int pwnable_handler(request_rec *r)
{
    /* Init welcome object */
    welcome_msg_obj welcome_msg;
    memset(&welcome_msg, NULL, sizeof(welcome_msg));
    welcome_msg.suffix = &footer;
    strcpy(welcome_msg.color, "blue");

    /* Set the appropriate content type */
    ap_set_content_type(r, "text/html");
    
    /* Verify HTTP request method */
    if (strcmp(r->method, "GET") == OK) {
        ap_rputs("<h1>BSidesTLV 2022 Apache module!</h1> <br/>", r);
        if (r->args) {
            fetch_name_param(r, &welcome_msg.name);
            ap_rprintf(r, "Welcome, <font color='%s'>%s</font> \n<br />\n%s", welcome_msg.color, welcome_msg.name, welcome_msg.suffix);
        }
        else {
             ap_rprintf(r, "<form>\n");
             ap_rprintf(r, "Enter your name: <input type='text' name='name'> -> <input type='submit' />\n");
             ap_rprintf(r, "</form>\n");
        }
    }
    return OK;
}

static void pwnable_register_hooks(apr_pool_t *p)
{
    ap_hook_handler(pwnable_handler, NULL, NULL, APR_HOOK_MIDDLE);
}

/* Dispatch list for API hooks */
module AP_MODULE_DECLARE_DATA pwnable_module = {
    STANDARD20_MODULE_STUFF, 
    NULL,                  /* create per-dir    config structures */
    NULL,                  /* merge  per-dir    config structures */
    NULL,                  /* create per-server config structures */
    NULL,                  /* merge  per-server config structures */
    NULL,                  /* table of config file commands       */
    pwnable_register_hooks  /* register hooks                      */
};