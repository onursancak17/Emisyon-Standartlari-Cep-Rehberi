"""Kaynak kontrollü dallı verilerden yeni Türkçe topoloji. Geliştirici bağımlılığı: Pillow."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
fd=Path('C:/Windows/Fonts')
regular=fd/'segoeui.ttf' if fd.exists() else Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
bold=fd/'segoeuib.ttf' if fd.exists() else regular.with_name('DejaVuSans-Bold.ttf')
navy='#183b50';teal='#087c80'
def font(n,b=False):return ImageFont.truetype(str(bold if b else regular),n)
measure=ImageDraw.Draw(Image.new('RGB',(1,1)))
def wrap(text,w,f):
    lines=[];line=''
    for word in text.split():
        candidate=(line+' '+word).strip()
        if measure.textlength(candidate,font=f)>w and line:lines.append(line);line=word
        else:line=candidate
    return lines+[line] if line else lines
def lines_for(n,w):
    parts=[(n['label'],31,True)]
    if n.get('optional'):parts.append(('İsteğe bağlı',25,True))
    parts.append((n['content'],27,False))
    if n.get('amount'):parts.append((n['amount'],26,True))
    return [(line,size,b) for text,size,b in parts for line in wrap(text,w-40,font(size,b))]
def render(p):
    diagram=p['diagram'];bw=340;gap=40;prefix_x=70;branch_x=1370
    rows=diagram['branches'];maxn=max(len(r['nodes']) for r in rows)
    w=max(2800,branch_x+maxn*(bw+gap)+50)
    heights=[max(250,max(sum(size+12 for _,size,_ in lines_for(n,bw))+40 for n in row['nodes'])) for row in rows]
    ys=[270,270+heights[0]+190]
    flow_y=[y+60 for y in ys];fork_y=sum(flow_y)/2
    shared_height=max(250,max(sum(size+12 for _,size,_ in lines_for(n,bw))+40 for n in diagram['shared']))
    h=max(ys[1]+heights[1],fork_y-60+shared_height)+210
    im=Image.new('RGB',(w,int(h)),'#f3f7fa');d=ImageDraw.Draw(im)
    def text(s,x,y,width,size=28,b=False):
        for line in wrap(s,width,font(size,b)):
            d.text((x,y),line,font=font(size,b),fill=navy);y+=size+10
    def arrow(points):
        d.line(points,fill=teal,width=7,joint='curve');x,y=points[-1]
        d.polygon([(x,y),(x-18,y-10),(x-18,y+10)],fill=teal)
    def box(n,x,y,bh):
        d.rounded_rectangle((x,y,x+bw,y+bh),22,fill='white',outline=teal,width=3)
        yy=y+18
        for line,size,b in lines_for(n,bw):d.text((x+20,yy),line,font=font(size,b),fill=navy);yy+=size+12
    text(f'{p["parameter"]} · {p["method"]}',70,40,w-140,56,True)
    text(p['variant'],70,130,w-140,33)
    for i,n in enumerate(diagram['shared']):
        x=prefix_x+i*(bw+gap);box(n,x,fork_y-60,shared_height)
        if i<len(diagram['shared'])-1:arrow([(x+bw,fork_y),(x+bw+gap,fork_y)])
    shared_end=prefix_x+(len(diagram['shared'])-1)*(bw+gap)+bw
    for i,row in enumerate(rows):
        text(row['label'].upper(),branch_x,ys[i]-60,w-branch_x-50,34,True)
        arrow([(shared_end,fork_y),(1300,fork_y),(1300,flow_y[i]),(branch_x,flow_y[i])])
        for j,n in enumerate(row['nodes']):
            x=branch_x+j*(bw+gap);box(n,x,ys[i],heights[i])
            if j<len(row['nodes'])-1:arrow([(x+bw,flow_y[i]),(x+bw+gap,flow_y[i])])
    text('Kolların debisi ve hacmi ayrı kaydedilir. Şema ölçekli ekipman çizimi değildir; seçili varyantı gösterir.',70,h-160,w-140,31,True)
    text('Kaynak: '+', '.join(p['sources'])+' · Koşullar ve kaynak maddeleri uygulamadaki yöntem kartındadır.',70,h-90,w-140,26)
    target=ROOT/diagram['asset'];target.parent.mkdir(parents=True,exist_ok=True);im.save(target,optimize=True)
    print(target)
if __name__=='__main__':
    for p in json.loads((ROOT/'assets/field_guide.json').read_text(encoding='utf-8'))['profiles']:
        if p.get('diagram'):render(p)
