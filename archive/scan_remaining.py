import os

articles = set()
for section in ["analysis", "evidence", "actors", "investigate"]:
    d = "/opt/ecoPrimals/tuebor-repo/site/content/" + section + "/"
    if os.path.exists(d):
        for f in os.listdir(d):
            if f.endswith(".md") and f != "_index.md":
                content = open(os.path.join(d, f)).read().lower()
                articles.add(f.replace(".md", ""))

entities_covered = set()
keyword_map = {
    "banks": ["banks", "brian banks", "brian roderick"],
    "pca": ["purpose charter academy", "pca"],
    "macdowell": ["macdowell", "mac dowell"],
    "purpose_group": ["purpose group"],
    "purpose_foundation": ["purpose foundation"],
    "walton": ["walton family", "walton foundation"],
    "devos": ["devos", "betsy devos"],
    "dykema": ["dykema", "dykema gossett"],
    "plante_moran": ["plante moran"],
    "beasley": ["beasley", "chalena"],
    "nessel": ["nessel", "attorney general"],
    "ison": ["dawn ison", "ison"],
    "sbm": ["state bar of michigan", "state bar"],
    "upl": ["unauthorized practice", "upl"],
    "roland_martin": ["roland martin"],
    "the_74": ["the 74"],
    "afc": ["american federation for children", "afc"],
    "miller": ["judge miller", "cylenthia miller"],
    "yancey": ["judge yancey", "yancey"],
    "goetz": ["goetz"],
    "kwame": ["kwame", "kilpatrick"],
    "sheffield": ["sheffield"],
    "holland": ["holland"],
    "gay_dagnogo": ["gay-dagnogo", "gay dagnogo", "dagnogo"],
    "stallworth": ["stallworth"],
    "kym_worthy": ["kym worthy", "worthy"],
    "naacp": ["naacp"],
    "inner_link": ["inner link"],
    "sbe": ["state board of education"],
    "mde": ["michigan department of education", "mde"],
    "barton_malow": ["barton malow"],
    "ellison": ["ellison"],
    "rogers": ["mike rogers", "rogers"],
    "archer": ["archer"],
    "moreland": ["moreland"],
}

all_content = ""
for section in ["analysis", "evidence", "actors", "investigate"]:
    d = "/opt/ecoPrimals/tuebor-repo/site/content/" + section + "/"
    if os.path.exists(d):
        for f in os.listdir(d):
            if f.endswith(".md") and f != "_index.md":
                all_content += open(os.path.join(d, f)).read().lower() + "\n"

print("=== ENTITY MENTION DENSITY ===")
print("")
mentions = []
for entity, keywords in keyword_map.items():
    count = 0
    for kw in keywords:
        count += all_content.count(kw)
    mentions.append((entity, count))

mentions.sort(key=lambda x: -x[1])
for entity, count in mentions:
    bar = "#" * min(count, 50)
    marker = " <-- NEEDS ARTICLE" if count < 5 else ""
    print("  " + entity.ljust(22) + str(count).rjust(5) + " " + bar + marker)

print("")
print("=== LOW/ZERO DENSITY — REMAINING GAPS ===")
low = [(e, c) for e, c in mentions if c < 10]
print("  " + str(len(low)) + " entities with fewer than 10 mentions across all articles:")
for e, c in low:
    print("    " + e + " (" + str(c) + " mentions)")
