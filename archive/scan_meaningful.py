import json

e = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/explore.json"))
g = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/graph.json"))

skip_types = {"structural_proximity", "nearby", "unlocked_by_evidence", "can_be_played_by",
              "same_city", "same_city_of", "cross_reference", "same_state"}

ent_map = {}
for ent in e["entities"]:
    ent_map[ent["id"]] = ent

targets = ["holland", "goetz", "sheffield", "naacp_detroit", "kym_worthy", "moreland", "roland_martin"]

for tid in targets:
    ent = ent_map.get(tid, {})
    print("=" * 60)
    print(tid.upper() + " — " + ent.get("label", "?") + " [" + ent.get("sort_class","?") + " " + str(ent.get("confidence","?")) + "]")
    
    edges = []
    for edge in g.get("edges", []):
        src = edge.get("source", "")
        tgt = edge.get("target", "")
        etype = edge.get("type", edge.get("edge_type", "?"))
        if (src == tid or tgt == tid) and etype not in skip_types:
            other = tgt if src == tid else src
            if other.startswith("article_") or other.startswith("achievement_") or other.startswith("beast_"):
                continue
            direction = "→" if src == tid else "←"
            other_sort = ent_map.get(other, {}).get("sort_class", "?")
            edges.append((direction, other, etype, other_sort))
    
    seen = set()
    unique = []
    for e2 in edges:
        key = e2[0] + e2[1] + e2[2]
        if key not in seen:
            seen.add(key)
            unique.append(e2)
    
    unique.sort(key=lambda x: x[1])
    print("  Meaningful edges: " + str(len(unique)))
    for d, o, et, s in unique[:40]:
        print("    " + d + " " + o.ljust(28) + et.ljust(28) + s)
    print("")
