import pyodbc as odbccon
from fastapi import FastAPI

# Connect to database
connection = odbccon.connect(   "DRIVER={ODBC Driver 17 for SQL Server};"
                                "SERVER=DESKTOP-UUN8BBB\SQLEXPRESS;"
                                "DATABASE=ApiTestUnitaires;"
                                "Trusted_Connection=yes;"
                            )
cursor = connection.cursor()
cursor.execute("SELECT * FROM USERS")
results = cursor.fetchall()
print(results)

# Create a instance of the FastApi()
app = FastAPI()

class User:

    @staticmethod
    @app.post("/users/")
    def create_user(firstname: str, lastname: str, age: int):
        cursor = connection.cursor()
        # Add row with value in USERS table
        cursor.execute("INSERT INTO USERS (FIRSTNAME, LASTNAME, AGE) VALUES (?, ?, ?)", (firstname, lastname, age))
        cursor.commit()
        return {"firstname": firstname, "lastname": lastname, "age": age}

    @staticmethod
    @app.get("/users/{user_id}")
    def read_user(user_id: int):
        cursor = connection.cursor()
        # Select row by Id
        cursor.execute("SELECT * FROM USERS WHERE ID = ?", user_id)
        user = cursor.fetchone()
        # No row exists with this Id
        if user is None:
            return {"message": "User not found"}
        return {"id": user[0], "firstname": user[1], "lastname": user[2], "age": user[3]}

    @staticmethod
    @app.put("/users/{user_id}")
    def update_user(user_id: int, firstname: str = None, lastname: str = None, age: int = None):
        cursor = connection.cursor()
        # Select row by Id
        cursor.execute("SELECT * FROM USERS WHERE ID = ?", user_id)
        user = cursor.fetchone()
        if user is None:
            return {"message": "User not found"}

        update_query = "UPDATE USERS SET "
        params = []
        if firstname is not None:
            update_query += "FIRSTNAME = ?, "
            params.append(firstname)
        if lastname is not None:
            update_query += "LASTNAME = ?, "
            params.append(lastname)
        if age is not None:
            update_query += "AGE = ?, "
            params.append(age)

        update_query = update_query[:-2]
        update_query += " WHERE ID = ?"
        params.append(user_id)

        cursor.execute(update_query, *params)
        cursor.commit()

        cursor.execute("SELECT * FROM USERS WHERE ID = ?", user_id)
        updated_user = cursor.fetchone()
        return {"id": updated_user[0], "firstname": updated_user[1], "lastname": updated_user[2], "age": updated_user[3]}

    @staticmethod
    @app.delete("/users/{user_id}")
    def delete_user(user_id: int):
        cursor = connection.cursor()
        # Select row by Id
        cursor.execute("SELECT * FROM USERS WHERE ID = ?", user_id)
        user = cursor.fetchone()
        if user is None:
            return {"message": "User not found"}

        # Delete row by Id
        cursor.execute("DELETE FROM USERS WHERE ID = ?", user_id)
        cursor.commit()

        return {"message": "User deleted successfully"}  
    
    @staticmethod
    @app.delete("/users")
    def delete_all_users():
        cursor = connection.cursor()
        # Delete all rows in USERS table
        cursor.execute("DELETE FROM USERS")
        cursor.commit()