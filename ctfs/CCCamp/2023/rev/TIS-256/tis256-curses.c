#include <bits/time.h>
#include <sys/select.h>
#define NCURSES_WIDECHAR 1

#include "tpu.h"
#include "util.h"
#include "asm.h"

#include <ncurses.h>
#include <sys/inotify.h>
#include <time.h>
#include <unistd.h>
#include <locale.h>
#include <errno.h>
#include <stdarg.h>
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#define KEY_ESC 0x1b
#define KEY_CTRL(c) ((c) & ~0x60)

#define TPU_INPUT_ROWS 14
#define TPU_INPUT_COLS 21
#define TPU_INFO_W 7
#define TPU_INFO_H 4
#define TPU_W (1 + TPU_INPUT_COLS + TPU_INFO_W)
#define TPU_H (1 + TPU_INPUT_ROWS + 1)

enum input_mode {
	MAIN,
	TPU_NAV
};

enum {
	NONE, MIN, MAX, MID
};

enum {
	COLOR_WARN = 1
};

static const char *mode_repr[] = {
	"IDL", "RUN", "REA", "WRI"
};

static int scrx = 0;
static int scry = 0;
static int scrw = 80;
static int scrh = 40;

static struct tis tis;

static struct timespec show_reloaded = { 0 };
static bool showing_reloaded = false;

static enum input_mode input_mode = MAIN;

static struct tpu *tpu_sel = NULL;

int (*cleanup)(void) = endwin;
const char *progname = "tis256-curses";

static int64_t
ms_since(struct timespec *ts)
{
	struct timespec now;

	if (clock_gettime(CLOCK_REALTIME, &now) < 0)
		die("clock_gettime:");

	return (now.tv_sec - ts->tv_sec) * 1000
		+ (now.tv_nsec - ts->tv_nsec) / 1000000;
}

static enum tpu_port_dir
key_to_dir(int key)
{
	switch (key) {
	case KEY_LEFT:
	case 'A':
		return DIR_LEFT;
	case KEY_RIGHT:
	case 'D':
		return DIR_RIGHT;
	case KEY_UP:
	case 'W':
		return DIR_UP;
	case KEY_DOWN:
	case 'S':
		return DIR_DOWN;
	default:
		abort();
	}
}

static const cchar_t *
dir_to_arrow(enum tpu_port_dir dir)
{
	switch (dir) {
	case DIR_UP:
		return WACS_UARROW;
	case DIR_DOWN:
		return WACS_DARROW;
	case DIR_LEFT:
		return WACS_LARROW;
	case DIR_RIGHT:
		return WACS_RARROW;
	}
}

static int
tpu_pos_x(struct tpu *tpu)
{
	return 2 + (int) tpu->x * (TPU_W + 4);
}

static int
tpu_pos_y(struct tpu *tpu)
{
	return 2 + (int) tpu->y * (TPU_H + 2);
}

static void
tui_draw_box(int sx, int sy, int w, int h, attr_t attr,
	const cchar_t *ul, const cchar_t *ur,
	const cchar_t *ll, const cchar_t *lr)
{
	int x, y;

	if (sx + w < scrx || sx >= scrx + scrw) return;
	if (sy + h < scry || sy >= scry + scrh) return;

	sx -= scrx;
	sy -= scry;

	attron(attr);
	mvadd_wch(sy, sx, ul);
	mvadd_wch(sy, sx + w - 1, ur);
	mvadd_wch(sy + h - 1, sx, ll);
	mvadd_wch(sy + h - 1, sx + w - 1, lr);
	for (x = sx + 1; x < sx + w - 1; x++)
		mvadd_wch(sy, x, WACS_D_HLINE);
	for (x = sx + 1; x < sx + w - 1; x++)
		mvadd_wch(sy + h - 1, x, WACS_D_HLINE);
	for (y = sy + 1; y < sy + h - 1; y++)
		mvadd_wch(y, sx, WACS_D_VLINE);
	for (y = sy + 1; y < sy + h - 1; y++)
		mvadd_wch(y, sx + w - 1, WACS_D_VLINE);
	attroff(attr);
}

