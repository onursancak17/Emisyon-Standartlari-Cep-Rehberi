import 'dart:async';
import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:shared_preferences/shared_preferences.dart';

const navy = Color(0xFF123349);
const teal = Color(0xFF07858C);
String searchKey(String s) => s.replaceAll('İ', 'i').toLowerCase()
    .replaceAll('ı', 'i').replaceAll('ş', 's').replaceAll('ğ', 'g')
    .replaceAll('ü', 'u').replaceAll('ö', 'o').replaceAll('ç', 'c')
    .replaceAll('₂', '2').replaceAll('₁', '1').replaceAll('₀', '0');
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await settings.restore();
  runApp(const FieldApp());
}

class Appearance extends ChangeNotifier {
  double scale = 1, rate = .45;
  bool dark = false;
  Future<void> restore() async {
    final p = SharedPreferencesAsync();
    scale = (await p.getDouble('manual-text-scale') ?? 1).clamp(1, 1.4);
    rate = (await p.getDouble('narration-rate') ?? .45).clamp(.25, .65);
    dark = await p.getBool('manual-dark') ?? false;
  }
  Future<void> change({double? font, double? speech, bool? night}) async {
    scale = font ?? scale; rate = speech ?? rate; dark = night ?? dark;
    notifyListeners();
    final p = SharedPreferencesAsync();
    await p.setDouble('manual-text-scale', scale);
    await p.setDouble('narration-rate', rate);
    await p.setBool('manual-dark', dark);
  }
}
final settings = Appearance();

class Section {
  Section(this.title, this.items, this.ordered);
  final String title;
  final List<String> items;
  final bool ordered;
  factory Section.fromJson(Map<String, dynamic> j) => Section(j['title'] as String,
      (j['items'] as List).cast<String>(), j['ordered'] == true);
}
class Vessel {
  Vessel.fromJson(Map<String, dynamic> j)
      : content = j['content'] as String, amount = j['amount'] as String,
        strength = j['strength'] as String, kind = j['kind'] as String,
        tip = j['tip'] as String;
  final String content, amount, strength, kind, tip;
}
class Train {
  Train.fromJson(Map<String, dynamic> j)
      : name = j['name'] as String, note = j['note'] as String,
        bottles = (j['bottles'] as List).map((x) => Vessel.fromJson(x)).toList();
  final String name, note;
  final List<Vessel> bottles;
}
class Article {
  Article.fromJson(Map<String, dynamic> j)
      : id = j['id'] as String, title = j['title'] as String,
        method = j['method'] as String, domain = j['domain'] as String,
        visual = j['visual'] as String?,
        sections = (j['sections'] as List).map((x) => Section.fromJson(x)).toList(),
        trains = ((j['trains'] ?? []) as List).map((x) => Train.fromJson(x)).toList();
  final String id, title, method, domain;
  final String? visual;
  final List<Section> sections;
  final List<Train> trains;
  String get searchable => searchKey('$title $method ${sections.map((s) => '${s.title} ${s.items.join(' ')}').join(' ')}');
  List<String> get narration => [title, method,
    for (final t in trains) ...[t.name,
      for (var i=0; i<t.bottles.length; i++)
        '${i+1}. şişe. ${t.bottles[i].content}. ${t.bottles[i].amount}. ${t.bottles[i].strength}.', t.note],
    for (final s in sections) ...[s.title, ...s.items]];
}
class Content {
  Content(this.common, this.manuals, this.training);
  final Article common;
  final List<Article> manuals, training;
  static Future<Content> load() async {
    final j = jsonDecode(await rootBundle.loadString('assets/manuals.json'));
    final t = jsonDecode(await rootBundle.loadString('assets/training.json')) as List;
    return Content(Article.fromJson(j['common']),
      (j['manuals'] as List).map((x) => Article.fromJson(x)).toList(),
      t.map((x) => Article.fromJson(x)).toList());
  }
}

