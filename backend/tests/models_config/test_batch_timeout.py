from app.config import Settings
from app.models_config.resolver import ActiveModels
from app.models_config.types import ModelChoice, Step
from app.services import batch_jobs
from tests.models_config_fakes import fake_registry


def test_cloud_runs_keep_the_ticket_timeout():
    assert batch_jobs.ticket_timeout_s(ActiveModels.from_env(Settings(_env_file=None))) == batch_jobs.TICKET_TIMEOUT_S


def test_local_drafts_get_room_for_their_longer_deadline():
    settings = Settings(_env_file=None, local_agent_timeout_s=300)
    models = ActiveModels(settings, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")}, fake_registry(settings))
    assert batch_jobs.ticket_timeout_s(models) == 360


def test_local_extract_alone_extends_the_ticket_timeout():
    settings = Settings(_env_file=None, local_agent_timeout_s=300)
    models = ActiveModels(settings, {Step.EXTRACT: ModelChoice("ollama", "qwen3:4b")}, fake_registry(settings))
    assert batch_jobs.ticket_timeout_s(models) == 360


def test_short_local_deadlines_never_shrink_the_ticket_timeout():
    settings = Settings(_env_file=None, local_agent_timeout_s=30)
    models = ActiveModels(settings, {Step.EXTRACT: ModelChoice("ollama", "qwen3:4b")}, fake_registry(settings))
    assert batch_jobs.ticket_timeout_s(models) == batch_jobs.TICKET_TIMEOUT_S


def test_local_extract_or_draft_lowers_batch_concurrency():
    settings = Settings(_env_file=None, pipeline_concurrency=20, local_pipeline_concurrency=2)
    registry = fake_registry(settings)
    assert batch_jobs.batch_concurrency(settings, ActiveModels(settings, {}, registry)) == 20
    for step in (Step.EXTRACT, Step.DRAFT):
        local = ActiveModels(settings, {step: ModelChoice("ollama", "qwen3:4b")}, registry)
        assert batch_jobs.batch_concurrency(settings, local) == 2
    intake_only = ActiveModels(settings, {Step.INTAKE: ModelChoice("ollama", "qwen3:4b")}, registry)
    assert batch_jobs.batch_concurrency(settings, intake_only) == 20


def test_batch_concurrency_stays_within_bounds():
    low = Settings(_env_file=None, pipeline_concurrency=1, local_pipeline_concurrency=5)
    local = ActiveModels(low, {Step.DRAFT: ModelChoice("ollama", "qwen3:4b")}, fake_registry(low))
    assert batch_jobs.batch_concurrency(low, local) == 1
    huge = Settings(_env_file=None, pipeline_concurrency=500)
    assert batch_jobs.batch_concurrency(huge, ActiveModels(huge, {}, fake_registry(huge))) == 20
    zero = Settings(_env_file=None, pipeline_concurrency=0)
    assert batch_jobs.batch_concurrency(zero, ActiveModels(zero, {}, fake_registry(zero))) == 1
