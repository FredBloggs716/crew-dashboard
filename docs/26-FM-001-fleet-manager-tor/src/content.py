# -*- coding: utf-8 -*-
"""Document body — content preserved verbatim from 26-FM-001 v1.0."""
from lib_ooxml import *
from style import *

DOC_REF   = "26-FM-001"
DOC_VER   = "1.0"
DOC_STATE = "DRAFT"
DOC_DATE  = "13 September 2026"
DOC_TITLE = "Fleet Manager and Mechanical Services"
DOC_SUB   = "Terms of Reference"


# ------------------------------------------------------------------ cover page
def cover(mark_rid):
    o = []

    # Brand lockup: mark + wordmark, borderless table for exact baseline control
    lockup_r = (
        para(run("LG HOWSON LTD", font=DISPLAY, sz=26, b=True, color=INK, spacing=70),
             before=0, after=40, line=290, line_rule="exact")
        + para(run("Groundworks and Civil Engineering  ·  Ringwood", **SMALL_KW),
               before=0, after=0, line=230, line_rule="exact")
    )
    o.append(table(
        [row([
            cell(para(image(mark_rid, 630000, 630000, "LGH mark"), before=0, after=0),
                 1180, valign="center", margins=(0, 0, 0, 0)),
            cell(lockup_r, W - 1180, valign="center", margins=(0, 240, 0, 0)),
        ], height=1080)],
        [1180, W - 1180],
        borders={'top': None, 'left': None, 'bottom': None, 'right': None,
                 'insideH': None, 'insideV': None},
    ))

    o.append(para(before=0, after=0, line=140, line_rule="exact",
                  borders={'bottom': (24, CRIMSON, 10)}))
    o.append(spacer(1500))

    # Status chip
    o.append(table(
        [row([cell(
            para(run(f"{DOC_STATE}  ·  FOR DISCUSSION", font=DISPLAY, sz=16,
                     b=True, color=WHITE, spacing=40),
                 before=0, after=0, line=210, line_rule="exact", jc="center"),
            3480, shade=CRIMSON, margins=(80, 0, 85, 0))],
            height=340)],
        [3480],
        borders={'top': None, 'left': None, 'bottom': None, 'right': None,
                 'insideH': None, 'insideV': None},
    ))
    o.append(spacer(320))

    o.append(para(run(DOC_TITLE, font=DISPLAY, sz=58, b=True, color=INK),
                  before=0, after=90, line=660, line_rule="exact"))
    o.append(para(run(DOC_SUB, font=DISPLAY, sz=34, color=CRIMSON),
                  before=0, after=0, line=420, line_rule="exact"))
    o.append(spacer(700))

    o.append(field_table([
        ("Document reference", DOC_REF),
        ("Version",            f"{DOC_VER} — DRAFT for discussion"),
        ("Date",               DOC_DATE),
        ("Company",            "LG Howson Ltd"),
        ("Contractor / post holder", "Alex Kidd"),
        ("Owner",              "Dean Bradley, Managing Director"),
        ("Status",             "Not for signature until Sections 1, 9 and 10 are completed"),
    ]))

    o.append(spacer(380))
    o.append(callout(
        "This document defines a role. It does not by itself determine employment "
        "status. Complete Section 1.3 before signature.",
        label="Before you sign"))

    o.append(spacer(1780))
    o.append(para(
        run("LG Howson Ltd  ·  Ringwood, Hampshire", font=BODY, sz=16, color=MUTE)
        + tab_run()
        + run(f"{DOC_REF}  ·  v{DOC_VER}", font=MONO, sz=16, color=MUTE),
        before=0, after=0, line=240, line_rule="exact",
        tabs=[("right", W)], borders={'top': (4, LINE, 8)}))
    return ''.join(o)


