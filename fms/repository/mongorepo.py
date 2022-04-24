import pymongo
from nanoid import generate
import time
from fms.domain import documents

class MongoRepo:
    def __init__(self, configuration):
        client = pymongo.MongoClient(
            host=configuration["MONGODB_HOSTNAME"],
            port=int(configuration["MONGODB_PORT"]),
            username=configuration["MONGODB_USER"],
            password=configuration["MONGODB_PASSWORD"],
            authSource="admin",
        )

        self.db = client[configuration["APPLICATION_DB"]]

    def _create_documents_objects(self, results):
        return [
            documents.Document.from_dict(q)
            for q in results
        ]

    def insert_document(self, filename, user):
        collection = self.db.documents
        id = f"i.doc.{generate()}"
        document = documents.Document(
            _id=id,
            filename=filename,
            uploaded_by=user,
            created_at=time.time()
        )
        return collection.insert_one(document.to_dict()).inserted_id

    def find_document(self, id):
        collection = self.db.documents
        return documents.Document.from_dict(collection.find_one({"_id": id}))