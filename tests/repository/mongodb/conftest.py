import pymongo
import pytest


@pytest.fixture(scope="session")
def mg_database_empty(app_configuration):
    client = pymongo.MongoClient(
        host=app_configuration["MONGODB_HOSTNAME"],
        port=int(app_configuration["MONGODB_PORT"]),
        username=app_configuration["MONGODB_USER"],
        password=app_configuration["MONGODB_PASSWORD"],
        authSource="admin",
    )
    db = client[app_configuration["APPLICATION_DB"]]

    yield db

    client.drop_database(app_configuration["APPLICATION_DB"])
    client.close()

@pytest.fixture(scope="function")
def mg_test_data():
    return [
        {
            "_id": "i.doc.IRFa-VaY2b",
            "uploaded_by": "ik",
            "filename": "document for case id 1234",
            "created_at" : 123456,
        },
    ]

@pytest.fixture(scope="function")
def mg_database(mg_database_empty, mg_test_data):
    collection = mg_database_empty.documents
    collection.insert_many(mg_test_data)
    yield mg_database_empty

    collection.delete_many({})
