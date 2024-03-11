"""rename user to username

Revision ID: 1376ae683d9d
Revises: 9a911893dd0c
Create Date: 2024-03-11 14:35:35.362521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1376ae683d9d'
down_revision: Union[str, None] = '9a911893dd0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account', sa.Column('username', sa.String(length=30), nullable=False))
    op.drop_constraint('user_account_name_key', 'user_account', type_='unique')
    op.create_unique_constraint(None, 'user_account', ['username'])
    op.drop_column('user_account', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account', sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user_account', type_='unique')
    op.create_unique_constraint('user_account_name_key', 'user_account', ['name'])
    op.drop_column('user_account', 'username')
    # ### end Alembic commands ###
