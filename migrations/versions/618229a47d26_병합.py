"""병합

Revision ID: 618229a47d26
Revises: aea1ad5a3b05, f04b54b035e9
Create Date: 2025-04-12 22:14:01.269405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '618229a47d26'
down_revision: Union[str, None] = 'f04b54b035e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
