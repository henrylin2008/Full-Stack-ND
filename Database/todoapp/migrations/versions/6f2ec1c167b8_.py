"""empty message

Revision ID: 6f2ec1c167b8
Revises: d62b7a2667e0
Create Date: 2020-05-03 12:00:07.581235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f2ec1c167b8'
down_revision = 'd62b7a2667e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###