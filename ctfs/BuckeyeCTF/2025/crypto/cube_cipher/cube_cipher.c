#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

typedef uint8_t face_t;

typedef uint8_t edge_t;
typedef uint8_t center_t;
typedef uint16_t corner_t;

#define FACE_SIZE 4
#define FACE_MASK ((1 << FACE_SIZE) - 1)
#define TWO_FACE_MASK ((1 << 2 * FACE_SIZE) - 1)

#define ALGORITHM_LENGTH 40

const size_t CENTER_CT = 6;
const size_t FACE_CT = CENTER_CT * 3 * 3;
const size_t CORNER_CT = 8;
const size_t EDGE_CT = 12;

/**
 * Create a corner.
 */
corner_t corner(const face_t top, const face_t left, const face_t right) {
	return (top << FACE_SIZE | left) << FACE_SIZE | right;
}

/**
 * Retrieve the top face of a corner.
 */
face_t corner_top(const corner_t corner) {
	return corner >> 2 * FACE_SIZE;
}

/**
 * Retrieve the left face of a corner.
 */
face_t corner_left(const corner_t corner) {
	return (corner >> FACE_SIZE) & FACE_MASK;
}

/**
 * Retrieve the right face of a corner.
 */
face_t corner_right(const corner_t corner) {
	return corner & FACE_MASK;
}

/**
 * Create an edge.
 */
edge_t edge(const face_t left, const face_t right) {
	return left << FACE_SIZE | right;
}

/**
 * Retrieve the left face of an edge.
 */
face_t edge_left(const edge_t edge) {
	return (edge >> FACE_SIZE) & FACE_MASK;
}

/**
 * Retrieve the right face of an edge.
 */
face_t edge_right(const edge_t edge) {
	return edge & FACE_MASK;
}

/**
 * Flip an edge.
 */
edge_t flip_edge(const edge_t edge) {
	return edge << FACE_SIZE | edge >> FACE_SIZE;
}

/**
 * Rotate a corner clockwise.
 */
corner_t rotate_corner(const corner_t corner) {
	return ((corner & FACE_MASK) << 2 * FACE_SIZE)
		| (corner >> FACE_SIZE);
}

/**
 * Rotate a corner counterclockwise.
 */
corner_t rotate_corner_(const corner_t corner) {
	return ((corner & TWO_FACE_MASK) << FACE_SIZE)
		| (corner >> 2 * FACE_SIZE);
}

/**
 * Naming:
 * Each field is comprised of each face the piece touches. The first letter is
 * chosen from the following order of precedence:
 *
 * f - front
 * b - back
 * u - up
 * d - down
 * l - left
 * r - right
 *
 * Then, for corners, the other two are chosen as the left and right ones if
 * the first face were on top.
 */
struct Cube {
	corner_t ful;
	corner_t fru;
	corner_t fld;
	corner_t fdr;

	corner_t blu;
	corner_t bur;
	corner_t bdl;
	corner_t brd;

	edge_t fu;
	edge_t fr;
	edge_t fd;
	edge_t fl;

	edge_t bu;
	edge_t br;
	edge_t bd;
	edge_t bl;

	edge_t ur;
	edge_t ul;
	edge_t dr;
	edge_t dl;

	center_t f;
	center_t b;
	center_t u;
	center_t d;
	center_t l;
	center_t r;
};

/**
 * Rotate front face clockwise.
 */
void move_F(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->ful;
	cube->ful = cube->fld;
	cube->fld = cube->fdr;
	cube->fdr = cube->fru;
	cube->fru = temp_corner;

	temp_edge = cube->fu;
	cube->fu = cube->fl;
	cube->fl = cube->fd;
	cube->fd = cube->fr;
	cube->fr = temp_edge;
}

/**
 * Rotate front face counterclockwise.
 */
void move_F_(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->ful;
	cube->ful = cube->fru;
	cube->fru = cube->fdr;
	cube->fdr = cube->fld;
	cube->fld = temp_corner;

	temp_edge = cube->fu;
	cube->fu = cube->fr;
	cube->fr = cube->fd;
	cube->fd = cube->fl;
	cube->fl = temp_edge;
}

/**
 * Rotate back face clockwise.
 */
void move_B(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->blu;
	cube->blu = cube->bur;
	cube->bur = cube->brd;
	cube->brd = cube->bdl;
	cube->bdl = temp_corner;

	temp_edge = cube->bu;
	cube->bu = cube->br;
	cube->br = cube->bd;
	cube->bd = cube->bl;
	cube->bl = temp_edge;
}

