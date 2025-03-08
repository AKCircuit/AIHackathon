import sqlite3

DBNAME = "Back end/DB.db"

CREATEQ = ["""CREATE TABLE IF NOT EXISTS tblUsers (
            UserName VarChar(50) PRIMARY KEY,
            PW VarChar(50),
            Supervisor BOOLEAN);""",
            """CREATE TABLE IF NOT EXISTS tblHints (
            HintID INTEGER PRIMARY KEY AUTOINCREMENT,
            Text VarChar(500));""",
            """CREATE TABLE IF NOT EXISTS tblUserHints (
            UserName VarChar(50),
            HintID INTEGER,
            PRIMARY KEY(UserName, HintID));""",
            """CREATE TABLE IF NOT EXISTS tblSupervisorStudent (
            SupervisorUserName VarChar(50),
            StudentUserName VarChar(50),
            PRIMARY KEY(SupervisorUserName, StudentUserName)
            );"""]

ADDUSERQ = """INSERT INTO tblUsers VALUES (?, ?, ?)"""

AUTHENTICATEQ = """SELECT PW FROM tblUsers WHERE UserName = ?"""



class Database:

    def __init__(self):
        self.__conn = sqlite3.connect(DBNAME)
        self.__cursor = self.__conn.cursor()
        for i in CREATEQ:
            self.__cursor.execute(i)
    
    def addUser(self, userName, PW, supervisor=False):
        self.__cursor.execute(ADDUSERQ, (userName, PW, supervisor))
    
    def authenticateUser(self, userName, PW):
        records = self.__cursor.execute(AUTHENTICATEQ, (userName,)).fetchall()
        print(records)
        if len(records) != 1:
            return False
        else:
            if records[0][0] == PW:
                return True
            else:
                return False
    
if __name__ == "__main__":
    db = Database()
    db.addUser("TestUserA", "abcd")
    print(db.authenticateUser("TestUserA", "abcd"))
    print(db.authenticateUser("TestUserA", "abc"))
    print(db.authenticateUser("TestUserB", "abcd"))

