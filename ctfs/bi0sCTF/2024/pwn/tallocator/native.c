#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
#include <jni.h>
#include <math.h>

#define x 4
#define y 1.0e-5

float v6[4][4] = {
        {0.058767, 0.001944, -0.011339, -0.032914},
        {-0.005842, 0.045599, -0.035272, -0.002990},
        {0.664623, 0.054662, 0.089370, -0.872437},
        {-0.674525, -0.097455, -0.040884, 0.875243}
};

void func_1(float a1[4][4],char s[] ){
    int cnt = 0;
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            a1[i][j] = (float)s[cnt++];
        }
    }

}

float func_2(int a1, int a2, float a3[a1][a2])
{
    if (a1 != a2) {
        return 0;
    }

    float v1 = 0;

    if (a1 == 1) {
        v1 = a3[0][0];
    } else {
        for (int i = 0; i < a1; i++) {
            float v2[a1 - 1][a2 - 1];
            for (int j = 1; j < a1; j++) {
                for (int k = 0; k < i; k++) {
                    v2[j - 1][k] = a3[j][k];
                }
                for (int k = i + 1; k < a2; k++) {
                    v2[j - 1][k - 1] = a3[j][k];
                }
            }
            int v3 = (i % 2 == 0) ? 1 : -1;
            v1 += v3 * a3[0][i] * func_2(a1 - 1, a2 - 1, v2);
        }
    }

    return v1;
}


void func_3(int a1, float a2[a1][a1], float a3[a1][a1])
{
    float v1[a1 - 1][a1 - 1];

    for (int i = 0; i < a1; i++)
    {
        for (int j = 0; j < a1; j++)
        {
            int sub_i = 0, sub_j = 0;

            for (int v2 = 0; v2 < a1; v2++)
            {
                if (v2 == i)
                    continue;
                for (int v3 = 0; v3 < a1; v3++)
                {
                    if (v3 == j)
                        continue;

                    v1[sub_i][sub_j] = a2[v2][v3];
                    sub_j++;
                }

                sub_i++;
                sub_j = 0;
            }

            int v4 = (i + j) % 2 == 0 ? 1 : -1;
            a3[i][j] = v4 * func_2(a1 - 1, a1 - 1, v1);
        }
    }
}



void func_4(int a1, int a2, float a3[a1][a2], float a4[a2][a1])
{
    for (int i = 0; i < a1; i++)
    {
        for (int j = 0; j < a2; j++)
        {
            a4[j][i] = a3[i][j];
        }
    }
}


void func_5(int a1, float a2[a1][a1], float a3[a1][a1], int a4, float a5[a1][a1])
{

    for (int i = 0; i < a1; i++)
    {
        for (int j = 0; j < a1; j++)
        {
            a3[i][j] = (float) (a5[j][i] / a4);
        }
    }
}



int func_6(float a1[x][x], float a2[x][x])
{
    int i, j;
    for (i = 0; i < x; i++) {
        for (j = 0; j < x; j++) {
            if (isnan(a1[i][j]) || isnan(a2[i][j]) || isinf(a1[i][j]) || isinf(a2[i][j])) {
                return 0;
            }

            float v1 = a1[i][j], v2 = a2[i][j];
            float v3 = fabsl(v1 - v2);
            if (v3 > y) {
                return 0;
            }
        }
    }
    return 1;
}


void func_7(float a1[x][x], float a2[x][x])
{
    int i, j;
    for (i = 0; i < x; i++) {
        for (j = 0; j < x; j++) {
            a2[i][j] = a1[i][j];
        }
    }
}

JNIEXPORT jboolean JNICALL Java_bi0sctf_android_challenge_a_check(JNIEnv* env,jobject thiz,jstring str){
    char* buf = (*env)->GetStringUTFChars(env, str, NULL);

    char st[16];
    for(int i=0;i<16;i++){
        st[i] = (char)buf[i];
    }

    float v1[4][4];
    func_1(v1,st);

    float v2[4][4];
    func_7(v1, v2);

    float v3 = func_2(x, x, v1);
    float v4[x][x];

    func_3(x, v1, v4);
    func_4(x, x, v4, v1);

    float v5[x][x];
    func_5(x, v1, v5, v3, v4);

    int r1 = func_6(v5, v6);

    if(r1 == 1){
        return JNI_TRUE;
    }else{
        return JNI_FALSE;
    }
}