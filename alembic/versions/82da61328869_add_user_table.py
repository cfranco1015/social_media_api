"""add user table

Revision ID: 82da61328869
Revises: 8d9c8bb220cb
Create Date: 2022-01-23 16:07:36.079947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82da61328869'
down_revision = '8d9c8bb220cb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass