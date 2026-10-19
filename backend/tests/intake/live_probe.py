"""Opt-in synthetic vision check: uv run python -m tests.intake.live_probe.

Uses the configured provider, never run by pytest. Prints observations, timings
and provider-reported cost only; no credentials or customer data are logged.
"""
import asyncio
import json
import time
from io import BytesIO
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont

from app.config import Settings
from app.intake.contracts import Attachment, ImageInput
from app.intake.evidence import merge_analysis
from app.intake.model import ModelBudget, OpenRouterIntakeModel, _analysis_prompt
from app.intake.policy import assess_readiness, choose_question
from app.intake.review import build_review
from app.taxonomy import load_taxonomy
from tests.intake.helpers import context, message


async def main():
    settings = Settings()
    model = OpenRouterIntakeModel(settings)
    for readable in (True, False):
        image = Image.new("RGB", (900, 340), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("DejaVuSans.ttf", 28)
        draw.multiline_text((25, 25), "FICTIONAL DEMO - NOT A REAL RECEIPT\nReference: DEMO-2410000123\n"
                            + ("Amount: 50000 IQD\n" if readable else "Amount: [UNREADABLE]\n")
                            + "Error: DEMO TRANSFER FAILED", fill="black", font=font, spacing=20)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        aid = uuid4()
        source = message("This fictional screenshot shows my transfer problem. Read it and ask about missing details.", language="en", attachments=[aid])
        ctx = context([source], attachments=[Attachment(id=aid, filename="fictional.png", mime_type="image/png",
            size=len(buffer.getvalue()), width=900, height=340, message_id=source.id)])
        images = [ImageInput(aid, "image/png", buffer.getvalue())]
        blocks = _analysis_prompt(ctx, images)[1]
        report = {"readable": readable, "model": settings.intake_model or settings.gemini_model,
                  "timeout_s": settings.intake_timeout_s, "max_requests": settings.intake_max_model_requests,
                  "image_blocks": sum(block["type"] == "image_url" for block in blocks)}
        budget = ModelBudget(settings.intake_timeout_s, settings.intake_max_model_requests)
        started = time.monotonic()
        try:
            result = await model.analyze(ctx, images, budget)
            report["observations"] = result.value.model_dump(mode="json")
            merged = merge_analysis(ctx, result.value)
            merged.readiness = assess_readiness(merged, load_taxonomy(settings.taxonomy_path))
            question = choose_question(merged, result.value.suggested_question, 1)
            report["next_question"] = question.model_dump(mode="json") if question else None
            report["validated"] = True
            merged.readiness = assess_readiness(merged, load_taxonomy(settings.taxonomy_path), allow_partial=True)
            summary = await model.summarize(merged, "en", budget)
            review = build_review(ctx, merged, summary.value, publication=1, language="en")
            report["review"] = {"customer_text": review.customer_text, "employee_text_ar": review.employee_text_ar,
                               "quality": review.quality, "unknown_keys": review.unknown_keys}
        except Exception as error:
            report["error_type"] = type(error).__name__
            if error.__cause__ is not None:
                detail = str(error.__cause__)
                if settings.openrouter_api_key:
                    detail = detail.replace(settings.openrouter_api_key, "<redacted>")
                report["failure_detail"] = detail[:1000]
        report["latency_s"] = round(time.monotonic() - started, 3)
        report["trace"] = budget.trace
        print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
