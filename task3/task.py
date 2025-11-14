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
    
    return json.dumps(contradiction_core, ensure_ascii=False)

if __name__ == "__main__":
    ranking_A = json.dumps([1,[2,3],4,[5,6,7],8,9,10])
    ranking_B = json.dumps([[1,2],[3,4,5,],6,7,9,[8,10]])
    
    result = main(ranking_A, ranking_B)
    print("Ядро противоречий:", result)