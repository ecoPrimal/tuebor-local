css_path = "/opt/ecoPrimals/tuebor-repo/site/static/css/main.css"
with open(css_path) as f:
    css = f.read()

search_css = '''
/* ═══════════════════════════════════════════════════════════
   SEARCH BAR
   ═══════════════════════════════════════════════════════════ */

.nav-search {
  position: relative;
  margin-left: auto;
}
.nav-search input {
  background: var(--bg);
  border: 1px solid var(--border);
  color: var(--text);
  font-family: var(--font);
  font-size: 0.85rem;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  width: 220px;
  transition: width 0.2s, border-color 0.2s;
  outline: none;
}
.nav-search input:focus {
  border-color: var(--accent);
  width: 320px;
}
.nav-search input::placeholder { color: var(--text-secondary); opacity: 0.7; }

.search-results {
  position: absolute;
  top: 100%;
  right: 0;
  width: 420px;
  max-height: 70vh;
  overflow-y: auto;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  z-index: 1000;
  margin-top: 4px;
}
.sr-item {
  display: block;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  text-decoration: none;
  color: var(--text);
  transition: background 0.1s;
}
.sr-item:hover, .sr-item:focus {
  background: rgba(96, 165, 250, 0.1);
  outline: none;
}
.sr-item:last-child { border-bottom: none; }
.sr-section {
  display: inline-block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent);
  background: rgba(96, 165, 250, 0.1);
  padding: 0.15rem 0.4rem;
  border-radius: 3px;
  margin-bottom: 0.25rem;
}
.sr-title {
  display: block;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text);
  margin-bottom: 0.2rem;
}
.sr-snippet {
  display: block;
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.4;
}
.sr-snippet mark {
  background: rgba(251, 191, 36, 0.3);
  color: var(--warning);
  padding: 0 2px;
  border-radius: 2px;
}
.sr-empty {
  padding: 1rem;
  color: var(--text-secondary);
  font-size: 0.85rem;
  text-align: center;
}
.sr-more {
  padding: 0.5rem 1rem;
  color: var(--text-secondary);
  font-size: 0.8rem;
  text-align: center;
  border-top: 1px solid var(--border);
}

/* ═══════════════════════════════════════════════════════════
   CROSS-LINKS — Related Articles Graph
   ═══════════════════════════════════════════════════════════ */

.cross-links {
  margin: 3rem 0 2rem;
  padding: 1.5rem;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
}
.cross-links h2 {
  font-size: 1.1rem;
  margin: 0 0 0.25rem;
  border: none;
  padding: 0;
}
.cross-desc {
  color: var(--text-secondary);
  font-size: 0.85rem;
  margin-bottom: 1rem;
}
.cross-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}
.cross-card {
  display: block;
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  text-decoration: none;
  color: var(--text);
  transition: border-color 0.15s, background 0.15s;
}
.cross-card:hover {
  border-color: var(--accent);
  background: rgba(96, 165, 250, 0.05);
}
.cross-card.cross-strong {
  border-left: 3px solid var(--danger);
}
.cross-card.cross-medium {
  border-left: 3px solid var(--warning);
}
.cross-card.cross-weak {
  border-left: 3px solid var(--border);
}
.cross-section {
  display: inline-block;
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent);
  opacity: 0.8;
}
.cross-title {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  margin: 0.2rem 0;
  line-height: 1.3;
}
.cross-strength {
  display: block;
  font-size: 0.7rem;
  color: var(--text-secondary);
}
.cross-empty {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .nav-search input { width: 140px; }
  .nav-search input:focus { width: 200px; }
  .search-results { width: calc(100vw - 2rem); right: -1rem; }
  .cross-grid { grid-template-columns: 1fr; }
}
'''

css += search_css
with open(css_path, 'w') as f:
    f.write(css)

print("OK: CSS patched with search + cross-links styles (" + str(len(css)) + " bytes)")
