"""add content column to posts table

Revision ID: 8d9c8bb220cb
Revises: c75b96e3cb94
Create Date: 2022-01-23 16:00:05.968467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d9c8bb220cb'
down_revision = 'c75b96e3cb94'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
