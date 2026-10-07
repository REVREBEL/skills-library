---
name: "wordpress"
description: "Route WordPress development and administration tasks across core configuration, theme engineering, plugin development, WooCommerce customization, performance optimization, security hardening, testing, and deployment. Use when planning, building, extending, or tuning WordPress environments."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# WordPress Development Workflow Bundle

Coordinate WordPress engineering workflows across core administration, themes, plugins, e-commerce, performance optimization, security, testing, and deployment.

## Overview

WordPress powers modern web applications ranging from decoupled publishing systems to complex e-commerce platforms. This router coordinates specialized skills for core administration, theme engineering, custom plugin development, WooCommerce, and performance tuning.

## WordPress 7.0 Features (Backward Compatible)

### Real-Time Collaboration (RTC)
Native collaborative editing engine for block editing and RTC-compatible post meta.

### AI Connectors API
Standardized endpoint integration for LLM and generative AI services.

### Abilities API (Stable in 7.0)
Granular capability registration for plugin actions and workflow automation.

### DataViews & DataForm
Modern administrative UI components for dataset management and block templates.

### PHP-Only Block Registration
Streamlined server-side block registration without JavaScript toolchain overhead.

### Interactivity API Updates
Declarative frontend reactive directives and client-side navigation.

### Admin Refresh
Next-generation responsive administrative design and navigation.

### Pattern Editing
Enhanced pattern creation and full-page layout composition tools.

## When to Use This Workflow

Use this master router to navigate complex WordPress development tasks across the full software lifecycle.

## Workflow Phases

- **Phase 1: WordPress Setup**: Core installation, multisite configuration, and WP-CLI automation.
- **Phase 2: Theme Development**: Block themes, `theme.json` styling, template hierarchy, and FSE.
- **Phase 3: Plugin Development**: Custom post types, REST API endpoints, AI Connectors, and Abilities API.
- **Phase 4: WooCommerce Integration**: Product models, checkout flows, and payment integrations.
- **Phase 5: Performance Optimization**: Object caching, query tuning, and asset optimization.
- **Phase 6: Security Hardening**: Permissions, salt rotation, and XML-RPC disablement.
- **Phase 7: Testing**: PHPUnit, WP-CLI test runner, and Playwright verification.
- **Phase 8: Deployment**: Database migrations, search-replace, and zero-downtime rollouts.

## Decision Matrix & Routing Table

| User Goal | Focus Area | Specialized Child Skill |
|---|---|---|
| Core setup, multisite config, WP-CLI automation, deployment, security hardening | Core & Admin | [WordPress Core & Admin](./wordpress-core-admin/SKILL.md) |
| Block themes, `theme.json`, template hierarchy, FSE styling, PHP block registration | Theme Engineering | [WordPress Theme Development](./wordpress-theme-development/SKILL.md) |
| Custom plugins, action/filter hooks, REST API routes, AI Connectors, Abilities API | Plugin Engineering | [WordPress Plugin Development](./wordpress-plugin-development/SKILL.md) |
| WooCommerce catalog, custom cart/checkout, payment gateways, product data models | E-Commerce | [WordPress WooCommerce](./wordpress-woocommerce/SKILL.md) |
| Object caching (Redis), query profiling, asset minification, database indexing | Performance | [WordPress Performance Optimization](./wordpress-performance-optimization/SKILL.md) |

## WordPress-Specific Workflows

Refer to specialized child skills for detailed workflow implementations across Custom Post Types, Custom REST Endpoints, AI Connectors, PHP-only blocks, Abilities API, and WooCommerce Product Types.

## Quality Gates

- **Coding Standards**: Enforce `WordPress-Core`, `WordPress-Docs`, and `WordPress-Extra` via PHP_CodeSniffer.
- **Security Hardening**: Sanitize all inputs (`sanitize_text_field`), validate nonces (`wp_verify_nonce`), escape all outputs (`esc_html`, `esc_attr`), and use `$wpdb->prepare()`.
- **Testing Priorities**: Unit testing with PHPUnit, integration testing with WP-CLI test runner, and Playwright for frontend block interactions.

## Related Workflow Bundles

- **PHP Backend Engineering**: Modern PHP 8.1+ practices.
- **Gutenberg & React**: Custom block creation with React.
- **Infrastructure**: Redis object cache and MariaDB database tuning.

## Limitations

Requires PHP 8.1+ and MySQL 8.0+ / MariaDB 10.5+ for modern WordPress 7.0 feature compatibility.
