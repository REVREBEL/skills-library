---
name: wordpress-plugin-development
description: 'Develop custom WordPress plugins with action/filter hooks, custom post types, custom REST API endpoints, RTC-compatible post meta, AI Connectors API, and Abilities API. Use when extending WordPress functionality or building integrations.'
compatibility: 'Requires PHP 8.1+ and WordPress 6.0+.'
metadata:
  category: development
  type: execution-child
  source: custom
---

# WordPress Plugin Development

Author robust, secure, and extensible custom WordPress plugins using standard hooks, REST endpoints, and WordPress 7.0 APIs.

## When to Use

- Registering custom post types and taxonomies with RTC compatibility
- Creating custom REST API endpoints under `register_rest_route`
- Integrating AI Connectors API and registering Abilities API
- Implementing secure lifecycle hooks (`init`, `wp_enqueue_scripts`, `save_post`)

## Phase 3: Plugin Development

### Skills to Invoke
Use `wordpress-plugin-development` for custom plugin authoring.

### Actions
- Register hooks, post types, and REST routes.
- Integrate AI connectors and Abilities API.

### WordPress 7.0 Plugin Considerations & Plugin Structure
- Support RTC collaborative editing for post meta.
- Provide declarative ability definitions for agentic workflows.

### RTC-Compatible Post Meta Registration
```php
add_action('init', function () {
    register_post_type('project', [
        'public'       => true,
        'label'        => 'Projects',
        'show_in_rest' => true,
        'supports'     => ['title', 'editor', 'custom-fields', 'revisions', 'rtc'],
    ]);

    register_post_meta('project', '_project_status', [
        'show_in_rest' => true,
        'single'       => true,
        'type'         => 'string',
        'auth_callback' => function () { return current_user_can('edit_posts'); }
    ]);
});
```

### AI Connector Example
```php
add_action('wp_ai_connectors_init', function () {
    wp_register_ai_connector('gemini-summarizer', [
        'provider' => 'google',
        'model'    => 'gemini-1.5-pro',
    ]);
});
```

### Copy-Paste Prompts
Prompt: `Create a custom plugin with RTC-compatible custom post type and REST route.`

## WordPress-Specific Workflows

### Custom Post Type Development (RTC-Compatible)
Documented in the registration example above.

### Custom REST API Endpoint
```php
add_action('rest_api_init', function () {
    register_rest_route('custom/v1', '/data', [
        'methods'  => 'GET',
        'callback' => 'custom_get_data_handler',
        'permission_callback' => function () {
            return current_user_can('read');
        },
    ]);
});

function custom_get_data_handler(WP_REST_Request $request) {
    return new WP_REST_Response(['status' => 'success', 'data' => []], 200);
}
```

### WordPress 7.0 AI Connector Usage
Documented in AI connector registration.

### Abilities API Registration
```php
add_action('wp_abilities_init', function () {
    wp_register_ability('generate_summary', [
        'label'       => 'Generate Summary',
        'description' => 'Uses AI connector to summarize post content.',
        'callback'    => 'custom_ai_summarize_post',
    ]);
});
```

## Completion Evidence

- Plugin activation without PHP warnings/errors and passing `phpcs --standard=WordPress`.
