import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

typedef Json = Map<String, dynamic>;

class FieldGuideRepository {
  static Future<Json> load() async {
    final data = jsonDecode(await rootBundle.loadString('assets/field_guide.json')) as Json;
    if (data['schemaVersion'] != 1) throw const FormatException('Desteklenmeyen saha rehberi sürümü.');
    return data;
  }
}

List<Json> _objects(dynamic values) => (values as List).map((e) => Map<String, dynamic>.from(e as Map)).toList();
List<String> _strings(dynamic values) => (values as List).map((e) => e.toString()).toList();
String _fold(String text) => text.replaceAll('İ', 'i').replaceAll('I', 'ı').toLowerCase();

class FieldGuidePage extends StatefulWidget {
  const FieldGuidePage({super.key});
  @override
  State<FieldGuidePage> createState() => _FieldGuidePageState();
}

class _FieldGuidePageState extends State<FieldGuidePage> {
  late final Future<Json> _data = FieldGuideRepository.load();
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Parametreye göre saha rehberi')),
    body: FutureBuilder<Json>(
      future: _data,
      builder: (context, snapshot) {
        if (snapshot.hasError) return Center(child: Text('Saha rehberi açılamadı: ${snapshot.error}'));
        if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
        final data = snapshot.data!;
        return FieldGuideCatalog(data: data);
      },
    ),
  );
}

class FieldGuideCatalog extends StatefulWidget {
  const FieldGuideCatalog({super.key, required this.data});
  final Json data;
  @override
  State<FieldGuideCatalog> createState() => _FieldGuideCatalogState();
}

class _FieldGuideCatalogState extends State<FieldGuideCatalog> {
  String _query = '';
  String _scope = 'Tümü';
  @override
  Widget build(BuildContext context) {
    final profiles = _objects(widget.data['profiles']);
    final parameters = profiles.map((e) => e['parameter'] as String).toSet().toList();
    final found = parameters.where((parameter) => profiles.where((p) => p['parameter'] == parameter && (_scope == 'Tümü' || p['scope'] == _scope)).any(
      (p) => _fold('$parameter ${p['method']} ${p['variant']}').contains(_fold(_query)))).toList();
    return ListView(padding: const EdgeInsets.all(16), children: [
      Text('Sahada doğru metot, doğru düzen', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w800)),
      const SizedBox(height: 8),
      const Text('Parametreyi seç, ardından standart ve düzenek varyantını belirle. Şema ve sayısal koşullar seçiminle birlikte değişir.'),
      const SizedBox(height: 12),
      GuideNotice(text: widget.data['notice'] as String),
      const SizedBox(height: 12),
      Wrap(spacing: 8, children: [for (final s in ['Tümü', 'Emisyon', 'İmisyon']) ChoiceChip(label: Text(s), selected: _scope == s, onSelected: (_) => setState(() => _scope = s))]),
      TextField(decoration: const InputDecoration(labelText: 'Parametre veya metot ara', prefixIcon: Icon(Icons.search), border: OutlineInputBorder()),
        onChanged: (v) => setState(() => _query = v)),
      const SizedBox(height: 12),
      FilledButton.tonalIcon(icon: const Icon(Icons.fact_check_outlined), label: const Text('Ölçüm yeri uygunluğu ve girdap açısı'),
        onPressed: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => const SiteChecksPage()))),
      OutlinedButton.icon(icon: const Icon(Icons.menu_book_outlined), label: const Text('Personelin bilmesi gereken saha esasları'),
        onPressed: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => FundamentalsPage(topics: _objects(widget.data['fundamentals']))))),
      OutlinedButton.icon(icon: const Icon(Icons.straighten), label: const Text('Birim dönüşümleri ve referans koşulları'),
        onPressed: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => const UnitsPage()))),
      OutlinedButton.icon(icon: const Icon(Icons.source_outlined), label: const Text('Kaynaklar ve sürüm kontrolleri'),
        onPressed: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => const SourcesPage()))),
      const SizedBox(height: 12),
      for (final parameter in found)
        Card(child: ListTile(
          leading: const Icon(Icons.science_outlined), title: Text(parameter),
          subtitle: Text('${profiles.where((p) => p['parameter'] == parameter).length} metot / varyant'),
          trailing: const Icon(Icons.chevron_right),
          onTap: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => MethodGuidePage(
            profiles: profiles.where((p) => p['parameter'] == parameter).toList()))),
        )),
      if (found.isEmpty) const Padding(padding: EdgeInsets.all(16), child: Text('Eşleşen parametre bulunamadı.')),
    ]);
  }
}