static void
__attribute__((format(printf, 4, 5)))
tui_draw_text(int x, int y, attr_t attr, const char *fmt, ...)
{
	char buf[512];
	va_list ap;
	int i;

	va_start(ap, fmt);
	vsnprintf(buf, 512, fmt, ap);
	va_end(ap);

	attron(attr);
	for (i = 0; i < strlen(buf) && x + i < scrx + scrw; i++)
		mvaddch(y - scry, x + i - scrx, (chtype) buf[i]);
	attroff(attr);
}

static void
tui_draw_wch(int x, int y, attr_t attr, const cchar_t *c)
{
	attron(attr);
	mvadd_wch(y - scry, x - scrx, c);
	attroff(attr);
}

static void
tui_draw_tpu(struct tpu *tpu)
{
	char linebuf[TPU_INPUT_COLS + 1];
	struct tpu_port *port;
	int sx, sy, x, y, w, h;
	int off, start, inst;
	size_t len;
	attr_t attr;
	int idle;

	attr = (tpu_sel == tpu && input_mode == TPU_NAV) ? A_BOLD : 0;

	sx = tpu_pos_x(tpu);
	sy = tpu_pos_y(tpu);
	tui_draw_box(sx, sy, TPU_W, TPU_H, attr,
		WACS_D_ULCORNER, WACS_D_URCORNER,
		WACS_D_LLCORNER, WACS_D_LRCORNER);

	if (tpu->inst_cnt > 0) {
		start = MAX(0, (int) tpu->pc - 6);
		for (off = 0, inst = start; inst < TPU_MAX_INST; inst++) {
			if (tpu->labels[inst]) {
				len = strlen(tpu->labels[inst]);
				if (len > TPU_INPUT_COLS - 1) {
					tui_draw_text(sx + 1, sy + 1 + off, A_DIM,
						"%.*s..:", TPU_INPUT_COLS - 3,
						tpu->labels[inst]);
				} else {
					tui_draw_text(sx + 1, sy + 1 + off, A_DIM,
						"%s:", tpu->labels[inst]);
				}
				if (++off >= TPU_INPUT_ROWS) break;
			}
			if (inst < tpu->inst_cnt) {
				asm_print_inst(linebuf, sizeof(linebuf),
					&tpu->insts[inst]);
				tui_draw_text(sx + 1, sy + 1 + off,
					inst == tpu->pc ? A_STANDOUT : 0, "%-*.*s",
					TPU_INPUT_COLS, TPU_INPUT_COLS, linebuf);
				if (++off >= TPU_INPUT_ROWS) break;
			}
		}
	}

	x = sx + TPU_W - TPU_INFO_W;
	y = sy;
	w = TPU_INFO_W;
	h = TPU_INFO_H;
	tui_draw_box(x, y, w, h, attr,
		WACS_D_TTEE, WACS_D_URCORNER, WACS_D_LTEE, WACS_D_RTEE);
	tui_draw_text(x + 2, y + 1, A_BOLD, "ACC");
	tui_draw_text(x + 2, y + 2, 0, "%03i", tpu->acc);

	tui_draw_box(x, (y += TPU_INFO_H - 1), w, h, attr,
		WACS_D_LTEE, WACS_D_RTEE, WACS_D_LTEE, WACS_D_RTEE);
	tui_draw_text(x + 2, y + 1, A_BOLD, "BAK");
	tui_draw_text(x + 2, y + 2, 0, "%03i", tpu->bak);

	tui_draw_box(x, (y += TPU_INFO_H - 1), w, h, attr,
		WACS_D_LTEE, WACS_D_RTEE, WACS_D_LTEE, WACS_D_RTEE);
	tui_draw_text(x + 2, y + 1, A_BOLD, "LST");
	if (tpu->last < 0) {
		tui_draw_text(x + 2, y + 2, 0, "N/A");
	} else {
		tui_draw_wch(x + 2, y + 2, 0,
			dir_to_arrow((enum tpu_port_dir) tpu->last));
		tui_draw_wch(x + 3, y + 2, 0,
			dir_to_arrow((enum tpu_port_dir) tpu->last));
		tui_draw_wch(x + 4, y + 2, 0,
			dir_to_arrow((enum tpu_port_dir) tpu->last));
	}

	tui_draw_box(x, (y += TPU_INFO_H - 1), w, h, attr,
		WACS_D_LTEE, WACS_D_RTEE, WACS_D_LTEE, WACS_D_RTEE);
	tui_draw_text(x + 2, y + 1, A_BOLD, "MOD");
	tui_draw_text(x + 2, y + 2, 0, "%s", mode_repr[tpu->status]);

	tui_draw_box(x, (y += TPU_INFO_H - 1), w, h, attr,
		WACS_D_LTEE, WACS_D_RTEE, WACS_D_BTEE, WACS_D_LRCORNER);
	tui_draw_text(x + 2, y + 1, A_BOLD, "IDL");
	if (tpu->steps > 0)
		idle = (int) ((double) tpu->idle_steps * 100 / (double) tpu->steps);
	else
		idle = 100;
	tui_draw_text(x + 2, y + 2, 0, "%03i", idle);

	port = &tpu->ports[DIR_LEFT];
	if (!port->dst_port || !(port->dst_port->type & PORT_OUT))
		attron(COLOR_PAIR(COLOR_WARN));
	if (port->in >= 0)
		tui_draw_text(sx - 3, sy + 6, A_BOLD, "%03i", port->in);
	if (port->type & PORT_IN)
		tui_draw_wch(sx - 1, sy + 7,
			port->in >= 0 ? A_BOLD : 0, WACS_RARROW);
	attroff(COLOR_PAIR(COLOR_WARN));
	if (!port->dst_port || !(port->dst_port->type & PORT_IN))
		attron(COLOR_PAIR(COLOR_WARN));
	if (port->type & PORT_OUT)
		tui_draw_wch(sx - 1, sy + 8,
			port->out_pending >= 0 ? A_BOLD : 0, WACS_LARROW);
	if (port->out_pending >= 0)
		tui_draw_text(sx - 3, sy + 10, A_BOLD, "%03i", port->out_pending);
	attroff(COLOR_PAIR(COLOR_WARN));

	port = &tpu->ports[DIR_RIGHT];
	if (!port->dst_port || !(port->dst_port->type & PORT_IN))
		attron(COLOR_PAIR(COLOR_WARN));
	if (port->out_pending >= 0)
		tui_draw_text(sx + TPU_W, sy + 5, A_BOLD, "%03i", port->out_pending);
	if (port->type & PORT_OUT)
		tui_draw_wch(sx + TPU_W, sy + 7,
			port->out_pending >= 0 ? A_BOLD : 0, WACS_RARROW);
	attroff(COLOR_PAIR(COLOR_WARN));
	if (!port->dst_port || !(port->dst_port->type & PORT_OUT))
		attron(COLOR_PAIR(COLOR_WARN));
	if (port->type & PORT_IN)
		tui_draw_wch(sx + TPU_W, sy + 8,
			port->in >= 0 ? A_BOLD : 0, WACS_LARROW);
	if (port->in >= 0)
		tui_draw_text(sx + TPU_W, sy + 9, A_BOLD, "%03i", port->in);
	attroff(COLOR_PAIR(COLOR_WARN));

	port = &tpu->ports[DIR_UP];
	if (!port->dst_port || !(port->dst_port->type & PORT_IN))
		attron(COLOR_PAIR(COLOR_WARN));
	if (port->out_pending >= 0)
		tui_draw_text(sx + 9, sy - 1, A_BOLD, "%03i", port->out_pending);
	if (port->type & PORT_OUT)
		tui_draw_wch(sx + 13, sy - 1,
			port->out_pending >= 0 ? A_BOLD : 0, WACS_UARROW);
	attroff(COLOR_PAIR(COLOR_WARN));
	if (!port->dst_port || !(port->dst_port->type & PORT_OUT))
		attron(COLOR_PAIR(COLOR_WARN));
	if (port->type & PORT_IN)
		tui_draw_wch(sx + 15, sy - 1,
			port->in >= 0 ? A_BOLD : 0, WACS_DARROW);
	if (port->in >= 0)
		tui_draw_text(sx + 17, sy - 1, A_BOLD, "%03i", port->in);
	attroff(COLOR_PAIR(COLOR_WARN));

	port = &tpu->ports[DIR_DOWN];
	if (!port->dst_port || !(port->dst_port->type & PORT_OUT))
		attron(COLOR_PAIR(COLOR_WARN));
	if (port->in >= 0)
		tui_draw_text(sx + 9, sy + TPU_H, A_BOLD, "%03i", port->in);
	if (port->type & PORT_IN)
		tui_draw_wch(sx + 13, sy + TPU_H,
			port->in >= 0 ? A_BOLD : 0, WACS_UARROW);
	attroff(COLOR_PAIR(COLOR_WARN));
	if (!port->dst_port || !(port->dst_port->type & PORT_IN))
		attron(COLOR_PAIR(COLOR_WARN));
	if (port->type & PORT_OUT)
		tui_draw_wch(sx + 15, sy + TPU_H,
			port->out_pending >= 0 ? A_BOLD : 0, WACS_DARROW);
	if (port->out_pending >= 0)
		tui_draw_text(sx + 17, sy + TPU_H, A_BOLD, "%03i", port->out_pending);
	attroff(COLOR_PAIR(COLOR_WARN));
}

