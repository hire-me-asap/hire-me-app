"""add study_thread_id column to users

Revision ID: 55ce2bfb197d
Revises: e63dea5ff995
Create Date: 2025-04-10 11:46:16.113577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55ce2bfb197d'
down_revision: Union[str, None] = 'e63dea5ff995'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
