#!/usr/bin/env python3
"""Builds the static pages (about, projects, case studies, services, contact),
sitemap.xml and per-page social images. Run: python3 scripts/make_images.py && python3 scripts/build_site.py
Pass --og to (re)render the 1200x630 social images with headless Chrome."""
import html as _html, json, os, re, shutil, subprocess, sys, tempfile
from content import *  # noqa
from blog_content import POSTS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TODAY = "2026-10-13"
PMAP = {p["slug"]: p for p in PROJECTS}
SMAP = {s["slug"]: s for s in SERVICES}
BRAND = "Saad Ali Khan"


def e(s):
    return _html.escape(s, quote=True)


def h(s):
    """Escape text but keep <code> tags from the content files."""
    out = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return out.replace("&lt;code&gt;", "<code>").replace("&lt;/code&gt;", "</code>")


def plain(s):
    return re.sub(r"<[^>]+>", "", s)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}


PERSON = {"@type": "Person", "@id": SITE + "/#person", "name": BRAND, "url": SITE + "/", "jobTitle": "Software Engineer",
          "worksFor": {"@type": "Organization", "name": "Technyx"}, "email": EMAIL,
          "address": {"@type": "PostalAddress", "addressLocality": "Karachi", "addressCountry": "PK"},
          "sameAs": [GITHUB, LINKEDIN],
          "knowsAbout": ["Laravel", "PHP", "MySQL", "REST APIs", "Payment integrations", "WordPress", "Shopify", "Next.js"]}

NAV = [("Home", "/"), ("About", "/about"), ("Services", "/services"), ("Projects", "/projects"), ("Blog", "/blog"), ("Contact", "/contact")]


def page(path, title, desc, body, active, schema=(), og=None, robots=None):
    og_img = f"{SITE}/assets/images/og/{og}.png" if og else f"{SITE}/assets/images/og-image.png"
    url = SITE + path
    full = f"{title} | {BRAND}"
    nav = "".join(f'<a href="{u}" class="nav-link{" active" if n == active else ""}">{n}</a>' for n, u in NAV)
    svc = "".join(f'<li><a href="/services/{s["slug"]}">{e(s["name"])}</a></li>' for s in SERVICES)
    cs = "".join(f'<li><a href="/projects/{p["slug"]}">{e(p["short"])}</a></li>' for p in PROJECTS)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(full)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="author" content="{BRAND}">
  <meta name="theme-color" content="#07080D">
  <link rel="canonical" href="{url}">
  <meta name="google-site-verification" content="9KDuOrVRG-VaSCaI2UogYvvNn2mkYmluYzR9lXaMEKY" />
  <meta name="robots" content="{robots or 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'}">
  <meta property="og:locale" content="en_US">
  <link rel="alternate" hreflang="en" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="me" href="https://github.com/ali-saad-khan">
  <link rel="me" href="https://www.linkedin.com/in/saad-ali-khan-01976124a/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{e(full)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(full)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image:alt" content="{e(full)}">
  <meta name="twitter:title" content="{e(full)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  {''.join(ld(s) for s in schema)}
  <script src="/js/theme-init.js"></script>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="scroll-progress" id="scroll-progress" aria-hidden="true"></div>
  <a class="skip-link" href="#main-content">Skip to content</a>

  <header class="navbar">
    <div class="container nav-container">
      <a href="/" class="nav-brand" aria-label="Saad Ali Khan Portfolio Home"><span class="brand-tag">&lt;</span>SAAD<span class="brand-tag">/&gt;</span><span class="brand-dot"></span></a>
      <div class="nav-right">
        <nav class="nav-menu" id="nav-menu" aria-label="Main Navigation">{nav}</nav>
        <button id="theme-toggle" class="theme-toggle" aria-label="Toggle Light and Dark Mode">
          <svg class="icon-svg icon-moon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
          <svg class="icon-svg icon-sun" viewBox="0 0 24 24"><path d="M12 7a5 5 0 100 10 5 5 0 000-10zM2 13h2a1 1 0 100-2H2a1 1 0 100 2zm18 0h2a1 1 0 100-2h-2a1 1 0 100 2zm-9 8h2a1 1 0 100-2h-2a1 1 0 100 2zm0-18h2a1 1 0 100-2h-2a1 1 0 100 2zM5.636 19.778l1.414-1.414a1 1 0 10-1.414-1.414L4.222 18.364a1 1 0 101.414 1.414zm14.142-14.142l-1.414 1.414a1 1 0 001.414 1.414l1.414-1.414a1 1 0 00-1.414-1.414zM4.222 5.636l1.414 1.414a1 1 0 001.414-1.414L5.636 4.222a1 1 0 00-1.414 1.414zm14.142 14.142l1.414-1.414a1 1 0 00-1.414-1.414l-1.414 1.414a1 1 0 001.414 1.414z"/></svg>
        </button>
        <a href="/contact" class="btn btn-primary btn-sm nav-cta">Hire Me</a>
        <button class="mobile-toggle" aria-label="Toggle Mobile Navigation" aria-expanded="false"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>

  <main id="main-content">
{body}
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-about">
          <div class="footer-brand">&lt;SAAD ALI KHAN /&gt;</div>
          <p>Laravel &amp; PHP engineer in Karachi, Pakistan. I build secure backends, REST APIs, payment systems and e-commerce platforms for clients worldwide.</p>
          <a href="mailto:{EMAIL}" class="footer-link">{EMAIL}</a>
        </div>
        <div><h4 class="footer-heading">Pages</h4><ul>{''.join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV)}</ul></div>
        <div><h4 class="footer-heading">Services</h4><ul>{svc}</ul></div>
        <div><h4 class="footer-heading">Case studies</h4><ul>{cs}</ul></div>
      </div>
      <div class="footer-bottom">
        <div class="copyright">&copy; <span id="current-year">2026</span> {BRAND}. All rights reserved.</div>
        <div class="footer-links">
          <a href="{GITHUB}" target="_blank" rel="noopener noreferrer" class="footer-link">GitHub</a>
          <a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer" class="footer-link">LinkedIn</a>
        </div>
      </div>
    </div>
  </footer>

  <script src="/js/script.js"></script>
