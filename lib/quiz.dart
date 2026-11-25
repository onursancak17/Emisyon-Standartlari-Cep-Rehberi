import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class QuizQuestion {
  const QuizQuestion({required this.id,required this.prompt,required this.choices,required this.correctIndex,
    required this.explanation,required this.source,required this.topic,required this.scope,required this.standards,required this.parameters});
  final String id,prompt,explanation,source,topic,scope;
  final List<String> choices,standards,parameters;
  final int correctIndex;
  factory QuizQuestion.fromJson(Map<String,dynamic> j) => QuizQuestion(
    id:j['id'] as String,prompt:j['prompt'] as String,choices:List<String>.from(j['choices'] as List),correctIndex:j['correctIndex'] as int,
    explanation:j['explanation'] as String,source:j['source'] as String,topic:j['topic'] as String,scope:j['scope'] as String,
    standards:List<String>.from(j['standards'] as List),parameters:List<String>.from(j['parameters'] as List));
  QuizQuestion shuffled(Random random) {
    final order=List<int>.generate(choices.length,(i)=>i)..shuffle(random);
    return QuizQuestion(id:id,prompt:prompt,choices:[for(final i in order) choices[i]],correctIndex:order.indexOf(correctIndex),
      explanation:explanation,source:source,topic:topic,scope:scope,standards:standards,parameters:parameters);
  }
}

class QuizBank {
  const QuizBank({required this.questions,required this.notice,required this.catalog});
  final List<QuizQuestion> questions;
  final List<Map<String,dynamic>> catalog;
  final String notice;
  static Future<QuizBank> load() async {
    final j=jsonDecode(await rootBundle.loadString('assets/quiz_bank.json')) as Map<String,dynamic>;
    if(j['schemaVersion']!=1) throw const FormatException('Soru bankası sürümü desteklenmiyor.');
    return QuizBank(questions:[for(final q in j['questions'] as List) QuizQuestion.fromJson(Map<String,dynamic>.from(q as Map))],
      notice:j['notice'] as String,catalog:[for(final c in j['catalog'] as List) Map<String,dynamic>.from(c as Map)]);
  }
}

class QuizSession {
  QuizSession(List<QuizQuestion> pool,int count,{int? seed}) {
    final random=seed==null?Random():Random(seed);
    final selected=List<QuizQuestion>.from(pool)..shuffle(random);
    questions=selected.take(count).map((q)=>q.shuffled(random)).toList();
    answers=List<int?>.filled(questions.length,null);
  }
  late final List<QuizQuestion> questions;
  late final List<int?> answers;
  int get answered=>answers.whereType<int>().length;
  int get correct=>List.generate(questions.length,(i)=>answers[i]==questions[i].correctIndex).where((x)=>x).length;
  int get wrong=>answered-correct;
  int get blank=>questions.length-answered;
  double get score=>questions.isEmpty?0:100*correct/questions.length;
}

class QuizHomePage extends StatefulWidget {
  const QuizHomePage({super.key});
  @override
  State<QuizHomePage> createState()=>_QuizHomePageState();
}
class _QuizHomePageState extends State<QuizHomePage> {
  late final Future<QuizBank> _bank=QuizBank.load();
  @override
  Widget build(BuildContext context)=>Scaffold(appBar:AppBar(title:const Text('Açıklamalı bilgi testi')),
    body:FutureBuilder<QuizBank>(future:_bank,builder:(context,snapshot){
      if(snapshot.hasError)return Center(child:Text('Soru bankası okunamadı: ${snapshot.error}'));
      if(!snapshot.hasData)return const Center(child:CircularProgressIndicator());
      return QuizSetup(bank:snapshot.data!);
    }));
}

