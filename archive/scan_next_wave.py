import json, os

e = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/explore.json"))
g = json.load(open("/opt/ecoPrimals/hud/site/public/detroit-data/graph.json"))

# Read ALL article content for mention scanning
all_content = ""
for section in ["analysis", "evidence", "actors", "investigate"]:
    d = "/opt/ecoPrimals/tuebor-repo/site/content/" + section + "/"
    if os.path.exists(d):
        for f in os.listdir(d):
            if f.endswith(".md") and f != "_index.md":
                all_content += open(os.path.join(d, f)).read().lower() + "\n"

# Build entity map
ent_map = {}
for ent in e["entities"]:
    ent_map[ent["id"]] = ent

# EXPANDED keyword map — ALL entities not yet deeply covered
keyword_map = {
    "kwame": (["kwame", "kilpatrick"], "partial", 18, 2, "Former mayor, 28yr sentence, commuted"),
    "archer": (["archer", "dennis archer"], "null", 9, 3, "Dennis Archer — former mayor, Dykema partner"),
    "crump_gibson": (["crump", "gibson"], "partial", 15, 2, "Crump Gibson — connected entity"),
    "miller_judge": (["cylenthia miller", "judge miller"], "partial", 12, 2, "Judge who chairs PCA board"),
    "wilk": (["wilk"], "null", 10, 2, "Wilk — unclassified, 10 edges"),
    "v_hall": (["v hall", "v_hall"], "partial", 5, 2, "V Hall — connected"),
    "bettison": (["bettison"], "partial", 4, 2, "Police chief appointed by Sheffield"),
    "jolia_hill": (["jolia hill", "jolia"], "partial", 10, 3, "Jolia Hill — inner circle governance"),
    "mike_rogers": (["mike rogers", "congressman rogers"], "partial", 10, 3, "Mike Rogers — Congress, fundraising"),
    "charter_law_1993": (["pa 362", "charter school law", "charter law 1993", "act 362"], "partial", 11, 3, "The law that started it all"),
    "renae_moore": (["renae moore", "renae"], "null", 9, 3, "Renae Moore — Dykema compliance"),
    "barton_malow": (["barton malow"], "partial", 2, 4, "Construction company, Beasley employer"),
    "wendell_anthony": (["wendell anthony"], "partial", 4, 3, "Rev. Wendell Anthony — NAACP, political"),
    "bert_johnson": (["bert johnson"], "partial", 4, 3, "State senator, conviction"),
    "vitti": (["vitti", "nikolai"], "partial", 6, 3, "Nikolai Vitti — DPSCD superintendent"),
    "johnson_l": (["latisha johnson"], "null", 8, 3, "Latisha Johnson — City Council, PCA board"),
    "carolyn_kilpatrick": (["carolyn kilpatrick"], "null", 4, 3, "Congresswoman, Kwame's mother"),
    "virgil_smith": (["virgil smith"], "null", 2, 4, "State senator, conviction"),
    "inner_link": (["inner link"], "null", 8, 5, "Banks LLC — Yancey payments"),
    "dpd": (["detroit police", "dpd"], "partial", 6, 2, "Detroit Police Department"),
    "cmu": (["central michigan", "cmu"], "self", 12, 2, "CMU — authorizer, no background checks"),
}

print("=== NEXT WAVE — MENTION DENSITY ===")
print("")
results = []
for eid, (keywords, sort, edges, tier, desc) in keyword_map.items():
    count = 0
    for kw in keywords:
        count += all_content.count(kw)
    results.append((eid, count, sort, edges, tier, desc))

results.sort(key=lambda x: x[1])
for eid, count, sort, edges, tier, desc in results:
    bar = "#" * min(count, 40)
    marker = " *** NEEDS ARTICLE" if count < 10 else (" * THIN" if count < 15 else "")
    print("  " + eid.ljust(22) + str(count).rjust(4) + " " + sort.ljust(9) + str(edges).rjust(3) + "e T" + str(tier) + "  " + bar + marker)

print("")
print("=== STORY PATHS NOT COVERED ===")
stories = e.get("stories", [])
for story in stories:
    sid = story.get("id", "?")
    title = story.get("title", "?")
    nodes = len(story.get("nodes", []))
    # Check if story has a dedicated article
    slug_match = sid.replace("_", "-")
    has_article = slug_match in all_content or sid in all_content
    marker = "" if has_article else " *** NO DEDICATED ARTICLE"
    print("  " + sid.ljust(25) + str(nodes).rjust(3) + " nodes  " + title[:50] + marker)

print("")
print("=== ACTORS SECTION GAPS ===")
# Check which high-edge entities have NO actors page
actors_dir = "/opt/ecoPrimals/tuebor-repo/site/content/actors/"
existing_actors = set()
if os.path.exists(actors_dir):
    for f in os.listdir(actors_dir):
        if f.endswith(".md") and f != "_index.md":
            existing_actors.add(f.replace(".md", ""))

need_actors = []
for ent in e["entities"]:
    if ent.get("edges", 0) >= 5 and ent["id"] not in existing_actors:
        sort = ent.get("sort_class", "?")
        if sort in ["non-self", "partial", "null"]:
            need_actors.append(ent)

need_actors.sort(key=lambda x: -x.get("edges", 0))
print("  " + str(len(need_actors)) + " entities with 5+ edges, no actors page:")
for ent in need_actors[:25]:
    print("    " + ent["id"].ljust(28) + ent.get("sort_class","?").ljust(10) + str(ent.get("edges",0)).rjust(3) + "e  " + ent.get("label", ent["id"])[:40])
