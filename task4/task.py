import json

def trapezoid(x, points):
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    x4, y4 = points[3]
    
    if x <= x1:
        return y1
    if x >= x4:
        return y4
    
    if x1 <= x <= x2:
        if x1 == x2:
            return y1
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    elif x2 <= x <= x3:
        if x2 == x3:
            return y2
        return y2 + (y3 - y2) * (x - x2) / (x3 - x2)
    elif x3 <= x <= x4:
        if x3 == x4:
            return y3
        return y3 + (y4 - y3) * (x - x3) / (x4 - x3)
    
    return 0.0

def parse_json(json_str, var_name):
    data = json.loads(json_str)
    terms_data = data.get(var_name, data)
    
    terms = {}
    for term_data in terms_data:
        term_id = term_data.get("id", "").strip('"{}')
        points = term_data["points"]
        terms[term_id] = points
    
    return terms

def get_membership(terms, term, x):
    if term not in terms:
        return 0.0
    return trapezoid(x, terms[term])    

def main(temp_json: str, reg_json: str, rules_json: str, temp: float) -> float:
    temp_terms = parse_json(temp_json, "температура")
    heat_terms = parse_json(reg_json, "температура")
    
    rules = json.loads(rules_json)
    
    all_points = []
    for term_name, points in heat_terms.items():
        for point in points:
            all_points.append(point[0])
    
    s_min, s_max = min(all_points), max(all_points)
    resolution = 1000
    s_values = [s_min + i * (s_max - s_min) / (resolution - 1) for i in range(resolution)]
    aggregated = [0.0] * resolution
    
    for rule_pair in rules:
        antecedent = str(rule_pair[0]).strip('"{}')
        consequent = str(rule_pair[1]).strip('"{}')
        
        activation = get_membership(temp_terms, antecedent, temp)
        if activation > 0:
            for i, s in enumerate(s_values):
                mu_consequent = get_membership(heat_terms, consequent, s)
                aggregated[i] = max(aggregated[i], min(activation, mu_consequent))
    
    max_value = max(aggregated)
    if max_value == 0:
        return (s_min + s_max) / 2
    
    for i, mu in enumerate(aggregated):
        if mu == max_value:
            return s_values[i]
    
    return s_values[0]

if __name__ == "__main__":
    with open('temperature.json', 'r', encoding='utf-8') as file:
        temp_json = file.read()
    with open('regulation.json', 'r', encoding='utf-8') as file:
        reg_json = file.read()
    with open('rules.json', 'r', encoding='utf-8') as file:
        rules_json = file.read()
    temp = 19
    control  = main(temp_json, reg_json, rules_json, temp)
    print(f"Температура: {temp}°C -> Управление: {control:.2f}")