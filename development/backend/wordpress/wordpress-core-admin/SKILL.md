---
name: wordpress-core-admin
description: 'Install, configure, manage, secure, test, and deploy WordPress instances using WP-CLI, environment configuration, database management, security hardening, and deployment scripts. Use for core setup, multisite, maintenance, and deployment workflows.'
compatibility: 'Requires PHP 8.1+, MySQL/MariaDB, and WP-CLI.'
metadata:
  category: development
  type: execution-child
  source: custom
---

# WordPress Core, Administration, Security & Deployment

Automate WordPress core installation, database configuration, multisite networks, security hardening, testing, and deployment via WP-CLI.

## When to Use

- Installing new WordPress sites or setting up local development environments
- Managing multisite networks and site mappings
- Automating database maintenance and options via WP-CLI
- Hardening site security
- Running administrative integration tests
- Executing production deployments and database migrations

## Phase 1: WordPress Setup

### Skills to Invoke
Use `wordpress-core-admin` for automated initialization.

### Actions
- Download core files and generate `wp-config.php`.
- Install database schema and configure initial admin account.

### WordPress 7.0 Configuration
```bash
wp core download
wp config create --dbname=wp_db --dbuser=wp_user --dbpass=secret --dbhost=localhost
wp core install --url=example.com --title="Production Site" --admin_user=admin --admin_email=admin@example.com
wp core multisite-convert --subdomains
```

### Copy-Paste Prompts
Prompt: `Initialize WordPress core with database wp_db and enable multisite subdomains.`

## Phase 6: Security Hardening

### Skills to Invoke
Use `wordpress-core-admin` for security hardening.

### Actions
- Configure file permissions (directories `755`, files `644`, `wp-config.php` `600`).
- Rotate salts and disable file modifications.

### WordPress 7.0 Security Considerations & Security Checklist
- [x] Security salts rotated (`wp config shuffle-salts`)
- [x] XML-RPC disabled
- [x] File editing disabled (`DISALLOW_FILE_EDIT`)
- [x] Custom table prefix configured (`wp_secure_`)

### Copy-Paste Prompts
Prompt: `Harden WordPress installation and verify file permissions.`

## Phase 7: Testing

### Skills to Invoke
Use `wordpress-core-admin` for testing.

### Actions
- Execute WP-CLI test runner and check database health.

### WordPress 7.0 Testing Priorities
- Verify database integrity with `wp db check`.
- Run health check scripts with `wp eval-file`.

### Copy-Paste Prompts
Prompt: `Run complete WordPress core and database health checks.`

## Phase 8: Deployment

### Skills to Invoke
Use `wordpress-core-admin` for deployment.

### Actions
- Export database and perform search-replace migration.

### Copy-Paste Prompts
```bash
wp db export backup.sql
wp search-replace 'https://dev.example.com' 'https://example.com' --all-tables
```

## Completion Evidence

- Verified site access via URL and successful response from `wp core is-installed`.
- Passing security audit and clean database migration report.
