# CURRENT_HANDOFF

## 2026-09-07 12:20:37 UTC
- Debugged preorder sprite regression after beef photo replacement.
- Root cause: image binary layout was correct for the newly approved beef photos, but downstream appetizer/dessert IDs still pointed to pre-insertion tile positions, causing cascading wrong images.
- Fix: remapped a3->100% 80%, a4->0% 100%, d1->33.333% 100%, d3->66.667% 100%; kept a1->33.333% 80%; left a2 and d2 unmapped placeholders.
- Added sprite cache-buster so LIFF/Safari cannot keep the stale binary.
- Regression checks: m9/m10/m11, Monday guard, LIFF sendMessages, placeholder rules, and git diff --check.

## 2026-09-08 12:17 ICT
- Restored per-menu +/- quantity controls.
- Fixed malformed LINE receipt by joining explicit message lines with newline characters.
- Preserved add-on flow, Monday guard, prices, cart totals, and LIFF sendMessages.

## 2026-09-08 12:31 ICT
- Changed menu quantity UX to two-step selection: +/- adjusts pending quantity only; Add to cart commits it.
- Normal items add selected copies together; add-on items keep the existing add-on modal and commit selected copies after confirmation.
- Pending quantity resets after successful add; cart totals and LINE receipt use committed cart entries only.
- Preserved Monday guard, LIFF sendMessages, menu prices, and formatted LINE receipt.
