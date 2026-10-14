#!/usr/bin/env python3
"""Deterministic diagrams: labels and sequence come from the reviewed guide data."""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
NAVY='#102A43'; TEAL='#087F8C'; GRAY='#526477'
def font(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)
def lines(d,text,f,width):
    out=[]
    for paragraph in text.split('\n'):
        row=''
        for w in paragraph.split():
            cand=(row+' '+w).strip()
            if row and d.textlength(cand,font=f)>width: out.append(row);row=w
            else:row=cand
        out.append(row)
    return out
def text(d,xy,s,size=28,bold=False,width=360,fill=NAVY):
    f=font(size,bold);x,y=xy
    for row in lines(d,s,f,width):d.text((x,y),row,font=f,fill=fill);y+=size+8
    return y
def arrow(d,a,b):
    d.line([a,b],fill=TEAL,width=7)
    angle=math.atan2(b[1]-a[1],b[0]-a[0]);r=17
    d.polygon([b,(b[0]-r*math.cos(angle-.5),b[1]-r*math.sin(angle-.5)),(b[0]-r*math.cos(angle+.5),b[1]-r*math.sin(angle+.5))],fill=TEAL)

def component(d,cx,y,kind):
    color={'acid':'#C68C24','alkali':'#119C97','purple':'#7B51B4','organic':'#C47848','silica':'#A297C7','water':'#4AA5DF'}.get(kind,'#D5E7F0')
    if kind in {'acid','alkali','purple','organic','silica','water','empty'}:
        # Vessel, dipping inlet, outlet and liquid. A filled vessel always has a submerged inlet.
        d.rounded_rectangle((cx-66,y+12,cx+66,y+128),radius=20,fill='#FFFFFF',outline=NAVY,width=4)
        d.rectangle((cx-50,y-6,cx+50,y+21),fill='#FFFFFF',outline=NAVY,width=4)
        if kind!='empty':
            d.rounded_rectangle((cx-59,y+72,cx+59,y+121),radius=13,fill=color)
            if kind=='silica':
                for dx in range(-45,46,15):
                    for dy in range(80,117,15):d.ellipse((cx+dx-4,y+dy-4,cx+dx+4,y+dy+4),fill='#FFF5FF')
            else:
                for dx,dy in [(-18,66),(-8,55),(2,45)]:d.ellipse((cx+dx-4,y+dy-4,cx+dx+4,y+dy+4),outline=color,width=2)
        d.line([(cx-32,y-28),(cx-32,y+99)],fill=NAVY,width=5)
        d.line([(cx+32,y-28),(cx+32,y+34)],fill=NAVY,width=5)
        arrow(d,(cx-69,y-23),(cx-33,y-23));arrow(d,(cx+33,y-23),(cx+70,y-23))
    elif kind=='filter':
        d.ellipse((cx-70,y+15,cx+70,y+125),fill='#FFFFFF',outline=NAVY,width=5)
        for dx in range(-35,36,14):d.line((cx+dx,y+33,cx+dx,y+108),fill='#8CB3C2',width=3)
        d.line((cx-95,y+70,cx-70,y+70),fill=TEAL,width=7);d.line((cx+70,y+70,cx+95,y+70),fill=TEAL,width=7)
    elif kind=='resin':
        d.rounded_rectangle((cx-50,y+5,cx+50,y+130),radius=13,fill='#F0E8FF',outline=NAVY,width=4)
        for dx in range(-34,35,17):
            for dy in range(27,111,17):d.ellipse((cx+dx-5,y+dy-5,cx+dx+5,y+dy+5),fill='#7B51B4')
        d.line((cx,y-17,cx,y+5),fill=NAVY,width=5);d.line((cx,y+130,cx,y+145),fill=NAVY,width=5)
    elif kind=='probe':
        d.rectangle((cx-70,y+5,cx-15,y+132),fill='#E5EBF1',outline=NAVY,width=4)
        d.line([(cx-80,y+95),(cx+60,y+95),(cx+60,y+45)],fill=TEAL,width=10)
        arrow(d,(cx-8,y+65),(cx-8,y+25))
    elif kind=='cooler':
        d.rounded_rectangle((cx-75,y+5,cx+75,y+135),radius=15,fill='#E6F5FC',outline='#318CAF',width=4)
        for yy in [25,55,85,115]:d.line([(cx-45,y+yy),(cx+45,y+yy)],fill=TEAL,width=6)
        pass
    elif kind=='pump':
        d.ellipse((cx-62,y+15,cx+62,y+130),fill='#DDF2EF',outline=TEAL,width=5)
        d.polygon([(cx-25,y+50),(cx+30,y+73),(cx-25,y+100)],fill=TEAL)
    else:
        d.rounded_rectangle((cx-85,y+14,cx+85,y+130),radius=18,fill='#EDF5F9',outline=NAVY,width=4)
        d.rounded_rectangle((cx-65,y+34,cx+65,y+80),radius=8,fill=NAVY)
        d.text((cx-42,y+41),'T / P' if kind=='meter' else 'KONTROL',font=font(20,True),fill='white')
        for xx in [-40,0,40]:d.ellipse((cx+xx-6,y+100,cx+xx+6,y+112),fill=TEAL)

