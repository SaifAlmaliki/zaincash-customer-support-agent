"""Add the evaluation plan to slide 5 without dropping risks, the schedule, or the repo link."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

PATH = (
    "/home/cvzmh_saif/dev/zaincash-support/presentation/"
    "SaifAlmaliki_Topic06_FAZAA_Design_Brief.pptx"
)

NAVY = RGBColor(0x14, 0x2C, 0x3B)
TEAL = RGBColor(0x08, 0x7E, 0x83)
INK = RGBColor(0x20, 0x39, 0x47)
MUTED = RGBColor(0x53, 0x68, 0x73)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CHIP = RGBColor(0xE7, 0xF3, 0xF1)
LINE = RGBColor(0xD9, 0xE3, 0xE7)

METRICS = [
    (
        "Classification",
        "Accuracy and macro-F1. Write up the top 3 confusions.",
    ),
    (
        "Priority and fraud",
        "Exact priority, and within one level. Fraud-flag recall is the safety headline.",
    ),
    (
        "Extraction",
        "Exact match on each field. Count invented values and missed fields.",
    ),
    (
        "Routing",
        "Team and lookup accuracy. Accuracy on tickets we keep, against coverage.",
    ),
    (
        "Draft quality",
        "Guardrail pass rate and valid citations. 30 hand ratings: send with minor edits?",
    ),
    (
        "Protected test",
        "Tune on 200. Hold out 100. Commit the hash first. One run: Jev, Gemini, cascade.",
    ),
]

LEAD = (
    "Right category, team and priority — or an escalation that says why. "
    "Details that appear in the ticket. A cited Iraqi-Arabic draft that never asks "
    "for an OTP, PIN or password. A person approves, edits or rejects. Nothing is sent."
)

NOTE = """

