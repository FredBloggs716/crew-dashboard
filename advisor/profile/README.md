# Profile library

Anything you drop in this folder is read into the advisor's context on every message. This is how the advisor links to your MBTI system.

Accepted file types: `.txt`, `.md`, `.csv`, `.tsv`, `.json`. Other files are ignored. Keep the total under about 150,000 characters (roughly 40,000 words) or the advisor will warn you at startup.

Suggested files:

- `people.csv` or `people.md` exported from your MBTI system. One row or section per person: name, role, type, and any notes on how they behave.
- `notes.md` for standing facts: current negotiations, who owes you what, commitments you have made, patterns you want the advisor to track. When the advisor says "Worth adding to your notes file", paste the line in here.
- `me.md` for your own type and how you know you behave under pressure. The advisor will use it against you when it is useful.

Everything in this folder except this README and `example-profile.csv` is ignored by git, so names and notes never reach the public repo.

If your MBTI system is a spreadsheet, export the sheet as CSV into this folder. If it is something else, say what it is and the server can be given a reader for it.
