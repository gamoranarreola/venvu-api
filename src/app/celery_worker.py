from . import create_app

app = create_app()
app.app_context().push()

from app import celery  # noqa: F401, E402
