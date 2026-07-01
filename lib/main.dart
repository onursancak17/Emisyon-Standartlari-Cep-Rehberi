import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(const StandardsApp());
}

class StandardsApp extends StatelessWidget {
  const StandardsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Emisyon İmisyon Ölçüm Standartları',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF145DA0)),
        useMaterial3: true,
      ),
      home: const StandardsHomePage(),
    );
  }
}

class StandardsHomePage extends StatefulWidget {
  const StandardsHomePage({super.key});

  @override
  State<StandardsHomePage> createState() => _StandardsHomePageState();
}

class _StandardsHomePageState extends State<StandardsHomePage> {
  late final Future<List<StandardItem>> _itemsFuture;
  final TextEditingController _searchController = TextEditingController();
  String _query = '';
  String _selectedCategory = 'Tümü';

  @override
  void initState() {
    super.initState();
    _itemsFuture = StandardsRepository.loadItems();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  List<String> _categories(List<StandardItem> items) {
    final categories = <String>{'Tümü'};
    for (final item in items) {
      categories.add(item.category);
    }
    return categories.toList();
  }

  List<StandardItem> _filter(List<StandardItem> items) {
    final normalizedQuery = TurkishUnitText.normalize(_query).toLowerCase().trim();
    return items.where((item) {
      final categoryMatches = _selectedCategory == 'Tümü' || item.category == _selectedCategory;
      if (!categoryMatches) return false;
      if (normalizedQuery.isEmpty) return true;
      return item.searchText.contains(normalizedQuery);
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Emisyon İmisyon Ölçüm Standartları'), centerTitle: false),
      body: SafeArea(
        child: FutureBuilder<List<StandardItem>>(
          future: _itemsFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
            if (snapshot.hasError) {
              return Center(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Text('Standart verisi okunamadı: ${snapshot.error}'),
                ),
              );
            }

            final items = snapshot.data ?? const <StandardItem>[];
            final categories = _categories(items);
            final filteredItems = _filter(items);

            return Column(
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                  child: TextField(
                    controller: _searchController,
                    decoration: InputDecoration(
                      prefixIcon: const Icon(Icons.search),
                      labelText: 'Standart, kirletici, çözelti veya cihaz ara',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(16)),
                      suffixIcon: _query.isEmpty
                          ? null
                          : IconButton(
                              onPressed: () {
                                _searchController.clear();
                                setState(() => _query = '');
                              },
                              icon: const Icon(Icons.clear),
                            ),
                    ),
                    onChanged: (value) => setState(() => _query = value),
                  ),
                ),
                SizedBox(
                  height: 52,
                  child: ListView.separated(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    scrollDirection: Axis.horizontal,
                    itemCount: categories.length,
                    separatorBuilder: (_, __) => const SizedBox(width: 8),
                    itemBuilder: (context, index) {
                      final category = categories[index];
                      return ChoiceChip(
                        label: Text(category),
                        selected: _selectedCategory == category,
                        onSelected: (_) => setState(() => _selectedCategory = category),
                      );
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 2, 16, 8),
                  child: Row(
                    children: [
                      Icon(Icons.offline_bolt, size: 18, color: Theme.of(context).colorScheme.primary),
                      const SizedBox(width: 6),
                      Expanded(child: Text('Tamamen offline • Sahacı odaklı profesyonel standart rehberi', style: Theme.of(context).textTheme.bodySmall)),
                      Text('${filteredItems.length} kayıt'),
                    ],
                  ),
                ),
                Expanded(
                  child: filteredItems.isEmpty
                      ? const Center(child: Text('Sonuç bulunamadı.'))
                      : ListView.separated(
                          padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                          itemCount: filteredItems.length,
                          separatorBuilder: (_, __) => const SizedBox(height: 10),
                          itemBuilder: (context, index) => StandardCard(item: filteredItems[index]),
                        ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}

class StandardCard extends StatelessWidget {
  const StandardCard({super.key, required this.item});

  final StandardItem item;

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 1,
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => StandardDetailPage(item: item))),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(child: Text(item.title, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800))),
                  const SizedBox(width: 8),
                  const Icon(Icons.chevron_right),
                ],
              ),
              const SizedBox(height: 6),
              Wrap(spacing: 6, runSpacing: 6, children: [_MiniChip(label: item.code), _MiniChip(label: item.category), _MiniChip(label: item.subgroup)]),
              const SizedBox(height: 10),
              Text(TurkishUnitText.normalize(item.purpose), maxLines: 3, overflow: TextOverflow.ellipsis),
              if (item.visualNotes.isNotEmpty || item.educationNotes.isNotEmpty) ...[
                const SizedBox(height: 8),
                Row(
                  children: [
                    Icon(Icons.school, size: 16, color: Theme.of(context).colorScheme.primary),
                    const SizedBox(width: 5),
                    Expanded(child: Text('${item.educationNotes.length} eğitim notu • ${item.visualNotes.length} seçilmiş görsel', style: Theme.of(context).textTheme.labelMedium)),
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class StandardDetailPage extends StatelessWidget {
  const StandardDetailPage({super.key, required this.item});

  final StandardItem item;

  List<VisualNote> _notes(String placement) => item.visualNotes.where((note) => note.placement == placement).toList();

  List<VisualNote> get _unplacedNotes {
    const known = <String>{'purpose', 'quality', 'flowRate', 'equipment', 'fieldSteps', 'criticalControls', 'acceptance', 'reporting'};
    return item.visualNotes.where((note) => !known.contains(note.placement)).toList();
  }

  @override
  Widget build(BuildContext context) {
    final purposeNotes = [..._notes('purpose'), ..._notes('quality')];
    final labels = DetailSectionLabels.forItem(item);
    return Scaffold(
      appBar: AppBar(title: Text(item.code)),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 24),
        children: [
          Text(item.title, style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w800)),
          const SizedBox(height: 8),
          Wrap(spacing: 8, runSpacing: 8, children: [_MiniChip(label: item.category), _MiniChip(label: item.subgroup), _MiniChip(label: item.code)]),
          const SizedBox(height: 16),
          const _UnitInfoBlock(),
          _InfoBlock(title: labels.purposeTitle, body: item.purpose),
          _VisualNotesBlock(notes: purposeNotes),
          _InfoBlock(title: labels.durationTitle, body: item.duration),
          _InfoBlock(title: labels.flowRateTitle, body: item.flowRate),
          _VisualNotesBlock(notes: _notes('flowRate')),
          _InfoBlock(title: labels.equipmentTitle, body: item.equipment.join('\n')),
          _VisualNotesBlock(notes: _notes('equipment')),
          _InfoBlock(title: labels.reagentsTitle, body: item.reagents.join('\n')),
          _InfoBlock(title: labels.fieldStepsTitle, body: _numbered(item.fieldSteps)),
          _VisualNotesBlock(notes: _notes('fieldSteps')),
          _InfoBlock(title: labels.criticalControlsTitle, body: item.criticalControls.join('\n')),
          _VisualNotesBlock(notes: _notes('criticalControls')),
          _InfoBlock(title: labels.acceptanceTitle, body: item.acceptance.join('\n')),
          _VisualNotesBlock(notes: _notes('acceptance')),
          _InfoBlock(title: labels.reportingTitle, body: item.reporting.join('\n')),
          _VisualNotesBlock(notes: _notes('reporting')),
          _InfoBlock(title: labels.educationTitle, body: _numbered(item.educationNotes)),
          _VisualNotesBlock(notes: _unplacedNotes),
          _InfoBlock(title: labels.mistakesTitle, body: item.mistakes.join('\n')),
          const SizedBox(height: 12),
          Text('Not: Bu uygulama sahacı hızlı rehberi olarak hazırlanmıştır. Resmi raporlamada yürürlükteki standart, mevzuat ve laboratuvar talimatı esas alınmalıdır.', style: Theme.of(context).textTheme.bodySmall),
        ],
      ),
    );
  }

  String _numbered(List<String> values) => values.asMap().entries.map((entry) => '${entry.key + 1}. ${entry.value}').join('\n');
}

class DetailSectionLabels {
  const DetailSectionLabels({
    this.purposeTitle = 'Amaç / kullanım alanı',
    this.durationTitle = 'Ölçüm süresi',
    this.flowRateTitle = 'Debi / hacim notu',
    this.equipmentTitle = 'Cihaz / ekipman',
    this.reagentsTitle = 'Çözelti / absorban / impinger',
    this.fieldStepsTitle = 'Saha adımları',
    this.criticalControlsTitle = 'Kritik teknik kontroller',
    this.acceptanceTitle = 'Kabul / ret kriterleri',
    this.reportingTitle = 'Raporlama notları',
    this.educationTitle = 'Eğitim dokümanı ayrıntıları',
    this.mistakesTitle = 'Sık yapılan saha hataları',
  });

  final String purposeTitle;
  final String durationTitle;
  final String flowRateTitle;
  final String equipmentTitle;
  final String reagentsTitle;
  final String fieldStepsTitle;
  final String criticalControlsTitle;
  final String acceptanceTitle;
  final String reportingTitle;
  final String educationTitle;
  final String mistakesTitle;

  static DetailSectionLabels forItem(StandardItem item) {
    final text = TurkishUnitText.normalize('${item.title} ${item.code} ${item.subgroup}').toLowerCase();
    if (text.contains('çöken toz')) {
      return const DetailSectionLabels(
        purposeTitle: 'Ölçüm mantığı ve kapsam',
        durationTitle: 'Maruziyet süresi',
        flowRateTitle: 'Kap alanı / maruziyet hesabı',
        equipmentTitle: 'Toplama kabı ve saha yerleşim ekipmanı',
        reagentsTitle: 'Kap hazırlığı / koruyucu sıvı',
        fieldStepsTitle: 'Saha yerleşimi ve toplama adımları',
        criticalControlsTitle: 'Saha geçerliliğini bozan durumlar',
        acceptanceTitle: 'Kabul / geçerlilik kontrolü',
        reportingTitle: 'SKHKKY Ek-2 raporlama notları',
        mistakesTitle: 'Çöken tozda sık yapılan hatalar',
      );
    }
    if (text.contains('pasif örnekleme') || text.contains('difüzyon tüp')) {
      return const DetailSectionLabels(
        purposeTitle: 'Pasif örnekleme mantığı ve kapsam',
        durationTitle: 'Maruziyet süresi ve tüp açma-kapama',
        flowRateTitle: 'Difüzyon / alım hızı mantığı',
        equipmentTitle: 'Pasif tüp, shelter ve saha ekipmanı',
        reagentsTitle: 'Tüp adsorbanı / blank düzeni',
        fieldStepsTitle: 'Pasif tüp saha uygulaması',
        criticalControlsTitle: 'Maruziyet ve kirlenme kontrolleri',
        acceptanceTitle: 'Tüp kabul / ret kontrolü',
        reportingTitle: 'Pasif örnekleme raporlama notları',
        mistakesTitle: 'Pasif örneklemede sık yapılan hatalar',
      );
    }
    if (text.contains('15259') || text.contains('method 1') || text.contains('traverse')) {
      return const DetailSectionLabels(
        purposeTitle: 'Ölçüm düzlemi seçiminin amacı',
        durationTitle: 'Ölçüm öncesi planlama süresi',
        flowRateTitle: 'Hız profili / traverse planı notu',
        equipmentTitle: 'Port, platform ve geometri kontrol ekipmanı',
        reagentsTitle: 'Kimyasal kullanılmaz',
        fieldStepsTitle: 'Port seçimi ve nokta yerleşimi adımları',
        criticalControlsTitle: 'Bozucu etki ve akış açısı kontrolleri',
        acceptanceTitle: 'Ölçüm düzlemi uygunluk kriterleri',
        reportingTitle: 'Kroki, port ve nokta raporlama notları',
      );
    }
    if (text.contains('method 29') || text.contains('14385') || text.contains('ağır metal')) {
      return const DetailSectionLabels(
        purposeTitle: 'Metal ölçümünün kapsamı',
        durationTitle: 'İzokinetik süre ve hedef hacim',
        flowRateTitle: 'İzokinetik çekiş / toplam hacim',
        equipmentTitle: 'Metal örnekleme treni ve temiz ekipman',
        reagentsTitle: 'Absorbanlar, impinger dizilimi ve mL bilgileri',
        fieldStepsTitle: 'Örnekleme ve geri kazanım fraksiyonları',
        criticalControlsTitle: 'Kontaminasyon ve blank kontrolleri',
        acceptanceTitle: 'Metal numunesi kabul kriterleri',
        reportingTitle: 'Fraksiyon ve blank raporlama notları',
        mistakesTitle: 'Metal ölçümünde sık yapılan hatalar',
      );
    }
    if (text.contains('1911') || text.contains('26a') || text.contains('hcl') || text.contains('halojen')) {
      return const DetailSectionLabels(
        purposeTitle: 'Asit gazı / halojen ölçüm kapsamı',
        durationTitle: 'Örnekleme süresi ve hedef hacim',
        flowRateTitle: 'Çekiş debisi / absorpsiyon verimi',
        equipmentTitle: 'Prob, filtre ve impinger treni',
        reagentsTitle: 'Absorban çözeltileri ve impinger hacimleri',
        fieldStepsTitle: 'Saha kurulumu ve numune geri kazanımı',
        criticalControlsTitle: 'Breakthrough, karışma ve kaçak kontrolleri',
        acceptanceTitle: 'Asit gazı numunesi kabul kriterleri',
        reportingTitle: 'Fraksiyon ve çözelti raporlama notları',
      );
    }
    if (text.contains('pm10') || text.contains('pm2.5') || text.contains('12341')) {
      return const DetailSectionLabels(
        purposeTitle: 'Ortam havası PM ölçüm kapsamı',
        durationTitle: '24 saatlik örnekleme süresi',
        flowRateTitle: 'Qref / Qamb ve hacim hesabı',
        equipmentTitle: 'PM başlığı, cihaz ve filtre ekipmanı',
        reagentsTitle: 'Filtre / saha blankı',
        fieldStepsTitle: 'Cihaz kurulumu ve filtre yönetimi',
        criticalControlsTitle: 'Debi, filtre ve saha şartı kontrolleri',
        acceptanceTitle: 'PM10/PM2.5 kabul kriterleri',
        reportingTitle: 'Hacim, debi ve filtre raporlama notları',
      );
    }
    return const DetailSectionLabels();
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
            color: Theme.of(context).colorScheme.tertiaryContainer.withAlpha(120),
            margin: const EdgeInsets.only(bottom: 12),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.image_search, size: 18, color: Theme.of(context).colorScheme.primary),
                      const SizedBox(width: 6),
                      Expanded(child: Text(note.title, style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w800))),
                    ],
                  ),
                  const SizedBox(height: 10),
                  _VisualImage(note: note),
                  const SizedBox(height: 8),
                  Text(TurkishUnitText.normalize(note.caption)),
                  const SizedBox(height: 4),
                  Text('Görseli büyütmek için dokun veya çift dokun.', style: Theme.of(context).textTheme.bodySmall),
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
      child: ClipRRect(borderRadius: BorderRadius.circular(12), child: imageWidget),
    );
  }

  Widget _buildImage(BuildContext context) {
    if (note.imageAsset.trim().isNotEmpty) {
      return Image.asset(note.imageAsset, fit: BoxFit.contain, width: double.infinity, errorBuilder: (context, error, stackTrace) => _MissingVisualBox(path: note.imageAsset));
    }
    if (note.imageBase64.trim().isNotEmpty) {
      final bytes = _tryDecodeBase64(note.imageBase64);
      if (bytes != null) return Image.memory(bytes, fit: BoxFit.contain, width: double.infinity);
    }
    return const _MissingVisualBox(path: 'Görsel verisi yok');
  }

  void _open(BuildContext context) => Navigator.of(context).push(MaterialPageRoute(builder: (_) => ImageViewerPage(note: note)));

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
      appBar: AppBar(backgroundColor: Colors.black, foregroundColor: Colors.white, title: Text(note.title, maxLines: 1, overflow: TextOverflow.ellipsis)),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(child: InteractiveViewer(minScale: 0.8, maxScale: 6, child: Center(child: _viewerImage()))),
            Padding(padding: const EdgeInsets.all(12), child: Text(TurkishUnitText.normalize(note.caption), style: const TextStyle(color: Colors.white70), textAlign: TextAlign.center)),
          ],
        ),
      ),
    );
  }

  Widget _viewerImage() {
    if (note.imageAsset.trim().isNotEmpty) return Image.asset(note.imageAsset, fit: BoxFit.contain);
    if (note.imageBase64.trim().isNotEmpty) {
      try {
        return Image.memory(base64Decode(note.imageBase64), fit: BoxFit.contain);
      } catch (_) {
        return const Text('Görsel açılamadı.', style: TextStyle(color: Colors.white));
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
      decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), color: Theme.of(context).colorScheme.errorContainer),
      child: Text('Görsel APK içinde bulunamadı. Dosya yolu: $path', style: Theme.of(context).textTheme.bodySmall),
    );
  }
}