class Narrator extends ChangeNotifier {
  FlutterTts? _tts;
  Future<bool>? _opening;
  bool preparing=false;
  bool playing = false, paused = false;
  String? error;
  List<String> chunks = [];
  int index = 0, offset = 0, _baseOffset = 0, _session = 0;
  bool _closed = false;
  String get current => chunks.isEmpty || index >= chunks.length ? '' : chunks[index];
  double get progress => chunks.isEmpty ? 0 :
    ((index + (current.isEmpty ? 0 : offset/current.length)) / chunks.length).clamp(0, 1);
  void announce() { if (!_closed) notifyListeners(); }
  Future<bool> init() async {
    if (_tts != null) return true;
    final result=await (_opening ??= configure());
    if(!result) _opening=null;
    return result;
  }
  Future<bool> configure() async {
    try {
      final t = FlutterTts();
      final available = await t.isLanguageAvailable('tr-TR');
      if (available != true && available != 1) {
        error = 'Telefonda Türkçe ses bulunamadı. Android metin okuma ayarlarından Türkçe sesi yükleyebilirsin.';
        announce(); return false;
      }
      await t.setLanguage('tr-TR');
      final voices=await t.getVoices;
      if(voices is List){
        final local=voices.whereType<Map>().where((v)=>v['locale'].toString().replaceAll('_','-').toLowerCase().startsWith('tr-') && v['network_required']!=true && v['network_required']!='true').toList();
        if(local.isNotEmpty){local.sort((a,b)=>(int.tryParse(b['quality'].toString())??0).compareTo(int.tryParse(a['quality'].toString())??0));await t.setVoice({'name':local.first['name'].toString(),'locale':local.first['locale'].toString()});}
      }
      await t.awaitSpeakCompletion(true);
      await t.setPitch(1);
      t.setProgressHandler((text, start, end, word) {
        if (playing) { offset = (_baseOffset + end).clamp(0, current.length).toInt(); announce(); }
      });
      t.setErrorHandler((message) { error = 'Sesli anlatım başlatılamadı: $message'; playing = false; announce(); });
      _tts = t; return true;
    } catch (_) { error = 'Ses motoruna ulaşılamadı. Android metin okuma ayarlarını kontrol et.'; announce(); return false; }
  }
  static String pronounce(String s) {
    const map = {'HNO₃':'nitrik asit', 'H₂O₂':'hidrojen peroksit', 'H₂SO₄':'sülfürik asit',
      'KMnO₄':'potasyum permanganat','NaOH':'sodyum hidroksit','CdSO₄':'kadmiyum sülfat',
      'CuSO₄':'bakır sülfat','XAD-2':'iks ad iki','T90':'T doksan','HCl':'hidrojen klorür',
      'mL':'mililitre','L/dakika':'litre bölü dakika','°C':'derece Celsius','m³':'metreküp',
      'µg':'mikrogram','mg':'miligram','±':'artı eksi','×':'çarpı',
      'CO₂':'karbondioksit','SO₂':'kükürt dioksit','NO₂':'azot dioksit','NOx':'azot oksitler','O₂':'oksijen'};
    for (final e in map.entries) { s=s.replaceAll(e.key, e.value); }
    return s;
  }
  Future<void> start(List<String> text) async {
    await halt(); chunks = text.map(pronounce).expand((value){final parts=<String>[];while(value.length>1800){var end=value.lastIndexOf('. ',1800);if(end<700)end=value.lastIndexOf(' ',1800);if(end<1)end=1800;parts.add(value.substring(0,end));value=value.substring(end).trim();}if(value.isNotEmpty)parts.add(value);return parts;}).toList(); index=0; offset=0;
    await resume();
  }
  Future<void> resume() async {
    error=null;
    final session=++_session;preparing=true;announce();
    final ready=await init();
    if(_closed || session!=_session) return;
    preparing=false;
    if(!ready || chunks.isEmpty){playing=false;announce();return;}
    if(index>=chunks.length) {index=0; offset=0;}
    playing=true; paused=false; announce();
    await _tts!.setSpeechRate(settings.rate);
    while (!_closed && playing && session==_session && index<chunks.length) {
      _baseOffset=offset;
      final phrase=current.substring(offset.clamp(0,current.length).toInt());
      if(phrase.isNotEmpty) {
        try { await _tts!.speak(phrase,focus:true); }
        catch (_) { if(session==_session) {error='Sesli anlatım kesildi. Yeniden oynatabilirsin.';playing=false;announce();} return; }
      }
      if(session!=_session || !playing || _closed) return;
      index++; offset=0; announce();
    }
    if(session==_session && !_closed) {playing=false; paused=false; announce();}
  }
  Future<void> pause() async { _session++; playing=false; paused=true; await _tts?.stop(); announce(); }
  Future<void> halt() async { _session++; preparing=false;playing=false; paused=false; await _tts?.stop(); announce(); }
  Future<void> skip(int direction) async {
    final wasPlaying=playing; await halt();
    index=(index+direction).clamp(0, math.max(0,chunks.length-1)).toInt(); offset=0;
    paused=true; announce(); if(wasPlaying) unawaited(resume());
  }
  @override void dispose() { _closed=true; _session++; unawaited(_tts?.stop() ?? Future.value()); super.dispose(); }
}

