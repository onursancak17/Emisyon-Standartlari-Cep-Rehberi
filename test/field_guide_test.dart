import 'dart:async';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
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
  expect(find.byType(TrainCard),findsOneWidget);expect(find.text('100 mL'),findsNWidgets(2));
  expect(find.text('Ortak hazırlığı aç'),findsNothing);expect(find.textContaining('REVİZYON'),findsNothing);
  await t.runAsync(()async{for(final k in ['water','empty','silica']){await precacheImage(AssetImage('assets/equipment/$k.webp'),t.element(find.byType(TrainCard)));}});
  await t.pumpAndSettle();await shot(t,key,'hcl');
  await t.tap(find.text('Tam ekran • Büyüt'));await t.pumpAndSettle();expect(find.byType(InteractiveViewer),findsOneWidget);expect(t.takeException(),isNull);
  await t.pageBack();await t.pumpAndSettle();await t.pageBack();await t.pumpAndSettle();
  await t.tap(find.text('Eğitim'));await t.pumpAndSettle();await t.enterText(find.byType(TextField),'tayin sınırları');await t.pumpAndSettle();
  expect(find.text('Tayin sınırları ve ölçüm süresi'),findsOneWidget);await t.tap(find.text('Tayin sınırları ve ölçüm süresi'));await t.pumpAndSettle();
  expect(find.text('Tayin sınırını sahaya taşımak'),findsOneWidget);expect(t.takeException(),isNull);await shot(t,key,'education');
 },timeout:const Timeout(Duration(seconds:90)));
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
 },timeout:const Timeout(Duration(seconds:90)));
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
  expect(spoken.first,contains('nitrik asit'));expect(spoken.first,contains('100 mililitre'));
  await t.runAsync(()async{await n.pause();});expect(n.paused,isTrue);expect(n.playing,isFalse);
  await t.runAsync(()async{await n.resume();});expect(spoken.length,4);
  await t.runAsync(()async{await n.halt();});expect(calls.where((x)=>x=='stop').length,greaterThanOrEqualTo(3));
  n.dispose();TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,null);
 });
 testWidgets('Missing Turkish voice produces an actionable message', (t)async{
  const channel=MethodChannel('flutter_tts');TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,(call)async=>call.method=='isLanguageAvailable'?false:1);
  final n=Narrator();await n.start(['Deneme']);expect(n.error,contains('Türkçe ses bulunamadı'));expect(n.playing,isFalse);n.dispose();
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel,null);
 });
}
