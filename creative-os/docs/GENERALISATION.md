# How to make it general

**Companion to:** `ERROR-REGISTER.md` (the concrete evidence log)
**Machine-readable:** `failure-classes.json` · **Enforced by:** `lint_rules.py`

---

## The problem you spotted

`ERROR-REGISTER.md` says *"never write `#2D5BFF`, never say matte navy bottle, keep the bottom 200 px clean."*
Pasted into a playbook, that teaches the next agent about **one bottle campaign**. Give it a perfume,
a sneaker or a SaaS dashboard and every clause is either meaningless or actively wrong.

A rule earns its place only if it is **still true when the product, the palette and the platform change**.

---

## The test

> **Can this sentence be true for a completely different brand, product and format?**
>
> If yes → it is a **rule**. It goes in the playbook.
> If no → it is an **instance**. It goes in the campaign folder.

Run it on the findings:

| Written as an instance | Survives the test? | Why |
|---|---|---|
| "Never paste the bottle PNG" | ✗ | says *bottle* — next campaign has no bottle |
| "No pipeline operation may composite the artwork of a locked entity" | ✓ | holds for any entity in any category |
| "Keep the bottom 200 px clear for the swipe chip" | ✗ | 200 is this layout's number |
| "Generated content may not enter the union of chrome boxes + halo" | ✓ | the number comes from the component registry |
| "Don't use #2D5BFF as a frame" | ✗ | one brand's blue |
| "A constraint named as a boundary will be rendered as artwork" | ✓ | a property of diffusion models, not of a colour |

---

## The mechanism: authority → symbol → invariant

A general rule never contains a value. It contains a **symbol**, and the symbol resolves from an
authority the agent already has on a campaign it has never seen.

```
AUTHORITY            SYMBOL                INVARIANT
platform policy  →   {{TARGET_ASPECT}}  →   raw aspect must equal target ± tolerance
brand config     →   {{BRAND_PALETTE}}  →   no colour literal anywhere else
component reg.   →   {{CHROME_BBOX}}    →   generated content outside box ⊕ halo
campaign assets  →   {{CANONICAL_ENTITY}} → one asset per locked role, every slide
copy deck        →   {{LABEL_SET}}      →   each string exactly once, right-reading
layout spec      →   {{TYPO_REGION}}    →   no glyph outside it
```

The agent never needs to know what the product is. It needs to know **which symbol to bind**
and **where that symbol comes from**. Full binding table: `failure-classes.json → symbols`.

Each entry carries `authority`, a `campaign_instance` (proof the binding works) and a `note`.
The instance field exists to demonstrate resolution — it must never be copied into a rule.

---

## The transferable output: 14 failure classes

The real product of this campaign is not 28 fixes. It is **14 classes of failure** that any future
agent can check for, in any category. Each one is a sentence, a predicate and an evidence artefact.

| Class | The failure, stated generally | Comes from |
|---|---|---|
| **FC-01 Identity drift** | a locked entity is re-invented between outputs | product described in prose |
| **FC-02 Geometry loss** | a transform changes aspect, scale or content extent | square raw cropped to portrait |
| **FC-03 Constraint as ink** | a constraint stated in a prompt is rendered as visible artwork | "keep inside a 70 px border" |
| **FC-04 Chrome collision** | overlay geometry is unknown when generated content is composed | pill under the swipe chip |
| **FC-05 Label echo** | a string is duplicated, mirrored or echoed | reflection of a callout |
| **FC-06 Doctrine contradiction** | a capability, rule or doc prescribes what doctrine forbids | `place_product()` |
| **FC-07 Proxy QA** | a semantic judgment is published as a numeric test | three failed identity matchers |
| **FC-08 Scope leakage** | a rule is evaluated outside its asset class | flat-field ring test on photos |
| **FC-09 Unknown as pass** | absence of failure is treated as a pass | green gate from 2 rules |
| **FC-10 Cheap fix pressure** | defect adjusted around instead of corrected at source | cropping instead of regenerating |
| **FC-11 Config drift** | a value with an authority is typed as a literal | sampled field colour |
| **FC-12 Evidence integrity** | a verdict rests on unreproducible evidence | hand-drawn region boxes |
| **FC-13 Tooling contract** | an interface's real contract is undocumented or unsafe at edges | arity, paths, ROI crashes |
| **FC-14 Status assertion** | completion is asserted rather than derived | "released" before sign-off |