class _UnitInfoBlock extends StatelessWidget {
  const _UnitInfoBlock();

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      color: Theme.of(context).colorScheme.secondaryContainer,
      margin: const EdgeInsets.only(bottom: 12),
      child: const Padding(
        padding: EdgeInsets.all(14),
        child: Text('Birim notu: Amerikan kaynaklı scf/scm/cfm ifadeleri Türkiye saha kullanımına uygun Nm³, m³/dk ve L/dk karşılıklarıyla değerlendirilir.'),
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
            Text(title, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
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
      decoration: BoxDecoration(color: Theme.of(context).colorScheme.primaryContainer, borderRadius: BorderRadius.circular(999)),
      child: Text(TurkishUnitText.normalize(label), style: Theme.of(context).textTheme.labelSmall),
    );
  }
}

class StandardsRepository {
  static const _standardAssetFiles = <String>['assets/standards.json', 'assets/standards_extra.json', 'assets/standards_overrides.json'];
  static const _educationAssetFiles = <String>['assets/education_notes.json', 'assets/education_notes_extra.json'];
  static const _visualAssetFiles = <String>['assets/visual_notes.json', 'assets/visual_notes_extra.json'];

  static Future<List<StandardItem>> loadItems() async {
    final decoded = <Map<String, dynamic>>[];
    for (final path in _standardAssetFiles) {
      final list = await _loadListAsset(path);
      for (final item in list) {
        if (item is Map<String, dynamic>) decoded.add(item);
      }
    }

    final notesByKey = await _loadEducationNotes();
    final visualsByKey = await _loadVisualNotes();
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
      final keys = <String>{TurkishUnitText.key(code), TurkishUnitText.key(title)};
      final notes = _collectStrings(notesByKey, keys);
      final visuals = _collectVisuals(visualsByKey, keys);
      items.add(StandardItem.fromJson(json, educationNotes: notes, visualNotes: visuals));
    }

