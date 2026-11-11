"""Generates every page of the site (index.html and portfolio/<project>/index.html).

Run from anywhere:   python3 tools/build.py      (needs Pillow: pip install pillow)
See tools/README.md for what to edit.
"""
import json,re,os,html
HERE=os.path.dirname(os.path.abspath(__file__))
S=HERE+'/content/'                       # case-study content (one JSON file per project)
R=os.path.dirname(HERE)+'/'              # repository root: pages are written here
NAME='Olga Tochilin'
# order as on the original homepage
PROJECTS=[
 dict(slug='patpat',src='patpat',title='PatPat Search Revamp',cat='Mobile App',client='PatPat',role='Lead Designer',team='Product Manager / Researcher / Two iOS engineers / QA specialist',thumb='patpat-featured-5.webp'),
 dict(slug='midland',src='midland',title='Midland State Bank Color System Overhaul',cat='Design Systems',client='Midland State Bank',role='Lead Designer',thumb='midland-featured-5.webp'),
 dict(slug='lucid',src='lucid',title='Lucid Motors',cat='Web Design',client='Lucid Motors',role='Lead Designer',thumb='lucid-featured-5.webp'),
 dict(slug='outdoorsy',src='outdoorsy',title='Bonfire: Outdoorsy Design System',card='Outdoorsy',cat='Design Systems',client='Outdoorsy',role='Lead Designer',thumb='outdoorsy-featured-5.webp'),
 dict(slug='jpmorgan-chase',src='jpmorgan-chase',title='JP Morgan Chase HR Portal',card='JPMorgan Chase',cat='Web Design',client='JP Morgan Chase',role='Lead Designer',thumb='jpmc-featured-5.webp'),
 dict(slug='franky',src='franky',title='Frankenstein\u2019s Input Field',thumb='franky-featured.webp'),
 dict(slug='mayo',src='mayo',title='Mayo Clinic',thumb='mayo-featured.webp'),
]
EXPERIENCE=[('Founding Designer','MacroFactor','2025 – Present'),('Design Lead','Code & Theory','2023'),('Sr. Product Designer','YML','2021'),('Sr. Product Designer','Alight Solutions','2020'),('UX Designer','United Airlines','2019'),('Product Designer','Walgreens','2018'),('Product Designer','BookingWhale','2016')]
e=html.escape


ICON={
 'brief':'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/></svg>',
 'layers':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/></svg>',
 'pen':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h4L19 9a2.8 2.8 0 0 0-4-4L4 16v4Z"/><path d="m13.5 6.5 4 4"/></svg>',
 'ext':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
}

PROBLEMS=[
 ('Multiple and incomplete component libraries','Outdoorsy had six incomplete component libraries with inconsistent names, causing inefficiency and confusion.'),
 ('No consistency between Design and Code','Designers and developers lacked a shared source of truth, leading to confusion and misaligned components.'),
 ('Inefficient collaboration without a Design System','Designers and developers repeatedly built the same components, losing focus on user experience and wasting time coding slight variations of the same elements.'),
 ('Inconsistent UI across products','These issues led to a disjointed UI, compromising the brand\u2019s identity across all products.'),
 ('Messy Code','Inconsistent designs led to messy code that was hard to maintain. Without component-based code, developers had to manually update every instance of an element\u2014a true nightmare.'),
 ('Compromised Accessibility','Designers and developers lacked accessibility standards. Many components violated accessibility guidelines, such as color contrast, spacing, clickable areas, font size, and tab order.'),
]
PROBLEM_TITLES={t for t,_ in PROBLEMS}
# first image of each pair that is shown side by side with the image that follows it
ROW_FIRST={'What-is-outdoorsy-1','bonfire-colors','bonfire-icons','bonfire-units'}

