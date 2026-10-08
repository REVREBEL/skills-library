---
name: wordpress-theme-development
description: 'Build custom WordPress block themes and classic themes adhering to the WordPress template hierarchy, theme.json v3, PHP-only block registration, and Interactivity API. Use when authoring custom themes, block patterns, and template parts.'
compatibility: 'Requires WordPress 6.0+ Full Site Editing (FSE).'
metadata:
  category: development
  type: execution-child
  source: custom
---

# WordPress Theme Development

Author custom WordPress block themes and hybrid themes following modern Full Site Editing (FSE) and WordPress 7.0 standards.

## When to Use

- Creating custom block themes using `theme.json` styling configurations
- Developing custom block patterns, template parts, and block variations
- Registering PHP-only blocks without JavaScript build steps
- Implementing reactive frontend behavior using the Interactivity API

## Phase 2: Theme Development

### Skills to Invoke
Use `wordpress-theme-development` for custom theme engineering.

### Actions
- Author `theme.json` styling definitions and color palettes.
- Create block templates and template parts in HTML and PHP.

### WordPress 7.0 Theme Considerations & Theme Structure
```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "color": {
      "palette": [
        { "slug": "primary", "color": "#0066cc", "name": "Primary" },
        { "slug": "neutral-dark", "color": "#111827", "name": "Dark Neutral" }
      ]
    },
    "layout": {
      "contentSize": "800px",
      "wideSize": "1200px"
    }
  }
}
```

### Copy-Paste Prompts
Prompt: `Scaffold a block theme with theme.json v3 and custom hero template part.`

## PHP-Only Block Registration (WordPress 7.0)

```php
add_action('init', function () {
    register_block_type('custom/hero-banner', [
        'render_callback' => 'custom_render_hero_banner',
        'title'           => 'Hero Banner',
        'category'        => 'text',
        'icon'            => 'cover-image',
    ]);
});

function custom_render_hero_banner($attributes, $content) {
    return sprintf('<div class="hero-banner">%s</div>', esc_html($content));
}
```

## Testing & Quality Gates

- Validate theme schema with `wp theme status`.
- Check styling across responsive viewports in FSE editor.

## Completion Evidence

- Validated `theme.json` schema and theme activation without fatal errors.
