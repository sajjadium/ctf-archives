#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/random.h>

int main() {

    // Use the slow Linux cryptographically secure rng to seed the faster insecure rng
    unsigned int seed_val = 0;
    int ret = getrandom((void*)&seed_val, 4, GRND_RANDOM);

    if(ret == -1){
        printf("Contact SwampCTF organizers there is an issue with this challenge.\nExiting....\n");
        exit(1);
    }

    // Seed the rng
    srand(seed_val);

    int equ0[5] = {0};
    int equ1[5] = {0};
    int equ2[5] = {0};
    int equ3[5] = {0};
    int equ4[5] = {0};
    int solution[5] = {0};
    int result[5] = {0};
    int submission[5] = {0};

    for(int i = 0; i < 5; i++){
        // Generate the coefficients of the linear equations (provided to stdout)
        equ0[i] = rand() % 10000;
        equ1[i] = rand() % 10000;
        equ2[i] = rand() % 10000;
        equ3[i] = rand() % 10000;
        equ4[i] = rand() % 10000;

        // Generate the solution set (hidden)
        solution[i] = rand() % 10000;
    }

    // Calculate the results of all the linear equations (provided to stdout)
    for(int i = 0; i < 5; i++){
        result[0] += equ0[i]*solution[i];
        result[1] += equ1[i]*solution[i];
        result[2] += equ2[i]*solution[i];
        result[3] += equ3[i]*solution[i];
        result[4] += equ4[i]*solution[i];
    }


    //printf("Solution set = %d %d %d %d %d\n", solution[0], solution[1], solution[2], solution[3], solution[4]);

    printf("Quick! These set of linear equations describe the secretes to time travel!\n"
           "But the quantum state of the universe only gives us 10 mere seconds to solve them!!!\n\n");

    printf("%d*a + %d*b + %d*c + %d*d + %d*e = %d\n", equ0[0],equ0[1],equ0[2],equ0[3],equ0[4],result[0]);
    printf("%d*a + %d*b + %d*c + %d*d + %d*e = %d\n", equ1[0],equ1[1],equ1[2],equ1[3],equ1[4],result[1]);
    printf("%d*a + %d*b + %d*c + %d*d + %d*e = %d\n", equ2[0],equ2[1],equ2[2],equ2[3],equ2[4],result[2]);
    printf("%d*a + %d*b + %d*c + %d*d + %d*e = %d\n", equ3[0],equ3[1],equ3[2],equ3[3],equ3[4],result[3]);
    printf("%d*a + %d*b + %d*c + %d*d + %d*e = %d\n", equ4[0],equ4[1],equ4[2],equ4[3],equ4[4],result[4]);

    unsigned long time_start = time(0);

    printf("a = ");
    scanf("%d", &submission[0]);

    printf("b = ");
    scanf("%d", &submission[1]);

    printf("c = ");
    scanf("%d", &submission[2]);

    printf("d = ");
    scanf("%d", &submission[3]);

    printf("e = ");
    scanf("%d", &submission[4]);

    // Fail if it takes longer then 10 seconds to solve the system
    if((time(0) - time_start) >= 10){
        printf("Aaaah we didn't solve the system fast enough!\n");
        exit(1);
    }

    // Fail if one of variables is incorrect
    for(int i = 0; i < 5; i++){
        if(solution[i] != submission[i]) {
            printf("AAaaahhh the time jump failed!!! The solution set must have been wrong!!\n");
            exit(1);
        }
    }

    printf("We did it! We have traveled through time! Here is the flag: \n");

    return 0;
}