import 'dart:async';
import 'dart:convert';
import 'dart:math';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:just_audio/just_audio.dart';
import 'package:just_audio_background/just_audio_background.dart';
import 'package:shared_preferences/shared_preferences.dart';

const navy = Color(0xFF102A43);
const teal = Color(0xFF087F8C);
String searchKey(String s) => s
    .toLowerCase()
    .replaceAll('ı', 'i')
    .replaceAll('ş', 's')
    .replaceAll('ğ', 'g')
    .replaceAll('ü', 'u')
    .replaceAll('ö', 'o')
    .replaceAll('ç', 'c')
    .replaceAll('₁', '1')
    .replaceAll('₂', '2')
    .replaceAll('ₓ', 'x')
    .replaceAll(RegExp(r'\s+'), ' ')
    .trim();
final preferences = UserPreferences();
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await preferences.restore();
  if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
    await JustAudioBackground.init(
      androidNotificationChannelId: 'com.onursancak.emisyon.audio',
      androidNotificationChannelName: 'Sesli saha anlatımı',
      androidNotificationOngoing: true,
    );
  }
  runApp(const StandardsApp());
}

class UserPreferences extends ChangeNotifier {
  late final _prefs = SharedPreferencesAsync();
  bool memoryOnly = false;
  bool dark = false;
  double scale = 1;
  final Set<String> favorites = {};
  final List<String> recent = [];
  final Map<String, Set<String>> checks = {};
  Future<void> restore() async {
    favorites.addAll(await _prefs.getStringList('favorites') ?? []);
    recent.addAll(await _prefs.getStringList('recent') ?? []);
    dark = await _prefs.getBool('dark') ?? false;
    scale = (await _prefs.getDouble('scale') ?? 1).clamp(1, 1.3);
    try {
      final j = jsonDecode(
        await _prefs.getString('checks') ?? '{}',
      ) as Map<String, dynamic>;
      for (final e in j.entries) {
        checks[e.key] = StandardItem.listFromDynamic(e.value).toSet();
      }
    } catch (_) {
      checks.clear();
    }
  }

  Future<void> favorite(String code) async {
    if (!favorites.remove(code)) favorites.add(code);
    notifyListeners();
    if (!memoryOnly)
      await _prefs.setStringList('favorites', favorites.toList());
  }

  Future<void> visit(String code) async {
    recent.remove(code);
    recent.insert(0, code);
    if (recent.length > 12) recent.removeLast();
    notifyListeners();
    if (!memoryOnly) await _prefs.setStringList('recent', recent);
  }

  Future<void> mark(String code, String task, bool value) async {
    final s = checks.putIfAbsent(code, () => {});
    if (value) {
      s.add(task);
    } else {
      s.remove(task);
    }
    notifyListeners();
    await saveChecks();
  }

  Future<void> reset(String code) async {
    checks.remove(code);
    notifyListeners();
    await saveChecks();
  }

  Future<void> saveChecks() async {
    if (!memoryOnly)
      await _prefs.setString(
        'checks',
        jsonEncode(checks.map((k, v) => MapEntry(k, v.toList()))),
      );
  }

  Future<void> appearance({bool? isDark, double? textScale}) async {
    dark = isDark ?? dark;
    scale = textScale ?? scale;
    notifyListeners();
    if (!memoryOnly) {
      await _prefs.setBool('dark', dark);
      await _prefs.setDouble('scale', scale);
    }
  }
}

class StandardsApp extends StatelessWidget {
  const StandardsApp({super.key, this.initialItems});
  final List<StandardItem>? initialItems;
  ThemeData theme(Brightness b) => ThemeData(
    useMaterial3: true,
    brightness: b,
    colorScheme: ColorScheme.fromSeed(seedColor: teal, brightness: b),
    scaffoldBackgroundColor: b == Brightness.light
        ? const Color(0xFFF3F7FA)
        : const Color(0xFF0E1C28),
    textTheme: const TextTheme(
      bodyMedium: TextStyle(fontSize: 16, height: 1.55),
      bodyLarge: TextStyle(fontSize: 17, height: 1.5),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(18),
        borderSide: BorderSide.none,
      ),
    ),
  );
  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: preferences,
    builder: (_, __) => MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Emisyon İmisyon Ölçüm Standartları',
      theme: theme(Brightness.light),
      darkTheme: theme(Brightness.dark),
      themeMode: preferences.dark ? ThemeMode.dark : ThemeMode.light,
      builder: (context, child) => MediaQuery(
        data: MediaQuery.of(context).copyWith(
          textScaler: TextScaler.linear(
            MediaQuery.textScalerOf(context).scale(1) * preferences.scale,
          ),
        ),
        child: child!,
      ),
      home: StandardsHomePage(initialItems: initialItems),
    ),
  );
}

IconData iconFor(String group) => switch (group) {
  'Partikül madde' => Icons.grain,
  'Yanma gazları' => Icons.local_fire_department_outlined,
  'Halojen ve asit gazları' => Icons.science_outlined,
  'Metaller' => Icons.layers_outlined,
  'Organik bileşikler' => Icons.bubble_chart_outlined,
  'İmisyon' => Icons.air,
  'Hız ve debi' => Icons.speed,
  'Kalite kontrol' => Icons.fact_check_outlined,
  _ => Icons.biotech,
};

class StandardsHomePage extends StatefulWidget {
  const StandardsHomePage({super.key, this.initialItems});
  final List<StandardItem>? initialItems;
  @override
  State<StandardsHomePage> createState() => _HomeState();
}

class _HomeState extends State<StandardsHomePage> {
  late Future<List<StandardItem>> future;
  final search = TextEditingController();
  int tab = 0;
  String domain = 'Tümü', group = 'Tümü';
  @override
  void initState() {
    super.initState();
    future = widget.initialItems == null
        ? StandardsRepository.loadItems()
        : Future.value(widget.initialItems);
  }

  @override
  void dispose() {
    search.dispose();
    super.dispose();
  }

  void open(StandardItem item) {
    unawaited(preferences.visit(item.code));
    Navigator.push(
      context,
      MaterialPageRoute<void>(builder: (_) => StandardDetailPage(item: item)),
    );
  }