# Selected work captions: slug -> (title, company), as provided by the owner
WORK_CAPTION={
 'patpat':('Search Revamp','PatPat'),
 'midland':('Semantic color system','Midland State Bank'),
 'lucid':('Lucid Cars\u2019 website redesign','Lucid Motors'),
 'outdoorsy':('Bonfire: Outdoorsy Design System','Outdoorsy'),
 'jpmorgan-chase':('HR Portal','JP Morgan Chase'),
 'franky':('Frankenstein\u2019s Input Field','Personal project'),
 'mayo':('Design System components','Mayo Clinic'),
}
def work_item(p,up=''):
    t,sub=WORK_CAPTION[p['slug']]
    return f'''<a class="work-item" href="{up}portfolio/{p['slug']}/">
  <span class="work-img"><img src="{up}assets/img/{p['thumb']}" alt="" width="1200" height="509" loading="lazy"></span>
  <span class="work-cap"><span class="work-title">{e(t)}</span><span class="work-sub">{e(sub)}</span></span>
</a>'''

def page(title,body,depth,desc='',back=False):
    up='../'*depth
    if back:   # case studies: the logo becomes a back button (arrow + name) to the work list
        brand_link=f'''<a class="brand brand-back" href="{up}#work" aria-label="Back to all work"><span class="mono"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></span><span class="brand-name">{NAME}</span></a>'''
    else:
        brand_link=f'''<a class="brand" href="{up or './'}"><span class="mono">OT</span><span class="brand-name">{NAME}</span></a>'''
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<script>document.documentElement.classList.add('js')</script>
<link rel="preload" href="{up}assets/fonts/HostGrotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    {brand_link}
    <nav>
      <a href="{up}#work">Work</a>
      <a href="{up}#experience">Experience</a>
      <a class="nav-cta" href="https://www.linkedin.com/in/olgatoc/" target="_blank" rel="noopener noreferrer"><span>LinkedIn</span>{ICON['ext']}<span class="sr-only"> (opens in a new tab)</span></a>
    </nav>
  </div>
