from sqlalchemy import Table, Column, Integer, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


profile_habit_association_table = Table(
    "profile_habit",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profile.id")),
    Column("habit_id", Integer, ForeignKey("habit.id")),
)

class ProfileORM(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    habit = relationship(
        "Habit",
        secondary=profile_habit_association_table,
        primaryjoin=profile_habit_association_table.c.profile_id,
        secondaryjoin=profile_habit_association_table.c.habit_id,
        back_populates="profile"
    )

    def __repr__(self):
        return f"Profile(username: {self.username})"


class HabitORM(Base):
    __tablename__ = "habit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    profile = relationship(
        "Profile",
        secondary=profile_habit_association_table,
        primaryjoin=id==profile_habit_association_table.c.habit_id,
        secondaryjoin=id==profile_habit_association_table.c.profile_id,
        back_populates="habit"
    )

    def __repr__(self):
        return f"Habit(title: {self.title})"