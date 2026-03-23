from snake_game.user_database.user_database import UserDatabase

class User:
    def __init__(self):
        pass

    def login(self, username, check_password):
        with UserDatabase() as user_database:
            id = user_database.check_username(username)
            if not id:
                return None    
            password = user_database.get_user_field(id, 'password')
            if not (password == check_password):
                return None
            user = user_database.get_user(id)
            return user
        
    def signup(self, username, password):
        if username == None or password == None:
            return None
        with UserDatabase() as user_database:
            id = user_database.check_username(username)
            if id:
                return None
            else:
                user_database.create_user(username, password)
                id = user_database.check_username(username)
                user = user_database.get_user(id)
                return user
            
    def update_highscore(self, id, highscore):
        with UserDatabase() as user_database:
            user_database.update_user_field(id, 'highscore', highscore)
