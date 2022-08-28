from tinydb import TinyDB,Query
def accountdetails(username):
    db = TinyDB("database.json")
    User = Query()
    data = db.search(User.username == username)
    return data
print(accountdetails("humam"))