class FieldApp extends StatelessWidget {
  const FieldApp({super.key, this.content});
  final Content? content;
  @override Widget build(BuildContext context) => ListenableBuilder(listenable:settings,
    builder: (_,__) => MaterialApp(debugShowCheckedModeBanner:false,
      title:'Emisyon Saha Talimatları',
      theme: ThemeData(useMaterial3:true, brightness:Brightness.light,
        colorScheme:ColorScheme.fromSeed(seedColor:teal),
        appBarTheme:const AppBarTheme(backgroundColor:Color(0xFFF3F6F8),foregroundColor:navy,titleTextStyle:TextStyle(fontFamily:'Roboto',color:navy,fontSize:22,fontWeight:FontWeight.w700)),
        cardTheme:CardThemeData(color:Colors.white,surfaceTintColor:Colors.transparent,elevation:0,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18),side:const BorderSide(color:Color(0xFFDCE6ED)))),
        scaffoldBackgroundColor:const Color(0xFFF3F6F8),
        textTheme:const TextTheme(bodyMedium:TextStyle(fontSize:16,height:1.55),bodyLarge:TextStyle(fontSize:17,height:1.5))),
      darkTheme:ThemeData(useMaterial3:true,brightness:Brightness.dark,colorScheme:ColorScheme.fromSeed(seedColor:teal,brightness:Brightness.dark),
        textTheme:const TextTheme(bodyMedium:TextStyle(fontSize:16,height:1.55),bodyLarge:TextStyle(fontSize:17,height:1.5))),
      themeMode:settings.dark?ThemeMode.dark:ThemeMode.light,
      builder:(c,child)=>MediaQuery(data:MediaQuery.of(c).copyWith(textScaler:TextScaler.linear(MediaQuery.textScalerOf(c).scale(1)*settings.scale)),child:child!),
      home:HomePage(content:content)));
}
void showAppearance(BuildContext context) => showModalBottomSheet<void>(context:context,
  isScrollControlled:true, useSafeArea:true, builder:(c)=>ListenableBuilder(listenable:settings,builder:(_,__)=>Padding(
    padding:const EdgeInsets.all(24), child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
    Text('Okuma ve ses ayarları',style:Theme.of(c).textTheme.titleLarge),const SizedBox(height:16),
    const Text('Yazı boyutu'),Slider(value:settings.scale,min:1,max:1.4,divisions:4,label:'${(settings.scale*100).round()}%',onChanged:(v)=>unawaited(settings.change(font:v))),
    const Text('Sesli anlatım hızı'),Slider(value:settings.rate,min:.25,max:.65,divisions:8,onChanged:(v)=>unawaited(settings.change(speech:v))),
    SwitchListTile(contentPadding:EdgeInsets.zero,title:const Text('Koyu görünüm'),value:settings.dark,onChanged:(v)=>unawaited(settings.change(night:v))),
    const Text('Anlatım, telefonun Türkçe metin okuma sesini kullanır. Türkçe ses yüklüyse internet gerekmez.',style:TextStyle(fontSize:14)),
  ]))));
