import numpy as np
import math


def rehang_vertex(neighbours: dict[str: int], edges: set[tuple[str, str]]) -> list[set[tuple[str, str]]]:
    graphs = [edges.copy()]
    for v, n in neighbours.items():
        if len(n) == 1:
            edges.discard((v, n[0]))
            edges.discard((n[0], v))
            for u in neighbours.keys():
                if u != v and u != n[0]:
                    edges.add((v, u))
                    graphs.append(edges.copy())
                    edges.remove((v, u))
            edges.add((v, n[0]))

    return graphs


def calc_rs(adjacency_matrix: list[list[bool]]) -> tuple[list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]]]:
    r1 = adjacency_matrix
    r2 = np.array(r1).T.tolist()
    r3 = (np.array(r1) @ np.array(r1)).tolist()
    r4 = np.array(r3).T.tolist()
    r5 = (np.array(r2) @ np.array(r1)).tolist()
    for i in range(len(r5)):
        r5[i][i] = 0

    return r1, r2, r3, r4, r5


def calc_entropy(rs: tuple[list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]]]) -> tuple[float, float]:
    k = len(rs)
    n = len(rs[0])

    H = 0
    for i in range(k):
        for j in range(n):
            l_ij = sum(rs[i][j])
            p_ij = l_ij / (n - 1)
            if p_ij != 0:
                H -= p_ij * math.log2(p_ij)
    
    h = H / (n * k * math.log2(math.e) / math.e)
    return H, h


def main(s: str, root: str) -> tuple[float, float]:
    edges_str = s.strip().split('\n')
    
    vertices = set()
    neighbours = dict()
    edges = set()
    for edge in edges_str:
        if edge:
            v1, v2 = edge.split(',')
            v1 = v1.strip()
            v2 = v2.strip()
            vertices.add(v1)
            vertices.add(v2)
            edges.add((v1, v2))
            if v1 in neighbours.keys():
                neighbours[v1].append(v2)
            else:
                neighbours[v1] = [v2]
            if v2 in neighbours.keys():
                neighbours[v2].append(v1)
            else:
                neighbours[v2] = [v1]
    
    sorted_vertices = sorted(vertices)
    vertex_index = {vertex: idx for idx, vertex in enumerate(sorted_vertices)}
    n = len(sorted_vertices)

    graphs = rehang_vertex(neighbours, edges)
    H_max, h_max = 0, 0

    for graph in graphs:
        adjacency_matrix = [[0] * n for _ in range(n)]
        used_edges = set()
        used_vertices = set(root)

        while len(used_edges) != len(graph):
            for edge in graph:
                if edge not in used_edges:
                    v1, v2 = edge
                    if v1 in used_vertices:
                        i = vertex_index[v1]
                        j = vertex_index[v2]
                        adjacency_matrix[i][j] = 1
                        used_vertices.add(v2)
                        used_edges.add(edge)
                    elif v2 in used_vertices:
                        i = vertex_index[v1]
                        j = vertex_index[v2]
                        adjacency_matrix[j][i] = 1
                        used_vertices.add(v1)
                        used_edges.add(edge)
        
        H, h = calc_entropy(calc_rs(adjacency_matrix))
        H_max = max(H_max, H)
        h_max = max(h_max, h)

    return (round(H_max, 2), round(h_max, 2))


if __name__ == "__main__":
    with open('task2.csv', 'r', encoding='utf-8') as file:
        s = file.read()
    
    H, h = main(s, '1')
    print("H:", H)
    print("h:", h)
