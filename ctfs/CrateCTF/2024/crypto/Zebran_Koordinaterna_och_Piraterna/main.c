#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <gmp.h>
#include <unistd.h>

int current_time_in_seconds() {
    struct timespec spec;
    clock_gettime(CLOCK_REALTIME, &spec);
    int seconds = spec.tv_sec;
    return seconds;
}

void welcome(mpz_t g, mpz_t p, mpz_t y) {
	char dummy[2];

    printf("  .  ,\n");
    printf("  |\\/|\n");
    printf("  bd \"n.\n");
    printf(" /   _,\"n.___.,--x.\n");
    printf("''\\             Y\n");
    printf(" ~~   \\       L   7|\n");
    printf("       H l--'~\\\\ (||\n");
    printf("       H l     H |`'    -Row (Rowan Crawford)\n");
    printf("       H [     H [\n");
    printf("  ____//,]____//,]___\n\n");
    
	printf("Prove to me that you know the coordinates of the Zebra!\n\n");
	gmp_printf("Public Modulus p: %Zd\n"
             "Public Secret y: %Zd\n"
             "Public Generator g: %Zd\n", p, y, g);
	printf("The time was %d seconds past the beginning of the epoch... Ready? [Enter]", current_time_in_seconds());
	fgets(dummy, 2, stdin);
}
void getC(mpz_t c) {
	char *cStr = malloc(1000);
	printf("Give me the result of your computation (C): ");
	fgets(cStr, 1000, stdin);
	mpz_init_set_str(c, cStr, 10);
	free(cStr);
}

int issueChallenge(mpz_t response) {
	char *responseStr = malloc(1000);
	int choice = rand() % 2;
	if (choice) {
		printf("Send me r: ");
	} else {
		printf("Send me (x + r) \% (p - 1): ");
	}
	fgets(responseStr, 1000, stdin);

	mpz_init_set_str(response, responseStr, 10);
	free(responseStr);
	return choice;
}
int verifyResponse(mpz_t g, mpz_t p, mpz_t y, mpz_t c, mpz_t response, int choice) {
	mpz_t pow_res;
	mpz_t second_choice_res;
	int res;

	mpz_init(pow_res);
	mpz_powm(pow_res, g, response, p);
	if (choice) {
		res = mpz_cmp(pow_res, c);
	} else {
		mpz_init(second_choice_res);
		mpz_mul(second_choice_res, c, y);
		mpz_mod(second_choice_res, second_choice_res, p);
		res = mpz_cmp(pow_res, second_choice_res);
		mpz_clear(second_choice_res);

	}
  	mpz_clear(pow_res);
	return res;
}

int main(int argc, char **argv) {
	mpz_t g, p, y, c, response;
	int choice, isValid;
	char dummy[3];

	setvbuf(stdout, NULL, _IONBF, 1024);

    sleep(1);

	mpz_init_set_str(g, "2", 10);
	mpz_init_set_str(p, "130851816140806784262465187424384020255180865248723176579787523852687726893618398440363884994211452030261229010683886003183000989818745801599611634888374505658697250332748967647230720292304149162739917789497819202548690478815982097197719984621922523995560643717675225042321120446320674624889924956904284110187", 10);
  	mpz_init_set_str(y, "105303443565077642507717682127429060264676643000017980456127179564353567623961870270506367886821692819989112839349292109605044903240124246391803056494350035248269936075820558428447318109525031341523952584957439977065121740824526153326758170083963963616633068416400339426575891236621067467740725444592115561502", 10);
	mpz_init(c);
  	mpz_init(response);

	welcome(g,p,y);
	srand(current_time_in_seconds());
	for (int i = 0; i < 100; i++) {
		getC(c);
		choice = issueChallenge(response);
		isValid = verifyResponse(g, p, y, c, response, choice);
		if (isValid != 0) {
			printf("Those coordinates do not check out! No deal.");
		  	mpz_clear(g);
  			mpz_clear(p);
		  	mpz_clear(y);
		  	mpz_clear(c);
		  	mpz_clear(response);

			return 0;
		}
	}
	printf("You have proved that you have the coordinates to a zebra, here is the gold.\n");
	printf("cratectf{FAKEFLAG}");

	mpz_clear(g);
	mpz_clear(p);
	mpz_clear(y);
	mpz_clear(c);
	mpz_clear(response);
	return 0;
}