    items.sort((a, b) => a.title.compareTo(b.title));
    return items;
  }

  static List<String> _collectStrings(Map<String, List<String>> index, Set<String> keys) {
    final result = <String>[];
    for (final key in keys) {
      if (key.isEmpty) continue;
      result.addAll(index[key] ?? const <String>[]);
    }
    return result;
  }

  static List<VisualNote> _collectVisuals(Map<String, List<VisualNote>> index, Set<String> keys) {
    final result = <VisualNote>[];
    final seen = <String>{};
    for (final key in keys) {
      if (key.isEmpty) continue;
      for (final note in index[key] ?? const <VisualNote>[]) {
        final noteKey = '${note.title}|${note.imageAsset}|${note.imageBase64.hashCode}|${note.placement}';
        if (seen.add(noteKey)) result.add(note);
      }
    }
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

  static Future<Map<String, List<String>>> _loadEducationNotes() async {
    final result = <String, List<String>>{};
    for (final path in _educationAssetFiles) {
      final decoded = await _loadMapAsset(path);
      for (final entry in decoded.entries) {
        final key = TurkishUnitText.key(entry.key);
        result.putIfAbsent(key, () => <String>[]).addAll(StandardItem.listFromDynamic(entry.value));
      }
    }
    return result;
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

  String get searchText => TurkishUnitText.normalize([
        title,
        code,
        category,
        subgroup,
        purpose,
        duration,
        flowRate,
        ...keywords,
        ...equipment,
        ...reagents,
        ...fieldSteps,
        ...criticalControls,
        ...acceptance,
        ...reporting,
        ...mistakes,
        ...educationNotes,
        ...visualNotes.map((note) => '${note.title} ${note.caption}'),
      ].join(' ')).toLowerCase();

  factory StandardItem.fromJson(Map<String, dynamic> json, {List<String> educationNotes = const <String>[], List<VisualNote> visualNotes = const <VisualNote>[]}) {
    return StandardItem(
      title: json['title'] as String? ?? '',
      code: json['code'] as String? ?? '',
      category: json['category'] as String? ?? '',
      subgroup: json['subgroup'] as String? ?? '',
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
    );
  }

  static List<String> listFromDynamic(dynamic value) {
    if (value is! List) return const <String>[];
    return value.map((item) => item.toString()).toList();
  }
}

class VisualNote {
  const VisualNote({required this.title, required this.caption, required this.imageBase64, required this.imageAsset, required this.placement});

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

class TurkishUnitText {
  const TurkishUnitText._();

  static String key(String input) => normalize(input).toLowerCase().trim();

  static String normalize(String input) {
    if (input.isEmpty) return input;
    var value = input;
    value = value.replaceAll(RegExp(r'0[,.]60\s*scm\s*/\s*21\s*scf', caseSensitive: false), '0,60 Nm³');
    value = value.replaceAll(RegExp(r'21\s*scf', caseSensitive: false), '0,60 Nm³');
    value = value.replaceAll(RegExp(r'0[,.]75\s*cfm\s*/\s*(yaklaşık\s*)?0[,.]021\s*m3\s*/\s*dk', caseSensitive: false), 'yaklaşık 21 L/dk (0,021 m³/dk)');
    value = value.replaceAll(RegExp(r'0[,.]021\s*m3\s*/\s*dk', caseSensitive: false), '0,021 m³/dk (yaklaşık 21 L/dk)');
    value = value.replaceAll(RegExp(r'0[,.]00057\s*m3\s*/\s*dk\s*/\s*0[,.]020\s*cfm', caseSensitive: false), '0,00057 m³/dk (yaklaşık 0,57 L/dk)');
    value = value.replaceAll(RegExp(r'0[,.]020\s*cfm', caseSensitive: false), '0,57 L/dk (0,00057 m³/dk)');
    value = value.replaceAll(RegExp(r'0[,.]00057\s*m3\s*/\s*dk', caseSensitive: false), '0,00057 m³/dk');
    value = value.replaceAll(RegExp(r'\bscm\b', caseSensitive: false), 'Nm³');
    value = value.replaceAll(RegExp(r'\bscf\b', caseSensitive: false), 'standart ft³ (Türkiye karşılığı: Nm³)');
    value = value.replaceAll(RegExp(r'\bcfm\b', caseSensitive: false), 'ft³/dk (Türkiye karşılığı: m³/dk veya L/dk)');
    value = value.replaceAll(RegExp(r'\bm3\s*/\s*dk\b', caseSensitive: false), 'm³/dk');
    value = value.replaceAll(RegExp(r'\bm3\b', caseSensitive: false), 'm³');
    value = value.replaceAll(RegExp(r'\bm2\b', caseSensitive: false), 'm²');
    return value;
  }
}
