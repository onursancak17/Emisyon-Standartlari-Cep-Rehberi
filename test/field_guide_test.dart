import 'dart:async';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:emisyon_standartlari_cep_rehberi/main.dart';

Future<void> fonts() async {
 for(final e in {'Roboto':'/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
  'MaterialIcons':'${Platform.environment['FLUTTER_ROOT']}/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf'}.entries){
  final f=File(e.value);if(f.existsSync()){final l=FontLoader(e.key)..addFont(Future.value(ByteData.sublistView(f.readAsBytesSync())));await l.load();}
 }
}
Future<void> shot(WidgetTester t,GlobalKey key,String name) async {
 await t.pump();await t.runAsync(() async {
 final b=key.currentContext!.findRenderObject() as RenderRepaintBoundary;
 final im=await b.toImage(pixelRatio:2);final bytes=await im.toByteData(format:ui.ImageByteFormat.png);
 Directory('test-output').createSync(recursive:true);File('test-output/$name.png').writeAsBytesSync(bytes!.buffer.asUint8List());im.dispose();
 });
}
void main(){
 TestWidgetsFlutterBinding.ensureInitialized();
 setUp(() {settings.scale=1;settings.dark=false;settings.rate=.45;});
 testWidgets('Two tabs, Turkish search and independent common chapter', (t) async {
  t.view.physicalSize=const Size(390,844);t.view.devicePixelRatio=1;addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);
  await t.runAsync(fonts);final data=(await t.runAsync(Content.load))!;final key=GlobalKey();
  await t.pumpWidget(RepaintBoundary(key:key,child:FieldApp(content:data)));await t.pumpAndSettle();
  expect(find.text('Ortak Saha Talimatları'),findsOneWidget);expect(find.byType(NavigationDestination),findsNWidgets(2));
  expect(t.takeException(),isNull);await shot(t,key,'home');
  await t.enterText(find.byType(TextField),'klorür');await t.pumpAndSettle();
  await t.tap(find.text('HCl • Gaz hâlindeki klorür'));await t.pumpAndSettle();
  expect(find.byType(TrainCard),findsOneWidget);expect(find.text('40 veya 100 mL'),findsNWidgets(2));
  expect(find.text('Ortak hazırlığı aç'),findsNothing);expect(find.textContaining('REVİZYON'),findsNothing);
  await t.runAsync(()async{for(final k in ['water','empty','silica']){await precacheImage(AssetImage('assets/equipment/$k.webp'),t.element(find.byType(TrainCard)));}});
  await t.pumpAndSettle();await shot(t,key,'hcl');
  await t.tap(find.text('Tam ekran • Büyüt'));await t.pumpAndSettle();expect(find.byType(InteractiveViewer),findsOneWidget);expect(t.takeException(),isNull);
  await t.pageBack();await t.pumpAndSettle();await t.pageBack();await t.pumpAndSettle();
  await t.tap(find.text('Eğitim'));await t.pumpAndSettle();await t.enterText(find.byType(TextField),'tayin sınırları');await t.pumpAndSettle();
  expect(find.text('Tayin sınırları ve ölçüm süresi'),findsOneWidget);await t.tap(find.text('Tayin sınırları ve ölçüm süresi'));await t.pumpAndSettle();
  expect(find.text('Tayin sınırını sahaya taşımak'),findsOneWidget);expect(t.takeException(),isNull);await shot(t,key,'education');
 },variant:TargetPlatformVariant.only(TargetPlatform.android),timeout:const Timeout(Duration(seconds:90)));
 testWidgets('All instructions fit narrow phone at large text', (t) async {
  t.view.physicalSize=const Size(320,800);t.view.devicePixelRatio=1;addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);
  final data=(await t.runAsync(Content.load))!;
  for(final a in [data.common,...data.manuals]){
   await t.pumpWidget(MaterialApp(home:MediaQuery(data:const MediaQueryData(size:Size(320,800),textScaler:TextScaler.linear(1.4)),child:DetailPage(article:a))));await t.pumpAndSettle();
   expect(t.takeException(),isNull,reason:'${a.id} intro');
   final heading=find.text(a.sections[2].title);await t.scrollUntilVisible(heading,180,maxScrolls:60,scrollable:find.byType(Scrollable).first);await t.pumpAndSettle();await t.tap(heading);await t.pumpAndSettle();
   expect(t.takeException(),isNull,reason:'${a.id} expanded');
   await t.pumpWidget(const SizedBox.shrink());await t.pumpAndSettle();
  }
 },variant:TargetPlatformVariant.only(TargetPlatform.android),timeout:const Timeout(Duration(seconds:90)));
 testWidgets('Android dust instructions render readable paragraphs in every section', (t) async {
  t.view.physicalSize=const Size(393,873);t.view.devicePixelRatio=1;
  addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);
  await t.runAsync(fonts);final data=(await t.runAsync(Content.load))!;
  final dust=data.manuals.singleWhere((a)=>a.id=='toz-ts');final key=GlobalKey();
  for(final dark in [false,true]){
   settings.dark=dark;
   await t.pumpWidget(RepaintBoundary(key:key,child:FieldApp(content:data)));await t.pumpAndSettle();
   await t.enterText(find.byType(TextField),'');await t.pumpAndSettle();
   await t.tap(find.text(dust.title));await t.pumpAndSettle();
   for(final section in dust.sections){
    final heading=find.text(section.title);
    await t.scrollUntilVisible(heading,150,maxScrolls:80,scrollable:find.byType(Scrollable).first);
    await t.pumpAndSettle();
    final tile=t.widget<ExpansionTile>(find.ancestor(of:heading,matching:find.byType(ExpansionTile)));
    if(!tile.initiallyExpanded){await t.tap(heading);await t.pumpAndSettle();}
    final paragraph=find.text(section.items.first);
    await t.scrollUntilVisible(paragraph,150,maxScrolls:80,scrollable:find.byType(Scrollable).first);
    await t.pumpAndSettle();
    expect(t.widget(paragraph),isA<Text>());
    if(section.title.contains('hazırlık'))await shot(t,key,dark?'dust-dark':'dust-light');
    expect(find.byType(ErrorWidget),findsNothing);
    expect(t.takeException(),isNull,reason:section.title);
   }
   expect(find.byType(SelectableText),findsNothing);
   await t.pumpWidget(const SizedBox.shrink());await t.pumpAndSettle();
  }
 },variant:TargetPlatformVariant.only(TargetPlatform.android),timeout:const Timeout(Duration(seconds:90)));
 testWidgets('Every method train renders on Android at narrow large text', (t) async {
  t.view.physicalSize=const Size(320,800);t.view.devicePixelRatio=1;
  addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);
  await t.runAsync(fonts);final data=(await t.runAsync(Content.load))!;
  for(final a in data.manuals){for(final train in a.trains){
   await t.pumpWidget(MaterialApp(home:MediaQuery(data:const MediaQueryData(size:Size(320,800),textScaler:TextScaler.linear(1.4)),child:Scaffold(body:SingleChildScrollView(child:TrainCard(train:train))))));
   await t.pumpAndSettle();
   expect(find.text(train.sampling),findsOneWidget,reason:train.name);
   expect(find.text(train.flow),findsOneWidget);
   expect(t.takeException(),isNull,reason:'${a.id}: ${train.name}');
   expect(find.byType(ErrorWidget),findsNothing);
   await t.pumpWidget(const SizedBox.shrink());await t.pumpAndSettle();
  }}
 },variant:TargetPlatformVariant.only(TargetPlatform.android),timeout:const Timeout(Duration(seconds:90)));
 testWidgets('Train choice switches diagram, conditions and narrated method together', (t) async {
  t.view.physicalSize=const Size(390,844);t.view.devicePixelRatio=1;
  addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);
  await t.runAsync(fonts);final data=(await t.runAsync(Content.load))!;
  final key=GlobalKey();
  for(final id in ['nem','halojen','hcl','flor','formaldehit','metal-en','pah','dioksin']){
   final a=data.manuals.singleWhere((a)=>a.id==id);
   await t.pumpWidget(RepaintBoundary(key:key,child:MaterialApp(home:DetailPage(article:a))));await t.pumpAndSettle();
   for(var i=0;i<a.trains.length;i++){
    final dropdown=find.byType(DropdownButtonFormField<int>);
    await t.scrollUntilVisible(dropdown,-150,maxScrolls:60,scrollable:find.byType(Scrollable).first);
    await t.pumpAndSettle();await t.tap(dropdown);await t.pumpAndSettle();
    await t.tap(find.text(a.trains[i].name).last);await t.pumpAndSettle();
    final card=t.widget<TrainCard>(find.byType(TrainCard));expect(card.train,a.trains[i]);
    final audio=t.widget<AudioPanel>(find.byType(AudioPanel));
    expect(audio.narration,contains(a.trains[i].sampling));
    expect(audio.narration,contains(a.trains[i].flow));
    expect(find.byType(BranchView),a.trains[i].branch?findsOneWidget:findsNothing);
    expect(t.takeException(),isNull,reason:'$id / $i');
    if(id=='nem'||id=='halojen'){
     await t.runAsync(()async{for(final asset in ['water','empty','silica','standard']){await precacheImage(AssetImage('assets/equipment/$asset.webp'),t.element(find.byType(TrainCard)));}});
     final diagram=find.byType(TrainView);
     await t.scrollUntilVisible(diagram,150,maxScrolls:40,scrollable:find.byType(Scrollable).first);await t.pumpAndSettle();
     await shot(t,key,'$id-$i');
    }
   }
   await t.pumpWidget(const SizedBox.shrink());await t.pumpAndSettle();
  }
  final moisture=data.manuals.singleWhere((a)=>a.id=='nem');
  expect(moisture.trains[0].bottles.map((b)=>b.amount).toList(),['100 mL','100 mL','Sıvı eklenmez','200 g']);
  expect(moisture.trains[2].bottles.first.amount,isNot('100 mL'));
 },variant:TargetPlatformVariant.only(TargetPlatform.android),timeout:const Timeout(Duration(seconds:90)));
 testWidgets('T90, amounts and device TTS use the actual instruction text', (t) async {
  final data=(await t.runAsync(Content.load))!;
  final gas=data.manuals.singleWhere((a)=>a.id=='yanma');expect(gas.sections.any((s)=>s.title.startsWith('T90')),isTrue);
  final metal=data.manuals.singleWhere((a)=>a.id=='metal-epa');expect(metal.trains.first.bottles.length,7);
  expect(metal.narration.any((s)=>s.contains('100 mL')&&s.contains('HNO₃')),isTrue);
  const channel=MethodChannel('flutter_tts');final spoken=<String>[];final calls=<String>[];
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,(call)async{
   calls.add(call.method);
   if(call.method=='isLanguageAvailable')return true;
   if(call.method=='speak'){spoken.add(call.arguments is Map ? (call.arguments as Map)['text'] as String : call.arguments as String);return 1;}
   return 1;
  });
  final n=Narrator();
  await t.runAsync(()async{await n.start(['HNO₃ 100 mL','İkinci adım']);});
  expect(spoken.length,2,reason:'${n.error}; methods: $calls; chunks: ${n.chunks}');
  expect(Narrator.pronounce('CO₂ / SO₂ / NO₂ / O₂'), 'karbondioksit / kükürt dioksit / azot dioksit / oksijen');
  expect(spoken.first,contains('nitrik asit'));expect(spoken.first,contains('100 mililitre'));
  await t.runAsync(()async{await n.pause();});expect(n.paused,isTrue);expect(n.playing,isFalse);
  await t.runAsync(()async{await n.resume();});expect(spoken.length,4);
  await t.runAsync(()async{await n.halt();});expect(calls.where((x)=>x=='stop').length,2);
  n.dispose();TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,null);
 },variant:TargetPlatformVariant.only(TargetPlatform.android));
 testWidgets('Missing Turkish voice produces an actionable message', (t)async{
  const channel=MethodChannel('flutter_tts');TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,(call)async=>call.method=='isLanguageAvailable'?false:1);
  final n=Narrator();await n.start(['Deneme']);expect(n.error,contains('Türkçe ses bulunamadı'));expect(n.playing,isFalse);n.dispose();
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,null);
 });
}

