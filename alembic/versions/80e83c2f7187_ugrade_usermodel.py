"""ugrade UserModel

Revision ID: 80e83c2f7187
Revises: 52585dfffdcc
Create Date: 2022-01-05 23:05:37.730068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80e83c2f7187'
down_revision = '52585dfffdcc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
