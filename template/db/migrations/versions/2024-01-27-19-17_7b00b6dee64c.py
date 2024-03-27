"""criando superuser

Revision ID: 7b00b6dee64c
Revises: 634fdd2bd607
Create Date: 2024-01-27 19:17:16.886713

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7b00b6dee64c"
down_revision = "634fdd2bd607"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("INSERT INTO users (id, username, fullname, is_superuser, email, password) VALUES (1, 'admin', 'administrador', 1, 'admin@template.com', '$pbkdf2-sha512$25000$onSO0XrvXYvx3hsjBIDQeg$MBNIIQ1WUtQVKdwK5Yf2HVOJwVQdFDZDqWXCqAIQTfZhg/w6nsMkyBV4qKDEFFvgTsM0/qdKL3aS0Vo40s8PiQ')")
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
    # ### end Alembic commands ###
