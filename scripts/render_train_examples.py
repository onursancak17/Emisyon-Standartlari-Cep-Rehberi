"""Kesin veri paketinden şematik örnek görsel. Geliştirici gereksinimi: Pillow."""
import json
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'assets/field_guide.json').read_text(encoding='utf-8'))
BY_ID={p['id']:p for p in DATA['profiles']}
IDS=['moisture_epa4','fluoride_epa13a_rear','halogen_epa26a','metals_epa29_hg','acid_epa8','pah_iso11338_b','dioxin_en1948_filter']
W=2400; ROW=450; HEADER=230
im=Image.new('RGB',(W,HEADER+len(IDS)*ROW+100),'#edf3f6');d=ImageDraw.Draw(im)
fontdir=Path('C:/Windows/Fonts')
if fontdir.exists():regular=fontdir/'segoeui.ttf';bold=fontdir/'segoeuib.ttf'
else:regular=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');bold=regular.with_name('DejaVuSans-Bold.ttf')
f=lambda n,b=False:ImageFont.truetype(str(bold if b else regular),n)
navy='#183c52';teal='#087c80';light='#a3ded7'


def wrap(text,width,font):
    lines=[];line=''
    for word in text.split():
        test=(line+' '+word).strip()
        if d.textlength(test,font=font)>width and line:lines.append(line);line=word
        else:line=test
    return lines+[line] if line else lines


def centered(text,cx,y,width,font,color=navy,maxlines=5):
    for line in wrap(text,width,font)[:maxlines]:
        d.text((cx-d.textlength(line,font=font)/2,y),line,font=font,fill=color);y+=font.size+5
    return y


def symbol(kind,cx,y,content):
    if kind in ('impinger','trap'):
        x=cx-37
        if 'boş' not in content and kind=='impinger':
            d.rounded_rectangle((x+3,y+67,x+71,y+107),8,fill='#e5ce98' if 'silika' in content.lower() else light)
            if 'silika' in content.lower():
                for xx in range(x+10,x+70,10):
                    for yy in range(y+74,y+103,10):d.ellipse((xx-2,yy-2,xx+2,yy+2),fill='#80623e')
        d.rounded_rectangle((x,y+25,x+74,y+110),10,outline=navy,width=3)
        d.line([(cx-70,y+12),(cx-14,y+12),(cx-14,y+94)],fill=navy,width=3)
        d.line([(cx+15,y+43),(cx+15,y+12),(cx+70,y+12)],fill=navy,width=3)
    elif kind=='filter':
        d.line((cx-65,y+60,cx+65,y+60),fill=navy,width=3)
        d.rounded_rectangle((cx-30,y+24,cx+30,y+98),8,fill='#edc37d',outline=navy,width=3)
        for x in range(cx-20,cx+25,10):d.line((x,y+32,x,y+90),fill=navy,width=2)
    elif kind=='adsorber':
        d.line((cx-70,y+60,cx+70,y+60),fill=navy,width=3)
        d.rounded_rectangle((cx-50,y+35,cx+50,y+85),8,fill=light,outline=navy,width=3)
        for x in range(cx-40,cx+45,14):
            for yy in range(y+44,y+80,14):d.ellipse((x-2,yy-2,x+2,yy+2),fill=navy)
    elif kind=='condenser':
        d.rounded_rectangle((cx-55,y+25,cx+55,y+100),8,fill=light,outline=navy,width=2)
        pts=[(cx-70,y+60)]+[(cx-45+i*18,y+(40 if i%2==0 else 85)) for i in range(6)]+[(cx+70,y+60)]
        d.line(pts,fill=navy,width=3)
    elif kind=='probe':d.line([(cx-65,y+87),(cx-65,y+60),(cx+65,y+60)],fill=navy,width=5)
    else:
        d.rounded_rectangle((cx-55,y+25,cx+55,y+100),10,fill='white',outline=navy,width=3)
        d.ellipse((cx-24,y+39,cx+24,y+87),outline=navy,width=3)
        d.line((cx,y+63,cx+13,y+48),fill=teal,width=3)


d.rounded_rectangle((35,25,W-35,205),24,fill=navy)
d.text((70,44),'HER METODA KENDİ NUMUNE ALMA TRENİ',font=f(42,True),fill='white')
d.text((72,105),'Emisyon / İmisyon Ölçüm Standartları · İlk şema örnekleri',font=f(28),fill='#bde5e5')
d.text((72,150),'Akış soldan sağa · Ölçekli değildir · Arşiv sürümüne bağlıdır; tam yöntem onayı değildir.',font=f(23),fill='white')
for row,pid in enumerate(IDS):
    p=BY_ID[pid];top=HEADER+row*ROW
    d.rounded_rectangle((35,top,W-35,top+ROW-15),20,fill='white')
    d.text((65,top+12),f'{p["parameter"]}  |  {p["method"]}  |  {p["sourceVersion"]}',font=f(28,True),fill=navy)
    d.text((65,top+54),p['variant'],font=f(22),fill=teal)
    nodes=p['train'];step=(W-150)/len(nodes)
    for j,n in enumerate(nodes):
        cx=round(75+step*(j+.5));sy=top+96
        symbol(n['kind'],cx,sy,n['content'])
        yy=centered(n['label'],cx,sy+120,step-28,f(22,True),maxlines=2)
        if n['amount']:yy=centered(n['amount'],cx,yy,step-28,f(23,True),teal,maxlines=2)
        if n['kind']!='meter':yy=centered(n['content'],cx,yy,step-24,f(19),maxlines=6)
        if n['optional']:centered('İSTEĞE BAĞLI',cx,sy-8,step-10,f(15,True),'#8a5700',1)
        if j<len(nodes)-1:
            ax=round(75+step*(j+1));ay=sy+60
            d.line((ax-18,ay,ax+18,ay),fill=teal,width=4)
            d.polygon([(ax+18,ay),(ax+7,ay-7),(ax+7,ay+7)],fill=teal)
    d.text((65,top+ROW-53),'Kaynak: '+', '.join(p['sources'])+'  ·  Çekiş / DGM grubunun iç sırası cihaz şemasına göre.',font=f(18),fill='#536875')
y=HEADER+len(IDS)*ROW+8
d.text((60,y),'Diğer varyantlar uygulamada ayrı seçilir. Geometri, fraksiyonlar, kaçak ve saklama ayrıntıları ilgili yöntem kartındadır.',font=f(23),fill=navy)
out=ROOT/'docs/impinger_ornekleri.png';im.save(out,optimize=True)
print(out)
