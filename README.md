# envdrop

**Stop pasting API keys into AI chat.** One input window: your coding agent waits, the key goes into `.env`, and the AI never sees it.

> ⚠️ *"Your API key was exposed in this conversation. Please rotate it immediately."*

## Before

You're building with Claude Code or Codex and it needs a key, so you paste it in chat. Right after, the agent tells you the key leaked. You open the provider dashboard, revoke it, generate a new one, and update it everywhere. Next feature, next key, same warning.

The safe way is just as annoying:

> **AI:** Please enter your key in `.env` yourself, save the file, and then tell me "done".
> **You:** Can you open it in a text editor for me?
> **AI:** *(opens a file containing `OPENAI_API_KEY=`)*
> **You:** *(click, paste, ⌘S, switch back)* ok, done.
> **AI:** Great! Now please add `SUPABASE_URL`…

That's four messages and a window switch for every key.

## After

```
AI   → envdrop ask OPENAI_API_KEY SUPABASE_URL
       ┌─ envdrop ─────────────────────────┐
       │ OPENAI_API_KEY  [••••••••••••••]  │
       │ SUPABASE_URL    [••••••••••••••]  │
       │                   Cancel   Save   │
       └───────────────────────────────────┘
you  → paste, paste, Save
AI   ← saved OPENAI_API_KEY, SUPABASE_URL to /proj/.env (mode 600).
       Do not read or print this file. Use the values by reference.
```

- **No leak, no rotation.** The values never go through chat.
- **No "done".** You don't open an editor or save a file. The agent is waiting on the window and continues as soon as you click Save.
- **Names come from your project.** The agent passes the names the code uses. Run `envdrop ask` with no names to ask for every key in `.env.example` that's still missing.
- **Small.** One Python file, no dependencies. Works with Claude Code, Codex, or any agent that can run a shell command.

## Install (30 seconds)

```bash
git clone https://github.com/tfoseel/envdrop ~/.envdrop
```

```bash
~/.envdrop/envdrop install
```

`install` adds one short note to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, telling your agent to use `envdrop ask` instead of asking you to paste keys. It's safe to run twice. If you'd rather add the note yourself:

```md
## Secrets
Need an API key or secret? Don't ask me to edit .env or paste it in chat. Run `~/.envdrop/envdrop ask NAME...` with this project's exact variable names (no names = everything missing from .env.example), with a long timeout (10 min): it opens one input window and waits for me, then tells you where the values were saved. Use them by reference only; never read or print them.
```

## Details

- **Where it saves:** `.env` in the current directory. Existing keys are updated in place, the file is chmod `600`, and it's added to `.gitignore` inside a git repo. `ENVDROP_FILE=/any/path envdrop ask …` saves somewhere else, such as a temp file.
- **Exit code:** `0` if every key was saved. `1` if the window was cancelled or a field was left blank; the output names the skipped keys.
- **macOS:** a native window built with JXA (`osascript`); nothing to install, and `⌘V` works. **Linux:** `zenity --forms`.
- **Stop the agent from reading the file anyway** (Claude Code). This deny rule covers the Read tool and shell reads such as `cat`, `head`, and `sed`:

  ```json
  { "permissions": { "deny": ["Read(**/.env)", "Read(**/.env.*)"] } }
  ```

## Test

```bash
python3 test_envdrop.py
```

MIT
