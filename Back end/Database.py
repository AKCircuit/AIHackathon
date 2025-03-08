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

SUPERVISORSTUDENTSQ = """SELECT StudentUserName FROM tblSupervisorStudent WHERE SupervisorUserName = ?"""

ADDSTUDENTTOSUPERVISORQ = """INSERT INTO tblSupervisorStudent VALUES (?, ?)"""

ADDUSERHINTQ = """INSERT INTO tblUserHints VALUES (?, ?)"""

GETUSERHINTSQ = """SELECT HintID FROM tblUserHints WHERE UserName = ?"""

GETHINTQ = """SELECT Text FROM tblHints WHERE HintID = ?"""

ADDHINTQ = """INSERT INTO tblHints (Text) VALUES (?)"""

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
        if len(records) != 1:
            return False
        else:
            if records[0][0] == PW:
                return True
            else:
                return False
    
    def addStudentsForSupervisor(self, supervisorUserName, studentsUserNames):
        for i in studentsUserNames:
            self.__cursor.execute(ADDSTUDENTTOSUPERVISORQ, (supervisorUserName, i))
            
    def getStudentsForSupervisor(self, supervisorUserName):
        studentsList = self.__cursor.execute(SUPERVISORSTUDENTSQ, (supervisorUserName,)).fetchall()
        return studentsList

    def addStudentHint(self, userName, hintID):
        self.__cursor.execute(ADDUSERHINTQ, (userName, hintID))
    
    def getUserHints(self, userName):
        hintIDs = self.__cursor.execute(GETUSERHINTSQ, (userName,)).fetchall()
        hints = []
        for i in hintIDs:
            hints.append(self.__cursor.execute(GETHINTQ, (i[0],)).fetchone()[0])
        return hints
        

    def addHint(self, Text):
        self.__cursor.execute(ADDHINTQ, (Text,))
        '''Need to add delimiter separating
            hints for different questions later on when the front-end is finished'''


    
if __name__ == "__main__":
    db = Database()
    db.addUser("TestUserA", "abcd")
    print(db.authenticateUser("TestUserA", "abcd"))
    print(db.authenticateUser("TestUserA", "abc"))
    print(db.authenticateUser("TestUserB", "abcd"))

    db.addUser("TestSupervisor", "abcd", True)
    db.addStudentsForSupervisor("TestSupervisor", ["TestUserA"])
    print(db.getStudentsForSupervisor("TestSupervisor"))

    db.addHint("TestHintA")
    db.addStudentHint("TestUserA", 1)
    print(db.getUserHints("TestUserA"))
