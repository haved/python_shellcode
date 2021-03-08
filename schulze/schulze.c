
#define at(i,j) values[(i)*n+(j)]
#define min(a,b) ((a)<(b)?(a):(b))
#define max(a,b) ((a)>(b)?(a):(b))

int schulze(int n, int* values, int* output) {
  for(int i = 0; i < n; i++) {
    for(int j = 0; j < n; j++) {
      if(at(i,j) <= at(j,i))
        at(i,j) = 0;
    }
  }

  for(int k = 0; k < n; k++) {
    for(int i = 0; i < n; i++) {
      for(int j = 0; j < n; j++) {
        at(i,j) = max(at(i,j), min(at(i,k), at(k,j)));
      }
    }
  }

  return 0;
}
