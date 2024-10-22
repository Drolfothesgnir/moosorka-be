"""empty message

Revision ID: 5c0d5a4662a5
Revises: 849455a1c964
Create Date: 2024-10-22 18:40:11.447063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c0d5a4662a5'
down_revision = '849455a1c964'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pinned', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.drop_column('pinned')

    # ### end Alembic commands ###