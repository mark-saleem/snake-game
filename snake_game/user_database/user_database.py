import sqlite3 

class UserDatabase:
    def __enter__(self):
        self.connection = sqlite3.connect('users_database.db')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id integer PRIMARY KEY AUTOINCREMENT,
                username text UNIQUE NOT NULL,
                password text NOT NULL,
                highscore integer DEFAULT 0
            )"""
        )

        self.id_position = 0

        return self

    def __exit__(self, exc_type, exc, tb):
        self.connection.close()

    def create_user(self, username, password):
        if self._check_field('username', username):
            return 
        with self.connection:    
            self.cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (:username, :password)""",
                {
                    'username': username, 
                    'password': password, 
                }
            )
    
    def update_user_field(self, id, field ,new_value):
        with self.connection:
            self.cursor.execute(
                f"UPDATE users SET {field} = :value WHERE id = :id",
                {
                    'id': id,
                    'value': new_value
                }
            )
        
    def get_user_field(self, id, field):
        if not self._check_field('id', id):
            return None
        self.cursor.execute(f"SELECT {field} FROM users WHERE id = :id", {'id': id})
        
        result = self.cursor.fetchone()
        return result[0]

    def get_user(self, id):
        if not self._check_field('id', id):
            return None
        self.cursor.execute(f"SELECT * FROM users WHERE id = :id", {'id': id})
        user = self.cursor.fetchone()
        return user 

    def check_username(self, username): # this function checks if the username exists and if it does it returns the users id
        if not self._check_field('username', username):
            return False
        self.cursor.execute(f"SELECT * FROM users WHERE username = :username", {'username': username})
        user = self.cursor.fetchone()
        return user[self.id_position]

    def delete_user(self, id):
        if not self._check_field('id', id):
            return 
        with self.conncetion:
            self.curser.execute("DELETE from users WHERE id = :id",
                {'id': id})
            
    def _check_field(self, field, value):
        self.cursor.execute(f"SELECT * FROM users WHERE {field} =:value", {'value': value})
        user = self.cursor.fetchone()
        if user == None: # empty list means no user found
            return False
        
        return True
