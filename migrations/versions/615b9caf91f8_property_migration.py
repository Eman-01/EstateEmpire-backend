"""property migration

Revision ID: 615b9caf91f8
Revises: 0847b0bed85e
Create Date: 2024-08-18 18:47:29.523005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '615b9caf91f8'
down_revision = '0847b0bed85e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bedrooms', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('bathrooms', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('amenities', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.drop_column('amenities')
        batch_op.drop_column('bathrooms')
        batch_op.drop_column('bedrooms')

    # ### end Alembic commands ###
