#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/mman.h>

#include <xpc/xpc.h>
#include <mach/mach.h>
#include <dispatch/dispatch.h>
#include <Foundation/Foundation.h>
#include <CoreFoundation/CoreFoundation.h>

// ------------------ imports ------------------
// These XPC functions are private for some reason... 
// But Linus helped us out ;)

// write mach ports into xpc dictionaries
extern void xpc_dictionary_set_mach_send(xpc_object_t dictionary,
                                        const char* name,
                                        mach_port_t port);

// get mach ports from xpc objects
extern mach_port_t xpc_mach_send_get_right(xpc_object_t value);

// ------------------ types ------------------
typedef struct {
    uint32_t token_index;
    uint32_t owner;
    uint32_t *allowed_uids;
    xpc_object_t object;
} client_entry_t;

// ------------------ globals ------------------
#define MAX_UIDS        8
#define TABLE_SIZE      10000
#define LOG             1
#define DEBUG           1
// #define SERVICE_NAME    "com.alles.sandbox_share"

char *service_name = NULL;
FILE *output = NULL;
client_entry_t **entry_table = NULL;
xpc_object_t registered_clients = NULL;

// ------------------ mach stuff ------------------
kern_return_t _xpc_mach_port_retain_send(mach_port_name_t name){
  return mach_port_mod_refs(mach_task_self(), name, MACH_PORT_RIGHT_SEND, 1);
}

// ------------------ helpers ------------------
#define log(msg...)    fprintf(output, msg);fflush(output);
#define brk()           __asm__("brk");

// Parses up to max_size comma-seperated unsigned ints into
// an int array and pads with zeros
uint32_t *parse_uids(char *str, size_t max_size) {
    uint32_t *uids = (uint32_t *)calloc(max_size, sizeof(uint32_t));
    int i = 0;

    char *end = str;
    while(*end) {
        if (i == max_size) break;

        uint32_t n = strtoul(str, &end, 10);
        uids[i] = n;  i++;

        while (*end == ',') {
            end++;
        }
        str = end;
    }

    return uids;
}

// Apple's Endpoint Security framework allows processes to query 
// security-relevant information about clients through audit tokens.
// This token is essentially just an array of unsigned ints
// containing stuff from the kernels cred structure for the process
// e.g. EUID in audit_token->val[1], PID in audit_token->val[5], 
// pidversion in audit_token->val[7], ...
// 
// We can use this to filter clients and only allow specific, pids, uids or sandboxes
// to access entries.
int get_audit_token_value(xpc_object_t xpc_task, uint32_t token_index) {
    mach_msg_type_number_t task_info_out_cnt = 8;
    audit_token_t *audit_token;

    if(token_index >= TASK_AUDIT_TOKEN) {
        log("[-] Index out of bounds!");
        return -1;
    }

    audit_token = (audit_token_t *) calloc(1, sizeof(audit_token_t));
    task_port_t task = xpc_mach_send_get_right(xpc_task);
    if(task != MACH_PORT_NULL) {
        kern_return_t kr = task_info(task, TASK_AUDIT_TOKEN, audit_token, &task_info_out_cnt);
        if(kr != KERN_SUCCESS) {
            log("[-] Failed to get task info! \nError (%d): %s\n", kr, mach_error_string(kr));
            return -1;
        }

        return audit_token->val[token_index];
    }

    return -1;
}

int get_entry(char *client_id, uint64_t index, xpc_object_t *out_entry, uint64_t *owner) {
    // Index has already been bounds checked
    client_entry_t *entry = entry_table[index];
    if(entry == NULL) {
        return -1;
    }

    xpc_object_t xpc_task = xpc_dictionary_get_value(registered_clients, client_id);
    uint32_t our_value = get_audit_token_value(xpc_task, entry->token_index);
    
    int found = 0;
    for (int i = 0; i < MAX_UIDS; i++) {
        if (our_value == entry->allowed_uids[i]) {
            *out_entry = entry->object;
            *owner = entry->owner;
            return 0;
        }
    }

    return -2;
}

