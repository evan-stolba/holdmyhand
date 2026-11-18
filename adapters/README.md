# Using holdmyhand outside Claude

The skill is written in plain Markdown, so it works with other AI assistants. `SKILL.md` is the core; everything in `references/` is extra detail the assistant reads when needed. Claude loads these files automatically. Other tools need a little setup.

Whatever tool you use, the confidentiality rules are the same: check your company's approved tools, use a work account, and review that account's data-retention and training settings.

## Claude (reference setup)

- **Claude.ai / Claude app:** zip the `holdmyhand` folder and upload it under **Settings > Capabilities > Skills**.
- **Claude Code:** copy the folder to `~/.claude/skills/holdmyhand/` (personal) or `.claude/skills/holdmyhand/` in a project.

## Gemini

**Gemini app (Gems):**
1. Open Gemini > **Gems** > **New Gem**. Name it "holdmyhand".
2. In **Instructions**, paste the body of `SKILL.md` (everything below the `---` front matter), then paste the text from `gems-and-gpts-preamble.md` at the very top.
3. Under **Knowledge**, upload the files from `references/` (and `references/playbooks/`, `references/tools/`) as long as the total fits the upload limit. Most important, in order: `confidentiality.md`, `teaching-method.md`, `output-standards.md`, `output-templates.md`, then the playbooks and tool guides you use most.
4. Upload `scripts/README.md` too, so it can explain the redaction tools. Share `redact.py` / `redact.html` with users separately (don't upload data through the Gem).

**Gemini CLI:** put the folder in your project and create a `GEMINI.md` at the project root containing:

```markdown
@holdmyhand/SKILL.md

When the instructions mention a file in references/ or scripts/, read it from the holdmyhand/ folder.
```

(Gemini CLI supports `@file` imports in GEMINI.md. If your version doesn't, paste the SKILL.md body in instead.)

## ChatGPT

**Custom GPT (best):**
1. **Explore GPTs > Create > Configure.** Name it "holdmyhand".
2. **Instructions:** paste the preamble from `gems-and-gpts-preamble.md`, then the body of `SKILL.md`. If it's over the character limit, keep the SKILL.md sections in order and drop "Other files".
3. **Knowledge:** upload the `references/` files as above.
4. Turn off capabilities you don't need. If your workspace has a setting for whether conversations can be used to improve models, check it matches your company's policy.

**Custom instructions only** (no GPT builder): these have a small character limit, so paste the short version in `custom-instructions-short.md`. It keeps the core behaviors (intake, sensitivity tiers, hard stops, step-by-step with check-ins, How to check this) but not the playbooks.

## Keeping versions in sync

Treat this folder (or its GitHub repo) as the single source of truth. When you change `SKILL.md` or a reference file, re-paste or re-upload it in each tool. Record the version/date at the top of each Gem or GPT's instructions so you can tell which copy is current.