  void settings() => showModalBottomSheet<void>(
    context: context,
    useSafeArea: true,
    isScrollControlled: true,
    builder: (context) => ListenableBuilder(
      listenable: preferences,
      builder: (_, __) => Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Görünüm ve kullanım',
              style: TextStyle(fontSize: 23, fontWeight: FontWeight.w800),
            ),
            SwitchListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text('Koyu tema'),
              value: preferences.dark,
              onChanged: (v) => preferences.appearance(isDark: v),
            ),
            const Text('Yazı boyutu'),
            Slider(
              value: preferences.scale,
              min: 1,
              max: 1.3,
              divisions: 3,
              label: '%${(preferences.scale * 100).round()}',
              onChanged: (v) => preferences.appearance(textScale: v),
            ),
            const Divider(),
            const Text(
              'Saha Rehberi · 1.0.0\n31 rehber, numaralı çizimler ve mevcut ses kayıtları çevrimdışı kullanılabilir.\n\nPrensip şeması ile kaynakta doğrulanan düzenek ayrımı her metotta belirtilir.',
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    ),
  );
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: const Text(
        'Saha Rehberi',
        style: TextStyle(fontWeight: FontWeight.w800),
      ),
      actions: [
        IconButton(
          tooltip: 'Görünüm ve kullanım',
          onPressed: settings,
          icon: const Icon(Icons.tune_rounded),
        ),
      ],
    ),
    bottomNavigationBar: NavigationBar(
      selectedIndex: tab,
      onDestinationSelected: (v) => setState(() => tab = v),
      destinations: const [
        NavigationDestination(
          icon: Icon(Icons.menu_book_outlined),
          label: 'Rehber',
        ),
        NavigationDestination(
          icon: Icon(Icons.bookmark_border),
          label: 'Favoriler',
        ),
        NavigationDestination(icon: Icon(Icons.history), label: 'Son açılan'),
        NavigationDestination(icon: Icon(Icons.headphones), label: 'Dinle'),
      ],
    ),
    body: SafeArea(
      child: FutureBuilder<List<StandardItem>>(
        future: future,
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done)
            return const Center(child: CircularProgressIndicator());
          if (snap.hasError)
            return Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('Rehber açılamadı.'),
                  FilledButton(
                    onPressed: () => setState(
                      () => future = StandardsRepository.loadItems(),
                    ),
                    child: const Text('Yeniden dene'),
                  ),
                ],
              ),
            );
          final all = snap.data!;
          return ListenableBuilder(
            listenable: preferences,
            builder: (context, _) {
              if (tab == 3) {
                final notes = <String, AudioNote>{};
                final methods = <String, Set<String>>{};
                for (final g in all) {
                  for (final a in g.audioNotes) {
                    notes[a.audioAsset] = a;
                    methods.putIfAbsent(a.audioAsset, () => {}).add(g.code);
                  }
                }
                final ordered = notes.values.toList()
                  ..sort((a, b) => a.sortOrder.compareTo(b.sortOrder));
                return ListView(
                  padding: const EdgeInsets.all(20),
                  children: [
                    const Text(
                      'Sesli saha eğitimi',
                      style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    Text('${ordered.length} mevcut kayıt · çevrimdışı'),
                    const SizedBox(height: 12),
                    const _InfoBlock(
                      title: 'Dinle ve rehberle karşılaştır',
                      body: 'Kayıtlar korunmuştur; yeni seslendirme yapılmamıştır. Bir kayıt birden fazla yöntemi kapsayabilir. Sayısal şartları yazılı rehber ve seçilen metot sürümüyle doğrula.',
                    ),
                    for (final a in ordered)
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Padding(
                            padding: const EdgeInsets.only(bottom: 8),
                            child: Text(
                              methods[a.audioAsset]!.join(' · '),
                              style: Theme.of(context).textTheme.bodySmall,
                            ),
                          ),
                          _AudioCard(note: a),
                        ],
                      ),
                  ],
                );
              }
              var items = all
                  .where(
                    (g) =>
                        (tab != 1 || preferences.favorites.contains(g.code)) &&
                        (tab != 2 || preferences.recent.contains(g.code)),
                  )
                  .toList();
              if (tab == 2)
                items.sort(
                  (a, b) => preferences.recent
                      .indexOf(a.code)
                      .compareTo(preferences.recent.indexOf(b.code)),
                );
              items = items
                  .where(
                    (g) =>
                        (domain == 'Tümü' || g.category == domain) &&
                        (group == 'Tümü' || g.guide['group'] == group) &&
                        searchKey(g.searchText)
                            .contains(searchKey(search.text)),
                  )
                  .toList();
              final groups = all
                  .where((g) => domain == 'Tümü' || g.category == domain)
                  .map((g) => g.guide['group'] as String)
                  .toSet()
                  .toList();
              return CustomScrollView(
                slivers: [
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(20, 8, 20, 12),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          if (tab == 0)
                            Container(
                              padding: const EdgeInsets.all(20),
                              decoration: BoxDecoration(
                                color: navy,
                                borderRadius: BorderRadius.circular(26),
                              ),
                              child: Row(
                                children: [
                                  Image.asset(
                                    'assets/branding/launcher.png',
                                    width: 66,
                                    height: 66,
                                    excludeFromSemantics: true,
                                  ),
                                  const SizedBox(width: 12),
                                  const Expanded(
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          'Emisyon & İmisyon',
                                          style: TextStyle(
                                            fontSize: 23,
                                            fontWeight: FontWeight.w800,
                                            color: Colors.white,
                                          ),
                                        ),
                                        SizedBox(height: 6),
                                        Text(
                                          'Hazırlan. Kur. Ölç. Kontrol et.',
                                          style: TextStyle(
                                            fontSize: 15,
                                            color: Color(0xFFC7E7EA),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          if (tab != 0)
                            Text(
                              tab == 1
                                  ? 'Favori ölçümlerin'
                                  : 'Kaldığın yerden devam et',
                              style: const TextStyle(
                                fontSize: 25,
                                fontWeight: FontWeight.w800,
                              ),
                            ),
                          const SizedBox(height: 18),
                          TextField(
                            controller: search,
                            onChanged: (_) => setState(() {}),
                            decoration: InputDecoration(
                              hintText: 'Parametre, metot veya kavram ara',
                              prefixIcon: const Icon(Icons.search),
                              suffixIcon: search.text.isEmpty
                                  ? null
                                  : IconButton(
                                      tooltip: 'Aramayı temizle',
                                      onPressed: () {
                                        search.clear();
                                        setState(() {});
                                      },
                                      icon: const Icon(Icons.close),
                                    ),
                            ),
                          ),
                          const SizedBox(height: 12),
                          Wrap(
                            spacing: 8,
                            children: ['Tümü', 'Emisyon', 'İmisyon']
                                .map(
                                  (s) => ChoiceChip(
                                    label: Text(s),
                                    selected: domain == s,
                                    onSelected: (_) => setState(() {
                                      domain = s;
                                      group = 'Tümü';
                                    }),
                                  ),
                                )
                                .toList(),
                          ),
                          const SizedBox(height: 8),
                          SizedBox(
                            height: 48,
                            child: ListView(
                              scrollDirection: Axis.horizontal,
                              children: ['Tümü', ...groups]
                                  .map(
                                    (s) => Padding(
                                      padding: const EdgeInsets.only(right: 8),
                                      child: ChoiceChip(
                                        label: Text(s),
                                        selected: group == s,
                                        onSelected: (_) =>
                                            setState(() => group = s),
                                      ),
                                    ),
                                  )
                                  .toList(),
                            ),
                          ),
                          const SizedBox(height: 12),
                          Row(
                            children: [
                              const Icon(
                                Icons.offline_bolt,
                                size: 18,
                                color: teal,
                              ),
                              const SizedBox(width: 6),
                              const Expanded(
                                child: Text('Çevrimdışı saha rehberi'),
                              ),
                              Text(
                                '${items.length} rehber',
                                style: const TextStyle(
                                  fontWeight: FontWeight.w800,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                  if (items.isEmpty)
                    const SliverFillRemaining(
                      hasScrollBody: false,
                      child: Center(
                        child: Padding(
                          padding: EdgeInsets.all(28),
                          child: Text(
                            'Bu seçimde rehber bulunamadı. Favoriye eklemek için yer imi simgesini kullan.',
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ),
                    ),
                  SliverList.builder(
                    itemCount: items.length,
                    itemBuilder: (context, i) => Padding(
                      padding: const EdgeInsets.fromLTRB(20, 0, 20, 12),
                      child: StandardCard(
                        item: items[i],
                        onTap: () => open(items[i]),
                      ),
                    ),
                  ),
                  const SliverToBoxAdapter(child: SizedBox(height: 20)),
                ],
              );
            },
          );
        },
      ),
    ),
  );
}

class StandardCard extends StatelessWidget {
  const StandardCard({super.key, required this.item, required this.onTap});
  final StandardItem item;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) => Card(
    margin: EdgeInsets.zero,
    elevation: 0,
    child: InkWell(
      borderRadius: BorderRadius.circular(16),
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.primaryContainer,
                    borderRadius: BorderRadius.circular(13),
                  ),
                  child: Icon(
                    iconFor(item.guide['group'] as String),
                    color: teal,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        item.title,
                        style: const TextStyle(
                          fontSize: 18,
                          height: 1.3,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      const SizedBox(height: 5),
                      Text(
                        item.code,
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
                ),
                IconButton(
                  tooltip: 'Favoriye ekle / çıkar',
                  onPressed: () => preferences.favorite(item.code),
                  icon: Icon(
                    preferences.favorites.contains(item.code)
                        ? Icons.bookmark
                        : Icons.bookmark_border,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(item.purpose, maxLines: 2, overflow: TextOverflow.ellipsis),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                _MiniChip(label: item.guide['group'] as String),
                const _MiniChip(label: 'Adım adım'),
                if (item.audioNotes.isNotEmpty)
                  _MiniChip(label: '${item.audioNotes.length} ses kaydı'),
              ],
            ),
          ],
        ),
      ),
    ),
  );
}

const stages = [
  'Ölçümü tanı',
  'Hazırlan',
  'Treni kur',
  'Ölçümü yap',
  'Numuneyi toparla',
  'Kontrol et',
  'Görseller & ses',
  'Kaynaklar',
];
const stageKeys = [
  'intro',
  'preparation',
  'setup',
  'sampling',
  'recovery',
  'checks',
  'media',
  'sources',
];
List<Map<String, dynamic>> maps(dynamic v) =>
    v is List ? v.whereType<Map<String, dynamic>>().toList() : [];

class StandardDetailPage extends StatefulWidget {
  const StandardDetailPage({super.key, required this.item});
  final StandardItem item;
  @override
  State<StandardDetailPage> createState() => _DetailState();
}

class _DetailState extends State<StandardDetailPage> {
  int stage = 0;
  final scroll = ScrollController();
  @override
  void dispose() {
    scroll.dispose();
    super.dispose();
  }

  void select(int n) {
    setState(() => stage = n);
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  List<VisualNote> visuals(String key) {
    const mapping = {
      'intro': ['purpose', 'quality'],
      'preparation': ['equipment'],
      'setup': ['flowRate'],
      'sampling': ['fieldSteps'],
      'checks': ['criticalControls', 'acceptance', 'reporting'],
    };
    return widget.item.visualNotes
        .where((v) => (mapping[key] ?? []).contains(v.placement))
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    final i = widget.item;
    final g = i.guide;
    final key = stageKeys[stage];
    return Scaffold(
      appBar: AppBar(
        title: Text(i.code, maxLines: 2, style: const TextStyle(fontSize: 16)),
        actions: [
          ListenableBuilder(
            listenable: preferences,
            builder: (_, __) => IconButton(
              tooltip: 'Favoriye ekle / çıkar',
              onPressed: () => preferences.favorite(i.code),
              icon: Icon(
                preferences.favorites.contains(i.code)
                    ? Icons.bookmark
                    : Icons.bookmark_border,
              ),
            ),
          ),
        ],
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(60),
          child: SizedBox(
            height: 60,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              children: stages.indexed
                  .map(
                    (e) => Padding(
                      padding: const EdgeInsets.only(right: 8, bottom: 8),
                      child: ChoiceChip(
                        label: Text(e.$2),
                        selected: stage == e.$1,
                        onSelected: (_) => select(e.$1),
                      ),
                    ),
                  )
                  .toList(),
            ),
          ),
        ),
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Wrap(
            alignment: WrapAlignment.spaceBetween,
            spacing: 8,
            runSpacing: 6,
            children: [
              OutlinedButton.icon(
                onPressed: () => Navigator.push(
                  context,
                  MaterialPageRoute<void>(
                    builder: (_) => ChecklistPage(item: i),
                  ),
                ),
                icon: const Icon(Icons.checklist),
                label: const Text('Saha kontrol listesi'),
              ),
              if (stage < 7)
                FilledButton.icon(
                  onPressed: () => select(stage + 1),
                  icon: const Icon(Icons.arrow_forward, size: 18),
                  label: const Text('Sonraki'),
                ),
            ],
          ),
        ),
      ),
      body: SafeArea(
        child: ListView(
          controller: scroll,
          padding: const EdgeInsets.fromLTRB(20, 18, 20, 24),
          children: [
            Text(
              i.title,
              style: Theme.of(context).textTheme.headlineSmall
                  ?.copyWith(fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 6,
              children: [
                _MiniChip(label: i.category),
                _MiniChip(label: g['group'] as String),
                _MiniChip(label: '${stage + 1} / 8'),
              ],
            ),
            const SizedBox(height: 22),
            Text(
              stages[stage],
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 12),
            if (key == 'intro') ...[
              _InfoBlock(title: 'Bu ölçüm neden yapılır?', body: i.purpose),
              _InfoBlock(
                title: 'Yöntemin prensibi',
                body: g['method'] as String,
              ),
              _InfoBlock(title: 'Süre nasıl belirlenir?', body: i.duration),
              _InfoBlock(title: 'Debi ve hacim', body: i.flowRate),
              if (i.audioNotes.isNotEmpty)
                OutlinedButton.icon(
                  onPressed: () => select(6),
                  icon: const Icon(Icons.headphones),
                  label: const Text('İlgili eğitim kaydını dinle'),
                ),
            ],
            if (key == 'preparation')
              ExpansionTile(
                title: const Text('Cihaz ve ekipman listesi'),
                children: [
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: i.equipment
                          .map(
                            (s) => Padding(
                              padding: const EdgeInsets.only(bottom: 10),
                              child: Text('• $s'),
                            ),
                          )
                          .toList(),
                    ),
                  ),
                ],
              ),
            if (key == 'setup')
              for (final t in maps(g['trains'])) TrainCard(train: t),
            for (final e in maps(g[key]).indexed)
              StepCard(number: e.$1 + 1, point: e.$2),
            if (key == 'sampling' && maps(g['concepts']).isNotEmpty) ...[
              const SizedBox(height: 18),
              const Text(
                'T90 · açıklama ve saha uygulaması',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 12),
              for (final e in maps(g['concepts']).indexed)
                StepCard(number: e.$1 + 1, point: e.$2),
            ],
            _VisualNotesBlock(notes: visuals(key)),
            if (key == 'checks' && i.mistakes.isNotEmpty)
              ExpansionTile(
                title: const Text('Sık yapılan hatalar'),
                children: i.mistakes
                    .map(
                      (s) => ListTile(
                        leading: const Icon(Icons.warning_amber_rounded),
                        title: Text(s),
                      ),
                    )
                    .toList(),
              ),
            if (key == 'media') ...[
              const _InfoBlock(
                title: 'Mevcut eğitim kayıtları',
                body: 'Bir kayıt birden fazla metodu kapsayabilir. Yeni seslendirme yapılmamıştır; güncel sayısal şartları yazılı rehber ve kendi metot sürümünle karşılaştır.',
              ),
              if (i.audioNotes.isEmpty)
                const Text('Bu rehbere bağlı ses kaydı bulunmuyor.'),
              _AudioNotesBlock(notes: i.audioNotes),
              const SizedBox(height: 20),
              const Text(
                'Konu görselleri',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 12),
              if (i.visualNotes.isEmpty)
                const Text('Düzenek çizimi “Treni kur” bölümündedir.'),
              _VisualNotesBlock(notes: i.visualNotes),
            ],
            if (key == 'sources') ...[
              if ((g['sourceScope'] as String? ?? '').isNotEmpty)
                _InfoBlock(
                  title: 'Kaynak kapsamı',
                  body: g['sourceScope'] as String,
                ),
              const _InfoBlock(
                title: 'Etiketler nasıl okunur?',
                body: 'Metot şartı: açık kaynakta doğrulanan koşul. Saha uygulaması: işlemin sırası ve gerekçesi. Prensip şeması: kesin miktar yerine onaylı konfigürasyona işaret eden çizim.',
              ),
              for (final s in maps(g['sources']))
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          s['title'] as String,
                          style: const TextStyle(fontWeight: FontWeight.w800),
                        ),
                        const SizedBox(height: 8),
                        SelectableText(
                          s['url'] as String,
                          style: const TextStyle(fontSize: 13),
                        ),
                        TextButton.icon(
                          onPressed: () {
                            Clipboard.setData(
                              ClipboardData(text: s['url'] as String),
                            );
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Kaynak bağlantısı kopyalandı.'),
                              ),
                            );
                          },
                          icon: const Icon(Icons.copy, size: 16),
                          label: const Text('Bağlantıyı kopyala'),
                        ),
                      ],
                    ),
                  ),
                ),
              const Text(
                'Gözden geçirme: 12 Ekim 2026. Rehber tam standardın yerine geçmez; sürüm, izin ve laboratuvar prosedürü birlikte uygulanır.',
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class StepCard extends StatelessWidget {
  const StepCard({super.key, required this.number, required this.point});
  final int number;
  final Map<String, dynamic> point;
  @override
  Widget build(BuildContext context) => Card(
    margin: const EdgeInsets.only(bottom: 12),
    elevation: 0,
    child: Padding(
      padding: const EdgeInsets.all(18),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CircleAvatar(
            radius: 17,
            backgroundColor: teal,
            foregroundColor: Colors.white,
            child: Text(
              '$number',
              style: const TextStyle(fontWeight: FontWeight.w800),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  point['title'] as String,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 8),
                if ((point['text'] as String).isNotEmpty)
                  Text(point['text'] as String),
                const SizedBox(height: 10),
                _MiniChip(label: point['kind'] as String),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}

class TrainCard extends StatelessWidget {
  const TrainCard({super.key, required this.train});
  final Map<String, dynamic> train;
  VisualNote get note => VisualNote(
    title: train['title'] as String,
    caption: train['note'] as String,
    imageAsset: train['imageAsset'] as String,
    imageBase64: '',
    placement: 'setup',
  );
  @override
  Widget build(BuildContext context) => Card(
    margin: const EdgeInsets.only(bottom: 18),
    elevation: 0,
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            train['title'] as String,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 10),
          Align(
            alignment: Alignment.centerLeft,
            child: _MiniChip(
              label: train['verified'] == true
                  ? 'Kaynak metniyle doğrulanan sıra'
                  : 'Prensip / işlev şeması',
            ),
          ),
          const SizedBox(height: 12),
          _VisualImage(note: note),
          TextButton.icon(
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute<void>(
                builder: (_) => ImageViewerPage(note: note),
              ),
            ),
            icon: const Icon(Icons.zoom_in),
            label: const Text('Tam ekran aç ve yakınlaştır'),
          ),
          Text(train['note'] as String),
          const SizedBox(height: 14),
          const Text(
            'Bileşenler · gaz / işlem sırasıyla',
            style: TextStyle(fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 10),
          for (final e in maps(train['nodes']).indexed)
            Padding(
              padding: const EdgeInsets.only(bottom: 14),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(
                    width: 30,
                    child: Text(
                      '${e.$1 + 1}.',
                      style: const TextStyle(
                        fontWeight: FontWeight.w800,
                        color: teal,
                      ),
                    ),
                  ),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          e.$2['label'] as String,
                          style: const TextStyle(fontWeight: FontWeight.w800),
                        ),
                        if ((e.$2['value'] as String).isNotEmpty)
                          Text(e.$2['value'] as String),
                        if ((e.$2['role'] as String).isNotEmpty)
                          Text(
                            e.$2['role'] as String,
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                        if ((e.$2['zone'] as String).isNotEmpty)
                          Text(
                            e.$2['zone'] as String,
                            style: const TextStyle(fontSize: 12, color: teal),
                          ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          Text(
            'Kaynak: ${train['source']}',
            style: Theme.of(context).textTheme.bodySmall,
          ),
        ],
      ),
    ),
  );
}

class ChecklistPage extends StatelessWidget {
  const ChecklistPage({super.key, required this.item});
  final StandardItem item;
  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: preferences,
    builder: (context, _) {
      final selected = preferences.checks[item.code] ?? <String>{};
      final total = [
        'preparation',
        'setup',
        'sampling',
        'recovery',
        'checks',
      ].fold<int>(0, (n, k) => n + maps(item.guide[k]).length);
      return Scaffold(
        appBar: AppBar(title: const Text('Saha kontrol listesi')),
        body: SafeArea(
          child: ListView(
            padding: const EdgeInsets.all(20),
            children: [
              Text(
                item.title,
                style: const TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                '${selected.length} / $total adım işaretli · kişisel kontrol',
              ),
              const SizedBox(height: 10),
              LinearProgressIndicator(
                value: total == 0 ? 0 : selected.length / total,
              ),
              const SizedBox(height: 12),
              const Text(
                'İşaretler cihazında saklanır. Her yeni ölçümde listeyi sıfırla. Liste teknik uygunluğu otomatik hesaplamaz.',
              ),
              TextButton.icon(
                onPressed: () => preferences.reset(item.code),
                icon: const Icon(Icons.restart_alt),
                label: const Text('Yeni ölçüm · işaretleri sıfırla'),
              ),
              for (final key in [
                'preparation',
                'setup',
                'sampling',
                'recovery',
                'checks',
              ]) ...[
                Padding(
                  padding: const EdgeInsets.only(top: 18, bottom: 8),
                  child: Text(
                    stages[stageKeys.indexOf(key)],
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
                for (final e in maps(item.guide[key]).indexed)
                  Card(
                    child: CheckboxListTile(
                      controlAffinity: ListTileControlAffinity.leading,
                      value: selected.contains('$key:${e.$1}'),
                      onChanged: (v) => preferences.mark(
                        item.code,
                        '$key:${e.$1}',
                        v ?? false,
                      ),
                      title: Text(e.$2['title'] as String),
                      subtitle: Text(e.$2['text'] as String),
                    ),
                  ),
              ],
            ],
          ),
        ),
      );
    },
  );
}

class SharedAudio extends ChangeNotifier {
  SharedAudio._();
  static final instance = SharedAudio._();
  AudioPlayer? _player;
  String? asset;
  bool loading = false;
  late final _prefs = SharedPreferencesAsync();
  int position = 0;
  AudioPlayer get player {
    if (_player == null) {
      _player = AudioPlayer();
      _player!.playerStateStream.listen((_) => notifyListeners());
      _player!.positionStream.listen((p) => position = p.inMilliseconds);
      Timer.periodic(const Duration(seconds: 5), (_) {
        unawaited(save());
      });
    }
    return _player!;
  }

  void refresh() => notifyListeners();
  Future<void> save() async {
    final a = asset;
    if (a != null && !preferences.memoryOnly)
      await _prefs.setInt('audio:$a', position);
  }

  Future<void> toggle(AudioNote note) async {
    if (loading) return;
    if (asset != note.audioAsset) {
      await save();
      await player.pause();
      asset = note.audioAsset;
      loading = true;
      notifyListeners();
      try {
        await player.setAudioSource(
          AudioSource.asset(
            note.audioAsset,
            tag: MediaItem(
              id: note.audioAsset,
              title: note.title,
              album: 'Emisyon İmisyon · Saha Eğitimi',
            ),
          ),
        );
        final old = preferences.memoryOnly
            ? 0
            : await _prefs.getInt('audio:${note.audioAsset}') ?? 0;
        final end = player.duration?.inMilliseconds ?? 0;
        await player.seek(
          Duration(
            milliseconds: end > 0 && old >= end - 1000 ? 0 : max(0, old),
          ),
        );
      } catch (_) {
        asset = null;
        rethrow;
      } finally {
        loading = false;
        notifyListeners();
      }
    }
    if (player.playing) {
      await player.pause();
      await save();
    } else {
      if (player.processingState == ProcessingState.completed)
        await player.seek(Duration.zero);
      unawaited(player.play());
    }
    notifyListeners();
  }
}

class _AudioNotesBlock extends StatelessWidget {
  const _AudioNotesBlock({required this.notes});

  final List<AudioNote> notes;

  @override
  Widget build(BuildContext context) {
    if (notes.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [for (final note in notes) _AudioCard(note: note)],
    );
  }
}

class _AudioCard extends StatefulWidget {
  const _AudioCard({required this.note});

  final AudioNote note;

  @override
  State<_AudioCard> createState() => _AudioCardState();
}

class _AudioCardState extends State<_AudioCard> {
  final SharedAudio _shared = SharedAudio.instance;
  AudioPlayer get _player => _shared.player;
  bool get _loading =>
      _shared.loading && _shared.asset == widget.note.audioAsset;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _shared.addListener(_changed);
  }

  void _changed() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    _shared.removeListener(_changed);
    super.dispose();
  }

  Future<void> _toggle() async {
    if (_shared.loading) return;
    setState(() => _errorMessage = null);
    try {
      await _shared.toggle(widget.note);
    } catch (_) {
      if (mounted)
        setState(
          () => _errorMessage = 'Ses açılamadı. Yeniden deneyebilirsin.',
        );
    }
  }

  Future<void> _seekRelative(int seconds) async {
    if (_errorMessage != null || _loading) return;
    final duration = _player.duration ?? Duration.zero;
    final current = _player.position;
    final targetMs = (current.inMilliseconds + seconds * 1000).clamp(
      0,
      duration.inMilliseconds == 0
          ? current.inMilliseconds + seconds * 1000
          : duration.inMilliseconds,
    );
    await _player.seek(Duration(milliseconds: targetMs));
  }

  Future<void> _seekTo(double seconds) async {
    if (_errorMessage != null || _loading) return;
    await _player.seek(Duration(milliseconds: (seconds * 1000).round()));
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return Card(
      elevation: 0,
      color: colorScheme.primaryContainer.withAlpha(150),
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.headphones, color: colorScheme.primary),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'Sesli Saha Anlatımı',
                    style: Theme.of(context).textTheme.titleMedium
                        ?.copyWith(fontWeight: FontWeight.w800),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              widget.note.title,
              style: Theme.of(context).textTheme.titleSmall
                  ?.copyWith(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 4),
            Text(
              'Mevcut eğitim kaydı · çevrimdışı · ekran kilitliyken çalabilir.',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            if (_loading) ...[
              const SizedBox(height: 12),
              const LinearProgressIndicator(),
            ] else if (_errorMessage != null) ...[
              const SizedBox(height: 12),
              Text(_errorMessage!, style: TextStyle(color: colorScheme.error)),
              TextButton(onPressed: _toggle, child: const Text("Yeniden dene")),
            ] else if (_shared.asset != widget.note.audioAsset) ...[
              const SizedBox(height: 10),
              FilledButton.icon(
                onPressed: _toggle,
                icon: const Icon(Icons.play_arrow),
                label: const Text("Kaydı aç / kaldığın yerden devam et"),
              ),
            ] else ...[
              const SizedBox(height: 10),
              StreamBuilder<Duration?>(
                stream: _player.durationStream,
                builder: (context, durationSnapshot) {
                  final duration =
                      durationSnapshot.data ??
                      _player.duration ??
                      Duration.zero;
                  return StreamBuilder<Duration>(
                    stream: _player.positionStream,
                    builder: (context, positionSnapshot) {
                      final rawPosition =
                          positionSnapshot.data ?? _player.position;
                      final position = duration == Duration.zero
                          ? rawPosition
                          : Duration(
                              milliseconds: min(
                                rawPosition.inMilliseconds,
                                duration.inMilliseconds,
                              ),
                            );
                      final maxSeconds = max(1, duration.inSeconds).toDouble();
                      final valueSeconds = min(
                        position.inSeconds.toDouble(),
                        maxSeconds,
                      );
                      return Column(
                        children: [
                          Slider(
                            value: valueSeconds,
                            min: 0,
                            max: maxSeconds,
                            onChanged: (value) => _seekTo(value),
                          ),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                _formatDuration(position),
                                style: Theme.of(context).textTheme.bodySmall,
                              ),
                              Text(
                                _formatDuration(duration),
                                style: Theme.of(context).textTheme.bodySmall,
                              ),
                            ],
                          ),
                        ],
                      );
                    },
                  );
                },
              ),
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: [.75, 1.0, 1.25, 1.5, 2.0]
                    .map(
                      (v) => ChoiceChip(
                        label: Text('${v}×'),
                        selected: _player.speed == v,
                        onSelected: (_) async {
                          await _player.setSpeed(v);
                          _shared.refresh();
                        },
                      ),
                    )
                    .toList(),
              ),
              TextButton(
                onPressed: () async {
                  await _player.seek(Duration.zero);
                  await _shared.save();
                },
                child: const Text('Baştan başlat'),
              ),
              const SizedBox(height: 6),
              StreamBuilder<PlayerState>(
                stream: _player.playerStateStream,
                builder: (context, snapshot) {
                  final playing = _player.playing;
                  final completed =
                      _player.processingState == ProcessingState.completed;
                  return Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton.filledTonal(
                        onPressed: () => _seekRelative(-10),
                        icon: const Icon(Icons.replay_10),
                      ),
                      const SizedBox(width: 12),
                      IconButton.filled(
                        iconSize: 34,
                        onPressed: _toggle,
                        icon: Icon(
                          playing && !completed
                              ? Icons.pause
                              : Icons.play_arrow,
                        ),
                      ),
                      const SizedBox(width: 12),
                      IconButton.filledTonal(
                        onPressed: () => _seekRelative(10),
                        icon: const Icon(Icons.forward_10),
                      ),
                    ],
                  );
                },
              ),
            ],
          ],
        ),
      ),
    );
  }

  String _formatDuration(Duration duration) {
    final hours = duration.inHours;
    final minutes = duration.inMinutes.remainder(60).toString().padLeft(2, '0');
    final seconds = duration.inSeconds.remainder(60).toString().padLeft(2, '0');
    if (hours > 0) return '$hours:$minutes:$seconds';
    return '$minutes:$seconds';
  }
}

