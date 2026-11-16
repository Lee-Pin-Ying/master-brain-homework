"""Build a topic-based static knowledge library with Python standard library only."""
from pathlib import Path
from html import escape
import json, re, os

ROOT = Path(__file__).resolve().parents[1]
TOPICS = json.loads((ROOT / 'topics.json').read_text(encoding='utf-8-sig'))['topics']

def rel(target, origin):
    return os.path.relpath(ROOT / target, (ROOT / origin).parent).replace('\\', '/')

def link(target, label, origin, cls=''):
    href = target if target.startswith(('https://', 'http://', '#')) else rel(target, origin)
    return f'<a class="{cls}" href="{escape(href, quote=True)}">{escape(label)}</a>'

def shell(title, body, origin, topic=None):
    nav = link('index.html', '主題首頁', origin) + link('wiki/index.html', '知識筆記', origin) + link('raw/index.html', '原始資料', origin) + link('presentations/index.html', '簡報區', origin)
    crumb = link('index.html', '知識庫', origin)
    if topic:
        crumb += ' / ' + link(f'pages/{topic["slug"]}/index.html', topic['title'], origin)
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}｜碩士班知識庫</title><meta name="description" content="依主題整理論文、課程與作業的個人知識庫，連結原始來源、知識筆記與按需製作的簡報。"><link rel="stylesheet" href="{rel('assets/site.css', origin)}"><script defer src="{rel('assets/library.js', origin)}"></script></head><body><header><a class="brand" href="{rel('index.html', origin)}">碩士班知識庫 <span class="eyebrow">/ KNOWLEDGE LIBRARY</span></a><nav aria-label="主要導覽">{nav}</nav></header><main class="wrap"><div class="breadcrumb">{crumb}</div>{body}</main><footer class="wrap">原始資料 → 關聯筆記 → 按需展示。新增資料後，請啟動 AI 並指示收錄；本網站不會自行監控檔案。<br>{link('README.md','使用說明',origin)} · {link('AGENTS.md','通用 AI 工作規則',origin)}</footer></body></html>'''

def save(origin, html):
    p = ROOT / origin
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding='utf-8')

def md_html_path(p):
    return p.relative_to(ROOT).with_suffix('.html').as_posix()

def inline(text, md_path, origin):
    # Escape source HTML; only a small, explicit Markdown subset is rendered.
    chunks, last = [], 0
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
        chunks.append(escape(text[last:m.start()]))
        label, href = m.groups()
        if not href.startswith(('https://', 'http://', '#')):
            clean, _, anchor = href.partition('#')
            target = (md_path.parent / clean).resolve()
            if target.is_relative_to(ROOT.resolve()):
                if target.suffix == '.md':
                    # Wiki notes have HTML twins; other Markdown remains a source file.
                    if target.is_relative_to((ROOT/'wiki').resolve()): target = target.with_suffix('.html')
                if target.name == 'zhong-2023-gnss-pdr-fgo.pdf':
                    href = 'https://arxiv.org/pdf/2212.14264v2'
                else:
                    href = rel(target.relative_to(ROOT.resolve()).as_posix(), origin) + ('#'+anchor if anchor else '')
        if href.startswith(('javascript:', 'data:')): href = '#'
        chunks.append(f'<a href="{escape(href, quote=True)}">{escape(label)}</a>')
        last = m.end()
    chunks.append(escape(text[last:]))
    value = ''.join(chunks)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)

def render_md(p):
    origin = md_html_path(p)
    lines = p.read_text(encoding='utf-8-sig').splitlines()
    blocks, i = [], 0
    while i < len(lines):
        line = lines[i].strip()
        if not line: i += 1; continue
        if line.startswith('```'):
            code = []; i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i]); i += 1
            blocks.append('<pre><code>'+escape('\n'.join(code))+'</code></pre>'); i += 1; continue
        if line.startswith('|') and i+1 < len(lines) and re.match(r'^\|[\s:|-]+\|?$', lines[i+1].strip()):
            rows = []; headers = [c.strip() for c in line.strip('|').split('|')]; i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            blocks.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+inline(c,p,origin)+'</th>' for c in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c,p,origin)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'); continue
        heading = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading:
            n = min(len(heading[1])+1, 6)
            # Page title is emitted separately by the wrapper.
            if len(heading[1]) > 1: blocks.append(f'<h{n}>'+inline(heading[2],p,origin)+f'</h{n}>')
        elif re.match(r'^[-*]\s+', line):
            items=[]
            while i < len(lines) and re.match(r'^[-*]\s+',lines[i].strip()):
                items.append('<li>'+inline(re.sub(r'^[-*]\s+','',lines[i].strip()),p,origin)+'</li>'); i+=1
            blocks.append('<ul>'+''.join(items)+'</ul>'); continue
        elif re.match(r'^\d+\.\s+',line):
            items=[]
            while i < len(lines) and re.match(r'^\d+\.\s+',lines[i].strip()):
                items.append('<li>'+inline(re.sub(r'^\d+\.\s+','',lines[i].strip()),p,origin)+'</li>'); i+=1
            blocks.append('<ol>'+''.join(items)+'</ol>'); continue
        else: blocks.append('<p>'+inline(line,p,origin)+'</p>')
        i+=1
    title = next((l.lstrip('# ').strip() for l in lines if l.startswith('# ')),p.stem)
    return title, ''.join(blocks)

def notes(topic):
    return sorted(p for p in (ROOT/'wiki'/topic['slug']).rglob('*.md'))

def note_title(p):
    return next((l[2:].strip() for l in p.read_text(encoding='utf-8-sig').splitlines() if l.startswith('# ')),p.stem)

def card(target, title, description, origin, tag=''):
    return f'<a class="card" href="{rel(target,origin)}"><span class="num">{escape(tag)}</span><h3>{escape(title)}</h3><p>{escape(description)}</p><span class="arrow">開啟 →</span></a>'

def decks(topic, origin):
    return ''.join(card(d['path'],d['title'],d['description'],origin,d.get('type','展示頁')) for d in topic.get('presentations',[]))

def topic_cards(origin, section):
    dests={'topics':lambda s:f'pages/{s}/index.html','wiki':lambda s:f'wiki/{s}/index.html','raw':lambda s:f'raw/{s}/index.html'}
    return ''.join(card(dests[section](t['slug']),t['title'],t['description'],origin,t.get('category','主題')) for t in TOPICS)

def source_rows(t, origin):
    rows=[]
    described=set()
    for s in t.get('sources',[]):
        described.add(s['file'])
        file=f'raw/{t["slug"]}/{s["file"]}'
        actions=link(s['url'],'原始來源',origin) if s.get('url') else ''
        if not s.get('local_only'): actions += ' · '+link(file,'檔案',origin)
        else: actions += '<span class="caption"> · PDF 僅保留本機</span>'
        if s.get('note'): actions+=' · '+link(s['note'],'閱讀筆記',origin)
        rows.append(f'<article class="source-row"><div><span class="tag">{escape(s["id"])} · {escape(s["status"])}</span><h3>{escape(s["title"])}</h3><p>{escape(s["description"])}</p></div><div>{actions}</div></article>')
    other=[]
    for p in sorted((ROOT/'raw'/t['slug']).iterdir()):
        if p.is_file() and p.name not in described and p.name != 'index.html':
            other.append('<li>'+link(p.relative_to(ROOT).as_posix(),p.name,origin)+'</li>')
    return ''.join(rows)+('<details><summary>其他原始檔與來源紀錄</summary><ul>'+''.join(other)+'</ul></details>' if other else '')

def build():
    # Global entry: topic-neutral content, actual topics only.
    home='index.html'
    total_notes=sum(len(notes(t)) for t in TOPICS)
    total_decks=sum(len(t.get('presentations',[])) for t in TOPICS)
    body=f'''<section class="hero library-hero"><div><div class="eyebrow">MY GRADUATE KNOWLEDGE LIBRARY</div><h1>碩士班知識庫</h1><p class="lead">把論文、課程與作業，整理成能持續累積的知識。先選主題，再進入來源、筆記與簡報。</p><div class="actions">{link('#topics','選擇主題 ↓',home,'button')}{link('presentations/index.html','瀏覽簡報區',home,'button secondary')}</div></div><div class="library-art" aria-label="資料、筆記、展示三層架構"><div><span>01</span><b>原始資料</b><small>論文 · 講義 · 研究構想</small></div><div><span>02</span><b>知識筆記</b><small>理解 · 連結 · 比較</small></div><div><span>03</span><b>簡報展示</b><small>報告 · 分享 · 回顧</small></div></div></section><div class="facts"><div><b>{len(TOPICS):02d}</b><span>已建立主題</span></div><div><b>{total_notes:02d}</b><span>主題知識筆記</span></div><div><b>{total_decks:02d}</b><span>展示與簡報</span></div></div><section id="topics" class="section"><div class="eyebrow">CHOOSE A TOPIC</div><h2>從你正在研究的事情開始。</h2><p>每個主題保有自己的來源、概念與成果；相關知識仍可跨主題連結。</p><div class="cards topic-grid">{topic_cards(home,'topics')}</div><p class="caption">目前已有 GPS 主題。新增其他課程或研究後，會出現在這裡。</p></section><section class="section"><div class="eyebrow">YOUR WORKFLOW</div><h2>讀進來、想清楚，再講出去。</h2><div class="flow"><div><b>放入來源</b><small>依主題放進 raw 資料夾。</small></div><div><b>請 AI 整理</b><small>保留證據，更新相關概念。</small></div><div><b>閱讀與追問</b><small>從筆記回查原文，留下自己的理解。</small></div><div><b>需要時做簡報</b><small>將選好的內容整理成展示。</small></div></div><div class="note">放入檔案後，仍需啟動 AI 並指示處理。新增來源不會自行觸發整理，也不必每次生成簡報。</div></section>'''
    save(home,shell('首頁',body,home))
    for section,title,desc in [('wiki','知識筆記','依主題閱讀來源筆記、概念與比較；所有筆記都有網頁版本。'),('raw','原始資料','依主題收納原始論文與資料；來源狀態與閱讀筆記一起查找。')]:
        origin=f'{section}/index.html'
        body=f'<section class="deck-head"><div class="eyebrow">{section.upper()} LIBRARY</div><h1>{title}</h1><p class="lead">{desc}</p></section><div class="cards topic-grid">{topic_cards(origin,section)}</div>'
        save(origin,shell(title,body,origin))
    origin='presentations/index.html'
    body='<section class="deck-head"><div class="eyebrow">PRESENTATION LIBRARY</div><h1>簡報區</h1><p class="lead">收藏需要報告或分享時製作的成果。選主題，開啟一份展示。</p></section>'
    for t in TOPICS:
        if t.get('presentations'):
            body+=f'<section class="section"><h2>{escape(t["title"])}</h2><div class="cards">{decks(t,origin)}</div></section>'
    save(origin,shell('簡報區',body,origin))
    for t in TOPICS:
        slug=t['slug']; origin=f'pages/{slug}/index.html'
        body=f'<section class="deck-head"><span class="pill">{escape(t.get("category","主題"))}</span><h1>{escape(t["title"])}</h1><p class="lead">{escape(t["description"])}</p></section>'
        body+='<div class="cards">'+card(f'raw/{slug}/index.html','原始資料','原文、閱讀狀態與檔案入口。',origin,'01 / SOURCES')+card(f'wiki/{slug}/index.html','知識筆記','概念、論文閱讀與跨來源比較。',origin,'02 / WIKI')+card('#presentations','簡報與展示','把研究內容講給別人聽。',origin,'03 / PRESENTATIONS')+'</div>'
        # card() assumes a file target; replace the local fragment explicitly.
        body=body.replace(rel('#presentations',origin),'#presentations')
        body+='<section id="presentations" class="section"><h2>簡報與展示</h2><div class="cards">'+decks(t,origin)+'</div></section>'
        if t.get('status'):body+='<div class="note">'+escape(t['status'])+'</div>'
        save(origin,shell(t['title'],body,origin,t))
        origin=f'raw/{slug}/index.html'
        body=f'<section class="deck-head"><div class="eyebrow">ORIGINAL SOURCES</div><h1>{escape(t["title"])}<br>原始資料</h1><p class="lead">保留來源，分清研究構想、已讀內容與待取得的全文。</p></section>'+source_rows(t,origin)
        save(origin,shell(t['title']+'｜原始資料',body,origin,t))
        origin=f'wiki/{slug}/index.html'
        body=f'<section class="deck-head"><div class="eyebrow">CONNECTED NOTES</div><h1>{escape(t["title"])}<br>知識筆記</h1><p class="lead">點擊筆記直接閱讀網頁，或用 Obsidian 開啟同一批 Markdown。</p></section><div class="note-list">'
        for p in notes(t):
            kind={'sources':'來源筆記','concepts':'概念筆記','syntheses':'比較與整理'}.get(p.parent.name,'主題說明')
            body+=f'<article class="source-row"><div><span class="tag">{kind}</span><h3>{link(md_html_path(p),note_title(p),origin)}</h3></div><div>{link(p.relative_to(ROOT).as_posix(),"Markdown 原檔",origin)}</div></article>'
            title,content=render_md(p)
            note_origin=md_html_path(p)
            note_body=f'<article class="reading"><span class="tag">{kind}</span><h1>{escape(title)}</h1>{content}<div class="bottom-links">{link(f"wiki/{slug}/index.html","← 返回主題筆記",note_origin)}{link(p.relative_to(ROOT).as_posix(),"Markdown 原檔",note_origin)}</div></article>'
            save(note_origin,shell(title,note_body,note_origin,t))
        body+='</div>'
        save(origin,shell(t['title']+'｜知識筆記',body,origin,t))
    save('wiki/log.html',shell('更新紀錄','<article class="reading"><h1>更新紀錄</h1>'+render_md(ROOT/'wiki/log.md')[1]+'</article>','wiki/log.html'))
    print(f'Built {len(TOPICS)} topic(s); {total_notes} note pages; {total_decks} existing presentations retained.')

if __name__ == '__main__': build()
