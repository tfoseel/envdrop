# envdrop

**English** · [한국어](README.ko.md)

**Stop pasting API keys into AI chat.** One input window: your coding agent waits, the key goes into `.env`, and the AI never sees it.

> ⚠️ *"Your API key was exposed in this conversation. Please rotate it immediately."*

## Before

You've seen this a hundred times.

> **You:** add OpenAI to the app
> **AI:** Sure! I'll need your `OPENAI_API_KEY`.
> **You:** sk-proj-8fK2...
> **AI:** ⚠️ **Your API key was exposed in this conversation. Please rotate it immediately.**
> **You:** …you're the one who asked for it
> **AI:** I understand the frustration! For security, please never share secrets in chat. Instead, open `.env` yourself, paste your key, save the file, and then tell me "done".
> **You:** *(opens OpenAI dashboard, revokes key, creates new key, copies it)*
> **You:** can you at least open the file for me
> **AI:** *(opens `.env` in TextEdit)*
> **You:** *(clicks, pastes, ⌘S, ⌘Tab back)* done
> **AI:** Thanks! Now I'll also need `SUPABASE_URL` and `SUPABASE_ANON_KEY`. Please open `.env`, add them, save, and tell me "done".
> **You:** 🙃

And it isn't made up. Here's a real message from Codex:

> Ready to run locally once it can read the key.
>
> 1. Get an API key from the TypeSafe console.
> 2. Open **Keychain Access** on your Mac and add a new password item to the login keychain. Name: `codex.typesafe.jev`, account: `jev`, password: the key you got.
> 3. Don't put the key in chat. Just tell me **"done."**

So you open Keychain Access, find "New Password Item", type a service name you'll never remember, paste, save, switch back, and type "done", for one key.

Some chat apps now hide pasted keys. That's worse:

> **You:** Let's build a chat app with Gemini. Key: `AIzaSyFA•••••••••••••••••••••••••••••••`
> **AI:** Project folder created. Writing the server and UI.
> **AI:** Google rejected this key too with `API_KEY_INVALID`. I'll keep building; just swap the key in `.env`.

The key was fine. The app hid it before the AI saw it, so the AI called Google with a string of `•` and blamed your key. Now you're back to editing `.env` by hand.

Then the next feature needs a Stripe key, and you go through it again.

You end up with either:

- **a leaked key** that has to be rotated, or
- **a four-message round-trip** for every key: open the editor, paste, save, switch windows, and type "done" to a program that could have just waited.

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

envdrop is an [Agent Skill](https://agentskills.io). Clone it once, and both Codex and Claude Code pick it up:

```bash
git clone https://github.com/tfoseel/envdrop ~/.agents/skills/envdrop
```

```bash
ln -s ~/.agents/skills/envdrop ~/.claude/skills/envdrop
```

Codex reads `~/.agents/skills`, and Claude Code reads `~/.claude/skills` (the symlink). Nothing gets added to your CLAUDE.md or AGENTS.md. The agent loads the skill only when it needs a secret, and then uses `envdrop ask` instead of asking you to paste the key.

Using a different agent? Run `python3 ~/.agents/skills/envdrop/envdrop ask NAME...` yourself, or tell your agent to.

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
