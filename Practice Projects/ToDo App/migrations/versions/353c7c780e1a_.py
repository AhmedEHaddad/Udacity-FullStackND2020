"""empty message

Revision ID: 353c7c780e1a
Revises: 7a91ed575996
Create Date: 2020-04-08 04:33:20.467476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '353c7c780e1a'
down_revision = '7a91ed575996'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###
    op.execute('UPDATE todos SET completed=False WHERE completed IS NULL;')
    op.alter_column('todos','completed', nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