class _VisualNotesBlock extends StatelessWidget {
  const _VisualNotesBlock({required this.notes});

  final List<VisualNote> notes;

  @override
  Widget build(BuildContext context) {
    if (notes.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        for (final note in notes)
          Card(
            elevation: 0,
            color: Theme.of(context).colorScheme.tertiaryContainer
                .withAlpha(120),
            margin: const EdgeInsets.only(bottom: 12),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        Icons.image_search,
                        size: 18,
                        color: Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          note.title,
                          style: Theme.of(context).textTheme.titleSmall
                              ?.copyWith(fontWeight: FontWeight.w800),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  _VisualImage(note: note),
                  const SizedBox(height: 8),
                  Text(TurkishUnitText.normalize(note.caption)),
                  const SizedBox(height: 4),
                  Text(
                    'Görseli büyütmek için dokun veya çift dokun.',
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
          ),
      ],
    );
  }
}

class _VisualImage extends StatelessWidget {
  const _VisualImage({required this.note});

  final VisualNote note;

  @override
  Widget build(BuildContext context) {
    final imageWidget = _buildImage(context);
    return GestureDetector(
      onTap: () => _open(context),
      onDoubleTap: () => _open(context),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(12),
        child: imageWidget,
      ),
    );
  }

  Widget _buildImage(BuildContext context) {
    if (note.imageAsset.trim().isNotEmpty) {
      return Image.asset(
        note.imageAsset,
        fit: BoxFit.contain,
        width: double.infinity,
        errorBuilder: (context, error, stackTrace) =>
            _MissingVisualBox(path: note.imageAsset),
      );
    }
    if (note.imageBase64.trim().isNotEmpty) {
      final bytes = _tryDecodeBase64(note.imageBase64);
      if (bytes != null)
        return Image.memory(bytes, fit: BoxFit.contain, width: double.infinity);
    }
    return const _MissingVisualBox(path: 'Görsel verisi yok');
  }

  void _open(BuildContext context) =>
      Navigator.of(context)
          .push(MaterialPageRoute(builder: (_) => ImageViewerPage(note: note)));

  Uint8List? _tryDecodeBase64(String value) {
    try {
      return base64Decode(value);
    } catch (_) {
      return null;
    }
  }
}

