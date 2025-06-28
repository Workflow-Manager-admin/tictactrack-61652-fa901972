from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# PUBLIC_INTERFACE
class Player(Base):
    """SQLAlchemy ORM model for players."""
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique username for the player"
    )
    password_hash = Column(
        String(200),
        nullable=False,
        doc="Hashed password for authentication"
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        doc="Timestamp of player creation"
    )
    last_login = Column(
        DateTime,
        nullable=True,
        doc="Timestamp of player's last login"
    )

    games_as_x = relationship(
        "Game",
        back_populates="player_x",
        foreign_keys="Game.player_x_id"
    )
    games_as_o = relationship(
        "Game",
        back_populates="player_o",
        foreign_keys="Game.player_o_id"
    )
    moves = relationship("Move", back_populates="player")


# PUBLIC_INTERFACE
class Game(Base):
    """SQLAlchemy ORM model for games."""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    player_x_id = Column(
        Integer,
        ForeignKey('players.id'),
        nullable=True,
        doc="Player X (First player)"
    )
    player_o_id = Column(
        Integer,
        ForeignKey('players.id'),
        nullable=True,
        doc="Player O (Second player)"
    )
    winner_id = Column(
        Integer,
        ForeignKey('players.id'),
        nullable=True,
        doc="Winner of the game"
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        doc="Timestamp when game was created"
    )
    finished_at = Column(
        DateTime,
        nullable=True,
        doc="Timestamp when game ended"
    )
    board_state = Column(
        Text,
        nullable=False,
        default="",
        doc="Serialized board state (e.g., JSON)"
    )

    player_x = relationship(
        "Player",
        foreign_keys=[player_x_id],
        back_populates="games_as_x"
    )
    player_o = relationship(
        "Player",
        foreign_keys=[player_o_id],
        back_populates="games_as_o"
    )
    winner = relationship("Player", foreign_keys=[winner_id])
    moves = relationship("Move", back_populates="game")


# PUBLIC_INTERFACE
class Move(Base):
    """SQLAlchemy ORM model for game moves."""
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(
        Integer,
        ForeignKey('games.id'),
        nullable=False,
        doc="Game in which the move was made"
    )
    player_id = Column(
        Integer,
        ForeignKey('players.id'),
        nullable=False,
        doc="Player who made the move"
    )
    move_number = Column(
        Integer,
        nullable=False,
        doc="Sequential move number in the game"
    )
    row = Column(
        Integer,
        nullable=False,
        doc="Row index (0-2) of the board"
    )
    col = Column(
        Integer,
        nullable=False,
        doc="Column index (0-2) of the board"
    )
    symbol = Column(
        String(1),
        nullable=False,
        doc="'X' or 'O'"
    )
    made_at = Column(
        DateTime,
        default=datetime.utcnow,
        doc="Timestamp when move was made"
    )

    game = relationship("Game", back_populates="moves")
    player = relationship("Player", back_populates="moves")