IconData articleIcon(Article a) => a.domain=='İmisyon'?Icons.air:
 a.id.startsWith('hiz')?Icons.speed_outlined:a.id.startsWith('toz')?Icons.grain:
 a.id=='yanma'?Icons.local_fire_department_outlined:Icons.science_outlined;

class HomePage extends StatefulWidget {
 const HomePage({super.key,this.content});final Content? content;
 @override State<HomePage> createState()=>_HomeState();
}
class _HomeState extends State<HomePage> {
 late Future<Content> future;final search=TextEditingController(); int tab=0;String domain='Emisyon';
 @override void initState(){super.initState();future=widget.content==null?Content.load():Future.value(widget.content);}
 @override void dispose(){search.dispose();super.dispose();}
 void open(Article a)=>Navigator.of(context).push(MaterialPageRoute<void>(builder:(_)=>DetailPage(article:a)));
 @override Widget build(BuildContext context)=>Scaffold(
  appBar:AppBar(title:Text(tab==0?'Ölçüm Talimatları':'Emisyon–İmisyon Eğitimi'),actions:[IconButton(tooltip:'Okuma ve ses ayarları',onPressed:()=>showAppearance(context),icon:const Icon(Icons.tune))]),
  bottomNavigationBar:NavigationBar(selectedIndex:tab,onDestinationSelected:(i)=>setState((){tab=i;search.clear();}),destinations:const[
   NavigationDestination(icon:Icon(Icons.fact_check_outlined),selectedIcon:Icon(Icons.fact_check),label:'Talimatlar'),
   NavigationDestination(icon:Icon(Icons.menu_book_outlined),label:'Eğitim')]),
  body:FutureBuilder<Content>(future:future,builder:(c,s){
   if(s.hasError) return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[const Text('İçerik açılamadı.'),TextButton(onPressed:()=>setState(()=>future=Content.load()),child:const Text('Yeniden dene'))]));
   if(!s.hasData) return const Center(child:CircularProgressIndicator());
   final data=s.data!;final query=searchKey(search.text.trim());
   final list=(tab==0?data.manuals:data.training).where((a)=>(tab==1||a.domain==domain)&&(query.isEmpty||a.searchable.contains(query))).toList();
   return ListView(padding:const EdgeInsets.fromLTRB(16,8,16,24),children:[
    Text(tab==0?'Sahada adım adım uygulama':'Konuların ayrıntılı anlatımı',style:Theme.of(c).textTheme.bodyMedium),const SizedBox(height:16),
    TextField(controller:search,onChanged:(_)=>setState((){}),decoration:InputDecoration(hintText:tab==0?'Ölçüm veya parametre ara':'Eğitim konusu ara',prefixIcon:const Icon(Icons.search),suffixIcon:search.text.isEmpty?null:IconButton(tooltip:'Aramayı temizle',onPressed:()=>setState(search.clear),icon:const Icon(Icons.close)),filled:true,border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),borderSide:BorderSide.none))),
    if(tab==0)...[const SizedBox(height:12),Card(child:ListTile(leading:const Icon(Icons.checklist,color:teal),title:const Text('Ortak Saha Talimatları',style:TextStyle(fontWeight:FontWeight.w700)),trailing:const Icon(Icons.chevron_right),onTap:()=>open(data.common))),const SizedBox(height:12),
     Row(children:[for(final d in ['Emisyon','İmisyon']) Expanded(child:Padding(padding:const EdgeInsets.symmetric(horizontal:4),child:ChoiceChip(label:SizedBox(width:double.infinity,child:Text(d,textAlign:TextAlign.center)),selected:domain==d,onSelected:(_)=>setState(()=>domain=d),showCheckmark:false)))]),],
    const SizedBox(height:12),if(list.isEmpty) const Padding(padding:EdgeInsets.all(24),child:Text('Bu aramada sonuç bulunamadı. Parametre adı veya yöntem numarasıyla arayabilirsin.')),
    for(final a in list) Card(margin:const EdgeInsets.only(bottom:8),child:ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:16,vertical:8),leading:Icon(tab==0?articleIcon(a):Icons.menu_book_outlined,color:teal),title:Text(a.title,style:const TextStyle(fontWeight:FontWeight.w700)),subtitle:Text(a.method),trailing:const Icon(Icons.chevron_right),onTap:()=>open(a))),
   ]);
  }));
}
class DetailPage extends StatefulWidget {
 const DetailPage({super.key,required this.article});final Article article;
 @override State<DetailPage> createState()=>_DetailState();
}
class _DetailState extends State<DetailPage> {
 final narrator=Narrator();
 @override void dispose(){narrator.dispose();super.dispose();}
 @override Widget build(BuildContext c){ final a=widget.article;
  return Scaffold(appBar:AppBar(title:Text(a.title),actions:[IconButton(tooltip:'Okuma ve ses ayarları',onPressed:()=>showAppearance(c),icon:const Icon(Icons.tune))]),
   body:ListView(padding:const EdgeInsets.fromLTRB(16,8,16,40),children:[
    Text(a.method,style:Theme.of(c).textTheme.titleMedium?.copyWith(color:teal)),const SizedBox(height:16),
    AudioPanel(narrator:narrator,article:a),
    if(a.trains.isNotEmpty)...[const SizedBox(height:24),Text('Ölçüm düzeneği',style:Theme.of(c).textTheme.titleLarge?.copyWith(fontWeight:FontWeight.bold)),
      for(final t in a.trains) TrainCard(train:t)],
    if(a.visual=='resin') ...[const SizedBox(height:20),ImageCard(asset:'assets/equipment/resin.webp',title:'Kondenser ve dik XAD-2 kartuşu'),
     const Padding(padding:EdgeInsets.all(8),child:Text('Gaz girişi kartuşun altında, çıkışı üstündedir. Yan bağlantılar soğutma suyuna aittir.'))],
    if(a.visual=='settled') ...[const SizedBox(height:20),const SettledCard()],
    const SizedBox(height:20),
    for(var i=0;i<a.sections.length;i++) Card(margin:const EdgeInsets.only(bottom:10),clipBehavior:Clip.antiAlias,child:ExpansionTile(
      key:PageStorageKey('${a.id}-$i'),initiallyExpanded:i==0,maintainState:true,
      title:Text(a.sections[i].title,style:const TextStyle(fontWeight:FontWeight.w700)),
      childrenPadding:const EdgeInsets.fromLTRB(16,0,16,16),children:[
       Align(alignment:Alignment.centerRight,child:TextButton.icon(onPressed:()=>unawaited(narrator.start([a.sections[i].title,...a.sections[i].items])),icon:const Icon(Icons.volume_up_outlined,size:20),label:const Text('Bu bölümü dinle'))),
       for(var j=0;j<a.sections[i].items.length;j++) Padding(padding:const EdgeInsets.only(bottom:14),child:Row(crossAxisAlignment:CrossAxisAlignment.start,children:[
        if(a.sections[i].ordered)...[CircleAvatar(radius:15,backgroundColor:teal.withValues(alpha:.12),child:Text('${j+1}',style:const TextStyle(color:teal,fontSize:14,fontWeight:FontWeight.bold))),const SizedBox(width:10)],
        Expanded(child:Text(a.sections[i].items[j],
          style:Theme.of(c).textTheme.bodyMedium,
          softWrap:true)),
       ])),
      ])),
   ]));
 }
}
class AudioPanel extends StatelessWidget {
 const AudioPanel({super.key,required this.narrator,required this.article});final Narrator narrator;final Article article;
 @override Widget build(BuildContext c)=>ListenableBuilder(listenable:narrator,builder:(_,__)=>Card(child:Padding(padding:const EdgeInsets.all(12),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
  Row(children:[IconButton.filled(tooltip:narrator.playing?'Duraklat':'Sesli anlatımı oynat',onPressed:narrator.preparing?null:()=>unawaited(narrator.playing?narrator.pause():narrator.paused?narrator.resume():narrator.start(article.narration)),icon:Icon(narrator.playing?Icons.pause:Icons.play_arrow)),const SizedBox(width:10),
   const Expanded(child:Text('Sesli anlatım',style:TextStyle(fontWeight:FontWeight.w700))),
   IconButton(tooltip:'Önceki madde',onPressed:narrator.chunks.isEmpty?null:()=>unawaited(narrator.skip(-1)),icon:const Icon(Icons.skip_previous)),
   IconButton(tooltip:'Sonraki madde',onPressed:narrator.chunks.isEmpty?null:()=>unawaited(narrator.skip(1)),icon:const Icon(Icons.skip_next)),
   IconButton(tooltip:'Anlatımı durdur',onPressed:narrator.playing||narrator.paused?()=>unawaited(narrator.halt()):null,icon:const Icon(Icons.stop)),]),
  const SizedBox(height:8),LinearProgressIndicator(value:narrator.progress),
  if(narrator.chunks.isNotEmpty) Padding(padding:const EdgeInsets.only(top:8),child:Text('${math.min(narrator.index+1,narrator.chunks.length)} / ${narrator.chunks.length} madde',style:Theme.of(c).textTheme.bodySmall)),
  if(narrator.error!=null) Padding(padding:const EdgeInsets.only(top:8),child:Text(narrator.error!,style:TextStyle(color:Theme.of(c).colorScheme.error))),
 ]))));
}