class ImageViewerPage extends StatelessWidget {
  const ImageViewerPage({super.key, required this.note});

  final VisualNote note;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        title: Text(note.title, maxLines: 1, overflow: TextOverflow.ellipsis),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: InteractiveViewer(
                minScale: 0.8,
                maxScale: 6,
                child: Center(child: _viewerImage()),
              ),
            ),
            ConstrainedBox(
              constraints: const BoxConstraints(maxHeight: 130),
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(12),
                child: Text(
                  TurkishUnitText.normalize(note.caption),
                  style: const TextStyle(color: Colors.white70),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _viewerImage() {
    if (note.imageAsset.trim().isNotEmpty)
      return Image.asset(note.imageAsset, fit: BoxFit.contain);
    if (note.imageBase64.trim().isNotEmpty) {
      try {
        return Image.memory(
          base64Decode(note.imageBase64),
          fit: BoxFit.contain,
        );
      } catch (_) {
        return const Text(
          'Görsel açılamadı.',
          style: TextStyle(color: Colors.white),
        );
      }
    }
    return const Text('Görsel yok.', style: TextStyle(color: Colors.white));
  }
}

class _MissingVisualBox extends StatelessWidget {
  const _MissingVisualBox({required this.path});

  final String path;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        color: Theme.of(context).colorScheme.errorContainer,
      ),
      child: Text(
        'Görsel APK içinde bulunamadı. Dosya yolu: $path',
        style: Theme.of(context).textTheme.bodySmall,
      ),
    );
  }
}