static void
tui_draw(void)
{
	struct tpu *tpu;
	size_t i;
	int tx;

	clear();
	for (tpu = tis.tpu_vec.tpus, i = 0; i < tis.tpu_vec.cnt; i++, tpu++)
		tui_draw_tpu(tpu);
	if (showing_reloaded) {
		tx = scrx + scrw / 2 - 4;
		tui_draw_text(scrx, scry, A_STANDOUT, "%*s", scrw, "");
		tui_draw_text(tx, scry, A_STANDOUT, "RELOADED");
	}
	refresh();
}

static void
tui_resize(void)
{
	scrw = getmaxx(stdscr);
	scrh = getmaxy(stdscr);
}

static void
tpu_seek_running(void)
{
	struct tpu *tpu;
	size_t i;

	for (tpu = tis.tpu_vec.tpus, i = 0; i < tis.tpu_vec.cnt; i++, tpu++) {
		if (tpu->status == STATUS_RUN) tpu_sel = tpu;
	}
}

static void
tui_seek(struct tpu *tpu, int dx, int dy)
{
	int minx, miny, maxx, maxy;
	int x, y;
	size_t i;

	if (tpu) {
		minx = maxx = tpu_pos_x(tpu);
		miny = maxy = tpu_pos_y(tpu);
 	} else {
		minx = miny = maxx = maxy = -1;
		for (tpu = tis.tpu_vec.tpus, i = 0; i < tis.tpu_vec.cnt; i++, tpu++) {
			x = tpu_pos_x(tpu);
			if (minx == -1 || x < minx) minx = x;
			if (maxx == -1 || x > maxx) maxx = x;
			y = tpu_pos_y(tpu);
			if (miny == -1 || y < miny) miny = y;
			if (maxy == -1 || y > maxy) maxy = y;
		}
		if (minx == -1 || miny == -1) return;
	}

	if (dx == MIN) scrx = minx - 2;
	else if (dx == MAX) scrx = maxx + TPU_W + 2 - scrw;
	else if (dx == MID) scrx = (minx + maxx + TPU_W - scrw) / 2;

	if (dy == MIN) scry = miny - 2;
	else if (dy == MAX) scry = maxy + TPU_H + 2 - scrh;
	else if (dy == MID) scry = (miny + maxy + TPU_H - scrh) / 2;
}