EVALUATION PLAN added 18 October 2026 (design spec section 7). This is the measurement plan, not a result.
A good result, on judge input and on the held-out set: the category, priority and team match the label, or the ticket is escalated with a reason when confidence is low; every extracted amount, date, phone and reference appears in the ticket (a value predicted where gold is null is a hallucination); the draft cites a policy passage, uses only known numbers, and does not ask for an OTP, PIN or password; a reviewer approves, edits or rejects. There is no send path.
Protocol: about 300 synthetic Iraqi-dialect tickets, stratified across 12 categories. Labels come from code; a model writes the text; code checks that every gold value appears in the text. Seed-42 split, 200 dev and 100 test. Commit test.sha256 before tuning prompts, thresholds or wording. Tune on dev only, freeze, then run the test set once for jev, gemini and cascade and commit those three results.
Also measured, and named in the speaker script if the slide is tight: per-flag precision as well as fraud recall; reliability diagram and expected calibration error; an LLM judge for correctness, tone, dialect and actionability beside the 30 human ratings; throughput, p50/p95 latency and cost per ticket; separate scores for Arabizi, mixed language, multi-issue, missing details and prompt injection.
Known bias: Gemini helps generate the tickets and may also judge drafts. Human ratings are the check. Say so. pytest and ruff guard the rules, lookup and draft checks; they are not the held-out score.
As of this brief, Plan 2 held-out evaluation has not been run. The five-ticket smoke runs and the 17 October RAG demo are not this test set. The 6–8 November milestone is when the first held-out numbers are committed.
Risks, the week-by-week plan and the GitHub link were already on this slide. The link is https://github.com/SaifAlmaliki/zaincash-customer-support-agent
"""


def inches(value):
    return Inches(value)


def set_run_font(run, name="Arial"):
    run.font.name = name
    r_pr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = r_pr.find(qn(tag))
        if el is None:
            el = r_pr.makeelement(qn(tag), {})
            r_pr.append(el)
        el.set("typeface", name)


def write(shape, text, size, bold, color, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    frame = shape.text_frame
    frame.word_wrap = True
    frame.auto_size = None
    frame.margin_left = inches(0.08)
    frame.margin_right = inches(0.08)
    frame.margin_top = inches(0.02)
    frame.margin_bottom = inches(0.02)
    frame.paragraphs[0].alignment = align
    # Clear extra paragraphs, keep one run.
    paragraph = frame.paragraphs[0]
    if paragraph.runs:
        paragraph.runs[0].text = text
        run = paragraph.runs[0]
        for extra in paragraph.runs[1:]:
            extra.text = ""
    else:
        run = paragraph.add_run()
        run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    set_run_font(run)
    body = frame._txBody.find(qn("a:bodyPr"))
    body.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr"}[anchor])


def fill_rect(shape, color, line=None):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)


def add_text(slide, name, x, y, w, h, text, size, bold, color, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    shape = slide.shapes.add_textbox(inches(x), inches(y), inches(w), inches(h))
    shape.name = name
    write(shape, text, size, bold, color, align, anchor)
    return shape


def add_box(slide, name, x, y, w, h, color, line=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, inches(x), inches(y), inches(w), inches(h)
    )
    shape.name = name
    fill_rect(shape, color, line)
    # Keep the rectangle from showing a leftover empty paragraph in a loud font.
    frame = shape.text_frame
    frame.word_wrap = False
    paragraph = frame.paragraphs[0]
    if paragraph.runs:
        paragraph.runs[0].text = ""
    return shape


def move(shape, x, y, w, h):
    shape.left = inches(x)
    shape.top = inches(y)
    shape.width = inches(w)
    shape.height = inches(h)


def shrink_font(shape, size):
    if not shape.has_text_frame:
        return
    for paragraph in shape.text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(size)
            set_run_font(run)
    frame = shape.text_frame
    frame.word_wrap = True
    frame.margin_left = inches(0.04)
    frame.margin_right = inches(0.04)
    frame.margin_top = inches(0.0)
    frame.margin_bottom = inches(0.0)


def replace_run(shape, text):
    paragraph = shape.text_frame.paragraphs[0]
    paragraph.runs[0].text = text


def main():
    prs = Presentation(PATH)
    slide = prs.slides[4]
    shapes = {shape.name: shape for shape in slide.shapes}
    assert shapes["title"].text_frame.paragraphs[0].runs[0].text.startswith("Risks")
    assert "github.com/SaifAlmaliki" in shapes["repo-url"].text_frame.text

    replace_run(shapes["title"], "How we test, what can go wrong, and the plan")

    # Compress the two lower cards so the measurement band fits under the header.
    move(shapes["risks"], 0.56, 5.10, 7.96, 3.26)
    move(shapes["risks-heading"], 0.78, 5.18, 7.50, 0.24)
    shrink_font(shapes["risks-heading"], 12)
    for i in range(5):
        move(shapes[f"risk-title-{i}"], 0.78, 5.46 + i * 0.56, 7.50, 0.22)
        move(shapes[f"risk-body-{i}"], 0.78, 5.68 + i * 0.56, 7.50, 0.30)
        shrink_font(shapes[f"risk-title-{i}"], 13)
        shrink_font(shapes[f"risk-body-{i}"], 12)

    move(shapes["schedule"], 8.86, 5.10, 8.36, 3.26)
    move(shapes["schedule-heading"], 9.08, 5.18, 7.90, 0.24)
    shrink_font(shapes["schedule-heading"], 12)
    for i in range(4):
        move(shapes[f"week-badge-{i}"], 9.08, 5.50 + i * 0.72, 1.72, 0.34)
        move(shapes[f"week-date-{i}"], 9.12, 5.53 + i * 0.72, 1.64, 0.28)
        move(shapes[f"week-title-{i}"], 10.98, 5.48 + i * 0.72, 5.98, 0.26)
        move(shapes[f"week-body-{i}"], 10.98, 5.76 + i * 0.72, 5.98, 0.40)
        shrink_font(shapes[f"week-date-{i}"], 11)
        shrink_font(shapes[f"week-title-{i}"], 13)
        shrink_font(shapes[f"week-body-{i}"], 12)

    add_box(slide, "test-card", 0.56, 1.78, 16.66, 3.20, WHITE, LINE)
    add_text(
        slide,
        "test-heading",
        0.74,
        1.86,
        16.28,
        0.28,
        "WHAT A GOOD RESULT LOOKS LIKE  /  HOW WE MEASURE IT",
        13,
        True,
        TEAL,
    )
    add_text(
        slide,
        "test-lead",
        0.74,
        2.14,
        16.28,
        0.52,
        LEAD,
        13,
        False,
        INK,
    )

    tile_w = 5.28
    gap = 0.16
    origin_x = 0.78
    for index, (label, body) in enumerate(METRICS):
        col = index % 3
        row = index // 3
        x = origin_x + col * (tile_w + gap)
        y = 2.72 + row * 1.08
        add_box(slide, f"metric-{index}", x, y, tile_w, 0.98, CHIP, None)
        add_text(
            slide,
            f"metric-title-{index}",
            x + 0.08,
            y + 0.06,
            tile_w - 0.16,
            0.26,
            label,
            13,
            True,
            TEAL,
        )
        add_text(
            slide,
            f"metric-body-{index}",
            x + 0.08,
            y + 0.32,
            tile_w - 0.16,
            0.60,
            body,
            12,
            False,
            INK,
        )

    notes = slide.notes_slide.notes_text_frame
    existing = notes.text or ""
    if "EVALUATION PLAN added" not in existing:
        notes.text = existing.rstrip() + NOTE

    prs.save(PATH)
    print("saved", PATH)


if __name__ == "__main__":
    main()
