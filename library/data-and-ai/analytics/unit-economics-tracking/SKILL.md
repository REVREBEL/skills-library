---
name: "unit-economics-tracking"
description: "Track customer acquisition cost, lifetime value, payback period, and contribution margin by cohort and channel with profitability benchmarks and trend analysis. Use when working with unit economics tracking."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Unit Economics Tracking

## Overview

Unit economics describes the financial dynamics of a single customer. The four key metrics — Customer Acquisition Cost (CAC), Customer Lifetime Value (LTV), the LTV:CAC ratio, and payback period — tell you whether your business model is economically viable. These metrics are among the most scrutinized by investors and boards because they reveal the underlying health of the business independent of short-term revenue trends.

This skill guides you through calculating and tracking these metrics using your platform's analytics tools and dedicated customer analytics apps.

## When to Use This Skill

- When preparing investor materials and needing to present unit economics metrics
- When understanding whether it is profitable to increase marketing spend in a given channel
- When analyzing why CAC has increased over the past 6 months
- When comparing the quality of customers acquired through different channels
- When building a financial model and needing to validate LTV assumptions
- When setting budget guardrails: maximum allowable CAC by channel
- When evaluating a new acquisition channel and projecting its payback period

## Core Instructions

### Step 1: Choose your unit economics tracking tool by platform

| Platform | Tool | What It Provides |
|----------|------|-----------------|
| **Shopify** | **Lifetimely** (App Store) | CAC by channel, cohort LTV curves, payback period, predicted CLV per customer |
| **Shopify** | **Triple Whale** (App Store) | New customer CAC by channel, blended CAC, LTV vs. CAC ratio |
| **Shopify** | **Polar Analytics** (App Store) | CAC tracking with channel breakdown, MER, and LTV trending |
| **WooCommerce** | **Metorik** | Customer cohort analysis, repeat purchase rate, LTV by acquisition channel |
| **BigCommerce** | **Glew.io** (App Marketplace) | Customer cohort retention, CLV by segment, repeat purchase analysis |
| **All platforms** | **Google Analytics 4** | Acquisition channel reporting; pair with cost data from ad platforms for CAC calculation |

### Step 2: Calculate Customer Acquisition Cost (CAC)

CAC is the total marketing and sales spend required to acquire one new customer.

**Types of CAC:**

| CAC Type | Formula | When to Use |
|----------|---------|------------|
| **Blended CAC** | Total marketing spend / Total new customers acquired | Overall efficiency trend; monthly reporting |
| **Paid CAC** | Total paid media spend / New customers from paid channels only | Channel budget decisions |
| **Fully-loaded CAC** | Total marketing spend + agency fees + marketing tech + team salaries / New customers | Investor presentations; true economic cost |

**Getting CAC data by platform:**

**Shopify with Lifetimely:**
1. Install **Lifetimely** from the Shopify App Store
2. Connect ad accounts (Meta, Google, TikTok) under **Integrations**
3. Go to **Lifetimely → Channels** — view CAC by acquisition channel with trend over time
4. Lifetimely tracks "new customers" based on first Shopify order date and attributes them to their first-touch UTM source

**Shopify with Triple Whale:**
1. Install **Triple Whale** and connect ad accounts
2. Go to **Triple Whale → Summary Dashboard** — "New Customer CAC" tile shows blended new customer acquisition cost
3. Go to **Triple Whale → Attribution → New Customer Revenue** for CAC by channel

