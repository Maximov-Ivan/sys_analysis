import numpy as np

def main(s: str, root: str) -> tuple[list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]], list[list[bool]]]:
    edges = s.strip().split('\n')
    
    vertices = set[str]()
    for edge in edges:
        if edge:
            v1, v2 = edge.split(',')
            vertices.add(v1.strip())
            vertices.add(v2.strip())
    
    sorted_vertices = sorted(vertices)
    vertex_index = {vertex: idx for idx, vertex in enumerate(sorted_vertices)}
    n = len(sorted_vertices)
    
    r1 = [[0] * n for _ in range(n)]
    r2 = [[0] * n for _ in range(n)]
    
    used_edges = set()
    used_vertices = set(root)
    while len(used_edges) != len(edges):
        for edge in edges:
            if edge and edge not in used_edges:
                v1, v2 = edge.split(',')
                v1 = v1.strip()
                v2 = v2.strip()
                if v1 in used_vertices:
                    i = vertex_index[v1]
                    j = vertex_index[v2]
                    r1[i][j] = 1
                    r2[j][i] = 1
                    used_vertices.add(v2)
                    used_edges.add(edge)
                elif v2 in used_vertices:
                    i = vertex_index[v1]
                    j = vertex_index[v2]
                    r1[j][i] = 1
                    r2[i][j] = 1
                    used_vertices.add(v1)
                    used_edges.add(edge)
    
    r3 = (np.array(r1) @ np.array(r1)).tolist()
    r4 = np.array(r3).T.tolist()
    r5 = (np.array(r2) @ np.array(r1)).tolist()

    for i in range(len(r5)):
        r5[i][i] = 0

    return r1, r2, r3, r4, r5


if __name__ == "__main__":
    with open('task1.csv', 'r', encoding='utf-8') as file:
        s = file.read()
    
    r1, r2, r3, r4, r5 = main(s, '1')

    print("r1:")
    for row in r1:
        print(row)
    print()
    
    print("r2:")
    for row in r2:
        print(row)
    print()
    
    print("r3:")
    for row in r3:
        print(row)
    print()
    
    print("r4:")
    for row in r4:
        print(row)
    print()
    
    print("r5:")
    for row in r5:
        print(row)