class _InfoBlock extends StatelessWidget {
  const _InfoBlock({required this.title, required this.body});

  final String title;
  final String body;

  @override
  Widget build(BuildContext context) {
    final displayBody = TurkishUnitText.normalize(body);
    if (displayBody.trim().isEmpty) return const SizedBox.shrink();
    return Card(
      elevation: 0,
      color: Theme.of(context).colorScheme.surfaceContainerHighest,
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: Theme.of(context).textTheme.titleMedium
                  ?.copyWith(fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 8),
            Text(displayBody),
          ],
        ),
      ),
    );
  }
}

class _MiniChip extends StatelessWidget {
  const _MiniChip({required this.label});

  final String label;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 5),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.primaryContainer,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        TurkishUnitText.normalize(label),
        style: Theme.of(context).textTheme.labelSmall,
      ),
    );
  }
}

class StandardsRepository {
  static const _standardAssetFiles = <String>['assets/field_guides.json'];
  static const _educationAssetFiles = <String>[
    'assets/education_notes.json',
    'assets/education_notes_extra.json',
  ];
  static const _visualAssetFiles = <String>[
    'assets/visual_notes.json',
    'assets/visual_notes_extra.json',
  ];
  static const _audioAssetFile = 'assets/standard_audio.json';

  static Future<List<StandardItem>> loadItems() async {
    final decoded = <Map<String, dynamic>>[];
    for (final path in _standardAssetFiles) {
      final list = await _loadListAsset(path);
      for (final item in list) {
        if (item is Map<String, dynamic>) decoded.add(item);
      }
    }

    final notesByKey = <String, List<String>>{};
    final visualsByKey = await _loadVisualNotes();
    final audioByKey = await _loadAudioNotes();
    final itemByKey = <String, Map<String, dynamic>>{};
    final codeToKey = <String, String>{};
    final titleToKey = <String, String>{};

    for (final json in decoded) {
      final code = json['code'] as String? ?? '';
      final title = json['title'] as String? ?? '';
      final codeKey = TurkishUnitText.key(code);
      final titleKey = TurkishUnitText.key(title);
      var key = '';
      if (codeKey.isNotEmpty && codeToKey.containsKey(codeKey)) {
        key = codeToKey[codeKey]!;
      } else if (titleKey.isNotEmpty && titleToKey.containsKey(titleKey)) {
        key = titleToKey[titleKey]!;
      } else {
        key = codeKey.isNotEmpty ? codeKey : titleKey;
      }
      if (key.isEmpty) continue;
      itemByKey[key] = json;
      if (codeKey.isNotEmpty) codeToKey[codeKey] = key;
      if (titleKey.isNotEmpty) titleToKey[titleKey] = key;
    }

    final items = <StandardItem>[];
    for (final json in itemByKey.values) {
      final code = json['code'] as String? ?? '';
      final title = json['title'] as String? ?? '';
      final keys = <String>{
        TurkishUnitText.key(code),
        TurkishUnitText.key(title),
        ...StandardItem.listFromDynamic(json['aliases'])
            .map(TurkishUnitText.key),
      };
      final notes = _collectStrings(notesByKey, keys);
      final visuals = _collectVisuals(visualsByKey, keys);
      final audioNotes = _collectAudio(audioByKey, keys);
      items.add(
        StandardItem.fromJson(
          json,
          educationNotes: notes,
          visualNotes: visuals,
          audioNotes: audioNotes,
        ),
      );
    }

    items.sort((a, b) => a.title.compareTo(b.title));
    return items;
  }

