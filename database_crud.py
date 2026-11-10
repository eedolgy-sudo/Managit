from sqlalchemy.orm import Session
from database_models import Base, TaskDB#, User, Notification
from sqlalchemy import create_engine, select, event, update

engine = create_engine('sqlite:///managit_database.db', echo=True)


@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables(tables_list):
    Base.metadata.drop_all(
        engine,
        tables=[table.__table__ for table in tables_list]
    )


def add_data(input_data: list):
    with Session(engine) as session:
        with session.begin():
            session.add_all(input_data)


'''def select_users():
    with Session(engine) as session:
        stmt = select(User)
        return session.scalars(stmt).all()'''


def select_tasks():
    with Session(engine) as session:
        stmt = select(TaskDB)
        return session.scalars(stmt).all()


def select_task(task_id):
    with Session(engine) as session:
        return session.get(TaskDB, task_id)


def select_user_data(model, user_id):
    with Session(engine) as session:
        stmt = select(model).where(model.user_id == user_id)
        return session.scalars(stmt).all()


'''def select_notifications_for_task(task_id):
    with Session(engine) as session:
        stmt = select(Notification).where(Notification.task_id == task_id)
        return session.scalars(stmt).all()'''


def update_data(model, record_id, changes: dict):
    with Session(engine) as session:
        with session.begin():
            stmt = select(model).where(model.id == record_id)
            record = session.scalar(stmt)

            if record is None:
                return False

            for key, value in changes.items():
                setattr(record, key, value)

            return True


def delete_data(model, record_id):
    with Session(engine) as session:
        with session.begin():
            stmt = select(model).where(model.id == record_id)

            '''if model == TaskDB:
                stmt = stmt.where(TaskDB.user_id == user_id)
            elif model == Notification:
                stmt = stmt.join(Notification.TaskDB).where(
                    TaskDB.user_id == user_id
                )
            else:
                raise ValueError("Unsupported model")'''

            record = session.scalar(stmt)

            if record is None:
                return False

            session.delete(record)
            return True