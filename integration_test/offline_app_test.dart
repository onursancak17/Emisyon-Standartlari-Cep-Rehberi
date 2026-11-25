import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:emisyon_standartlari_cep_rehberi/main.dart' as app;
import 'package:emisyon_standartlari_cep_rehberi/field_guide.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Offline Android: home, parameter, train, zoom and explained quiz', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    expect(find.textContaining('Standart verisi okunamadı'),findsNothing);
    await tester.tap(find.text('Parametre seç · Numune alma ve impinger rehberi'));
    await tester.pumpAndSettle();
    await tester.enterText(find.byType(TextField),'Hidrojen sülfür');
    await tester.pumpAndSettle();
    final parameter=find.text('Hidrojen sülfür');
    await tester.ensureVisible(parameter.last);
    await tester.tap(parameter.last);
    await tester.pumpAndSettle();
    final diagram=find.byType(TrainDiagram);
    await tester.scrollUntilVisible(diagram,300,scrollable:find.byType(Scrollable).first);
    final nodes=tester.widget<TrainDiagram>(diagram).nodes;
    expect(nodes.where((n)=>n['kind']=='impinger').length,5);
    expect(nodes.firstWhere((n)=>n['id']=='i1')['amount'],'15 mL');
    await tester.scrollUntilVisible(find.text('Şemayı tam ekran aç'),300,scrollable:find.byType(Scrollable).first);
    await tester.tap(find.text('Şemayı tam ekran aç'));
    await tester.pumpAndSettle();
    expect(find.byType(InteractiveViewer),findsOneWidget);
    await tester.pageBack();await tester.pumpAndSettle();
    await tester.pageBack();await tester.pumpAndSettle();
    await tester.pageBack();await tester.pumpAndSettle();
    await tester.tap(find.text('Bilgini sına · Emisyon / İmisyon açıklamalı testler'));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const ValueKey('quiz-scope')));
    await tester.pumpAndSettle();
    await tester.tap(find.text('İmisyon').last);
    await tester.pumpAndSettle();
    await tester.scrollUntilVisible(find.text('Testi başlat'),300,scrollable:find.byType(Scrollable).first);
    await tester.tap(find.text('Testi başlat'));
    await tester.pumpAndSettle();
    await tester.ensureVisible(find.byKey(const ValueKey('answer-0')));
    await tester.tap(find.byKey(const ValueKey('answer-0')));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Bitir'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Bitir ve değerlendir'));
    await tester.pumpAndSettle();
    expect(find.text('Test sonucu ve açıklamalar'),findsOneWidget);
    await tester.scrollUntilVisible(find.textContaining('Doğru:').first,350,scrollable:find.byType(Scrollable).first);
    expect(find.textContaining('Doğru:'),findsWidgets);
    expect(tester.takeException(),isNull);
  });
}
