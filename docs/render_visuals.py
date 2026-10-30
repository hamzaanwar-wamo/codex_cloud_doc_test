"""Quantitative and sequence figures. Values are illustrative, not benchmarks."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def render_all(out: Path):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    names=['User','API / scope','Retrieval','Sources','Model / verifier']
    fig,ax=plt.subplots(figsize=(9.5,6.4));ax.set_xlim(-.5,4.5);ax.set_ylim(9.7,-1)
    for x,name in enumerate(names):
        ax.text(x,-.6,name,ha='center',weight='bold',color='#123B55',bbox={'facecolor':'#EAF2F8','edgecolor':'#397399','pad':7})
        ax.plot([x,x],[-.1,9.1],':',color='#A2B4C2',zorder=0)
    messages=[(0,1,'Question + authenticated session'),(1,2,'Search with server-enforced scope'),(2,1,'Candidate IDs / ranks / versions'),(1,3,'Fetch applicable authorized chunks'),(3,1,'Original evidence + citation references'),(1,4,'Bounded source blocks + question'),(4,4,'Draft then check material claims'),(4,1,'Supported answer or explicit gaps'),(1,0,'Release verified result')]
    mermaid=['sequenceDiagram','  participant U as User','  participant A as API / scope','  participant R as Retrieval','  participant S as Sources','  participant M as Model / verifier']
    aliases=['U','A','R','S','M']
    for y,(a,b,label) in enumerate(messages):
        if a==b:
            ax.annotate('',xy=(a,y+.4),xytext=(a,y-.15),arrowprops={'arrowstyle':'->','connectionstyle':'arc3,rad=-1','color':'#397399'})
            ax.text(a-.1,y,label,ha='right',fontsize=10,color='#123B55')
        else:
            ax.add_patch(FancyArrowPatch((a,y),(b,y),arrowstyle='->',mutation_scale=12,color='#397399',linewidth=1.5))
            ax.text((a+b)/2,y-.15,label,ha='center',fontsize=10,color='#123B55',bbox={'facecolor':'white','edgecolor':'none','pad':1})
        mermaid.append(f'  {aliases[a]}->>{aliases[b]}: {label}')
    ax.axis('off');fig.tight_layout()
    save(fig,out/'36-query-sequence');(out/'36-query-sequence.mmd').write_text('\n'.join(mermaid)+'\n')
    chunks=20_000_000
    labels=['384 dims / float32','768 dims / float32','1536 dims / float32','768 dims / int8']
    values=[chunks*384*4/1e9,chunks*768*4/1e9,chunks*1536*4/1e9,chunks*768*1/1e9]
    fig,ax=plt.subplots(figsize=(9,4.2));bars=ax.barh(labels,values,color=['#397399','#1C567C','#123B55','#62A19C']);ax.invert_yaxis();ax.set_xlabel('Raw vector storage (decimal GB)');ax.set_title('20 million chunks: representation size only',loc='left',weight='bold',color='#123B55')
    for b,v in zip(bars,values):ax.text(v+1,b.get_y()+b.get_height()/2,f'{v:.2f} GB',va='center')
    ax.set_xlim(0,145);ax.spines[['top','right']].set_visible(False);fig.text(.02,.01,'Hypothetical arithmetic. Excludes ANN structures, quantization metadata, text, replicas and rebuild space.',fontsize=8);fig.tight_layout(rect=(0,.05,1,1));save(fig,out/'39-storage-chart')
    (out/'39-storage-chart.json').write_text(json.dumps({'chunks':chunks,'labels':labels,'decimal_GB':values,'kind':'hypothetical raw storage arithmetic'},indent=2))
    stages=['Auth / understand','Lexical (parallel)','Vector (parallel)','Rerank / pack','Generate','Verify']
    left=[0,100,100,300,550,1550];width=[100,120,200,250,1000,300]
    fig,ax=plt.subplots(figsize=(10,4.3));ax.barh(stages,width,left=left,color=['#7FA9C2','#397399','#62A19C','#5987A8','#123B55','#658E82']);ax.invert_yaxis();ax.set_xlabel('Illustrative elapsed time (ms)');ax.set_title('Critical path: 1850 ms under stated assumptions',loc='left',weight='bold',color='#123B55');ax.axvline(1850,color='#123B55',ls='--',lw=1)
    for y,(l,w) in enumerate(zip(left,width)):ax.text(l+w+12,y,f'{w} ms',va='center',fontsize=8)
    ax.set_xlim(0,2050);ax.spines[['top','right']].set_visible(False);fig.text(.02,.01,'Hypothetical budget, not measured latency. Search branches overlap; real overhead and contention must be measured.',fontsize=8);fig.tight_layout(rect=(0,.05,1,1));save(fig,out/'40-latency-chart')
    (out/'40-latency-chart.json').write_text(json.dumps({'stages':stages,'start_ms':left,'duration_ms':width,'kind':'hypothetical critical-path budget'},indent=2))

def save(fig,path):
    fig.savefig(path.with_suffix('.png'),dpi=180,facecolor='white');fig.savefig(path.with_suffix('.svg'),facecolor='white');plt.close(fig)
    svg=path.with_suffix('.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
