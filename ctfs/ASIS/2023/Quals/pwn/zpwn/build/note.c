#include "note.mdh"

#define MAX_NOTES 0x100

uint32_t notes_cnt;
uint32_t sizes[MAX_NOTES+2];
char *bufs[MAX_NOTES+2];

static int
bin_note_add(char *nam, char **args, Options ops, UNUSED(int func))
{
	uint32_t note_sz = 0;
	char *note_buf = NULL;
	int r = 0;

	if(notes_cnt >= MAX_NOTES) return 0;

	puts("Note size: ");
	fflush(stdout);
	scanf("%u",&note_sz);
	if(note_sz > 0x300) return 0;
	note_buf = zalloc(note_sz+2);
	puts("Note content: ");
	fflush(stdout);
	r = read(0,note_buf,note_sz);
	if(r <= 0) exit(1);
	note_buf[r] = '\x00';

	bufs[notes_cnt] = note_buf;
	sizes[notes_cnt] = note_sz;
	notes_cnt += 1;

	printf("Saved in: %d",notes_cnt-1);
	fflush(stdout);

    return 0;
}

static int
bin_note_view(char *nam, char **args, Options ops, UNUSED(int func))
{
	uint32_t note_idx = 0;

	puts("Note idx: ");
	fflush(stdout);
	scanf("%u",&note_idx);
	if(note_idx >= notes_cnt) return 0;

	puts("Note content: ");
	puts(bufs[note_idx]);
    return 0;
}


static int
bin_note_edit(char *nam, char **args, Options ops, UNUSED(int func))
{
	uint32_t note_idx = 0;
	int r = 0;

	puts("Note idx: ");
	fflush(stdout);
	scanf("%u",&note_idx);
	if(note_idx >= notes_cnt) return 0;

	puts("Note content: ");
	fflush(stdout);
	r = read(0,bufs[note_idx],sizes[note_idx]);
	if(r <= 0) exit(1);
	bufs[note_idx][r] = '\x00';

    return 0;
}

static struct builtin bintab[] = {
    BUILTIN("note-add", 0, bin_note_add, 0, -1, 0, NULL, NULL),
    BUILTIN("note-view", 0, bin_note_view, 0, -1, 0, NULL, NULL),
    BUILTIN("note-edit", 0, bin_note_edit, 0, -1, 0, NULL, NULL),
};

static struct features module_features = {
    bintab, sizeof(bintab)/sizeof(*bintab),
    NULL, 0,
    NULL, 0,
    NULL, 0,
    0
};


/**/
int
setup_(UNUSED(Module m))
{
    return 0;
}

/**/
int
features_(Module m, char ***features)
{
    *features = featuresarray(m, &module_features);
    return 0;
}

/**/
int
enables_(Module m, int **enables)
{
    return handlefeatures(m, &module_features, enables);
}

/**/
int
boot_(UNUSED(Module m))
{
    return 0;
}


/**/
int
cleanup_(Module m)
{
    return setfeatureenables(m, &module_features, NULL);
}

/**/
int
finish_(UNUSED(Module m))
{
    return 0;
}
