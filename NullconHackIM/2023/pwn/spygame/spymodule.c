#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <bits/time.h>
#include <stdbool.h>
#include <stdio.h>

static PyObject *spy_easy(PyObject *self, PyObject *args);
static PyObject *spy_hard(PyObject *self, PyObject *args);

static PyMethodDef spy_methods[] = {
	{ "easy", spy_easy, METH_VARARGS, "Play Spy Game (Easy)" },
	{ "hard", spy_hard, METH_VARARGS, "Play Spy Game (Hard)" },
	{ 0 }
};

static struct PyModuleDef spy_module = {
	PyModuleDef_HEAD_INIT,
	"spy",
	"Spy Game Module",
	-1,
	spy_methods,
};

PyObject *
spy_game(PyObject *self, PyObject *args, unsigned count)
{
	char user_input[256];
	uint8_t numbers[count];
	struct timespec start, end;
	uint64_t start_ns, end_ns;
	uint64_t total_ns, total_ok;
	size_t swap1, swap2;
	size_t swap1_in, swap2_in;
	size_t i, k;
	bool ok;

	if (!PyArg_ParseTuple(args, ""))
		return NULL;

	printf("Ready? ");
	getchar();
	printf("\n");

	total_ok = 0;
	total_ns = 0;
	for (i = 0; i < 8; i++) {
		for (k = 0; k < count; k++)
			numbers[k] = k;

		swap1 = rand() % count;
		swap2 = (swap1 + 1 + rand() % (count - 1)) % count;

		numbers[swap1] ^= numbers[swap2];
		numbers[swap2] ^= numbers[swap1];
		numbers[swap1] ^= numbers[swap2];

		printf("Before: ");
		for (k = 0; k < count; k++)
			printf("%u ", numbers[k]);
		printf("\n");

		clock_gettime(CLOCK_REALTIME, &start);
		start_ns = start.tv_nsec + start.tv_sec * 1e9;

		fflush(stdin);

		printf("Index 1: ");
		(void)fgets(user_input, sizeof(user_input), stdin);
		swap1_in = strtoull(user_input, NULL, 10);

		printf("Index 2: ");
		(void)fgets(user_input, sizeof(user_input), stdin);
		swap2_in = strtoull(user_input, NULL, 10);

		clock_gettime(CLOCK_REALTIME, &end);
		end_ns = end.tv_nsec + end.tv_sec * 1e9;

		numbers[swap1_in] ^= numbers[swap2_in];
		numbers[swap2_in] ^= numbers[swap1_in];
		numbers[swap1_in] ^= numbers[swap2_in];

		printf("After: ");
		for (k = 0; k < count; k++)
			printf("%u ", numbers[k]);
		printf("\n");

		ok = (swap1_in == swap1 && swap2_in == swap2)
			|| (swap1_in == swap2 && swap2_in == swap1);
		printf("You answered %s in %lu nanoseconds!\n",
			ok ? "correctly" : "incorrectly",
			end_ns - start_ns);
		printf("\n");

		total_ok += ok;
		total_ns += end_ns - start_ns;
	}

	if (count == 256 && total_ok == 5 && total_ns < 1000) {
		return PyUnicode_FromString("REWARD");
	} else if (count == 10 && total_ok == 5 && total_ns < 1e9 * 60) {
		return PyUnicode_FromString("MOTIVATE");
	}

	return PyUnicode_FromString("SLOW");
}

PyObject *
spy_easy(PyObject *self, PyObject *args)
{
	return spy_game(self, args, 10);
}

PyObject *
spy_hard(PyObject *self, PyObject *args)
{
	return spy_game(self, args, 256);
}

PyMODINIT_FUNC PyInit_spy(void) {
	setvbuf(stdout, NULL, _IONBF, 0);
	return PyModule_Create(&spy_module);
};
