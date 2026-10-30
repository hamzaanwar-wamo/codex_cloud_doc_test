"""Rebuild diagrams and the Markdown, PDF and Word editions from chapter sources."""
from pathlib import Path
import re,json,subprocess,textwrap
from xml.sax.saxutils import escape
from docx import Document
from docx.shared import Inches,Pt
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,Preformatted,Image,Table,TableStyle,PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parent
BLUE=colors.HexColor('#123B55')
INTRO='''# The Complete RAG Engineering Handbook

From fundamentals to production-grade retrieval systems. Detailed visual edition for senior AI / LLM engineer interviews.

**Reading path:** Chapters 1-9: core pipeline. Chapters 10-16: architecture choices. Chapters 17-23: evidence and evaluation. Chapters 24-30: production and implementation. Chapters 31-34: interviews and revision.

**Source boundary:** Based on the user-provided RAG master prompt. The original shared ChatGPT conversation returned HTTP 403 on both access attempts and could not be audited. This edition expands the supplied topic list; it does not claim to reproduce unseen chat content.

**Evidence boundary:** Enterprise facts, scores, capacities, prices and latency budgets are hypothetical examples, not benchmarks. Code labeled pseudocode is not runnable. The offline Python lab is runnable but is not a production platform. Verify current product details in official documentation.

**How to study:** Follow the arrows in each figure. Explain what happens before the query, during the query, and what is stored. Read the failure case. Then answer the interview question aloud.
'''
def figures():
 for name,s in json.loads((ROOT/'diagrams/specs.json').read_text()).items():
  dot=['digraph G {','graph [rankdir=TB,bgcolor="white",pad="0.2",ranksep="0.35"];','node [shape=box,style="rounded,filled",fillcolor="#EAF2F8",color="#397399",fontname="DejaVu Sans",fontsize=11];','edge [color="#526574",fontname="DejaVu Sans",fontsize=9];']
  mm=['flowchart TD']
  for k,v in s['nodes'].items():
   dot.append(f'{k} [label={json.dumps(v)}];');mm.append(f'  {k}["{v.replace(chr(10),"<br/>")}"]')
  for a,b,*label in s['edges']:
   dot.append(f'{a} -> {b}'+(f' [label={json.dumps(label[0])}]' if label else '')+';')
   mm.append(f'  {a} -->'+(f'|"{label[0]}"|' if label else '')+f' {b}')
  dot.append('}');p=ROOT/'diagrams'/name
  p.with_suffix('.dot').write_text('\n'.join(dot));p.with_suffix('.mmd').write_text('\n'.join(mm)+'\n')
  for fmt in ['png','svg']:subprocess.run(['dot',f'-T{fmt}','-Gdpi=150',str(p.with_suffix('.dot')),'-o',str(p.with_suffix('.'+fmt))],check=True)
def plain(s):return re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s).replace('**','').replace('`','')
def rich(s):
 s=escape(s);s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s);s=re.sub(r'`([^`]+)`',r'<font name="Mono">\1</font>',s)
 return re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s)
class Book(BaseDocTemplate):
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name=='Chapter':
   key='h'+str(self.seq.nextf('heading'));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,0,False);self.notify('TOCEntry',(0,f.getPlainText(),self.page,key))