/**
 * Rotate back face counterclockwise.
 */
void move_B_(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->blu;
	cube->blu = cube->bdl;
	cube->bdl = cube->brd;
	cube->brd = cube->bur;
	cube->bur = temp_corner;

	temp_edge = cube->bu;
	cube->bu = cube->bl;
	cube->bl = cube->bd;
	cube->bd = cube->br;
	cube->br = temp_edge;
}

/**
 * Rotate right face clockwise.
 */
void move_R(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->fru;
	cube->fru = rotate_corner_(cube->fdr);
	cube->fdr = rotate_corner(cube->brd);
	cube->brd = rotate_corner_(cube->bur);
	cube->bur = rotate_corner(temp_corner);

	temp_edge = cube->fr;
	cube->fr = cube->dr;
	cube->dr = cube->br;
	cube->br = cube->ur;
	cube->ur = temp_edge;
}

/**
 * Rotate right face counterclockwise.
 */
void move_R_(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->fru;
	cube->fru = rotate_corner_(cube->bur);
	cube->bur = rotate_corner(cube->brd);
	cube->brd = rotate_corner_(cube->fdr);
	cube->fdr = rotate_corner(temp_corner);

	temp_edge = cube->fr;
	cube->fr = cube->ur;
	cube->ur = cube->br;
	cube->br = cube->dr;
	cube->dr = temp_edge;
}

/**
 * Rotate left face clockwise.
 */
void move_L(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->ful;
	cube->ful = rotate_corner(cube->blu);
	cube->blu = rotate_corner_(cube->bdl);
	cube->bdl = rotate_corner(cube->fld);
	cube->fld = rotate_corner_(temp_corner);

	temp_edge = cube->fl;
	cube->fl = cube->ul;
	cube->ul = cube->bl;
	cube->bl = cube->dl;
	cube->dl = temp_edge;
}

/**
 * Rotate left face counterclockwise.
 */
void move_L_(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->ful;
	cube->ful = rotate_corner(cube->fld);
	cube->fld = rotate_corner_(cube->bdl);
	cube->bdl = rotate_corner(cube->blu);
	cube->blu = rotate_corner_(temp_corner);

	temp_edge = cube->fl;
	cube->fl = cube->dl;
	cube->dl = cube->bl;
	cube->bl = cube->ul;
	cube->ul = temp_edge;
}

/**
 * Rotate up face clockwise.
 */
void move_U(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->ful;
	cube->ful = rotate_corner_(cube->fru);
	cube->fru = rotate_corner(cube->bur);
	cube->bur = rotate_corner_(cube->blu);
	cube->blu = rotate_corner(temp_corner);

	temp_edge = cube->fu;
	cube->fu = flip_edge(cube->ur);
	cube->ur = flip_edge(cube->bu);
	cube->bu = flip_edge(cube->ul);
	cube->ul = flip_edge(temp_edge);
}

/**
 * Rotate up face counterclockwise.
 */
void move_U_(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->ful;
	cube->ful = rotate_corner_(cube->blu);
	cube->blu = rotate_corner(cube->bur);
	cube->bur = rotate_corner_(cube->fru);
	cube->fru = rotate_corner(temp_corner);

	temp_edge = cube->fu;
	cube->fu = flip_edge(cube->ul);
	cube->ul = flip_edge(cube->bu);
	cube->bu = flip_edge(cube->ur);
	cube->ur = flip_edge(temp_edge);
}

/**
 * Rotate down face clockwise.
 */
void move_D(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->fld;
	cube->fld = rotate_corner(cube->bdl);
	cube->bdl = rotate_corner_(cube->brd);
	cube->brd = rotate_corner(cube->fdr);
	cube->fdr = rotate_corner_(temp_corner);

	temp_edge = cube->fd;
	cube->fd = flip_edge(cube->dl);
	cube->dl = flip_edge(cube->bd);
	cube->bd = flip_edge(cube->dr);
	cube->dr = flip_edge(temp_edge);
}

/**
 * Rotate down face counterclockwise.
 */