// ------------------ XPC code ------------------
void handle_message(xpc_connection_t conn, xpc_object_t message) {
    uint64_t status = -1;
    
    char *client_id = calloc(1, 10);
    char *desc = xpc_copy_description(message);
    log("[i] Handling message: %s\n", desc);
    free(desc);

    xpc_connection_t remote = xpc_dictionary_get_remote_connection(message);
    xpc_object_t reply = xpc_dictionary_create_reply(message);
    if(!reply) {
        log("[-] Message didn't come with reply context!\n");
        return;
    }

    uint64_t op = xpc_dictionary_get_uint64(message, "op");

    // Register new client
    if (op == 1) {
        xpc_object_t xpc_task = xpc_dictionary_get_value(message, "task");
        log("[i] Got client task port with name: 0x%x\n", xpc_mach_send_get_right(xpc_task));

        if(!registered_clients) {
            registered_clients = xpc_dictionary_create(NULL, NULL, 0);
        }

        // we generate a random client ID and save the task port 
        // for auth stuff later on
        int client_id_int = arc4random();
        snprintf(client_id, 9, "%x", client_id_int);
        xpc_dictionary_set_value(registered_clients, client_id, xpc_task);

        xpc_dictionary_set_string(reply, "client_id", client_id);
        status = 0;
        goto send_reply;
    }

    client_id = xpc_dictionary_get_string(message, "client_id");
    if(!client_id) {
        xpc_dictionary_set_string(reply, "error", "invalid client_id");
        goto send_reply;
    }

    // Eval commands
    switch (op) {

        // Create a new entry
        case 2: {
            client_entry_t *entry = calloc(1, sizeof(client_entry_t));

            char *uids = xpc_dictionary_get_string(message, "UIDs");
            xpc_object_t object = xpc_dictionary_get_value(message, "data");
            uint64_t token_index = xpc_dictionary_get_uint64(message, "token_index");

            xpc_object_t xpc_task = xpc_dictionary_get_value(registered_clients, client_id);
            uint32_t owner = get_audit_token_value(xpc_task, token_index);
            if (owner == 0xffffffff) {
                xpc_dictionary_set_string(reply, "error", "Couldn't get owner UID");
                goto send_reply;                
            }

            if(!uids || !object) {
                xpc_dictionary_set_string(reply, "error", "Didn't provide UIDs or data");
                goto send_reply;
            }

            uint64_t idx = 0;
            while (entry_table[idx] != 0) {
                idx += 1;

                if (idx >= TABLE_SIZE) {
                    xpc_dictionary_set_string(reply, "error", "No more space");
                    goto send_reply;                
                }
            }

            entry->owner = owner;
            entry->token_index = token_index;
            entry->allowed_uids = parse_uids(uids, MAX_UIDS);
            entry->object = object;
            xpc_retain(entry->object);

            entry_table[idx] = entry;
            xpc_dictionary_set_uint64(reply, "index", idx);

            status = 0;
            break;
        }

        // Query stored entry
        case 3: {
            uint64_t index = xpc_dictionary_get_uint64(message, "index");
            if (index >= TABLE_SIZE) {
                xpc_dictionary_set_string(reply, "error", "Provided index is out of bounds");
                goto send_reply;                
            }
            
            xpc_object_t data;
            uint64_t owner = 0;
            int kr = get_entry(client_id, index, &data, &owner);

            if (kr == 0) {
                xpc_dictionary_set_value(reply, "data", data);
                xpc_dictionary_set_uint64(reply, "owner", owner);

            } else if (kr == -1) {
                xpc_dictionary_set_string(reply, "error", "Entry empty");
                goto send_reply;              
            
            } else {
                xpc_dictionary_set_string(reply, "error", "Not authorized");
                goto send_reply;  
            }

            status = 0;
            break;
        }

        // Delete entry
        case 4: {
            uint64_t index = xpc_dictionary_get_uint64(message, "index");
            if (index >= TABLE_SIZE) {
                xpc_dictionary_set_string(reply, "error", "Provided index is out of bounds");
                goto send_reply;                
            }

            client_entry_t *entry = entry_table[index];
            if(entry == NULL) {
                xpc_dictionary_set_string(reply, "error", "Entry empty");
                goto send_reply;                
            }

            xpc_object_t xpc_task = xpc_dictionary_get_value(registered_clients, client_id);
            uint32_t our_value = get_audit_token_value(xpc_task, entry->token_index);

            if(our_value != entry->owner) {
                xpc_release(entry->object);
                xpc_dictionary_set_string(reply, "error", "Not owner");
                goto send_reply;
            }

            free(entry->allowed_uids);
            xpc_release(entry->object);
            free(entry);
            entry_table[index] = NULL;

            status = 0;
            break;
        }

        default:
            xpc_dictionary_set_string(reply, "error", "Unknown operation");

    }

send_reply:
	xpc_dictionary_set_int64(reply, "status", status);
	xpc_connection_send_message(remote, reply);
    xpc_release(reply);
}

