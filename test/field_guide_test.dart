import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:emisyon_standartlari_cep_rehberi/field_guide.dart';
import 'package:emisyon_standartlari_cep_rehberi/main.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late Map<String, dynamic> data;
  setUpAll(() async { data = await FieldGuideRepository.load(); });
  test('Signed angles cannot cancel each other; zero points count', () {
    expect(FieldMath.averageAbsoluteAngles([25, -25, 0]), closeTo(50/3, 1e-12));
    expect(FieldMath.averageAbsoluteAngles([20, -20]),20);
    expect(()=>FieldMath.averageAbsoluteAngles([]),throwsFormatException);
    expect(()=>FieldMath.averageAbsoluteAngles([91]),throwsFormatException);
    expect(()=>FieldMath.averageAbsoluteAngles([double.nan]),throwsFormatException);
  });
  test('Unit conversion preserves volume reference rather than changing gas state', () {
    expect(FieldMath.convert(1,'ft3'),closeTo(28.316846592,1e-10));
    expect(FieldMath.convert(32,'f'),0);
    expect(FieldMath.convert(212,'f'),100);
    expect(FieldMath.convert(1,'inhg'),closeTo(33.8638866667,1e-9));
    expect(()=>FieldMath.convert(-1,'cfm'),throwsFormatException);
    expect(()=>FieldMath.convert(double.infinity,'ft3'),throwsFormatException);
    expect(TurkishUnitText.normalize('0.60 scm / 21 scf'),contains('standart m³'));
    expect(TurkishUnitText.normalize('21 scf'),isNot(contains('Nm³')));
  });
  testWidgets('Offline catalog opens and renders the moisture method with zoom', (tester) async {
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:FieldGuideCatalog(data:data))));
    expect(find.text('Sahada doğru metot, doğru düzen'),findsOneWidget);
    final moisture=find.text('Nem');
    await tester.scrollUntilVisible(moisture,400,scrollable:find.byType(Scrollable).first);
    await tester.ensureVisible(moisture);
    await tester.pumpAndSettle();
    await tester.tap(moisture);
    await tester.pumpAndSettle();
    expect(find.textContaining('Referans yöntem — dört impinger'),findsOneWidget);
    expect(find.byType(TrainDiagram),findsOneWidget);
    expect(tester.takeException(),isNull);
  });
  testWidgets('Changing method replaces the filter topology', (tester) async {
    final profiles=(data['profiles'] as List).where((x)=>x['parameter']=='Flor / florür').map((x)=>Map<String,dynamic>.from(x as Map)).toList();
    await tester.pumpWidget(MaterialApp(home:MethodGuidePage(profiles:profiles)));
    expect(tester.widget<TrainDiagram>(find.byType(TrainDiagram)).nodes[4]['id'],'filter');
    await tester.tap(find.byType(DropdownButtonFormField<int>));
    await tester.pumpAndSettle();
    await tester.tap(find.textContaining('Filtre probdan sonra — alternatif').last);
    await tester.pumpAndSettle();
    expect(tester.widget<TrainDiagram>(find.byType(TrainDiagram)).nodes[1]['id'],'filter');
    expect(tester.takeException(),isNull);
  });
  testWidgets('Every method remains readable on a narrow phone with double text size', (tester) async {
    tester.view.physicalSize = const Size(390,844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    for (final raw in data['profiles'] as List) {
      final p = Map<String,dynamic>.from(raw as Map);
      await tester.pumpWidget(MaterialApp(key:ValueKey(p['id']),builder:(context,child)=>MediaQuery(
        data:MediaQuery.of(context).copyWith(textScaler:const TextScaler.linear(2)),child:child!),
        home:MethodGuidePage(profiles:[p])));
      await tester.pumpAndSettle();
      expect(tester.takeException(),isNull,reason:p['id'] as String);
      for(var i=0;i<6;i++) {
        await tester.drag(find.byType(ListView).first,const Offset(0,-650));
        await tester.pumpAndSettle();
        expect(tester.takeException(),isNull,reason:'${p['id']} scroll $i');
      }
    }
  });
}
