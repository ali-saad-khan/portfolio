"""Idempotent: syncs the shared header/footer into index.html and (re)writes the Shopify showroom section."""
import re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_site import project_card, PROJECTS
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
s = open(ROOT + "/index.html").read()
about = open(ROOT + "/about.html").read()

hdr = re.search(r"  <header class=\"navbar\">.*?</header>", about, re.S).group(0)
hdr = hdr.replace('class="nav-link active"', 'class="nav-link"').replace('href="/" class="nav-link"', 'href="/" class="nav-link active"')
s = re.sub(r"  <header class=\"navbar\">.*?</header>", lambda m: hdr, s, count=1, flags=re.S)
ftr = re.search(r"  <footer class=\"footer\">.*?</footer>", about, re.S).group(0)
s = re.sub(r"  <footer class=\"footer\">.*?</footer>", lambda m: ftr, s, count=1, flags=re.S)

cards = "\n".join(project_card(p) for p in PROJECTS if p["kind"] == "showcase")
block = f'''<!-- shopify-showroom:start -->
    <section id="shopify" class="section section-alt">
      <div class="container">
        <div class="section-header reveal">
          <span class="section-tag">// SHOPIFY SHOWROOM</span>
          <h2 class="section-title">Four original Shopify storefronts</h2>
          <p class="section-subtitle">Bespoke themes, interactive sections and repeatable store setup, each with its own brand and art direction.</p>
        </div>
        <div class="projects-grid">
{cards}
        </div>
        <p class="section-more reveal"><a href="/shopify" class="btn btn-secondary">See the Shopify showroom &rarr;</a></p>
      </div>
    </section>
    <!-- shopify-showroom:end -->
'''
if "<!-- shopify-showroom:start -->" in s:
    s = re.sub(r"<!-- shopify-showroom:start -->.*?<!-- shopify-showroom:end -->\n", lambda m: block, s, flags=re.S)
else:
    i = s.index('<section id="projects"')
    s = s[:i] + block + "    " + s[i:]
open(ROOT + "/index.html", "w").write(s)
print("index.html updated")
