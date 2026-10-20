import json, os

e = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/explore.json"))
g = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/graph.json"))

all_content = ""
for section in ["analysis", "evidence", "actors", "investigate"]:
    d = "/opt/ecoPrimals/tuebor-repo/site/content/" + section + "/"
    if os.path.exists(d):
        for f in os.listdir(d):
            if f.endswith(".md") and f != "_index.md":
                all_content += open(os.path.join(d, f)).read().lower() + "\n"

ent_map = {}
for ent in e["entities"]:
    ent_map[ent["id"]] = ent

# BIG SCAN — every entity with 3+ edges that hasn't been deeply written about
expanded = {
    "v_hall": ["v hall", "v_hall", "vanessa hall"],
    "fiore": ["fiore", "steve fiore"],
    "burris": ["burris"],
    "sean_perkins": ["sean perkins", "judge perkins"],
    "perkins_david": ["david perkins", "perkins law"],
    "eric_sabree": ["eric sabree"],
    "adam_sabree": ["adam sabree"],
    "sabree": ["sabree"],
    "jacquie_hood_martin": ["jacquie hood", "hood martin"],
    "raphael_washington": ["raphael washington"],
    "sheila_cockrel": ["sheila cockrel", "cockrel"],
    "agc_willis": ["willis"],
    "maleyko": ["maleyko"],
    "hutchings": ["hutchings"],
    "dumas": ["dumas"],
    "wells_stallworth": ["wells stallworth"],
    "johnson_l": ["latisha johnson"],
    "scbc_tour": ["school choice black", "scbc"],
    "npe": ["network for public education", "npe"],
    "the_74": ["the 74", "the74"],
    "dpsa": ["dpsa", "detroit prep"],
    "od_banks": ["od banks", "o.d. banks"],
    "anchor_rock": ["anchor rock"],
    "citizendetroit": ["citizen detroit", "citizendetroit"],
    "bing": ["dave bing", "bing"],
    "coleman_young": ["coleman young"],
    "virgil_smith": ["virgil smith"],
    "agc_robinson": ["robinson agc"],
    "miller": ["cylenthia miller", "judge miller"],
    "yancey": ["judge yancey", "tenisha yancey"],
    "wilk": ["alan wilk", "w. alan wilk", "wilk"],
}

print("=== REMAINING ENTITY GAPS ===\n")
results = []
for eid, keywords in expanded.items():
    count = 0
    for kw in keywords:
        count += all_content.count(kw)
    ent = ent_map.get(eid, {})
    sort = ent.get("sort_class", "?")
    edges = ent.get("edges", 0)
    tier = ent.get("tier", "?")
    label = ent.get("label", eid)
    results.append((eid, count, sort, edges, tier, label))

results.sort(key=lambda x: x[1])
for eid, count, sort, edges, tier, label in results:
    bar = "#" * min(count, 30)
    marker = " *** NEEDS" if count < 5 else (" * THIN" if count < 10 else "")
    print("  " + eid.ljust(22) + str(count).rjust(3) + " " + sort.ljust(9) + str(edges).rjust(3) + "e T" + str(tier) + "  " + label[:30].ljust(32) + bar + marker)

# Check what TYPES of articles we're missing
print("\n=== MISSING ARTICLE TYPES ===")
print("\nACTORS pages (profile pages for key people):")
actors_dir = "/opt/ecoPrimals/tuebor-repo/site/content/actors/"
existing_actors = set()
if os.path.exists(actors_dir):
    for f in os.listdir(actors_dir):
        if f.endswith(".md") and f != "_index.md":
            existing_actors.add(f.replace(".md", ""))
print("  Have: " + ", ".join(sorted(existing_actors)))

key_people = ["banks", "beasley", "goetz", "moreland", "holland", "crump-gibson", 
              "jolia-hill", "vitti", "sheffield", "gay-dagnogo", "kwame",
              "kym-worthy", "miller", "yancey", "ison", "roland-martin",
              "wendell-anthony", "bert-johnson"]
missing_actors = [p for p in key_people if p not in existing_actors]
print("  Need: " + ", ".join(missing_actors))

print("\nEVIDENCE pages (documents, records, data):")
evidence_dir = "/opt/ecoPrimals/tuebor-repo/site/content/evidence/"
existing_evidence = set()
if os.path.exists(evidence_dir):
    for f in os.listdir(evidence_dir):
        if f.endswith(".md") and f != "_index.md":
            existing_evidence.add(f.replace(".md", ""))
print("  Have: " + ", ".join(sorted(existing_evidence)))

# Check for needed evidence pages
needed_evidence = ["banks-convictions", "pca-test-scores", "purpose-group-extraction",
                   "banks-llc-network", "board-connections", "walton-funding-trail",
                   "cmu-authorization-records", "dpscd-authorization-records"]
missing_evidence = [p for p in needed_evidence if p not in existing_evidence]
print("  Need: " + ", ".join(missing_evidence))

print("\nINVESTIGATE pages (how-to guides):")
investigate_dir = "/opt/ecoPrimals/tuebor-repo/site/content/investigate/"
existing_invest = set()
if os.path.exists(investigate_dir):
    for f in os.listdir(investigate_dir):
        if f.endswith(".md") and f != "_index.md":
            existing_invest.add(f.replace(".md", ""))
print("  Have: " + ", ".join(sorted(existing_invest)))

needed_invest = ["lara-lookup-guide", "charter-school-complaint", "ag-complaint-guide",
                 "campaign-finance-lookup", "990-lookup-guide"]
missing_invest = [p for p in needed_invest if p not in existing_invest]
print("  Need: " + ", ".join(missing_invest))
