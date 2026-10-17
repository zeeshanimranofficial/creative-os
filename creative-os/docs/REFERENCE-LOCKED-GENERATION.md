# Reference-Locked Generation Mode

**Purpose:** preserve pixel-level visual consistency across carousel slides when
the selected, approved DNA requires repeated designs or backgrounds.

**This mode is NOT default.** It activates only when the selected DNA declares
explicit repetition requirements. Creative variety is the norm; locking is the
exception the DNA asks for.

| Slide type | Reference rule |
|---|---|
| Repeating middle slides | Same approved Master Reference |
| First / hook slide | Own distinct design; lock only if the DNA says so |
| Last / closing slide | Own distinct design; lock only if the DNA says so |
| Same background, different layout | Background-only lock; layout free per DNA |
| Completely unique slides | No reference lock unless the DNA explicitly requires it |

## 1. DNA Eligibility Check
- Before generation, inspect the selected DNA and carousel recipe for explicit
  repeat-layout, repeat-background, or repeat-component requirements.
- Apply reference locking only to the slides identified as repeatable.
- Never assume that all slides in a carousel must share one layout.
- First and final slides may use separate designs when the approved DNA
  specifies distinct hook or closing layouts.
- Enforced by `orchestrator.set_series_anchor` — it refuses to lock unless the
  DNA declares repetition (override `force=True` requires human approval).

## 2. Master Approval
- Generate and review the first representative slide of each repeated design
  family. Once approved, designate it that family's **Master Reference**.
- Never use an unapproved or failed generation as a master.

## 3. Reference Reuse
- Attach the SAME approved master to every subsequent slide of that family.
- Never replace the master with the most recently generated slide unless the
  new slide has been explicitly reviewed and approved as a revised master
  (`revise=True`).
- Provide the master alongside the exact slide-specific content instructions.

## 4. Locked Properties (full lock)
Background color/texture/lighting/gradients; composition, grid, spacing,
alignment; shapes, decorative elements, shadows, effects; illustration style,
perspective, recurring graphic placement; relative scale, position, hierarchy.
Change only the content elements the DNA and slide brief permit.

## 5. Background-Only Lock
When the DNA requires the same background with different compositions, lock
the background reference only (`lock_mode="background"`) — or better, reuse
the original background asset directly. Do not lock full layout unnecessarily.

## 6. Brand-Critical Elements
Never ask the image model to recreate exact brand typography, logos, icons,
labels, pills or page numbers — these are composited programmatically from
approved assets and real fonts after raw generation (`lib/components.py`).

## 7. Drift Check — QA30
Compare every generated slide against its designated master: background,
geometry, spacing, decorative details, palette, recurring elements.
Unauthorized deviation → regenerate via the prescribed workflow. QA30 must be
resolved on every release (not_applicable with justification when no lock).

## 8. Reference & Output Integrity
One approved master per repeat family. Hook, middle and closing reference
groups stay separate when their DNA treatments differ. Reference locking never
overrides brand rules, the approved DNA, safe margins or the QA gate.

## 9. Tool Limitation — Reuse Beats Re-prompting
Image-reference prompting improves consistency but does not guarantee
pixel-identical output. Where exact repetition is required, prefer in order:
1. **Text-only change** → reuse the approved background asset unchanged and
   composite the new text with real brand fonts
   (`components.render_text_block`) — never regenerate unchanged visuals.
2. **Content/scene change** → generate with the approved master as primary
   reference (this mode).
3. **Background repeat only** → preserve the background asset separately and
   reuse it directly.

Scope guard: option 1 is assembly from approved assets under an active lock.
It is NOT a license to rebuild artwork programmatically or to patch a
DNA-mismatched generation — a mismatch is still a regenerate, per fail_policy.