class QuizSetup extends StatefulWidget {
  const QuizSetup({super.key,required this.bank});
  final QuizBank bank;
  @override
  State<QuizSetup> createState()=>_QuizSetupState();
}
class _QuizSetupState extends State<QuizSetup> {
  String _scope='Karışık',_mode='Karışık',_topic='Tümü';
  int _count=20;
  List<QuizQuestion> get _scoped=>widget.bank.questions.where((q)=>_scope=='Karışık'||q.scope==_scope).toList();
  List<String> get _topics {
    final values=<String>{};
    for(final q in _scoped){
      if(_mode=='Konu')values.add(q.topic);
      if(_mode=='Standart / metot')values.addAll(q.standards);
      if(_mode=='Parametre')values.addAll(q.parameters);
    }
    final sorted=values.toList()..sort();
    return ['Tümü',...sorted];
  }
  List<QuizQuestion> get _pool=>_scoped.where((q)=>_topic=='Tümü'||_mode=='Karışık'||
    (_mode=='Konu'&&q.topic==_topic)||(_mode=='Standart / metot'&&q.standards.contains(_topic))||
    (_mode=='Parametre'&&q.parameters.contains(_topic))).toList();
  @override
  Widget build(BuildContext context){
    final pool=_pool;
    return ListView(padding:const EdgeInsets.all(16),children:[
      Text('Bilgini sahaya hazırla',style:Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight:FontWeight.w800)),
      const SizedBox(height:8),
      Text('${widget.bank.questions.length} açıklamalı soru · ${widget.bank.catalog.length} katalog başlığı · Emisyon ve imisyon'),
      const SizedBox(height:12),
      Text(widget.bank.notice,style:Theme.of(context).textTheme.bodySmall),
      const SizedBox(height:20),
      DropdownButtonFormField<String>(key:const ValueKey('quiz-scope'),value:_scope,isExpanded:true,
        decoration:const InputDecoration(labelText:'Ölçüm kapsamı',border:OutlineInputBorder()),
        items:[for(final s in ['Karışık','Emisyon','İmisyon','Ortak'])DropdownMenuItem(value:s,child:Text(s))],
        onChanged:(v){if(v!=null)setState((){_scope=v;_topic='Tümü';});}),
      const SizedBox(height:12),
      DropdownButtonFormField<String>(key:const ValueKey('quiz-mode'),value:_mode,isExpanded:true,
        decoration:const InputDecoration(labelText:'Test türü',border:OutlineInputBorder()),
        items:[for(final s in ['Karışık','Konu','Standart / metot','Parametre'])DropdownMenuItem(value:s,child:Text(s))],
        onChanged:(v){if(v!=null)setState((){_mode=v;_topic='Tümü';});}),
      if(_mode!='Karışık')...[
        const SizedBox(height:12),
        DropdownButtonFormField<String>(key:ValueKey('quiz-topic-$_scope-$_mode'),value:_topic,isExpanded:true,itemHeight:null,
          decoration:InputDecoration(labelText:_mode,border:const OutlineInputBorder()),
          selectedItemBuilder:(context)=>[for(final t in _topics)Text(t,maxLines:2,overflow:TextOverflow.ellipsis)],
          items:[for(final t in _topics)DropdownMenuItem(value:t,child:Padding(padding:const EdgeInsets.symmetric(vertical:8),child:Text(t)))],
          onChanged:(v){if(v!=null)setState(()=>_topic=v);}),
      ],
      const SizedBox(height:12),
      DropdownButtonFormField<int>(value:_count,decoration:const InputDecoration(labelText:'Soru sayısı',border:OutlineInputBorder()),
        items:[for(final n in [10,20,40,60,100,0])DropdownMenuItem(value:n,child:Text(n==0?'Bu seçimdeki tüm sorular':'$n soru'))],
        onChanged:(v){if(v!=null)setState(()=>_count=v);}),
      const SizedBox(height:16),
      Text('Bu seçimde ${pool.length} soru var. ${_count==0?pool.length:(_count<pool.length?_count:pool.length)} soruluk test açılacak.'),
      const SizedBox(height:8),
      const Text('Sorular ve seçenekler her testte karıştırılır. Cevaplar test sonunda açıklanır. İleri/geri gidebilir ve soruyu boş bırakabilirsin.'),
      const SizedBox(height:20),
      FilledButton.icon(icon:const Icon(Icons.play_arrow),label:const Text('Testi başlat'),onPressed:pool.isEmpty?null:()=>Navigator.push(context,
        MaterialPageRoute<void>(builder:(_)=>QuizExamPage(session:QuizSession(pool,_count==0?pool.length:_count))))),
      ExpansionTile(title:const Text('Standartlara göre soru kapsamı'),subtitle:const Text('Mevcut katalogdaki başlıklar ve soru adetleri'),
        children:[for(final c in widget.bank.catalog)ListTile(title:Text(c['code'] as String),
          trailing:Text('${widget.bank.questions.where((q)=>q.standards.contains(c['code'])).length}'))]),
    ]);
  }
}

