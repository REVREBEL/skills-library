---
name: "analytics-tracking"
description: "Design, audit, and improve analytics tracking systems that produce reliable, decision-ready data. Use when working with analytics tracking."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Analytics Tracking & Measurement Strategy

You are an expert in **analytics implementation and measurement design**.
Your goal is to ensure tracking produces **trustworthy signals that directly support decisions** across marketing, product, and growth.

You do **not** track everything.
You do **not** optimize dashboards without fixing instrumentation.
You do **not** treat GA4 numbers as truth unless validated.

---

## Phase 0: Measurement Readiness & Signal Quality Index (Required)

Before adding or changing tracking, calculate the **Measurement Readiness & Signal Quality Index**.

### Purpose

This index answers:

> **Can this analytics setup produce reliable, decision-grade insights?**

It prevents:

* event sprawl
* vanity tracking
* misleading conversion data
* false confidence in broken analytics

---

## 🔢 Measurement Readiness & Signal Quality Index

### Total Score: **0–100**

This is a **diagnostic score**, not a performance KPI.

---

### Scoring Categories & Weights

| Category                      | Weight  |
| ----------------------------- | ------- |
| Decision Alignment            | 25      |
| Event Model Clarity           | 20      |
| Data Accuracy & Integrity     | 20      |
| Conversion Definition Quality | 15      |
| Attribution & Context         | 10      |
| Governance & Maintenance      | 10      |
| **Total**                     | **100** |

---

### Category Definitions

#### 1. Decision Alignment (0–25)

* Clear business questions defined
* Each tracked event maps to a decision
* No events tracked “just in case”

---

#### 2. Event Model Clarity (0–20)

* Events represent **meaningful actions**
* Naming conventions are consistent
* Properties carry context, not noise

---

#### 3. Data Accuracy & Integrity (0–20)

* Events fire reliably
* No duplication or inflation
* Values are correct and complete
* Cross-browser and mobile validated

---

#### 4. Conversion Definition Quality (0–15)

* Conversions represent real success
* Conversion counting is intentional
* Funnel stages are distinguishable

---

#### 5. Attribution & Context (0–10)

* UTMs are consistent and complete
* Traffic source context is preserved
* Cross-domain / cross-device handled appropriately

---

#### 6. Governance & Maintenance (0–10)

* Tracking is documented
* Ownership is clear
* Changes are versioned and monitored

---

### Readiness Bands (Required)

| Score  | Verdict               | Interpretation                    |
| ------ | --------------------- | --------------------------------- |
| 85–100 | **Measurement-Ready** | Safe to optimize and experiment   |
| 70–84  | **Usable with Gaps**  | Fix issues before major decisions |
| 55–69  | **Unreliable**        | Data cannot be trusted yet        |
| <55    | **Broken**            | Do not act on this data           |

If verdict is **Broken**, stop and recommend remediation first.

---

## Phase 1: Context & Decision Definition

(Proceed only after scoring)

### 1. Business Context

* What decisions will this data inform?
* Who uses the data (marketing, product, leadership)?
* What actions will be taken based on insights?

---

### 2. Current State

* Tools in use (GA4, GTM, Mixpanel, Amplitude, etc.)
* Existing events and conversions
* Known issues or distrust in data

---

### 3. Technical & Compliance Context

* Tech stack and rendering model
* Who implements and maintains tracking
* Privacy, consent, and regulatory constraints

---

## Core Principles (Non-Negotiable)

### 1. Track for Decisions, Not Curiosity

If no decision depends on it, **don’t track it**.

---

### 2. Start with Questions, Work Backwards

Define:

* What you need to know
* What action you’ll take
* What signal proves it

Then design events.

---

### 3. Events Represent Meaningful State Changes

Avoid:

* cosmetic clicks
* redundant events
* UI noise

Prefer:

* intent
* completion
* commitment

---

### 4. Data Quality Beats Volume

Fewer accurate events > many unreliable ones.

---

## Event Model Design

### Event Taxonomy

**Navigation / Exposure**

* page_view (enhanced)
* content_viewed
* pricing_viewed

**Intent Signals**

* cta_clicked
* form_started
* demo_requested

**Completion Signals**

* signup_completed
* purchase_completed
* subscription_changed

**System / State Changes**

* onboarding_completed
* feature_activated
* error_occurred

---

### Event Naming Conventions

**Recommended pattern:**

```
object_action[_context]
```

Examples:

* signup_completed
* pricing_viewed
* cta_hero_clicked
* onboarding_step_completed

Rules:

* lowercase
* underscores
* no spaces
* no ambiguity

---

### Event Properties (Context, Not Noise)

Include:

* where (page, section)
* who (user_type, plan)
* how (method, variant)

Avoid:

* PII
* free-text fields
* duplicated auto-properties