void move_D_(struct Cube *cube) {
	corner_t temp_corner;
	edge_t temp_edge;

	temp_corner = cube->fld;
	cube->fld = rotate_corner(cube->fdr);
	cube->fdr = rotate_corner_(cube->brd);
	cube->brd = rotate_corner(cube->bdl);
	cube->bdl = rotate_corner_(temp_corner);

	temp_edge = cube->fd;
	cube->fd = flip_edge(cube->dr);
	cube->dr = flip_edge(cube->bd);
	cube->bd = flip_edge(cube->dl);
	cube->dl = flip_edge(temp_edge);
}

/**
 * Rotate middle layer following L.
 */
void move_M(struct Cube *cube) {
	center_t temp_center;
	edge_t temp_edge;

	temp_center = cube->f;
	cube->f = cube->u;
	cube->u = cube->b;
	cube->b = cube->d;
	cube->d = temp_center;

	temp_edge = cube->fu;
	cube->fu = flip_edge(cube->bu);
	cube->bu = flip_edge(cube->bd);
	cube->bd = flip_edge(cube->fd);
	cube->fd = flip_edge(temp_edge);
}

/**
 * Rotate middle layer following R.
 */
void move_M_(struct Cube *cube) {
	center_t temp_center;
	edge_t temp_edge;

	temp_center = cube->f;
	cube->f = cube->d;
	cube->d = cube->b;
	cube->b = cube->u;
	cube->u = temp_center;

	temp_edge = cube->fu;
	cube->fu = flip_edge(cube->fd);
	cube->fd = flip_edge(cube->bd);
	cube->bd = flip_edge(cube->bu);
	cube->bu = flip_edge(temp_edge);
}

/**
 * Rotate middle layer following D.
 */
void move_E(struct Cube *cube) {
	center_t temp_center;
	edge_t temp_edge;

	temp_center = cube->f;
	cube->f = cube->l;
	cube->l = cube->b;
	cube->b = cube->r;
	cube->r = temp_center;

	temp_edge = cube->fr;
	cube->fr = flip_edge(cube->fl);
	cube->fl = flip_edge(cube->bl);
	cube->bl = flip_edge(cube->br);
	cube->br = flip_edge(temp_edge);
}

/**
 * Rotate middle layer following U.
 */
void move_E_(struct Cube *cube) {
	center_t temp_center;
	edge_t temp_edge;

	temp_center = cube->f;
	cube->f = cube->r;
	cube->r = cube->b;
	cube->b = cube->l;
	cube->l = temp_center;

	temp_edge = cube->fr;
	cube->fr = flip_edge(cube->br);
	cube->br = flip_edge(cube->bl);
	cube->bl = flip_edge(cube->fl);
	cube->fl = flip_edge(temp_edge);
}

/**
 * Rotate middle layer following F.
 */
void move_S(struct Cube *cube) {
	center_t temp_center;
	edge_t temp_edge;

	temp_center = cube->u;
	cube->u = cube->l;
	cube->l = cube->d;
	cube->d = cube->r;
	cube->r = temp_center;

	temp_edge = cube->ur;
	cube->ur = flip_edge(cube->ul);
	cube->ul = flip_edge(cube->dl);
	cube->dl = flip_edge(cube->dr);
	cube->dr = flip_edge(temp_edge);
}

/**
 * Rotate middle layer following B.
 */
void move_S_(struct Cube *cube) {
	center_t temp_center;
	edge_t temp_edge;

	temp_center = cube->u;
	cube->u = cube->r;
	cube->r = cube->d;
	cube->d = cube->l;
	cube->l = temp_center;

	temp_edge = cube->ur;
	cube->ur = flip_edge(cube->dr);
	cube->dr = flip_edge(cube->dl);
	cube->dl = flip_edge(cube->ul);
	cube->ul = flip_edge(temp_edge);
}

/**
 * Rotate cube following R.
 */
void move_x(struct Cube *cube) {
	move_L_(cube);
	move_M_(cube);
	move_R(cube);
}

/**
 * Rotate cube following L.
 */
void move_x_(struct Cube *cube) {
	move_L(cube);
	move_M(cube);
	move_R_(cube);
}

/**
 * Rotate cube following U.
 */
void move_y(struct Cube *cube) {
	move_U(cube);
	move_E_(cube);
	move_D_(cube);
}

/**
 * Rotate cube following D.
 */
void move_y_(struct Cube *cube) {
	move_U_(cube);
	move_E(cube);
	move_D(cube);
}

/**
 * Rotate cube following F.
 */
void move_z(struct Cube *cube) {
	move_F(cube);
	move_S(cube);
	move_B_(cube);
}

/**
 * Rotate cube following B.
 */
