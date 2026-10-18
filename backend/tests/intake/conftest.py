"""Real support_test fixtures for intake. Never resets the development database."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db.session import make_engine, make_sessionmaker, reset_db
from app.main import create_app
from app.pipeline.graph import PipelineDeps, build_graph
from app.pipeline.stage4_lookup.lookup import InMemoryTransactionRepo
from app.taxonomy import load_taxonomy
from tests.fakes import FakeClassifier, make_output

pytestmark = pytest.mark.integration


@pytest.fixture
def intake_db():
    settings = Settings(_env_file=None, openrouter_api_key="", typesafe_api_key="")
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    with engine.connect() as connection:
        assert connection.exec_driver_sql("SELECT current_database()").scalar() == "support_test"
    reset_db(engine)
    factory = make_sessionmaker(engine)
    yield settings, factory
    engine.dispose()


@pytest.fixture
def intake_client(tmp_path):
    from app.intake.attachments import AttachmentStore
    from app.intake.graph import IntakeGraph
    from app.intake.repository import IntakeRepository
    from app.intake.service import IntakeService
    from app.intake.turns import TurnStore
    from tests.intake.helpers import ScriptedIntakeModel

    settings = Settings(
        _env_file=None, openrouter_api_key="", typesafe_api_key="", intake_upload_dir=str(tmp_path)
    )
    assert make_url(settings.test_database_url).database == "support_test"
    engine = make_engine(settings.test_database_url)
    reset_db(engine)
    factory = make_sessionmaker(engine)
    model = ScriptedIntakeModel()
    taxonomy = load_taxonomy(settings.taxonomy_path)

    def pipeline(_settings, _mode, _repo):
        return build_graph(PipelineDeps(
            mode="jev", taxonomy=taxonomy, txn_repo=InMemoryTransactionRepo([]),
            jev=FakeClassifier(make_output("general_inquiry", priority="P4"), fail_for={"fail"}),
        ))

    def builder(session_factory, app_settings, app_taxonomy):
        store = AttachmentStore(app_settings, session_factory)
        graph = IntakeGraph(model, app_taxonomy, store, app_settings)
        repo = IntakeRepository(session_factory)
        turns = TurnStore(session_factory)
        return IntakeService(repo, turns, graph, store)

    def dispatcher(_app, _submission):
        return None

    with TestClient(create_app(
        settings, session_factory=factory, pipeline_builder=pipeline,
        intake_builder=builder, intake_dispatcher=dispatcher,
    )) as client:
        client.model = model
        client.factory = factory
        yield client
    engine.dispose()