</header>
{body}
<footer class="site-footer"><span>© {NAME} · 2026</span><a href="#top" class="to-top">Back to top ↑</a></footer>
<script src="{up}assets/site.js" defer></script>
</body>
</html>
"""

def head_line(title,num):
    return f'<h2 class="section-head"><span>{title}</span><i></i>{f"<b>{num:02d}</b>" if num else ""}</h2>'

def img_dims(fn):
    """(width, height) of a file in assets/img; works for raster and svg."""
    path=R+'assets/img/'+fn
    if fn.endswith('.svg'):
        m=re.search(r'<svg[^>]*?\bwidth="([\d.]+)"[^>]*?\bheight="([\d.]+)"',open(path,encoding='utf8').read(4000))
        return (round(float(m.group(1))),round(float(m.group(2)))) if m else None
    from PIL import Image
    return Image.open(path).size

def render_blocks(blocks,p):
    if p['slug']=='midland':
        # In the source, 'Key takeaways' sits right under 'Results' and splits it from its own
        # images. Move it (heading, intro and bullets) to the end, just above the thank-you line.
        ks=next(j for j,b in enumerate(blocks) if b[0]=='h2' and b[1]=='Key takeaways')
        ke=next(j for j in range(ks,len(blocks)) if blocks[j][0]=='img')
        seg=blocks[ks:ke]; rest=blocks[:ks]+blocks[ke:]
        te=next(j for j,b in enumerate(rest) if b[0]=='h1' and b[1].startswith('Thank you'))
        blocks=rest[:te]+seg+rest[te:]
    out=[];i=0;n=len(blocks);sec=0;decisions=False
    while blocks[i][0]!='h1': i+=1
    i+=1
    while i<n:
        t=blocks[i]; k=t[0]
        if k=='h6': i+=1; continue
        if k=='h1' and re.fullmatch(r'\d+%',t[1]):
            items=[]
            while i<n and blocks[i][0]=='h1' and re.fullmatch(r'\d+%',blocks[i][1]):
                num=blocks[i][1]; lab=blocks[i+1][1]; txt=blocks[i+2][1]
                items.append(f'<div class="stat"><div class="num">{num}</div><h3>{lab}</h3><p>{txt}</p></div>')
                i+=3
            out.append('<div class="stats">'+''.join(items)+'</div>'); continue
        if k=='h1':
            if t[1].startswith('Thank you'): out.append(f'<p class="thanks">{t[1]}</p>')
            else:
                sec+=1; out.append(head_line(t[1],sec))
        elif k=='h2' and t[1]=='Key takeaways':
            # closes the Results part: same section-title style as the other sections, numbered on
            decisions=False; sec+=1; out.append(head_line(t[1],sec))
        elif k=='h2':
            decisions=(p['slug']=='patpat' and t[1]=='Product decisions')
            out.append(f'<h3 class="h">{t[1]}</h3>')
        elif decisions and k in('h3','h4','h5') and i+1<n and blocks[i+1][0]=='p':
            cards=[]
            while i+1<n and blocks[i][0] in('h3','h4','h5') and blocks[i+1][0]=='p':
                num=len(cards)+1
                cards.append(f'<article class="pcard"><span class="pnum">{num:02d}</span><h4>{blocks[i][1]}</h4><p>{blocks[i+1][1]}</p></article>')
                i+=2
            out.append('<div class="pcards">'+''.join(cards)+'</div>'); continue
        elif k=='h4' and p['slug']=='outdoorsy' and t[1] in PROBLEM_TITLES:
            cards=[]
            while i<n and blocks[i][0]=='h4' and blocks[i][1] in PROBLEM_TITLES:
                title=blocks[i][1]; desc=dict(PROBLEMS)[title]; num=len(cards)+1
                cards.append(f'<article class="pcard"><span class="pnum">{num:02d}</span><h4>{title}</h4><p>{desc}</p></article>')
                i+=1
            out.append('<div class="pcards">'+''.join(cards)+'</div>'); continue
        elif k=='meta': pass
        elif k=='pull': out.append(f'<p class="pull">{t[1]}</p>')
        elif k=='thanks': out.append(f'<p class="thanks">{t[1]}</p>')
        elif k=='stat':
            items=[]
            while i<n and blocks[i][0]=='stat':
                num,lab=blocks[i][1]; items.append(f'<div class="stat"><div class="num">{num}</div><h3>{lab}</h3></div>'); i+=1
            out.append('<div class="stats">'+''.join(items)+'</div>'); continue
        elif k=='strip':
            names,section=t[1],t[2] or p['title']
            figs=''.join(f'<figure><img src="../../assets/img/{nm}" alt="{e(section)} \u2013 screenshot {j+1}" width="{img_dims(nm)[0]}" height="{img_dims(nm)[1]}" loading="lazy"></figure>' for j,nm in enumerate(names))
            out.append(f'<div class="strip" tabindex="0" role="group" aria-label="{e(section)} \u2013 screenshots, scroll sideways">{figs}</div>')
        elif k=='img' and len(t)>2 and p['slug'] in('franky','mayo'):
            fn=t[1]; w,h=img_dims(fn); alt=t[2] or p['title']
            cls=' class="figure-small"' if w<400 else ''
            sty=f' style="max-width:{w}px"' if w<400 else ''
            out.append(f'<figure{cls}{sty}><img src="../../assets/img/{fn}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy"></figure>')
        elif k in('h3','h4','h5'): out.append(f'<h4 class="sub">{t[1]}</h4>')
        elif k=='p': out.append(f'<p>{t[1]}</p>')
        elif k=='li':
            items=[]
            while i<n and blocks[i][0]=='li': items.append(f'<li>{blocks[i][1]}</li>'); i+=1
            out.append('<ul>'+''.join(items)+'</ul>'); continue
        elif k=='img':
            f=t[1].split('/')[-1]; b,ext=os.path.splitext(f)
            if ext.lower() in('.png','.jpg','.jpeg'): f=b+'.webp'
            fig=lambda fn: f'<figure><img src="../../assets/img/{fn}" alt="{e(p["title"])} – illustration" loading="lazy"></figure>'
            if os.path.splitext(f)[0] in ROW_FIRST and i+1<n and blocks[i+1][0]=='img':
                # these pairs of same-size images sit side by side in one row
                f2=os.path.splitext(blocks[i+1][1].split('/')[-1])[0]+'.webp'
                out.append('<div class="figure-row">'+fig(f)+fig(f2)+'</div>')
                i+=1
            else:
                out.append(fig(f))
        i+=1
    return '\n'.join(out)


def dots(shape,uid):
    # one <path> of zero-length round-capped segments = a grid of dots, clipped by a shape test
    import math
    def inside(x,y):
        if shape=='square': return x<=330 and 14<=y<=350
        if shape=='circle': return math.hypot(x-200,y-190)<=184
        return y>=8 and abs(x-200)<=(y-8)*200/348+2 and y<=352
    d=''.join(f'M{x} {y}h0' for y in range(8,384,16) for x in range(8,400,16) if inside(x,y))
    return f'<svg class="dots" viewBox="0 0 400 384" aria-hidden="true"><path d="{d}" fill="none" stroke="currentColor" stroke-width="4.6" stroke-linecap="round"/></svg>'

WHAT=[
 ('square','Design for<br>Complex Products','Turn complex workflows and systems into simple, intuitive experiences.'),
 ('circle','Human-Centered AI','Design AI-powered experiences that keep people informed and in control.'),
 ('triangle','Design Systems<br>from the Ground Up','Build scalable, consistent design systems that help teams move faster.'),
]
what_html=''.join(
  f'<div class="what-card">{dots(sh,i)}<div class="what-text"><h3>{t}</h3><p class="what-desc">{d}</p></div></div>'
  for i,(sh,t,d) in enumerate(WHAT))

exp=''.join(f'<li><span class="yr">{y}</span><span class="role">{r}</span><span class="co">{c}</span></li>' for r,c,y in EXPERIENCE)
home=f"""<main id="top">
<section class="hero">
  <h1>A designer focused on user experience and visual design with a passion for design&nbsp;systems.</h1>
  <div class="hero-cta">
    <a class="link-ext" href="https://www.linkedin.com/in/olgatoc/" target="_blank" rel="noopener noreferrer"><span>LinkedIn</span>{ICON['ext']}<span class="sr-only"> (opens in a new tab)</span></a>
  </div>