**Manual CAC calculation (any platform):**
1. Export: Monthly marketing spend by channel (from your ad platforms or agency reports)
2. Export: New customer count by acquisition channel and month (from your platform's analytics: Shopify Analytics → New vs. returning customers; Metorik → Customers → First order date)
3. Calculate: CAC by channel = Channel spend / New customers attributed to that channel

**Typical CAC benchmarks by channel:**
- Google Shopping / Search: $15–$50 (lower for branded, higher for competitive non-branded)
- Meta (Facebook/Instagram): $20–$80 for DTC
- TikTok: $10–$40 (often lower for discovery-driven products)
- Influencer marketing: $15–$60 (highly variable)
- Email/SMS (acquisition via lead gen): $5–$20

### Step 3: Calculate Customer Lifetime Value (LTV)

LTV is the total net revenue (or contribution margin) you expect from a customer over their relationship with your business.

**Historical (observed) LTV:**
Pull this from your analytics tool directly.

**Shopify + Lifetimely:**
1. Go to **Lifetimely → Cohorts** — see a cohort table showing cumulative revenue per customer at 1, 3, 6, 12, 18, 24 months after acquisition
2. The month-12 and month-24 rows represent your observed LTV at those time horizons
3. Go to **Lifetimely → Predicted CLV** — Lifetimely's model predicts 12-month and 24-month CLV per customer based on their early purchase behavior

**WooCommerce + Metorik:**
1. Go to **Metorik → Reports → Customer Cohorts** — cohort retention table with cumulative revenue per customer by months since acquisition
2. Go to **Metorik → Customers → Filter by: First order date range** — view average revenue per customer for any acquisition cohort

**Predicted LTV formula (for planning models):**

When you do not have 12+ months of cohort data, use this simplified formula:
```
LTV = (Average Order Value × Purchase Frequency per Year × Gross Margin %) / Annual Churn Rate

Example:
  AOV: $65
  Purchase Frequency: 2.5 orders/year
  Gross Margin: 55%
  Annual Churn Rate: 40%

LTV = ($65 × 2.5 × 0.55) / 0.40 = $89.375 / 0.40 = $223.44
```

This formula gives steady-state LTV. It assumes stable purchase behavior, which is a simplification — cohort-based analysis is more accurate when you have the data.

### Step 4: Calculate LTV:CAC ratio and payback period

**LTV:CAC ratio:**

```
LTV:CAC = LTV / CAC

Benchmarks:
  2:1 = Minimum viable (barely profitable customer acquisition)
  3:1 = Healthy for DTC ecommerce
  5:1+ = Excellent; strong case for scaling marketing spend
```

| LTV:CAC | Assessment | Action |
|---------|-----------|--------|
| < 2:1 | Unprofitable | Stop scaling paid acquisition; improve retention or reduce costs |
| 2:1 – 3:1 | Marginal | Monitor closely; improve one driver (AOV, repeat rate, or CAC) before scaling |
| 3:1 – 5:1 | Healthy | Good baseline; evaluate where to scale |
| 5:1+ | Excellent | Prioritize scaling this channel or business |

**Payback period:**

Payback period = CAC / (Monthly Contribution per Customer)

```
Example:
  CAC: $60
  AOV: $65
  Purchase Frequency: 2.5 orders/year → 0.21 orders/month
  Gross Margin: 55%
  Fulfillment + other variable costs: 15%
  Contribution margin rate: 40%

Monthly contribution per customer = $65 × 0.21 × 0.40 = $5.46
Payback period = $60 / $5.46 = 11 months
```

**Payback benchmarks:**
- <6 months: Excellent; very capital-efficient growth
- 6–12 months: Healthy
- 12–24 months: Acceptable if retention is strong past month 24
- 24+ months: Problematic unless you have significant venture/debt capital to bridge

### Step 5: Track unit economics by acquisition channel

The most important dimension for unit economics is acquisition channel — customers from different sources often have dramatically different LTVs, repeat purchase rates, and initial AOVs.

**Using Lifetimely (Shopify) to compare channels:**
1. Go to **Lifetimely → Channels** — select "LTV comparison by channel"
2. View 12-month and 24-month LTV by first-touch acquisition source
3. Pair with CAC by channel (from ad platform spend) to calculate LTV:CAC by channel

**Channel LTV comparison template:**

| Channel | CAC | Month-12 LTV | LTV:CAC | Payback (months) | Assessment |
|---------|-----|-------------|---------|-----------------|-----------|
| Google Shopping | $35 | $180 | 5.1:1 | 4 | Excellent; scale |
| Meta Prospecting | $62 | $145 | 2.3:1 | 13 | Marginal; optimize creatives |
| TikTok | $28 | $95 | 3.4:1 | 9 | Healthy; test scaling |
| Influencer | $45 | $210 | 4.7:1 | 6 | Excellent; invest more |
| Organic/SEO | $0 | $165 | ∞ | 0 | Free acquisition; protect this channel |

**Key insight from this type of analysis:** Meta Prospecting appears to have a high ROAS in Meta's dashboard but has the worst LTV:CAC because those customers have lower repeat purchase rates. This is the power of LTV-based analysis over single-order ROAS.

### Step 6: Monitor CAC trends weekly

Rising CAC is the first warning sign of channel saturation or increased competition. Monitor it weekly:

1. Set up a **CAC alert** in Triple Whale or Polar Analytics: alert when weekly new customer CAC exceeds your maximum allowable CAC by channel
2. Your **maximum allowable CAC** = LTV / Target LTV:CAC ratio
   - Example: If LTV = $180 and target LTV:CAC = 3.0, max CAC = $60
3. Any channel where CAC exceeds the maximum allowable CAC should be reviewed before the next weekly budget cycle

## Best Practices

- **Use contribution margin LTV, not gross revenue LTV** — LTV calculated on revenue overstates actual customer value; use contribution margin (after COGS, fulfillment, and variable costs) for a realistic economic picture
- **Segment LTV by acquisition channel from day one** — customers from organic search, paid social, and influencer partnerships often have dramatically different LTVs; pooling them into a blended LTV obscures channel economics
- **Track LTV curves, not just point estimates** — plot cumulative gross profit per customer over 24 months for each cohort; comparing curves across cohorts reveals whether recent cohorts are better or worse than historical averages
- **Set maximum CAC guardrails for each channel** — derive Max CAC = LTV / Target LTV:CAC ratio; use this as a hard budget guardrail so marketing teams cannot overpay for customers without executive approval
- **Validate LTV predictions against cohort actuals** — every 6 months, compare LTV predictions against the actual cumulative gross profit of cohorts that are now old enough to measure; recalibrate if predictions are consistently off
- **Account for reactivation costs in long-tail LTV** — customers who lapse and return via win-back campaigns have reactivation costs (discounts, extra email volume) that should reduce the apparent value of long-tail behavior

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| Using only media spend to calculate CAC | True CAC includes agency fees, marketing technology (email platforms, analytics apps), marketing team salaries, and first-order discounts; using media-only CAC understates true CAC by 20–50% |
| Using ARPU (average revenue per user) instead of contribution margin for LTV | LTV in revenue terms overstates economic value; always use average contribution margin per customer per period |
| Ignoring cohort degradation | Newer cohorts often have worse retention than earlier cohorts as you move from early adopters to broader audiences; always compare cohort curves against each other rather than assuming all cohorts are equal |
| Confusing blended CAC with channel-level CAC | Blended CAC mixes organic (free) and paid customers; since organic customers cost nothing to acquire, blending them flatters paid CAC; use paid CAC by channel for budget decisions |
| Presenting LTV with too-long forecasts when business is young | If your business has 18 months of data, a 36-month LTV is highly speculative; be transparent about what portion of LTV is observed vs. modeled extrapolation |

## Related Skills

- @customer-analytics
- @attribution-modeling
- @marketing-spend-analysis
- @financial-analytics-dashboard
- @ecommerce-budgeting-forecasting

---

# Merged from customer-analytics

> Folded in from the former standalone skill of the same capability. Kept as a section so nothing is lost; remove it once the guidance is fully absorbed.

# Customer Analytics

## Overview

Customer analytics transforms raw order data into actionable insights about purchase patterns, lifecycle stages, and churn risk. The core analyses — RFM scoring, cohort retention, purchase frequency, and churn prediction — reveal which customers are loyal, which are at risk, and which channels produce the best long-term customers.

This skill guides you through running these analyses using your platform's built-in tools and dedicated analytics apps, with data warehouse approaches for stores that need deeper segmentation.

## When to Use This Skill

- When the marketing team needs data-driven segments beyond simple demographic filters
- When calculating at-risk customer counts for quarterly business reviews
- When measuring the impact of loyalty programs on purchase frequency
- When identifying the acquisition channels that produce the highest-LTV customers
- When preparing customer health dashboards for account management or VIP programs
- When building cohort retention analysis to understand customer lifetime value trends

## Core Instructions

### Step 1: Choose the right tool for your platform

| Platform | Recommended Tool | What It Provides |
|----------|-----------------|-----------------|
| **Shopify** | **Klaviyo** + Shopify's built-in customer segments | RFM-style segments, purchase frequency, CLV prediction, cohort reports |
| **Shopify** (advanced) | **Lifetimely** or **Triple Whale** | True cohort LTV, CLV by acquisition channel, retention curves |
| **WooCommerce** | **Metorik** | Customer segmentation, RFM analysis, cohort retention, churn identification |
| **WooCommerce** (email) | **Klaviyo** for WooCommerce | Behavioral segments + automated flows based on customer lifecycle stage |
| **BigCommerce** | **Klaviyo** for BigCommerce + **Glew.io** | Glew provides cohort analysis and CLV tracking natively for BigCommerce |
| **All platforms** (data-first) | Export to **Google Looker Studio** + **BigQuery** via Fivetran | Full SQL-based analysis; required for advanced RFM and cohort modeling |

### Step 2: Set up customer segmentation on your platform

---

#### Shopify

**Using Shopify's built-in customer segments (all plans):**

1. Go to **Customers → Segments**
2. Shopify provides pre-built segments including:
   - **Abandoned checkout in the last 30 days**
   - **Customers who have purchased more than X times**
   - **Customers who haven't purchased in 90 days** (at-risk segment)
   - **High-spend customers** (based on total spend threshold)
3. Create custom segments using the query editor with filters like:
   - `number_of_orders >= 3` (loyal customers)
   - `days_since_last_order > 90` (churn risk)
   - `total_spent > 500` (high-value)
4. Export segments to CSV or sync directly to Klaviyo for email campaigns

**Using Klaviyo for RFM segmentation on Shopify:**

1. Install **Klaviyo** from the Shopify App Store
2. Klaviyo automatically syncs all historical and new Shopify order data
3. Go to **Segments → Create Segment** and build RFM-style segments using:
   - **Recency:** "Has placed an order in the last X days"
   - **Frequency:** "Number of orders is greater than X"
   - **Monetary:** "Total amount spent is greater than $X"
4. Pre-built segment examples:
   - **Champions:** Ordered in last 30 days + 3+ orders + $200+ lifetime spend
   - **At Risk:** No order in 90–180 days + previously placed 2+ orders
   - **Lost:** No order in 180+ days
5. Use these segments to trigger flows in Klaviyo: win-back campaigns for at-risk, VIP rewards for champions

**Using Lifetimely for cohort LTV on Shopify:**

1. Install **Lifetimely** from the Shopify App Store
2. Go to **Lifetimely → Cohorts** to see a month-by-month retention matrix: what percentage of customers from each acquisition cohort are still buying at months 1, 3, 6, 12
3. Go to **Lifetimely → Channels** to compare 12-month LTV by acquisition source (Google, Meta, organic, email)
4. Go to **Lifetimely → Customer Segments** to see RFM distribution and predicted CLV per customer

---

#### WooCommerce

**Using Metorik:**

1. Connect Metorik to your WooCommerce store via API
2. Go to **Metorik → Customers** to browse all customers with filters:
   - Last order date (identify churned/at-risk)
   - Total spent (identify high-value)
   - Order count (identify one-time vs. repeat buyers)
3. Go to **Metorik → Reports → Customer Cohorts** to see retention by monthly acquisition cohort
4. Go to **Metorik → Segments** to create saved customer segments (equivalent to RFM groups); export segments as CSVs for Klaviyo or Mailchimp

**Using Klaviyo for WooCommerce:**

1. Install the **Klaviyo for WooCommerce** plugin
2. Klaviyo syncs WooCommerce customers and orders, enabling the same RFM segments described for Shopify above
3. Go to **Klaviyo → Analytics → Cohort Analysis** to see retention curves and predicted CLV by acquisition date

---

#### BigCommerce

1. **BigCommerce Customer Groups:** Go to **Customers → Customer Groups** — create groups based on purchase history, spend thresholds, and geographic criteria
2. Install **Glew.io** from the BigCommerce App Marketplace — provides cohort retention analysis, RFM scoring, and CLV by acquisition channel
3. Install **Klaviyo** for BigCommerce for behavioral email segmentation and lifecycle automation

---

### Step 3: Analyze purchase frequency and retention

**Purchase frequency distribution (using any platform's export):**

Export your customer order data to a CSV or Google Sheet and calculate:
- What % of customers have placed exactly 1 order?
- What % have placed 2–3 orders?
- What % have placed 4+ orders?

Industry benchmarks:
- Typical DTC brand: 60–70% of customers are one-time buyers
- Healthy subscription or consumable brand: 40–50% of customers reorder within 90 days
- Your second-purchase rate (% of first-time buyers who place a second order within 90 days) is the single most important leading indicator of long-term CLV

**Cohort retention analysis:**

A cohort retention grid shows what percentage of customers acquired in month X are still buying at months 1, 3, 6, 12:

- **Shopify + Lifetimely:** Available natively in the **Cohorts** view
- **Klaviyo:** Available under **Analytics → Cohort Analysis**
- **Metorik:** Available under **Reports → Cohorts**
- **Manual (any platform):** Export all orders to Google Sheets; create a pivot table with acquisition month as rows and "months since first order" as columns

**What good retention looks like:**
| Months After First Order | Minimum Viable | Healthy | Excellent |
|--------------------------|---------------|---------|-----------|
| Month 1 (second purchase rate) | 15% | 25% | 40%+ |
| Month 3 retention | 10% | 20% | 35%+ |
| Month 12 retention | 5% | 15% | 30%+ |

### Step 4: Identify at-risk customers and act

**At-risk customer identification:**

The simplest at-risk definition: customers who previously ordered multiple times but have not ordered in longer than their typical interval.

- **Shopify Segments:** `number_of_orders > 1 AND days_since_last_order > 90`
- **Klaviyo:** Create a "Winback" segment: "Has placed more than 1 order" AND "Has not placed an order in the last 90 days"
- **Metorik:** Use the "Customers at risk of churning" pre-built filter

**Action by segment:**

| Segment | Recommended Action |
|---------|-------------------|
| Champions (recent, frequent, high-spend) | Invite to VIP program; early access to new products |
| Loyal but cooling (frequent but not recent) | Targeted win-back email with personalized product recommendations |
| At risk (inactive > 90 days, multiple prior orders) | Win-back sequence: reminder → small incentive → final offer |
| One-time buyers | Second purchase campaign; show complementary products |
| Lost (inactive > 180 days) | Low-cost re-engagement attempt; if no response, suppress to reduce email costs |

## Best Practices

- **Run RFM scoring monthly** — customer order history changes continuously; stale segments lead to wrong targeting
- **Track second-purchase rate as a leading indicator** — the conversion from one-time to repeat buyer is the highest-leverage retention metric; it predicts CLV far in advance of any LTV model
- **Segment CLV by acquisition channel** — customers from organic search, paid social, and email/SMS referrals often have dramatically different LTVs; measure them separately to inform budget allocation
- **Build alerts for segment migration** — when the "at risk" segment grows week over week, it signals a retention problem needing immediate action; set up alerts in Klaviyo or Lifetimely
- **Flag seasonal buyers separately** — customers who only buy in Q4 should not be marked as churned in Q2; apply a seasonal buyer tag before running churn analysis

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| RFM segments shift dramatically after a sale event | Use a rolling 90-day window for scoring; recent sales spikes should not permanently elevate scores for customers who only responded to a discount |
| Acquisition channel CLV analysis not accounting for multi-touch | Use first-touch attribution for CLV by channel — the channel that introduced the customer, not the channel that converted the last order |
| Cohort retention shows 0% after month 6 | Check whether the query or export is filtering out cohorts that do not have 6 months of data yet; exclude cohorts acquired in the last 6 months from long-term retention views |
| Customer count in segments does not match email list size | Some customers in your store may not be subscribed to email; segment by customer (order-based) separately from email list (consent-based) |
| Win-back campaigns going to customers who bought recently | Ensure segment filters are current — sync order data before running segment exports; stale data causes emails to go to wrong contacts |

## Related Skills

- @customer-segmentation
- @attribution-modeling
- @sales-reporting-dashboard
- @ab-testing-ecommerce
- @unit-economics-tracking