static void
handlekey(int key)
{
	enum tpu_port_dir dir;

	if (input_mode == MAIN) {
		switch (key) {
		case 'I':
			input_mode = TPU_NAV;
			break;
		case KEY_UP:
		case 'W':
			scry -= 2;
			break;
		case KEY_DOWN:
		case 'S':
			scry += 2;
			break;
		case KEY_LEFT:
		case 'A':
			scrx -= 4;
			break;
		case KEY_RIGHT:
		case 'D':
			scrx += 4;
			break;
		}
	} else {
		switch (key) {
		case KEY_ESC:
			input_mode = MAIN;
			break;
		case KEY_UP:
		case 'W':
		case KEY_DOWN:
		case 'A':
		case KEY_LEFT:
		case 'S':
		case KEY_RIGHT:
		case 'D':
			dir = key_to_dir(key);
			if (tpu_sel && tpu_sel->ports[dir].dst_tpu)
				tpu_sel = tpu_sel->ports[dir].dst_tpu;
			tui_seek(tpu_sel, MID, MID);
			break;
		case 'c':
			if (!tpu_sel) return;
			do {
				tis_step(&tis);
			} while (tpu_sel->status != STATUS_RUN && tis.alive);
			break;
		case 'p':
			tpu_seek_running();
			break;
		}
	}
}

