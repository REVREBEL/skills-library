---
name: "lifecycle-marketing-automation"
description: "Map customer journey stages from first visit to loyal advocate with personalized messaging, triggered workflows, and segment-based campaign automation. Use when working with lifecycle marketing automation."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Lifecycle Marketing Automation

## Overview

Lifecycle marketing treats each customer as being at a defined stage in their relationship with your brand — from anonymous visitor to loyal advocate — and delivers stage-appropriate messaging automatically. Unlike broadcast campaigns, lifecycle automation is triggered by behavior and stage transitions, ensuring every message is relevant. Klaviyo's predictive analytics and flow builder cover most lifecycle automation needs without custom code.

## When to Use This Skill

- When moving from batch-and-blast campaigns to behavior-triggered messaging
- When different customer segments are receiving identical generic emails
- When onboarding new customers and needing a structured first-30-day nurture plan
- When LTV and repeat purchase rate are flat despite healthy acquisition numbers
- When building a holistic view of the customer journey across email, SMS, and push

## Core Instructions

### Step 1: Define your lifecycle stages

| Stage | Definition | Primary Goal |
|-------|-----------|-------------|
| **Subscriber** | Email captured, no purchase | Convert to first purchase |
| **First-time buyer** | 1 order, placed < 60 days ago | Onboard, reduce returns, build habit |
| **Active** | 2+ orders, purchased within repurchase window | Grow AOV and purchase frequency |
| **Loyal** | 4+ orders OR > $500 LTV | Maintain, protect from churn, reward |
| **At-risk** | Approaching 1.5x their normal repurchase window | Proactive re-engagement |
| **Lapsed** | Beyond 2x their normal repurchase window | Win-back campaign |
| **Advocate** | Has reviewed, referred, or engaged heavily | Amplify via referral program |

### Step 2: Set up lifecycle automation per stage

---

#### Shopify with Klaviyo

Klaviyo computes expected repurchase dates and churn risk automatically based on your order history — you do not need to calculate lifecycle stages manually.

**Subscriber stage — Welcome Series:**
1. Go to **Klaviyo → Flows → Create Flow → Welcome Series** (use template)
2. The flow fires when someone joins your email list
3. Configure 3 emails over 7 days:
   - Email 1 (immediate): Welcome + brand story + first-order discount
   - Email 2 (day 2): Bestsellers or "Start here" product guide
   - Email 3 (day 7): Social proof (reviews, customer photos, media mentions)
4. Add a **flow filter**: "Has NOT placed an order" — exits the flow if they purchase before completing it

