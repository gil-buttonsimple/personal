# _inbox -- Cross-context captures

**Last Updated:** 2026-05-14

Holding pen for business-flavored items that surface during personal chats. Append-only log. Entries stay here until explicitly triaged out to the appropriate business doc.

---

## How this works

1. During a personal chat, if business stuff comes up, Claude flags it in the moment.
2. On confirmation (or if clearly business), Claude appends a row below.
3. Entries remain until you say "process inbox" or "convert these" -- then they get moved to the appropriate business doc and marked `converted` (row stays for audit).

## Conventions

- Append-only. Never delete; only update status.
- Status values: `captured` (new), `triaged` (reviewed, destination known), `converted` (moved to destination doc).
- Keep the captured content brief but verbatim enough to preserve intent. Add `context` for what the surrounding personal chat was about.
- When converting, note the destination doc and date in the entry.

## Entry format

```
### YYYY-MM-DD -- short title
- **Status:** captured | triaged | converted
- **Context:** what personal topic was being discussed when this came up
- **Captured:** the business item itself
- **Destination:** (when known) which business doc this belongs in
- **Converted:** (when done) YYYY-MM-DD -> doc name
```

---

## Entries

### 2026-06-02 -- Salvaged email-migration edits from stale Documents/Personal clone
- **Status:** captured
- **Context:** A second, stale clone of the personal repo at ~/Documents/Personal (stuck at session 7, on the old current_state.md) had uncommitted edits dated 2026-05-30 that never reached origin. The clone was deleted during the Baobab Documents cleanup. Its VW cellular spec was salvaged to gov (architecture/vehicle_eurovan.md). These Google clean-up table edits CONFLICT with the newer mainline personal_state.md (session 9) and need manual reconciliation -- do not assume either is current.
- **Captured (clone's version of the Google clean-up table deltas):**
  - Step 1: "Redirect email: web@gkasparek.com forward to tgk@ -- set up at mailserver" -- status **Needs redo** (mainline says "Namecheap DNS forward web@ to tgk@" / Done).
  - Step 7: "Emails -- start fresh, skip copy. tgkasparek@gmail.com is new primary" -- status Next (mainline says "Copy emails / Next -- method TBD").
  - Open-question rewrite: "web@gkasparek.com is a Google login identity only -- not a Gmail inbox. Forward-only via mailserver. No send-from needed." (replaces mainline's "custom domain email likely cannot stay on free Gmail" note).
- **Destination:** personal_state.md -- Google clean-up section (reconcile against session 9 mainline).