void move_z_(struct Cube *cube) {
	move_F_(cube);
	move_S_(cube);
	move_B(cube);
}

/**
 * Print out the cube in the following format:
 *
 *            u  u  u
 *            u  u  u
 *            u  u  u
 *
 *  l  l  l   f  f  f   r  r  r
 *  l  l  l   f  f  f   r  r  r
 *  l  l  l   f  f  f   r  r  r
 *
 *            d  d  d
 *            d  d  d
 *            d  d  d
 *
 *            b  b  b
 *            b  b  b
 *            b  b  b
 */
void print_cube(struct Cube cube) {
	/* u u u */
	printf("           %2i %2i %2i\n",
			corner_right(cube.blu), edge_right(cube.bu), corner_left(cube.bur));

	/* u u u */
	printf("           %2i %2i %2i\n",
			edge_left(cube.ul), (face_t)cube.u, edge_left(cube.ur));

	/* u u u */
	printf("           %2i %2i %2i\n",
			corner_left(cube.ful), edge_right(cube.fu), corner_right(cube.fru));

	printf("\n");

	/* l l l  u u u  f f f*/
	printf("%2i %2i %2i   %2i %2i %2i   %2i %2i %2i\n",
			corner_left(cube.blu), edge_right(cube.ul), corner_right(cube.ful),
			corner_top(cube.ful), edge_left(cube.fu), corner_top(cube.fru),
			corner_left(cube.fru), edge_right(cube.ur), corner_right(cube.bur));

	/* l l l  u u u  f f f*/
	printf("%2i %2i %2i   %2i %2i %2i   %2i %2i %2i\n",
			edge_right(cube.bl), (face_t)cube.l, edge_right(cube.fl),
			edge_left(cube.fl), (face_t)cube.f, edge_left(cube.fr),
			edge_right(cube.fr), (face_t)cube.r, edge_right(cube.br));

	/* l l l  u u u  f f f*/
	printf("%2i %2i %2i   %2i %2i %2i   %2i %2i %2i\n",
			corner_right(cube.bdl), edge_right(cube.dl), corner_left(cube.fld),
			corner_top(cube.fld), edge_left(cube.fd), corner_top(cube.fdr),
			corner_right(cube.fdr), edge_right(cube.dr), corner_left(cube.brd));

	printf("\n");

	/* d d d */
	printf("           %2i %2i %2i\n",
			corner_right(cube.fld), edge_right(cube.fd), corner_left(cube.fdr));

	/* d d d */
	printf("           %2i %2i %2i\n",
			edge_left(cube.dl), (face_t)cube.d, edge_left(cube.dr));

	/* d d d */
	printf("           %2i %2i %2i\n",
			corner_left(cube.bdl), edge_right(cube.bd), corner_right(cube.brd));

	printf("\n");

	/* b b b */
	printf("           %2i %2i %2i\n",
			corner_top(cube.bdl), edge_left(cube.bd), corner_top(cube.brd));

	/* b b b */
	printf("           %2i %2i %2i\n",
			edge_left(cube.bl), (face_t)cube.b, edge_left(cube.br));

	/* b b b */
	printf("           %2i %2i %2i\n",
			corner_top(cube.blu), edge_left(cube.bu), corner_top(cube.bur));
}

#define NIBBLE_SIZE 4
#define NIBBLE_MASK ((1 << NIBBLE_SIZE) - 1)
#define NIBBLE(input, i) ((input[i / 2] >> NIBBLE_SIZE * (1 - i % 2)) \
		& NIBBLE_MASK)
/**
 * Build a cube from a string of length
 * `FACE_CT / 2` from its nibbles in this order:
 *
 *           18 19 20
 *           21 22 23
 *           24 25 26
 *
 * 27 28 29  00 01 02  09 10 11
 * 30 31 32  03 04 05  12 13 14
 * 33 34 35  06 07 08  15 16 17
 *
 *           36 37 38
 *           39 40 41
 *           42 43 44
 *
 *           45 46 47
 *           48 49 50
 *           51 52 53
 */