class MethodGuidePage extends StatefulWidget {
  const MethodGuidePage({super.key, required this.profiles});
  final List<Json> profiles;
  @override
  State<MethodGuidePage> createState() => _MethodGuidePageState();
}

class _MethodGuidePageState extends State<MethodGuidePage> {
  int _selected = 0;
  bool _includeOptional = true;
  @override
  Widget build(BuildContext context) {
    final p = widget.profiles[_selected];
    final train = _objects(p['train']);
    final selectedTrain = train.where((n) => n['optional'] != true || _includeOptional).toList();
    final pending = p['reviewState'] == 'pending';
    final sop = p['reviewState'] == 'sop_only';
    return Scaffold(
      appBar: AppBar(title: Text(p['parameter'] as String)),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        DropdownButtonFormField<int>(
          key: ValueKey('method-$_selected'), value: _selected, isExpanded: true,
          decoration: const InputDecoration(labelText: 'Standart / metot / varyant', border: OutlineInputBorder()),
          selectedItemBuilder: (context) => [for (final q in widget.profiles) Align(alignment: Alignment.centerLeft,
            child: Text(q['method'] as String, maxLines: 1, overflow: TextOverflow.ellipsis))],
          items: [for (var i = 0; i < widget.profiles.length; i++) DropdownMenuItem(value: i,
            child: Text('${widget.profiles[i]['method']}\n${widget.profiles[i]['variant']}', style: const TextStyle(fontSize: 13)))],
          onChanged: (v) { if (v != null) setState(() { _selected = v; _includeOptional = true; }); },
          itemHeight: null,
        ),
        const SizedBox(height: 12),
        Text(p['variant'] as String, style: Theme.of(context).textTheme.titleLarge),
        Text('Kaynak sürümü: ${p['sourceVersion']}'),
        const SizedBox(height: 12),
        GuideNotice(text: pending ? 'İçerik hazırlanıyor. Doğrulanmış sayısal talimat ve çizim henüz yok.' : sop
          ? 'Talimat kaynaklı aktarım. Birincil metotla karşılaştırma tamamlanmadı.'
          : p['reviewState'] == 'sections_checked' ? 'Belirtilen birincil kaynak bölümleri karşılaştırıldı. Alan ve madde izleri aşağıda. Açık kalan koşulları uygulamadan önce tamamla.'
          : 'Belirtilen arşiv kaynağındaki şema ve maddeler kontrol edildi. Tam yöntem onayı ve güncel yürürlük doğrulaması tamamlanmış değildir.'),
        const SizedBox(height: 12),
        if (train.isNotEmpty) ...[
          Text('Numune alma treni', style: Theme.of(context).textTheme.titleLarge),
          const Text('Akış soldan sağa. Şema ölçekli değildir; şekiller impinger geometrisinin imalat çizimi değildir.'),
          if (train.any((n) => n['optional'] == true)) SwitchListTile.adaptive(
            contentPadding: EdgeInsets.zero, title: const Text('İsteğe bağlı şişeleri göster'),
            subtitle: const Text('Çıkarma koşulu aşağıdaki hazırlık bölümündedir. Metot şişe numaraları korunur.'),
            value: _includeOptional, onChanged: (v) => setState(() => _includeOptional = v)),
          TrainDiagram(nodes: selectedTrain),
          OutlinedButton.icon(icon: const Icon(Icons.zoom_in), label: const Text('Şemayı tam ekran aç'),
            onPressed: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => TrainFullScreen(profile: p, nodes: selectedTrain)))),
          for (final n in selectedTrain.where((n) => n['kind'] == 'impinger' || n['kind'] == 'adsorber'))
            ListTile(contentPadding: EdgeInsets.zero, leading: const Icon(Icons.water_drop_outlined),
              title: Text('${n['label']} · ${n['amount']}'), subtitle: Text(n['content'] as String)),
        ],
        if(p['diagram']!=null)...[
          Text('Ana ve yan kol şeması',style:Theme.of(context).textTheme.titleLarge),
          const Text('Yatay kaydır; ayrıntı için tam ekran açıp iki parmakla büyüt.'),
          SingleChildScrollView(scrollDirection:Axis.horizontal,child:SizedBox(width:1400,child:Image.asset(
            p['diagram']['asset'] as String,key:const ValueKey('split-train-image'),semanticLabel:'${p['method']}: filtre sonrası ayrılan ana ve analiz yan kolu'))),
          OutlinedButton.icon(icon:const Icon(Icons.zoom_in),label:const Text('Şemayı tam ekran aç'),onPressed:()=>Navigator.push(context,
            MaterialPageRoute<void>(builder:(_)=>AssetTrainPage(profile:p)))),
          GuideSection(title:'Ortak giriş',items:_objects(p['diagram']['shared']).map((n)=>'${n['label']}: ${n['content']}').toList()),
          for(final b in _objects(p['diagram']['branches'])) GuideSection(title:b['label'] as String,
            items:_objects(b['nodes']).map((n)=>'${n['label']}: ${n['content']}').toList()),
        ],
        if (p['trainNote'] != null) GuideNotice(text: p['trainNote'] as String),
        const SizedBox(height: 12),
        for (final limit in _objects(p['limits'])) GuideSection(title: limit['label'] as String, items: [limit['value'] as String]),
        for (final phase in _objects(p['phases'])) GuideSection(title: phase['title'] as String, items: _strings(phase['items'])),
        GuideSection(title: 'Doğrulanacak ayrıntılar', items: _strings(p['gaps'])),
        for (final e in _objects(p['evidence'] ?? [])) GuideSection(title: 'Kaynak izi · ${e['field']}',
          items: ['${e['clause']} · ${_strings(e['references']).join('; ')} (PDF sayfası)']),
        Text('Kaynaklar', style: Theme.of(context).textTheme.titleLarge),
        for (final s in _objects(p['sourceDetails'] ?? [])) Padding(padding: const EdgeInsets.symmetric(vertical:8),
          child: SelectableText('${s['title']}\n${s['edition']}\n${s['reference']} · PDF sayfası${s['url'] == '' ? '' : '\n${s['url']}'}')),
        const Text('Bir koşulun henüz doğrulanmamış olması, o konuda şart bulunmadığı anlamına gelmez.'),
      ]),
    );
  }
}

