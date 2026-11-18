---
name: ux-laws
description: >-
  Use when sizing interactive targets, grouping elements on a screen, limiting
  choices, setting response-time targets, or making one element stand out.
  Covers Fitts's Law, Hick's Law, Miller's Law, the Doherty Threshold, the
  Gestalt laws of proximity and common region, and the Von Restorff effect.
type: capability
version: 1.0.0
---

# UX Laws

Seven well-established principles that govern how people perceive and act on an interface. Each
answers a different question, so use the one that matches the problem in front of you rather than
applying all of them at once.

## Which law applies

| Problem | Law |
|---|---|
| A target is hard to hit or reach | Fitts's Law |
| A decision takes too long, or a menu feels overwhelming | Hick's Law |
| A list or form is hard to scan and recall | Miller's Law |
| The interface feels sluggish or flow-breaking | Doherty Threshold |
| Elements don't read as related, or read as related when they aren't | Law of Proximity |
| A group needs an explicit boundary | Law of Common Region |
| Nothing on the screen draws the eye | Von Restorff Effect |

## Fitts's Law

**The time to acquire a target is a function of distance to the target and target size.**
`MT = a + b × log₂(2D / W)`

Large targets close to the pointer are fast to hit; small targets far away are slow and
error-prone. Size and proximity matter independently.

- Touch targets: **44×44pt** (Apple HIG) or **48×48dp** (Material) minimum. Pointer targets can be
  smaller but should stay generous — 24×24px at minimum.
- Target size is the **interactive area**, not the visual icon. A 16px icon can carry a 44px tap area.
- Screen edges and corners are effectively infinite targets — good for persistent navigation.
- Place actions near the content they act on. A card action belongs on the card.
- On mobile, bottom placement shortens reach for one-handed use.

**Does not cover:** cognitive cost (the time to decide what to tap), touch-vs-pointer accuracy
differences, or the accidental-activation risk of large gesture targets.

## Hick's Law

**Decision time increases logarithmically with the number of choices.** `RT = a + b × log₂(n + 1)`

Fewer simultaneous options speed decisions — but the goal is reducing *simultaneous* choices, not
removing functionality.

- Navigation: limit top-level items, group the rest.
- Toolbars: surface common actions, tuck the rest into overflow.
- Onboarding: one decision per step.
- Pricing: three tiers is the conventional sweet spot.
- Feeds and results: paginate rather than presenting the full count.

**Common mistakes:** conflating "fewer options" with "less functionality"; hiding options users
need frequently; ignoring choice quality — five clear options often beat three vague ones.

Group related options *before* reducing the count. Categorisation reduces apparent complexity more
than removal does.

## Miller's Law

**Working memory holds a limited number of meaningful chunks.** Miller's often-quoted "7 ± 2" has
been revised downward — Cowan (2001) puts the realistic limit nearer **4 ± 1** — and Miller's own
point was that the limit applies to **chunks**, not raw items.

Do not cite "7 items" as a design rule. Cite chunking as the strategy.

- Navigation: three groups of three or four beat a flat list of ten.
- Forms: break into sections that each feel completable as a unit.
- Codes and phone numbers: format as chunks (`555-867-5309`).
- Onboarding: show 3–5 named phases rather than "step 12 of 20".
- Feature lists: 3–5 bullets per tier.

Familiarity expands chunk size — expert users handle more than first-time users.

## Doherty Threshold

**A response under 400ms keeps people in flow.** Above it, they notice the wait and disengage.

| Response | Perception |
|---|---|
| 0–100ms | Instant |
| 100–300ms | Fast, perceptible |
| 300–400ms | Boundary — some notice |
| 400ms–1s | Slow — needs an indicator |
| 1s+ | Flow broken — needs progress |
| 10s+ | Task-level disruption |

When you cannot meet 400ms:

1. Acknowledge within **100ms** with a visual state change on the trigger.
2. Show a loading indicator if completion takes 400ms–3s.
3. Show **progress**, not just a spinner, beyond 3s.
4. Use optimistic UI — update immediately, reconcile when the response arrives.
5. Prefer **skeleton screens** over spinners where the layout is known; they preserve spatial context.

## Law of Proximity

**Elements close together are perceived as a group.** Whitespace separates; tightness implies
relationship.

- Label tighter to its input than to the next field.
- Section header closer to the content below it than to the section above.
- Related actions grouped; destructive actions separated.
- Row padding tighter than row gap.

What creates hierarchy is the **ratio** of within-group to between-group spacing — there is no fixed
pixel value. Apply the same spacing increments consistently so the relationships read at a glance.

## Law of Common Region

**Elements inside a shared boundary are perceived as a group**, even when not especially close.

| | Proximity | Common Region |
|---|---|---|
| Mechanism | Spatial closeness | Shared boundary or background |
| Best for | Items already close | Items needing an explicit boundary |
| Cost | Zero — just spacing | Visual weight — a border or surface |

Use proximity first. Add common region when proximity alone is insufficient, or when the group must
be actionable as a unit (a card, a form section, a modal).

**When containment backfires:** cards for everything flatten hierarchy; nested regions create noise
(limit to two levels); a border for its own sake is clutter when proximity already communicates the
grouping.

## Von Restorff Effect

**An item that differs from its surroundings is noticed and remembered.** Also called the isolation
effect.

The effect depends on **contrast with context**. If everything is differentiated, nothing is. It
only works when one or very few items deviate, the rest are visually consistent, and the deviation
is meaningful.

- One filled primary button; all others ghost or text.
- Highlight one recommended pricing tier; reduce the weight of the others.
- Active navigation state distinct from inactive.
- One key row emphasised in a table.

**Avoid:** highlighting multiple competing elements; decorative colour pops, which train users to
ignore them; relying on colour alone — pair with shape, size, or weight.

Decide in advance what the single most important element per screen is. Audit for "isolation
inflation", where every new feature requests highlight treatment and the system degrades.

## How they interact

- **Proximity and common region** are alternatives for the same job. Use one, or use both
  deliberately — not both by accident.
- **Von Restorff and visual hierarchy** overlap: emphasis is how hierarchy is expressed at the
  element level.
- **Hick and Miller** both reduce cognitive load, from different directions — fewer choices, and
  fewer chunks per choice.
- **Fitts and Doherty** are both about time, but motor time versus perceived latency. A fast
  interface with badly placed targets still feels slow.

## Review checklist

- Are touch targets at least 44×44pt, with the interactive area larger than the icon?
- Are related elements closer to each other than to unrelated ones?
- Is there at most one dominant action per screen region?
- Does every interaction acknowledge within 100ms?
- Are choices grouped before being reduced?
- Is any group using both proximity and a border without reason?
- Does the emphasis survive grayscale and colour-blindness simulation?