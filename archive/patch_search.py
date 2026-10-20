import re

# 1. Patch base.html — add search bar to nav + search JS
base_path = "/opt/ecoPrimals/tuebor-repo/site/templates/base.html"
with open(base_path) as f:
    html = f.read()

# Add search bar after nav-links div
old_nav = '</div>\n    </div>\n  </nav>'
new_nav = '''</div>
      <div class="nav-search">
        <input type="text" id="tuebor-search" placeholder="Search Beasley, Moran, PCA..." autocomplete="off" aria-label="Search articles">
        <div id="tuebor-search-results" class="search-results" style="display:none"></div>
      </div>
    </div>
  </nav>'''

if old_nav in html:
    html = html.replace(old_nav, new_nav)
    print("OK: patched nav with search bar")
else:
    print("WARN: nav pattern not found, trying alternate")
    # Try with different whitespace
    old_nav2 = '</div>\n    </div>\n  </nav>'
    if old_nav2 in html:
        html = html.replace(old_nav2, new_nav)
        print("OK: patched nav (alt)")

# Add search JS before closing body
old_body = '  {# biomeOS HUD widget'
new_body = '''  <script src="{{ get_url(path='search_index.en.js') }}"></script>
  <script src="{{ get_url(path='js/search.js') }}"></script>
  {# biomeOS HUD widget'''

if old_body in html:
    html = html.replace(old_body, new_body)
    print("OK: added search scripts")

with open(base_path, 'w') as f:
    f.write(html)

# 2. Patch page.html — add cross-links / related articles section
page_path = "/opt/ecoPrimals/tuebor-repo/site/templates/page.html"
with open(page_path) as f:
    page = f.read()

# Add related articles section before the opsonization layer
old_opsn = "{# ═══════════════════"
related_block = '''{# ═══════════════════════════════════════════════════════════
   CROSS-LINKS — Graph Navigation Between Articles
   ═══════════════════════════════════════════════════════════ #}

{% if page.extra.keywords is defined %}
<nav class="cross-links" aria-label="Related articles">
  <h2>🔗 Connections</h2>
  <p class="cross-desc">Other articles that touch the same entities and patterns.</p>
  <div id="cross-link-list" data-keywords="{{ page.extra.keywords }}"></div>
</nav>
{% endif %}

{# ═══════════════════'''

if old_opsn in page:
    page = page.replace(old_opsn, related_block, 1)
    print("OK: added cross-links section to page.html")

with open(page_path, 'w') as f:
    f.write(page)

print("DONE: templates patched")
