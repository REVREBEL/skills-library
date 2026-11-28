---
name: "seo-image-gen-suite"
description: "Generate SEO-focused images such as OG cards, hero images, schema assets, product visuals, and infographics. Use when image generation is part of an SEO workflow or content publishing task."
license: "MIT"
metadata:
  canonical_id: "marketing-and-seo:seo-image-gen-suite"
  urn: "urn:skill:marketing-and-seo:seo-image-gen-suite"
  role: "capability"
  applications:
    - gemini
    - banana
  keywords:
    - seo-image-generation
    - og-cards
    - hero-images
    - schema-assets
    - product-visuals
    - infographics
    - social-preview-images
    - banana-creative-director
    - gemini-image-generation
    - aspect-ratios
  tags:
    - marketing
    - seo
    - content
    - image-generation
    - publishing
  applications_compatibility: "universal"
  execution_provider:
    default: "banana"
    supported:
      - name: "banana"
        provider_type: "mcp"
        transport: "mcp"
        server_name: "banana"
        tool_name: "gemini_generate_image"
  relationships:
    depends_on: []
    composed_of: []
    extends: null
    adapts: null
    aliased_to: null
  security:
    risk: "low"
    side_effects: "write"
    requires_approval: true
---
# SEO Image Gen: AI Image Generation for SEO Assets (Extension)

Generate production-ready images for SEO use cases using Gemini's image generation
via the banana Creative Director pipeline. Maps SEO needs to optimized domain modes,
aspect ratios, and resolution defaults.

## When to Use
- Use when generating OG images, hero images, schema visuals, infographics, or similar SEO assets.
- Use when image generation is part of a broader SEO or publishing workflow.
- Use only when the required image-generation extension is available.

## Architecture Note

This skill has two components with distinct roles:
- **SKILL.md** (this file): Handles interactive `/seo image-gen` commands for generating images
- **Agent** (`agents/seo-image-gen.md`): Audit-only analyst spawned during `/seo audit` to assess existing OG/social images and produce a generation plan (never auto-generates)

## Prerequisites

This skill requires the banana extension to be installed:
```bash
./extensions/banana/install.sh
```

**Check availability:** Before using any image generation tool, verify the MCP server
is connected by checking if `gemini_generate_image` or `set_aspect_ratio` tools are
available. If tools are not available, inform the user the extension is not installed
and provide install instructions.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo image-gen og <description>` | Generate OG/social preview image (1200x630 feel) |
| `/seo image-gen hero <description>` | Blog hero image (widescreen, dramatic) |
| `/seo image-gen product <description>` | Product photography (clean, white BG) |
| `/seo image-gen infographic <description>` | Infographic visual (vertical, data-heavy) |
| `/seo image-gen custom <description>` | Custom image with full Creative Director pipeline |
| `/seo image-gen batch <description> [N]` | Generate N variations (default: 3) |

## SEO Image Use Cases

Each use case maps to pre-configured banana parameters:

| Use Case | Aspect Ratio | Resolution | Domain Mode | Notes |
|----------|-------------|------------|-------------|-------|
| **OG/Social Preview** | `16:9` | `1K` | Product or UI/Web | Clean, professional, text-friendly |
| **Blog Hero** | `16:9` | `2K` | Cinema or Editorial | Dramatic, atmospheric, editorial quality |
| **Schema Image** | `4:3` | `1K` | Product | Clean, descriptive, schema ImageObject |
| **Social Square** | `1:1` | `1K` | UI/Web | Platform-optimized square |
| **Product Photo** | `4:3` | `2K` | Product | White background, studio lighting |
| **Infographic** | `2:3` | `4K` | Infographic | Data-heavy, vertical layout |
| **Favicon/Icon** | `1:1` | `512` | Logo | Minimal, scalable, recognizable |
| **Pinterest Pin** | `2:3` | `2K` | Editorial | Tall vertical card |

## Generation Pipeline

For every generation request:

1. **Identify use case** from command or context (og, hero, product, etc.)
2. **Apply SEO defaults** from the use cases table above
3. **Set aspect ratio** via `set_aspect_ratio` MCP tool
4. **Construct Reasoning Brief** using the banana Creative Director pipeline:
   - Load `references/prompt-engineering.md` for the 6-component system
   - Apply domain mode emphasis (Subject 30%, Style 25%, Context 15%, etc.)
   - Be SPECIFIC and VISCERAL: describe what the camera sees
5. **Generate** via `gemini_generate_image` MCP tool
6. **Post-generation SEO checklist** (see below)

### Check for Presets

If the user mentions a brand or has SEO presets configured:
```bash
python3 ~/.agents/skills/seo-image-gen/scripts/presets.py list
```
Load matching preset and apply as defaults. Also check `references/seo-image-presets.md`
for SEO-specific preset templates.

## Post-Generation SEO Checklist


## Merged Capabilities

- Install banana extension via ./extensions/banana/install.sh
- Check availability of gemini_generate_image or set_aspect_ratio tools before using image generation
- Inform user if tools are not available and provide install instructions
- Generate OG/social preview image via /seo image-gen og <description>
- Generate blog hero image via /seo image-gen hero <description>
- Generate product photography via /seo image-gen product <description>
- Generate infographic visual via /seo image-gen infographic <description>
- Generate custom image with full Creative Director pipeline via /seo image-gen custom <description>
- Generate N variations via /seo image-gen batch <description> [N]
- Identify use case from command or context (og, hero, product, etc.)
- Apply SEO defaults from the use cases table
- Set aspect ratio via set_aspect_ratio MCP tool
- Load references/prompt-engineering.md for the 6-component system
- Apply domain mode emphasis (Subject 30%, Style 25%, Context 15%, etc.)
- Be SPECIFIC and VISCERAL: describe what the camera sees
- Generate via gemini_generate_image MCP tool
- Check for presets via python3 presets.py list
- Load matching preset and apply as defaults
- Also check references/seo-image-presets.md for SEO-specific preset templates
- Write descriptive, keyword-rich alt text for the generated image
- Rename to SEO-friendly format: keyword-description-widthxheight.webp
- Convert to WebP for optimal page speed: magick output.png -quality 85 output.webp
- Target under 200KB for hero images, under 100KB for thumbnails
- Suggest ImageObject schema with @type, url, width, height, caption
- Remind about OG meta tags: og:image, og:image:width, og:image:height, og:image:alt
- Show estimated cost before generating (especially for batch)
- Log every generation via cost_tracker.py log --model MODEL --resolution RES --prompt brief
- Run cost_tracker.py summary if user asks about usage
- Use gemini-3.1-flash-image-preview @ 1K for OG images, social previews
- Use gemini-3.1-flash-image-preview @ 2K for hero images, product photos
- Use gemini-3.1-flash-image-preview @ 2K, thinking: high for infographics with text
- Use gemini-2.5-flash-image @ 512 for quick drafts
- Get new API key at https://aistudio.google.com/apikey if API key invalid
- Wait 60s, retry if rate limited (429)
- Rephrase prompt if IMAGE_SAFETY error
- Fall back: python3 generate.py --prompt ... --aspect-ratio 16:9 if MCP unavailable
- Provide image path where it was saved after generating
- Provide crafted prompt showing what was sent to the API after generating
- Provide settings: model, aspect ratio, resolution after generating
- Provide SEO checklist: alt text suggestion, file naming, WebP conversion after generating
- Provide schema snippet: ImageObject or og:image markup if applicable after generating
