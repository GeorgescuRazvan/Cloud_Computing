from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["cloud_computing"]
books_collection = db["books"]

def find_book_by_id(book_id):
    return books_collection.find_one({"_id": book_id})

def create_book_with_id(book_id, data):
    data["_id"] = book_id
    books_collection.insert_one(data)

def update_book(book_id, data):
    books_collection.update_one({"_id": book_id}, {"$set": data})

def delete_book(book_id):
    books_collection.delete_one({"_id": book_id})

def list_books():
    books = list(books_collection.find({}, {"_id": 1, "title": 1, "author": 1, "description": 1}))
    return books

def delete_all_books():
    books_collection.delete_many({})

def generate_new_id():
    # For simplicity, generate a new id based on the count of documents.
    count = books_collection.count_documents({})
    new_id = str(count + 1)
    return new_id

def replace_all_books(books):
    # Replace the entire collection with the provided list.
    delete_all_books()
    for book in books:
        if "_id" not in book:
            book["_id"] = generate_new_id()
        books_collection.insert_one(book)