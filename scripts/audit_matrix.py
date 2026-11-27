"""Katalog başlığı sayısını nihai standart onayıyla karıştırmayan izlenebilir matris."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def attach(index,data):
    catalog={}
    for name in ('standards.json','standards_extra.json','standards_overrides.json'):
        for item in json.loads((ROOT/'assets'/name).read_text(encoding='utf-8')):catalog[item['code']]=item
    rules=[('Method 2',['velocity_epa2']),('16911',['velocity_iso16911_pitot']),('Method 5',['dust_epa5']),('Method 17',['dust_epa17']),
        ('Method 4',['moisture_epa4']),('13284',['dust_en13284_in','dust_en13284_out']),('1911',['hcl_en1911_noniso','hcl_en1911_iso','hcl_en1911_split']),
        ('26A',['halogen_epa26a']),('Method 29',['metals_epa29_hg','metals_epa29_no_hg']),('14385',['metals_en14385_full','metals_en14385_split']),
        ('12619',['toc_en12619']),('25A',['toc_epa25a']),('13649',['voc_13649_charcoal','voc_13649_td','voc_13649_dynamic']),
        ('11338',['pah_iso11338_b','pah_iso11338_b_split']),('1948',['dioxin_en1948_filter','dioxin_en1948_liquid','dioxin_en1948_split']),
        ('12341',['ambient_pm10','ambient_pm2_5']),('2341',['dustfall']),('Pasif',['passive']),('426',['cyanide_carb426']),('425',['chromium_carb425']),
        ('CTM 027',['ammonia_ctm027_empty3','ammonia_ctm027_acid3']),('207.1',['ammonia_2071_gs','ammonia_2071_mini']),('13A',['fluoride_epa13a_front','fluoride_epa13a_rear']),
        ('323',['formaldehyde_epa323']),('7935',['so2_iso7935']),('Method 8',['acid_epa8']),('Method 11',['h2s_epa11'])]
    profiles={p['id']:p for p in data}
    rows=[]
    for code,item in catalog.items():
        ids=list(dict.fromkeys(pid for needle,selected in rules if re.search(re.escape(needle)+r'(?![0-9A-Za-z])',code) for pid in selected))
        state='field_sections_checked' if ids and all(profiles[pid]['reviewState']=='sections_checked' for pid in ids) else 'comparison_open'
        reasons=[]
        if '15259' in code:
            state='source_missing';reasons+=['EN 15259:2007 tam metni yok. EPA Method 1 null açı/alternatif yer koşulları ayrı kontrol edildi; EN koşullarının yerine geçirilmez.']
        if '14789' in code or '14792' in code or '15058' in code:
            state='source_missing';reasons+=['EN 14789:2017 / EN 14792:2017 / EN 15058:2017 tam metinleri yok. Resmî kapsam ve yetkili ön izlemeler bulundu; sayısal saha kabul hükümlerinin tamamı bunlardan doğrulanamaz. ISO 12039:2019 tam metni mevcut, ayrıntılı karşılaştırması açık.']
        if '12141' in code:
            state='source_missing';reasons+=['D31 ve yeni gönderilen aynı PDF, TS ISO 12141:2004 / ISO 12141:2002 esaslıdır. Güncel ISO 12141:2024 tam metni yok; eski sayılar yeni sürüm diye sunulmaz.']
        if '1911' in code:
            state='comparison_open';reasons+=['HCl kaynak maddeleri karşılaştırıldı; EN 13284-1:2001 tarihli atfının tam metniyle süre koşulları henüz kapanmadı. 2017 baskısının süreleri eski atfa otomatik uygulanmaz.']
        if '14385' in code:
            state='comparison_open';reasons+=['Çözelti, kap, verim, yıkama ve <25 °C saha / <6 °C laboratuvar / 4 hafta karşılaştırıldı. §8.1’de 180 °C yazımının yüksek baca sıcaklığına uygulanışı ve ulusal TS baskısı eşleşmesi açık.']
        if '9096' in code:
            if state!='source_missing':state='comparison_open'
            reasons+=['ISO 9096:2017 tam D33 mevcut; bütün saha sayısal koşullarının yeni parametre kartına madde madde aktarımı henüz tamamlanmadı.']
        if '11338' in code:
            state='comparison_open';reasons+=['ISO 11338-1:2003 katalogda 2026’da teyitli. B varyantı ve -7 °C saklama görüntüden kontrol edildi; A/C varyantları ve Part 2 analitik bağlantılarının tamamı henüz kartlaştırılmadı.']
        if '1948' in code:
            state='comparison_open';reasons+=['Filtre/yoğuşturucu düzeninin seçili Ek B örnekleri ayrı çizildi. Seyreltme/soğutulmuş prob alternatiflerinin bütün koşulları ve Parts 2–3 bağlantısı henüz kapanmadı.']
        if '425' in code or '426' in code:
            state='comparison_open';reasons+=['Birincil CARB düzeni ve koruma bölümleri karşılaştırıldı. Kartta görünen numune saklama/süre ve metin içi kap numarası çelişkileri henüz kapanmadı.']
        if '2341' in code or 'Pasif' in code or '9503' in code or 'ISDL' in code:
            state='source_missing';reasons+=['İlgili tam birincil yöntem/mevzuat nüshası yeterli değil. Eğitim notu, kurum içi talimat ve yaklaşım özeti birincil standart yerine geçmez.']
        if '10780' in code:
            reasons+=['ISO 10780:1994 tam D29 mevcut ve ISO’da 2022 teyitli; EN ISO Pitot ve EPA2 kartları bu ayrı standardın nihai karşılaştırması sayılmaz.']
            if state!='source_missing':state='comparison_open'
        if '12039' in code and '14789' not in code:
            state='comparison_open';reasons+=['ISO 7935 seçili SO₂ koşulları kontrol edildi; ISO 12039 ve CTM-022’nin tüm saha yeterlilik hükümleri henüz kapanmadı.']
        if not reasons:
            reasons=['Belirtilen yöntem kartlarının kaynak izli saha bölümleri karşılaştırıldı. Bu durum bütün standardın, tüm analitik işlemlerin veya güncel ulusal uygulamanın nihai onayı değildir.']
        rows.append(dict(code=code,title=item['title'],state=state,profileIds=ids,
            sourceReferences=list(dict.fromkeys(r for pid in ids for r in profiles[pid]['sources'])),remaining=reasons))
    index['auditMatrix']=dict(asOf='2026-11-27',allStandardsFinallyVerified=False,
        meaning='Saha bölümü karşılaştırması, kaynak erişimi ve nihai teknik onay ayrı durumlardır.',
        labels=dict(field_sections_checked='Seçili saha bölümleri karşılaştırıldı',comparison_open='Teknik karşılaştırma açık',source_missing='Tam birincil kaynak eksik'),rows=rows)
    return rows

def write_report(rows):
    labels={'field_sections_checked':'Saha bölümleri karşılaştırıldı','comparison_open':'Teknik karşılaştırma açık','source_missing':'Birincil kaynak eksik'}
    lines=['# Teknik doğrulama matrisi — 27 Kasım 2026','',
        '37 katalog başlığı, 37 ayrı standart veya 37 nihai onay anlamına gelmez. Bazı başlıklarda birden fazla yöntem vardır; aynı yöntem farklı başlıklarda da geçer. **Tüm standartların nihai teknik doğrulaması tamamlanmadı.**','',
        'Aşağıdaki durumlar kaynak erişimini ve uygulamadaki seçili saha bölümlerini gösterir. Laboratuvar yeterliliği, cihaz validasyonu, ilgili mevzuat ve saha özelindeki kabul planı ayrıca gerekir.','',
        '| Katalog başlığı | Durum | Kalan karşılaştırma / kapsam |','|---|---|---|']
    for row in rows:
        lines.append('| '+row['code']+' | '+labels[row['state']]+' | '+' '.join(row['remaining']).replace('|','/')+' |')
    lines+=['','## Kaynak ayrımı','',
        'D26 dosyası ISO 16911 standardının tam metni değil, eğitim sunumudur. Tam standart L04; VOC tam metni L05’tir. D31’e eşit yeni 12141 yüklemesi 2024 baskısı değildir. Lisanslı PDF’ler açık uygulama deposuna kopyalanmaz; özgün Türkçe rehber, kaynak izleri ve dosya özetleri tutulur.','',
        'ISO 16911-1 ikinci baskı 27 Kasım 2026 kontrolünde 60.00 (under publication), planlanan tarih Aralık 2026 durumundadır. 2013 baskısıyla hazırlanmış kart yeni baskıya göre doğrulanmış sayılmaz. ISO ve EN/TS kabul tarihleri ayrı izlenir.','',
        'Kaynak: https://www.iso.org/standard/85707.html ; https://www.iso.org/standard/57947.html','']
    (ROOT/'docs/TEKNIK_DOGRULAMA_MATRISI.md').write_text('\n'.join(lines),encoding='utf-8')