</section>
<section id="what" class="wrap">
  {head_line('What I Do',1)}
  <div class="what-grid">{what_html}</div>
</section>
<section id="work" class="wrap">
  {head_line('Selected work',2)}
  <div class="work-grid">
{chr(10).join(work_item(p) for p in PROJECTS)}
  </div>
</section>
<section id="experience" class="wrap">
  {head_line('Experience',3)}
  <ul class="exp">{exp}</ul>
</section>
</main>"""
open(R+'index.html','w').write(page(NAME,home,0,'Olga Tochilin — designer focused on user experience, visual design and design systems.'))

for p in PROJECTS:
    blocks=json.load(open(S+p['src']+'.json'))
    m0=blocks[0][1] if blocks and blocks[0][0]=='meta' else {}
    client=p.get('client') or m0.get('client'); role=p.get('role') or m0.get('role'); lead=m0.get('lead','')
    meta=''
    if client: meta+=f'<div><dt>Client</dt><dd>{e(client)}</dd></div>'
    if role: meta+=f'<div><dt>My role</dt><dd>{e(role)}</dd></div>'
    if p.get('team'): meta+=f'<div><dt>Team</dt><dd>{e(p["team"])}</dd></div>'
    others=[q for q in PROJECTS if q is not p][:2]
    head_extra='\n  '.join(x for x in [f'<p class="lead">{e(lead)}</p>' if lead else '', f'<dl class="meta">{meta}</dl>' if meta else ''] if x)
    body=f"""<main class="project" id="top">
<article class="wrap narrow">
  <p class="back"><a href="../../#work">← All work</a></p>
  <h1>{e(p['title'])}</h1>
  {head_extra}
  {render_blocks(blocks,p)}
</article>
<section class="wrap">
  {head_line('More work',0)}
  <div class="work-grid work-grid-pair">
{chr(10).join(work_item(q,'../../') for q in others)}
  </div>
</section>
</main>"""
    d=R+'portfolio/'+p['slug']; os.makedirs(d,exist_ok=True)
    open(d+'/index.html','w').write(page(f"{p['title']} — {NAME}",body,2,lead or p['title'],back=True))
print('ok')
