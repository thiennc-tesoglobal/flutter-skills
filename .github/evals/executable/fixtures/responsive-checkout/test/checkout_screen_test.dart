import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:responsive_checkout_fixture/checkout_screen.dart';

class Scenario {
  const Scenario(
    this.name,
    this.width, {
    this.height = 700,
    this.textScale = 1,
    this.longContent = false,
    this.validationError = false,
    this.rtl = false,
    this.keyboardInset = 0,
  });

  final String name;
  final double width;
  final double height;
  final double textScale;
  final bool longContent;
  final bool validationError;
  final bool rtl;
  final double keyboardInset;
}

void main() {
  const scenarios = [
    Scenario('compact', 320),
    Scenario('below breakpoint', 599),
    Scenario('at breakpoint', 600),
    Scenario('above breakpoint', 601),
    Scenario('wide', 840),
    Scenario(
      'compact long RTL enlarged error with keyboard',
      320,
      height: 640,
      textScale: 2,
      longContent: true,
      validationError: true,
      rtl: true,
      keyboardInset: 260,
    ),
  ];

  for (final scenario in scenarios) {
    testWidgets(scenario.name, (tester) async {
      final view = tester.view;
      view.devicePixelRatio = 1;
      view.physicalSize = Size(scenario.width, scenario.height);
      view.viewInsets = FakeViewPadding(bottom: scenario.keyboardInset);
      addTearDown(view.reset);

      await tester.pumpWidget(
        MaterialApp(
          builder: (context, child) => MediaQuery(
            data: MediaQuery.of(
              context,
            ).copyWith(textScaler: TextScaler.linear(scenario.textScale)),
            child: Directionality(
              textDirection: scenario.rtl
                  ? TextDirection.rtl
                  : TextDirection.ltr,
              child: child!,
            ),
          ),
          home: CheckoutScreen(
            longContent: scenario.longContent,
            validationError: scenario.validationError,
          ),
        ),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);

      final delivery = tester.getRect(
        find.byKey(const ValueKey('delivery-control')),
      );
      final pickup = tester.getRect(
        find.byKey(const ValueKey('pickup-control')),
      );
      expect(
        delivery.overlaps(pickup),
        isFalse,
        reason: 'Independent controls must not intersect',
      );
      expect(
        find.byKey(
          ValueKey(
            scenario.width >= 600 ? 'wide-controls' : 'compact-controls',
          ),
        ),
        findsOneWidget,
        reason: 'The controls switch composition at 600 logical pixels',
      );
      final viewport = Rect.fromLTWH(0, 0, scenario.width, scenario.height);
      expect(
        delivery.left >= viewport.left && delivery.right <= viewport.right,
        isTrue,
      );
      expect(
        pickup.left >= viewport.left && pickup.right <= viewport.right,
        isTrue,
      );

      final avatar = tester.getRect(find.byKey(const ValueKey('avatar')));
      final badge = tester.getRect(
        find.byKey(const ValueKey('verified-badge')),
      );
      expect(
        avatar.overlaps(badge),
        isTrue,
        reason: 'The named verification badge is an intentional overlay',
      );

      await tester.drag(
        find.byKey(const ValueKey('form-scroll')),
        const Offset(0, -1200),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      final field = tester.getRect(find.byKey(const ValueKey('last-field')));
      final action = tester.getRect(
        find.byKey(const ValueKey('checkout-action')),
      );
      expect(
        field.bottom <= action.top - 8,
        isTrue,
        reason: 'The final field must scroll above the sticky action',
      );
      expect(
        action.bottom <= scenario.height - scenario.keyboardInset,
        isTrue,
        reason: 'The action must stay above the simulated keyboard',
      );
      expect(action.top >= 0, isTrue);
      expect(
        find.byKey(const ValueKey('checkout-action')).hitTestable(),
        findsOneWidget,
      );

      if (scenario.validationError) {
        final error = tester.getRect(find.text(errorMessage));
        final paragraph = tester.renderObject<RenderParagraph>(
          find.text(errorMessage),
        );
        expect(
          paragraph.didExceedMaxLines,
          isFalse,
          reason: 'The validation message must not be ellipsized',
        );
        expect(
          error.height,
          greaterThan(18),
          reason: 'The complete enlarged validation message must reflow',
        );
        expect(error.bottom <= action.top - 8, isTrue);
      }

      await tester.tap(find.byKey(const ValueKey('checkout-action')));
      await tester.pump();
      expect(find.text('Order placed'), findsOneWidget);
    });
  }
}
