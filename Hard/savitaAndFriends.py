#!/bin/python3

import math
import os
import random
import re
import sys
from collections import defaultdict
import heapq

#
# Complete the 'solve' function below.
#
# The function is expected to return a DOUBLE_ARRAY.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER k
#  3. 2D_INTEGER_ARRAY roads
#

def shortest_path(graph, start):
    visited = set()
    dist = {start : 0}
    heap = [(0, start)]
    while heap:
        dist_x, x = heapq.heappop(heap)
        if x in visited:
            continue
        visited.add(x)
        for y, d in graph[x]:
            if y in visited:
                continue
            dist_y = dist_x + d
            if y not in dist or dist[y] > dist_y:
                dist[y] = dist_y
                heapq.heappush(heap, (dist_y, y))
    return dist

def get_minMax(dist_a, dist_b, dist_ab):
    def edge_weights(edges):
        edges = sorted(edges, key = lambda x : x[1], reverse = True)
        out = [edges[0]]
        for x, y in edges[1:]:
            if any(y0 - y >= abs(x0 - x) for x0, y0 in out):
                continue
            out.append((x, y))
        return out
    
    def remove_outliers(edges):
        edges = sorted(edges, key = lambda x: x[0])
        n1 = 0
        n2 = 0
        for x, y in edges:
            if x <= 0:
                n1 += 1
            elif x >= dist_ab:
                n2 += 1
        return edges[max(n1 - 1, 0) : -(n2 - 1) if n2 > 1 else len(edges)]
    
    def minMax(x):
        return max(min(da + x, db + dist_ab - x) for da, db in zip(dist_a, dist_b))
    
    edges = []
    for da, db in zip (dist_a, dist_b):
        if da < math.inf and db < math.inf:
            edge = (db - da + dist_ab) / 2, (da + db + dist_ab) / 2
            if edge[0] < 0:
                edge = 0, db + dist_ab
            elif edge [0] > dist_ab:
                edge = dist_ab, da + dist_ab
        elif da < math.inf:
            edge = dist_ab, da + dist_ab
        elif db < math.inf:
            edge = 0, db + dist_ab
        else:
            raise ValueError('Node INF')
        edges.append(edge)
    
    edges = edge_weights(edges)
    edges = remove_outliers(edges)
    return minMax, edges

def getMinLocal(edges, dist_ab):
    min = []
    x1, y1 = edges[0]
    if x1 > 0:
        min.append((0, y1 - x1))
        
    for i, (x2, y2) in enumerate(edges[1:]):
        x0 = (x1 + x2 + y1 - y2) / 2
        y0 = (x1 - x2 + y1 + y2) / 2
        min.append((x0, y0))
        x1, y1 = x2, y2
        
    x2, y2 = edges[-1]
    if x2 < dist_ab:
        min.append((dist_ab, x2 + y2 - dist_ab))
    
    return min

def solve(n, k, roads):
    # Write your code here
    edges = roads.copy()
    dest_a, dest_b, dist_ab = edges[k - 1]
    edges.pop(k-1)
    edges.extend([(r, l, c) for l, r, c in edges])
    graph = defaultdict(list)
    for l, r, c in edges:
        graph[l].append((r, c))
        
    dist_a = n * [math.inf]
    for node, dist in shortest_path(graph, dest_a).items():
        dist_a[node - 1] = dist
    dist_b = n * [math.inf]
    for node, dist in shortest_path(graph, dest_b).items():
        dist_b[node - 1] = dist
    minmax, e = get_minMax(dist_a, dist_b, dist_ab)
    min = getMinLocal(e, dist_ab)
    x = sorted(min, key = lambda x : math.floor(x[1] * 1e7))[0]
    return x
    
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])

        m = int(first_multiple_input[1])

        k = int(first_multiple_input[2])

        roads = []

        for _ in range(m):
            roads.append(list(map(int, input().rstrip().split())))

        result = solve(n, k, roads)
        result = '{0[0]:.5f} {0[1]:.5f}\n'.format(result)
        fptr.write(result)
        #fptr.write(' '.join(map(str, result)))
        #fptr.write('\n')

    fptr.close()