class QuizExamPage extends StatefulWidget {
  const QuizExamPage({super.key,required this.session});
  final QuizSession session;
  @override
  State<QuizExamPage> createState()=>_QuizExamPageState();
}
class _QuizExamPageState extends State<QuizExamPage> {
  int _index=0;
  bool _leaving=false;
  final Stopwatch _clock=Stopwatch()..start();
  @override
  void dispose(){_clock.stop();super.dispose();}
  Future<void> _finish() async {
    final s=widget.session;
    final ok=await showDialog<bool>(context:context,builder:(context)=>AlertDialog(title:const Text('Testi bitir?'),
      content:Text('${s.answered} yanıt, ${s.blank} boş. Bitirince cevapları ve açıklamaları göreceksin.'),actions:[
        TextButton(onPressed:()=>Navigator.pop(context,false),child:const Text('Devam et')),
        FilledButton(onPressed:()=>Navigator.pop(context,true),child:const Text('Bitir ve değerlendir'))]));
    if(ok!=true||!mounted)return;
    _clock.stop();
    setState(()=>_leaving=true);
    Navigator.pushReplacement(context,MaterialPageRoute<void>(builder:(_)=>QuizResultsPage(session:s,elapsed:_clock.elapsed)));
  }
  Future<void> _exit() async {
    final ok=await showDialog<bool>(context:context,builder:(context)=>AlertDialog(title:const Text('Testten çık?'),
      content:const Text('Bu test oturumunun yanıtları kaybolacak.'),actions:[
        TextButton(onPressed:()=>Navigator.pop(context,false),child:const Text('Devam et')),
        TextButton(onPressed:()=>Navigator.pop(context,true),child:const Text('Çık'))]));
    if(ok==true&&mounted){setState(()=>_leaving=true);await Future<void>.delayed(Duration.zero);if(mounted)Navigator.pop(context);}
  }
  @override
  Widget build(BuildContext context){
    final s=widget.session;
    final q=s.questions[_index];
    return PopScope(canPop:_leaving,onPopInvokedWithResult:(didPop,result){if(!didPop)_exit();},
      child:Scaffold(appBar:AppBar(title:Text('Soru ${_index+1} / ${s.questions.length}'),actions:[TextButton(onPressed:_finish,child:const Text('Bitir'))]),
      body:ListView(padding:const EdgeInsets.all(16),children:[
        LinearProgressIndicator(value:s.answered/s.questions.length),const SizedBox(height:8),
        Text('${q.scope} · ${q.topic}'),const SizedBox(height:16),
        Text(q.prompt,style:Theme.of(context).textTheme.titleLarge),const SizedBox(height:16),
        for(var i=0;i<q.choices.length;i++) Padding(padding:const EdgeInsets.only(bottom:8),child:OutlinedButton(
          style:OutlinedButton.styleFrom(alignment:Alignment.centerLeft,padding:const EdgeInsets.all(16),
            backgroundColor:s.answers[_index]==i?Theme.of(context).colorScheme.primaryContainer:null),
          onPressed:()=>setState(()=>s.answers[_index]=i),child:Text('${String.fromCharCode(65+i)}) ${q.choices[i]}'))),
        TextButton(onPressed:s.answers[_index]==null?null:()=>setState(()=>s.answers[_index]=null),child:const Text('Yanıtı kaldır / boş bırak')),
        Row(children:[Expanded(child:OutlinedButton(onPressed:_index==0?null:()=>setState(()=>_index--),child:const Text('Önceki'))),const SizedBox(width:12),
          Expanded(child:FilledButton(onPressed:_index==s.questions.length-1?_finish:()=>setState(()=>_index++),child:Text(_index==s.questions.length-1?'Testi bitir':'Sonraki')))]),
        const SizedBox(height:16),
        Wrap(spacing:6,runSpacing:6,children:[for(var i=0;i<s.questions.length;i++)ChoiceChip(label:Text('${i+1}${s.answers[i]==null?'':' ✓'}'),selected:i==_index,onSelected:(_)=>setState(()=>_index=i))]),
      ])));
  }
}

class QuizResultsPage extends StatelessWidget {
  const QuizResultsPage({super.key,required this.session,required this.elapsed});
  final QuizSession session;
  final Duration elapsed;
  @override
  Widget build(BuildContext context){
    final s=session;
    final topics=s.questions.map((q)=>q.topic).toSet();
    return Scaffold(appBar:AppBar(title:const Text('Test sonucu ve açıklamalar')),body:ListView(padding:const EdgeInsets.all(16),children:[
      Text('${s.score.toStringAsFixed(0)} / 100',style:Theme.of(context).textTheme.headlineLarge),
      Text('${s.correct} doğru · ${s.wrong} yanlış · ${s.blank} boş · ${elapsed.inMinutes} dk ${elapsed.inSeconds.remainder(60)} sn'),
      const SizedBox(height:12),
      const Text('Puan = doğru sayısı / toplam soru × 100. Yanlış cevap doğruları götürmez; boşlar doğru sayılmaz.'),
      const SizedBox(height:16),
      Text('Konu dağılımı',style:Theme.of(context).textTheme.titleLarge),
      for(final topic in topics) Builder(builder:(context){
        final indices=List.generate(s.questions.length,(i)=>i).where((i)=>s.questions[i].topic==topic).toList();
        final correct=indices.where((i)=>s.answers[i]==s.questions[i].correctIndex).length;
        return ListTile(contentPadding:EdgeInsets.zero,title:Text(topic),trailing:Text('$correct / ${indices.length}'));
      }),
      const Divider(),
      for(var i=0;i<s.questions.length;i++)Card(child:Padding(padding:const EdgeInsets.all(14),child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
        Text('${i+1}. ${s.questions[i].prompt}',style:Theme.of(context).textTheme.titleMedium),const SizedBox(height:8),
        Text(s.answers[i]==null?'Boş bırakıldı.':'Yanıtın: ${s.questions[i].choices[s.answers[i]!]}',
          style:TextStyle(color:s.answers[i]==s.questions[i].correctIndex?Colors.green.shade800:Colors.red.shade800)),
        Text('Doğru: ${s.questions[i].choices[s.questions[i].correctIndex]}',style:const TextStyle(fontWeight:FontWeight.bold)),
        const SizedBox(height:8),SelectableText(s.questions[i].explanation),const SizedBox(height:8),
        Text('Kaynak / kapsam: ${s.questions[i].source}',style:Theme.of(context).textTheme.bodySmall),
      ]))),
      FilledButton.icon(onPressed:()=>Navigator.pop(context),icon:const Icon(Icons.replay),label:const Text('Yeni test seç')),
    ]));
  }
}
