import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:emisyon_standartlari_cep_rehberi/quiz.dart';

void main(){
  TestWidgetsFlutterBinding.ensureInitialized();
  late QuizBank bank;
  setUpAll(()async{bank=await QuizBank.load();});
  test('Shuffling keeps answer identity and does not mutate source',(){
    for(final q in bank.questions){
      final shuffled=q.shuffled(Random(13));
      expect(shuffled.choices[shuffled.correctIndex],q.choices[q.correctIndex]);
      expect(q.correctIndex,0);
    }
  });
  test('Selection has no duplicates and scoring distinguishes blanks',(){
    final s=QuizSession(bank.questions,10,seed:1);
    expect(s.questions.map((q)=>q.id).toSet().length,10);
    s.answers[0]=s.questions[0].correctIndex;
    s.answers[1]=(s.questions[1].correctIndex+1)%4;
    expect(s.correct,1);expect(s.wrong,1);expect(s.blank,8);expect(s.score,10);
    expect(QuizSession(bank.questions.take(2).toList(),20).questions.length,2);
  });
  testWidgets('A user can answer and receive explanations after finishing',(tester)async{
    final s=QuizSession(bank.questions,1,seed:2);
    await tester.pumpWidget(MaterialApp(home:QuizExamPage(session:s)));
    expect(find.textContaining('Doğru:'),findsNothing);
    await tester.tap(find.text('A) ${s.questions.first.choices.first}'));
    await tester.pump();
    await tester.tap(find.text('Bitir'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Bitir ve değerlendir'));
    await tester.pumpAndSettle();
    expect(find.text('Test sonucu ve açıklamalar'),findsOneWidget);
    expect(find.textContaining('Doğru:'),findsOneWidget);
    expect(find.text(s.questions.first.explanation),findsOneWidget);
    expect(tester.takeException(),isNull);
  });
  testWidgets('Quiz setup offers separate scopes and test types',(tester)async{
    await tester.pumpWidget(MaterialApp(home:Scaffold(body:QuizSetup(bank:bank))));
    expect(find.text('Ölçüm kapsamı'),findsOneWidget);
    expect(find.text('Test türü'),findsOneWidget);
    await tester.tap(find.byKey(const ValueKey('quiz-scope')));
    await tester.pumpAndSettle();
    await tester.tap(find.text('İmisyon').last);
    await tester.pumpAndSettle();
    expect(find.textContaining('Bu seçimde 25 soru var.'),findsOneWidget);
    expect(tester.takeException(),isNull);
  });
}