class SourcesPage extends StatefulWidget {
  const SourcesPage({super.key});
  @override
  State<SourcesPage> createState() => _SourcesPageState();
}

class _SourcesPageState extends State<SourcesPage> {
  late final Future<Json> _index = rootBundle.loadString('assets/source_index.json').then((s) => jsonDecode(s) as Json);
  String _query = '';
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Kaynaklar ve sürümler')),
    body: FutureBuilder<Json>(future:_index, builder:(context,snapshot) {
      if (snapshot.hasError) return const Center(child:Text('Kaynak dizini açılamadı.'));
      if (!snapshot.hasData) return const Center(child:CircularProgressIndicator());
      final data = snapshot.data!;
      return ListView(padding:const EdgeInsets.all(16),children:[
        const GuideNotice(text:'Kaynak adları ve sürüm notları çevrimdışı okunur. Web adresi asıl metne erişim içindir. Bir katalog kaydının güncel olması, arşivdeki eski PDF’nin yenilendiği anlamına gelmez.'),
        for (final c in _objects(data['catalogChecks'] ?? [])) GuideSection(title:c['method'] as String,
          items:[if(c['currentEdition']!=null) 'Güncel katalog sürümü: ${c['currentEdition']}',c['status'] as String,c['url'] as String]),
        TextField(decoration:const InputDecoration(labelText:'Kaynak adı veya kimliği ara',prefixIcon:Icon(Icons.search)),
          onChanged:(s)=>setState(()=>_query=s)),
        for (final s in _objects(data['documents']).where((s)=>_fold('${s['id']} ${s['title']}').contains(_fold(_query))))
          Card(child:Padding(padding:const EdgeInsets.all(12),child:SelectableText(
            '${s['id']} · ${s['title']}\n${s['edition'] ?? 'Arşiv belgesi'} · ${s['pages']} PDF sayfası${s['url']==null ? '' : '\n${s['url']}'}'))),
      ]);
    }),
  );
}

