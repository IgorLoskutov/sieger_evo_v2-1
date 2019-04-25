"""create db and trigger

Revision ID: 79b9a7b13064
Revises:
Create Date: 2019-04-22 00:35:03.721743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79b9a7b13064'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('datafiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(length=120), nullable=True),
    sa.Column('datafile', sa.LargeBinary(), nullable=True),
    sa.Column('expire', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_datafiles_filename'), 'datafiles', ['filename'], unique=False)
    op.execute("""CREATE FUNCTION delete_expired() RETURNS trigger
        LANGUAGE plpgsql
        AS $$
            BEGIN
              DELETE FROM datafiles WHERE expire < NOW();
              RETURN NULL;
            END;
        $$;
        CREATE TRIGGER trigger_delete_expired
        AFTER INSERT ON datafiles
        EXECUTE PROCEDURE delete_expired();""")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_datafiles_filename'), table_name='datafiles')
    op.drop_table('datafiles')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