void build_cube_from_string(struct Cube *cube, const char *input) {
	cube->ful = corner(
			NIBBLE(input, 0),
			NIBBLE(input, 24),
			NIBBLE(input, 29)
			);
	cube->fru = corner(
			NIBBLE(input, 2),
			NIBBLE(input, 9),
			NIBBLE(input, 26)
			);
	cube->fld = corner(
			NIBBLE(input, 6),
			NIBBLE(input, 35),
			NIBBLE(input, 36)
			);
	cube->fdr = corner(
			NIBBLE(input, 8),
			NIBBLE(input, 38),
			NIBBLE(input, 15)
			);

	cube->blu = corner(
			NIBBLE(input, 51),
			NIBBLE(input, 27),
			NIBBLE(input, 18)
			);
	cube->bur = corner(
			NIBBLE(input, 53),
			NIBBLE(input, 20),
			NIBBLE(input, 11)
			);
	cube->bdl = corner(
			NIBBLE(input, 45),
			NIBBLE(input, 42),
			NIBBLE(input, 33)
			);
	cube->brd = corner(
			NIBBLE(input, 47),
			NIBBLE(input, 17),
			NIBBLE(input, 44)
			);

	cube->fu = edge(
			NIBBLE(input, 1),
			NIBBLE(input, 25)
			);
	cube->fr = edge(
			NIBBLE(input, 5),
			NIBBLE(input, 12)
			);
	cube->fd = edge(
			NIBBLE(input, 7),
			NIBBLE(input, 37)
			);
	cube->fl = edge(
			NIBBLE(input, 3),
			NIBBLE(input, 32)
			);

	cube->bu = edge(
			NIBBLE(input, 52),
			NIBBLE(input, 19)
			);
	cube->br = edge(
			NIBBLE(input, 50),
			NIBBLE(input, 14)
			);
	cube->bd = edge(
			NIBBLE(input, 46),
			NIBBLE(input, 43)
			);
	cube->bl = edge(
			NIBBLE(input, 48),
			NIBBLE(input, 30)
			);

	cube->ur = edge(
			NIBBLE(input, 23),
			NIBBLE(input, 10)
			);
	cube->ul = edge(
			NIBBLE(input, 21),
			NIBBLE(input, 28)
			);
	cube->dr = edge(
			NIBBLE(input, 41),
			NIBBLE(input, 16)
			);
	cube->dl = edge(
			NIBBLE(input, 39),
			NIBBLE(input, 34)
			);

	cube->f = NIBBLE(input, 4);
	cube->r = NIBBLE(input, 13);
	cube->u = NIBBLE(input, 22);
	cube->l = NIBBLE(input, 31);
	cube->d = NIBBLE(input, 40);
	cube->b = NIBBLE(input, 49);
}

void set_nibble(unsigned char *bytes, const size_t i, const uint8_t nibble) {
	bytes[i / 2] &= (NIBBLE_MASK << (NIBBLE_SIZE * (i % 2)));
	bytes[i / 2] |= nibble << (NIBBLE_SIZE * (1 - i % 2));

}

void extract_bytes_from_front(
		const struct Cube cube,
		unsigned  char *output,
		const size_t base
		) {
	set_nibble(output, base + 0, corner_top(cube.ful));
	set_nibble(output, base + 1, edge_left(cube.fu));
	set_nibble(output, base + 2, corner_top(cube.fru));

	set_nibble(output, base + 3, edge_left(cube.fl));
	set_nibble(output, base + 4, (face_t)cube.f);
	set_nibble(output, base + 5, edge_left(cube.fr));

	set_nibble(output, base + 6, corner_top(cube.fld));
	set_nibble(output, base + 7, edge_left(cube.fd));
	set_nibble(output, base + 8, corner_top(cube.fdr));
}

void extract_bytes_from_cube(struct Cube cube, unsigned char *output) {
	/* front */
	extract_bytes_from_front(cube, output, 9 * 0);
	move_y(&cube);
	/* right */
	extract_bytes_from_front(cube, output, 9 * 1);
	move_y_(&cube);
	move_x_(&cube);
	/* up */
	extract_bytes_from_front(cube, output, 9 * 2);
	move_x(&cube);
	move_y_(&cube);
	/* left */
	extract_bytes_from_front(cube, output, 9 * 3);
	move_y(&cube);
	move_x(&cube);
	/* down */
	extract_bytes_from_front(cube, output, 9 * 4);
	move_x(&cube);
	/* back */
	extract_bytes_from_front(cube, output, 9 * 5);
}

/**
 * Execute an algorithm.
 */
