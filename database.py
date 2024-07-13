import sqlite3

conn = sqlite3.connect("omores.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Orders(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    brand STRING NOT NULL,
    model STRING NOT NULL,
    description TEXT NOT NULL,
    price STRING NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
)""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    name STRING NOT NULL,
    surname STRING NOT NULL,
    phone STRING NOT NULL,
    tag STRING
)""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS Photos(
    user_id INTEGER NOT NULL,
    ad_id INTEGER NOT NULL,
    picture BLOB,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (ad_id) REFERENCES Orders(id)
)""")
conn.commit()


class Database:
    @classmethod
    def register_user(cls, data: dict):
        cur.execute(
            "INSERT INTO Users(name, surname, phone) VALUES (?, ?, ?)",
            (data["name"], data["surname"], data["phone"])
        )
        conn.commit()

    @classmethod
    def create_order(cls, user_id: int, data: dict):
        cur.execute(
            "INSERT INTO Orders(user_id, brand, model, description, price) VALUES (?, ?, ?, ?, ?)",
            (user_id, data["brand"], data["model"], data["description"], data["price"])
        )
        conn.commit()

        cls.save_photo(user_id, cur.lastrowid, data["photo"])

    @classmethod
    def save_photo(cls, user_id: int, order_id: int, picture: bytes):
        # f"INSERT INTO Users(login, ad_id, picture) VALUES ({'; DROP TABLE Users; --'} LIMIT 5)"
        cur.execute(
            "INSERT INTO Photos(user_id, ad_id, picture) VALUES (?, ?, ?)",
            (user_id, order_id, picture)
        )
        conn.commit()

    @classmethod
    def get_orders(cls, user_id: int):
        return cur.execute(
            "SELECT * FROM Orders WHERE user_id = ?", (user_id, )
        ).fetchall()

