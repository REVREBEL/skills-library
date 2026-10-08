---
name: wordpress-performance-optimization
description: 'Optimize WordPress performance, database queries, Redis/Memcached object caching, asset loading, and CDN integration. Use when tuning slow WordPress sites, reducing TTFB, or optimizing Core Web Vitals.'
compatibility: 'Requires WordPress 6.0+, Redis/Memcached server, and WP-CLI.'
metadata:
  category: development
  type: execution-child
  source: custom
---

# WordPress Performance Optimization

Tune WordPress site speed, query performance, object caching, and Core Web Vitals.

## When to Use

- Configuring Redis or Memcached persistent object caching
- Profiling slow database queries with Query Monitor and indexing tables
- Optimizing script enqueueing, CSS delivery, and image compression
- Automating database transients and revision cleanup via WP-CLI

## Phase 5: Performance Optimization

### Skills to Invoke
Use `wordpress-performance-optimization` for tuning.

### Actions
- Configure object caching and optimize database tables.

### WordPress 7.0 Performance & Performance Checklist
- [x] Redis persistent object cache drop-in configured
- [x] Autoloaded options under 800KB
- [x] Database transients and revisions cleaned
- [x] Script deferral strategy enabled for non-critical assets

### Copy-Paste Prompts
```bash
wp db optimize
wp transient delete --all
wp post delete $(wp post list --post_type='revision' --format=ids) --force
```

## Completion Evidence

- Measurable reduction in TTFB and database query count.
