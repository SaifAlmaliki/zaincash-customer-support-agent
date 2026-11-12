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
