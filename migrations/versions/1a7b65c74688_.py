"""empty message

Revision ID: 1a7b65c74688
Revises: e481cc1e3d67
Create Date: 2023-03-30 19:19:40.381060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a7b65c74688'
down_revision = 'e481cc1e3d67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mass', sa.String(length=50), nullable=False))
        batch_op.drop_column('homeworld')
        batch_op.drop_column('specie')
        batch_op.drop_column('vehicle')
        batch_op.drop_column('starship')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('starship', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('vehicle', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('specie', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('homeworld', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.drop_column('mass')

    # ### end Alembic commands ###