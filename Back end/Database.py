import sqlite3

DBNAME = "Back end/DB.db"

CREATEQ = ["""CREATE TABLE IF NOT EXISTS tblUsers (
            UserName VarChar(50) PRIMARY KEY,
            PW VarChar(50),
            Role VarChar(10));""",
            """CREATE TABLE IF NOT EXISTS tblHints (
            HintID INTEGER PRIMARY KEY AUTOINCREMENT,
            Text VarChar(500),
            QuestionID INTEGER,
            HintNo INTEGER);""",
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

AUTHENTICATEQ = """SELECT PW, Role FROM tblUsers WHERE UserName = ?"""

SUPERVISORSTUDENTSQ = """SELECT StudentUserName FROM tblSupervisorStudent WHERE SupervisorUserName = ?"""

ADDSTUDENTTOSUPERVISORQ = """INSERT INTO tblSupervisorStudent VALUES (?, ?)"""

ADDUSERHINTQ = """INSERT INTO tblUserHints VALUES (?, ?)"""

GETUSERHINTSQ = """SELECT HintID FROM tblUserHints WHERE UserName = ?"""

CHECKUSERHINTQ = """SELECT HintID FROM tblUserHints WHERE UserName = ? AND HintID = ?"""

GETHINTQ = """SELECT Text FROM tblHints WHERE HintID = ?"""

GETHINTNOQ = """SELECT Text, HintID FROM tblHints WHERE QuestionID = ? AND HintNo = ?"""

ADDHINTQ = """INSERT INTO tblHints (Text, QuestionID, HintNo) VALUES (?, ?, ?)"""

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
    
    def addUser(self, userName, PW, role):
        self.__cursor.execute(ADDUSERQ, (userName, PW, role))
        self.__conn.commit()
    
    def authenticateUser(self, userName, PW):
        records = self.__cursor.execute(AUTHENTICATEQ, (userName,)).fetchall()
        if len(records) != 1:
            return False, ""
        else:
            if records[0][0] == PW:
                return True, records[0][1]
            else:
                return False, ""
    
    def addStudentsForSupervisor(self, supervisorUserName, studentsUserNames):
        for i in studentsUserNames:
            self.__cursor.execute(ADDSTUDENTTOSUPERVISORQ, (supervisorUserName, i))
        self.__conn.commit()
            
    def getStudentsForSupervisor(self, supervisorUserName):
        studentsList = self.__cursor.execute(SUPERVISORSTUDENTSQ, (supervisorUserName,)).fetchall()
        return studentsList

    def addStudentHint(self, userName, hintID):
        record = self.__cursor.execute(CHECKUSERHINTQ, (userName, hintID)).fetchall()
        if len(record) == 0:
            self.__cursor.execute(ADDUSERHINTQ, (userName, hintID))
            self.__conn.commit()
    
    def getHint(self, Module, PaperNo, QuestionNo, HintNo):
        questionID = self.__cursor.execute(GETQUESTIONQ, (Module, PaperNo, QuestionNo)).fetchone()[0]
        return self.__cursor.execute(GETHINTNOQ, (questionID, HintNo)).fetchone()
    
    def getUserHints(self, userName):
        hintIDs = self.__cursor.execute(GETUSERHINTSQ, (userName,)).fetchall()
        hints = []
        for i in hintIDs:
            hints.append(self.__cursor.execute(GETHINTQ, (i[0],)).fetchone()[0])
        return hints

    def userSeenHint(self, userName, Module, PaperNo, QuestionNo, HintNo):
        questionID = self.__cursor.execute(GETQUESTIONQ, (Module, PaperNo, QuestionNo)).fetchone()[0]
        hintText, hintID = self.__cursor.execute(GETHINTNOQ, (questionID, HintNo)).fetchone()
        record = self.__cursor.execute(CHECKUSERHINTQ, (userName, hintID)).fetchall()
        if len(record) > 0:
            return True, hintText
        else:
            return False, ""

    def addHint(self, Text, QuestionID, HintNo):
        self.__cursor.execute(ADDHINTQ, (Text, QuestionID, HintNo))
        self.__conn.commit()
    
    def addQuestion(self, module, paperNo, questionNo):
        questionID = self.__cursor.execute(ADDQUESTIONQ, (module, paperNo, questionNo)).fetchone()[0]
        self.__conn.commit()
        return questionID

    def questionInDatabase(self, module, paperNo, questionNo):
        records = self.__cursor.execute(GETQUESTIONQ, (module, paperNo, questionNo)).fetchall()
        if len(records) > 0:
            return True, records[0][0]
        else:
            return False, 0
    
    def hintsInDatabase(self):
        records = self.__cursor.execute("""SELECT HintID FROM tblHints""").fetchall()
        if len(records) > 0:
            return True
        else:
            return False

    def getNumQuestions(self):
        questions = self.__cursor.execute("""SELECT * FROM tblQuestions""").fetchall()
        numQuestions = {}
        for i in questions:
            if not i[1] in numQuestions.keys():
                numQuestions[i[1]] = {}
            if not i[2] in numQuestions[i[1]].keys():
                numQuestions[i[1]][i[2]] = 1
            else:
                numQuestions[i[1]][i[2]] += 1
        return numQuestions
    
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