# --------------------------------------------------------------------- contents
SECTIONS = [
    ("s01", "1", "Purpose and standing"),
    ("s02", "2", "Fleet in scope"),
    ("pa",  None, "Part A — Fleet management (standing duty)"),
    ("s03", "3", "Statutory and regulatory compliance"),
    ("s04", "4", "Planned maintenance and availability"),
    ("s05", "5", "Parts, suppliers, hire and cost"),
    ("s06", "6", "Records and system of record"),
    ("s07", "7", "Reporting cadence"),
    ("pb",  None, "Part B — Mechanical services (booked work)"),
    ("s08", "8", "Mechanical duties"),
    ("s09", "9", "Authority and limits"),
    ("s10", "10", "Time, commitment and remuneration"),
    ("s11", "11", "Company obligations"),
    ("s12", "12", "Restrictions"),
    ("s13", "13", "Out of scope"),
    ("s14", "14", "Measures and review"),
    ("s15", "15", "Acceptance"),
    ("apa", None, "Appendix A  ·  Fleet asset register and commencement survey"),
    ("apb", None, "Appendix B  ·  Compliance register, minimum content"),
    ("apc", None, "Appendix C  ·  Measures"),
]


def contents():
    o = [para(run("CONTENTS", font=DISPLAY, sz=17, b=True, color=CRIMSON, spacing=70),
              page_break=True, before=0, after=60, line=240, line_rule="exact")]
    o.append(para(run("Terms of Reference", font=DISPLAY, sz=32, b=True, color=INK),
                  before=0, after=200, line=380, line_rule="exact",
                  borders={'bottom': (8, CRIMSON, 8)}))
    for anchor, num, title in SECTIONS:
        label = f"{num}    {title}" if num else title
        o.append(toc_entry(label, anchor, bold=(num is None)))
    o.append(spacer(500))
    o.append(callout(
        "Items shown in a tinted box, for example [ name ] or £[        ], are "
        "outstanding and must be completed before signature. Sections 1.3, 9 and 10 "
        "carry the majority of them.",
        label="Reading this document", tone="grey"))
    return ''.join(o)


# ------------------------------------------------------------------------ body
def part_one():
    o = []
    o.append(h1("1", "Purpose and standing", anchor="s01", page_break=True))
    o.append(clause("1.1", "This document defines the Fleet Manager and Mechanical Services role: "
                    "the duties, the authority, the reporting, the standards and the measures. It "
                    "separates a **standing management duty** (Part A) from **reactive mechanical "
                    "work** (Part B), because the two cannot be managed on the same basis."))
    o.append(clause("1.2", "This document is deliberately status-neutral. It works on either of "
                    "two routes:", after=100))
    o.append(bullet("**Route A — Employed.** This document becomes the job description and "
                    "objectives. The Subcontract Mechanic Agreement is terminated and replaced by "
                    "a contract of employment. Section 10 is replaced by salary, hours and benefits."))
    o.append(bullet("**Route B — Contract for services.** This document is attached as "
                    "Schedule 4 to the Subcontract Mechanic Agreement, and clause 5.3 of that "
                    "agreement is amended so that Part A is a standing retained duty, not a "
                    "bookable task. Section 10 records the retainer.", after=180))
    o.append(clause("1.3", "**Status must be resolved before signature.** The combination of a "
                    "standing management duty, a company van, container, tools and fuel, weekly "
                    "reporting to the Company and a defined role inside the business points "
                    "materially towards employment. Confirm the position with the Company’s "
                    "accountant or employment solicitor and record the outcome below.", after=180))
    o.append(field_table([
        ("Status route selected", "[ A — employed ]   /   [ B — contract for services ]"),
        ("Advised by", "[ name ]"),
        ("Date of advice", "[ date ]"),
    ], indent=GUTTER, label_w=2900))
    o.append(spacer(300))
    o.append(clause("1.4", "Reports to: Dean Bradley, LG Howson Ltd. Deputy approver: [ name ]."))
    o.append(clause("1.5", "Effective date: [ date ]. First formal review at 30 calendar days, "
                    "then monthly for three months, then quarterly.", after=0))

    o.append(h1("2", "Fleet in scope", anchor="s02"))
    o.append(clause("2.1", "The role covers every asset on the **Fleet Asset Register** at "
                    "Appendix A, which must be completed and signed before the effective date. "
                    "Indicative categories:", after=100))
    for b in ["Vans and cars",
              "Tippers and other goods vehicles, including any over 3,500 kg GVW",
              "Plant trailers and towed equipment",
              "Excavators, dumpers, rollers, telehandlers",
              "Small plant, breakers, compactors, generators, pumps",
              "Lifting accessories: chains, slings, shackles, quick hitches, lifting eyes"]:
        o.append(bullet(b))
    o.append(spacer(120))
    o.append(clause("2.2", "Assets are added to or removed from the register only by written "
                    "notice from the Company. An asset not on the register is not in scope, and "
                    "the Fleet Manager carries no responsibility for it."))
    o.append(clause("2.3", "Howson Pools Ltd assets: [ in scope / out of scope / in scope and "
                    "recharged ]. Where in scope, work is authorised through LG Howson Ltd and "
                    "recharged under the agreed intercompany arrangement.", after=0))
    return ''.join(o)


