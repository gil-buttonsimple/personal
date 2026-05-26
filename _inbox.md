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

*(none yet)*