class GuideNotice extends StatelessWidget {
  const GuideNotice({super.key, required this.text});
  final String text;
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(12), decoration: BoxDecoration(color: Theme.of(context).colorScheme.secondaryContainer, borderRadius: BorderRadius.circular(12)),
    child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [const Icon(Icons.info_outline, size: 20), const SizedBox(width: 8), Expanded(child: Text(text))]),
  );
}

class GuideSection extends StatelessWidget {
  const GuideSection({super.key, required this.title, required this.items});
  final String title;
  final List<String> items;
  @override
  Widget build(BuildContext context) => Card(child: Padding(padding: const EdgeInsets.all(14), child: Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [Text(title, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)),
      for (var i = 0; i < items.length; i++) Padding(padding: const EdgeInsets.only(top: 8), child: Text('${i + 1}. ${items[i]}'))],
  )));
}

class FundamentalsPage extends StatelessWidget {
  const FundamentalsPage({super.key, required this.topics});
  final List<Json> topics;
  @override
  Widget build(BuildContext context) => Scaffold(appBar: AppBar(title: const Text('Ortak saha esasları')),
    body: ListView(padding: const EdgeInsets.all(16), children: [
      const GuideNotice(text: 'Bu bölüm planlama ve kontrol çerçevesidir. Sayısal kabul sınırları ilgili standart ve sürümden seçilir.'),
      for (final t in topics) GuideSection(title: t['title'] as String, items: _strings(t['items'])),
    ]));
}

class TrainFullScreen extends StatelessWidget {
  const TrainFullScreen({super.key, required this.profile, required this.nodes});
  final Json profile;
  final List<Json> nodes;
  @override
  Widget build(BuildContext context) => Scaffold(appBar: AppBar(title: Text(profile['method'] as String)),
    body: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      Padding(padding: const EdgeInsets.all(16), child: Text('${profile['variant']}\nİki parmakla büyüt; kaydırarak tüm treni gör.')),
      Expanded(child: InteractiveViewer(constrained: false, minScale: 0.25, maxScale: 4,
        boundaryMargin: const EdgeInsets.all(80), child: TrainDiagram(nodes: nodes, scrollable: false))),
    ]));
}

class AssetTrainPage extends StatelessWidget {
  const AssetTrainPage({super.key,required this.profile});
  final Json profile;
  @override
  Widget build(BuildContext context)=>Scaffold(appBar:AppBar(title:Text(profile['method'] as String)),
    body:Center(child:InteractiveViewer(minScale:1,maxScale:12,boundaryMargin:const EdgeInsets.all(100),
      child:Image.asset(profile['diagram']['asset'] as String,semanticLabel:'Akış bölünmeli örnekleme treni'))));
}

class TrainDiagram extends StatelessWidget {
  const TrainDiagram({super.key, required this.nodes, this.scrollable = true});
  final List<Json> nodes;
  final bool scrollable;
  @override
  Widget build(BuildContext context) {
    final scene = Container(color: const Color(0xFFF4F8FB), padding: const EdgeInsets.all(16),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
        for (var i = 0; i < nodes.length; i++) ...[
          SizedBox(width: 150, child: Column(children: [
            SizedBox(width: 110, height: 120, child: CustomPaint(painter: ComponentPainter(
              kind: nodes[i]['kind'] as String, empty: (nodes[i]['content'] as String).contains('boş'), solid: (nodes[i]['content'] as String).toLowerCase().contains('silika')))),
            Text(nodes[i]['label'] as String, textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF15364B))),
            const SizedBox(height: 4),
            Text(nodes[i]['amount'] as String, textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF086F71))),
            Text(nodes[i]['content'] as String, textAlign: TextAlign.center, style: const TextStyle(color: Color(0xFF15364B), fontSize: 12)),
            if (nodes[i]['optional'] == true) const Text('İsteğe bağlı', style: TextStyle(color: Color(0xFF7C5200))),
          ])),
          if (i < nodes.length - 1) const Padding(padding: EdgeInsets.only(top: 44), child: Icon(Icons.arrow_forward, color: Color(0xFF086F71))),
        ],
      ]));
    return Semantics(label: 'Soldan sağa örnekleme treni', child: scrollable
      ? SingleChildScrollView(scrollDirection: Axis.horizontal, child: scene) : scene);
  }
}