def part_a():
    o = [spacer(500), bookmark("pa", part_divider(
        "PART A", "Fleet management — standing duty")), spacer(200)]

    o.append(h1("3", "Statutory and regulatory compliance", anchor="s03"))
    o.append(clause("3.1", "Maintain a live **Compliance Register** covering every in-scope "
                    "asset, showing the next due date, the responsible person and the evidence "
                    "reference. Minimum content at Appendix B."))
    o.append(clause("3.2", "Ensure nothing in the register runs overdue. Where a date cannot be "
                    "met, escalate to Dean **before** the expiry date, not after, with the asset, "
                    "the date, the consequence and the proposed action."))
    o.append(clause("3.3", "Items to be tracked and evidenced. Frequencies are indicative and "
                    "must be confirmed against the manufacturer’s schedule, the insurer’s "
                    "requirements and any Operator’s Licence undertakings:", after=100))
    for b in ["MOT and annual test",
              "Vehicle excise duty and insurance renewal",
              "Planned servicing and safety inspections",
              "LOLER thorough examination of lifting equipment and lifting accessories",
              "PUWER inspection of work equipment",
              "Tachograph calibration, and driver card and vehicle unit downloads, where applicable",
              "Quick hitch checks and excavator lifting duty certification",
              "Statutory inspections of hired-in plant, confirmed at the point of hire"]:
        o.append(bullet(b))
    o.append(spacer(120))
    o.append(clause("3.4", "**Operator’s Licence.** Establish and record whether the Company "
                    "requires a goods vehicle Operator’s Licence for any vehicle in scope, and "
                    "if so its type, the nominated Transport Manager, the disc allocation and the "
                    "inspection frequency stated in the licence undertakings. Where a licence is "
                    "held, the Fleet Manager maintains the 15-month rolling inspection planner and "
                    "the driver defect reporting records to the standard required by the Traffic "
                    "Commissioner. This does not transfer the Company’s operator duties."))
    o.append(clause("3.5", "**Drivers.** Maintain a driver register with licence category, DVLA "
                    "check date and result, and any restrictions. Licence checks at least every "
                    "six months, or more frequently where points are recorded. Flag immediately "
                    "any driver whose entitlement does not cover the vehicle they are using."))
    o.append(clause("3.6", "**Insurance fit.** Confirm before any use that the Company’s motor "
                    "policy covers the vehicle, the driver and the actual use. Report immediately "
                    "any use falling outside cover, and stop it.", after=0))

    o.append(h1("4", "Planned maintenance and availability", anchor="s04"))
    o.append(clause("4.1", "Maintain a rolling **six-week lookahead** of planned maintenance, "
                    "inspections and off-road time, issued to Dean each Friday and reconciled "
                    "against the site programme, so that plant is not removed from a live job "
                    "without notice."))
    o.append(clause("4.2", "Plan maintenance around operational demand where possible. Where a "
                    "clash is unavoidable, present the options and the consequences; the Company "
                    "decides."))
    o.append(clause("4.3", "Maintain a **defect log**. Every defect has a severity, an owner, a "
                    "next action and a date. Defects rendering an asset unsafe are marked "
                    "**DO NOT USE**, keys controlled where practicable, and Dean notified the "
                    "same day."))
    o.append(clause("4.4", "Own the daily walkaround and pre-use check regime: ensure operators "
                    "are issued check sheets, that completed sheets are collected, and that "
                    "reported defects are entered into the log within one working day. Audit "
                    "compliance monthly and report the rate.", after=0))

    o.append(h1("5", "Parts, suppliers, hire and cost", anchor="s05"))
    o.append(clause("5.1", "Source parts and consumables within the approval limits at Section 9. "
                    "Obtain comparative pricing for any single item above the quote threshold."))
    o.append(clause("5.2", "Manage the fleet supplier and hire relationships: servicing agents, "
                    "tyre supply, breakdown and recovery, plant hire, specialist inspection "
                    "bodies. Maintain contact details, account references and renewal dates."))
    o.append(clause("5.3", "Where an asset is off the road beyond the agreed tolerance, propose "
                    "the hire-versus-repair option with cost and timescale. The Company decides."))
    o.append(clause("5.4", "Reconcile fuel card transactions against vehicle and mileage monthly. "
                    "Flag anomalies."))
    o.append(clause("5.5", "Report monthly fleet spend by asset against budget, split into "
                    "labour, parts, hire, fuel and third-party.", after=0))

    o.append(h1("6", "Records and system of record", anchor="s06"))
    o.append(clause("6.1", "The system of record is [ Notion fleet database / named Google Drive "
                    "folder ]. Records held only on a personal device, in a personal notebook or "
                    "in a private messaging thread do not satisfy this role."))
    o.append(clause("6.2", "Every asset has a record holding: identification, ownership or "
                    "finance status, service history, statutory certificates, defect history, "
                    "cost history and photographs."))
    o.append(clause("6.3", "All records remain Company property and must be current at all "
                    "times, not reconstructed at review. On the ending of the role, the register "
                    "and forward schedule are handed over complete and up to date within five "
                    "working days.", after=0))

    o.append(h1("7", "Reporting cadence", anchor="s07"))
    o.append(spacer(60))
    o.append(data_table(
        ["Frequency", "Output", "To"],
        [["Daily, on active days",
          "End of work update: completed, outstanding, parts awaited, assets unavailable, next actions",
          "Dean"],
         ["Weekly, Friday",
          "Six-week maintenance lookahead and compliance exceptions", "Dean"],
         ["Monthly",
          "Fleet report: compliance status, availability, defect position, spend against budget, "
          "check-sheet audit rate", "Dean"],
         ["Immediately",
          "Any asset made unsafe, any statutory date at risk, any insurance or licence gap, any "
          "spend heading above limit", "Dean"]],
        [2050, 6062, 1300]))
    return ''.join(o)