void init_service(dispatch_queue_t queue) {
    xpc_connection_t conn;

    conn = xpc_connection_create_mach_service(service_name, queue, 1);
    if (!conn) {
        log("[-] Failed to create connection!\n");
        exit(1);
    }
    log("[+] Registered %s\n", service_name);

    entry_table = (client_entry_t **)calloc(TABLE_SIZE, sizeof(client_entry_t *));
    if (!entry_table) {
        log("[-] allocation failed\n");
        exit(1);
    }
    log("[+] Entry table at 0x%llx\n", entry_table);

	xpc_connection_set_event_handler(conn, ^(xpc_object_t client) {
		char *desc = xpc_copy_description(client);
		log("[i] Event: %s\n", desc);
		free(desc);

        xpc_type_t type = xpc_get_type(client);

        if (type == XPC_TYPE_CONNECTION) {
            log("[i] Got connection!\n")

            xpc_connection_set_event_handler(client, ^(xpc_object_t object) {
                xpc_type_t type = xpc_get_type(object);

                if (type == XPC_TYPE_DICTIONARY) {
                    handle_message(client, object);

                } else if (type == XPC_TYPE_ERROR) {
                    char *error = (char *)xpc_dictionary_get_string(object, XPC_ERROR_KEY_DESCRIPTION);
                    log("[-] Message error: %s\n", error);
                    xpc_connection_cancel(client);
                    return;

                } else {
                    log("[-] Got unknown event!\n");
                    xpc_connection_cancel(client);
                    return;
                }
            });
            xpc_connection_resume(client);

        } else if (type == XPC_TYPE_ERROR) {
            char *error = (char *)xpc_dictionary_get_string(client, XPC_ERROR_KEY_DESCRIPTION);
            log("[-] Connection error: %s\n", error);
            xpc_connection_cancel(conn);
            return;

        } else {
            log("[-] Got unknown event!\n");
            xpc_connection_cancel(conn);
            exit(1);
        }
    });
    xpc_connection_resume(conn);
}

int main(int argc, char *argv[]) {
	dispatch_queue_t queue;

    if(argc < 2) {
        puts("Missing argument!");
        printf("usage: %s <service name>\n", argv[0]);
        exit(-1);
    }

    service_name = argv[1];
    printf("[i] Using service: %s\n", service_name);

	output = fopen("/tmp/xa2nkf_daemon.log", "a+");
	if (!LOG || !output) {
		output = stderr;
	}

    queue = dispatch_queue_create("xpc daemon", 0);
    dispatch_set_target_queue(queue, dispatch_get_global_queue(QOS_CLASS_USER_INITIATED, 0));

    init_service(queue);

	dispatch_main();
	return 0;
}