def build():
 figures()
 from render_visuals import render_all
 render_all(ROOT/'diagrams')
 chapters=sorted((ROOT/'chapters').glob('*.md'))
 text=INTRO+'\n## Contents\n\n'+'\n'.join(f'- [{p.read_text().splitlines()[0][2:]}](chapters/{p.name})' for p in chapters)+'\n\n'+'\n\n'.join(p.read_text().replace('](../diagrams/','](diagrams/') for p in chapters)
 (ROOT/'RAG_Interview_Handbook.md').write_text(text)
 for name,file in [('Body','DejaVuSans.ttf'),('Body-Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
 pdfmetrics.registerFontFamily('Body',normal='Body',bold='Body-Bold',italic='Body',boldItalic='Body-Bold')
 styles=getSampleStyleSheet()
 for name,font,size,leading in [('BookBody','Body',9,13),('Chapter','Body-Bold',18,23),('Subhead','Body-Bold',12,17),('Smallhead','Body-Bold',10,14),('CodeBook','Mono',7,10),('Cell','Body',7.3,10)]:styles.add(ParagraphStyle(name=name,fontName=font,fontSize=size,leading=leading,spaceAfter=8,keepWithNext=name in ['Chapter','Subhead','Smallhead'],textColor=BLUE if 'head' in name.lower() or name=='Chapter' else colors.black))
 doc=Document();sec=doc.sections[0];sec.top_margin=sec.bottom_margin=Inches(.65);sec.left_margin=sec.right_margin=Inches(.7)
 doc.styles['Normal'].font.name='Calibri';doc.styles['Normal'].font.size=Pt(10);sec.header.paragraphs[0].text='RAG ENGINEERING  |  DETAILED VISUAL EDITION'
 sec.footer.paragraphs[0].text='Source-based answers. Measured trade-offs. Secure retrieval.'
 story=[]
 def para(s):doc.add_paragraph(plain(s));story.append(Paragraph(rich(s),styles['BookBody']))
 def parse(source):
  lines=source.splitlines();i=0
  while i<len(lines):
   line=lines[i].strip();i+=1
   if not line:continue
   if line.startswith('```'):
    block=[]
    while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
    i+=1;p=doc.add_paragraph();r=p.add_run('\n'.join(block));r.font.name='Consolas';r.font.size=Pt(8)
    wrapped=[]
    for b in block:wrapped.extend(textwrap.wrap(b,94,replace_whitespace=False,drop_whitespace=False) or [''])
    story.append(Preformatted('\n'.join(wrapped),styles['CodeBook']))
   elif line.startswith('!['):
    m=re.match(r'!\[(.*?)\]\((.*?)\)',line);path=ROOT/'diagrams'/m[2].split('diagrams/')[-1]
    with PILImage.open(path) as im:w,h=im.size
    scale=min(490/w,370/h);story.append(Image(str(path),width=w*scale,height=h*scale));doc.add_picture(str(path),width=Inches(min(6.6,w*scale/72)));para('Figure: '+m[1])
   elif line.startswith('|'):
    rows=[line]
    while i<len(lines) and lines[i].strip().startswith('|'):rows.append(lines[i].strip());i+=1
    data=[[plain(x.strip()) for x in r.strip('|').split('|')] for r in rows if not re.fullmatch(r'[| :\-]+',r)]
    n=len(data[0]);table=doc.add_table(rows=1,cols=n);table.style='Light Shading Accent 1'
    for j,x in enumerate(data[0]):table.rows[0].cells[j].text=x
    for row in data[1:]:
     cells=table.add_row().cells
     for j,x in enumerate(row):cells[j].text=x
    tab=Table([[Paragraph(escape(c),styles['Cell']) for c in row] for row in data],colWidths=[490/n]*n,repeatRows=1,hAlign='LEFT');tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF2F8')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#CCD6DD')),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([tab,Spacer(1,9)])
   elif line.startswith('# '):doc.add_heading(plain(line[2:]),0);story.append(Paragraph(rich(line[2:]),styles['Chapter']))
   elif line.startswith('## '):doc.add_heading(plain(line[3:]),2);story.append(Paragraph(rich(line[3:]),styles['Subhead']))
   elif line.startswith('### '):doc.add_heading(plain(line[4:]),3);story.append(Paragraph(rich(line[4:]),styles['Smallhead']))
   elif line.startswith('- '):doc.add_paragraph(plain(line[2:]),style='List Bullet');story.append(Paragraph('• '+rich(line[2:]),styles['BookBody']))
   else:para(line)
 parse(INTRO);doc.add_page_break();story.append(PageBreak());doc.add_heading('Contents',1)
 for p in chapters:doc.add_paragraph(p.read_text().splitlines()[0][2:])
 story.append(Paragraph('Contents',styles['Chapter']));toc=TableOfContents();toc.levelStyles=[ParagraphStyle(name='TOC0',fontName='Body',fontSize=9,leading=14,spaceBefore=5)];story.append(toc)
 for p in chapters:doc.add_page_break();story.append(PageBreak());parse(p.read_text())
 doc.save(ROOT/'RAG_Interview_Handbook.docx')
 def page(c,d):
  c.setFont('Body',7);c.setFillColor(BLUE);c.drawString(42,815,'RAG ENGINEERING  /  DETAILED VISUAL EDITION');c.drawString(42,24,'Source-based answers. Measured trade-offs. Secure retrieval.');c.drawRightString(553,24,str(d.page))
 pdf=Book(str(ROOT/'RAG_Interview_Handbook.pdf'),pagesize=(595,842),leftMargin=42,rightMargin=42,topMargin=42,bottomMargin=40,title='The Complete RAG Engineering Handbook',author='OpenAI');pdf.addPageTemplates(PageTemplate(id='book',frames=[Frame(42,40,511,760,id='main')],onPage=page));pdf.multiBuild(story)
 print(json.dumps({'chapters':len(chapters),'words':len(text.split()),'figures':len(list((ROOT/'diagrams').glob('*.png')))}))
if __name__=='__main__':build()
