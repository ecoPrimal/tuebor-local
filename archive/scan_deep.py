import json

e = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/explore.json"))
g = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/graph.json"))

targets = ["holland", "goetz", "sheffield", "naacp_detroit", "kym_worthy", "moreland", "roland_martin"]

ent_map = {}
for ent in e["entities"]:
    ent_map[ent["id"]] = ent

for tid in targets:
    print("=" * 60)
    ent = ent_map.get(tid, {})
    print(tid.upper())
    print("  label: " + ent.get("label", "?"))
    print("  sort:  " + ent.get("sort_class", "?"))
    print("  conf:  " + str(ent.get("confidence", "?")))
    print("  tier:  " + str(ent.get("tier", "?")))
    print("  edges: " + str(ent.get("edges", "?")))
    print("  role:  " + ent.get("role", "?"))
    print("")

    # Find all edges involving this entity
    edges = []
    for edge in g.get("edges", []):
        src = edge.get("source", "")
        tgt = edge.get("target", "")
        if src == tid or tgt == tid:
            other = tgt if src == tid else src
            etype = edge.get("type", edge.get("edge_type", "?"))
            direction = "OUT" if src == tid else "IN"
            edges.append((direction, other, etype))
    
    edges.sort(key=lambda x: x[1])
    print("  CONNECTIONS (" + str(len(edges)) + "):")
    for direction, other, etype in edges[:30]:
        label = ent_map.get(other, {}).get("label", other)
        sort = ent_map.get(other, {}).get("sort_class", "?")
        print("    " + direction + " " + other.ljust(28) + etype.ljust(25) + sort)
    if len(edges) > 30:
        print("    ... and " + str(len(edges) - 30) + " more")
    print("")
