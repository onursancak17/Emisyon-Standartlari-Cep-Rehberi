import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:emisyon_standartlari_cep_rehberi/main.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUp(() {
    preferences.memoryOnly = true;
    preferences.favorites.clear();
    preferences.recent.clear();
    preferences.checks.clear();
    preferences.scale = 1;
    preferences.dark = false;
  });
  Future<void> fonts() async {
    final file = File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
    if (file.existsSync()) {
      final loader = FontLoader('Roboto')
        ..addFont(Future.value(ByteData.sublistView(file.readAsBytesSync())));
      await loader.load();
    }
  }

  Future<void> screenshot(
    WidgetTester tester,
    GlobalKey key,
    String name,
  ) async {
    await tester.pump();
    final boundary =
        key.currentContext!.findRenderObject()! as RenderRepaintBoundary;
    await tester.runAsync(() async {
      final image = await boundary.toImage(pixelRatio: 2);
      final bytes = await image.toByteData(format: ui.ImageByteFormat.png);
      Directory('test-output').createSync(recursive: true);
      File('test-output/$name.png')
          .writeAsBytesSync(bytes!.buffer.asUint8List());
      image.dispose();
    });
  }

  testWidgets(
    'Turkish search, favorites and personal checklist stay connected',
    (tester) async {
      tester.view.physicalSize = const Size(390, 844);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.runAsync(fonts);
      // Decode large JSON assets outside the test fake clock before the home future reads them.
      await tester.runAsync(StandardsRepository.loadItems);
      final key = GlobalKey();
      await tester.pumpWidget(
        RepaintBoundary(key: key, child: const StandardsApp()),
      );
      await tester.pumpAndSettle();
      expect(find.text('31 rehber'), findsOneWidget);
      expect(tester.takeException(), isNull);
      await screenshot(tester, key, 'home');
      await tester.enterText(find.byType(TextField), 'yanma gazları');
      await tester.pumpAndSettle();
      expect(find.byType(StandardCard), findsOneWidget);
      await tester.tap(find.byType(StandardCard));
      await tester.pumpAndSettle();
      await tester.tap(find.byTooltip('Favoriye ekle / çıkar'));
      await tester.pump();
      expect(preferences.favorites.length, 1);
      await tester.ensureVisible(find.widgetWithText(ChoiceChip, 'Ölçümü yap'));
      await tester.tap(find.widgetWithText(ChoiceChip, 'Ölçümü yap'));
      await tester.pumpAndSettle();
      expect(find.byType(StepCard), findsWidgets);
      expect(tester.takeException(), isNull);
      await screenshot(tester, key, 'combustion-steps');
      await tester.tap(find.text('Saha kontrol listesi'));
      await tester.pumpAndSettle();
      await tester.scrollUntilVisible(find.byType(CheckboxListTile).first, 150);
      await tester.tap(find.byType(CheckboxListTile).first);
      await tester.pump();
      expect(preferences.checks.values.single.length, 1);
      await screenshot(tester, key, 'checklist');
    },
    timeout: const Timeout(Duration(seconds: 90)),
  );
  testWidgets('Every guide and diagram fits a narrow screen with large text', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(320, 800);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final guides = await tester.runAsync(StandardsRepository.loadItems);
    expect(guides!.length, 31);
    preferences.scale = 1.3;
    for (final item in guides) {
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData(useMaterial3: true),
          home: MediaQuery(
            data: const MediaQueryData(
              size: Size(320, 800),
              textScaler: TextScaler.linear(1.3),
            ),
            child: StandardDetailPage(item: item),
          ),
        ),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull, reason: '${item.code} intro');
      await tester.ensureVisible(find.widgetWithText(ChoiceChip, 'Treni kur'));
      await tester.tap(find.widgetWithText(ChoiceChip, 'Treni kur'));
      await tester.pumpAndSettle();
      expect(find.byType(TrainCard), findsOneWidget);
      expect(tester.takeException(), isNull, reason: '${item.code} train');
      await tester.pumpWidget(const SizedBox.shrink());
      await tester.pumpAndSettle();
    }
  }, timeout: const Timeout(Duration(seconds: 90)));
  testWidgets(
    'Method-specific media, T90 and chemistry are present without duplicate records',
    (tester) async {
      final guides = await tester.runAsync(StandardsRepository.loadItems);
      expect(guides!.map((g) => g.code).toSet().length, 31);
      expect(
        guides
            .expand((g) => g.audioNotes)
            .map((a) => a.audioAsset)
            .toSet()
            .length,
        13,
      );
      final gas = guides.singleWhere((g) => g.title.startsWith('Yanma'));
      expect(maps(gas.guide['concepts']).length, 7);
      final halogen = guides.singleWhere((g) => g.code == 'EPA Method 26A');
      expect(
        maps(maps(halogen.guide['trains']).single['nodes'])
            .where((n) => (n['label'] as String).startsWith('İmpinger'))
            .length,
        6,
      );
      expect(
        guides.singleWhere((g) => g.code == 'EPA Method 323').flowRate,
        contains('0,2–0,4'),
      );
      // Media cards are idle until explicitly played; no concurrent native players are created by navigation.
      await tester.pumpWidget(MaterialApp(home: StandardDetailPage(item: gas)));
      await tester.pumpAndSettle();
      await tester.ensureVisible(
        find.widgetWithText(ChoiceChip, 'Görseller & ses'),
      );
      await tester.pumpAndSettle();
      await tester.tap(find.widgetWithText(ChoiceChip, 'Görseller & ses'));
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
    },
    timeout: const Timeout(Duration(seconds: 90)),
  );
}
