def main(s: str) -> list[list]:#tuple[list[list], list[str]]:
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
    
    adjacency_matrix = [[0] * n for _ in range(n)]
    
    for edge in edges:
        if edge:
            v1, v2 = edge.split(',')
            v1 = v1.strip()
            v2 = v2.strip()
            i = vertex_index[v1]
            j = vertex_index[v2]
            adjacency_matrix[i][j] = 1
            adjacency_matrix[j][i] = 1
    
    return adjacency_matrix#, sorted_vertices


if __name__ == "__main__":
    with open('task0.csv', 'r', encoding='utf-8') as file:
        s = file.read()
    
    #matrix, vertices = main(s)
    matrix = main(s)
    
    #print("Вершины:", vertices)
    print("Матрица смежности:")
    for row in matrix:
        print(row)