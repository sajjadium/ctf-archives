#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdio.h>

void shuffle(int *indices, int n) {
	int i;
	for (i = n - 1; i > 0; i--) {
		int j = rand() % (i + 1);
		int temp = indices[i];
		indices[i] = indices[j];
		indices[j] = temp;
	}
}

int main(int argc, char *argv[]) {
	int i;

	if (argc != 3) {
		fprintf(stderr, "Usage: %s <filename> <n>\n", argv[0]);
		return 1;
	}

	const char *filename = argv[1];
	const int n = atoi(argv[2]);

	if (n > 50) {
		fprintf(stderr, "Woah now! I'm not THAT good a shredder... :(\n");
		return 1;
	}

	FILE *file = fopen(filename, "rb");

	fseek(file, 0, SEEK_END);
	long filesize = ftell(file);
	fseek(file, 0, SEEK_SET);

	long chunk_size = (filesize + n - 1) / n;
	char **chunks = calloc(n, sizeof(char *));
	int *indices = calloc(n, sizeof(int));

	for (i = 0; i < n; i++) {
		chunks[i] = calloc(chunk_size, 1);
		indices[i] = i;
	}

	for (i = 0; i < n; i++) {
		fread(chunks[i], 1, chunk_size, file);
	}

	fclose(file);

	srand(time(NULL));
	shuffle(indices, n);

	int output_filename_length = strlen(filename) + strlen(".shredded");
	char *output_filename = calloc(output_filename_length + 1, sizeof(char));
	snprintf(output_filename, output_filename_length + 1, "%s.shredded", filename);
	FILE *outfile = fopen(output_filename, "wb");

	for (i = 0; i < n; i++) {
		fwrite(chunks[indices[i]], 1, chunk_size, outfile);
		free(chunks[indices[i]]);
	}

	free(chunks);
	free(indices);
	fclose(outfile);

	printf("Shredded file saved as %s\n", output_filename);
	free(output_filename);
	return 0;
}
