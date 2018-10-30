"""update book

Revision ID: 56581e0fbe24
Revises: 5de035505c6e
Create Date: 2018-10-30 19:59:20.458873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56581e0fbe24'
down_revision = '5de035505c6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('author', sa.String(length=255), nullable=True))
    op.add_column('book', sa.Column('pages', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'pages')
    op.drop_column('book', 'author')
    # ### end Alembic commands ###