from typer.testing import CliRunner

from app.cli import app


def test_stored_run_refuses_tickets_without_a_customer_phone(tmp_path):
    p = tmp_path / "tickets.jsonl"
    p.write_text('{"external_id": "A", "text": "hi"}\n', encoding="utf-8")
    result = CliRunner().invoke(app, ["run-batch", str(p)])
    assert result.exit_code == 2
    assert "customer phone" in result.output and "A" in result.output


def test_invalid_phone_is_an_input_error_not_a_traceback(tmp_path):
    p = tmp_path / "tickets.jsonl"
    p.write_text('{"external_id": "A", "text": "hi", "customer_phone": "123"}\n', encoding="utf-8")
    result = CliRunner().invoke(app, ["run-batch", str(p), "--no-db"])
    assert result.exit_code == 2
    assert "valid ZainCash phone number" in result.output
