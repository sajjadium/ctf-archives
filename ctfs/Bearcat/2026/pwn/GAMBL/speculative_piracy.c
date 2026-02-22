#include <stdio.h>
#include <stdlib.h>

#define MAX(a,b) a > b ? a : b

float money = 100.0;
float investedMoney = 0.0;
float moneyBet = 0.0;
int betOn = 0;
int values[5] = {5, 2, 10, 8, 13}; // I got these values from my ultimate predictive powers

int isWinning(int value) {
	for (int i = 0; i < 5; i++) {
		if ( values[i] == value )
			return 1;
	}
	return 0;
}

void printFlag() {
	FILE *fptr = fopen("flag.txt", "r");
	if (fptr == NULL) {
		printf("Unable to open flag.txt\n");
		exit(1);
	}

	char buffer[50];
	while (fgets(buffer,sizeof(buffer),fptr) != NULL) {
		printf("%s", buffer);
	}

	fclose(fptr);
	exit(0);
}

void mainMenu(int day, int *n) {
	printf("\nIt is day %d and you have %.2f dollars\nHow would you like GAMBL today?\n1) Place a bet\n2) Invest in crypto\n3) Complete day\n4) Buy Flag\n5) Quit\n > ", day, money);
	scanf("%d", n);
}

void gamble() {
	printf("\nWhich piracy group would you like to bet on?\n1) DataBucaneer\n2) LogicGate Rogue\n3) BlackFlag Binary\n4) OpenSource Insurgency\n5) ONYX\n > ");
	scanf("%d", &betOn);

	if ( betOn > 5 || betOn < 1 ) {
		betOn = 0;
		return;
	}

	printf("\nHow much would you like to bet?\n > ");
	scanf("%f", &moneyBet);

	if ( moneyBet > money ) {
		printf("\nYou don't have enough money to bet that much! And you can't go into debt either.\n");
	} else if ( moneyBet < 0.0 ) {
		printf("\nYou can't gamble negative money!\n");
		exit(0);
	} else {
		money -= moneyBet;
	}
}

void investCrypto() {
	float investmentAmount;
	printf("How much of your $%.2f would you like to invest in $GAMBL coin? You will get your investments back the next day along with the profits you made, because these coins only go up!\n Enter your investment amount > ", money);
	scanf("%f", &investmentAmount);

	if (investmentAmount < 0.0) {
		printf("\nYou can't invest negative money!\n");
		exit(0);
	} else if (investmentAmount > money) {
		// Sometimes this fails when I try and invest all my money?? I'll ask chat later
		printf("You don't have that much money!\n");
	} else {
		investedMoney = investmentAmount;
		money -= investmentAmount;
	}
}

int main() {

	int day = 1;
	int i = 1;
	int choice = 0;
	int continueDay;
	float dayStartMoney;
	float gamblingLosses = 0.0;

	while (i <= 15) {

		dayStartMoney = money;
		continueDay = 1;
		betOn = 0;

		while (continueDay) {
			mainMenu(day, &choice);

			switch(choice) {
				case 1:
					if ( betOn ) {
						printf("Sorry, you only get one bet per day. I'm too lazy to implement more than that");
					} else {
						gamble();
					}
					break;
				case 2: // Crypto always pays out
					investCrypto();
					break;
				case 3:
					continueDay = 0;
					break;
				case 4:
					if ( money >= 5000000.0) {
						printFlag();
					} else {
						printf("\nSorry, your measly %.2f is not enough money\n", money);
					}
					break;
				default:
					exit(0);

			}
		}

		if ( betOn && isWinning(day) ) {
			money += moneyBet * 2;
		}
		betOn = 0;
		moneyBet = 0.0;

		day++;
		i++;

		if ((money + investedMoney) / dayStartMoney < .75) {
			printf("\nUh oh, it looks like you had a bad day on the grind. Since not everyone is as clairvoyant as me, you can try again.\n");
			day--;
			money = dayStartMoney;
			investedMoney = 0.0;
			if ( MAX(0, --i) == 0 ) {
				i++; day++;
				continue;
			}
		}

		float investmentMultiplier = ((rand() % 16) + 44) / 100.0 + 1;
		money += investedMoney * investmentMultiplier;
		investedMoney = 0.0;
	}
}
