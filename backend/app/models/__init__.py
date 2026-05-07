from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User  # noqa: F401
from app.models.contact import Contact  # noqa: F401
from app.models.company import Company  # noqa: F401
from app.models.deal import Deal  # noqa: F401
from app.models.pipeline import PipelineStage  # noqa: F401
from app.models.email_template import EmailTemplate  # noqa: F401
from app.models.activity import Activity  # noqa: F401
