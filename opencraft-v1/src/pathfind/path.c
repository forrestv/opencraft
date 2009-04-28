#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdio.h>

#define TRUE 1
#define FALSE 0

#define REV(d) ((d+(DIRLEN/2))%DIRLEN)
#define IND(x,y) ((x)+(y)*width)

#define OVERLAYS 4

#define DIRLEN 8
int dirs[8][2] = {
{1,0},{2,1},{0,1},{-2,1},{-1,0},{-2,-1},{0,-1},{2,-1},
};
int dists[8] = {
//4,9,4,9,4,9,4,9,
17,38,17,38,17,38,17,38,
//1,1,1,1,1,1,1,1,
};
int direxpand[8][5][5] = {
{{0,0,0,0,0},
 {0,0,0,0,0},
 {0,0,1,1,0},
 {0,0,0,0,0},
 {0,0,0,0,0}},
{{0,0,0,0,0},
 {0,0,0,0,0},
 {0,0,1,1,0},
 {0,0,0,1,1},
 {0,0,0,0,0}},
{{0,0,0,0,0},
 {0,0,0,0,0},
 {0,0,1,0,0},
 {0,0,1,0,0},
 {0,0,0,0,0}},
{{0,0,0,0,0},
 {0,0,0,0,0},
 {0,1,1,0,0},
 {1,1,0,0,0},
 {0,0,0,0,0}},
{{0,0,0,0,0},
 {0,0,0,0,0},
 {0,1,1,0,0},
 {0,0,0,0,0},
 {0,0,0,0,0}},
{{0,0,0,0,0},
 {1,1,0,0,0},
 {0,1,1,0,0},
 {0,0,0,0,0},
 {0,0,0,0,0}},
{{0,0,0,0,0},
 {0,0,1,0,0},
 {0,0,1,0,0},
 {0,0,0,0,0},
 {0,0,0,0,0}},
{{0,0,0,0,0},
 {0,0,0,1,1},
 {0,0,1,1,0},
 {0,0,0,0,0},
 {0,0,0,0,0}},
};

typedef struct {
  int width;
  int height;
  
  char *overlay[OVERLAYS];
  int overlays[OVERLAYS];
  
  int statecounter;
  
  int *state; // incremented
  char *parent;
  int *gcost;
  int *hcost;
  int *openlistrev;
  
  int *openlist; // Binary heap of indexes to work
  
  int destx;
  int desty;
} pathData;

pathData *pathNew(int width, int height) {
  pathData *data;
  int i;
  
  if (width <= 0 || width > 1024 || height <= 0 || height > 1024) return NULL;
  
  data = malloc(sizeof(pathData));
  
  data->width = width;
  data->height = height;
  for (i = 0; i < OVERLAYS; i++) {
    data->overlay[i] = NULL;
    data->overlays[i] = 0;
  }
  
  data->state = malloc(sizeof(int)*width*height);
  data->parent = malloc(sizeof(char)*width*height);
  data->gcost = malloc(sizeof(int)*width*height);
  data->hcost = malloc(sizeof(int)*width*height);
  data->openlist = malloc(sizeof(int)*width*height);
  data->openlistrev = malloc(sizeof(int)*width*height);
  
  data->statecounter = 0;
  memset(data->state, 0, sizeof(int)*width*height);
  int x, y;
  for (x = 0; x < width; x++)
    for (y = 0; y < height; y++)
      data->hcost[IND(x,y)] = sqrt(x*x+y*y)*17.0; // Not 4...
  
  return data;
}    

void pathFree(pathData *data)
{
  free(data->state);
  free(data->parent);
  free(data->gcost);
  free(data->hcost);
  free(data->openlist);
  free(data->openlistrev);
  free(data);
}

void pathSetOverlay(pathData *data, int num, char *odata, int settings) {
  if (num < 0 || num >= OVERLAYS) return;
  data->overlay[num] = odata;
  data->overlays[num] = settings;
}

