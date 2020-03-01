import pytest
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import create_database, drop_database, database_exists

"""
test_<what>__<when>__<expect>
"""


@pytest.fixture(scope="session", autouse=True)
def db():
    from app.main.model.users import metadata
    from database import configure_engine

    url = 'sqlite:///test.db'

    engine = configure_engine(url)
    if not database_exists(url):
        create_database(url)

    metadata.bind = engine
    metadata.create_all(engine)

    try:
        yield
    finally:
        drop_database(url)


@pytest.fixture(scope="function", autouse=True)
def transaction(db):
    from database import session_factory, Session, engine

    connection = engine.connect()
    session_factory.configure(bind=connection)
    transaction = connection.begin_nested()

    try:
        yield transaction
    finally:
        transaction.rollback()
        connection.close()
        Session.remove()


Session = scoped_session(sessionmaker())
session = Session(autocommit=False, autoflush=True)


def db_entry():
    from app.main.model.users import user
    entry = session.execute(user.select()).fetchone()
    return entry


def test_new_user_created_successfully():
    from app.main.service.user_service import new_user
    test_data = {'username': "test_user", "repositories": ["test_repo", "test_repo_2"]}
    test_insert = new_user({'username': "test_user"}, ["test_repo", "test_repo_2"])
    entry = db_entry()
    assert test_insert == test_data
    assert entry['username'] == test_data['username']
    assert entry['repositories'].strip("{}") == ",".join(test_data['repositories'])


def test_update_user_updated_successfully():
    from app.main.service.user_service import new_user, update_user
    test_data = {'username': "test_user", "repositories": ["test_repo"]}
    seed_new_user = new_user({"username": "test_user"}, repositories=[])
    first_entry = db_entry()
    test_update_user = update_user(data={'username': "test_user"}, repositories=["test_repo"])
    updated_entry = db_entry()
    assert first_entry['username'] == updated_entry['username']
    assert first_entry['repositories'] != updated_entry['repositories']
    assert test_update_user == test_data
    assert seed_new_user != test_update_user


def test_existing_user_when_user_exist():
    from app.main.service.user_service import new_user, existing_user
    test_data = {'username': "test_user", "repositories": []}
    seed_new_user = new_user({"username": 'test_user'}, repositories=[])
    check_existing_user = existing_user(test_data)
    assert check_existing_user['username'] == "test_user"
    assert check_existing_user['repositories'] == "{}"
    assert seed_new_user['username'] == check_existing_user['username']


def test_existing_user_when_user_doesnt_exist():
    from app.main.service.user_service import existing_user
    test_username = {'username': "unique"}
    check_existing_user = existing_user(test_username)
    assert check_existing_user is None