</body>
</html>
'''


def breadcrumb_html(items):
    parts = []
    for i, (n, p) in enumerate(items):
        parts.append(f'<span aria-current="page">{e(n)}</span>' if i == len(items) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="breadcrumb" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(parts) + "</nav>"


def hero(items, tag, title, lead, cover=None, alt="", actions="", meta_chips=()):
    chips = "".join(f'<span class="badge badge-cyan">{e(c)}</span>' for c in meta_chips)
    art = (f'<figure class="cover-frame reveal"><img src="/assets/images/covers/{cover}.svg" width="1200" height="675" alt="{e(alt)}" fetchpriority="high"></figure>' if cover else "")
    return f'''    <section class="page-hero">
      <div class="container">
        {breadcrumb_html(items)}
        <div class="page-hero-grid{' no-art' if not cover else ''}">
          <div class="page-hero-text">
            <span class="section-tag">{e(tag)}</span>
            <h1 class="page-title">{e(title)}</h1>
            <p class="page-lead">{h(lead)}</p>
            {f'<div class="chip-row">{chips}</div>' if chips else ''}
            {actions}
          </div>
          {art}
        </div>
      </div>
    </section>'''


def cta(title="Have a project like this in mind?", text="Tell me what you're building. I'll reply by email with questions or a suggested approach."):
    return f'''    <section class="section cta-section">
      <div class="container">
        <div class="cta-band reveal">
          <h2>{e(title)}</h2>
          <p>{e(text)}</p>
          <div class="hero-actions" style="justify-content:center">
            <a href="/contact" class="btn btn-primary">Start a Project</a>
            <a href="mailto:{EMAIL}?subject=Project%20inquiry" class="btn btn-secondary">Email Me</a>
          </div>
        </div>
      </div>
    </section>'''


def project_card(p, size=""):
    badge = '<span class="badge badge-green">Open Source</span>' if p["kind"] == "open" else '<span class="badge badge-cyan">Production · Private</span>'
    return f'''<article class="project-card media-card reveal">
  <a class="card-media" href="/projects/{p["slug"]}" tabindex="-1" aria-hidden="true"><img src="/assets/images/covers/{p["cover"]}.svg" width="1200" height="675" loading="lazy" decoding="async" alt=""></a>
  <div class="project-top">
    <div class="project-meta"><span class="project-category">{e(p["cat"])}</span>{badge}</div>
    <h3 class="project-title"><a href="/projects/{p["slug"]}">{e(p["title"])}</a></h3>
    <p class="project-description">{h(p["lead"])}</p>
  </div>
  <div class="project-bottom">
    <a href="/projects/{p["slug"]}" class="btn btn-primary btn-sm">Read case study</a>
    {f'<a href="{p["repo"]}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-sm">View code</a>' if p["kind"] == "open" else ''}
  </div>
