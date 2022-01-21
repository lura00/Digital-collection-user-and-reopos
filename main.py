import sqlite3

def menu():
    print("\n===========================================================")
    print("|                        Welcome                          |")
    print("|   Enter your information and connect your Github repo   |")
    print("|             Add data to user-table? press .1            |")
    print("|             ADd data to repo-table? press .2            |")
    print("|             See all users and repos? press .3           |")
    print("|             Edit post? press .4                         |")
    print("|             Delete post? press .5                       |")
    print("|             Exit, press .6                              |")
    print("===========================================================")

class userRepos:
    def __init__(self):
        self.conn = sqlite3.connect('mydb.db')
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA foreign_keys = OFF")
        self.create_table_user()
        self.create_table_repo()
        

    def create_table_user(self):
        # self.c.execute("""DROP TABLE user""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR NOT NULL,
                password VARCHAR,
                handle VARCHAR NOT NULL UNIQUE,
                email VARCHAR NOT NULL)""")
        self.conn.commit()

    def create_table_repo(self):
        # self.c.execute("DROP TABLE repo")
        self.c.execute("""CREATE TABLE IF NOT EXISTS repo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url VARCHAR NOT NULL,
                description TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE)""")
        self.c.execute("PRAGMA FOREIGN_KEYS=ON;")
        self.conn.commit()

    def insert_user(self, name, password, handle, email):
        self.c.execute("INSERT INTO user (name, password, handle, email) VALUES (?,?,?,?)", (name, password, handle, email))
        self.conn.commit()

    def insert_repo(self, url, description, userID):
        self.c.execute("INSERT INTO repo (url, description, user_id) VALUES (?,?,?)", (url, description, userID))
        self.conn.commit()

    def show_all(self):
        self.c.execute("SELECT * FROM user LEFT JOIN repo")
        items = self.c.fetchall()

        for item in items:
            print(item)
        self.conn.commit()

    def delete_one(self, table, id):
        self.c.execute(f"DELETE FROM '{table}' WHERE rowid = (?)", id)
        self.conn.commit()

    def edit_post(self, table, column, changed_data, id):
        self.c.execute(f"""UPDATE '{table}' SET '{column}' = '{changed_data}'
            WHERE rowid = {id}
            """)
        self.conn.commit()

db = userRepos()

while True:
    menu()
    choice = int(input("Make our choice: 1 - 6: "))
    if choice == 1:
        name = input("Enter your name: ")
        password = input("Enter a password: ")
        handle = input("Enter your username: ")
        email = input("Enter your email: ")
        db.insert_user(name, password, handle, email)

    elif choice == 2:
        url = input("Enter your repo URL: ")
        description = input("Enter a description of the repo: ")
        userID = input("Enter the user id: ")
        db.insert_repo(url, description, userID)

    elif choice == 3:
        db.show_all()

    elif choice == 4:
        table = input("What table needs editing, user or repo? ")
        column = input(
            "What column do you want to edit? ")
        data = input("What is the new data? ")
        id = input("Enter the row ID ")
        db.edit_post(table, column, data, id)

    elif choice == 5:
        table = input("Choose table, user or repo: ")
        delete_user_id = input("Enter id of user to be deleted: ")
        db.delete_one(table, delete_user_id)

    elif choice == 6:
        print("Thank you for using my app, your notes have been saved, come back any time!")
        break
    else:
        print("==>Now something went a little bit wrong, try another number<==")
