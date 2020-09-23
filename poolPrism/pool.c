
#define minF(a, b) ((a)<(b)?(a):(b))
#define maxF(a, b) ((a)>(b)?(a):(b))

int cuboid(int n, int* heights, int* data) {

#define height(x, y) heights[x+y*n]
#define col(x, y1, y2) data[(y1*n+y2)*n+x]

  //First find all column mins
  for(int x = 0; x < n; x++) {
    for(int y1 = 0; y1 < n; y1++) {
      int min = 100000000;
      for(int y2 = y1; y2 < n; y2++) {
        min = minF(min, height(x,y2));
        col(x,y1,y2) = min;
      }
    }
  }

  int bestPool = 0;
  for(int x1 = 0; x1 < n; x1++) {
    for(int y1 = 0; y1 < n; y1++) {
      for(int y2 = y1; y2 < n; y2++) {
        int min = 100000000;
        for(int x2 = x1; x2 < n; x2++) {
          min = minF(min, col(x2, y1, y2));
          bestPool = maxF(bestPool, min*(x2-x1+1)*(y2-y1+1));
        }
      }
    }
  }

  return bestPool;
}

/*#include <stdio.h>
int data[] = {1, 1, 2, 1};
int BUFFER[1024];
int main() {
  printf("Største prisme: %ld \n", cuboid(2, data, BUFFER));
}*/
