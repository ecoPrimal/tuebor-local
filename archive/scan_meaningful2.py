import json

e = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/explore.json"))
g = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/graph.json"))

skip_types = {"structural_proximity", "nearby", "unlocked_by_evidence", "can_be_played_by",
              "same_city", "same_city_of", "cross_reference", "same_state"}

ent_map = {}
for ent in e["entities"]:
    ent_map[ent["id"]] = ent

targets = ["jolia_hill", "crump_gibson", "vitti", "archer", "charter_law_1993", 
           "dpd", "v_hall", "wendell_anthony", "bert_johnson", "carolyn_kilpatrick",
           "kwame", "cmu", "mike_rogers"]

for tid in targets:
    ent = ent_map.get(tid, {})
    print("=" * 50)
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
            direction = "->" if src == tid else "<-"
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
    for d, o, et, s in unique[:20]:
        print("  " + d + " " + o.ljust(26) + et.ljust(25) + s)
    if len(unique) > 20:
        print("  ... +" + str(len(unique)-20) + " more")
    print("")
