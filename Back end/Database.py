import sqlite3

DBNAME = "Back end/DB.db"

CREATEQ = ["""CREATE TABLE IF NOT EXISTS tblUsers (
            UserName VarChar(50) PRIMARY KEY,
            PW VarChar(50),
            Supervisor BOOLEAN);""",
            """CREATE TABLE IF NOT EXISTS tblHints (
            HintID INTEGER PRIMARY KEY AUTOINCREMENT,
            Text VarChar(500),
            QuestionID INTEGER);""",
            """CREATE TABLE IF NOT EXISTS tblUserHints (
            UserName VarChar(50),
            HintID INTEGER,
            PRIMARY KEY(UserName, HintID));""",
            """CREATE TABLE IF NOT EXISTS tblSupervisorStudent (
            SupervisorUserName VarChar(50),
            StudentUserName VarChar(50),
            PRIMARY KEY(SupervisorUserName, StudentUserName)
            );""",
            """CREATE TABLE IF NOT EXISTS tblQuestions (
            QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
            Module VarChar(50),
            PaperNo INTEGER,
            QuestionNo INTEGER);"""]

ADDUSERQ = """INSERT INTO tblUsers VALUES (?, ?, ?)"""

AUTHENTICATEQ = """SELECT PW FROM tblUsers WHERE UserName = ?"""

SUPERVISORSTUDENTSQ = """SELECT StudentUserName FROM tblSupervisorStudent WHERE SupervisorUserName = ?"""

ADDSTUDENTTOSUPERVISORQ = """INSERT INTO tblSupervisorStudent VALUES (?, ?)"""

ADDUSERHINTQ = """INSERT INTO tblUserHints VALUES (?, ?)"""

GETUSERHINTSQ = """SELECT HintID FROM tblUserHints WHERE UserName = ?"""

GETHINTQ = """SELECT Text FROM tblHints WHERE HintID = ?"""

ADDHINTQ = """INSERT INTO tblHints (Text, QuestionID) VALUES (?, ?)"""

ADDQUESTIONQ = """INSERT INTO tblQuestions (Module, PaperNo, QuestionNo) VALUES (?, ?, ?) RETURNING QuestionID"""

GETQUESTIONQ = """SELECT QuestionID FROM tblQuestions WHERE Module = ? AND PaperNo = ? AND QuestionNo = ?"""

class Database:

    def __init__(self):
        self.__conn = sqlite3.connect(DBNAME)
        self.__cursor = self.__conn.cursor()
        for i in CREATEQ:
            self.__cursor.execute(i)
        self.__conn.commit()
    
    def close(self):
        self.__conn.close()
    
    def addUser(self, userName, PW, supervisor=False):
        self.__cursor.execute(ADDUSERQ, (userName, PW, supervisor))
        self.__conn.commit()
    
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
        self.__conn.commit()
            
    def getStudentsForSupervisor(self, supervisorUserName):
        studentsList = self.__cursor.execute(SUPERVISORSTUDENTSQ, (supervisorUserName,)).fetchall()
        return studentsList

    def addStudentHint(self, userName, hintID):
        self.__cursor.execute(ADDUSERHINTQ, (userName, hintID))
        self.__conn.commit()
    
    def getHint(self, Module, PaperNo, QuestionNo):
        questionID = self.__cursor.execute(GETQUESTIONQ, (Module, PaperNo, QuestionNo)).fetchone()[0]
        return self.__cursor.execute(GETHINTQ, (questionID,)).fetchone()[0]
    
    def getUserHints(self, userName):
        hintIDs = self.__cursor.execute(GETUSERHINTSQ, (userName,)).fetchall()
        hints = []
        for i in hintIDs:
            hints.append(self.__cursor.execute(GETHINTQ, (i[0],)).fetchone()[0])
        return hints
        

    def addHint(self, Text, QuestionID):
        self.__cursor.execute(ADDHINTQ, (Text, QuestionID))
    
    def addQuestion(self, module, paperNo, questionNo):
        questionID = self.__cursor.execute(ADDQUESTIONQ, (module, paperNo, questionNo)).fetchone()[0]
        self.__conn.commit()
        return questionID
    
    def hintsInDatabase(self):
        records = self.__cursor.execute("""SELECT HintID FROM tblHints""").fetchall()
        if len(records) > 0:
            return True
        else:
            return False

    
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
