#include "asm.h"
#include "util.h"

#include "raylib.h"
#include "raymath.h"
#include "tpu.h"

#include <math.h>
#include <string.h>

#define TPU_PAD 15
#define TPU_SIZE 160
#define TPU_DIST (TPU_SIZE + 2 * TPU_PAD)

struct tpu_info {
	int inst_off;
};

static uint16_t window_width = 0;
static uint16_t window_height = 0;

static bool drag = false;
static Vector2 drag_mouse = { 0 };
static Vector2 drag_target = { 0 };

static float mouse_scroll = 0;
static Vector2 mouse = { 0 };

static Camera2D camera = { 0 };

static struct tis tis = { 0 };

int (*cleanup)(void) = NULL;
const char *progname = "tis256-gui";

static void
draw_rect(float x, float y, float w, float h, Color c)
{
	DrawRectangle((int) x, (int) y, (int) w, (int) h, c);
}

static void
draw_text(float x, float y, const char *str, int size, Color c)
{
	DrawText(str, (int) x, (int) y, size, c);
}

static void
draw_tpu(struct tpu *tpu)
{
	const int max_h = (TPU_SIZE - 8) / 8;
	const int max_w = (TPU_SIZE - 8) / 5;
	struct tpu_info *info;
	char linebuf[32];
	int inst, off;
	float sx, sy;
	size_t len;
	Vector2 v;

	sx = (float) tpu->x * TPU_DIST;
	sy = (float) tpu->y * TPU_DIST;

	v = Vector2Transform((Vector2) { sx, sy }, GetCameraMatrix2D(camera));
	if (v.x >= window_width || v.y >= window_height) return;

	v = Vector2Transform((Vector2) { sx + TPU_SIZE, sy + TPU_SIZE },
		GetCameraMatrix2D(camera));
	if (v.x < 0 || v.y < 0) return;

	draw_rect(sx, sy, TPU_SIZE, TPU_SIZE,
		tpu->status == STATUS_RUN ? GREEN : WHITE);
	if (camera.zoom >= 1) {
		draw_rect(sx + 2, sy + 2, TPU_SIZE - 4, TPU_SIZE - 4, BLACK);
		info = tpu->user;
		inst = info->inst_off;
		for (off = 0; inst < TPU_MAX_INST; inst++) {
			if (tpu->labels[inst]) {
				len = strlen(tpu->labels[inst]);
				snprintf(linebuf, 32, "%.*s:", max_w - 1,
					tpu->labels[inst]);
				draw_text(sx + 4, sy + 4 + (float) off * 8,
					linebuf, 6, WHITE);
				if (++off >= max_h) break;
			}
			if (inst < tpu->inst_cnt) {
				asm_print_inst(linebuf, 32, &tpu->insts[inst]);
				draw_text(sx + 4, sy + 4 + (float) off * 8,
					linebuf, 6, WHITE);
				if (++off >= max_h) break;
			}
		}
	}
	if (tpu->ports[DIR_LEFT].type != 0)
		draw_rect(sx - TPU_PAD, sy + TPU_SIZE / 2.f, TPU_PAD, 4,
			tpu->ports[DIR_LEFT].attached ? WHITE : RED);
	if (tpu->ports[DIR_RIGHT].type != 0)
		draw_rect(sx + TPU_SIZE, sy + TPU_SIZE / 2.f, TPU_PAD, 4,
			tpu->ports[DIR_RIGHT].attached ? WHITE : RED);
	if (tpu->ports[DIR_UP].type != 0)
		draw_rect(sx + TPU_SIZE / 2.f, sy - TPU_PAD, 4, TPU_PAD,
			tpu->ports[DIR_UP].attached ? WHITE : RED);
	if (tpu->ports[DIR_DOWN].type != 0)
		draw_rect(sx + TPU_SIZE / 2.f, sy + TPU_SIZE, 4, TPU_PAD,
			tpu->ports[DIR_DOWN].attached ? WHITE : RED);
}

static struct tpu *
in_tpu(Vector2 pos)
{
	struct tpu *tpu;
	float x, y;
	size_t i;

	for (tpu = tis.tpu_vec.tpus, i = 0; i < tis.tpu_vec.cnt; i++, tpu++) {
		x = (float) tpu->x * TPU_DIST;
		y = (float) tpu->y * TPU_DIST;
		if (pos.x >= x && pos.x < x + TPU_SIZE
				&& pos.y >= y && pos.y < y + TPU_SIZE)
			return tpu;
	}

	return NULL;
}

