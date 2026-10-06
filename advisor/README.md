# Counsel: a daily tactical advisor

A private adviser in the Talleyrand and Machiavelli school that you talk to every day, reads your MBTI profiles of the people around you, and remembers what you said you would do. It runs entirely on the Claude subscription you already pay for. There is no API key, no server and no per-message bill.

## What is in this folder

| Path | What it is |
|---|---|
| `prompt/advisor.md` | The advisor's persona, rules and tactical lens. Edit this to change how it thinks and speaks. |
| `profile/` | Your MBTI system exports and standing notes. Gitignored except the README and the example. |
| `journal/` | One debrief per day, written by the Claude Code skill. Gitignored. |
| `start-counsel.bat` | Double-click to open a counsel session in Claude Code. |
| `../.claude/skills/counsel/SKILL.md` | The Claude Code skill. Type `/counsel` in Claude Code with this repo open. |

## Two ways to use it

Both use the same `prompt/advisor.md`, so the advisor is the same person either way.

### A. Claude Project (talk to it anywhere, including by voice on your phone)

1. In the Claude app or claude.ai, go to Projects and create one called Counsel.
2. Open the project's instructions and paste the whole of `prompt/advisor.md`.
3. Under project knowledge, upload your MBTI export (CSV or text) and `profile/notes.md` if you keep one.
4. Each day, open the project and start a chat. On the phone app, use the microphone to dictate and the read-aloud option to hear replies.
5. When the advisor says "Worth adding to your notes file", add the line to `notes.md` and re-upload it. Once a week is enough.

Trade-off: project knowledge is a snapshot. When your MBTI system changes, you upload the new export. Memory between chats depends on Claude's memory feature on your plan plus the notes file.

### B. Claude Code skill (reads your files live and keeps a journal)

1. Open this repo in Claude Code (desktop app or terminal) on the machine that holds your MBTI system.
2. Export the MBTI system into `profile/` as CSV, text or Markdown. See `profile/README.md`.
3. Type `/counsel` for a morning brief, `/counsel debrief` for the evening, `/counsel read <name>`, `/counsel wargame` or `/counsel draft`. Or double-click `start-counsel.bat`.
4. At the end, say "done" or "log it". The skill writes `journal/<today>.md` and reads the last three days back next time.

Trade-off: you need to be at the computer with the repo open. In exchange the advisor sees your profile files as they are now, updates `notes.md` for you when you say yes, and has a real day-by-day memory.

## Cost

Both routes draw on your subscription's normal usage allowance. Neither adds a bill. If you ever want it on a phone without the Claude app, or wired into a website, that would need the API, which is billed per token on top of your plan. That path is deliberately not built here.

## Privacy

`profile/` and `journal/` hold names and judgements about real people. They are gitignored so they never reach this public repository. Do not commit them, and do not paste them into a shared chat.

## Linking your MBTI system

The skill reads whatever you put in `profile/`. If the system is a spreadsheet, export the sheet to CSV. If it is an app or a database, say what it is and a small exporter can be added that writes the CSV for you.
