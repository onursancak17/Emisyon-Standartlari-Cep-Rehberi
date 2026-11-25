"""Kaynak kontrollü veriden yeni, Türkçe akış topolojisi. Pillow geliştirici aracıdır."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
p=next(p for p in json.loads((ROOT/'assets/field_guide.json').read_text(encoding='utf-8'))['profiles'] if p['id']=='pah_iso11338_b_split')
im=Image.new('RGB',(2800,1200),'#f3f7fa');d=ImageDraw.Draw(im)
fd=Path('C:/Windows/Fonts')
regular=fd/'segoeui.ttf' if fd.exists() else Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
bold=fd/'segoeuib.ttf' if fd.exists() else regular.with_name('DejaVuSans-Bold.ttf')
navy='#183b50';teal='#087c80'
def font(n,b=False):return ImageFont.truetype(str(bold if b else regular),n)
def text(s,x,y,w,size=28,b=False):
    f=font(size,b);line=''
    for word in s.split():
        candidate=(line+' '+word).strip()
        if d.textlength(candidate,font=f)>w and line:
            d.text((x,y),line,font=f,fill=navy);y+=size+9;line=word
        else:line=candidate
    if line:d.text((x,y),line,font=f,fill=navy)
def arrow(points):
    d.line(points,fill=teal,width=7,joint='curve');x,y=points[-1]
    d.polygon([(x,y),(x-18,y-10),(x-18,y+10)],fill=teal)
def box(n,x,y,w=310):
    d.rounded_rectangle((x,y,x+w,y+245),22,fill='white',outline=teal,width=3)
    text(n['label'],x+20,y+18,w-40,31,True)
    text(n['content'],x+20,y+100,w-40,27)
d.text((70,45),'PAH · ISO 11338-1:2003 · Metot B',font=font(56,True),fill=navy)
text('Filtre sonrası akış bölünmesi — ana kol ve gaz fazını toplayan yan kol',70,125,2650,34)
shared=p['diagram']['shared']
box(shared[0],70,420,340);box(shared[1],470,420,340);box(shared[2],870,420,290)
arrow([(410,470),(470,470)]);arrow([(810,470),(870,470)])
arrow([(1160,470),(1220,470),(1220,300),(1450,300)])
arrow([(1160,470),(1220,470),(1220,760),(1300,760)])
text('ANA KOL',1450,205,1000,36,True)
box(p['diagram']['branches'][0]['nodes'][0],1450,250,1110)
text('YAN KOL · GAZ FAZI PAH',1300,650,1300,36,True)
for i,n in enumerate(p['diagram']['branches'][1]['nodes']):
    x=1300+i*355;box(n,x,710,310)
    if i<3:arrow([(x+310,760),(x+355,760)])
text('Hacimler ayrı kaydedilir. Kapasite sınırları bu örnek cihaz içindir; zorunlu sabit çekiş debileri değildir.',70,1030,2600,32,True)
text('Kaynak: §6.1–6.3, bilgi amaçlı Şekil B.3 (PDF s.25). Yeni şema; ölçekli ekipman / imalat çizimi değildir.',70,1110,2600,26)
target=ROOT/p['diagram']['asset'];target.parent.mkdir(parents=True,exist_ok=True);im.save(target,optimize=True)
print(target)
