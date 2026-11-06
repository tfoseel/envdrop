# envdrop

Coding agents keep asking for API keys. The usual dance:

> **AI:** Put `OPENAI_API_KEY` in `.env` and tell me when you're done.
> **You:** Open it in a text editor for me.
> **AI:** *(opens `OPENAI_API_KEY=`)*
> **You:** *(paste, save)* Saved.

Or you paste the key into chat, and now it's in the model's context and you should rotate it.

envdrop replaces all of that with **one input window**. The agent runs a command, a native window pops up with a masked field for each key, you paste and hit Save, and the agent continues. It never sees the values; it only learns where they were saved.

One Python file, no dependencies. Works with Claude Code, Codex, or any agent that can run a shell command.

## Protocol

```
agent  →  envdrop ask OPENAI_API_KEY DB_URL        (blocks)
you    →  [ one window · masked fields · Save ]
agent  ←  envdrop: saved OPENAI_API_KEY, DB_URL to /path/.env (mode 600).
          Do not read, cat, grep or print this file. Use the values by reference:
          let the app load it, or `set -a; . /path/.env; set +a; <command>`.
```

- **Names come from the project.** The agent passes the exact variable names the code uses. With no names, envdrop asks for every key declared in `.env.example` / `.env.sample` / `.env.template` / `.env.dist`, or left empty (`NAME=`) in `.env`, that has no value yet.
- **Where it saves:** `.env` in the current directory. Existing keys are updated in place, the file is set to `0600`, and it's added to `.gitignore` inside a git repo. `ENVDROP_FILE=/any/path envdrop ask …` saves somewhere else, such as a temp file.
- **Exit code:** `0` if every key was saved. `1` if the window was cancelled or a field was left blank; the output names the skipped keys.

## Install

```bash
git clone https://github.com/tfoseel/envdrop ~/.envdrop
```

```bash
~/.envdrop/envdrop install
```

`install` appends a short protocol note to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` (running it twice is safe). The note tells the agent to call `envdrop ask` instead of asking you to edit `.env`. Here it is, if you'd rather add it yourself:

```md
## Secrets
Need an API key or secret? Don't ask me to edit .env or paste it in chat. Run `~/.envdrop/envdrop ask NAME...` with this project's exact variable names (no names = everything missing from .env.example), with a long timeout (10 min): it opens one input window and waits for me, then tells you where the values were saved. Use them by reference only; never read or print them.
```

## Keep it from reading the file anyway

The protocol note asks the agent not to read the file. To enforce that in Claude Code, add a deny rule. It covers the Read tool and recognized shell reads such as `cat`, `head`, and `sed`:

```json
{ "permissions": { "deny": ["Read(**/.env)", "Read(**/.env.*)"] } }
```

## Platforms

- **macOS:** a native `NSAlert` window built with JXA (`osascript`); nothing to install. `⌘V` works in the fields.
- **Linux:** `zenity --forms` with a password field per key.

## Test

```bash
python3 test_envdrop.py
```

MIT
