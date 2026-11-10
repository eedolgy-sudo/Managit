from datetime import datetime, timezone
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TaskDB(Base):
    __tablename__ = "tasks"

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="check_task_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    date_created: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    description: Mapped[str] = mapped_column(default="")
    due_date: Mapped[datetime | None] = mapped_column(nullable=True)

    '''parent_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id")
    )

    subtasks: Mapped[list["Task"]] = relationship(
        back_populates="parent_task", cascade="all, delete-orphan"
    )

    parent_task: Mapped["Task | None"] = relationship(
        back_populates="subtasks",
        remote_side=[id]
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )'''


'''class NotificationDB(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(default="")
    date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    task: Mapped["Task"] = relationship(
        back_populates="notifications"
    )


class UserDB(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint("length(trim(username)) > 0",
                        name="check_username"),
        CheckConstraint("length(trim(name)) > 0", name="check_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(default="")
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )'''