static void
reset(int ifd, int argc, char **argv, bool watch)
{
	FILE *tis_stdin, *tis_stdout;

	tis_stdin = NULL;
	if (argc >= 3) {
		tis_stdin = fopen(argv[2], "r");
		if (!tis_stdin) die("fopen '%s':", argv[2]);
	}

	tis_stdout = NULL;
	if (argc >= 4) {
		tis_stdout = fopen(argv[3], "w+");
		if (!tis_stdout) die("fopen '%s':", argv[3]);
	}

	tis_load(&tis, argv[1], tis_stdin, tis_stdout);

	if (watch)
		if (inotify_add_watch(ifd, argv[1], IN_CLOSE_WRITE) < 0)
			die("inotify_add_watch '%s':", argv[1]);

	if (tis.stdin_port.attached) {
		tpu_sel = tis.stdin_port.dst_tpu;
	} else {
		tpu_sel = tis.tpu_vec.cnt ? &tis.tpu_vec.tpus[0] : NULL;
	}
}

int
main(int argc, char **argv)
{
	struct timeval timeout;
	struct inotify_event event;
	ssize_t len;
	fd_set fds;
	bool quit;
	int key;
	int ifd;
	int rc;

	if (argc < 2 || argc > 4) {
		fprintf(stderr, "Usage: tis256-curses FILE [STDIN] [STDOUT]\n");
		exit(1);
	}

	setlocale(LC_ALL, "");

	initscr();
	raw();
	noecho();
	keypad(stdscr, TRUE);
	start_color();
	curs_set(0);
	tui_resize();
	ESCDELAY = 0;

	init_pair(COLOR_WARN, COLOR_RED, COLOR_BLACK);

	tis_init(&tis, NULL, NULL);

	ifd = inotify_init1(IN_NONBLOCK);

	reset(ifd, argc, argv, true);

	tui_seek(NULL, MID, MID);

	quit = false;
	while (!quit) {
		tui_draw();

		FD_ZERO(&fds);
		FD_SET(ifd, &fds);
		FD_SET(0, &fds);
		timeout.tv_sec = 0;
		timeout.tv_usec = 500000;
		rc = select(ifd+1, &fds, NULL, NULL,
			showing_reloaded ? &timeout : NULL);
		if (rc < 0 && errno == EINTR) continue;
		if (rc < 0) die("select:");

		if (FD_ISSET(ifd, &fds)) {
			len = read(ifd, &event, sizeof(event));
			if (len < 0 && errno != EAGAIN)
				die("inotify_read:");
			if (len >= 0)
				reset(ifd, argc, argv, true);
			if (clock_gettime(CLOCK_REALTIME, &show_reloaded) < 0)
				die("clock_gettime:");
			showing_reloaded = true;
		}

		if (!showing_reloaded || ms_since(&show_reloaded) < 500) {
			if (!FD_ISSET(ifd, &fds) && !FD_ISSET(0, &fds))
				continue;
		} else {
			showing_reloaded = false;
		}

		if (!FD_ISSET(0, &fds)) continue;
		key = getch();
		switch (key) {
		case KEY_RESIZE:
			tui_resize();
			break;
		case 'g':
			tui_seek(tpu_sel, MID, MID);
			break;
		case 'h':
			tui_seek(NULL, MID, MID);
			break;
		case 'i':
			if (tis.stdin_port.dst_tpu) {
				tpu_sel = tis.stdin_port.dst_tpu;
				tui_seek(tis.stdin_port.dst_tpu, MID, MID);
			}
			break;
		case 'o':
			if (tis.stdout_port.dst_tpu) {
				tpu_sel = tis.stdout_port.dst_tpu;
				tui_seek(tis.stdout_port.dst_tpu, MID, MID);
			}
			break;
		case 'r':
			reset(ifd, argc, argv, false);
			break;
		case 's':
			tis_step(&tis);
			break;
		case KEY_CTRL('c'):
			quit = true;
			break;
		default:
			handlekey(key);
			break;
		}
	}

	tis_deinit(&tis);

	close(ifd);

	endwin();
}
