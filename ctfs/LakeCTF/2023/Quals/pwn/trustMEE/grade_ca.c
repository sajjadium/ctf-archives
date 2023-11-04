/* Exploit for the vulnerable TA */

#include "tee_client_api.h"
#include "grade_ca.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const TEEC_UUID uuid = {
	0x11223344, 0xA710, 0x469E, { 0xAC, 0xC8, 0x5E, 0xDF, 0x8C, 0x85, 0x90, 0xE1 }
};

int main()
{
	TEEC_Context context;
	TEEC_Session session;
	TEEC_Operation operation;
	TEEC_SharedMemory in_mem;
	TEEC_SharedMemory out_mem;
	TEEC_Result tee_rv;
	int i;
	memset((void *)&in_mem, 0, sizeof(in_mem));
	memset((void *)&operation, 0, sizeof(operation));

	printf("Initializing context: ");
	tee_rv = TEEC_InitializeContext(NULL, &context);
	if (tee_rv != TEEC_SUCCESS) {
		printf("TEEC_InitializeContext failed: 0x%x\n", tee_rv);
		exit(0);
	} else {
		printf("initialized\n");
	}

	/*
	Connect to the TA
	*/
	printf("Openning session: ");
	tee_rv = TEEC_OpenSession(&context, &session, &uuid, TEEC_LOGIN_PUBLIC,
				  NULL, &operation, NULL);
	if (tee_rv != TEEC_SUCCESS) {
		printf("TEEC_OpenSession failed: 0x%x\n", tee_rv);
		exit(0);
	} else {
		printf("opened\n");
	}

	/*
	Setup memory for the input/output classes
	*/
	struct studentclass* StudentClassInst = (struct studentclass*)malloc(sizeof(struct studentclass)); 
	struct signedStudentclass* signedStudentClassInst = (struct signedStudentclass*)malloc(sizeof(struct signedStudentclass)); 
	memset(StudentClassInst, 0, sizeof(struct studentclass));
	memset(signedStudentClassInst, 0, sizeof(struct signedStudentclass));

	StudentClassInst->students[0].grade = 6;
	memset(StudentClassInst->students[0].firstname, 'A', NAME_LEN-1);
	memset(StudentClassInst->students[0].lastname, 'B', NAME_LEN-1);

	in_mem.buffer = (void*)StudentClassInst;
	in_mem.size = sizeof(struct studentclass);
	in_mem.flags = TEEC_MEM_INPUT;

	/*
	Register shared memory, allows us to read data from TEE or read data from it
	*/
	tee_rv = TEEC_RegisterSharedMemory(&context, &in_mem);
	if (tee_rv != TEE_SUCCESS) {
		printf("Failed to register studentclass shared memory\n");
		exit(0);
	}

	printf("registered shared memory for student class\n");

	out_mem.buffer = (void*)signedStudentClassInst;
	out_mem.size = sizeof(struct signedStudentclass);
	out_mem.flags = TEEC_MEM_OUTPUT;

	tee_rv = TEEC_RegisterSharedMemory(&context, &out_mem);
	if (tee_rv != TEE_SUCCESS) {
		printf("Failed to register signed studentclass memory\n");
		exit(0);
	}

	/*
	@TODO: Implement actual logic to sign student grades.
	*/
	
}