class ComponentPainter extends CustomPainter {
  const ComponentPainter({required this.kind, required this.empty, this.solid = false});
  final String kind;
  final bool empty;
  final bool solid;
  @override
  void paint(Canvas canvas, Size size) {
    canvas.save();
    canvas.scale(size.width / 110, size.height / 120);
    final stroke = Paint()..color = const Color(0xFF24506A)..style = PaintingStyle.stroke..strokeWidth = 2.8;
    final fill = Paint()..color = const Color(0xFF8DDDD6);
    if (kind == 'impinger' || kind == 'trap') {
      final body = RRect.fromRectAndRadius(const Rect.fromLTWH(23, 30, 64, 78), const Radius.circular(10));
      if (!empty && kind == 'impinger') canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(25, 70, 60, 36), const Radius.circular(8)), fill);
      if (solid) {
        canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(25, 70, 60, 36), const Radius.circular(8)), Paint()..color = const Color(0xFFE5CE98));
        for (var x = 31.0; x < 81; x += 10) for (var y = 77.0; y < 103; y += 10) canvas.drawCircle(Offset(x, y), 1.5, Paint()..color = const Color(0xFF80623E));
      }
      canvas.drawRRect(body, stroke);
      canvas.drawPath(Path()..moveTo(0, 18)..lineTo(43, 18)..lineTo(43, 94), stroke);
      canvas.drawPath(Path()..moveTo(68, 44)..lineTo(68, 18)..lineTo(110, 18), stroke);
      canvas.drawLine(const Offset(35, 30), const Offset(77, 30), stroke);
    } else if (kind == 'filter') {
      canvas.drawLine(const Offset(0, 60), const Offset(110, 60), stroke);
      canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(27, 25, 56, 70), const Radius.circular(8)), Paint()..color = const Color(0xFFE5B971));
      for (var x = 37.0; x < 80; x += 10) canvas.drawLine(Offset(x, 32), Offset(x, 88), stroke);
    } else if (kind == 'adsorber') {
      canvas.drawLine(const Offset(0, 60), const Offset(110, 60), stroke);
      canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(14, 36, 82, 48), const Radius.circular(8)), fill);
      for (var x = 24.0; x < 91; x += 12) for (var y = 44.0; y < 80; y += 12) canvas.drawCircle(Offset(x, y), 2, stroke);
    } else if (kind == 'condenser') {
      canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(12, 22, 86, 76), const Radius.circular(10)), fill);
      final path = Path()..moveTo(0, 60);
      for (var i = 0; i < 6; i++) path.lineTo(Offset(20 + i * 14, i.isEven ? 40 : 80).dx, i.isEven ? 40 : 80);
      path.lineTo(110, 60); canvas.drawPath(path, stroke);
    } else if (kind == 'probe') {
      canvas.drawPath(Path()..moveTo(4, 85)..lineTo(4, 62)..lineTo(108, 62), stroke);
      canvas.drawLine(const Offset(10, 72), const Offset(98, 72), stroke);
    } else {
      canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(7, 25, 96, 72), const Radius.circular(12)), stroke);
      canvas.drawCircle(const Offset(55, 61), 23, stroke);
      canvas.drawLine(const Offset(55, 61), const Offset(68, 45), stroke);
    }
    canvas.restore();
  }
  @override
  bool shouldRepaint(covariant ComponentPainter oldDelegate) => oldDelegate.kind != kind || oldDelegate.empty != empty || oldDelegate.solid != solid;
}