</article>'''


def service_card(s):
    return f'''<article class="service-card media-card reveal">
  <a class="card-media" href="/services/{s["slug"]}" tabindex="-1" aria-hidden="true"><img src="/assets/images/covers/{s["cover"]}.svg" width="1200" height="675" loading="lazy" decoding="async" alt=""></a>
  <h3 class="service-title"><a href="/services/{s["slug"]}">{e(s["name"])}</a></h3>
  <p class="service-description">{h(s["short"])}</p>
  <a href="/services/{s["slug"]}" class="card-link">Learn more &rarr;</a>
</article>'''


# ---------------------------------------------------------------- pages
def build_case_study(p):
    path = f"/projects/{p['slug']}"
    items = [("Home", "/"), ("Projects", "/projects"), (p["short"], path)]
    badge_text = "Open source" if p["kind"] == "open" else "Production work (private code)"
    actions = ""
    if p["kind"] == "open":
        actions = f'<div class="hero-actions"><a href="{p["repo"]}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">View code on GitHub</a><a href="/contact" class="btn btn-secondary">Start a Project</a></div>'
    else:
        actions = '<div class="hero-actions"><a href="/contact" class="btn btn-primary">Start a Project</a><a href="/projects" class="btn btn-secondary">All case studies</a></div>'
    facts = "".join(f'<div class="stat-card"><div class="stat-number" style="font-size:1.6rem">{e(a)}</div><div class="stat-label">{e(b)}</div></div>' for a, b in p["facts"])
    approach = "".join(f'<li class="approach-item"><span class="approach-num">{i+1:02d}</span><div><h3>{e(a)}</h3><p>{h(b)}</p></div></li>' for i, (a, b) in enumerate(p["approach"]))
    did = "".join(f"<li>{h(x)}</li>" for x in p["did"])
    proves = "".join(f"<li>{h(x)}</li>" for x in p["proves"])
    tradeoffs = ""
    if p.get("tradeoffs"):
        tradeoffs = '<h2>Deliberate trade-offs</h2><ul class="check-list">' + "".join(f"<li>{h(x)}</li>" for x in p["tradeoffs"]) + "</ul>"
    note = f'<div class="callout">{h(p["note"])}</div>' if p.get("note") else ""
    stack = "".join(f'<span class="project-tag">{e(x)}</span>' for x in p["stack"])
    rel = "".join(project_card(PMAP[r]) for r in p["related"][:2])
    svcs = "".join(f'<li><a href="/services/{s}">{e(SMAP[s]["name"])}</a></li>' for s in p["services"])
    body = hero(items, "// CASE STUDY", p["title"], p["lead"], p["cover"], f"Illustration of the {p['short']} project", actions, [badge_text, p["cat"].split(" / ")[0]])
    body += f'''
    <section class="section tight">
      <div class="container">
        <div class="fact-grid reveal">{facts}</div>
      </div>
    </section>
    <section class="section tight">
      <div class="container article-grid">
        <article class="prose">
          <h2>The challenge</h2>
          {''.join(f"<p>{h(x)}</p>" for x in p["challenge"])}
          <h2>How I approached it</h2>
          <ol class="approach-list">{approach}</ol>
          {tradeoffs}
          <h2>What I built</h2>
          <ul class="check-list">{did}</ul>
          {note}
          <h2>What this project demonstrates</h2>
          <ul class="check-list">{proves}</ul>
        </article>
        <aside class="side-card-wrap">
          <div class="side-card"><h3>Tech stack</h3><div class="project-tags">{stack}</div></div>
          <div class="side-card"><h3>Related services</h3><ul class="link-list">{svcs}</ul></div>
          <div class="side-card side-cta"><h3>Need something similar?</h3><p>I take on freelance and contract projects.</p><a href="/contact" class="btn btn-primary btn-sm">Get in touch</a></div>
        </aside>
      </div>
    </section>
    <section class="section section-alt">
      <div class="container">
        <div class="section-header reveal"><span class="section-tag">// MORE WORK</span><h2 class="section-title">Related case studies</h2></div>
        <div class="projects-grid">{rel}</div>
      </div>
    </section>
{cta()}'''
    schema = [crumbs(items),
              {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["meta"],
               "image": f"{SITE}/assets/images/og/{p['slug']}.png", "author": PERSON, "datePublished": TODAY, "dateModified": TODAY,
               "mainEntityOfPage": SITE + path, "publisher": PERSON}]
    if p["kind"] == "open":
        schema.append({"@context": "https://schema.org", "@type": "SoftwareSourceCode", "name": p["short"], "codeRepository": p["repo"],
                       "author": PERSON, "description": p["lead"], "programmingLanguage": p["stack"][0], "url": SITE + path})
    return path, page(path, p["title"], p["meta"], body, "Projects", schema, og=p["slug"])


def build_service(s):
    path = f"/services/{s['slug']}"
    items = [("Home", "/"), ("Services", "/services"), (s["name"], path)]
    body = hero(items, "// SERVICE", s["title"], s["lead"], s["cover"], f"Illustration for {s['name']}",
                '<div class="hero-actions"><a href="/contact" class="btn btn-primary">Get a Quote</a><a href="/projects" class="btn btn-secondary">See my work</a></div>')
    pts = "".join(f"<li>{h(x)}</li>" for x in s["points"])
    cases = "".join(project_card(PMAP[c]) for c in s["cases"][:2])
    faqs = "".join(f'<details class="faq-item"><summary>{e(q)}</summary><p>{h(a)}</p></details>' for q, a in s["faqs"])
    others = "".join(f'<li><a href="/services/{o["slug"]}">{e(o["name"])}</a></li>' for o in SERVICES if o["slug"] != s["slug"])
    body += f'''
    <section class="section tight">
      <div class="container article-grid">
        <article class="prose">
          {''.join(f"<p>{h(x)}</p>" for x in s["body"])}
          <h2>What you get</h2>
          <ul class="check-list">{pts}</ul>
          <h2>Frequently asked questions</h2>
          <div class="faq">{faqs}</div>
        </article>
        <aside class="side-card-wrap">
          <div class="side-card side-cta"><h3>Let's talk about your project</h3><p>Freelance and contract work, remote and worldwide. Based in Karachi, Pakistan.</p><a href="/contact" class="btn btn-primary btn-sm">Start a Project</a></div>
          <div class="side-card"><h3>Other services</h3><ul class="link-list">{others}</ul></div>
        </aside>
      </div>
    </section>
    <section class="section section-alt">
      <div class="container">
        <div class="section-header reveal"><span class="section-tag">// PROOF</span><h2 class="section-title">Related case studies</h2><p class="section-subtitle">Real projects behind this service.</p></div>
        <div class="projects-grid">{cases}</div>
      </div>
    </section>
{cta("Ready to get started?", "Send a short description of what you need and I'll reply by email.")}'''
    schema = [crumbs(items),
              {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "description": s["meta"], "url": SITE + path,
               "serviceType": s["name"], "areaServed": "Worldwide", "provider": {"@type": "ProfessionalService", "name": BRAND, "url": SITE + "/", "email": EMAIL}},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                  {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in s["faqs"]]}]
    return path, page(path, s["title"], s["meta"], body, "Services", schema, og=s["slug"])


def build_projects_index():
    path = "/projects"
    items = [("Home", "/"), ("Projects", path)]
    openp = "".join(project_card(p) for p in PROJECTS if p["kind"] == "open")
    priv = "".join(project_card(p) for p in PROJECTS if p["kind"] != "open")
    body = hero(items, "// PROJECTS & CASE STUDIES", "Laravel, API and E-commerce Case Studies",
                "Two open-source builds you can read line by line, and four pieces of production work delivered at Technyx. Each case study explains the problem, the decisions and the result.",
                None)
    body += f'''
    <section class="section tight">
      <div class="container">
        <div class="section-header reveal"><span class="section-tag">// OPEN SOURCE</span><h2 class="section-title">Code you can audit</h2><p class="section-subtitle">Public repositories with tests and architecture docs.</p></div>
        <div class="projects-grid">{openp}</div>
      </div>
    </section>
    <section class="section section-alt">
      <div class="container">
        <div class="section-header reveal"><span class="section-tag">// PRODUCTION WORK</span><h2 class="section-title">Delivered at Technyx</h2><p class="section-subtitle">Client and employer code is private, so these case studies describe the problem and approach without exposing anything confidential.</p></div>
        <div class="projects-grid">{priv}</div>
      </div>
    </section>
{cta()}'''
    schema = [crumbs(items),
              {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Projects and case studies", "url": SITE + path,
               "mainEntity": {"@type": "ItemList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/projects/{p['slug']}", "name": p["title"]} for i, p in enumerate(PROJECTS)]}}]
    return path, page(path, "Laravel & API Case Studies",
                      "Case studies from a Laravel & PHP developer: open-source wallet ledger API, Next.js store, subscription backend, WordPress and payment integrations.",
                      body, "Projects", schema, og="projects")


def build_services_index():
    path = "/services"
    items = [("Home", "/"), ("Services", path)]
    body = hero(items, "// SERVICES", "Laravel, API & E-commerce Development Services",
                "Backend engineering for businesses that need software to stay correct: Laravel applications, REST APIs, payment integrations, database work, WordPress and e-commerce.", None)
    body += f'''
    <section class="section tight">
      <div class="container">
        <div class="services-grid">{''.join(service_card(s) for s in SERVICES)}</div>
      </div>
    </section>
    <section class="section section-alt">
      <div class="container">
        <div class="section-header reveal"><span class="section-tag">// PROCESS</span><h2 class="section-title">How a project runs</h2></div>
        <div class="approach-steps reveal">
          <div class="step-card"><span class="step-number">01</span><h3 class="step-title">Understand</h3><p class="step-description">Requirements, existing systems, data flows and constraints before any code.</p></div>
          <div class="step-card"><span class="step-number">02</span><h3 class="step-title">Design</h3><p class="step-description">Schemas, API payloads, relationships and system architecture.</p></div>
          <div class="step-card"><span class="step-number">03</span><h3 class="step-title">Build</h3><p class="step-description">Clean, readable, maintainable backend logic and responsive frontend.</p></div>
          <div class="step-card"><span class="step-number">04</span><h3 class="step-title">Test</h3><p class="step-description">Edge cases, database constraints, input validation and end-to-end flows.</p></div>
          <div class="step-card"><span class="step-number">05</span><h3 class="step-title">Deploy &amp; Maintain</h3><p class="step-description">Production deployment, server configuration, monitoring and root-cause debugging.</p></div>
        </div>
      </div>
    </section>
{cta()}'''
    schema = [crumbs(items), {"@context": "https://schema.org", "@type": "ProfessionalService", "name": BRAND, "url": SITE + "/", "email": EMAIL,
              "areaServed": "Worldwide", "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Development services", "itemListElement": [
                  {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{SITE}/services/{s['slug']}"}} for s in SERVICES]}}]
    return path, page(path, "Laravel, PHP & API Development Services",
                      "Freelance Laravel & PHP developer services: Laravel development, REST APIs, payment gateway integration, MySQL, WordPress, Shopify and production debugging.",
                      body, "Services", schema, og="services")


def build_about():
    path = "/about"
    items = [("Home", "/"), ("About", path)]
    body = hero(items, "// ABOUT ME", "Saad Ali Khan: Laravel & PHP Engineer in Karachi",
                "I build the backend your business depends on: secure APIs, payment flows and wallet systems that stay correct under load. Software Engineer at Technyx, available for freelance and contract projects.",
                "about", "Illustration with the initials SK, stack tags and a developer profile",
                '<div class="hero-actions"><a href="/contact" class="btn btn-primary">Work With Me</a><a href="/projects" class="btn btn-secondary">See case studies</a></div>',
                ["Karachi, Pakistan", "Remote · worldwide"])
    body += f'''
    <section class="section tight">
      <div class="container article-grid">
        <article class="prose">
          <h2>Who I am</h2>
          <p>I'm a <strong>Software Engineer at Technyx</strong> in Karachi, specializing in PHP, Laravel, MySQL and modern web application development. I enjoy building practical software that solves real business requirements rather than over-engineering simple problems.</p>
          <p><strong>Backend development is my core strength.</strong> I work extensively with PHP and the Laravel framework, modeling relational database schemas, engineering RESTful APIs and implementing business logic for applications with complex user flows, subscription plans, wallets and delivery operations.</p>
          <h2>What I work on day to day</h2>
          <p>Beyond custom web applications, I maintain enterprise <strong>WordPress installations</strong> (ACF, Elementor, Custom Post Types) and customize <strong>Shopify</strong> stores. I'm comfortable on Linux servers (Apache, Nginx, PHP-FPM, Caddy), managing deployments and troubleshooting production bugs under pressure.</p>
          <h2>How I think about software</h2>
          <p>I treat development as a full lifecycle: understand the business requirement, plan the database relationships, build clean backend and frontend code, validate data integrity, deploy securely and debug root causes instead of symptoms.</p>
          <blockquote class="pull-quote">"Good software isn't just code that works. It's code that remains understandable, testable and maintainable when the requirements change."</blockquote>
          <ul class="check-list">
            <li>Keep business logic explicit and centralized.</li>
            <li>Protect data integrity with database constraints and transactions.</li>
            <li>Validate all user and API inputs strictly.</li>
            <li>Handle boundary cases and unexpected failures gracefully.</li>
            <li>Understand the database execution plan, not just the ORM syntax.</li>
            <li>Keep production systems reliable, fast and secure.</li>
          </ul>
          <h2>Experience</h2>
          <p><strong>Software Engineer, Technyx (Karachi, Pakistan), August 2023 to present.</strong> Developing and maintaining Laravel and PHP backends for production applications; designing MySQL schemas including user accounts, meal plans and transactional ledgers; building REST APIs for web, mobile and external integrations; integrating payment gateways with request signing and webhook verification; restructuring a 800+ page WordPress site; customizing Shopify themes; and troubleshooting production servers.</p>
          <h2>Don't take my word for it</h2>
          <p>Two of my projects are public with tests and architecture docs: <a href="/projects/fincore-wallet-ledger-api">FinCore</a>, a double-entry wallet ledger API, and <a href="/projects/my-store-ecommerce-platform">my-store</a>, a production e-commerce platform. Read the code before you decide to hire me.</p>
        </article>
        <aside class="side-card-wrap">
          <div class="side-card"><h3>At a glance</h3>
            <ul class="link-list plain"><li><strong>3+</strong> years professional experience</li><li><strong>800+</strong> WordPress pages restructured</li><li><strong>50+</strong> automated tests in public projects</li><li><strong>2</strong> open-source case studies</li></ul></div>
          <div class="side-card"><h3>Core stack</h3><div class="project-tags">{''.join(f'<span class="project-tag">{x}</span>' for x in ["PHP", "Laravel", "MySQL", "REST APIs", "PostgreSQL", "Next.js", "WordPress", "Shopify", "Linux", "Nginx"])}</div></div>
          <div class="side-card"><h3>Services</h3><ul class="link-list">{''.join(f'<li><a href="/services/{s["slug"]}">{e(s["name"])}</a></li>' for s in SERVICES)}</ul></div>
          <div class="side-card side-cta"><h3>Let's work together</h3><p>Freelance and contract projects, remote.</p><a href="/contact" class="btn btn-primary btn-sm">Contact me</a></div>
        </aside>
      </div>
    </section>
{cta("Want a backend you can trust?")}'''
    schema = [crumbs(items), {"@context": "https://schema.org", "@type": "ProfilePage", "url": SITE + path, "name": "About Saad Ali Khan", "mainEntity": PERSON}]
    return path, page(path, "About Saad Ali Khan: Laravel & PHP Engineer",
                      "Saad Ali Khan is a Software Engineer at Technyx in Karachi with 3+ years of Laravel, PHP and MySQL experience, available for freelance projects.",
                      body, "About", schema, og="about")


def build_contact():
    path = "/contact"
    items = [("Home", "/"), ("Contact", path)]
    body = hero(items, "// CONTACT", "Hire a Laravel & PHP Developer",
                "Tell me about your project: what you're building, the problem you're stuck on, and any deadlines. I reply by email, usually with questions or a suggested approach.", None)
    body += f'''
    <section class="section tight">
      <div class="container">
        <div class="contact-grid">
          <div class="contact-info reveal">
            <div class="contact-card"><div class="contact-icon"><svg class="icon-svg" viewBox="0 0 24 24"><path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg></div><div class="contact-details"><label>Direct Email</label><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
            <div class="contact-card"><div class="contact-icon"><svg class="icon-svg" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg></div><div class="contact-details"><label>GitHub Profile</label><a href="{GITHUB}" target="_blank" rel="noopener noreferrer">github.com/ali-saad-khan</a></div></div>
            <div class="contact-card"><div class="contact-icon"><svg class="icon-svg" viewBox="0 0 24 24"><path d="M19 3a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h14m-.5 15.5v-5.3a3.26 3.26 0 00-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 011.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 001.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 00-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg></div><div class="contact-details"><label>LinkedIn Profile</label><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">linkedin.com/in/saad-ali-khan-01976124a</a></div></div>
            <div class="side-card"><h3>What helps me reply faster</h3><ul class="check-list"><li>What the project or problem is</li><li>Your current stack (if any)</li><li>Timeline and rough budget</li><li>Links to the site or repository</li></ul></div>
          </div>
          <div class="contact-form-container reveal">
            <form id="contact-form" class="contact-form" method="POST" novalidate>
              <div class="form-group" style="position:absolute;left:-9999px;" aria-hidden="true"><label for="website">Leave this empty</label><input type="text" id="website" name="website" tabindex="-1" autocomplete="off"></div>
              <div class="form-group"><label for="name" class="form-label">Your Name</label><input type="text" id="name" name="name" class="form-input" placeholder="e.g. John Doe" autocomplete="name" required></div>
              <div class="form-group"><label for="email" class="form-label">Email Address</label><input type="email" id="email" name="email" class="form-input" placeholder="e.g. john@example.com" autocomplete="email" required></div>
              <div class="form-group"><label for="message" class="form-label">Project Details / Message</label><textarea id="message" name="message" class="form-textarea" placeholder="Tell me about your project requirements or technical problem..." required></textarea></div>
              <button type="submit" class="btn btn-primary" style="width: 100%;">Send Message <svg class="icon-svg" viewBox="0 0 24 24"><path d="M14 5l7 7m0 0l-7 7m7-7H3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg></button>
              <div id="form-status" class="form-status" role="alert"></div>
            </form>
          </div>
        </div>
      </div>
    </section>'''
    schema = [crumbs(items), {"@context": "https://schema.org", "@type": "ContactPage", "url": SITE + path, "mainEntity": PERSON}]
    return path, page(path, "Hire a Laravel & PHP Developer: Contact",
                      "Contact Saad Ali Khan to hire a freelance Laravel & PHP developer for APIs, payment integrations, WordPress or e-commerce projects. Remote, based in Karachi.",
                      body, "Contact", schema, og="contact")


def post_card(b):
    return f'''<article class="project-card media-card reveal">
  <a class="card-media" href="/blog/{b["slug"]}" tabindex="-1" aria-hidden="true"><img src="/assets/images/covers/{b["cover"]}.svg" width="1200" height="675" loading="lazy" decoding="async" alt=""></a>
  <div class="project-top">
    <div class="project-meta"><span class="project-category">{e(b["tag"])}</span><span class="badge badge-cyan">{b["read"]} min read</span></div>
    <h3 class="project-title"><a href="/blog/{b["slug"]}">{e(b["title"])}</a></h3>
    <p class="project-description">{h(b["lead"])}</p>
  </div>
  <div class="project-bottom"><a href="/blog/{b["slug"]}" class="btn btn-primary btn-sm">Read article</a></div>