void execute_algorithm(struct Cube *cube, const char *str) {
	size_t i;

	void (*F[])(struct Cube*) = {
		move_F, move_F_,
	};

	void (*R[])(struct Cube*) = {
		move_R, move_R_,
	};

	void (*L[])(struct Cube*) = {
		move_L, move_L_,
	};

	void (*U[])(struct Cube*) = {
		move_U, move_U_,
	};

	void (*D[])(struct Cube*) = {
		move_D, move_D_,
	};

	void (*B[])(struct Cube*) = {
		move_B, move_B_,
	};

	void (*M[])(struct Cube*) = {
		move_M, move_M_,
	};

	void (*E[])(struct Cube*) = {
		move_E, move_E_,
	};

	void (*S[])(struct Cube*) = {
		move_S, move_S_,
	};

	void (*x[])(struct Cube*) = {
		move_x, move_x_,
	};

	void (*y[])(struct Cube*) = {
		move_y, move_y_,
	};

	void (*z[])(struct Cube*) = {
		move_z, move_z_,
	};

	const size_t len = strlen(str);
	for (i = 0; i < len; i++) {
		const int inverse = str[i + 1] == '\'' ? 1 : 0;
		switch (str[i]) {
			case 'F':
				F[inverse](cube);
				break;
			case 'R':
				R[inverse](cube);
				break;
			case 'L':
				L[inverse](cube);
				break;
			case 'U':
				U[inverse](cube);
				break;
			case 'D':
				D[inverse](cube);
				break;
			case 'B':
				B[inverse](cube);
				break;
			case 'M':
				M[inverse](cube);
				break;
			case 'E':
				E[inverse](cube);
				break;
			case 'S':
				S[inverse](cube);
				break;
			case 'x':
				x[inverse](cube);
				break;
			case 'y':
				y[inverse](cube);
				break;
			case 'z':
				z[inverse](cube);
				break;

			default:
				printf("[WARN] unrecognized move: %c\n", str[i]);
				break;
		}

		/* skip the inverse character if present */
		i += inverse;
	}
}

char *get_flag() {
		char *flag = calloc(FACE_CT / 2 + 1, sizeof(char));
    FILE *file;
    file = fopen("flag.txt", "r");
    if (file == NULL) {
    	perror("failed to open flag.txt for reading");
    	exit(1);
    }
    fread(flag, FACE_CT / 2, 1, file);
    fclose(file);
    return flag;
}

char *get_algorithm() {
		char *algorithm = calloc(ALGORITHM_LENGTH + 1, sizeof(char));
    FILE *file;
    file = fopen("algorithm.txt", "r");
    if (file == NULL) {
    	perror("failed to open algorithm.txt for reading");
    	exit(1);
    }
    fread(algorithm, sizeof(char), ALGORITHM_LENGTH, file);
    fclose(file);
    return algorithm;
}

/**
 * Cube Cipher implementation
 */
int main() {
	size_t i;
	struct Cube *cube = calloc(1, sizeof(struct Cube));
	char *flag = get_flag();
	char *scramble_algorithm = get_algorithm();
	unsigned char *output = calloc(FACE_CT, sizeof(unsigned char));
	int option;
	char algorithm_str[256];

	setvbuf(stdout, 0, 2, 0);

	build_cube_from_string(cube, flag);
	free(flag);
	execute_algorithm(cube, scramble_algorithm);

	printf("Welcome to the Interactive Cube Cipher App!\n"
			"Try and break my cipher! (you can't)\n"
			"Options:\n"
			"\t1: Execute an algorithm\n"
			"\t2: Display cube\n"
			"\t3: Display cube as bytes\n"
			"\t4: Re-apply cube cipher\n"
			"\t5: Exit\n"
			);

	option = 0;
	while (option != 5) {
get_option:
		printf("Option: ");
		if (scanf("%d", &option) != 1) {
			while (getchar() != '\n');
			printf("Please enter an integer.\n");
			goto get_option;
		}
		switch (option) {
			case 1:
				printf("Enter your algorithm:\n> ");
				scanf("%255s", algorithm_str);
				execute_algorithm(cube, algorithm_str);
				break;
			case 2:
				print_cube(*cube);
				break;
			case 3:
				extract_bytes_from_cube(*cube, output);
				for (i = 0; i < FACE_CT / 2; i++) {
					printf("%02x", output[i]);
				}
				printf("\n");
				break;
			case 4:
				printf("Scrambling...\n");
				execute_algorithm(cube, scramble_algorithm);
				break;
			case 5:
				printf("Goodbye!\n");
				break;
			default:
				printf("Invalid option.\n");
		}
	}

	free(output);
	free(cube);
	free(scramble_algorithm);
	return 0;
}