  static List<String> _collectStrings(
    Map<String, List<String>> index,
    Set<String> keys,
  ) {
    final result = <String>[];
    for (final key in keys) {
      if (key.isEmpty) continue;
      result.addAll(index[key] ?? const <String>[]);
    }
    return result;
  }

  static List<VisualNote> _collectVisuals(
    Map<String, List<VisualNote>> index,
    Set<String> keys,
  ) {
    final result = <VisualNote>[];
    final seen = <String>{};
    for (final key in keys) {
      if (key.isEmpty) continue;
      for (final note in index[key] ?? const <VisualNote>[]) {
        final noteKey = note.imageAsset.isNotEmpty
            ? note.imageAsset
            : '${note.title}|${note.imageBase64.hashCode}';
        if (seen.add(noteKey)) result.add(note);
      }
    }
    return result;
  }

  static List<AudioNote> _collectAudio(
    Map<String, List<AudioNote>> index,
    Set<String> keys,
  ) {
    final result = <AudioNote>[];
    final seen = <String>{};
    for (final key in keys) {
      if (key.isEmpty) continue;
      for (final note in index[key] ?? const <AudioNote>[]) {
        if (seen.add(note.audioAsset)) result.add(note);
      }
    }
    result.sort((a, b) => a.sortOrder.compareTo(b.sortOrder));
    return result;
  }

