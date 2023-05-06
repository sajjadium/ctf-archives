#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/mman.h>
#include <xpc/xpc.h>
#include <mach/mach.h>

// ------------------ imports ------------------
// These XPC functions are private for some reason... 
// But Linus helped us out ;)

// write mach ports into xpc dictionaries
extern void xpc_dictionary_set_mach_send(xpc_object_t dictionary,
                                        const char* name,
                                        mach_port_t port);

// get mach ports from xpc objects
extern mach_port_t xpc_mach_send_get_right(xpc_object_t value);

// ------------------ globals ------------------
// #define XPC_SERVICE_NAME    "com.alles.sandbox_share"

xpc_connection_t connection;
char *client_id = NULL;

// ------------------ code ------------------
int register_client(task_port_t task_port) {
	xpc_object_t message, reply;

    message = xpc_dictionary_create(NULL, NULL, 0);
    xpc_dictionary_set_uint64(message, "op", 1);
    xpc_dictionary_set_mach_send(message, "task", task_port);
    
    puts("Sending...");
    printf("%s\n%s\n", xpc_copy_description(connection), xpc_copy_description(message));

    reply = xpc_connection_send_message_with_reply_sync(connection, message);
    printf("reply: \n%s\n", xpc_copy_description(reply));

    if(xpc_dictionary_get_int64(reply, "status")) {
        char *error = xpc_dictionary_get_string(reply, "error");
        printf("[-] Error register_client: %s\n", error);
        return -1;
    }

    char *result = xpc_dictionary_get_string(reply, "client_id");
    
    client_id = calloc(1, 9);
    strncpy(client_id, result, 9);

    return 0;
}

uint64_t create_entry(xpc_object_t object, uint64_t token_index, char *UIDs) {
	xpc_object_t message, reply;

    message = xpc_dictionary_create(NULL, NULL, 0);
    xpc_dictionary_set_uint64(message, "op", 2);
    xpc_dictionary_set_string(message, "client_id", client_id);
    xpc_dictionary_set_value(message, "data", object);
    xpc_dictionary_set_string(message, "UIDs", UIDs);
    xpc_dictionary_set_uint64(message, "token_index", token_index);
    
    reply = xpc_connection_send_message_with_reply_sync(connection, message);
    // printf("create_entry reply: \n%s\n", xpc_copy_description(reply));

    if(xpc_dictionary_get_int64(reply, "status") != 0) {
        char *error = xpc_dictionary_get_string(reply, "error");
        printf("[-] Error create_entry: %s\n", error);
        return -1;
    }

    return xpc_dictionary_get_uint64(reply, "index");
}

xpc_object_t get_entry(uint64_t index) {
	xpc_object_t message, reply;

    message = xpc_dictionary_create(NULL, NULL, 0);
    xpc_dictionary_set_uint64(message, "op", 3);
    xpc_dictionary_set_string(message, "client_id", client_id);
    xpc_dictionary_set_uint64(message, "index", index);
    
    reply = xpc_connection_send_message_with_reply_sync(connection, message);
    // printf("get_entry reply: \n%s\n", xpc_copy_description(reply));

    if(xpc_dictionary_get_int64(reply, "status") != 0) {
        char *error = xpc_dictionary_get_string(reply, "error");
        printf("[-] Error get_entry: %s\n", error);
        return -1;
    }

    return xpc_dictionary_get_value(reply, "data");
}

int delete_entry(uint64_t index) {
	xpc_object_t message, reply;

    message = xpc_dictionary_create(NULL, NULL, 0);
    xpc_dictionary_set_uint64(message, "op", 4);
    xpc_dictionary_set_string(message, "client_id", client_id);
    xpc_dictionary_set_uint64(message, "index", index);

    reply = xpc_connection_send_message_with_reply_sync(connection, message);
    printf("delete_entry reply: %s\n", xpc_copy_description(reply));

    if(xpc_dictionary_get_int64(reply, "status") != 0) {
        char *error = xpc_dictionary_get_string(reply, "error");
        printf("[-] Error delete_entry: %s\n", error);
        return -1;
    }

    return 0;
}

uint64_t upload_data() {
    mach_msg_type_number_t info_out_cnt = TASK_EVENTS_INFO_COUNT;
    task_events_info_data_t task_events_info = {0};
    kern_return_t kr = -1;
    xpc_object_t data;

    kr = task_info(mach_task_self_, TASK_EVENTS_INFO, &task_events_info, &info_out_cnt);
    if(kr != KERN_SUCCESS) {
        printf("[-] Failed to get task info! \nError (%d): %s\n", kr, mach_error_string(kr));
        return -1;
    }
    data = xpc_data_create(&task_events_info, sizeof(task_events_info_data_t));
    
    return create_entry(data, 1, "0");
}


int main (int argc, const char * argv[]) {
    uint64_t index;

    if(argc < 2) {
        puts("Missing argument!");
        printf("usage: %s <service name>", argv[0]);
        exit(-1);
    }

    char *service_name = argv[1];
    printf("[i] Using service: %s\n", service_name);

	connection = xpc_connection_create_mach_service(service_name, NULL, 0);
	if (connection == NULL) {
		printf("[-] ERROR: cannot create connection\n");
		exit(1);
	}

	printf("[+] Connected to: %s\n", service_name);

	xpc_connection_set_event_handler(connection, ^(xpc_object_t response) {
        xpc_type_t t = xpc_get_type(response);
        if (t == XPC_TYPE_ERROR){
            printf("[-] ERROR: %s\n", xpc_dictionary_get_string(response, XPC_ERROR_KEY_DESCRIPTION));
            exit(-1);
        }
	});
	xpc_connection_resume(connection);
	puts("[+] Event handler registered!");

    client_id = calloc(1, 9);
    register_client(mach_task_self_);

    printf("[+] Got client_id: %s\n", client_id);

    while(1) {
        index = upload_data();

        printf("[+] Stats uploaded to index: %llu\n", index);
        sleep(120);

        if (index == -1) {
            puts("[-] Upload failed!");
            continue;
        }
        puts("[~] updating...");
        delete_entry(index);
    }

    free(client_id);
	xpc_release(connection);
	return 0;
}
