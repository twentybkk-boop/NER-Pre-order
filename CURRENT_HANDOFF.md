# CURRENT_HANDOFF

## 2026-09-07 12:20:37 UTC
- Debugged preorder sprite regression after beef photo replacement.
- Root cause: image binary layout was correct for the newly approved beef photos, but downstream appetizer/dessert IDs still pointed to pre-insertion tile positions, causing cascading wrong images.
- Fix: remapped a3->100% 80%, a4->0% 100%, d1->33.333% 100%, d3->66.667% 100%; kept a1->33.333% 80%; left a2 and d2 unmapped placeholders.
- Added sprite cache-buster so LIFF/Safari cannot keep the stale binary.
- Regression checks: m9/m10/m11, Monday guard, LIFF sendMessages, placeholder rules, and git diff --check.
