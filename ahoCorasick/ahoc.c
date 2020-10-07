
typedef struct Node {
  struct Node* parent;
  struct Node* next[26];
  char letter;
  struct Node* longest_suffix;
  int count;
} Node;

Node* getNext(Node* node, char letter);

Node* getLongestSuffix(Node* node) {
  if(node->longest_suffix == 0) {
    if(node->parent) { //The top node is supposed to have no longest suffix
      Node* longest = getLongestSuffix(node->parent);
      if(longest) { //Our parent is not the root node
        node->longest_suffix = getNext(longest, node->letter);
      } else { //Our parent is the root node, thus our longest suffix is empty string
        node->longest_suffix = node->parent;
      }
    }
  }
  return node->longest_suffix;
}

Node* getNext(Node* node, char letter) {
  if(node->next[letter] == 0) {
    if(node->parent) {
      //Any not that isn't the root at least has the root as longest suffix
      Node* longest_suffix = getLongestSuffix(node);
      node->next[letter] = getNext(longest_suffix, letter);
    } else {
      node->next[letter] = node; //We have no suffix because we are root. Ignore this letter
    }
  }
  return node->next[letter];
}

int getScore(Node* node) {
  if(node->count < 0) {
    node->count += 100000;
    if(node->parent)
      node->count += getScore(getLongestSuffix(node));
  }
  return node->count;
}

int string_match(char* dna, int dnalen, char* segments, int segment_count, void* data) {
  int usedNodes = 0;
  Node* nodes = (Node*) data;

  Node* root = &nodes[usedNodes++];

  for(int i = 0; i < segment_count; i++) {
    Node* node = root;
    char c;
    while((c = *segments)) {
      c-=65;
      if(node->next[c] == 0) {
        Node* newNode = &nodes[usedNodes++];
        newNode->parent = node;
        newNode->letter = c;
        newNode->count = -100000;
        node->next[c] = newNode;
      }
      node = node->next[c];
      segments++;
    }
    node->count++;
    segments++;
  }

  int score = 0;
  Node* node = root;
  for(int i = 0; i < dnalen; i++) {
    char c = dna[i]-65;
    node = getNext(node, c);
    score += getScore(node);
  }

  return score;
}

int main()
{
}
