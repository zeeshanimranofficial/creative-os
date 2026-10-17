# ZEESHAN IMRAN — MASTER BRAND & DESIGN SYSTEM
> Single source of truth. Every post/carousel MUST be verified against this file before delivery.
> Reference DNA (layout grammar) comes from the two reference templates — we borrow their **creativity only**, never their brand handles, logos, or colours.

---

## 1. IDENTITY

| Item | Value |
|---|---|
| Profile name | **Zeeshan Imran** |
| Title | **Cold Email & Outbound Strategist** |
| Type | Personal LinkedIn / social profile |
| Company / website / logo | ❌ NONE — never invent or add one |
| Profile block placement | **ONLY on the LAST slide of a carousel, or on a minimal single post — never on every slide** |
| Profile picture | **ALWAYS use the real DP asset `/home/user/brand/dp-circle.png` in the profile-block circle — NEVER initials ("ZI") or placeholder avatars** |
| Signature mascot | **Spider-Man** — used ONLY when a person/character is genuinely needed for creativity. Not mandatory on every design. |

## 2. BRAND COLOURS (strict — no other brand colours)

| Role | Name | Hex |
|---|---|---|
| PRIMARY | Burnt Orange | `#FF5A00` |
| Surface / light | Warm Cream | `#F5EFE6` |
| Text / dark | Charcoal | `#1A1A1A` |

Colour behaviour (adapted from reference DNA):
- **Orange background** → high-impact slides: hooks, CTAs, stats, myth/fact, FAQ. Text in cream/charcoal.
- **Cream background** → editorial, explanatory, process, typography-heavy slides. Text in charcoal, highlights in orange.
- **Charcoal** → primary typography, structure, signature arrows, labels; may be used as dark background variant with cream/orange type.
- Tints/shades of these three are allowed for depth (shadows, translucent shapes); unrelated hues are NOT.

## 3. TYPOGRAPHY — ONE FONT SYSTEM, ALWAYS THE SAME
- Pick ONE geometric sans family and reuse it across ALL designs (headline weight 800–900, sub 600–700, body 400–500).
- Working choice: **Poppins** (fallback: Montserrat / Inter). Once used, NEVER switch — Poppins IS the brand family for all structural text (headlines, subs, body, labels, components).
- **Accent-font exception (user directive 2026-09-28):** where a creative genuinely calls for it (per reference DNA), suitable accent fonts MAY be used for accent roles only — e.g. brush-script "Coming soon" flourishes, casual handwriting annotations, typewriter/monospace date stamps (Refs H/I). Rules: one accent voice per role, reused consistently across designs (same script font every time, same mono font every time); accents never carry headlines or body copy — Poppins always dominates.
- Strong size contrast; headline dominates and must be readable at thumbnail size.
- Uppercase for major topic words / labels. Body copy short — no dense paragraphs.

## 4. HARD LAYOUT RULES (non-negotiable)

| Rule | Spec |
|---|---|
| Safe-area grid | **EXACTLY 30 px margin on ALL four sides**, every canvas size. Nothing important outside it. |
| Engagement icons | Save / Repost / Like icons default **40 × 40 px** (24px was too small — user directive 2026-09-28). May scale to suit the creative (~32–56px range), but all three icons in one design are ALWAYS the same size. The **30px grid stays locked** regardless of icon size. |
| Icon files | `/home/user/brand/icons/` → `save|repost|like` in `orange`, `cream`, `charcoal` (40px production + 24px legacy + 512px masters — resize from 512 masters for any other size). |
| Swipe icon assets | `swipe-pill` (chevrons » » » » ●) and `swipe-hand` (finger gesture) registered in all 3 brand colors (24/48/512px). Candidates for an upgraded Swipe marker — the current 178×54 chip stays THE standard until explicitly switched; any switch applies everywhere at once. |
| Fonts on hand | Poppins Regular/Medium/SemiBold/Bold/ExtraBold + Italic/MediumItalic/BoldItalic — italic weights reserved for emphasis words and "Insight:"-style labels (same single family). |
| Accent fonts on hand (added 2026-10-15, per user — "supporting fonts also help in creatives") | All in brand/fonts/, accent ROLES only, Poppins always dominates: **Anton-Regular** = heavy condensed display accent (stamp headlines like "BIG NEWS.", poll display type); **Playfair Display** Regular/SemiBold/Bold + Italic/BoldItalic = serif editorial accent (testimonial quotes, torn-strip reveal lines, "and money."-style emphasis); **Dancing Script** Regular/Bold = script accent (headers like "Cold Email Tips", "limited offer" kickers). One accent voice per role, reused consistently. Specimen: brand/font-specimen.png. |
| Other icons | From Iconify (or best-fit source), always recoloured to brand palette, same visual family per design. |
| App/tool logos | Real logos allowed when contextually needed (e.g. Gmail, Apollo, LinkedIn) — choose the most suitable official mark. |