  static Future<List<dynamic>> _loadListAsset(String path) async {
    try {
      final raw = await rootBundle.loadString(path);
      final decoded = jsonDecode(raw);
      if (decoded is List<dynamic>) return decoded;
    } catch (_) {}
    return const <dynamic>[];
  }

  static Future<Map<String, dynamic>> _loadMapAsset(String path) async {
    try {
      final raw = await rootBundle.loadString(path);
      final decoded = jsonDecode(raw);
      if (decoded is Map<String, dynamic>) return decoded;
    } catch (_) {}
    return const <String, dynamic>{};
  }

  static Future<Map<String, List<VisualNote>>> _loadVisualNotes() async {
    final result = <String, List<VisualNote>>{};
    for (final path in _visualAssetFiles) {
      final decoded = await _loadListAsset(path);
      for (final entry in decoded) {
        if (entry is! Map<String, dynamic>) continue;
        final standards = StandardItem.listFromDynamic(entry['standards']);
        final note = VisualNote.fromJson(entry);
        for (final standard in standards) {
          final key = TurkishUnitText.key(standard);
          if (key.isEmpty) continue;
          result.putIfAbsent(key, () => <VisualNote>[]).add(note);
        }
      }
    }
    return result;
  }

  static Future<Map<String, List<AudioNote>>> _loadAudioNotes() async {
    final result = <String, List<AudioNote>>{};
    final decoded = await _loadListAsset(_audioAssetFile);
    for (final entry in decoded) {
      if (entry is! Map<String, dynamic>) continue;
      final standards = StandardItem.listFromDynamic(entry['standards']);
      final note = AudioNote.fromJson(entry);
      if (note.audioAsset.trim().isEmpty) continue;
      for (final standard in standards) {
        final key = TurkishUnitText.key(standard);
        if (key.isEmpty) continue;
        result.putIfAbsent(key, () => <AudioNote>[]).add(note);
      }
    }
    for (final notes in result.values) {
      notes.sort((a, b) => a.sortOrder.compareTo(b.sortOrder));
    }
    return result;
  }
}

