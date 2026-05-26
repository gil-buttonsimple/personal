# Workflow: Multi-AI Conversation Audit

**Last Updated:** 2026-05-26

---

## Purpose

A repeatable process for extracting useful information from AI conversation history
across multiple tools. Useful after travel, intensive work periods, or any time
conversations span multiple AI platforms and need to be consolidated.

---

## Governance Rule

Personal boot mode never writes to business canon directly. Learnings from personal
sessions that have work application are captured here first. A suggestions route
to business canon is a future design item.

---

## When to Use

- After a road trip or travel period where AI was used heavily on mobile
- When work has spanned Claude, ChatGPT, and Gemini across multiple sessions
- When building or updating a personal knowledge base or to-do list
- Periodically (quarterly?) to surface forgotten decisions and research

---

## Method Used (May 2026 Bus Trip Audit)

### Step 1: Claude Code sessions (local)

Claude Code stores sessions as JSONL files in:
`~/.claude/projects/<project-path>/*.jsonl`

Find sessions from a date range:
```
find ~/.claude/projects/ -name "*.jsonl" -not -path "*/subagents/*" -mtime -12
```

Spawn an Explore agent to read and summarize relevant sessions. Filter for
non-governance sessions (personal, mobile, voice setup).

**Good for:** Voice/mobile setup work, dev experiments, anything done in VS Code.

---

### Step 2: Claude.ai export

Settings > Export data at claude.ai. Downloads a ZIP with JSON conversation files.

**What it contains:** Full conversation history, all threads.
**What it misses:** Nothing significant.
**Turnaround:** Immediate download.

Import the ZIP and scan with an agent, filtering by topic.

**Good for:** Personal research, travel conversations, voice mode experiments.

---

### Step 3: Gemini (in-app self-summary -- preferred method)

Google Takeout does NOT export Gemini conversation history. Instead:

Open a new conversation at gemini.google.com and prompt:

> "Look at my recent conversation history from [date range] and summarize
> everything that happened -- what we discussed, what I was doing, where I was.
> Use the conversation titles to organize it. Then separately, give me detailed
> bullet points on [specific topics]."

Gemini can reference its own past conversations from the same account. This
produces a single consolidated summary covering all threads at once.

**Good for:** Navigation, voice assistant troubleshooting, quick lookups,
anything done via Google Assistant / Android.

**Limitation:** Quality depends on Gemini's recall. Cross-check against thread
titles if anything seems missing.

---

### Step 4: ChatGPT export

Settings > Data Controls > Export. Sends a ZIP download link via email.
Takes a few minutes to generate.

Unzip and scan JSON files for relevant conversations.

**Good for:** Technical research, anything done in the ChatGPT Android app,
speech-to-speech hands-free use while driving.

---

## Consolidation

After collecting from all sources:

1. Identify conflicts or contradictions across AIs (they may have different
   information about the same event -- treat as complementary, not authoritative)
2. Write vehicle / project findings to their respective files
3. Write to-do items to the relevant doc's Active Todos section
4. Update current_state.md with any new open items
5. Note which sources have been processed and which are still pending

---

## Mobile vs. Desktop Variations

**Mobile (traveling, driving):**
- Gemini in-app summary is the primary method (no export needed)
- ChatGPT is the best hands-free voice AI; its sessions are most valuable for
  voice workflow findings
- Claude.ai export covers research and planning done at rest stops or parked

**Desktop (office):**
- Claude Code JSONL scan is fast and fully local
- All exports can be processed in parallel via background agents
- Full consolidation and repo write happens here

---

## What Each AI Is Good For (observed patterns)

| AI | Strength on the road |
|---|---|
| Gemini | Navigation, Google Assistant integration, quick Android voice lookups |
| ChatGPT | Hands-free voice (speech-to-speech, handles road noise better) |
| Claude.ai | Deep research, longer conversations, planning |
| Claude Code | Dev work, repo management, structured tasks |

---

## Future: Suggestions Route to Business Canon

When a personal workflow or finding has clear business application, the method
for surfacing it to business canon is TBD. For now: note it in current_state.md
under a "Suggestions for canon" section and handle in a gov session.
