import 'dart:convert';

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
      title: 'Standartlar Cep Rehberi',
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
      appBar: AppBar(
        title: const Text('Emisyon / İmisyon Cep Rehberi'),
        centerTitle: false,
      ),
      body: SafeArea(
        child: FutureBuilder<List<StandardItem>>(
          future: _itemsFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
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
                      Expanded(
                        child: Text(
                          'Offline çalışır • Görsel eğitim notları eklendi',
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ),
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
        onTap: () => Navigator.of(context).push(
          MaterialPageRoute(builder: (_) => StandardDetailPage(item: item)),
        ),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Text(
                      item.title,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
                    ),
                  ),
                  const SizedBox(width: 8),
                  const Icon(Icons.chevron_right),
                ],
              ),
              const SizedBox(height: 6),
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: [
                  _MiniChip(label: item.code),
                  _MiniChip(label: item.category),
                  _MiniChip(label: item.subgroup),
                ],
              ),
              const SizedBox(height: 10),
              Text(TurkishUnitText.normalize(item.purpose), maxLines: 3, overflow: TextOverflow.ellipsis),
              if (item.educationNotes.isNotEmpty || item.visualNotes.isNotEmpty) ...[
                const SizedBox(height: 8),
                Row(
                  children: [
                    Icon(Icons.school, size: 16, color: Theme.of(context).colorScheme.primary),
                    const SizedBox(width: 5),
                    Expanded(
                      child: Text(
                        '${item.educationNotes.length} eğitim notu • ${item.visualNotes.length} görsel',
                        style: Theme.of(context).textTheme.labelMedium,
                      ),
                    ),
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(item.code)),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 24),
        children: [
          Text(
            item.title,
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              _MiniChip(label: item.category),
              _MiniChip(label: item.subgroup),
              _MiniChip(label: item.code),
            ],
          ),
          const SizedBox(height: 16),
          const _UnitInfoBlock(),
          _VisualNotesBlock(notes: item.visualNotes),
          _InfoBlock(title: 'Eğitim dokümanı ayrıntıları', body: _numbered(item.educationNotes)),
          _InfoBlock(title: 'Amaç', body: item.purpose),
          _InfoBlock(title: 'Ölçüm süresi', body: item.duration),
          _InfoBlock(title: 'Debi / hacim notu', body: item.flowRate),
          _InfoBlock(title: 'Cihaz / ekipman', body: item.equipment.join('\n')),
          _InfoBlock(title: 'Çözelti / absorban', body: item.reagents.join('\n')),
          _InfoBlock(title: 'Saha adımları', body: _numbered(item.fieldSteps)),
          _InfoBlock(title: 'Kritik teknik kontroller', body: item.criticalControls.join('\n')),
          _InfoBlock(title: 'Kabul / ret kriterleri', body: item.acceptance.join('\n')),
          _InfoBlock(title: 'Raporlama notları', body: item.reporting.join('\n')),
          _InfoBlock(title: 'Sık yapılan saha hataları', body: item.mistakes.join('\n')),
          const SizedBox(height: 12),
          Text(
            'Not: Bu uygulama sahacı hızlı rehberi olarak hazırlanmıştır. Resmi raporlamada yürürlükteki standart, mevzuat ve laboratuvar talimatı esas alınmalıdır.',
            style: Theme.of(context).textTheme.bodySmall,
          ),
        ],
      ),
    );
  }

  String _numbered(List<String> values) {
    return values.asMap().entries.map((entry) => '${entry.key + 1}. ${entry.value}').join('\n');
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
            color: Theme.of(context).colorScheme.tertiaryContainer,
            margin: const EdgeInsets.only(bottom: 12),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Görsel eğitim notu',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800),
                  ),
                  const SizedBox(height: 8),
                  Text(note.title, style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w700)),
                  const SizedBox(height: 10),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(12),
                    child: Image.memory(
                      base64Decode(note.imageBase64),
                      fit: BoxFit.contain,
                      width: double.infinity,
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(TurkishUnitText.normalize(note.caption)),
                ],
              ),
            ),
          ),
      ],
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
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Birim notu', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
            const SizedBox(height: 8),
            const Text('Bu rehberde Amerikan kaynaklı scf/scm/cfm ifadeleri Türkiye saha kullanımına çevrilmiş olarak gösterilir: Nm³, m³/dk ve L/dk esas alınır.'),
          ],
        ),
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
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.primaryContainer,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(TurkishUnitText.normalize(label), style: Theme.of(context).textTheme.labelSmall),
    );
  }
}

class StandardsRepository {
  static Future<List<StandardItem>> loadItems() async {
    final raw = await rootBundle.loadString('assets/standards.json');
    final decoded = jsonDecode(raw) as List<dynamic>;
    final notesByCode = await _loadEducationNotes();
    final visualsByCode = await _loadVisualNotes();

    return decoded.map((item) {
      final json = item as Map<String, dynamic>;
      final code = json['code'] as String? ?? '';
      final title = json['title'] as String? ?? '';
      final notes = notesByCode[code] ?? notesByCode[title] ?? const <String>[];
      final visuals = visualsByCode[code] ?? visualsByCode[title] ?? const <VisualNote>[];
      return StandardItem.fromJson(json, educationNotes: notes, visualNotes: visuals);
    }).toList();
  }

  static Future<Map<String, List<String>>> _loadEducationNotes() async {
    try {
      final raw = await rootBundle.loadString('assets/education_notes.json');
      final decoded = jsonDecode(raw) as Map<String, dynamic>;
      return decoded.map((key, value) => MapEntry(key, StandardItem.listFromDynamic(value)));
    } catch (_) {
      return const <String, List<String>>{};
    }
  }

  static Future<Map<String, List<VisualNote>>> _loadVisualNotes() async {
    try {
      final raw = await rootBundle.loadString('assets/visual_notes.json');
      final decoded = jsonDecode(raw) as List<dynamic>;
      final result = <String, List<VisualNote>>{};
      for (final entry in decoded) {
        final map = entry as Map<String, dynamic>;
        final standards = StandardItem.listFromDynamic(map['standards']);
        final note = VisualNote.fromJson(map);
        for (final standard in standards) {
          result.putIfAbsent(standard, () => <VisualNote>[]).add(note);
        }
      }
      return result;
    } catch (_) {
      return const <String, List<VisualNote>>{};
    }
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

  factory StandardItem.fromJson(
    Map<String, dynamic> json, {
    List<String> educationNotes = const <String>[],
    List<VisualNote> visualNotes = const <VisualNote>[],
  }) {
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
  const VisualNote({required this.title, required this.caption, required this.imageBase64});

  final String title;
  final String caption;
  final String imageBase64;

  factory VisualNote.fromJson(Map<String, dynamic> json) {
    return VisualNote(
      title: json['title'] as String? ?? '',
      caption: json['caption'] as String? ?? '',
      imageBase64: json['imageBase64'] as String? ?? '',
    );
  }
}

class TurkishUnitText {
  const TurkishUnitText._();

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