class FieldMath {
  static double averageAbsoluteAngles(List<double> angles) {
    if (angles.isEmpty || angles.any((x) => !x.isFinite || x.abs() > 90)) throw const FormatException('Her nokta için −90° ile +90° arasında sonlu bir açı gerekli.');
    return angles.map((x) => x.abs()).reduce((a, b) => a + b) / angles.length;
  }
  static double convert(double value, String unit) {
    if (!value.isFinite || (!{'f','fdiff'}.contains(unit) && value < 0) || (unit=='f' && value < -459.67)) throw const FormatException('Geçerli bir değer gir.');
    return switch(unit) {
      'cfm' => value * 28.316846592,
      'ft3' => value * 28.316846592,
      'f' => (value - 32) * 5 / 9,
      'fdiff' => value * 5 / 9,
      'inch' => value * 25.4,
      'ft' => value * 0.3048,
      'm3h' => value * 1000 / 60,
      'psi' => value * 6.894757293168,
      'grain' => value * 64.79891,
      'grain_ft3' => value * 64.79891 / 0.028316846592,
      'inhg' => value * 33.8638866667,
      'inh2o' => value * 249.08891,
      _ => throw const FormatException('Bilinmeyen birim.'),
    };
  }
}

class UnitsPage extends StatefulWidget {
  const UnitsPage({super.key});
  @override
  State<UnitsPage> createState() => _UnitsPageState();
}
class _UnitsPageState extends State<UnitsPage> {
  String _unit = 'cfm';
  String _value = '';
  static const units = {'cfm':'ft³/dk → L/dk', 'ft3':'ft³ → L', 'm3h':'m³/saat → L/dk', 'f':'Sıcaklık: °F → °C',
    'fdiff':'Sıcaklık farkı: Δ°F → Δ°C', 'inch':'inç → mm', 'ft':'ft → m', 'psi':'psi → kPa',
    'inhg':'inHg → hPa', 'inh2o':'inH₂O → Pa', 'grain':'grain (gr) → mg', 'grain_ft3':'grain/ft³ → mg/m³'};
  @override
  Widget build(BuildContext context) {
    String result = 'Bir değer gir.';
    try {
      final value = double.parse(_value.trim().replaceAll(',', '.'));
      final converted = FieldMath.convert(value, _unit);
      final target = {'cfm':'L/dk','ft3':'L','m3h':'L/dk','f':'°C','fdiff':'Δ°C','inch':'mm','ft':'m','psi':'kPa',
        'inhg':'hPa','inh2o':'Pa','grain':'mg','grain_ft3':'mg/m³'}[_unit];
      result = '${converted.toStringAsFixed(6).replaceAll('.', ',')} $target';
    } catch (_) { if (_value.isNotEmpty) result = 'Geçerli bir sayı gir. Debi/hacim/basınç/kütle negatif, sıcaklık mutlak sıfırın altında olamaz.'; }
    return Scaffold(appBar: AppBar(title: const Text('Birim dönüşümü')), body: ListView(padding: const EdgeInsets.all(16), children: [
      DropdownButtonFormField<String>(value: _unit, isExpanded: true, itemHeight:null,
        selectedItemBuilder:(context)=>units.values.map((s)=>Align(alignment:Alignment.centerLeft,child:Text(s,maxLines:1,overflow:TextOverflow.ellipsis))).toList(),
        items: units.entries.map((e) => DropdownMenuItem(value:e.key,child:Padding(padding:const EdgeInsets.symmetric(vertical:8),child:Text(e.value)))).toList(),
        onChanged: (v) { if (v != null) setState(() => _unit = v); }),
      TextField(decoration: const InputDecoration(labelText:'Kaynak birimdeki değer'), keyboardType: const TextInputType.numberWithOptions(decimal: true, signed: true), onChanged:(v)=>setState(()=>_value=v)),
      Padding(padding: const EdgeInsets.symmetric(vertical:24), child: SelectableText(result, style:Theme.of(context).textTheme.headlineSmall)),
      const GuideNotice(text: 'Bu araç birimi dönüştürür; gazın sıcaklık, basınç, kuru/yaş baz veya referans O₂ koşulunu değiştirmez. scf → L dönüşümünde kaynak koşulları aynen korunur. Nm³ dönüşümü için referans koşulları ayrıca gerekir.'),
      const GuideSection(title:'Basınç dönüşümünün tanımı', items:['inHg için geleneksel 0 °C cıva; inH₂O için geleneksel 4 °C su sütunu karşılığı kullanılır. Cihazın referansı farklıysa kendi kalibrasyon tanımını esas al.']),
      const GuideSection(title:'Sıcaklık ve kütle ayrımı',items:[
        'Mutlak sıcaklıkta °F→°C için 32 çıkarılır. Sıcaklık farkında/toleransta bu çıkarma yapılmaz; örneğin 25 Δ°F = yaklaşık 13,89 Δ°C.',
        'grain (gr), gram (g) değildir: 1 grain = 64,79891 mg. gr/dscf çevrilirken kuru baz ve kaynağın referans koşulları korunur; sonuç kendiliğinden 0 °C Nm³ bazına dönüşmez.',
        'Kaynak: NIST SP 811, Ek B.8 — https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8',
      ]),
    ]));
  }
}

