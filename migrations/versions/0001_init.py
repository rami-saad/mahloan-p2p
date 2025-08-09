from alembic import op
import sqlalchemy as sa
revision = '0001_init'
down_revision = None
def upgrade():
    op.create_table(
        'loans',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('rate', sa.Float(), nullable=False),
        sa.Column('term', sa.Integer(), nullable=False),
        sa.Column('balance', sa.Float(), nullable=False),
        sa.Column('status', sa.Enum('pending','approved','funded','closed', name='loanstatus'), nullable=False, server_default='pending')
    )
def downgrade():
    op.drop_table('loans')
