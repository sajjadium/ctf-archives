#include <ctype.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_ROUTES 6
#define MAX_TRAINS 4
#define MAX_EVENTS 8
#define LINE_BUF 512

struct Route;
typedef void (*route_callback_t)(struct Route *route);

typedef struct Route {
    char code[24];
    char manifest[64];
    route_callback_t depart_cb;
    int depart_tick;
    int cancelled;
} Route;

typedef struct Train {
    int id;
    Route *route;
} Train;

typedef struct CleanupEvent {
    int active;
    int due_tick;
    int slot;
    Route *route;
} CleanupEvent;

static Route *g_routes[MAX_ROUTES];
static Train g_trains[MAX_TRAINS];
static CleanupEvent g_cleanup_events[MAX_EVENTS];
static int g_tick = 0;
static int g_bulletin_pending = 0;
static unsigned char g_bulletin_packet[sizeof(Route)];

static void setup(void) {
    alarm(120);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

__attribute__((noinline)) void dispatch_override(Route *route) {
    const char *flag = getenv("FLAG");

    if (flag == NULL) {
        flag = "uctf{dev-train-dispatch-simulator}";
    }

    printf("Override accepted for route %s.\n", route->code);
    puts(flag);
}

__attribute__((noinline)) void normal_departure(Route *route) {
    printf("Train departed on %s carrying manifest '%s'.\n", route->code, route->manifest);
}

static void print_help(void) {
    puts("Commands:");
    puts("  new <slot> <depart_in_ticks> <route_code>");
    puts("  manifest <slot>");
    puts("  assign <train_id> <slot>");
    puts("  cancel <slot>");
    puts("  bulletin");
    puts("  diag <slot>");
    puts("  show");
    puts("  advance");
    puts("  help");
    puts("  quit");
}

static void strip_newline(char *s) {
    size_t n;

    if (s == NULL) {
        return;
    }

    n = strlen(s);
    if (n > 0 && s[n - 1] == '\n') {
        s[n - 1] = '\0';
    }
}

static int queue_cleanup(Route *route, int slot, int due_tick) {
    int i;

    for (i = 0; i < MAX_EVENTS; i++) {
        if (!g_cleanup_events[i].active) {
            g_cleanup_events[i].active = 1;
            g_cleanup_events[i].due_tick = due_tick;
            g_cleanup_events[i].slot = slot;
            g_cleanup_events[i].route = route;
            return 1;
        }
    }

    return 0;
}

static int hex_value(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    }
    if (c >= 'a' && c <= 'f') {
        return c - 'a' + 10;
    }
    if (c >= 'A' && c <= 'F') {
        return c - 'A' + 10;
    }
    return -1;
}

static int parse_hex_packet(const char *hex, unsigned char *out, size_t out_len) {
    size_t i;

    for (i = 0; i < out_len; i++) {
        int hi = hex_value(hex[i * 2]);
        int lo = hex_value(hex[i * 2 + 1]);

        if (hi < 0 || lo < 0) {
            return 0;
        }

        out[i] = (unsigned char)((hi << 4) | lo);
    }

    return hex[out_len * 2] == '\0';
}

static void cmd_new(int slot, int depart_in, const char *code) {
    Route *route;

    if (slot < 0 || slot >= MAX_ROUTES) {
        puts("Invalid slot.");
        return;
    }

    if (depart_in < 1 || depart_in > 20) {
        puts("depart_in_ticks must be between 1 and 20.");
        return;
    }

    if (g_routes[slot] != NULL) {
        puts("Slot already in use.");
        return;
    }

    route = (Route *)malloc(sizeof(Route));
    if (route == NULL) {
        puts("Allocation failed.");
        exit(1);
    }

    memset(route, 0, sizeof(Route));
    snprintf(route->code, sizeof(route->code), "%s", code);
    snprintf(route->manifest, sizeof(route->manifest), "standard cargo");
    route->depart_cb = normal_departure;
    route->depart_tick = g_tick + depart_in;
    route->cancelled = 0;

    g_routes[slot] = route;

    printf("Route %s created in slot %d. Scheduled for tick %d.\n", route->code, slot, route->depart_tick);
}

static void cmd_manifest(int slot) {
    char line[128];

    if (slot < 0 || slot >= MAX_ROUTES || g_routes[slot] == NULL) {
        puts("No route in that slot.");
        return;
    }

    printf("Manifest text for slot %d: ", slot);
    if (fgets(line, sizeof(line), stdin) == NULL) {
        puts("Input error.");
        exit(1);
    }
    strip_newline(line);

    snprintf(g_routes[slot]->manifest, sizeof(g_routes[slot]->manifest), "%s", line);
    puts("Manifest updated.");
}

static void cmd_assign(int train_id, int slot) {
    if (train_id < 0 || train_id >= MAX_TRAINS) {
        puts("Invalid train id.");
        return;
    }

    if (slot < 0 || slot >= MAX_ROUTES || g_routes[slot] == NULL) {
        puts("No route in that slot.");
        return;
    }

    g_trains[train_id].route = g_routes[slot];
    printf("Train %d assigned to route %s.\n", train_id, g_routes[slot]->code);
}

static void cmd_cancel(int slot) {
    Route *route;

    if (slot < 0 || slot >= MAX_ROUTES || g_routes[slot] == NULL) {
        puts("No route in that slot.");
        return;
    }

    route = g_routes[slot];
    if (route->cancelled) {
        puts("Route already cancelled.");
        return;
    }

    route->cancelled = 1;

    if (!queue_cleanup(route, slot, g_tick + 1)) {
        puts("Maintenance queue is full.");
        return;
    }

    printf("Route %s cancelled. Cleanup queued for tick %d.\n", route->code, g_tick + 1);
}

