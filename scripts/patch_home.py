"""One-off: upgrades index.html to use the shared header/footer, case-study cards and service cards."""
import re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_site import project_card, service_card, SERVICES, PROJECTS, NAV
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
s = open(ROOT + "/index.html").read()
about = open(ROOT + "/about.html").read()

hdr = re.search(r"  <header class=\"navbar\">.*?</header>", about, re.S).group(0)
hdr = hdr.replace('class="nav-link active"', 'class="nav-link"').replace('href="/" class="nav-link"', 'href="/" class="nav-link active"')
s = re.sub(r"  <header class=\"navbar\">.*?</header>", lambda m: hdr, s, count=1, flags=re.S)
ftr = re.search(r"  <footer class=\"footer\">.*?</footer>", about, re.S).group(0)
s = re.sub(r"  <footer class=\"footer\">.*?</footer>", lambda m: ftr, s, count=1, flags=re.S)
if "skip-link" not in s:
    s = s.replace('<div class="scroll-progress"', '<a class="skip-link" href="#main-content">Skip to content</a>\n  <div class="scroll-progress"', 1)

a = s.index('<div class="projects-grid">')
b = s.index("</section>", a)
cards = "\n".join(project_card(p) for p in PROJECTS)
s = s[:a] + '<div class="projects-grid">\n' + cards + '\n        </div>\n        <p class="section-more reveal"><a href="/projects" class="btn btn-secondary">View all case studies &rarr;</a></p>\n      </div>\n    ' + s[b:]

a = s.index('<div class="services-grid">')
b = s.index("</section>", a)
keep = [x for x in SERVICES if x["slug"] != "payment-gateway-integration"]
s = s[:a] + '<div class="services-grid">\n' + "\n".join(service_card(x) for x in keep) + '\n        </div>\n        <p class="section-more reveal"><a href="/services" class="btn btn-secondary">All services &rarr;</a></p>\n      </div>\n    ' + s[b:]

s = s.replace('''debugging root causes.
            </p>
          </div>''', '''debugging root causes.
            </p>
            <p><a href="/about" class="btn btn-secondary btn-sm">More about me &rarr;</a></p>
          </div>''', 1)

s = s.replace('<a href="#projects" class="btn btn-primary">', '<a href="/projects" class="btn btn-primary">', 1)
s = s.replace('<a href="#contact" class="btn btn-secondary">Start a Project</a>', '<a href="/contact" class="btn btn-secondary">Start a Project</a>', 1)

s = re.sub(r"  <!-- =+\s*PROJECT DETAILS MODAL DIALOG.*?(?=  <!-- Main JavaScript -->)", "", s, flags=re.S)
s = s.replace('src="js/script.js"', 'src="/js/script.js"').replace('href="css/style.css"', 'href="/css/style.css"').replace('href="favicon.svg"', 'href="/favicon.svg"')
open(ROOT + "/index.html", "w").write(s)
print("patched", len(s))
