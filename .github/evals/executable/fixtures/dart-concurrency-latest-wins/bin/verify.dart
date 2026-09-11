import 'dart:async';

import '../lib/latest_value.dart';

Future<void> main() async {
  final latest = LatestValue<String>();
  final older = Completer<String>();
  final newer = Completer<String>();

  final olderRun = latest.run(() => older.future);
  final newerRun = latest.run(() => newer.future);
  newer.complete('newer');
  await newerRun;
  older.complete('older');
  await olderRun;
  if (latest.value != 'newer') {
    throw StateError('An older result replaced the newest result.');
  }

  final afterDispose = Completer<String>();
  final disposedRun = latest.run(() => afterDispose.future);
  latest.dispose();
  afterDispose.complete('after-dispose');
  await disposedRun;
  if (latest.value != 'newer') {
    throw StateError('A result was accepted after disposal.');
  }
}
