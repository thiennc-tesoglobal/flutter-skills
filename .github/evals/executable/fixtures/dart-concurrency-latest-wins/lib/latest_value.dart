class LatestValue<T> {
  T? value;
  bool _disposed = false;

  Future<void> run(Future<T> Function() operation) async {
    if (_disposed) return;
    final result = await operation();
    if (!_disposed) value = result;
  }

  void dispose() {
    _disposed = true;
  }
}