class TrainCard extends StatelessWidget {
 const TrainCard({super.key,required this.train});final Train train;
 @override Widget build(BuildContext c)=>Card(margin:const EdgeInsets.only(top:12),child:Padding(padding:const EdgeInsets.all(12),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
  Text(train.name,style:const TextStyle(fontWeight:FontWeight.w700)),const SizedBox(height:8),
  SizedBox(height:400,child:SingleChildScrollView(scrollDirection:Axis.horizontal,child:ColoredBox(color:Colors.white,child:MediaQuery(data:MediaQuery.of(c).copyWith(textScaler:TextScaler.noScaling),child:TrainView(train:train))))),
  TextButton.icon(onPressed:()=>Navigator.push(c,MaterialPageRoute<void>(builder:(_)=>TrainFullScreen(train:train))),icon:const Icon(Icons.open_in_full),label:const Text('Tam ekran • Büyüt')),
  Text(train.note),
 ])));
}
class TrainView extends StatelessWidget {
 const TrainView({super.key,required this.train});final Train train;
 @override Widget build(BuildContext c)=>SizedBox(width:train.bottles.length*190.0,height:400,child:Stack(children:[
  // The bottles are illustrative raster assets. Topology, numbering and quantities are native data.
  Positioned(top:10,left:0,right:0,child:CustomPaint(size:Size(train.bottles.length*190.0-24,20),painter:ConnectionPainter(train.bottles.length))),
  Row(crossAxisAlignment:CrossAxisAlignment.start,children:[for(var i=0;i<train.bottles.length;i++) SizedBox(width:190,child:Column(children:[
   Image.asset('assets/equipment/${train.bottles[i].tip.contains('Standart') ? 'standard' : train.bottles[i].kind}.webp',width:190,height:270,fit:BoxFit.contain,semanticLabel:'${i+1}. şişe: ${train.bottles[i].content}, ${train.bottles[i].amount}, ${train.bottles[i].strength}'),
   const SizedBox(height:4),Text('${i+1}. şişe',style:const TextStyle(color:teal,fontSize:16,fontWeight:FontWeight.w700)),
   Text(train.bottles[i].content,textAlign:TextAlign.center,style:const TextStyle(color:navy,fontSize:19,fontWeight:FontWeight.w700)),
   Text(train.bottles[i].amount,textAlign:TextAlign.center,style:const TextStyle(color:teal,fontSize:20,fontWeight:FontWeight.bold)),
   if(train.bottles[i].strength.isNotEmpty) Text(train.bottles[i].strength,textAlign:TextAlign.center,style:const TextStyle(color:navy,fontSize:17)),
  ]))]),
 ]));
}
class ConnectionPainter extends CustomPainter {
 ConnectionPainter(this.count);final int count;
 @override void paint(Canvas canvas,Size size){
  final p=Paint()..color=teal..strokeWidth=3..style=PaintingStyle.stroke;
  for(var i=0;i<count-1;i++){
   final x=167.0+i*190;canvas.drawLine(Offset(x,0),Offset(x+46,0),p);
   canvas.drawLine(Offset(x+30,0),Offset(x+23,-5),p);canvas.drawLine(Offset(x+30,0),Offset(x+23,5),p);
  }
 }
 @override bool shouldRepaint(ConnectionPainter old)=>count!=old.count;
}
class TrainFullScreen extends StatefulWidget {
 const TrainFullScreen({super.key,required this.train});final Train train;
 @override State<TrainFullScreen> createState()=>_TrainFullState();
}
class _TrainFullState extends State<TrainFullScreen> {
 final controller=TransformationController();double oldWidth=0;
 @override void didChangeDependencies(){super.didChangeDependencies();final width=MediaQuery.sizeOf(context).width;if(width!=oldWidth){oldWidth=width;controller.value=Matrix4.diagonal3Values((width/(widget.train.bottles.length*190)).clamp(.2,1).toDouble(),(width/(widget.train.bottles.length*190)).clamp(.2,1).toDouble(),1);}}
 @override void dispose(){controller.dispose();super.dispose();}
 @override Widget build(BuildContext c){final train=widget.train;return Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:Text(train.name)),body:Column(children:[
  const Padding(padding:EdgeInsets.all(12),child:Text('Soldan sağa gaz akışı • Kaydır ve iki parmakla büyüt',style:TextStyle(color:navy))),
  Expanded(child:InteractiveViewer(transformationController:controller,constrained:false,minScale:.2,maxScale:3,child:ColoredBox(color:Colors.white,child:MediaQuery(data:MediaQuery.of(c).copyWith(textScaler:TextScaler.noScaling),child:TrainView(train:train))))),
  Flexible(child:SingleChildScrollView(padding:const EdgeInsets.all(16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
    for(var i=0;i<train.bottles.length;i++) Text('${i+1}. ${train.bottles[i].content} — ${train.bottles[i].amount}${train.bottles[i].strength.isEmpty?'':' • ${train.bottles[i].strength}'}${train.bottles[i].tip.contains('Standart')?' • ${train.bottles[i].tip}':''}',style:const TextStyle(color:navy,fontSize:18,height:1.6)),
  ]))),
 ]));}
}
class ImageCard extends StatelessWidget {
 const ImageCard({super.key,required this.asset,required this.title});final String asset,title;
 @override Widget build(BuildContext c)=>Card(clipBehavior:Clip.antiAlias,child:Column(children:[
  Image.asset(asset,semanticLabel:title),TextButton.icon(onPressed:()=>Navigator.push(c,MaterialPageRoute<void>(builder:(_)=>Scaffold(backgroundColor:Colors.white,appBar:AppBar(title:Text(title)),body:InteractiveViewer(minScale:1,maxScale:5,child:Center(child:Image.asset(asset)))))),icon:const Icon(Icons.open_in_full),label:const Text('Tam ekran • Büyüt')),
 ]));
}
class SettledCard extends StatelessWidget {
 const SettledCard({super.key});
 @override Widget build(BuildContext c)=>Card(child:Padding(padding:const EdgeInsets.all(16),child:Column(children:[
  const Text('Yönlü çöken toz toplama',style:TextStyle(fontWeight:FontWeight.w700)),const SizedBox(height:16),
  AspectRatio(aspectRatio:1,child:CustomPaint(painter:SettledPainter())),
  const Text('Her toplama kabı: 10 mL 0,02 N CuSO₄',textAlign:TextAlign.center,style:TextStyle(color:teal,fontWeight:FontWeight.w700,fontSize:18)),
  const SizedBox(height:8),const Text('A kabı işletmeye bakar. Yönler ve başlık alanı cihazın doğrulanmış düzenine göre kaydedilir.'),
 ])));
}
class SettledPainter extends CustomPainter {
 void label(Canvas c,String s,Offset p,double width,{Color color=navy,double font=16}){
  final t=TextPainter(text:TextSpan(text:s,style:TextStyle(color:color,fontSize:font,fontWeight:FontWeight.bold)),textDirection:TextDirection.ltr)..layout(maxWidth:width);t.paint(c,p);
 }
 @override void paint(Canvas c,Size s){
  final w=s.width;final metal=Paint()..shader=const LinearGradient(colors:[Color(0xFF6C8290),Color(0xFFE2EAF0),Color(0xFF7D929F)]).createShader(Rect.fromLTWH(w*.43,0,w*.14,s.height));
  c.drawRRect(RRect.fromRectAndRadius(Rect.fromLTWH(w*.46,w*.39,w*.07,w*.53),const Radius.circular(4)),metal);
  c.drawLine(Offset(w*.18,w*.5),Offset(w*.82,w*.5),Paint()..color=navy..strokeWidth=8);
  c.drawLine(Offset(w*.5,w*.18),Offset(w*.5,w*.72),Paint()..color=navy..strokeWidth=7);
  for(final e in [('A',.50,.18),('B',.79,.45),('C',.50,.68),('D',.21,.45)]){
   final x=w*e.$2,y=w*e.$3;final rect=Rect.fromCenter(center:Offset(x,y+20),width:w*.17,height:w*.20);
   c.drawRRect(RRect.fromRectAndRadius(rect,const Radius.circular(10)),Paint()..color=const Color(0xFFDDEFF5));
   c.drawRRect(RRect.fromRectAndRadius(rect,const Radius.circular(10)),Paint()..color=const Color(0xFF6F9BAD)..style=PaintingStyle.stroke..strokeWidth=2);
   final f=Path()..moveTo(x-w*.12,y-w*.12)..lineTo(x+w*.12,y-w*.12)..lineTo(x+w*.035,y+w*.01)..lineTo(x-w*.035,y+w*.01)..close();c.drawPath(f,metal);
   label(c,e.$1,Offset(x-6,y+20),30,font:18);
  }
  label(c,'İŞLETME YÖNÜ',Offset(w*.28,0),w*.6,color:teal,font:15);
  c.drawLine(Offset(w*.5,w*.07),Offset(w*.5,w*.13),Paint()..color=teal..strokeWidth=3);
  c.drawLine(Offset(w*.23,w*.93),Offset(w*.77,w*.93),Paint()..color=navy..strokeWidth=5);
 }
 @override bool shouldRepaint(SettledPainter old)=>false;
}
