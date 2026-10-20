base_path = "/opt/ecoPrimals/tuebor-repo/site/templates/base.html"
with open(base_path) as f:
    html = f.read()

old = """  <script src="{{ get_url(path='search_index.en.js') }}"></script>
  <script src="{{ get_url(path='js/search.js') }}"></script>"""

new = """  <script src="{{ get_url(path='js/elasticlunr.min.js') }}"></script>
  <script src="{{ get_url(path='search_index.en.js') }}"></script>
  <script src="{{ get_url(path='js/search.js') }}"></script>"""

if old in html:
    html = html.replace(old, new)
    print("OK: added elasticlunr.min.js before search_index")
else:
    print("ERROR: pattern not found")

with open(base_path, 'w') as f:
    f.write(html)