**First-time buyer stage — Post-Purchase Onboarding:**
1. Create a new flow: trigger = **Placed Order**, filter = "First order ever" (Klaviyo's "First order" conditional)
2. Configure 3 emails:
   - Email 1 (day 2): Product usage tips or setup guide
   - Email 2 (day 7): Cross-sell recommendations based on purchased product
   - Email 3 (day 21): Review request
3. This flow is separate from the standard post-purchase flow to give first-timers extra attention

**Loyal stage — VIP Recognition:**
1. Create a segment: `Total Customer Value > $500` OR `Total Order Count >= 4`
2. Create a flow triggered by **Segment Entry** for this segment
3. Send a single "You've unlocked VIP status" email with exclusive benefits (early access, free shipping, loyalty points bonus)
4. Add these customers to a **Klaviyo List** called "VIP" and use it as a segment for early access campaigns

**At-risk stage — Retention Nudge:**
1. Create a segment using Klaviyo's predictive analytics: `Predicted Churn Risk = High OR Mid`
2. Create a flow triggered by **Segment Entry**:
   - Email 1 (immediate): Personalized "We miss you" with product recommendations based on past purchases
   - Wait 5 days → Email 2: New arrivals or "What's changed since your last visit"
   - Wait 5 days → Email 3 (only for customers with > $200 LTV): 15% off exclusive offer

**Lapsed stage → Win-Back:**
- See @win-back-reactivation for the full win-back campaign setup

---

#### WooCommerce with AutomateWoo

1. Install **AutomateWoo** ($99/yr) from the WooCommerce marketplace
2. Build individual workflows for each stage transition:

**Welcome Series:**
- Trigger: **Subscribe → Newsletter** (with your email plugin) or **Customer → Created** (new account)
- Add 3 email actions with timing delays

**Post-purchase onboarding:**
- Trigger: **Order → Status Changed to Completed**
- Add condition: **Customer order count equals 1** (first-time buyer)
- Configure email sequence with delays

**At-risk re-engagement:**
- Trigger: **Customer → Win Back** (built-in AutomateWoo trigger)
- Set "No order in last" to 1.5x your average repurchase cycle
- Create escalating emails: reminder → offer

AutomateWoo's built-in **RFM Analysis** (go to **AutomateWoo → Reports → RFM Analysis**) shows your customers on an RFM grid — use this to identify which customers to target with each lifecycle stage campaign.

---

#### BigCommerce

1. Install **Klaviyo** from the BigCommerce App Marketplace
2. Klaviyo syncs all BigCommerce order history automatically
3. Follow the same Klaviyo flow setup as the Shopify section above

---

#### Custom / Headless

Send lifecycle events to Klaviyo's API:

```typescript
// Update customer's lifecycle stage as a Klaviyo profile property
async function updateLifecycleStage(email: string, stage: string) {
  await fetch('https://a.klaviyo.com/api/profile-import/', {
    method: 'POST',
    headers: {
      'Authorization': `Klaviyo-API-Key ${process.env.KLAVIYO_PRIVATE_KEY}`,
      'Content-Type': 'application/json',
      'revision': '2024-10-15',
    },
    body: JSON.stringify({
      data: {
        type: 'profile',
        attributes: {
          email,
          properties: {
            lifecycle_stage: stage,
            lifecycle_stage_updated_at: new Date().toISOString(),
          },
        },
      },
    }),
  });
}

// Call this on key events:
// After first purchase: updateLifecycleStage(email, 'first-time-buyer')
// After 4th purchase or $500 LTV: updateLifecycleStage(email, 'loyal')
// When churn risk detected: updateLifecycleStage(email, 'at-risk')
```

Then in Klaviyo, create flows triggered by **Profile Property Changed → lifecycle_stage equals [stage]**.

### Step 3: Configure stage-appropriate messaging

| Stage | Channel | Frequency | Content Focus | Incentive |
|-------|---------|-----------|--------------|-----------|
| Subscriber | Email | Weekly | Brand education, social proof | First-order discount |
| First-time buyer | Email | Triggered only | Product onboarding, care tips | No discount — build value |
| Active | Email | Biweekly | New arrivals, cross-sell | None (they are buying) |
| Loyal | Email | Weekly | Exclusive access, new drops | Early access, not discounts |
| At-risk | Email + SMS | Triggered only | Re-engagement, recommendations | Small offer for high-LTV only |
| Advocate | Email | Biweekly | Referral program, exclusives | Referral bonuses |

### Step 4: Measure lifecycle health

Track these in Klaviyo or your analytics dashboard:

| Metric | Target | Where to Find |
|--------|--------|---------------|
| Subscriber → first purchase conversion | > 10% within 30 days | Klaviyo → Welcome series flow analytics |
| First-time buyer repeat purchase rate | > 30% within 90 days | Shopify: Analytics → Customer cohorts |
| At-risk customers saved | > 20% convert after retention flow | Klaviyo → Segment size change over time |
| Loyal customer share of revenue | > 40% of total revenue | Klaviyo → VIP segment campaign analytics |

## Best Practices

- **Cancel competing flows on conversion** — in Klaviyo, add a flow filter to every win-back and retention flow: "Has placed order since starting flow → exit"; prevents irrelevant messages after purchase
- **Always cancel retention flows when a customer purchases** — set up a Klaviyo flow that triggers on "Placed Order" and uses a Trigger Split to exit the person from any active retention flows
- **Use Klaviyo's predictive analytics** — do not manually calculate lifecycle stages; Klaviyo's expected next purchase date and churn risk are more accurate than manual rules
- **Personalize with dynamic product blocks** — every retention and win-back email should show products based on what the customer has bought before, not generic bestsellers
- **Keep stage definitions simple** — 5–7 stages is enough; adding more stages creates messaging overlap and complexity without proportional benefit

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| Customers receive win-back email after just buying | Add flow filter "Has placed order in last 7 days → exit" and verify the Placed Order event is firing in Klaviyo |
| All customers stuck in "subscriber" stage | Check that Placed Order events are syncing from Shopify to Klaviyo; verify integration is active under Klaviyo → Integrations |
| Loyal customers receiving lapsed messaging | Segment filters in Klaviyo run at entry time; add re-evaluation by using **Flow Filters** that check current lifetime value before each send |
| Welcome series and post-purchase flow both send to new buyers | Add a flow filter to the Welcome Series: "Has NOT placed an order" — this exits them from Welcome when they buy |

## Related Skills

- @customer-retention-engine
- @email-marketing-automation
- @win-back-reactivation
- @loyalty-program-optimization
- @email-list-segmentation

---

# Merged from email-list-segmentation

> Folded in from the former standalone skill of the same capability. Kept as a section so nothing is lost; remove it once the guidance is fully absorbed.

# Email List Segmentation

## Overview

Sending the same email to your entire list is one of the most expensive mistakes in ecommerce marketing. ISPs throttle senders with low engagement, unsubscribe rates spike for irrelevant content, and you leave revenue on the table by treating a VIP customer identically to someone who has never purchased. Klaviyo (for Shopify/BigCommerce) and AutomateWoo or Mailchimp (for WooCommerce) include RFM and behavioral segmentation built-in — no custom code needed for most stores.

## When to Use This Skill

- When email open rates drop below 20% and you suspect low engagement dragging deliverability
- When migrating from blast-and-pray sends to targeted campaign logic
- When building a suppression system to protect high-value subscribers from over-messaging
- When launching a win-back program and need to identify the "at-risk" vs. "lapsed" cohort
- When analyzing email revenue and needing to attribute performance to specific segments

## Core Instructions

### Step 1: Choose the right segmentation tool

| Platform | Recommended Tool | Built-in Segmentation Capabilities |
|----------|-----------------|-------------------------------------|
| **Shopify** | Klaviyo | Predictive CLV, churn risk, RFM scoring, purchase behavior segments — all built-in |
| **WooCommerce** | Klaviyo (via plugin) or AutomateWoo | Klaviyo plugin syncs order data; AutomateWoo has native WooCommerce RFM reports |
| **BigCommerce** | Klaviyo | Native BigCommerce integration with full order history sync |
| **All platforms** | Klaviyo (via API) | Use Klaviyo's Track/Identify API to send behavioral events from any platform |

### Step 2: Set up the essential segments — start with five

Build these five segments first. They cover 80% of the value. Add more only when you have campaigns ready for each.

---

#### Klaviyo (Shopify, BigCommerce, or API-connected)

**Segment 1: Champions (VIP buyers)**
1. Go to **Klaviyo → Segments → Create Segment**
2. Conditions:
   - `Has placed order` at least 5 times ever
   - AND `Total Customer Value` greater than $500
   - AND `Opened email` in the last 60 days
3. Save as "Champions — VIP Buyers"

**Segment 2: Active buyers (engaged, not yet VIP)**
1. Create segment with conditions:
   - `Has placed order` at least 2 times ever
   - AND `Has placed order in the last 90 days`
2. Save as "Active Buyers"

**Segment 3: At-risk (used to buy, now quiet)**
1. Create segment using Klaviyo's predictive analytics:
   - `Predicted Churn Risk` equals `High`
   - AND `Has placed order` at least 1 time ever
2. Save as "At-Risk Customers"

**Segment 4: Email-engaged non-buyers**
1. Create segment with conditions:
   - `Has placed 0 orders`
   - AND `Opened email` in the last 30 days
2. Save as "Engaged Subscribers — No Purchase"

**Segment 5: Unengaged (to suppress)**
1. Create segment with conditions:
   - `Has NOT opened email` in the last 180 days
   - AND `Has NOT clicked email` in the last 180 days
   - AND `Email subscription status` is `Subscribed`
2. Save as "Unengaged — Suppression List"

**Suppress the unengaged segment before every campaign send:**
- When creating a campaign in Klaviyo, under **Excluded Segments**, add "Unengaged — Suppression List"
- This protects deliverability by not sending to cold contacts who will mark you as spam

---

#### WooCommerce with Mailchimp or Klaviyo

**Mailchimp:**
1. Go to **Mailchimp → Audience → Segments → Create Segment**
2. Mailchimp's ecommerce segments require the WooCommerce + Mailchimp plugin for purchase data sync
3. Common conditions: "Purchased" / "Has not purchased" / "Total spent is greater than" / "Last purchase was more than 90 days ago"

**AutomateWoo (for WooCommerce automation, not campaigns):**
1. Go to **AutomateWoo → Reports → RFM Analysis** to view your customers plotted on an RFM grid
2. Export customer lists from each RFM quadrant and import into your ESP for targeted campaigns

---

#### WooCommerce with Klaviyo plugin

1. Install the Klaviyo plugin from the WordPress plugin directory
2. In Klaviyo, all WooCommerce orders and customers sync automatically
3. Follow the same segment setup as the Shopify/Klaviyo instructions above

---

### Step 3: Set up behavioral segments for campaign targeting

Beyond RFM, create segments that map to specific campaigns:

**Sale shoppers** (always use discounts — suppress from full-price launches):
- Klaviyo condition: `Has used a discount code` more than 2 times ever

**High AOV customers** (show premium products):
- Klaviyo condition: `Average Order Value` greater than $150

**Category-specific buyers** (for product launches):
- Klaviyo condition: `Ordered product in category` = "Skincare" (use your Shopify product type or Klaviyo collection data)

**Recently subscribed non-buyers** (in welcome flow):
- Klaviyo condition: `Subscribed to email` in the last 30 days AND `Has placed 0 orders`

### Step 4: Apply segments to campaigns

In Klaviyo, when creating a campaign:
1. Under **Recipient Selection**, choose your target segment (e.g., "Active Buyers")
2. Under **Excluded Segments**, always add "Unengaged — Suppression List"
3. Preview the segment size before sending — avoid sending to segments under 200 contacts (can trigger spam filters on some providers)

**Frequency rules by segment:**
- Champions: max 2 emails/week (they are engaged; maintain relationship but don't over-message)
- Active Buyers: 1–2 emails/week
- At-Risk: 1 email/week (retention focus)
- Engaged Subscribers (no purchase): 1–2 emails/week (nurture toward first purchase)

### Step 5: List hygiene — run quarterly

1. In Klaviyo, go to **Segments → [Unengaged list]** and check the size
2. If unengaged segment exceeds 20% of your total list, run a sunset campaign:
   - Send one final email: "We've noticed you haven't engaged lately — still want to hear from us?"
   - Wait 7 days
   - Suppress anyone who did not open the sunset email
3. Never delete unsubscribed contacts — suppress them. Klaviyo retains the unsubscribe signal to prevent accidental re-subscription.

## Best Practices

- **Start with 5 segments, not 50** — champion, active, at-risk, engaged non-buyer, unengaged is enough to see 80% of the benefit
- **Suppress before you send** — always build a suppression list (unengaged + unsubscribed) and apply it to every campaign
- **Protect champions** — never include your champions segment in sales/discount campaigns unless you want to train VIPs to wait for promotions
- **Engagement tier beats purchase history for deliverability** — for inbox placement, behavioral engagement signals matter more than how much someone has spent
- **Process unsubscribes immediately** — Klaviyo handles this automatically via webhooks; ensure your ESP is connected to your platform's unsubscribe events
- **GDPR**: for EU contacts, track consent separately and never rely on legitimate interest for marketing emails — require explicit opt-in

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| Open rates drop after adding segmentation | Ensure segments are correctly excluding unsubscribed contacts; check Klaviyo's suppression list under Audience → Suppressions |
| Klaviyo lists go out of sync with Shopify | Confirm the Klaviyo–Shopify integration is connected under Klaviyo → Integrations → Shopify; enable "Sync historical data" |
| Champions segment shrinks after every send | You are emailing them too frequently — apply Klaviyo's Smart Sending limit (once every 16 hours per person) |
| GDPR violations from imported list | Validate lawful basis for all contacts before import; only import contacts who have explicitly opted in |
| Segments overlap and contacts receive duplicate emails | In Klaviyo, use "Send to unique recipients" option and check for segment overlap before sending |

## Related Skills

- @email-marketing-automation
- @win-back-reactivation
- @lifecycle-marketing-automation
- @customer-retention-engine
- @first-party-data-collection
