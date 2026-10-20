import json, os

# Get all existing articles
sections = ["analysis", "evidence", "actors", "investigate"]
for section in sections:
    d = "/opt/ecoPrimals/tuebor-repo/site/content/" + section + "/"
    if not os.path.exists(d):
        print(section.upper() + ": directory not found")
        continue
    files = [f for f in os.listdir(d) if f.endswith(".md") and f != "_index.md"]
    print("=== " + section.upper() + " (" + str(len(files)) + " articles) ===")
    for f in sorted(files):
        path = os.path.join(d, f)
        content = open(path).read()
        words = len(content.split())
        title = ""
        for line in content.split("\n"):
            if line.startswith("title = "):
                title = line.split("=", 1)[1].strip().strip('"')
                break
        slug = f.replace(".md", "")
        print("  " + slug.ljust(48) + str(words).rjust(6) + "w  " + title[:55])
    print("")

# Now get ALL entities and check which ones have articles about them
print("\n=== ENTITY COVERAGE ===")
e = json.load(open("/opt/ecoPrimals/tuebor-repo/site/content/../../../hud/site/public/detroit-data/explore.json"))
c = json.load(open("/opt/ecoPrimals/tuebor-repo/site/content/../../../hud/site/public/detroit-data/classification.json"))

# Entities by tier
tiers = {}
for ent in e["entities"]:
    tier = ent.get("tier", 99)
    if tier not in tiers:
        tiers[tier] = []
    tiers[tier].append(ent)

# Check which entities have tuebor links
for tier in sorted(tiers.keys()):
    ents = tiers[tier]
    print("\nTIER " + str(tier) + " (" + str(len(ents)) + " entities):")
    for ent in sorted(ents, key=lambda x: -x.get("edges", 0)):
        eid = ent["id"]
        label = ent.get("label", eid)
        sort_class = ent.get("sort_class", "?")
        edges = ent.get("edges", 0)
        links = ent.get("links", {})
        has_tuebor = bool(links.get("braid") or links.get("evidence") or links.get("analysis"))
        link_count = len(links.get("evidence", [])) + len(links.get("analysis", []))
        marker = "  [" + str(link_count) + " links]" if has_tuebor else "  NO ARTICLE"
        print("  " + eid.ljust(30) + sort_class.ljust(10) + str(edges).rjust(4) + "e" + marker)
