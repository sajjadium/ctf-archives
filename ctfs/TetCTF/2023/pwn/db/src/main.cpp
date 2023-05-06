#include <cstdio>
#include <iostream>
#include <memory>
#include <sys/signal.h>
#include <unistd.h>
#include "db.h"
#include "utils.h"

#define TIMEOUT 30 // give player 30s to pwn

using namespace std;


void timeout(int sig)
{
	cout << "Time out" << endl;
	exit(1);
}

int main()
{
	char buffer[1024] = {0};
	uint32_t op;
	bool is_stopped = false;
	unique_ptr<DB> db = make_unique<DB>();

#ifdef RELEASE
	alarm(TIMEOUT);
	signal(SIGALRM, timeout);
#endif

	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	while(!is_stopped)
	{
		puts("====== Menu =======");
		puts("1. Register");
		puts("2. Create Secret");
		puts("3. Read Secret");
		puts("4. Deactive User");
		puts("5. List Users");
		puts("6. Exit");
		printf(">> ");

		op = read_uint32();
		switch(op){
			case 1:{
				printf("Your username: ");
				read_str(buffer, sizeof(buffer));
				shared_ptr<IOSymbol> user_name = zmake_shared(IOSymbol, buffer);

				if(db->has_user(user_name)){
					printf("User \"%s\" was exists\n", user_name->to_cstr());
					break;
				}

				printf("Password: ");
				read_str(buffer, sizeof(buffer));
				shared_ptr<IOString> user_pass = zmake_shared(IOString, buffer);

				if(!db->create_user(user_name, user_pass)){
					printf("Unable to register user \"%s\" to this database", user_name->to_cstr());
					break;
				}

				puts("Created.");
				break;
				}
			case 2:{
				printf("Your username: ");
				read_str(buffer, sizeof(buffer));
				shared_ptr<IOSymbol> user_name = zmake_shared(IOSymbol, buffer);

				if(!db->has_user(user_name)){
					printf("User \"%s\" doesn't exist\n", user_name->to_cstr());
					break;
				}

				printf("Password: ");
				read_str(buffer, sizeof(buffer));
				shared_ptr<IOString> user_pass = zmake_shared(IOString, buffer);

				if(!db->login(user_name, user_pass)){
					printf("Invalid username or password\n");
					break;
				}

				printf("Your new key size:");
				uint32_t key_size = read_uint32();

				if(key_size > 512)
					key_size = 512;

				printf("Key: ");
				read_buf(buffer, key_size);
				shared_ptr<IOBytes> secret_key = zmake_shared(IOBytes, buffer, key_size);

				printf("Your secret size:");
				uint32_t secret_size = read_uint32();
				if(secret_size > 1024)
					secret_size = 1024;

				printf("Secret: ");
				shared_ptr<IOBytes> io_buffer = zmake_shared(IOBytes);
				read_buf((char *)io_buffer->get_raw_ptr(), secret_size);
				io_buffer->fill_buffer(secret_size);

				shared_ptr<SecretBuffer> secret_buffer = zmake_shared(SecretBuffer);
				secret_buffer->attach_buffer(*io_buffer);
				secret_buffer->set_key(*secret_key);
				secret_buffer->encrypt();

				if(!db->create_secret_for(user_name, user_pass, secret_buffer)){
					printf("Unable to create secret for \"%s\"\n", user_name->to_cstr());
				}
				puts("Created");
				}
				break;
			case 3:{
				printf("Your username: ");
				read_str(buffer, sizeof(buffer));
				shared_ptr<IOSymbol> user_name = zmake_shared(IOSymbol, buffer);

				if(!db->has_user(user_name)){
					printf("User \"%s\" doesn't exist\n", user_name->to_cstr());
					break;
				}

				printf("Password: ");
				read_str(buffer, sizeof(buffer));
				shared_ptr<IOString> user_pass = zmake_shared(IOString, buffer);

				if(!db->login(user_name, user_pass)){
					printf("Invalid username or password\n");
					break;
				}

				printf("Key size:");
				uint32_t key_size = read_uint32();

				if(key_size > 512)
					key_size = 512;

				printf("Key: ");
				read_buf(buffer, key_size);
				shared_ptr<IOBytes> secret_key = zmake_shared(IOBytes, buffer, key_size);

				auto secret_value = db->read_secret_of(user_name, user_pass, secret_key);
				if(!secret_value.has_value()){
					printf("Unable to read secret of %s\n", user_name->to_cstr());
					break;
				}
				unique_ptr<IOBytes> raw_secret = move(secret_value.value());
				
				printf("Your secret:\n");
				write(STDOUT_FILENO, raw_secret->get_raw_ptr(), raw_secret->get_size());
				puts("Done.");
				}
				break;
			case 4: {
				printf("Your username: ");
				read_str(buffer, sizeof(buffer));
				shared_ptr<IOSymbol> user_name = zmake_shared(IOSymbol, buffer);

				if(!db->has_user(user_name)){
					printf("User \"%s\" doesn't exist\n", user_name->to_cstr());
					break;
				}

				printf("Password: ");
				read_str(buffer, sizeof(buffer));
				shared_ptr<IOString> user_pass = zmake_shared(IOString, buffer);

				if(!db->login(user_name, user_pass)){
					printf("Invalid username or password\n");
					break;
				}

				db->del_user(user_name);
				puts("Done");
				break;
				}
			case 5:{
				unique_ptr<IOList> users = db->get_all_users();

				printf("Users:\n");
				for(size_t i = 0; i < users->get_size(); i++){
					printf("%lu) %s\n", i + 1, dynamic_pointer_cast<IOSymbol>(users->get_at(i))->to_cstr());
				}
				break;
				}
			default:
				is_stopped = true;
				break;
		}
	}

	return 0;
}
