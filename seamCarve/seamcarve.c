
#define at(x,y) (1+(x)+(y)*(1+w))
#define min(a,b) ((a)<(b)?(a):(b))

int seamcarve(int w, int h, int* values, int* output) {
  for(int y = h-2; y >= 0; y--) {
    for(int x = 0; x < w; x++) {
      int minst = values[at(x,y+1)];
      minst = min(minst, values[at(x-1,y+1)]);
      minst = min(minst, values[at(x+1,y+1)]);
      values[at(x,y)] += minst;
    }
  }

  //first find best starting point
  int pos = 0;
  int val = 0x7FFFFFFF;
  for(int x = 0; x < w; x++) {
    if(values[at(x,0)] < val) {
      val = values[at(x,0)];
      pos = x;
    }
  }

  output[0] = pos;
  for(int y = 1; y < h; y++) {
    int npos = pos;
    int val = values[at(pos,y)];
    if(values[at(pos+1,y)]<val) {
      npos = pos+1;
      val = values[at(pos+1,y)];
    }
    if(values[at(pos-1,y)]<val) {
      npos = pos-1;
      val = values[at(pos-1,y)];
    }
    output[y] = pos = npos;
  }

  return 0;
}