## 4b. STANDARD COMPONENT SPECS (identical on every slide — never let the image model freestyle these)
| Component | Spec |
|---|---|
| Slide-number / tag pill (e.g. "01 / 07", "REASON 3") | Height **56px**, radius 28, Poppins Bold **26px**, 26px side padding, positioned at **(60, 60)** top-left on every slide (panel-inset layouts: align to the panel's inner corner instead). Cream background → orange pill + cream text. Orange background → cream pill + orange text. |
| Label box (e.g. "BOUNCE RATE", "WRONG LIST") | Charcoal rectangle, height 56px, Poppins Bold 26px cream text, 24px padding, 16px gap beside/below its pill. |
| Toggle switch | 92×48px, radius 24. OFF = charcoal track + cream knob LEFT. ON = cream track + orange knob RIGHT. Both states MUST clearly contrast with the background — a toggle that blends into its background is a defect. |
| Swipe chip | 178×54px charcoal pill, Poppins SemiBold 24 "Swipe" + orange arrow, at (872, 1266) for 1080×1350 — never moves. |
| Profile block | DP circle + Poppins Bold name + Poppins Regular role + 40px icon row (was 24px in Week 1); carousel-final: stacked centered; minimal post: horizontal centered strip. |

## 5. CANVAS SIZES

| Format | Size | Ratio |
|---|---|---|
| LinkedIn carousel | **1080 × 1350** | 4:5 |
| LinkedIn single post | **1080 × 1080** | 1:1 |
| TikTok carousel | **1080 × 1920** | 9:16 |

30 px grid rule applies identically to all sizes (LOCKED); engagement icons 40px default / creative-scaled.

## 6. CAROUSEL "SWIPE" MARKER (identical on every carousel)
- Every carousel slide EXCEPT the last: the word **"Swipe"** + an arrow pointing right.
- Style: brand font, paired with the signature thick charcoal (or cream-on-orange) curved arrow.
- Position, size, and style must be **pixel-identical across all slides and all carousels** (bottom-right, inside the 30 px safe area).
- Last slide: no Swipe marker → carries the profile block (Zeeshan Imran / Cold Email & Outbound Strategist) + CTA + optional 40 px Save/Repost/Like icons.

## 7. REFERENCE DNA (what we preserve)
Stored in full at `/home/user/brand/reference-dna.json`.

**From Reference 1 (red social-media template → re-skinned to our palette):**
concept/metaphor posters, editorial definitions, numbered roadmaps, myth-vs-fact toggles, collage quick-start guides, best-practice highlight lists, service cards, typography posters, FAQ speech bubbles, statistic cards, step-by-step card stacks, big-number data slides, checklist fixes, giant Q&A type, benefit stacks, process infographics.

**From Reference 2 (yellow LinkedIn template → re-skinned to our palette):**
giant number posters, thick hand-drawn curved arrows, highlight rectangle bars, black label boxes, large circular visual zones, split-colour backgrounds, bottom author strip (last slide only for us), circle action button, flat business illustration style.

**From Reference Batch #2 (see `reference-analysis-2.md`, Refs D–G → re-skinned to our palette):**
quote-insight posts (giant quote + italic "Insight:" row + dashed rule), reverse highlight blocks on pivot words, myth-buster with device mockup, tilted sticker-over-headline, orbiting sticker pills (tilt + soft shadow), personal manifesto/intro poster, checklist ✓ bullets, date/edition chips, corner glow blobs, optional subtle paper/grid texture variant, **Series Mode** carousels.

**From Reference Batch #3 (Refs H–J → re-skinned to our palette):**
announcement/save-the-date poster (tilted calendar grid + typewriter date stamp + hand-drawn circle on ONE pivot word + halftone cutout w/ burst lines), UI-metaphor widgets (incoming-call / notification chrome → "Incoming reply: Interested" hooks), object-metaphor mockups (book/envelope/inbox as story device), circular text badge/seal, vertical-rule side notes, tilted text-block mode (whole block ~7° on rotated-grid/paper bg — declared per-design), orange line-doodle illustration sets (1–2 per slide, corners), physical props (paperclip/torn edge/note scrap) on texture variants, arrow-direction flip on carousel closers.

**Cross rules:** match content intent → archetype; one dominant focal point per slide; high negative space; decorations never compete with the message. Two carousel modes:
- **Rotation Mode** (default): rotate archetypes, never repeat composition on consecutive slides — for varied listicle content.
- **Series Mode** (for stages/states/steps content): distinct hook + closer, but ONE locked template repeated verbatim for all middle slides — repetition is the design; only content changes, geometry never moves.
Texture note: subtle cream-paper/grid texture backgrounds are allowed as a declared variant (tonal, within cream tint range); the exact-hex snap rule (3a) applies to solid fills — texture zones are exempt but must stay within brand tints.

**Anti-rules:** no off-palette colours, no dense paragraphs, no identical layout on every slide, no over-decoration, no sacrificing readability, no copying reference brands/handles/logos/colours.

## 8. PRE-DELIVERY VERIFICATION CHECKLIST (run on EVERY design)
1. ☐ Canvas size correct for the format?
2. ☐ 30 px safe margin respected on all 4 sides?
3. ☐ Only #FF5A00 / #F5EFE6 / #1A1A1A (+ tints) used?
3a. ☐ **EXACT-HEX CHECK (mandatory, learned from Friday s01/s07 defect):** pixel-sample every solid background in at least 3 zones — top-left, bottom-left, and the bottom-right Swipe-chip corner — all must measure EXACTLY the brand hex with zero off-tone patches. AI-generated fills always drift, so ALWAYS run the brand-color snap pass (converge orange/cream/charcoal clusters to exact #FF5A00 / #F5EFE6 / #1A1A1A) on every generated design BEFORE compositing the Swipe chip, icons, or profile block. The corner zone under the Swipe chip must be indistinguishable from the surrounding background.
3b. ☐ **MICRO-DETAIL CONSISTENCY CHECK (mandatory, learned from label/toggle defects):**
   - Repeating labels (slide-number pills "N / N", "REASON N" tags, kickers) are IDENTICAL in height, font size, padding, and y-position across every slide of a carousel — AI-generated labels always drift, so overpaint them and composite the standard components from section 4b instead.
   - Every UI widget (toggle, pill, button, chip) is clearly visible against its background — an OFF toggle that blends into a dark fill, or any element hiding in a same-tone area, is a defect.
   - After any patch/edit, re-inspect at 100% zoom for: leftover fragments of removed elements, clipped letterforms, stray shapes, seams at patch edges — and verify a wide margin around headlines before painting over "remnants" (letter tops/ascenders are easy to mistake for artifacts).
4. ☐ Same single font family as all previous designs?
5. ☐ Headline readable at thumbnail size, hierarchy obvious in 1 second?
6. ☐ Save/Repost/Like icons 40 px (or one deliberate creative-suited size, identical for all three) where used? 30px grid still intact?
7. ☐ Swipe + arrow identical on all non-final carousel slides?
8. ☐ Profile block ONLY on last slide / minimal post — no company name, website, or logo anywhere?
9. ☐ Layout maps to a reference archetype (DNA preserved, not pixels copied)?
10. ☐ Slide-to-slide variation present, but system consistent?
11. ☐ Icons/illustrations from one visual family, recoloured to brand?
12. ☐ Spider-Man only if a character genuinely adds creativity?

## 9. VISUAL HERO RULE + TYPE-SYSTEM WORKFLOW (client instruction, Oct 2026)

Learned from Week-3 drift: creatives came out typography-led (headline + small corner icon),
while every saved reference is GRAPHICS-led — the graphic IS the post (K05 shadow-pun,
K09 printed prop, K12 photo sandwich, K17 metaphor objects, K04 calendar-UI hero).
Root cause: defensive bias — text-led flat layouts are easier to QA, so pipeline
convenience was shaping art direction. Not acceptable.

**9a. VISUAL HERO RULE (mandatory):**
- Every creative carries ONE dominant graphic hero — object, scene, UI mockup, prop,
  character, or visual pun — occupying roughly 40%+ of the canvas.
- Typography supports the hero; it never substitutes for it.
- Pick the hero BEFORE the type treatment: "what is the hero object of this idea?"
- Exception: carousel mid-slides may stay lean for reading rhythm; covers, feature slides,
  and ALL single posts get heroes.

**9b. TYPE-SYSTEM WORKFLOW (mandatory):**
The reference library is a deliberate TYPE SYSTEM — at least one reference per post type
(see `reference-dna.json -> post_type_index`). For any brief:
1. Match the post TYPE → its reference(s).
2. RE-OPEN the actual reference image(s) with the vision model (uploads/) and extract the
   hero device, composition and visual weight fresh — never rely only on text DNA summaries.
3. Inherit the reference's STAGE (composition, scale, prop logic).
4. Swap in OUR topic-relevant hero (the ACTOR). Reference = stage, topic = actor.
5. Prompts describe the hero FIRST (size, position, dominance); text second.
Palette laws, programmatic brand elements, and all QA passes unchanged.

### Checklist additions (append to section 8):
13. ☐ VISUAL HERO present — one dominant graphic ≈40%+ of canvas; typography supporting,
    not substituting? (singles + carousel covers/feature slides)
14. ☐ TYPE-SYSTEM match — post type mapped to its reference via post_type_index, reference
    image re-analyzed with vision before generation, hero swapped to our topic?

15. HERO CENTERING / NEGATIVE SPACE: single-object heroes optically centered or counter-balanced; no dead half-canvas (Tue-W3 S2 failure: phone pushed left, right half empty).
16. LOCKED-SERIES EXACTNESS: identical headline size/alignment, hero footprint (+/-3%), fonts across series slides; one shared composite transform; drifting members get REGENERATED from the template slide (Tue-W3 S3-S6 failure: per-slide scales 0.78 vs 0.71, condensed S5).
17. RESERVED-ZONE COLLISION: TL pill/label and BR chip zones must be empty in the raw - measure before compositing; never blind-wipe a zone that contains headline pixels (Tue-W3 S7 failure: wipe clipped the W of WHAT; pill crowded headline).
18. LIST ROWS CARRY TEXT: numbered bars in heroes must contain real labels, never empty bars (Tue-W3 S8 failure: bare 1-4 bars looked like a wireframe).
19. LABEL HIERARCHY: counter pill TL -> section label under it -> swipe chip BR, identical size/placement on every slide, per reference DNA.

20. DNA-LIBRARY MATCH (22 profiles; DNA_16/17/19/22/25/26 REMOVED per user order 2026-10-15):
    NOTE 2026-10-15: the 9-tile IDAI collage reference image was ALSO deleted per user order.
    DNA_12, 13, 14, 15, 18, 20 are now JSON-ONLY recipes (no reference image on disk) -
    when using them, work from the written recipe fields alone; the vision re-open step
    does not apply. DNA_21-28 survivors (21, 23, 24, 27, 28) were already JSON-only. every new creative must be matched to the closest profile
    in brand/reference-dna.json design_dna_library (DNA_01-DNA_28) BEFORE generation; verify the
    final design inherits that profile's composition/hierarchy per global_recreation_rules
    (preserve composition, adapt topic, exclude logos/brand names/handles).
    Quick index:
    DNA_01: Dark Editorial Calendar Announcement - monthly announcements, milestone reminders
    DNA_02: Tactile Calendar Editorial Collage - appointment booking, limited-time offers
    DNA_03: Photographic Calendar Event Poster - religious celebrations, community events
    DNA_04: Oversized Typography Testimonial - customer testimonials, review highlights
    DNA_05: Minimal White 3D Service Orbital - service overviews, technology offerings
    DNA_06: Blue Modular Service Blocks - service lists, agency capabilities
    DNA_07: Red Photorealistic Social Advertising Composite - software product advertising, workflow automation
    DNA_08: Minimal Blue Paper Note - branding advice, marketing insights
    DNA_09: Clean Blue Editorial Explainer - educational carousels, marketing psychology
    DNA_10: Blue Clipboard Typography Poster - carousel cover slides, educational marketing posts
    DNA_11: Purple Layered Social Media Challenge Poll - Audience polls, Engagement questions
    DNA_12: Affordable Design Mascot Poster - Affordable creative services, Agency service promotion
    DNA_13: Brand Spotlight With Press Microphones - Brand awareness, Publicity and visibility
    DNA_14: 360 Degree Solutions Typography Wheel - Service menus, 360-degree agency offers
    DNA_15: Red Chain Link Brand Growth Poster - Brand positioning, Partnership and connection
    DNA_18: Relaxed Cat Astronaut Campaign - Relaxed service promotion, Brand growth and outsourcing
    DNA_20: Friendly Red Service Mascot - Service lists, Digital agency capability posts
    DNA_21: Purple Oversized Trust Statement With Device Mockups - Trust-building posts, Digital marketing service promotion
    DNA_23: Start Creating Astronaut Editorial Collage - Creative motivation, Starting a project
    DNA_24: Build Your Own Platform Pixel Disintegration - Building a platform, Creative action and initiative
    DNA_27: Opportunity Torch Editorial Collage - Action-oriented motivation, Opportunity and initiative
    DNA_28: One Percent Action Carousel Cover - Carousel covers, Motivational series title cards

## 10. CAROUSEL NAVIGATION KIT SYSTEM (added per client direction)
One navigation kit is chosen PER CAROUSEL at theme-proposal stage, declared before any
generation, then locked across every slide of that deck. Consistency is WITHIN a carousel;
variety is ACROSS carousels.

10a. Kit components (pick one of each):
  - COUNTER: orange rounded pill "NN / NN" | charcoal square tab | cream-on-charcoal corner
    flag | minimal text "N—N" | progress dots strip.
  - SWIPE CUE: "Swipe" chip + arrow | swipe-hand icon (brand/icons swipe-hand-*) |
    bare long arrow | "NEXT ->" edge-bleed tab.
  - PLACEMENT: counter TL or TR; swipe cue BR or bottom-center. Choose placement so the
    cover art never collides with the counter (prefer TR when the cover hero owns the TL).
10b. Pairing guidance: editorial-collage decks -> small editorial tab + bare arrow;
  playful/announcement decks -> pill + chip; minimal Swiss decks -> minimal text + arrow;
  motivational decks -> swipe-hand allowed. Match the deck's DNA profile mood.
10c. Rules that never change regardless of kit: identical size + position on every slide
  of the deck; contrast against background verified per slide (switch color variant, not
  position); reserved zones recalculated to the chosen corners BEFORE generation; closer
  slide drops the swipe cue.
10d. The theme proposal shown to the client must include a "Navigation kit" line for
  approval alongside the DNA mapping.
10e. Existing delivered carousels (Week-3 Tuesday, Week-3 Friday, Week-4 E-commerce
  Series) keep their current kit - do NOT retrofit.

QA AMENDMENT to item 19: "LABEL HIERARCHY" now reads kit-relative - counter and swipe cue
follow the carousel's declared navigation kit (Section 10); hierarchy and per-slide
consistency requirements unchanged. QA item 17's reserved zones are the zones implied by
the declared kit placement.

20b. LIBRARY EXTENSION (creative_design_dna): 10 additional profiles design_01-design_10 in
    brand/reference-dna.json creative_design_dna, each with a verified source_image path in
    uploads/ - open that image with vision before using its stage. Matching rule same as item 20.
    Quick index: 01 torn-paper secret poster | 02 service-search dropdown | 03 testimonial
    minimal-luxury | 04 editorial 3D still-life carousel cover | 05 gradient condensed-type
    brand poster | 06 clean branding explainer cover | 07 high-energy red character poster |
    08 engagement-strategy collage (hand + reaction bar) | 09 Roman-Urdu monochrome photo
    collage | 10 giant-numeral swiss carousel cover.

20c. COLLECTION LIBRARIES (template-grid DNA): two tile collections in brand/reference-dna.json,
    each entry a standalone design recipe sourced from one collage image (open the collage with
    vision and locate the tile before using its stage):
    - sage_green_collection: 24 creatives, muted sage botanical lifestyle (giveaway frames,
      daily-reminder toggles, question search bar, device mockups, reminder cards, numbered
      list cards, monthly hello, UGC-frame posts...). Source: uploads/10+ Modern Green
      Instagram Post Templates...jpeg
    - skincare_neutral_collection: 15 creatives, warm neutral skincare editorial (product promo,
      features card, serum trio, promo with portrait, skin-tips pills, testimonial phone,
      podcast episode, giveaway steps, livestream speakers...). Source: uploads/(Glow Up Your
      Feed) Aesthetic Skincare Templates...jpeg
    Matching rule same as item 20; collection palettes may be kept (client-neutral templates)
    or re-mapped to brand colors depending on the brief - confirm at theme stage.

20d. LIBRARY EXTENSION v2 (creative_design_dna_v2, merged 2026-10-16): 10 additional profiles
    in brand/reference-dna.json creative_design_dna_v2. IDs collide with 20b's design_01-10,
    so ALWAYS cite these as CD2_01..CD2_10 (dna_ref field). ALL reference images are PHANTOM
    (JSON-only recipes — reference_file names like 48643.jpg are not in the workspace; match
    and verify from the written recipe fields only):
    - CD2_01 bold editorial advice poster, human cutout photography (quality-over-cheapness)
    - CD2_02 calendar-led seasonal announcement (date + overhead event photo)
    - CD2_03 conceptual person-and-object ad poster (visual pun, oversized publication/feed)
    - CD2_04 high-energy service explainer with central social-post panel
    - CD2_05 minimal typographic insight infographic (contrasting speech panels)
    - CD2_06 number-led educational poster, flat vector illustration (mini-guide)
    - CD2_07 question-led engagement graphic, layered ribbon options
    - CD2_08 desktop-workspace flat-lay with bold callout bubbles
    - CD2_09 multi-tile campaign system / social content grid
    - CD2_10 nine-tile agency content grid (single-color campaign system)
    Matching rule same as item 20; recipe palettes re-map to brand colors unless the brief
    says otherwise. Each recipe carries a full prompt_blueprint field — use it as the
    generation skeleton, with brand palette + locked fonts swapped in.

21. DEVICE / HERO GEOMETRY FIDELITY (vision compare, MANDATORY): when a creative borrows a
    background graphic or hero device from a reference (giant numeral, torn strip, search bar,
    mockup, character...), build a side-by-side of reference vs output and verify with the
    vision model that the device's GEOMETRY matches the reference's character: crisp vs blurry,
    sharp-edged glyph vs translucent fog, anchoring/overflow behavior, scale relative to canvas.
    A device rendered as a washed/blurred approximation of the reference's crisp element FAILS.
    Known trap: image-model EDIT passes (e.g. typo fixes) can silently degrade background
    devices - after ANY edit or regen, re-run this compare. For structural fixes prefer a full
    regen with the original reference image + explicit geometry language ("crisp, sharp-edged,
    NOT blurry/translucent") over an edit pass. (Caught on instagram-kit carousel-cover: typo
    edit turned the crisp design_10 numeral into a blurry wash.)

22. HEADLINE-TO-DEVICE SPACING HIERARCHY (vision compare, MANDATORY): verify the breathing
    room between the headline block and the adjacent hero device matches the reference's
    hierarchy - e.g. design_01 keeps a clear gap between the headline and the torn strip;
    output where they touch or overlap FAILS. Measure the gap in the reference, demand it in
    the prompt ("clear ~70px gap between X and Y, must not touch"), and vision-check the output.
    If elements touch in a delivered raster, do NOT band-shift rectangles near overlapping
    glyphs (cuts letterforms) - fix via model edit "move device down, keep everything else
    identical" and re-composite. (Caught on instagram-kit announcement: "NEWS." touched the
    torn strip; reference kept a gap.)

23. INNER DESIGN FRAMES vs BRANDING STRIP (measure, MANDATORY): when a creative's design
    includes an inner frame/border (thin keyline box inside the canvas), the composited
    branding details (DP circle, name, role text incl. descenders, engagement icons) must
    NOT touch or cross the frame lines - keep >=10px clearance on every side. Before
    compositing, locate the frame's bottom border row programmatically (long dark-pixel run
    scan) and shift/compact the strip so it sits balanced between the frame line and the
    element above it. Default strip coords are NOT universal - frame position varies per gen.
    (Caught on instagram-kit promo: DP/role text sat 2-4px from the frame's bottom border at
    y1297; tips had ~15px and read correctly. Fix: strip dy=-12 -> 13px/13px balanced.)

