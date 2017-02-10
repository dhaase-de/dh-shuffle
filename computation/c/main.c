#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
   /* declarations */
   unsigned int N_start;
   unsigned int N_end;
   unsigned int N_diff;
   unsigned int N;
   char* format = "%d %d \n";

   /* get input number settings from command line */
   switch (argc) {
      /* one argument: single number */
      case 2:
         N_start = (unsigned int)atoi(argv[1]);
         N_end = N_start;
         N_diff = 1;
      break;
      
      /* two arguments: range */
      case 3:
         N_start = (unsigned int)atoi(argv[1]);
         N_end = (unsigned int)atoi(argv[2]);
         N_diff = 1;
      break;
      
      /* three arguments: range and diff */
      case 4:
         N_start = (unsigned int)atoi(argv[1]);
         N_end = (unsigned int)atoi(argv[2]);
         N_diff = (unsigned int)atoi(argv[3]);
      break;
      
      default:
         return 0;
      break;
   }
   
   /* main loop */
   for (N = N_start; N <= N_end; N += N_diff) {
      /* init shuffle procedure for input number N */
      unsigned int k = 0;
      unsigned int n = 1;
      unsigned int twoNPlusOne = 2 * N + 1;
      
      /* shuffle loop */
      do {
         k++;
         if (n <= N) {
            n *= 2;
         } else {
            n = 2 * n - twoNPlusOne;
         }
      } while (n != 1);

      printf(format, N, k);
   }

   return 0;
}