class StandardItem {
  const StandardItem({
    required this.title,
    required this.code,
    required this.category,
    required this.subgroup,
    required this.keywords,
    required this.purpose,
    required this.duration,
    required this.flowRate,
    required this.equipment,
    required this.reagents,
    required this.fieldSteps,
    required this.criticalControls,
    required this.acceptance,
    required this.reporting,
    required this.mistakes,
    required this.educationNotes,
    required this.visualNotes,
    required this.audioNotes,
    this.guide = const {},
  });

  final String title;
  final String code;
  final String category;
  final String subgroup;
  final List<String> keywords;
  final String purpose;
  final String duration;
  final String flowRate;
  final List<String> equipment;
  final List<String> reagents;
  final List<String> fieldSteps;
  final List<String> criticalControls;
  final List<String> acceptance;
  final List<String> reporting;
  final List<String> mistakes;
  final List<String> educationNotes;
  final List<VisualNote> visualNotes;
  final List<AudioNote> audioNotes;
  final Map<String, dynamic> guide;

  String get searchText => TurkishUnitText.normalize(
    [
      title,
      code,
      category,
      subgroup,
      purpose,
      duration,
      flowRate,
      ...keywords,
      ...listFromDynamic(guide['aliases']),
      guide['method'] as String? ?? '',
      jsonEncode(guide['concepts']),
      jsonEncode(guide['sampling']),
      ...equipment,
      ...reagents,
      ...fieldSteps,
      ...criticalControls,
      ...acceptance,
      ...reporting,
      ...mistakes,
      ...educationNotes,
      ...visualNotes.map((note) => '${note.title} ${note.caption}'),
      ...audioNotes.map((note) => '${note.title} ${note.audioAsset}'),
    ].join(' '),
  ).toLowerCase();

  factory StandardItem.fromJson(
    Map<String, dynamic> json, {
    List<String> educationNotes = const <String>[],
    List<VisualNote> visualNotes = const <VisualNote>[],
    List<AudioNote> audioNotes = const <AudioNote>[],
  }) {
    return StandardItem(
      title: json['title'] as String? ?? '',
      code: json['code'] as String? ?? '',
      category: json['category'] as String? ?? '',
      subgroup: json['group'] as String? ?? '',
      keywords: listFromDynamic(json['keywords']),
      purpose: json['purpose'] as String? ?? '',
      duration: json['duration'] as String? ?? '',
      flowRate: json['flowRate'] as String? ?? '',
      equipment: listFromDynamic(json['equipment']),
      reagents: listFromDynamic(json['reagents']),
      fieldSteps: listFromDynamic(json['fieldSteps']),
      criticalControls: listFromDynamic(json['criticalControls']),
      acceptance: listFromDynamic(json['acceptance']),
      reporting: listFromDynamic(json['reporting']),
      mistakes: listFromDynamic(json['mistakes']),
      educationNotes: educationNotes,
      visualNotes: visualNotes,
      audioNotes: audioNotes,
      guide: json,
    );
  }

  static List<String> listFromDynamic(dynamic value) {
    if (value is! List) return const <String>[];
    return value.map((item) => item.toString()).toList();
  }
}

class VisualNote {
  const VisualNote({
    required this.title,
    required this.caption,
    required this.imageBase64,
    required this.imageAsset,
    required this.placement,
  });

  final String title;
  final String caption;
  final String imageBase64;
  final String imageAsset;
  final String placement;

  factory VisualNote.fromJson(Map<String, dynamic> json) {
    return VisualNote(
      title: json['title'] as String? ?? '',
      caption: json['caption'] as String? ?? '',
      imageBase64: json['imageBase64'] as String? ?? '',
      imageAsset: json['imageAsset'] as String? ?? '',
      placement: json['placement'] as String? ?? 'general',
    );
  }
}

class AudioNote {
  const AudioNote({
    required this.title,
    required this.audioAsset,
    required this.sortOrder,
  });

  final String title;
  final String audioAsset;
  final int sortOrder;

  factory AudioNote.fromJson(Map<String, dynamic> json) {
    final rawSort = json['sortOrder'];
    return AudioNote(
      title: json['title'] as String? ?? 'Sesli Saha Anlatımı',
      audioAsset: json['audioAsset'] as String? ?? '',
      sortOrder: rawSort is int
          ? rawSort
          : int.tryParse(rawSort?.toString() ?? '') ?? 999,
    );
  }
}

class TurkishUnitText {
  const TurkishUnitText._();
  static String key(String input) => searchKey(input);
  static String normalize(String input) => input
      .replaceAll(RegExp(r'\bm3\b', caseSensitive: false), 'm³')
      .replaceAll(RegExp(r'\bm2\b', caseSensitive: false), 'm²');
}
