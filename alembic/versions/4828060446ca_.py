"""empty message

Revision ID: 4828060446ca
Revises: 741c5a053285
Create Date: 2025-05-14 09:41:58.255801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4828060446ca'
down_revision: Union[str, None] = '741c5a053285'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""ALTER TABLE rooms 
    ADD COLUMN celery_tasks UUID NOT NULL,
    ADD COLUMN tasks_status VARCHAR(255) NOT NULL""")


def downgrade() -> None:
    op.execute("""
    ALTER TABLE rooms DROP COLUMN celery_tasks
    """)
    op.execute("""ALTER TABLE rooms DROP COLUMN tasks_status""")
