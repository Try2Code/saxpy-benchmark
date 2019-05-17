#include "saxpy.h"
#include <omp.h>

int main() {
   float *x = new float[N], *y = new float[N];

   int g_num_threads = omp_get_max_threads();
#pragma omp parallel for schedule(static) shared(x,y)
   for (int i = 0; i < N; ++i) {
      x[i] = XVAL;
      y[i] = YVAL;
   }
   std::cout << "Number of threads: " << g_num_threads << std::endl;
   std::cout << "N: " << N << std::endl;

   saxpy_timer timer;

#pragma omp parallel for schedule(static) shared(x,y)
      for (int i=0; i<N; ++i)
         y[i] += AVAL * x[i];

   auto elapsed = timer.elapsed_msec();
   std::cout << "Elapsed: " << elapsed << " ms\n";

   saxpy_verify(y);
   delete[] x;
   delete[] y;
   return 0;
}