Note what happened here: `#2D5BFF`, "matte navy", `s04` and `180×120` all **disappeared**.
They were never the finding. They were the costume the finding was wearing.

---

## The procedure — how an agent generalises a new finding

Six steps. Worked on the frame defect, since that is the most tempting one to hard-code.

**1 · Record the observation with specifics.** (Concrete is correct here — evidence must be inspectable.)
> Outer band of near-constant colour, hard step against the interior, rounded-rect corner, on 4 of 5 slides.

**2 · Name the violated relation, not the violated value.**
Not "*the blue band*". The relation is: *a constraint about the edge produced ink at the edge*.

**3 · Assign the failure class.** → `FC-03 Constraint as ink`.

**4 · Write the predicate in symbols only.**
> No band of near-constant colour runs along most of an edge with a hard step > `{{BAND_DELTA}}`
> inside a band narrower than `{{BAND_WIDTH}}`.

**5 · Bind every symbol to an authority and give each a default.**
`BAND_DELTA` ← engine default 12 levels · `BAND_WIDTH` ← ≤ 8% of the dimension.
A default is a parameter with an owner, not a taste.

**6 · Declare scope and the evidence artefact.**
`applies_to: every generated asset` · evidence: edge-band report per slide.
Scope is what stops the rule from becoming the next FC-08.

**Abstraction level:** choose the *lowest* level that still holds for the next campaign —
this campaign → this asset class → all generated imagery. Higher is not better; over-abstraction
produces rules like "be creative", which is a value, not a predicate.

---

## What stays specific — and where it goes

Generality is not achieved by deleting specifics. It is achieved by **routing them**.

| If the sentence contains… | It belongs in | Never in |
|---|---|---|
| a colour | `brand.config` | a rule, a recipe, a prompt template |
| a product noun or adjective | campaign **entity manifest** | a rule or a prompt |
| a pixel value or region | component registry / platform policy | a rule |
| a slide number or version | campaign recipe | a rule |
| a scene idea ("splash hero", "commuter set") | campaign concept sheet | the playbook |
| a **relation between two symbols** | **the instruction set** | — |

The last row is the whole test. If it doesn't relate two symbols, it isn't a rule.

---

## Keeping it honest: the linter

`lint_rules.py` enforces the split mechanically. It scans **instructions only** — evidence is
allowed to be concrete, because evidence that can't be inspected is rumour.

```
$ python3 lint_rules.py errors.json          # the original register
28 instructions · 25 general · 3 leaked 9 instance value(s)
    P1  pixel-literal   '70px'
    P3  dimension-pair  '180x120'
    P5  filename        'canonical-bottle.png'
    P5  product-noun    'matte' / 'navy' / 'steel' / 'bottle'

$ python3 lint_rules.py failure-classes.json  # the generalised register
28 instructions · 28 general · 0 leaked 0 instance value(s)
```

It catches hex colours, pixel literals, canvas dimensions, slide/version ids, asset filenames,
bare percentages, and a per-campaign noun lexicon. Wire it into CI against the playbook and the
rule corpus: **an instruction that names an instance fails the build.**

---

## What the agent actually needs on a new campaign

Because every rule is symbolic, the agent needs only six answers — all from config, none from the brief's prose:

1. `TARGET_SIZE` / `TARGET_ASPECT` — from platform + placement policy
2. Which entities are **locked**, and where is each `CANONICAL_ENTITY`?
3. Which chrome components exist, and what are their `CHROME_BBOX` + `CHROME_HALO`?
4. `BRAND_PALETTE` — from brand config, never sampled
5. `LABEL_SET` per slide — from the copy deck
6. Given `INTEGRATION=scene`, which rules are applicable? (everything else is N/A, justified)

If any of the six is missing, the correct behaviour is to **stop and ask** — not to invent a value.
Inventing a value is FC-11, and it is how `#2D5BFF` got into a rule in the first place.

---

## Honest limits

- **Some rules are legitimately domain-bound.** Commerce price strike-through, carousel swipe
  affordance, story safe-areas. Keep them, but tag them `domain: ecommerce` so they are not applied
  to a brand campaign and then quietly ignored.
- **Generality is not the same as truth.** FC-03 is general because diffusion models behave that way,
  not because it sounds broader. A rule that is abstract but unverifiable is worse than a specific
  one that can be checked.
- **The corpus will drift back.** Every new incident tempts you to write the fix as the instance you
  just saw. The linter exists because that temptation is permanent.
