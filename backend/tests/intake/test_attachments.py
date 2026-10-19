from io import BytesIO
from uuid import uuid4

import pytest
from PIL import Image

from app.intake.errors import ImageRejected, NotOwned, OperationConflict, TurnBusy


def png_bytes(width=8, height=8, color="white"):
    buffer = BytesIO()
    Image.new("RGB", (width, height), color).save(buffer, format="PNG")
    return buffer.getvalue()


def jpeg_bytes():
    buffer = BytesIO()
    Image.new("RGB", (8, 8), "blue").save(buffer, format="JPEG")
    return buffer.getvalue()


@pytest.fixture
def repo(intake_db):
    from app.intake.repository import IntakeRepository
    return IntakeRepository(intake_db[1])


@pytest.fixture
def store(intake_db, tmp_path, repo):
    from app.intake.attachments import AttachmentStore
    settings = intake_db[0].model_copy(update={"intake_upload_dir": str(tmp_path)})
    return AttachmentStore(settings, intake_db[1])


def test_image_bytes_are_decoded_not_trusted(store, repo):
    credentials, view = repo.create("ar")
    with pytest.raises(ImageRejected):
        store.upload(credentials, uuid4(), view.revision, "receipt.png", b"<svg>not a PNG</svg>")
    assert repo.get(credentials).attachments == []


def test_forged_extension_uses_the_decoded_format(store, repo):
    credentials, view = repo.create("ar")
    attachment, updated = store.upload(credentials, uuid4(), view.revision, "notes.jpg.exe", png_bytes())
    assert attachment.mime_type == "image/png"
    assert updated.attachments[0].mime_type == "image/png"
    assert ".." not in attachment.filename


def test_limits_frames_and_truncated_images_are_rejected(intake_db, tmp_path, repo):
    from app.intake.attachments import AttachmentStore
    settings = intake_db[0].model_copy(update={
        "intake_upload_dir": str(tmp_path),
        "intake_max_image_bytes": 80,
        "intake_max_image_pixels": 16,
    })
    limited = AttachmentStore(settings, intake_db[1])
    credentials, view = repo.create("en")
    with pytest.raises(ImageRejected):
        limited.upload(credentials, uuid4(), view.revision, "big.png", png_bytes())
    settings = settings.model_copy(update={"intake_max_image_bytes": 5 * 1024 * 1024})
    pixels = AttachmentStore(settings, intake_db[1])
    with pytest.raises(ImageRejected):
        pixels.upload(credentials, uuid4(), view.revision, "wide.png", png_bytes(8, 8))
    with pytest.raises(ImageRejected):
        pixels.upload(credentials, uuid4(), view.revision, "cut.png", b"\x89PNG\r\n\x1a\nbroken")
    animated = BytesIO()
    frames = [Image.new("RGB", (4, 4), "red"), Image.new("RGB", (4, 4), "blue")]
    frames[0].save(animated, format="WEBP", save_all=True, append_images=frames[1:], duration=10)
    with pytest.raises(ImageRejected):
        pixels.upload(credentials, uuid4(), view.revision, "move.webp", animated.getvalue())


def test_replay_does_not_duplicate_and_changed_bytes_conflict(store, repo, tmp_path):
    credentials, view = repo.create("ar")
    request_id = uuid4()
    first, after = store.upload(credentials, request_id, view.revision, "../../etc/passwd.png", png_bytes())
    again, replayed = store.upload(credentials, request_id, view.revision, "../../etc/passwd.png", png_bytes())
    assert first.id == again.id
    assert replayed.revision == after.revision
    assert first.filename == "passwd.png"
    files = [path for path in tmp_path.rglob("*") if path.is_file()]
    assert len(files) == 1
    with pytest.raises(OperationConflict):
        store.upload(credentials, request_id, after.revision, "passwd.png", png_bytes(color="black"))
    assert len([path for path in tmp_path.rglob("*") if path.is_file()]) == 1


def test_cross_session_read_and_removal(store, repo):
    owner, view = repo.create("ar")
    stranger, _ = repo.create("en")
    attachment, view = store.upload(owner, uuid4(), view.revision, "shot.png", png_bytes())
    with pytest.raises(NotOwned):
        store.read(stranger, attachment.id)
    loaded = store.read(owner, attachment.id)
    assert loaded.data.startswith(b"\x89PNG")
    removed = store.remove(owner, attachment.id, uuid4(), view.revision)
    assert removed.attachments[0].removed is True
    with pytest.raises(ImageRejected):
        store.read(owner, attachment.id)


def test_active_turn_rejects_upload(store, repo, intake_db):
    from app.intake.db_models import IntakeSessionRow
    credentials, view = repo.create("ar")
    with intake_db[1]() as session:
        row = session.get(IntakeSessionRow, credentials.session_id)
        row.turn_status = "processing"
        session.commit()
    with pytest.raises(TurnBusy):
        store.upload(credentials, uuid4(), view.revision, "shot.png", png_bytes())


def test_concurrent_uploads_stop_at_the_session_cap(intake_db, tmp_path, repo):
    from concurrent.futures import ThreadPoolExecutor

    from app.intake.attachments import AttachmentStore
    settings = intake_db[0].model_copy(update={"intake_upload_dir": str(tmp_path), "intake_max_images_per_session": 10})
    store = AttachmentStore(settings, intake_db[1])
    credentials, _ = repo.create("ar")

    def attempt(index):
        while True:
            current = repo.get(credentials)
            try:
                store.upload(credentials, uuid4(), current.revision, f"{index}.png", png_bytes(color=(index, 0, 0)))
                return "stored"
            except ImageRejected:
                return "capped"
            except Exception as exc:
                if exc.__class__.__name__ != "RevisionConflict":
                    raise

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(attempt, range(14)))
    assert results.count("stored") == 10
    assert len(repo.get(credentials).attachments) == 10


def test_changed_invalid_bytes_conflict_before_decoding_replay(store, repo):
    owner, view = repo.create("en")
    request_id = uuid4()
    store.upload(owner, request_id, view.revision, "shot.png", png_bytes())
    with pytest.raises(OperationConflict):
        store.upload(owner, request_id, view.revision, "shot.png", b"invalid changed bytes")


def test_decoder_decompression_limit_is_a_safe_image_rejection(store, repo, monkeypatch):
    owner, view = repo.create("en")
    content = png_bytes()
    monkeypatch.setattr(Image, "MAX_IMAGE_PIXELS", 10)
    with pytest.raises(ImageRejected):
        store.upload(owner, uuid4(), view.revision, "shot.png", content)
