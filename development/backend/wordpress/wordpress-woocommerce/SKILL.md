---
name: wordpress-woocommerce
description: 'Customize WooCommerce e-commerce stores, custom product types, cart/checkout extensions, and payment gateway integrations. Use when building online stores or customizing WooCommerce functionality.'
compatibility: 'Requires WordPress 6.0+ and WooCommerce 8.0+.'
metadata:
  category: development
  type: execution-child
  source: custom
---

# WordPress WooCommerce Customization

Build and customize WooCommerce stores, checkout flows, and product data models.

## When to Use

- Creating custom product types and custom product fields
- Customizing checkout workflows, billing fields, and order processing
- Integrating custom payment gateways and shipping calculators
- Automating post-order webhook and inventory sync events

## Phase 4: WooCommerce Integration

### Skills to Invoke
Use `wordpress-woocommerce` for store customizations.

### Actions
- Register custom product types and checkout action hooks.

### WordPress 7.0 + WooCommerce Considerations
Ensure compatibility with High-Performance Order Storage (HPOS) and block-based checkout.

### Copy-Paste Prompts
Prompt: `Register a custom course product type and add order processing hooks.`

## WooCommerce Custom Product Type

```php
add_action('init', function () {
    class WC_Product_Custom_Course extends WC_Product {
        public function get_type() {
            return 'custom_course';
        }
    }
});
```

## Checkout Hook Integration

```php
add_action('woocommerce_checkout_order_processed', 'custom_process_order', 10, 3);
function custom_process_order($order_id, $posted_data, $order) {
    $order->add_order_note('Processed via custom automated inventory integration.');
}
```

## Completion Evidence

- Verified test transaction and error-free checkout workflow.
