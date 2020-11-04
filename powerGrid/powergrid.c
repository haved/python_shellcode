

//#include <stdio.h>

//data looks like:
// grid with ints (closest power station) (0 is no name)
// queue of int pairs
// binary tree of edges (wihtout length)
// list of edges with length
// list of sets

#define NULL 0
#define push(x) data[tail++] = (x)
#define pop() data[head++]
#define grid(x, y) data[(x)*h+(y)]

typedef struct {
  int a;
  int b;
} Edge;

typedef struct Node {
  Edge e;
  struct Node* left;
  struct Node* right;
} Node;

typedef struct {
  int a;
  int b;
  int len;
} LenEdge;

typedef struct Set {
  struct Set* parent;
  int size;
} Set;

int same(Edge first, Edge second) {
  return first.a == second.a && first.b == second.b;
}

int less(Edge first, Edge second) {
  if(first.a == second.a)
    return first.b < second.b;
  return first.a < second.a;
}

void addEdge(Node** root, Node** next, int a, int b) {
  Edge e;
  if(a < b) {
    e.a = a;
    e.b = b;
  } else {
    e.a = b;
    e.b = a;
  }

  Node** from;
  for(int i = 0; i < 2; i++) {
    from = root;
    Node* node = *root;
    while(node != NULL) {
      if(same(e, node->e))
        return;
      if(less(e, node->e)) {
        from = &node->left;
        node = node->left;
      } else {
        from = &node->right;
        node = node->right;
      }
    }
  }

  *from = *next;
  (*next)->e = e;
  (*next)->left = NULL;
  (*next)->right = NULL;
  (*next)++;
  //printf("Added egde %d - %d\n", a, b);
}

int abso(int a) {
  return a >= 0 ? a : -a;
}

void sort(LenEdge* edges, int s, int e) {
  if(s+1 >= e)
    return;
  LenEdge pivot = edges[s];

  //printf("Sorting: %d %d\n", s, e);

  int left = s;
  int right = e-1;

  while(1) {
    while(edges[left].len < pivot.len && left <= right)
      left++;
    while(edges[right].len > pivot.len && left <= right)
      right--;
    if(left < right) {
      LenEdge tmp = edges[left];
      edges[left] = edges[right];
      edges[right] = tmp;
      left++;
      right--;
    }
    else break;
  }
  sort(edges, s, left);
  sort(edges, right+1, e);
}

Set* find(Set* set) {
  if(set->parent != set)
    return set->parent = find(set->parent);
  return set;
}

int unioon(Set* a, Set* b) {
  Set* ap = find(a);
  Set* bp = find(b);

  if(ap == bp)
    return 0;

  if(ap->size > bp->size) {
    Set* tmp = ap;
    ap = bp;
    bp = tmp;
  }

  ap->parent = bp;
  bp->size += ap->size;
  return 1;
}

int powergrid(int w, int h, int n, int* stations, int* data) {
  int queueStart = w*h;
  int head = queueStart;
  int tail = queueStart;

  for(int i = 0; i < n; i++) {
    int x = stations[i*2];
    int y = stations[i*2+1];
    push(x);
    push(y);
    grid(x,y)=i+1;
  }

  Node* root = NULL;
  Node* next = (Node*) data+(queueStart+w*h*2);

  while(head != tail) {
    int x = pop();
    int y = pop();
    int station = grid(x,y);

    if(x-1 >= 0) {
      if(grid(x-1,y) == 0) {
        grid(x-1,y) = station;
        push(x-1);
        push(y);
      } else if(grid(x-1,y) != station) {
        addEdge(&root, &next, grid(x-1,y), station);
      }
    }
    if(y-1 >= 0) {
      if(grid(x,y-1) == 0) {
        grid(x,y-1) = station;
        push(x);
        push(y-1);
      } else if(grid(x,y-1) != station) {
        addEdge(&root, &next, grid(x,y-1), station);
      }
    }
    if(x+1 < w) {
      if(grid(x+1,y) == 0) {
        grid(x+1,y) = station;
        push(x+1);
        push(y);
      } else if(grid(x+1,y) != station) {
        addEdge(&root, &next, grid(x+1,y), station);
      }
    }
    if(y+1 < h) {
      if(grid(x,y+1) == 0) {
        grid(x,y+1) = station;
        push(x);
        push(y+1);
      } else if(grid(x,y+1) != station) {
        addEdge(&root, &next, grid(x,y+1), station);
      }
    }
  }

  int edge_count = next-root;

  LenEdge* edges = (LenEdge*) next;

  for(int i = 0; i < edge_count; i++) {
    int a = root[i].e.a-1;
    int b = root[i].e.b-1;
    edges[i].a = a;
    edges[i].b = b;
    edges[i].len = abso(stations[a*2]-stations[b*2])+abso(stations[a*2+1]-stations[b*2+1]);
  }

  sort(edges, 0, edge_count);

  /*for(int i = 0; i < edge_count; i++) {
    printf("Edge between %d - %d. Length: %d\n", edges[i].a, edges[i].b, edges[i].len);
    }*/

  Set* sets = (Set*)(edges+edge_count);
  for(int i = 0; i < n; i++) {
    sets[i].parent = sets+i;
    sets[i].size = 1;
  }

  int left = n-1;
  int dist = 0;
  for(int i = 0; left; i++) {
    if(unioon(sets+edges[i].a, sets+edges[i].b)) {
      dist += edges[i].len;
      left--;
      //printf("Unioned %d - %d   (len %d)\n", edges[i].a, edges[i].b, edges[i].len);
    }
  }

  return dist;
}

/*#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define LEN 70000
#define NS 20000
Node nodes[LEN];*/

int main() {
  /*srand(time(NULL));
  Node* root = NULL;
  Node* next = nodes;
  for(int i = 0; i < LEN; i++) {
    int a = rand() % NS;
    int b = rand() % NS;
    addEdge(&root, &next, a, b);
  }*/
}
