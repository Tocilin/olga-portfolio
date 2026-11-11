"""Extract a case study from a saved WordPress/Salient page into ordered content blocks (JSON).
Run:  python3 -I tools/extract_case_study.py <saved-page.html> <output.json>   (needs beautifulsoup4)
This is how the Franky and Mayo case studies were imported; see tools/README.md.
Blocks: [kind, value] with kind in h1,h2,h3,h4,h5,h6,p,li,text,img,stat."""
import sys,json,re,html
from urllib.parse import urlsplit
from bs4 import BeautifulSoup,NavigableString,Tag,Comment
src,out=sys.argv[1],sys.argv[2]
soup=BeautifulSoup(open(src,encoding='utf8',errors='ignore').read(),'html.parser')
for t in soup(['script','style','noscript']): t.decompose()
root=soup.find(id='ajax-content-wrap') or soup.body
ESC=lambda s: html.escape(s,quote=False)
def inline(n):
    if isinstance(n,Comment): return ''
    if isinstance(n,NavigableString): return ESC(str(n))
    if n.name=='br': return ' '
    if n.name=='img': return ESC(n.get('alt','')) if 'emoji' in (n.get('class') or []) else ''
    inner=''.join(inline(c) for c in n.children)
    if n.name=='a' and n.get('href'):
        h=html.escape(n['href'],quote=True)
        ext=not urlsplit(n['href']).netloc.endswith('olgadesignsystems.com') and n['href'].startswith('http')
        return f'<a href="{h}"'+(' target="_blank" rel="noopener noreferrer"' if ext else '')+f'>{inner}</a>'
    if n.name in('strong','b'): return f'<strong>{inner}</strong>' if inner.strip() else inner
    if n.name in('em','i'): return f'<em>{inner}</em>' if inner.strip() else inner
    return inner
def clean(s): return re.sub(r'\s+',' ',s.replace('\xa0',' ')).strip()
def best_img(im):
    cands=[]
    for attr in ('data-nectar-img-srcset','srcset','data-srcset'):
        for part in (im.get(attr) or '').split(','):
            bits=part.strip().split()
            if len(bits)==2 and bits[1].endswith('w'): cands.append((int(bits[1][:-1]),bits[0]))
    for attr in ('data-nectar-img-src','src','data-lazy-src'):
        if im.get(attr,'').startswith('http') and 'uploads' in im.get(attr,''): cands.append((0,im[attr]))
    if not cands: return None
    cands.sort(reverse=True); return cands[0][1]
blocks=[]
def emit(k,v):
    if k!='img' and k!='stat' and not clean(re.sub(r'<[^>]+>','',v) if isinstance(v,str) else 'x'): return
    blocks.append([k,v])
def walk(n):
    if isinstance(n,Comment): return
    if isinstance(n,NavigableString):
        t=clean(str(n))
        if t and not isinstance(n,type(soup.new_string('')).__mro__[0]) or t:
            if t: emit('text',ESC(t))
        return
    if not isinstance(n,Tag): return
    cls=' '.join(n.get('class') or [])
    if n.name in('nav','header','footer','form'): return
    if 'nectar-milestone' in cls:
        num=clean(n.select_one('.number').get_text()) if n.select_one('.number') else ''
        sym=n.get('data-symbol','')
        label=clean(''.join(inline(c) for c in (n.select_one('.subject') or soup.new_tag('x')).children))
        emit('stat',[num+sym,label]); return
    if n.name in('h1','h2','h3','h4','h5','h6'): emit(n.name,clean(''.join(inline(c) for c in n.children))); return
    if n.name=='p': emit('p',clean(''.join(inline(c) for c in n.children))); return
    if n.name in('ul','ol'):
        for li in n.find_all('li',recursive=False): emit('li',clean(''.join(inline(c) for c in li.children)))
        return
    if n.name=='img':
        if 'emoji' in (n.get('class') or []): return
        u=best_img(n)
        if u and 'logo' not in u.lower(): emit('img',[u,n.get('alt','')])
        return
    for c in n.children: walk(c)
walk(root)
# keep from the page title (first h1) to the 'Previous Project' navigation
i=next(j for j,b in enumerate(blocks) if b[0]=='h1')
j=next((j for j,b in enumerate(blocks) if isinstance(b[1],str) and 'Previous Project' in b[1]),len(blocks))
blocks=blocks[i:j]
# drop consecutive duplicate image blocks (responsive duplicates)
res=[]
for b in blocks:
    if res and b[0]=='img' and res[-1][0]=='img' and res[-1][1][0]==b[1][0]: continue
    res.append(b)
json.dump(res,open(out,'w'),ensure_ascii=False,indent=0)
print(src,'->',len(res),'blocks')
