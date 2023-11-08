"""add column to prices

Revision ID: 27a10c458b6f
Revises: 7eec3527259f
Create Date: 2023-11-01 13:36:14.804418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27a10c458b6f'
down_revision: Union[str, None] = '7eec3527259f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