</article>'''


def build_blog_index():
    path = "/blog"
    items = [("Home", "/"), ("Blog", path)]
    body = hero(items, "// BLOG", "Laravel, API and Payments Engineering Notes",
                "Practical, original write-ups on building secure Laravel backends: payment webhooks, wallet ledgers, REST API design and performance. Written by me, from how I build software.", None)
    body += f'''
    <section class="section tight">
      <div class="container"><div class="projects-grid">{"".join(post_card(b) for b in POSTS)}</div></div>
    </section>
{cta("Need this built properly?", "If one of these topics is what your project needs, send me a short description and I'll reply by email.")}'''
    schema = [crumbs(items),
              {"@context": "https://schema.org", "@type": "Blog", "name": "Saad Ali Khan: Laravel & API Engineering Blog", "url": SITE + path,
               "author": {"@id": SITE + "/#person"}, "inLanguage": "en",
               "blogPost": [{"@type": "BlogPosting", "headline": b["title"], "url": f"{SITE}/blog/{b['slug']}"} for b in POSTS]}]
    return path, page(path, "Laravel & API Engineering Blog",
                      "Original articles by a Laravel & PHP developer on payment webhooks, wallet ledgers, REST API design, performance and hiring a Laravel developer.",
                      body, "Blog", schema, og="blog")


def build_post(b):
    path = f"/blog/{b['slug']}"
    items = [("Home", "/"), ("Blog", "/blog"), (b["tag"], path)]
    items[2] = (b["title"], path)
    body = hero(items[:2] + [(b["tag"] + " article", path)], "// " + b["tag"].upper(), b["title"], b["lead"], b["cover"], b["title"],
                "", meta_chips=(f"{b['read']} min read", "By Saad Ali Khan", "Oct 2026"))
    svc, case = SMAP[b["related_service"]], PMAP[b["related_case"]]
    others = "".join(f'<li><a href="/blog/{o["slug"]}">{e(o["title"])}</a></li>' for o in POSTS if o["slug"] != b["slug"])
    body += f'''
    <section class="section tight">
      <div class="container article-grid">
        <article class="prose">
{b["body"]}
          <p class="post-note">Original article written by Saad Ali Khan. Code samples are illustrative and free to adapt in your own projects.</p>
        </article>
        <aside class="side-card-wrap">
          <div class="side-card side-cta"><h3>Need help with this?</h3><p>Freelance Laravel &amp; PHP development, remote and worldwide.</p><a href="/contact" class="btn btn-primary btn-sm">Start a Project</a></div>
          <div class="side-card"><h3>Related</h3><ul class="link-list"><li><a href="/services/{svc["slug"]}">{e(svc["name"])}</a></li><li><a href="/projects/{case["slug"]}">Case study: {e(case["short"])}</a></li></ul></div>
          <div class="side-card"><h3>More articles</h3><ul class="link-list">{others}</ul></div>
        </aside>
      </div>
    </section>
{cta("Want this done right in your project?", "Send a short description and I'll reply by email with questions or a suggested approach.")}'''
    img = f"{SITE}/assets/images/og/blog-{b['slug']}.png"
    schema = [crumbs(items),
              {"@context": "https://schema.org", "@type": "BlogPosting", "headline": b["title"], "description": b["meta"],
               "url": SITE + path, "mainEntityOfPage": SITE + path, "image": img, "inLanguage": "en",
               "datePublished": TODAY, "dateModified": TODAY, "author": PERSON, "publisher": {"@id": SITE + "/#person"},
               "copyrightHolder": {"@id": SITE + "/#person"}, "copyrightYear": 2026, "isPartOf": {"@type": "Blog", "url": SITE + "/blog"}}]
    return path, page(path, b["title"], b["meta"], body, "Blog", schema, og="blog-" + b["slug"])


# ---------------------------------------------------------------- output
def write(path, content):
    f = os.path.join(ROOT, path.lstrip("/") + ".html")
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, "w") as fh:
        fh.write(content)
    return f


def sitemap(paths):
    prio = {"/": "1.0", "/about": "0.8", "/projects": "0.9", "/services": "0.9", "/contact": "0.7", "/blog": "0.8"}
    rows = "".join(f"  <url>\n    <loc>{SITE}{p if p != '/' else '/'}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{prio.get(p, '0.8')}</priority>\n  </url>\n" for p in paths)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.w3.org/2000/svg">\n'.replace("http://www.w3.org/2000/svg", "http://www.sitemaps.org/schemas/sitemap/0.9") + rows + "</urlset>\n"


def render_og(slug, title, cover):
    out = os.path.join(ROOT, "assets", "images", "og", slug + ".png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cov = os.path.join(ROOT, "assets", "images", "covers", cover + ".svg")
    doc = f'''<html><body style="margin:0;width:1200px;height:630px;background:linear-gradient(135deg,#0B0D18,#1A1240);font-family:Inter,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#fff;position:relative;overflow:hidden">
