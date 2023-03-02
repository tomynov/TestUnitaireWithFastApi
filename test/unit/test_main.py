import unittest
import pyodbc as odbccon
import sys
sys.path.append("C:\\Users\\Tom\\Desktop\\YnovParis\\Ynov2022\\TestUnitaires\\app")
from main import User

class TestUserMethods(unittest.TestCase):
    def setUp(self):
        # Connect to the test database
        self.connection = odbccon.connect   (  "DRIVER={ODBC Driver 17 for SQL Server};"
                                                "SERVER=DESKTOP-UUN8BBB\SQLEXPRESS;"
                                                "DATABASE=ApiTestUnitairesTest;"
                                                "Trusted_Connection=yes;"
                                            )
        self.cursor = self.connection.cursor()

    def test_delete_all_users(self):

        # Add users to DB
        self.cursor.execute("INSERT INTO USERS (FIRSTNAME, LASTNAME, AGE) VALUES (?, ?, ?)", ("Tom", "Cousdikian", 23))
        self.cursor.execute("INSERT INTO USERS (FIRSTNAME, LASTNAME, AGE) VALUES (?, ?, ?)", ("Student", "Ynov", 22))
        self.connection.commit()

        # Call the delete_all_users method
        User.delete_all_users()

        # Verify if USERS table is empty
        self.cursor.execute("SELECT COUNT(*) FROM USERS")
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 0)


    def test_create_user(self):

        # Delete all users
        User.delete_all_users()

        # Call the create_user method
        User.create_user("Student", "Ynov", 23)

        # Check that the user was add to the database
        self.cursor.execute("SELECT * FROM USERS")
        result = self.cursor.fetchone()
        self.assertEqual(result[1], "Student")
        self.assertEqual(result[2], "Ynov")
        self.assertEqual(result[3], 23)
    
    def test_read_user(self):

        # Delete all users
        User.delete_all_users()

        # Create a user
        User.create_user("Tom", "Cousdikian", 23)

        # Call the read_user method
        response = User.read_user(1)
        self.assertEqual(response, {    "id": 1, 
                                        "firstname": "Tom", 
                                        "lastname": "Cousdikian", 
                                        "age": 23
                                    }
                        )

        # Test reading if there is no user in DB
        response = User.read_user(999)
        self.assertEqual(response, {"message": "User not found"})

    def test_update_user(self):

        # Delete all users
        User.delete_all_users()

        # Create a user
        User.create_user("Tom", "Ynov", 4)

        # Call the update_user method
        User.update_user(1, lastname="Cousdikian", age=23)

        # Check if user was updated in the database
        self.cursor.execute("SELECT * FROM USERS WHERE ID = ?", 1)
        result = self.cursor.fetchone()
        self.assertEqual(result[1], "Tom")
        self.assertEqual(result[2], "Cousdikian")
        self.assertEqual(result[3], 23)

        # Test updating if there is no user in DB
        response = User.update_user(999, firstname="Jane")
        self.assertEqual(response, {"message": "User not found"})

    def test_delete_user(self):

        # Delete all users
        User.delete_all_users()

        # Create a user
        User.create_user("Tom", "Cousdikian", 23)

        # Call the delete_user method
        User.delete_user(1)

        # Check that the user was deleted from the database
        self.cursor.execute("SELECT * FROM USERS")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

        # Test deleting if there is no user in DB
        response = User.delete_user(999)
        self.assertEqual(response, {"message": "User not found"})

if __name__ == '__main__':
    unittest.main()