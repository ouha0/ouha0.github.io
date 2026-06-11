---
title: "Three levels of Claude Code"
date: 2026-05-28
categories:
  - reflections
tags:
  - tools
  - ai
  - workflow
---

## Thesis

The value of Claude Code isn't that it writes code for you. It's that it
compresses the feedback loop. The three levels aren't about capability —
they're about how tight the loop between intention and result becomes.

## Target reader

Developers who are curious about Claude Code but haven't started, or who
started but stalled at the chatbot level.

---

## Outline

### 1. Opening — the moment it stopped feeling like a chatbot
- A concrete moment where Claude Code did something unexpected
- Not the most impressive thing — the moment the mental model shifted

### 2. Level 1: The chatbot
- You type a question, you get an answer. Google with better prose.
- Good for: "explain this error", "what's the difference between X and Y",
  "what does this regex do"
- The limitation: you're doing all the work of deciding what to ask, when,
  and what to do with the answer. The tool is reactive.
- The speed changes behavior — you start asking questions you wouldn't have
  bothered Googling

### 3. Level 2: Interactive session with skills
- Slash commands, CLAUDE.md, custom skills. The tool has memory and preferences.
- The shift: you stop repeating context. It knows your project.
- CLAUDE.md as institutional memory — constraints live in a file, not your head
- Context management as a skill: /compact, /clear, knowing when sessions
  get stale
- Example: custom command that scaffolds a new draft with correct front matter

### 4. Level 3: The agent
- You give a goal instead of instructions. "Fix this failing test," not
  "the test fails because X, change line Y."
- What autonomous work looks like: reads codebase, forms plan, edits files,
  runs tests, iterates on failures, presents result
- The trust question: when do you let it commit? When do you review every
  diff? How do you calibrate?
- Example: "create archive pages for all four sections" — multi-file,
  multi-step, self-verifying

### 5. What the day-to-day actually looks like
- Not a polished workflow diagram — the real thing
- When do you drop from agent mode back to interactive?
- The role of trust: verify more at first, less over time, but strategically
- CLAUDE.md as a living document — what goes in, what gets cut

### 6. What surprised me
- Speed of iteration, not generation. It tries things fast.
- Better at tasks with clear feedback loops (tests, linters, builds)
- Writing CLAUDE.md forces you to articulate things you'd left implicit
- The uncanny valley of reading code in your style that you didn't write

### 7. What it's not
- Not a replacement for knowing what you want. Vague goals -> vague results.
- It hallucinates API signatures, invents config options, "fixes" things that
  weren't broken
- The 80/20 split: handles 80% mechanical work, frees you for the 20% that
  requires judgment. That ratio is the real value.

---

## Differentiation from existing posts

Most Claude Code posts are product reviews (feature lists) or productivity
testimonials (before/after metrics). This post answers: "What does it feel
like to use this thing every day, and how does your relationship with it
change?" The three-level framing gives structure; personal examples keep it
grounded. Nobody has written about the psychological progression.

## Existing posts to be aware of
- Marmelab "Tips I Wish I'd Had" (useful but atomized, no narrative)
- Divy Yadav "3 Modes" (maps to different Anthropic products, not levels
  within Claude Code)
- Builder.io "50 Tips" (comprehensive but impersonal)
- Various Medium "How I Actually Use" posts (thin experience, clickbait)
