"""4

Revision ID: a4750b6163d2
Revises: 3303fef2bce7
Create Date: 2024-03-26 04:08:25.410859+07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4750b6163d2'
down_revision = '3303fef2bce7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('description', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    # ### end Alembic commands ###