static void cmd_diag(int slot) {
    if (slot < 0 || slot >= MAX_ROUTES || g_routes[slot] == NULL) {
        puts("No route in that slot.");
        return;
    }

    printf("Telemetry: depart callback @ %p\n", (void *)g_routes[slot]->depart_cb);
    printf("Telemetry: route departs at tick %d\n", g_routes[slot]->depart_tick);
}

static void cmd_show(void) {
    int i;

    printf("Tick: %d\n", g_tick);
    for (i = 0; i < MAX_ROUTES; i++) {
        if (g_routes[i] == NULL) {
            printf("Slot %d: [empty]\n", i);
            continue;
        }
        printf("Slot %d: %s depart=%d cancelled=%d\n", i, g_routes[i]->code, g_routes[i]->depart_tick,
               g_routes[i]->cancelled);
    }

    for (i = 0; i < MAX_TRAINS; i++) {
        if (g_trains[i].route == NULL) {
            printf("Train %d: idle\n", i);
        } else {
            printf("Train %d: tracking route ptr %p\n", i, (void *)g_trains[i].route);
        }
    }

    puts("Tick order: maintenance -> emergency bulletin -> departures");
}

static void cmd_bulletin(void) {
    char line[LINE_BUF];
    size_t expect_chars = sizeof(g_bulletin_packet) * 2;

    printf("Emergency bulletin packet (%zu hex chars): ", expect_chars);
    if (fgets(line, sizeof(line), stdin) == NULL) {
        puts("Input error.");
        exit(1);
    }
    strip_newline(line);

    if (strlen(line) != expect_chars) {
        puts("Invalid length.");
        return;
    }

    if (!parse_hex_packet(line, g_bulletin_packet, sizeof(g_bulletin_packet))) {
        puts("Invalid hex.");
        return;
    }

    g_bulletin_pending = 1;
    puts("Emergency bulletin queued for next tick.");
}

static void process_maintenance(void) {
    int i;

    for (i = 0; i < MAX_EVENTS; i++) {
        if (!g_cleanup_events[i].active || g_cleanup_events[i].due_tick > g_tick) {
            continue;
        }

        free(g_cleanup_events[i].route);
        if (g_routes[g_cleanup_events[i].slot] == g_cleanup_events[i].route) {
            g_routes[g_cleanup_events[i].slot] = NULL;
        }

        printf("Maintenance: cleaned slot %d at tick %d.\n", g_cleanup_events[i].slot, g_tick);
        g_cleanup_events[i].active = 0;
    }
}

static void process_bulletin(void) {
    void *p;

    if (!g_bulletin_pending) {
        return;
    }

    p = malloc(sizeof(Route));
    if (p == NULL) {
        puts("Emergency allocator failure.");
        exit(1);
    }

    memcpy(p, g_bulletin_packet, sizeof(Route));
    printf("Dispatch loaded an emergency route template at %p.\n", p);
    g_bulletin_pending = 0;
}

static void process_departures(void) {
    int i;

    for (i = 0; i < MAX_TRAINS; i++) {
        Route *route = g_trains[i].route;

        if (route == NULL) {
            continue;
        }

        if (route->depart_tick <= g_tick) {
            printf("Departure check: train %d leaving now.\n", i);
            route->depart_cb(route);
            g_trains[i].route = NULL;
        }
    }
}

static void cmd_advance(void) {
    g_tick++;
    printf("-- Tick advanced to %d --\n", g_tick);
    process_maintenance();
    process_bulletin();
    process_departures();
}

int main(void) {
    char line[LINE_BUF];
    int i;

    setup();

    for (i = 0; i < MAX_TRAINS; i++) {
        g_trains[i].id = i;
        g_trains[i].route = NULL;
    }

    puts("Northline Dispatch Sim v1.4");
    puts("Deterministic scheduler seed: 0xC0FFEE22");
    puts("Type 'help' for commands.");

    while (1) {
        int slot;
        int depart_in;
        int train_id;
        char code[24];

        printf("dispatch> ");
        if (fgets(line, sizeof(line), stdin) == NULL) {
            break;
        }
        strip_newline(line);

        if (strcmp(line, "help") == 0) {
            print_help();
            continue;
        }
        if (strcmp(line, "quit") == 0) {
            puts("Shift ended.");
            break;
        }
        if (strcmp(line, "show") == 0) {
            cmd_show();
            continue;
        }
        if (strcmp(line, "advance") == 0) {
            cmd_advance();
            continue;
        }
        if (strcmp(line, "bulletin") == 0) {
            cmd_bulletin();
            continue;
        }

        if (sscanf(line, "new %d %d %23s", &slot, &depart_in, code) == 3) {
            cmd_new(slot, depart_in, code);
            continue;
        }

        if (sscanf(line, "manifest %d", &slot) == 1) {
            cmd_manifest(slot);
            continue;
        }

        if (sscanf(line, "assign %d %d", &train_id, &slot) == 2) {
            cmd_assign(train_id, slot);
            continue;
        }

        if (sscanf(line, "cancel %d", &slot) == 1) {
            cmd_cancel(slot);
            continue;
        }

        if (sscanf(line, "diag %d", &slot) == 1) {
            cmd_diag(slot);
            continue;
        }

        puts("Unknown command.");
    }

    return 0;
}
