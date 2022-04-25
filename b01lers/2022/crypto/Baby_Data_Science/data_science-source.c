#include <stdio.h>
#include <stdlib.h>
#include <math.h>


double myrand() {
   unsigned int v;
   FILE* f = fopen("/dev/urandom", "r");
   fread(&v, 1, 4, f);
   fclose(f);
   unsigned int MAX = ~(0U);
   return v / (double) MAX;
}


double compute(double a, double b, double A, double B, double C) {

   const int N = 1000;
   double x[N + 1];
   double y[N + 1];
   for (int i = 0; i <= N; i ++) {
      x[i] = a + i * (b - a) / N;
      y[i] = A * x[i] * x[i] + B * x[i] + C;
   }


   double xlo = (-B + sqrt(B * B - 4. * A * C)) / (2. * A);
   double xhi = (-B - sqrt(B * B - 4. * A * C)) / (2. * A);
   double xmid = (xlo + xhi) * 0.5;
   for (int i = 0; i <= N; i ++) {
      if (x[i] >= xlo && x[i] <= xmid) y[i] = sqrt(y[i]);
   }


   int kmax = -1, imax = -1;
   double ymax = 0.;
   for (int i = 0; i <= N; i ++) {
      if (y[i] > ymax) {
         ymax = y[i];
         kmax = (ymax - a) * N / (b - a);
         imax = i;
      }
   }
   int k0 = kmax;
   for (int i = imax; i >= 0; i --) {
      if (y[i] > 0.) continue;
      k0 = (y[i] - a) * N / (b - a);
      break;
   }


   double s = 0.;
   int kprev = kmax;
   for (int i = 0; i <= N; i ++) {
      if (x[i] > xmid) continue;
      int k = (y[i] - a) * N / (b - a);
      if (k < k0) continue;
      if (k > kmax) continue;
      if (k == kprev) continue;
      kprev = k;
      s += x[i] - xlo;
   }
   s *= (b - a) / N;

   return s;
}



int main(int ARGC, const char** const ARGV) {



   double tolerance = (ARGC > 1) ? atof(ARGV[1]) : 0.;

   printf("== Data Science Academy, Tolerance Level %.17g ==\n\n", tolerance);



   double A = -1. - myrand(); 
   double B = 2.0 * myrand() - 1.0;
   B += (B > 0.) ? 2. : -2.;
   double C = 0.4 + 3.0 * myrand();

   printf("curve parameters:\n");
   printf("  A=%.17g\n", A);
   printf("  B=%.17g\n", B);
   printf("  C=%.17g\n\n", C);



   printf("pick your range [a,b]: ");
   fflush(stdout);

   double a, b;
   scanf("%24lf,%24lf", &a, &b);
   printf("a=%.17g b=%.17g\n", a, b);



   const double MAXab = 4e2;
   if (b > a && fabs(a) < MAXab && fabs(b) < MAXab) {
      double s = compute(a, b, A, B, C);
      printf("\nresult= %.17g\n", s);

      double sgoal = -M_PI;
      if (fabs(s - sgoal) > tolerance) printf("=> NO CIGAR :(, try harder...\n");
      else {
         FILE* f = fopen("./flag.txt", "r");
         char buf[256];
         fread(buf, 256, 1, f);
         fclose(f);
         if (s == sgoal) printf("=> THAT'S IT! Here is the flag: %s\n", buf);
         else printf("=> GOOD ENOUGH. Here is the flag: %s\n", buf);
      }     
   }
   else printf("invalid input\n");


   fflush(stdout);
   return 0;
}
