import 'package:flutter/material.dart';

const errorMessage =
    'Please enter the full delivery address, including building and floor.';

class CheckoutScreen extends StatefulWidget {
  const CheckoutScreen({
    super.key,
    required this.longContent,
    required this.validationError,
  });

  final bool longContent;
  final bool validationError;

  @override
  State<CheckoutScreen> createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends State<CheckoutScreen> {
  bool placed = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Stack(
          children: [
            SingleChildScrollView(
              key: const ValueKey('form-scroll'),
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 112),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 16),
                    SizedBox(
                      width: 64,
                      height: 64,
                      child: Stack(
                        children: [
                          const CircleAvatar(
                            key: ValueKey('avatar'),
                            radius: 32,
                            child: Icon(Icons.person),
                          ),
                          Positioned(
                            right: 0,
                            bottom: 0,
                            child: Container(
                              key: const ValueKey('verified-badge'),
                              width: 22,
                              height: 22,
                              decoration: const BoxDecoration(
                                color: Colors.green,
                                shape: BoxShape.circle,
                              ),
                              child: const Icon(Icons.check, size: 14),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      widget.longContent
                          ? 'Delivery preferences for a very long localized customer name'
                          : 'Delivery preferences',
                    ),
                    const SizedBox(height: 16),
                    LayoutBuilder(
                      builder: (context, constraints) {
                        final controls = [
                          SizedBox(
                            width: 160,
                            child: OutlinedButton(
                              key: const ValueKey('delivery-control'),
                              onPressed: () {},
                              child: const Text('Delivery'),
                            ),
                          ),
                          SizedBox(
                            width: 160,
                            child: OutlinedButton(
                              key: const ValueKey('pickup-control'),
                              onPressed: () {},
                              child: const Text('Pickup'),
                            ),
                          ),
                        ];
                        if (constraints.maxWidth >= 568) {
                          return Row(
                            key: const ValueKey('wide-controls'),
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: controls,
                          );
                        }
                        return Wrap(
                          key: const ValueKey('compact-controls'),
                          spacing: 8,
                          runSpacing: 8,
                          children: controls,
                        );
                      },
                    ),
                    SizedBox(height: widget.longContent ? 430 : 330),
                    const TextField(
                      key: ValueKey('last-field'),
                      decoration: InputDecoration(labelText: 'Address'),
                    ),
                    if (widget.validationError) const Text(errorMessage),
                  ],
                ),
              ),
            ),
            Positioned(
              left: 0,
              right: 0,
              bottom: 0,
              child: ColoredBox(
                color: Theme.of(context).colorScheme.surface,
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: FilledButton(
                    key: const ValueKey('checkout-action'),
                    onPressed: () => setState(() => placed = true),
                    child: Text(placed ? 'Order placed' : 'Place order'),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