24. DNA SOURCE POLICY FOR BUSINESS KITS (user correction 2026-10-15): BUSINESS KITS are
    built from the OLD DNA library (design_dna_library_extended.json -> DNA_01-28 in
    brand/reference-dna.json). Within it, default to the clean/consistent/white-space-perfect
    editorial recipes (e.g. DNA_01, 02, 04, 06, 09, 10, 11, 28); use its hero-object recipes
    (DNA_05, 13, 14, 15, 18, 20, 21, 23, 24, 27) when a post needs one dominant hero graphic (>=40% canvas, graphics-first directive). NOTE: DNA_16, 17, 19, 22, 25, 26 were REMOVED from the library per user order 2026-10-15 (their typography did not match the finalized brand font system) - never regenerate from them.
    The newer collections (design_01-10, sage, skincare) remain available for other/single
    creatives when the user asks for them - but kits default to the old library.

25. STRIP-ZONE BACKGROUND CONTINUITY (user flag 2026-10-16, MANDATORY): the bottom reserve
    band where the profile strip sits must be a CONTINUOUS part of the artwork background -
    never a flatter/lighter zone that reads as an overlaid patch.
    a) AUDIT (numeric, every final): compute the smoothed vertical color profile on clean
       margin columns (e.g. x40-90) across y980-1345 (1080x1350 scale); the max row-to-row
       smoothed jump must be < ~1.5 on flat backgrounds. Higher values on photo/texture
       pieces must be visually confirmed as real design edges (objects, panel borders).
    b) FIX POLICY: tone-shifted reserve bands are fixed by FULL REGEN with an explicit
       "background is ONE continuous even tone (or the scene continues full-bleed) to the
       very bottom edge; no lighter band, no vignette shift" clause - photo scenes get
       "calm, uncluttered, softly blurred continuation, no objects/text/hard edges" so
       strip text stays legible (pick strip color variant by measured band tone).
    c) BANNED: band-fills/extrapolation under or near rendered copy (smears text into
       streaks - destroyed two raws on 2026-10-16); per-column extrapolation through
       texture/content columns (vertical streaks); uniform-row fills on vignetted
       backgrounds (visible stripe). Small offset corrections and clean-grain refills are
       allowed ONLY on verified content-free flat zones, and must pass the audit in (a).