<img src="file://{cov}" style="position:absolute;right:-60px;top:70px;width:640px;border-radius:24px;border:1px solid rgba(255,255,255,.15);box-shadow:0 30px 80px rgba(139,124,255,.45)">
<div style="position:absolute;left:64px;top:64px;font:600 22px ui-monospace,Menlo,monospace;color:#22D3EE">&lt;SAAD/&gt; saadconsulting.tech</div>
<div style="position:absolute;left:64px;top:190px;width:560px;font-size:56px;line-height:1.08;font-weight:800;letter-spacing:-0.03em">{e(title)}</div>
<div style="position:absolute;left:64px;bottom:64px;font-size:26px;color:#B6BCCB">Saad Ali Khan · Laravel &amp; PHP Developer</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:8px;background:linear-gradient(90deg,#8B7CFF,#22D3EE,#F472B6)"></div></body></html>'''
    tmp = tempfile.mkdtemp()
    f = os.path.join(tmp, "og.html")
    open(f, "w").write(doc)
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630",
                    f"--screenshot={out}", "file://" + f], check=True, capture_output=True)


def main():
    pages = [build_about(), build_projects_index(), build_services_index(), build_contact(), build_blog_index()]
    pages += [build_post(b) for b in POSTS]
    pages += [build_case_study(p) for p in PROJECTS] + [build_service(s) for s in SERVICES]
    for path, content in pages:
        write(path, content)
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as fh:
        fh.write(sitemap(["/"] + [p for p, _ in pages]))
    print("built", len(pages), "pages")
    if "--og" in sys.argv:
        jobs = [("about", "About Saad Ali Khan", "about"), ("projects", "Projects & Case Studies", "fincore-ledger"),
                ("services", "Laravel, API & E-commerce Services", "rest-api"), ("contact", "Hire a Laravel & PHP Developer", "laravel-code")]
        jobs += [("blog", "Laravel & API Engineering Blog", "laravel-code")] + [("blog-" + b["slug"], b["title"], b["cover"]) for b in POSTS]
        jobs += [(p["slug"], p["title"], p["cover"]) for p in PROJECTS] + [(s["slug"], s["title"], s["cover"]) for s in SERVICES]
        for j in jobs:
            render_og(*j)
        print("rendered", len(jobs), "social images")


if __name__ == "__main__":
    main()