int
main(int argc, const char **argv)
{
	Vector2 wpos_prev, wpos;
	struct tpu *tpu;
	struct tpu_info *info;
	float min_x, min_y;
	float max_x, max_y;
	double last_step;
	FILE *tis_stdin, *tis_stdout;
	float x, y;
	size_t i;

	if (argc < 2 || argc > 4) {
		fprintf(stderr, "Usage: tis256-gui FILE [STDIN] [STDOUT]\n");
		exit(1);
	}

	tis_stdin = NULL;
	if (argc >= 3) {
		tis_stdin = fopen(argv[2], "r");
		if (!tis_stdin) die("fopen '%s':", argv[2]);
	}

	tis_stdout = NULL;
	if (argc >= 4) {
		tis_stdout = fopen(argv[3], "r");
		if (!tis_stdout) die("fopen '%s':", argv[3]);
	}

	tis_load(&tis, argv[1], tis_stdin, tis_stdout);

	min_x = min_y = INFINITY;
	max_x = max_y = -INFINITY;
	for (tpu = tis.tpu_vec.tpus, i = 0; i < tis.tpu_vec.cnt; i++, tpu++) {
		tpu->user = calloc(1, sizeof(struct tpu_info));
		if (!tpu->user) die("calloc:");
		x = (float) tpu->x * TPU_DIST;
		y = (float) tpu->y * TPU_DIST;
		min_x = MIN(min_x, x);
		min_y = MIN(min_y, y);
		max_x = MAX(max_x, x + TPU_SIZE);
		max_y = MAX(max_y, y + TPU_SIZE);
	}
	if (min_x == INFINITY) min_x = min_y = max_x = max_y = 0;

	SetConfigFlags(FLAG_WINDOW_RESIZABLE);
	InitWindow(800, 600, "tis256-gui");
	SetTargetFPS(60);

	camera.target.x = (min_x + max_x) / 2;
	camera.target.y = (min_y + max_y) / 2;
	camera.zoom = 1.f;

	while (!WindowShouldClose()) {
		if (IsWindowResized() || !window_width || !window_height) {
			window_width = (uint16_t) GetScreenWidth();
			window_height = (uint16_t) GetScreenHeight();
			camera.offset.x = (float) window_width / 2;
			camera.offset.y = (float) window_height / 2;
		}

		mouse = GetMousePosition();
		if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON)) {
			drag_mouse = mouse;
			drag_target = camera.target;
			drag = true;
		} else if (IsMouseButtonReleased(MOUSE_LEFT_BUTTON)) {
			drag = false;
		}

		mouse_scroll = GetMouseWheelMove();
		if (mouse_scroll != 0) {
			wpos_prev = Vector2Transform(mouse,
				MatrixInvert(GetCameraMatrix2D(camera)));
			if (IsKeyDown(KEY_LEFT_SHIFT) && (tpu = in_tpu(wpos_prev))) {
				info = tpu->user;
				info->inst_off += mouse_scroll > 0 ? -1 : 1;
				info->inst_off = MAX(0, MIN(info->inst_off,
					(int) tpu->inst_cnt-1));
			} else {
				camera.zoom *= mouse_scroll > 0 ? 2.f : 0.5f;
				wpos = Vector2Transform(mouse,
					MatrixInvert(GetCameraMatrix2D(camera)));
				camera.target.x += wpos_prev.x - wpos.x;
				camera.target.y += wpos_prev.y - wpos.y;
			}
		}

		if (IsKeyDown(KEY_S) && GetTime() > last_step + 0.05) {
			last_step = GetTime();
			tis_step(&tis);
		}

		if (drag) {
			camera.target.x = drag_target.x
				- (mouse.x - drag_mouse.x) / camera.zoom;
			camera.target.y = drag_target.y
				- (mouse.y - drag_mouse.y) / camera.zoom;
		}

		BeginDrawing();

		ClearBackground(BLACK);

		BeginMode2D(camera);

		for (tpu = tis.tpu_vec.tpus, i = 0; i < tis.tpu_vec.cnt; i++, tpu++)
			draw_tpu(tpu);

		EndMode2D();

		EndDrawing();
	}

	tis_deinit(&tis);
}
