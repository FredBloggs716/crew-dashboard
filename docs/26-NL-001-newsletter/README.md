# 26-NL-001 · Site Report — Issue 01 (Autumn 2026)

Company newsletter covering **17 July – 16 September 2026**: jobs signed off,
sites running now, and what starts next.

| File | Use |
|---|---|
| `newsletter.html` | The newsletter. Self-contained but for `assets/` |
| `assets/` | LGH mark, primary logo, three site/fleet photographs |

Published as an Artifact: https://claude.ai/artifact/YM6enH9iHVd9nCYeQ85Av7

## Brand tokens

Taken from the crew dashboard (`index.html`) so screen and print match — same
set used by `docs/26-FM-001-fleet-manager-tor`.

| Token | Value | Use |
|---|---|---|
| Crimson | `#B11722` | Section rules, accents, programme bars, masthead keyline |
| Crimson dark | `#8E1019` | Hover / pressed states |
| Ink | `#16191C` | Masthead and footer band, headings |
| Steel | `#23272B` | Body text |
| Mute | `#6B7177` | Captions, metadata, eyebrows |
| Line | `#E4E7EA` | Card borders, table rules |
| Green / Amber / Blue | `#1E8E4A` / `#B7791F` / `#1F5FB2` | Status chips and stat tiles |

Type: **Archivo** (display), **IBM Plex Sans** (body), **IBM Plex Mono** (dates,
values, percentages). Loaded from Google Fonts with system fallbacks.

Dark mode is supported at token level — bare `:root` carries the full light
palette, redefined under `prefers-color-scheme: dark` and `[data-theme="dark"]`.

## Sources

- Notion **Projects** register (`LG Howson Operations Hub / Projects`) — status,
  client, start and end dates
- Notion project pages — Forest Valley Court, Clifton Road, 73 West Street,
  Solent Grange, Norry Smith, Stanpit, Horton Commercials
- Planning meeting, 8 September 2026 (Notion meeting notes)
- Photography: Google Drive `photos/` — `aerial-site.jpg`,
  `site-foundations-wide.jpg`, `fleet-row.jpg`

## Voice

From v5 the job narratives are written for the crew, not for a client file —
what the job means and why it is worth doing, rather than a list of facts.
Programme dates, scope and trade detail are unchanged and still accurate; only
the framing moved. Keep that register for future issues.

## Outstanding — new kit section needs real detail

Section 04 (**New on the fleet**) carries a new van and a new roller, both with
`[ make / model ]` shown in the house tinted-field style because **neither
appears in any system**:

- Not in the Vehicle & Plant Register (`4b381c1e…`) — that database is empty
- Not in the People & HR *Vehicles & Plant* database — newest purchase there is
  an Isuzu DMAX V-Cross dated Sept 2024, and there is no roller of any kind
- Not in Gmail across the last 120 days
- Not in Notion search

Fill in make, model and the month each landed before this issue goes out, and
add both to the Vehicle & Plant Register so the next issue can pick them up
automatically.

## Caveats carried into the copy

- Programme bars show **time elapsed against programme**, not percentage of
  work complete. Labelled as such on the page.
- Horton Commercials is marked Complete on the register with no completion date
  and an open task list, so it is excluded from the completed count. The
  on-page register note flagging this was removed in v4 at the client's
  request — the data issue still stands, it is just no longer surfaced to
  readers.
- Stanpit has no recorded completion date; "August 2026" comes from the
  Projects page archive list.
- Silver Cranes, Benham Estate, Timbertoft and Venom appear only in the
  auto-transcribed 8 September meeting notes and are not on the register —
  spellings and details need confirming before this goes outside the company.
- **No job values, contract sums or costs appear anywhere in the newsletter.**
  Removed at the client's request in v2 — the stat strip, job cards, pipeline
  timeline and tender section carry programme and scope detail instead.
- **No forward work is identifiable.** In v3 the pipeline was anonymised for
  commercial confidentiality: site names, addresses, build names and client
  names are out of the "Coming up" timeline, the tender table was replaced by a
  count, and the "also open on the register" job list became a bare number.
  Forward entries carry timing, trade and crew only. A visible notice on the
  page states that sites and clients are withheld.
- **Current sites are still named** (Forest Valley Court, Clifton Road,
  73 West Street, Solent Grange, Martinique Farm, Plantation Bungalow) along
  with their clients. This is a deliberate split — a live site with hoardings
  and liveried plant is already visible — but it has not been confirmed with
  the client, so check before external circulation.
- Commercially sensitive material from the same meeting (debtor balances,
  supplier margins, individual performance) is deliberately excluded.