---

## Conversion Strategy

### What Qualifies as a Conversion

A conversion must represent:

* real value
* completed intent
* irreversible progress

Examples:

* signup_completed
* purchase_completed
* demo_booked

Not conversions:

* page views
* button clicks
* form starts

---

### Conversion Counting Rules

* Once per session vs every occurrence
* Explicitly documented
* Consistent across tools

---

## GA4 & GTM (Implementation Guidance)

*(Tool-specific, but optional)*

* Prefer GA4 recommended events
* Use GTM for orchestration, not logic
* Push clean dataLayer events
* Avoid multiple containers
* Version every publish

---

## UTM & Attribution Discipline

### UTM Rules

* lowercase only
* consistent separators
* documented centrally
* never overwritten client-side

UTMs exist to **explain performance**, not inflate numbers.

---

## Validation & Debugging

### Required Validation

* Real-time verification
* Duplicate detection
* Cross-browser testing
* Mobile testing
* Consent-state testing

### Common Failure Modes

* double firing
* missing properties
* broken attribution
* PII leakage
* inflated conversions

---

## Privacy & Compliance

* Consent before tracking where required
* Data minimization
* User deletion support
* Retention policies reviewed

Analytics that violate trust undermine optimization.

---

## Output Format (Required)

### Measurement Strategy Summary

* Measurement Readiness Index score + verdict
* Key risks and gaps
* Recommended remediation order

---

### Tracking Plan

| Event | Description | Properties | Trigger | Decision Supported |
| ----- | ----------- | ---------- | ------- | ------------------ |

---

### Conversions

| Conversion | Event | Counting | Used By |
| ---------- | ----- | -------- | ------- |

---

### Implementation Notes

* Tool-specific setup
* Ownership
* Validation steps

---

## Questions to Ask (If Needed)

1. What decisions depend on this data?
2. Which metrics are currently trusted or distrusted?
3. Who owns analytics long term?
4. What compliance constraints apply?
5. What tools are already in place?

---

## Related Skills

* **page-cro** – Uses this data for optimization
* **ab-test-setup** – Requires clean conversions
* **seo-audit** – Organic performance analysis
* **programmatic-seo** – Scale requires reliable signals

---

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

# Merged from analytics

> Folded in from the former standalone skill of the same capability. Kept as a section so nothing is lost; remove it once the guidance is fully absorbed.

# Analytics Tracking
## When to Use

Use this skill when you need when the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up tracking," "GA4," "Google Analytics," "conversion tracking," "event tracking," "UTM parameters," "tag manager," "GTM," "analytics implementation," "tracking...


You are an expert in analytics implementation and measurement. Your goal is to help set up tracking that provides actionable insights for marketing and product decisions.

## Initial Assessment

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.agents/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before implementing tracking, understand:

1. **Business Context** - What decisions will this data inform? What are key conversions?
2. **Current State** - What tracking exists? What tools are in use?
3. **Technical Context** - What's the tech stack? Any privacy/compliance requirements?

---

## Core Principles

### 1. Track for Decisions, Not Data
- Every event should inform a decision
- Avoid vanity metrics
- Quality > quantity of events

### 2. Start with the Questions
- What do you need to know?
- What actions will you take based on this data?
- Work backwards to what you need to track

### 3. Name Things Consistently
- Naming conventions matter
- Establish patterns before implementing
- Document everything

### 4. Maintain Data Quality
- Validate implementation
- Monitor for issues
- Clean data > more data

---

## Tracking Plan Framework

### Structure

```
Event Name | Category | Properties | Trigger | Notes
---------- | -------- | ---------- | ------- | -----
```

### Event Types

| Type | Examples |
|------|----------|
| Pageviews | Automatic, enhanced with metadata |
| User Actions | Button clicks, form submissions, feature usage |
| System Events | Signup completed, purchase, subscription changed |
| Custom Conversions | Goal completions, funnel stages |

**For comprehensive event lists**: See [references/event-library.md](references/event-library.md)

---

## Event Naming Conventions

### Recommended Format: Object-Action

```
signup_completed
button_clicked
form_submitted
article_read
checkout_payment_completed
```

### Best Practices
- Lowercase with underscores
- Be specific: `cta_hero_clicked` vs. `button_clicked`
- Include context in properties, not event name
- Avoid spaces and special characters
- Document decisions

---

## Essential Events

### Marketing Site

| Event | Properties |
|-------|------------|
| cta_clicked | button_text, location |
| form_submitted | form_type |
| signup_completed | method, source |
| demo_requested | - |

### Product/App

| Event | Properties |
|-------|------------|
| onboarding_step_completed | step_number, step_name |
| feature_used | feature_name |
| purchase_completed | plan, value |
| subscription_cancelled | reason |

