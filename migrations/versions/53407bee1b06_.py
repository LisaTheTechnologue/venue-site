"""empty message

Revision ID: 53407bee1b06
Revises: 
Create Date: 2020-05-06 16:10:46.946938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53407bee1b06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('city', sa.String(length=10), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('genres_artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('genre_artist_link', 'genres_artist', ['artist_id', 'genre_id'], unique=True)
    op.create_table('genres_venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('genre_venue_link', 'genres_venue', ['venue_id', 'genre_id'], unique=True)
    op.create_table('shows_artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('show_id', sa.Integer(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['show_id'], ['show.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('show_artist_link', 'shows_artist', ['artist_id', 'show_id'], unique=True)
    op.create_table('shows_venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('show_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['show_id'], ['show.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('show_venue_link', 'shows_venue', ['venue_id', 'show_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('show_venue_link', table_name='shows_venue')
    op.drop_table('shows_venue')
    op.drop_index('show_artist_link', table_name='shows_artist')
    op.drop_table('shows_artist')
    op.drop_index('genre_venue_link', table_name='genres_venue')
    op.drop_table('genres_venue')
    op.drop_index('genre_artist_link', table_name='genres_artist')
    op.drop_table('genres_artist')
    op.drop_table('venue')
    op.drop_table('show')
    op.drop_table('genre')
    op.drop_table('artist')
    # ### end Alembic commands ###
