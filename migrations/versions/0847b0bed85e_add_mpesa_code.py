"""add mpesa code

Revision ID: 0847b0bed85e
Revises: c6af782a4509
Create Date: 2024-08-16 12:24:47.786182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0847b0bed85e'
down_revision = 'c6af782a4509'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rented', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mpesa_code', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rented', schema=None) as batch_op:
        batch_op.drop_column('mpesa_code')

    # ### end Alembic commands ###
