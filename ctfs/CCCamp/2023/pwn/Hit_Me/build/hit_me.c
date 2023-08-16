#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define WIDTH 64
#define HEIGHT 16

char battlefield[WIDTH * HEIGHT];
char help_text[] = "Try to hit the target by using the commands below:\n"
  " X <velocity in X direction>\n"
  " Y <velocity in Y direction>\n"
  " Fire!!";
const int start_y = HEIGHT / 2;
const double G_2 = 9.81 / 2.0;
const double TSCALE = 0.005;

void clear_battlefield() { memset(battlefield, '.', WIDTH * HEIGHT); }
void print_battlefield() {
  for (int y = HEIGHT - 1; y >= 0; y--) {
    fwrite(battlefield + y * WIDTH, 1, WIDTH, stdout);
    putchar('\n');
  }
}
int draw_trajectory(double velocity_x, double velocity_y, int target_x,
                    int target_y, char projectile) {

  int x = 0;
  int y = start_y;

  battlefield[target_y * WIDTH + target_x] = 'T';

  for (int ti = 0;; ti++) {
    double t = ti * TSCALE;
    x = (int)(velocity_x * t);
    y = start_y + (int)(velocity_y * t - G_2 * t * t);

    if (x < WIDTH && y < HEIGHT) {
      battlefield[y * WIDTH + x] = projectile;
    }

    if (x == target_x && y == target_y) {
      return 1;
    } else if (x > target_x || y < target_y) {
      return 0;
    }
  }
}
char choose_projectile() {
  char projectile;
  printf("Choose your projectile: ");
  do {
    projectile = getchar();
  } while (projectile == '\n' || projectile == '\0' || projectile == ' ');
  printf("\nExcellent choice: %x\n", projectile);

  int c;
  while((c = getchar()) != '\n' && c != EOF);

  return projectile;
}
void print_help() {
  puts(help_text);
}
void generate_target(int *x, int *y) {
  *x = 4 + rand() % (WIDTH - 5);
  *y = rand() % (start_y + 1);
}
void parse_velocity(const char *arg, double *velocity) {
    *velocity = strtod(arg + 2, NULL);
}

int run_one_game() {
  char order[64];
  int target_x, target_y;
  int is_hit = 0;
  double velocity_x = 0.0;
  double velocity_y = 0.0;
  generate_target(&target_x, &target_y);

  printf("Ahh! Hello aaagain! Your target is at %d, %d\n", target_x, target_y);
  char projectile = choose_projectile();

  int fire = 0;
  while (!fire) {
    printf("[Vx = %lf, Vy = %lf]> ", velocity_x, velocity_y);
    memset(order, 0, sizeof(order));
    fgets(order, sizeof(order), stdin);

    switch (order[0]) {
    case 'X':
      parse_velocity(order, &velocity_x);
      break;
    case 'Y':
      parse_velocity(order, &velocity_y);
      break;
    case 'F':
      if (velocity_y > 0.0 && velocity_x > 0.0) {
        fire = 1;
      } else {
        printf("Sorry. We cannot shoot backwards: Vx = %lf; Vy = %lf\n",
               velocity_x, velocity_y);
      }
      break;
    case 'H':
    case 'h':
      print_help();
      break;
    default:
      puts("Sorry, I do not understand that :(");
      break;
    }
  }

  clear_battlefield();
  is_hit =
      draw_trajectory(velocity_x, velocity_y, target_x, target_y, projectile);
  print_battlefield();
  if (is_hit) {
    printf("\nExcellent hit, sir!\n");
  }
  return is_hit;
}

int main(void) {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);

  srand(time(NULL));

  int num_hits = 0;

  while (num_hits < 10) {
    num_hits += run_one_game();
  }

  exit(0);
}

void dont_mind_me() {
    system("no shell for you :(");
}
