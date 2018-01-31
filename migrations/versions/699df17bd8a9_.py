"""empty message

Revision ID: 699df17bd8a9
Revises: 
Create Date: 2017-12-27 20:58:59.489000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '699df17bd8a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_title', sa.String(length=50), nullable=False),
    sa.Column('question_content', sa.Text(), nullable=False),
    sa.Column('question_time', sa.DateTime(), nullable=True),
    sa.Column('question_athr', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telephone', sa.String(length=11), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer_content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('answer_author_id', sa.Integer(), nullable=True),
    sa.Column('answer_queston_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['answer_author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['answer_queston_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    op.drop_table('user')
    op.drop_table('question')
    # ### end Alembic commands ###
