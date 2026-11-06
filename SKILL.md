---
name: envdrop
description: Get API keys, tokens, passwords or any secret/env var from the user without seeing them. Use whenever the task needs a credential that isn't set yet (e.g. OPENAI_API_KEY, SUPABASE_URL, STRIPE_SECRET_KEY), INSTEAD of asking the user to paste it in chat or to edit .env and say "done". Opens one masked input window, waits, saves to .env.
---

# envdrop

Never ask the user to paste a secret in chat or to edit `.env` themselves. Do this instead:

1. Find the exact variable names this project uses (code, `.env.example`, framework docs).
2. From the project root, run the `envdrop` script that sits next to this SKILL.md, with a long timeout (10 min). It blocks while the user fills in the window:

   ```bash
   python3 <this-skill-dir>/envdrop ask OPENAI_API_KEY SUPABASE_URL
   ```

   With no names, it asks for every key in `.env.example` (or left empty in `.env`) that has no value yet.
3. Tell the user in one line that an input window is open.
4. Read the output:
   - `envdrop: saved A, B to /path/.env (mode 600).` means the values are saved; continue the task.
   - `Skipped: X` or `cancelled` (exit 1) means ask the user once whether to retry or skip.

Rules:
- Never `cat`, `grep`, `head` or print the env file, and never echo a secret. Use the values by reference: let the app load `.env`, or `set -a; . /path/.env; set +a; <command>`.
- To save somewhere other than `./.env`, run `ENVDROP_FILE=/path envdrop ask ...`.
