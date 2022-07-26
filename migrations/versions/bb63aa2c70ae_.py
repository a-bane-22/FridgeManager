"""empty message

Revision ID: bb63aa2c70ae
Revises: 8cde6ef66a54
Create Date: 2022-07-25 20:21:17.501748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb63aa2c70ae'
down_revision = '8cde6ef66a54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_phone', table_name='user')
    op.drop_column('user', 'phone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone', sa.VARCHAR(length=10), nullable=True))
    op.create_index('ix_user_phone', 'user', ['phone'], unique=False)
    # ### end Alembic commands ###