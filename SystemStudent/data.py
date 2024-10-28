import mysql.connector as mysql
import configDB as guiConf

from tkinter import messagebox as ms

class MySQL:

    GUIDB = "SystemStudent"

    def connect(self):
        conn = mysql.connect(**guiConf.dbConfig)

        cursor = conn.cursor()

        return conn, cursor
    
    def close(self, cursor, conn):
        cursor.close()
        conn.close()

    def createGuiDB(self):
        conn, cursor = self.connect()

        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.GUIDB}")
            conn.commit()
            print(f"Database {self.GUIDB} created successfully")
        except mysql.Error as error:
            print(f"Failed to create database: {error}")
        
        self.close(cursor, conn)

    def dropGuiDB(self):

        conn, cursor = self.connect()
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS {self.GUIDB}")
            conn.commit()
            print(f"Database {self.GUIDB} dropped successfully")
        except mysql.Error as error:
            print(f"Failed to drop database: {error}")

        self.close(cursor, conn)

    def useGuiDB(self, cursor):
        cursor.execute(f"USE {self.GUIDB}")

    def createTables(self):
        conn, cursor = self.connect()
        self.useGuiDB(cursor)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                contact_number VARCHAR(15),
                gender VARCHAR(10),
                dob DATE,
                stream VARCHAR(50)
            )
        ''')
        print("Bảng 'students' đã được tạo hoặc đã tồn tại.")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                password VARCHAR(255)
            )
        ''')
        print("Bảng 'users' đã được tạo hoặc đã tồn tại.")

        conn.commit()
        print("Tables created successfully.")


        self.close(cursor, conn)

    def dropTables(self):
        conn, cursor = self.connect()
        self.useGuiDB(cursor)
        try:
            cursor.execute("DROP TABLE IF EXISTS students")
            cursor.execute("DROP TABLE IF EXISTS users")
            conn.commit()
            print("Tables dropped successfully.")
        except mysql.connector.Error as err:
            print(f"Error dropping tables: {err}")
        finally:
            self.close(cursor, conn)

    def insert_student(self, name, email, contact_number, gender, dob, stream):
        conn, cursor = self.connect()
        self.useGuiDB(cursor)
        try:
            cursor.execute('''
                INSERT INTO students (name, email, contact_number, gender, dob, stream)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (name, email, contact_number, gender, dob, stream))
            conn.commit()
            print("Student inserted successfully.")
        except mysql.Error as err:
            print(f"Error inserting student: {err}")
        finally:
            self.close(cursor, conn)
    
    def showStudent(self):
        conn, cursor = self.connect()
        self.useGuiDB(cursor)
        try:
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            # for row in rows:
            #     print(row)
        except mysql.Error as err:
            print(f"Error fetching students: {err}")
        finally:
            self.close(cursor, conn)

            return rows
        
    def update_record(self, student_id, name, email, contact_number, gender, dob, stream):
        conn, cursor = self.connect()
        self.useGuiDB(cursor)
    
        try:
            cursor.execute('''
                UPDATE students
                SET name = %s, email = %s, contact_number = %s, gender = %s, dob = %s, stream = %s
                WHERE id = %s
            ''', (name, email, contact_number, gender, dob, stream, student_id))
        
            conn.commit()
            print("Record updated successfully.")
        except mysql.Error as err:
            print(f"Error updating record: {err}")
        finally:
            self.close(cursor, conn)

    def delete_record(self, student_id):
        conn, cursor = self.connect()
        self.useGuiDB(cursor)

        try:
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()
            print("Record deleted successfully.")
        except mysql.Error as e:
            print(f"Error deleting record: {e}")
        finally:
            self.close(cursor, conn)
    
    def login(self, username, password):
        conn, cursor = self.connect()
        self.useGuiDB(cursor)
        try:
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result and result[0] == password:
                print("Login successful!")
                return True
            else:
                print("Invalid username or password.")
                return False
        except mysql.Error as err:
            print(f"Error during login: {err}")
            return False
        finally:
            self.close(cursor, conn)
 


if __name__ == '__main__':
    db = MySQL()
    # db.createGuiDB()
    db.createTables()
    