int tilewalkable(pathData *data, int x, int y) {
  int width = data->width;
  return data->overlay[0][IND(x,y)] == 0;
}

int walkable(pathData *data, int startx, int starty, int dir) {
  int width = data->width;
  int height = data->height;
  int i, j;
  for (i = 0; i < 5 ; i++) {
    for (j = 0; j < 5 ; j++) {
      if (direxpand[dir][j][i]) {
        int x = startx+i-2;
        int y = starty+j-2;
        if (x < 0) return FALSE;
        if (y < 0) return FALSE;
        if (x >= width) return FALSE;
        if (y >= height) return FALSE;
        if (!tilewalkable(data,x,y)) return FALSE;
      }
    }
  }
  return TRUE;
}

int getfcost(pathData *data, int node) {
  int x,y;
  int width = data->width;
  x = node % width;
  y = node / width;
  return data->gcost[node] + data->hcost[IND(abs(x-data->destx),abs(y-data->desty))];
}

#define HeapUp(i) (((i)-1)/2)
#define HeapDown(i) (((i)*2)+1)

int pathHeapPopTop(pathData *data, int *last) {
  int width = data->width;
  int height = data->height;
  int len = width*height;
  int *heap = data->openlist;
  
  if (*last == -1) return -1;
  int result = heap[0];
  
  heap[0] = heap[*last];
  *last -= 1;
  
  // Bubble down heap[0]
  int cur = 0;
  
  while (TRUE) {
    int down = HeapDown(cur);
    int new = -1;
    
    int newcost = getfcost(data,heap[cur]);
    
    if ((down <= *last) && (down < len) && (getfcost(data,heap[down]) < newcost)) {
      new = down;
      newcost=getfcost(data,heap[new]);
    }
    if ((down+1 <= *last) && (down+1 < len) && (getfcost(data,heap[down+1]) < newcost)) {
      new = down+1;
      newcost=getfcost(data,heap[new]);
    }
    if (new == -1) break;
    
    int tmp = heap[new];
    heap[new] = heap[cur];
    heap[cur] = tmp;
    
    cur = new;
  }
  
  return result;
}

void pathHeapInsert(pathData *data, int *last, int num) {
  int *heap = data->openlist;
  
  *last += 1;
  
  int cur = *last;
  
  heap[cur] = num;
  
  while (TRUE) {
    int up = HeapUp(cur);
    int new = -1;
    
    if (up >= 0)
      if (getfcost(data,heap[up]) > getfcost(data,heap[cur]))
        new = up;
    
    if (new == -1) break;
    
    int tmp = heap[new];
    heap[new] = heap[cur];
    heap[cur] = tmp;
    
    cur = new;
  }
}

void pathHeapMoveUp(pathData *data, int *last, int num) {
  //printf("moveup actually called with %i and %i last\n", num, *last);
  return;
}