def part_b():
    o = [spacer(560), bookmark("pb", part_divider(
        "PART B", "Mechanical services — booked work")), spacer(200)]

    o.append(h1("8", "Mechanical duties", anchor="s08"))
    o.append(clause("8.1", "Inspection, servicing, fault finding, diagnosis and repair of "
                    "in-scope assets, to the manufacturer’s requirements and applicable law, "
                    "using safe methods and suitable equipment."))
    o.append(clause("8.2", "Follow accepted work through to resolution or formal handover. Where "
                    "the fault is beyond competence, arrange approved specialist support rather "
                    "than leaving it open."))
    o.append(clause("8.3", "Complete a **job card** for every task by the end of the next working "
                    "day: asset ID, date, mileage or hours, diagnosis, work done, parts, labour, "
                    "travel, tests, outstanding defects and the competent person releasing the asset."))
    o.append(clause("8.4", "No asset returns to service without release evidence from a competent "
                    "person. Statutory examinations and specialist work require the appropriate "
                    "competence and independence; routine servicing does not substitute for them."))
    o.append(clause("8.5", "**Priority.** Company work booked or committed under this role takes "
                    "precedence over external customers during agreed committed time. Outside "
                    "committed time, external work is unrestricted, subject to Section 12.", after=0))

    o.append(h1("9", "Authority and limits", anchor="s09"))
    o.append(spacer(60))
    o.append(data_table(
        ["Item", "Limit"],
        [["Parts or repair, single item, no prior approval", "£[        ]"],
         ["Parts or repair, per asset per month, no prior approval", "£[        ]"],
         ["Comparative quotes required above", "£[        ]"],
         ["Plant or vehicle hire", "Prior written approval in all cases"],
         ["Engaging a third-party supplier at Company cost", "Prior written approval above £[        ]"],
         ["Emergency make-safe action, no prior approval", "£[        ] , notify Dean same day"],
         ["Approver", "Dean Bradley;  deputy [ name ]"]],
        [5312, 4100]))
    o.append(spacer(260))
    o.append(clause("9.1", "**No splitting of orders** to stay under a limit. Where approval "
                    "cannot be obtained, stop and seek instructions; take only the minimum action "
                    "reasonably necessary to prevent imminent harm.", after=0))

    o.append(h1("10", "Time, commitment and remuneration", anchor="s10"))
    o.append(clause("10.1", "**Committed time.** [    ] days or [    ] hours per week for Part A "
                    "fleet management, on [ days ]. This is a standing commitment, not a bookable "
                    "slot, and is not displaced by external work without prior agreement."))
    o.append(clause("10.2", "Part B mechanical work is booked in addition and confirmed in "
                    "writing under clause 4.2 of the Subcontract Mechanic Agreement, or forms "
                    "part of the employed hours under Route A."))
    o.append(clause("10.3", "Remuneration:", after=140))
    o.append(data_table(
        ["Item", "Agreed detail"],
        [["Part A retainer or salary", "£[        ] per [ month / annum ]"],
         ["Part B rate", "£[        ] per hour  OR  £[        ] per day of [    ] hours"],
         ["Travel, call out, out of hours", "£[        ]  /  £[        ]  /  £[        ]"],
         ["Parts markup", "[ at cost  /  [    ]% markup ]"],
         ["Asset use: van, container, tools, fuel",
          "[ no cash charge, forming part of the consideration  /  £[        ] per [    ] ]"],
         ["Tax and VAT treatment of asset use confirmed by", "[ name ] on [ date ]"],
         ["Rate review", "Annually on [ date ], by written agreement only"]],
        [4100, 5312]))
    o.append(spacer(260))
    o.append(clause("10.4", "The asset-use arrangement at 10.3 must be checked for tax, VAT and "
                    "benefit-in-kind treatment before signature. A “no cash charge” "
                    "arrangement is consideration in kind, not an absence of value.", after=0))

    o.append(h1("11", "Company obligations", anchor="s11"))
    for n, t in [
        ("11.1", "Provide the complete asset register, ownership and finance status, and "
                 "available service history at commencement."),
        ("11.2", "Provide safe access to assets, a suitable and safe working location, and "
                 "reasonable notice of operational demands."),
        ("11.3", "Make decisions and give approvals within [ one working day ] of a properly "
                 "presented request, or accept the consequence of the delay."),
        ("11.4", "Maintain motor and plant insurance, and confirm in writing that cover extends "
                 "to the Fleet Manager, any approved substitute and the actual use."),
        ("11.5", "Retain and discharge the Company’s own duties as owner, operator and "
                 "employer. Nothing in this document transfers those duties."),
        ("11.6", "Resolve the land position for the 40 ft container, including the "
                 "landholder’s identity and the access and collection arrangement, and record "
                 "it at Appendix A."),
    ]:
        o.append(clause(n, t))
    o[-1] = o[-1].replace('w:after="140"', 'w:after="0"')

    o.append(h1("12", "Restrictions", anchor="s12"))
    for n, t in [
        ("12.1", "Company assets — van, container, tools, parts, fuel and accounts — are "
                 "for authorised Company work only, except where a specific written permission is "
                 "recorded in Schedule 2 of the Subcontract Mechanic Agreement."),
        ("12.2", "No servicing or repair of another customer’s vehicles or plant in the "
                 "Company container, or using Company tools, parts or fuel, without express "
                 "written permission."),
        ("12.3", "During this role and for [ 6 ] months afterwards, do not solicit the "
                 "Company’s clients, staff or subcontractors for competing services. This "
                 "restriction is limited to what is reasonably necessary to protect the "
                 "Company’s business connections."),
        ("12.4", "Disclose in writing any existing or proposed work for a competitor of the "
                 "Company, or any arrangement that could conflict with the fleet role, before "
                 "accepting it."),
        ("12.5", "Confidential information — customer, pricing, fleet, cost and security "
                 "information — is used only for authorised purposes and is not held on a "
                 "personal device as the sole copy."),
    ]:
        o.append(clause(n, t))
    o[-1] = o[-1].replace('w:after="140"', 'w:after="0"')

    o.append(h1("13", "Out of scope", anchor="s13"))
    o.append(body("For the avoidance of doubt, the role does not include:", after=100))
    for b in ["Undisclosed pre-existing defects not identified in the commencement survey at Appendix A",
              "Statutory examinations requiring an independent competent person",
              "Asset purchase and disposal decisions, which remain with the Company",
              "Operator’s Licence holding or Transport Manager duties, unless separately and "
              "expressly appointed",
              "Site operational decisions on plant deployment"]:
        o.append(bullet(b))

    o.append(h1("14", "Measures and review", anchor="s14"))
    o.append(clause("14.1", "Performance is measured against Appendix C. These are service "
                    "standards, not automatic financial penalties."))
    o.append(clause("14.2", "Review points: 30 days from the effective date, then monthly for "
                    "three months, then quarterly. Each review records the evidence, Alex’s "
                    "response, the agreed outcome, and the actions with owners and dates."))
    o.append(clause("14.3", "Where a measure is missed, the Company will state the fact, the "
                    "impact and the required correction with a reasonable deadline, and allow a "
                    "response, before any formal step under clause 12 of the Subcontract Mechanic "
                    "Agreement or the applicable employment procedure."))
    o.append(clause("14.4", "This document may be varied only in writing, signed by both "
                    "parties.", after=0))
    return ''.join(o)