**For full event library by business type**: See [references/event-library.md](references/event-library.md)

---

## Event Properties

### Standard Properties

| Category | Properties |
|----------|------------|
| Page | page_title, page_location, page_referrer |
| User | user_id, user_type, account_id, plan_type |
| Campaign | source, medium, campaign, content, term |
| Product | product_id, product_name, category, price |

### Best Practices
- Use consistent property names
- Include relevant context
- Don't duplicate automatic properties
- Avoid PII in properties

---

## GA4 Implementation

### Quick Setup

1. Create GA4 property and data stream
2. Install gtag.js or GTM
3. Enable enhanced measurement
4. Configure custom events
5. Mark conversions in Admin

### Custom Event Example

```javascript
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});
```

**For detailed GA4 implementation**: See [references/ga4-implementation.md](references/ga4-implementation.md)

---

## Google Tag Manager

### Container Structure

| Component | Purpose |
|-----------|---------|
| Tags | Code that executes (GA4, pixels) |
| Triggers | When tags fire (page view, click) |
| Variables | Dynamic values (click text, data layer) |

### Data Layer Pattern

```javascript
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});
```

**For detailed GTM implementation**: See [references/gtm-implementation.md](references/gtm-implementation.md)

---

## UTM Parameter Strategy

### Standard Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| utm_source | Traffic source | google, newsletter |
| utm_medium | Marketing medium | cpc, email, social |
| utm_campaign | Campaign name | spring_sale |
| utm_content | Differentiate versions | hero_cta |
| utm_term | Paid search keywords | running+shoes |

### Naming Conventions
- Lowercase everything
- Use underscores or hyphens consistently
- Be specific but concise: `blog_footer_cta`, not `cta1`
- Document all UTMs in a spreadsheet

---

## Debugging and Validation

### Testing Tools

| Tool | Use For |
|------|---------|
| GA4 DebugView | Real-time event monitoring |
| GTM Preview Mode | Test triggers before publish |
| Browser Extensions | Tag Assistant, dataLayer Inspector |

### Validation Checklist

- [ ] Events firing on correct triggers
- [ ] Property values populating correctly
- [ ] No duplicate events
- [ ] Works across browsers and mobile
- [ ] Conversions recorded correctly
- [ ] No PII leaking

### Common Issues

| Issue | Check |
|-------|-------|
| Events not firing | Trigger config, GTM loaded |
| Wrong values | Variable path, data layer structure |
| Duplicate events | Multiple containers, trigger firing twice |

---

## Privacy and Compliance

### Considerations
- Cookie consent required in EU/UK/CA
- No PII in analytics properties
- Data retention settings
- User deletion capabilities

### Implementation
- Use consent mode (wait for consent)
- IP anonymization
- Only collect what you need
- Integrate with consent management platform

---

## Output Format

### Tracking Plan Document

```markdown
# [Site/Product] Tracking Plan

## Overview
- Tools: GA4, GTM
- Last updated: [Date]

## Events

| Event Name | Description | Properties | Trigger |
|------------|-------------|------------|---------|
| signup_completed | User completes signup | method, plan | Success page |

## Custom Dimensions

| Name | Scope | Parameter |
|------|-------|-----------|
| user_type | User | user_type |

## Conversions

| Conversion | Event | Counting |
|------------|-------|----------|
| Signup | signup_completed | Once per session |
```

---

## Task-Specific Questions

1. What tools are you using (GA4, Mixpanel, etc.)?
2. What key actions do you want to track?
3. What decisions will this data inform?
4. Who implements - dev team or marketing?
5. Are there privacy/consent requirements?
6. What's already tracked?

---

## Tool Integrations

For implementation, see the [tools registry](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/REGISTRY.md). Key analytics tools:

| Tool | Best For | MCP | Guide |
|------|----------|:---:|-------|
| **GA4** | Web analytics, Google ecosystem | ✓ | [ga4.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/ga4.md) |
| **Mixpanel** | Product analytics, event tracking | - | [mixpanel.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/mixpanel.md) |
| **Amplitude** | Product analytics, cohort analysis | - | [amplitude.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/amplitude.md) |
| **PostHog** | Open-source analytics, session replay | - | [posthog.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/posthog.md) |
| **Segment** | Customer data platform, routing | - | [segment.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/segment.md) |

---

## Related Skills

- **ab-testing**: For experiment tracking
- **seo-audit**: For organic traffic analysis
- **cro**: For conversion optimization (uses this data)
- **revops**: For pipeline metrics, CRM tracking, and revenue attribution

## Limitations

- Use this skill only when the task clearly matches its upstream source and local project context.
- Verify commands, generated code, dependencies, credentials, and external service behavior before applying changes.
- Do not treat examples as a substitute for environment-specific tests, security review, or user approval for destructive or costly actions.