int *pathFind(pathData *data, int startx, int starty, int startdir, int endx, int endy) {
  int width = data->width;
  int height = data->height;
  data->destx = endx;
  data->desty = endy;
  int openlast = -1;
  int statecounter = data->statecounter;
  data->statecounter += 2;
  
  data->state[IND(startx,starty)] = statecounter + 1;
  data->gcost[IND(startx,starty)] = 0;
  data->parent[IND(startx,starty)] = REV(startdir);
  pathHeapInsert(data, &openlast, IND(startx,starty));
  
  int currx, curry;
  
  int tmpx, tmpy;
  
  while (TRUE) {
    int node = pathHeapPopTop(data, &openlast);
    if (node == -1) return NULL; // No path
    
    currx = node % width;
    curry = node / width;
    
    if (currx == endx && curry == endy) break; // Found path
    
    data->state[node] = statecounter + 2; // Closed
    
    int d;
    for (d=0; d<DIRLEN; d++) {
      tmpx = currx + dirs[d][0]; // next 4 not needed. much speed??
      tmpy = curry + dirs[d][1];
      if (tmpx < 0 || tmpx >= width) continue;
      if (tmpy < 0 || tmpy >= height) continue;
      if (!walkable(data,currx,curry,d)) continue;
      int dist = dists[d];
      int dirdiff = d-REV(data->parent[IND(currx,curry)]);
      if (dirdiff > (DIRLEN/2)) dirdiff -= DIRLEN;
      if (dirdiff < (-DIRLEN/2)) dirdiff += DIRLEN;
      int cost = data->gcost[IND(currx,curry)] + dist + abs(dirdiff)*100;
      if (data->state[IND(tmpx,tmpy)] == statecounter + 1) { // Open
        if (data->gcost[IND(tmpx,tmpy)] > cost) {
          data->parent[IND(tmpx,tmpy)] = REV(d);
//          printf("old cost %i, new %i\n", data->gcost[IND(tmpx,tmpy)], cost);
          data->gcost[IND(tmpx,tmpy)] = cost;
          pathHeapMoveUp(data, &openlast, IND(tmpx,tmpy));
        }
      } else if (data->state[IND(tmpx,tmpy)] == statecounter + 2) { // Closed
        if (data->gcost[IND(tmpx,tmpy)] > cost) {
          data->parent[IND(tmpx,tmpy)] = REV(d);
          data->gcost[IND(tmpx,tmpy)] = cost;
        }
      } else {
        data->state[IND(tmpx,tmpy)] = statecounter + 1;
        data->parent[IND(tmpx,tmpy)] = REV(d);
        data->gcost[IND(tmpx,tmpy)] = cost;
        pathHeapInsert(data, &openlast, IND(tmpx,tmpy));
      }
    }
  }
  int count;
  
  count = 0;
  tmpx = currx;
  tmpy = curry;
  while ((tmpx != startx) || (tmpy != starty)) {
    int p = data->parent[IND(tmpx,tmpy)];
    tmpx += dirs[p][0];
    tmpy += dirs[p][1];
    count += 1;
  }
  count += 1;
//  printf("res %i\n",sizeof(int)*(2*count+2));
  int *resultp;
  resultp = malloc(sizeof(int)*(2*count+2));
  
//  printf("res %i\n",count);
  resultp[0] = count;
  
  int cur = count - 2;
  tmpx = currx;
  tmpy = curry;
  while ((tmpx != startx) || (tmpy != starty)) {
    int p = data->parent[IND(tmpx,tmpy)];
    tmpx += dirs[p][0];
    tmpy += dirs[p][1];
    resultp[2+2*cur] = tmpx; // New
    resultp[2+2*cur+1] = tmpy; // New
    cur -= 1;
  }
  resultp[2*count] = endx; // New
  resultp[2*count+1] = endy; // New
  return resultp;
}
/*
void printh(pathData *data, int *last) {
  int i, cur, full;
  cur = 0;
  full = 1;
  for (i = 0; i <= *last; i++) {
    printf("%i ", data->openlist[i]);
    cur++;
    if (cur == full) {
      printf("\n");
      cur = 0;
      full = full * 2;
    }
  }
}

int test_heap() {
  pathData *data = pathNew(1000,1000);
  int width = data->width;
  int height = data->height;
  int x, y;
  for (x = 0; x < width; x++)
    for (y = 0; y < height; y++)
      data->gcost[IND(x,y)] = IND(x,y);
  for (x = 0; x < width; x++)
    for (y = 0; y < height; y++)
      data->hcost[IND(x,y)] = 0; // Not 4...
  
  int i;
  
  for (i = 0; i < 10000; i++)
    if (getfcost(data,i) != i)
      printf("bad %i\n",i);
  int last = -1;
  for (i = 0; i < 1000000; i++) {
    int r = rand() % 1000000;
    pathHeapInsert(data, &last, r);
  }
  int o=-1;
  for (i = 0; i < 1000000; i++) {
    int r = pathHeapPopTop(data, &last);
    if (r<o)
        printf("%i\n", r);
    o = r;
    int x;
  }
}

int main() {
  test_heap();
}
*/