out=ROOT/'assets/trains';out.mkdir(exist_ok=True)
for g in json.loads((ROOT/'assets/field_guides.json').read_text()):
    for t in g['trains']:
        nodes=t['nodes'];cols=min(4,len(nodes));rows=math.ceil(len(nodes)/cols)
        width=1920;height=250+rows*410+180
        im=Image.new('RGB',(width,height),'#F3F7FA');d=ImageDraw.Draw(im)
        d.rectangle((0,0,width,185),fill=NAVY)
        text(d,(64,28),t['title'],40,True,width-130,'white')
        text(d,(64,122),'Gaz / işlem yönü: numara sırasını ve okları izle',26,False,width-130,'#BFE6E5')
        positions=[];cardw=412;gap=48;x0=(width-(cols*cardw+(cols-1)*gap))//2
        for i,n in enumerate(nodes):
            row=i//cols;col=i%cols
            if row%2:col=cols-1-col
            x=x0+col*(cardw+gap);y=215+row*410;positions.append((x,y))
            d.rounded_rectangle((x,y,x+cardw,y+366),radius=22,fill='white',outline='#D2DFE8',width=2)
            d.ellipse((x+18,y+14,x+68,y+64),fill=TEAL)
            d.text((x+31,y+20),str(i+1),font=font(26,True),fill='white')
            if n['zone']:text(d,(x+80,y+18),n['zone'],18,False,cardw-90,TEAL)
            layer=Image.new('RGBA',(250,170),(0,0,0,0))
            component(ImageDraw.Draw(layer),125,28,n['kind'])
            if row%2 and n['kind'] not in {'equipment','meter','cooler'}: layer=ImageOps.mirror(layer)
            im.paste(layer,(int(x+cardw/2-125),y+48),layer)
            ty=text(d,(x+20,y+215),n['label'],27,True,cardw-40)
            value=n['value'];f=font(22)
            if len(lines(d,value,f,cardw-40))>2: f=font(19)
            for line in lines(d,value,f,cardw-40):d.text((x+20,ty),line,font=f,fill=GRAY);ty+=f.size+5
            if ty>y+360:raise RuntimeError(f'Label overflow: {g["id"]} {n}')
        for i in range(len(positions)-1):
            x,y=positions[i];nx,ny=positions[i+1]
            if y==ny:
                if nx>x:arrow(d,(x+cardw+4,y+162),(nx-5,ny+162))
                else:arrow(d,(x-4,y+162),(nx+cardw+5,ny+162))
            else:
                # Turn down between rows; visually connects successive numbered stages.
                arrow(d,(x+cardw/2,y+371),(nx+cardw/2,ny-6))
        fy=215+rows*410
        text(d,(64,fy),t['source'],24,True,width-130)
        text(d,(64,fy+40),t['note'],23,False,width-130,GRAY)
        im.save(ROOT/t['imageAsset'],optimize=True)

# Launcher graphic drawn as repo-native assets; no generated image model needed.
def icon(size):
    im=Image.new('RGBA',(size,size),'#102A43');d=ImageDraw.Draw(im);s=size/512
    def box(coords,fill,r=0):
        coords=tuple(int(x*s) for x in coords)
        if r:d.rounded_rectangle(coords,radius=int(r*s),fill=fill)
        else:d.rectangle(coords,fill=fill)
    box((79,357,280,395),'#66869A',10)
    d.polygon([(int(x*s),int(y*s)) for x,y in [(111,349),(131,169),(206,169),(230,349)]],fill='#FFFFFF')
    box((122,185,211,207),'#16B5B2');box((116,259,222,282),'#16B5B2')
    for b in [(133,96,208,152),(176,69,263,132),(235,57,327,112)]:d.ellipse(tuple(int(x*s) for x in b),fill='#CAE9F0')
    box((306,264,421,395),'#16B5B2',19);box((325,284,402,332),'#102A43',8)
    d.line([(int(270*s),int(321*s)),(int(291*s),int(321*s)),(int(291*s),int(286*s)),(int(305*s),int(286*s))],fill='#16B5B2',width=max(1,int(9*s)))
    for cx in [339,385]:d.ellipse(tuple(int(x*s) for x in [cx-8,350,cx+8,366]),fill='white')
    return im
brand=ROOT/'assets/branding';brand.mkdir(exist_ok=True)
icon(512).save(brand/'launcher.png')
for density,size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
    folder=brand/f'mipmap-{density}';folder.mkdir(exist_ok=True);icon(size).save(folder/'ic_launcher.png')
print('31 labeled diagrams and launcher density assets rendered')
