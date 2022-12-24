#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    road_nodes, road_edges = map(int, input().rstrip().split())

    road_from = [0] * road_edges
    road_to = [0] * road_edges
    road_weight = [0] * road_edges

    adjacent = [[] for i in range(road_nodes)]
    
    for i in range(road_edges):
        road_from[i], road_to[i], road_weight[i] = map(int, input().rstrip().split())
        road_from[i] -= 1
        road_to[i] -= 1
        adjacent[road_from[i]].append((road_to[i], +road_weight[i] % 10))
        adjacent[road_to[i]].append((road_from[i], -road_weight[i] % 10))
    
    _visited = [False] * road_nodes
    visited = [[False] * 10 for i in range(road_nodes)]
    
    ans = [0] * 10
    for s in range(road_nodes):
        if _visited[s] : continue
        queue = [(s, 0)]
        visited[s][0] = True
        f = 0
        ct = [0] * 10
        while f < len(queue):
            i, d = queue[f]; f += 1
            ct[d] += 1
            for j, nd in adjacent[i]:
                nd = (nd + d) % 10
                if not visited[j][nd]:
                    visited[j][nd] = True
                    queue.append((j, nd))
        for i, d in queue:
            if _visited[i]: continue
            _visited[i] = True
            d = -d % 10
            for nd in range(10):
                ans[(nd + d) % 10] += ct[nd] - visited[i][nd]
    for v in ans:
        print(v)