def acceptance():
    o = [h1("15", "Acceptance", anchor="s15", page_break=True)]
    o.append(body("We agree the role, duties, authority, measures and commercial particulars "
                  "set out above and in Appendices A to C.", after=300))
    o.append(signature_block("For LG Howson Ltd",
                             ["Name and position", "Signature", "Date"]))
    o.append(spacer(480))
    o.append(signature_block("Alex Kidd  [ personally / for [ entity ] ]",
                             ["Name and capacity", "Signature", "Date"]))
    o.append(spacer(600))
    o.append(callout(
        "Do not sign until Section 1.3 (status route), Section 9 (authority limits) and "
        "Section 10 (time and remuneration) are complete, and Appendix A is completed, "
        "photographed and signed.",
        label="Completion check", tone="grey"))
    return ''.join(o)


def appendices():
    o = [appendix_h1("Appendix A", "Fleet asset register and commencement survey", anchor="apa")]
    o.append(body("To be completed jointly and photographed before the effective date. One row "
                  "per asset; copy the block as required.", left=0, after=220))
    o.append(data_table(
        ["Field", "Entry"],
        [[f, ""] for f in [
            "Asset type and description",
            "Registration / serial / fleet number",
            "Year, make, model",
            "Legal owner / finance or hire agreement",
            "Current location and keeper",
            "Mileage or hours at survey",
            "Last service and next due",
            "Last MOT or test and next due",
            "Last statutory examination and next due",
            "Known defects at survey",
            "Condition and photograph reference",
            "In scope from"]],
        [3800, 5612], min_height=620))
    o.append(spacer(420))
    o.append(para(run("Container position", font=DISPLAY, sz=21, b=True, color=CRIMSON_DK),
                  keep_next=True, before=0, after=140, line=280, line_rule="exact"))
    o.append(data_table(
        ["Item", "Position"],
        [["Landholder", "[                    ]"],
         ["Written access permission", "[ attached / outstanding ]"],
         ["Collection arrangement", "[                    ]"],
         ["Resolved by", "[ date ]"]],
        [3800, 5612]))

    o.append(appendix_h1("Appendix B", "Compliance register, minimum content", anchor="apb"))
    o.append(body("Frequencies below are indicative. Confirm each against the "
                  "manufacturer’s schedule, the insurer’s requirements and any "
                  "Operator’s Licence undertakings before the register goes live.",
                  left=0, after=220))
    o.append(data_table(
        ["Item", "Applies to", "Frequency", "Evidence held"],
        [["MOT / annual test", "Vehicles and trailers as applicable", "Annual, or per class", "Certificate"],
         ["Vehicle excise duty", "Road-going vehicles", "Annual", "DVLA record"],
         ["Motor insurance", "Road-going vehicles", "Per policy", "Policy schedule"],
         ["Safety inspection", "Goods vehicles under an O-Licence", "Per licence undertaking", "Inspection sheet"],
         ["Planned service", "All powered assets", "Per manufacturer", "Job card"],
         ["LOLER thorough examination", "Lifting equipment and accessories", "Per regulation and duty",
          "Report of thorough examination"],
         ["PUWER inspection", "Work equipment", "Per risk assessment", "Inspection record"],
         ["Quick hitch check", "Excavators", "Per manufacturer", "Check record"],
         ["Tachograph calibration", "Where fitted and in scope", "Per regulation", "Calibration certificate"],
         ["Tachograph downloads", "Where applicable", "Driver card and vehicle unit, per regulation",
          "Download log"],
         ["Driver licence check", "All drivers", "Six-monthly minimum", "DVLA check record"],
         ["Daily walkaround check", "Vehicles and plant in use", "Each day of use", "Check sheet"],
         ["Hired-in plant certification", "All hire", "At point of hire", "Supplier certificate"]],
        [2500, 2600, 2312, 2000]))

    o.append(appendix_h1("Appendix C", "Measures", anchor="apc"))
    o.append(body("Service standards for the role. Measured at each review point under "
                  "Section 14.", left=0, after=220))
    o.append(data_table(
        ["Measure", "Target", "Evidence"],
        [["Statutory items overdue", "Zero at all times", "Compliance register"],
         ["Statutory items at risk escalated before expiry", "100%", "Escalation record"],
         ["Fleet availability, in-scope assets fit for use", "[    ]% monthly", "Defect log and register"],
         ["Unplanned off-road days", "Below [    ] per month", "Defect log"],
         ["Committed time honoured", "100%, exceptions agreed in advance", "Attendance log"],
         ["Accepted booking displaced by external work without agreement", "Zero", "Booking record"],
         ["Job card completed by end of next working day", "100%", "Job cards"],
         ["Weekly six-week lookahead issued by Friday", "100%", "Issued report"],
         ["Monthly fleet report issued by [ working day ]", "100%", "Issued report"],
         ["Daily check sheets returned and logged", "[    ]%", "Monthly audit"],
         ["Spend within approval limits", "100%", "Purchase records"],
         ["Fleet spend against budget", "Within [    ]%", "Monthly report"],
         ["Unapproved private use of Company assets", "Zero", "Inspection and fuel reconciliation"]],
        [4300, 2650, 2462]))
    o.append(spacer(500))
    o.append(para(
        run("End of document", font=DISPLAY, sz=17, b=True, color=MUTE, spacing=60),
        jc="center", before=0, after=0, line=240, line_rule="exact",
        borders={'top': (4, LINE, 10)}))
    return ''.join(o)
