import json
import numpy as np

def main(ranking1_json: str, ranking2_json: str) -> str:
    def parse_ranking(ranking_data: list) -> list[list]:
        clusters = []
        for item in ranking_data:
            if isinstance(item, list):
                clusters.append(item)
            else:
                clusters.append([item])
        return clusters
    
    def build_relation_matrix(clusters: list[list], objects: list) -> np.ndarray:
        n = len(objects)
        obj_to_index = {obj: idx for idx, obj in enumerate(objects)}
        matrix = np.zeros((n, n), dtype=int)
        
        for i in range(len(clusters)):
            for j in range(i, len(clusters)):
                for obj_i in clusters[i]:
                    for obj_j in clusters[j]:
                        idx_i = obj_to_index[obj_i]
                        idx_j = obj_to_index[obj_j]
                        matrix[idx_i][idx_j] = 1
        return matrix
    
    def warshall_algorithm(matrix: np.ndarray) -> np.ndarray:
        n = len(matrix)
        closure = matrix.copy()
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])
        return closure
    
    def find_connected_components(equivalence_matrix: np.ndarray, objects: list) -> list[list]:
        n = len(objects)
        visited = [False] * n
        components = []
        
        for i in range(n):
            if not visited[i]:
                component = []
                stack = [i]
                visited[i] = True
                
                while stack:
                    node = stack.pop()
                    component.append(objects[node])
                    
                    for j in range(n):
                        if equivalence_matrix[node][j] == 1 and not visited[j]:
                            visited[j] = True
                            stack.append(j)
                
                components.append(sorted(component))
        
        return sorted(components, key=lambda x: objects.index(x[0]))
    
    ranking1_data = json.loads(ranking1_json)
    ranking2_data = json.loads(ranking2_json)
    all_objects = set()
    
    def extract_objects(ranking):
        objects = []
        for item in ranking:
            if isinstance(item, list):
                objects.extend(item)
            else:
                objects.append(item)
        return objects
    
    objects1 = extract_objects(ranking1_data)
    objects2 = extract_objects(ranking2_data)
    if set(objects1) != set(objects2):
        raise ValueError("Ранжировки содержат разные наборы объектов")
    all_objects = sorted(objects1)
    clusters1 = parse_ranking(ranking1_data)
    clusters2 = parse_ranking(ranking2_data)
    
    YA = build_relation_matrix(clusters1, all_objects)
    YB = build_relation_matrix(clusters2, all_objects)
    YA_transposed = YA.T
    YB_transposed = YB.T
    YAB = YA * YB
    YAB_transposed = YA_transposed * YB_transposed
    Y_combined = YAB | YAB_transposed

    contradiction_core = []
    n = len(all_objects)
    for i in range(n):
        for j in range(i + 1, n):
            if Y_combined[i][j] == 0 and Y_combined[j][i] == 0:
                contradiction_core.append([all_objects[i], all_objects[j]])
    
    #return json.dumps(contradiction_core, ensure_ascii=False)
    
    C = YA * YB
    obj_to_index = {obj: idx for idx, obj in enumerate(all_objects)}
    for obj_i, obj_j in contradiction_core:
        idx_i = obj_to_index[obj_i]
        idx_j = obj_to_index[obj_j]
        C[idx_i][idx_j] = 1
        C[idx_j][idx_i] = 1
    
    E = C * C.T
    E_star = warshall_algorithm(E)
    clusters = find_connected_components(E_star, all_objects)

    obj_to_cluster_idx = {}
    for idx, cluster in enumerate(clusters):
        for obj in cluster:
            obj_to_cluster_idx[obj] = idx

    cluster_order = np.zeros((len(clusters), len(clusters)), dtype=int)
    for i in range(n):
        for j in range(n):
            if C[i][j] == 1 and i != j:
                cluster_i = obj_to_cluster_idx[all_objects[i]]
                cluster_j = obj_to_cluster_idx[all_objects[j]]
                if cluster_i != cluster_j:
                    cluster_order[cluster_i][cluster_j] = 1
    
    cluster_order_closure = warshall_algorithm(cluster_order)
    cluster_indices = list(range(len(clusters)))
    sorted_clusters = []
    remaining = set(cluster_indices)
    while remaining:
        candidates = []
        for i in remaining:
            has_predecessor = False
            for j in remaining:
                if i != j and cluster_order_closure[j][i] == 1:
                    has_predecessor = True
                    break
            if not has_predecessor:
                candidates.append(i)
        
        if not candidates:
            merged_cluster = []
            for idx in remaining:
                merged_cluster.extend(clusters[idx])
            sorted_clusters.append(sorted(merged_cluster))
            break
        
        cluster_group = []
        for idx in candidates:
            cluster_group.extend(clusters[idx])
            remaining.remove(idx)
        
        sorted_clusters.append(sorted(cluster_group))
    
    result = []
    for cluster in sorted_clusters:
        if len(cluster) == 1:
            result.append(cluster[0])
        else:
            result.append(cluster)
    
    return json.dumps(result, ensure_ascii=False)

if __name__ == "__main__":
    ranking_A = json.dumps([1,[2,3],4,[5,6,7],8,9,10])
    ranking_B = json.dumps([[1,2],[3,4,5,],6,7,9,[8,10]])

    #ranking_A2 = json.dumps([1, [2, 3], 4, [5, 6, 7], 8, 9, 10])
    #ranking_B2 = json.dumps([3, [1, 4], 2, 6, [5, 7, 8], [9, 10]])
    
    result = main(ranking_A, ranking_B)
    #print("Ядро противоречий:", result)
    print("Согласованная кластерная ранжировка:", result)