26. SERIES ALIGNMENT LOCK (added 2026-10-16 after F2-sequence slide-04 drift). Within any
    carousel/sequence, repeating structural elements (numerals, headlines, body paragraphs,
    underline/accent bars) must share ONE alignment scheme across every slide - all left-hung
    on a common margin, or all centered, never mixed.
    a) AUDIT: for each repeating element, compare its bounding-box left edge (or center-x)
       across slides; deviation > ~4% of canvas width = FAIL.
    b) ANY drift on ANY repeating element fails the slide - "minor" body-copy drift is NOT
       tolerable; a centered paragraph or numeral on an otherwise left-hung system is a
       system break even if it looks acceptable in isolation.
    c) FIX POLICY: regenerate the offending slide using an on-system sibling slide RAW as
       the style reference, with an explicit "numeral, headline, paragraph and underline are
       ALL LEFT ALIGNED to one shared left margin, ragged right, absolutely nothing center
       aligned" clause (verified working on f2 seq s4 v2).

27. TYPOGRAPHIC SCALE LOCK (added 2026-10-16 after F2-sequence size/weight drift). Within any
    carousel/sequence, repeating text elements must share ONE typographic scale:
    a) AUDIT (numeric, runs BEFORE presenting): measure per slide the headline cap-height
       (tallest charcoal row-run), numeral height (tallest orange row-run), and paragraph
       line height. Across the repeating detail slides, each measure must agree within ~5%.
       Weight is checked via ink-fill ratio of the headline bbox (bold >= ~0.45).
    b) The hook and recap slides may use different LAYOUTS but the same typeface and weight;
       their sizes should sit as close to the series scale as the layout allows and must
       never look lighter than the detail slides.
    c) FIX POLICY: regenerate off-scale slides CLONED from the best on-scale sibling RAW
       ("copy the reference layout EXACTLY, same typeface, same heavy bold weight, same font
       sizes, ONLY the numeral and the words change", plus "capital letters EXACTLY THE SAME
       HEIGHT as the reference headline" when needed). Verified: converges detail slides to
       identical scale (f2 seq v3/v4: headlines 154-155px, numerals 464-468px at 1080x1920).
    d) KNOWN CEILING: multi-line hook/recap headlines auto-balance smaller (~75-85% of the
       detail cap height) and repeated regens converge to the same size - accept the ceiling
       rather than burning generations, but weight must still match.
    e) ALWAYS check regens for COPY LEAK from the reference slide (a recap regen absorbed the
       reference paragraph on 2026-10-16) - full-res copy read is mandatory after every clone.