class SiteChecksPage extends StatefulWidget {
  const SiteChecksPage({super.key});
  @override
  State<SiteChecksPage> createState() => _SiteChecksPageState();
}

class _SiteChecksPageState extends State<SiteChecksPage> {
  String _angles = '';
  @override
  Widget build(BuildContext context) {
    String? result;
    if (_angles.trim().isNotEmpty) {
      try {
        final tokens = _angles.trim().split(RegExp(r'[;\s]+'));
        final values = tokens.map((x) => double.parse(x.replaceAll(',', '.'))).toList();
        final mean = FieldMath.averageAbsoluteAngles(values);
        result = '${values.length} nokta · ortalama |α| = ${mean.toStringAsFixed(2).replaceAll('.', ',')}°\n${mean > 20 ? 'EPA Method 1 §11.4: akış koşulu uygun değil; alternatif yöntem/onay değerlendirmesi gerekir.' : 'EPA Method 1 §11.4 girdap eşiği aşılmadı. Bu sonuç tek başına ölçüm yerinin tüm koşullara uygun olduğunu göstermez.'}';
      } catch (_) { result = 'Her noktanın açısını boşluk veya noktalı virgülle ayır. Eksik/ölçülemeyen noktaya 0 yazma; tüm değerler −90°…+90° aralığında olmalı.'; }
    }
    return Scaffold(appBar: AppBar(title: const Text('Ölçüm yeri ve uygunsuzluk')), body: ListView(padding: const EdgeInsets.all(16), children:[
      const GuideNotice(text:'Aşağıdaki açı prosedürü EPA Method 1 §11.4 içindir. EN/ISO ölçümlerine bu kabul eşiği otomatik uygulanmaz. Null tekniği ile üç boyutlu yön tayini farklı işlemlerdir.'),
      const GuideSection(title:'Girdap açısı nasıl ölçülür? — EPA Method 1', items:[
        'Manometreyi terazile ve sıfırla; S-tip Pitot bağlantısını ve kaçağı kontrol et.',
        'Her travers noktasında Pitot ağız düzlemlerini baca kesit düzlemine dik yerleştir; bu yön 0° referansıdır.',
        'Bu konumda Δp=0 ise α=0° kaydet. Değilse Pitotu kendi ekseninde ±90° sınırında çevirip sıfır basınç farkını bul; dönüş açısını en yakın dereceyle yaz.',
        'Bütün noktaların mutlak açılarını topla ve nokta sayısına böl. Sıfır okunan noktalar da ortalamaya dahildir; artı ve eksi açılar birbirini götürmez.',
        'Ortalama |α| >20° ise §11.4’e göre akış uygun değildir. Alternatif yöntem, gerekli yetkili onayıyla değerlendirilir. Eşiğin aşılmaması diğer uygunluk koşullarının yerine geçmez.',
      ]),
      TextField(maxLines: 3, decoration: const InputDecoration(labelText:'Ölçülmüş nokta açıları (°)', hintText:'12; -8; 0; 15', border:OutlineInputBorder()),
        keyboardType:TextInputType.text, onChanged:(v)=>setState(()=>_angles=v)),
      if (result != null) Padding(padding:const EdgeInsets.symmetric(vertical:16), child:SelectableText(result)),
      const Text('Ortalama yuvarlanmadan eşikle karşılaştırılır. Hesap yalnızca girilen noktaları içerir; nokta planının eksiksizliği ayrıca kontrol edilir.'),
      const GuideSection(title:'Uygunsuz ölçüm prosedürü', items:[
        'Güvenli olmayan erişim veya platform varsa saha güvenliği sağlanmadan ölçümü başlatma.',
        'Akış yönlü kroki, kesit, bozucu etki uzaklıkları, nokta planı ve erişilemeyen noktaları kaydet. Uygun başka düzlem/port olanağını değerlendir.',
        'Ters akış, girdap veya erişim sorunu varsa ilgili metodun uygulanabilirliğini kontrol et. Nokta sayısını rastgele artırarak uygunluk verme.',
        'Kaçak, sıcaklık, debi, izokinetik oran veya blank sınırı aşılırsa olay saatini ve etkilenen aralığı kaydet. İlgili metodun izin verdiği düzeltme/tekrar/ret yolunu kullan.',
        'Gerekli alternatif yöntem / yetkili onayını ve sapmanın sonuçlara etkisini ölçüm planında ve raporda açıkça belirt. Veriyi değiştirerek uygun hale getirme.',
      ]),
      const GuideSection(title:'EPA Method 1 §11.5 — alternatif yer prosedürü (30.05.2023)',items:[
        'Bozucunun akış yönünde 2D’den veya öncesinde 0,5D’den yakın düzlemler için alternatif prosedürü değerlendir. Uygulama yaklaşık 0,61 m’den büyük çaplarda, blokaj/duvar etkilerinin küçük olduğu kanallarla sınırlanır.',
        'Kalibre edilmiş yön algılayan probla hem pitch hem yaw ölçülür; tek S-tip Pitot null açısı yeterli değildir.',
        'Dairesel kanalda en az 40, dikdörtgende 42 nokta gerekir. 2023 açıklaması, kabul edilmiş bu yerde sonraki örnekleme ve hız ölçümlerinde de aynı asgari nokta sayılarını ister.',
        'Her noktada bileşke açı R=acos(cos(yaw)×cos(pitch)); bileşkelerin ortalaması ≤20° ve örnek standart sapması ≤10° olmalı (§12.3). Bu iki ölçüt, null tekniğinin ortalama mutlak açısıyla karıştırılmaz.',
        'Nokta yerleşimi, prob kalibrasyonu ve §11.5.3–11.5.4 işlemlerinin tamamını kaydet. Türkiye’deki seçili EN/ISO yöntemine bu EPA alternatifi kendiliğinden uygunluk sağlamaz.',
      ]),
      const GuideSection(title:'Ek kontroller', items:[
        'Pitot delikleri tıkalı mı? Hortumlar ters, ezilmiş veya yoğuşma dolu mu? Manometre sıfırı ve yön referansı doğru mu?',
        'Nozül yönü, nozül çapı, kaçak vakumu, sayaç sıcaklığı/basıncı, kalibrasyon katsayısı ve baca nemi doğru kaydedilmiş mi?',
        'Proses duruşu, filtre tıkanması, absorban taşması, adsorban kırılması, soğutma kaybı ve O₂ driftinin etkisi değerlendirilmiş mi?',
      ]),
      const GuideSection(title:'EN ölçüm yeri özeti — EPA null hesabından ayrı',items:[
        'TS EN 13284-1:2018 / EN 13284-1:2017 Ek D, EN 15259 bağlantılı olarak eksenden akış açısı <15°, ters akış olmaması, Pitot diferansiyel basıncı >5 Pa ve en yüksek/en düşük hız oranı <3:1 özetini verir.',
        'Akış yönünde düzlemin öncesinde >5 hidrolik çap, sonrasında >2 hidrolik çap düz hat; açık baca çıkışı öncesinde >5 hidrolik çap önerileri ayrı yerleşim koşullarıdır. Noktalar ve ölçme tekniği ilgili EN 15259/ISO 16911 prosedürüyle belirlenir.',
        'Bu özet, uygun ekipmanla açı/hız incelemesinin yerine geçmez. EPA’nın ±null açısı ortalamasını EN için doğrudan 15° ile karşılaştıran bir hesap uygulanmaz. Kaynak: L03 PDF s.44, Ek D; EN 15259:2007 bağlantısı.',
      ]),
      const SelectableText('Kaynak: US EPA Method 1 (30.05.2023), §11.4–11.5, §12.3. Federal Register 29.03.2023 değişikliği 30.05.2023 yürürlüğe girdi.\nhttps://www.epa.gov/system/files/documents/2023-09/2023%20Final%20MS%20%20Method%201_0.pdf\nhttps://www.epa.gov/system/files/documents/2023-04/2023%20Final%20Revisions%20Rule.pdf'),
    ]));
  }
}
