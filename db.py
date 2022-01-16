from fileinput import filename
import sqlite3, enum, re, const

class DB:
    class SearchCriteria(enum.Enum):
            ID = 0
            Name = 1
            Phone = 2
            Email = 3

    def __init__(self, FilePath = const.RAM_DB_PATH):
        self._db = sqlite3.connect(FilePath)

        self._db.cursor().execute('''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT unique, password TEXT)''')
        self._db.commit()

    def AddUser(self, Name, Phone, Email, Password):
        Email = Email.lower()
        self._db.cursor().execute('''INSERT INTO users(name, phone, email, password) VALUES(?,?,?,?)''', (Name, Phone, Email, Password))
        self._db.commit()
    
    def PrintDebugTable(self):
        print(self._db.cursor().execute('''SELECT * FROM users''').fetchall())

    def FindUser(self, SearchCriteria, Input):
        if SearchCriteria == self.SearchCriteria.Name:
            return self._db.cursor().execute('''SELECT id, name, phone, email FROM users WHERE name=?''', (Input,)).fetchone()
        elif SearchCriteria == self.SearchCriteria.Phone:
            return self._db.cursor().execute('''SELECT id, name, phone, email FROM users WHERE phone=?''', (Input,)).fetchone()
        elif SearchCriteria == self.SearchCriteria.Email:
            return self._db.cursor().execute('''SELECT id, name, phone, email FROM users WHERE email=?''', (Input,)).fetchone()
        elif SearchCriteria == self.SearchCriteria.ID:
            return self._db.cursor().execute('''SELECT id, name, phone, email FROM users WHERE id=?''', (Input,)).fetchone()
        return None

    def DoesUserExist(self, Email):
        if self.FindUser(self.SearchCriteria.Email, Email) != None:
            return True
        return False

    def AttemptLogIn(self, Email, Password):
        User = self.FindUser(self.SearchCriteria.Email, Email)
        if User != None:
            if self._DoesPasswordMatch(User[0], Password):
                return User[0]
        return -1
    
    def _DoesPasswordMatch(self, UserID, Password):
        CorrectPassword = self._db.cursor().execute('''SELECT password FROM users WHERE id=?''', (UserID,)).fetchall()[0][0]
        return Password == CorrectPassword

    def DeleteUser(self, ID, Password):
        if self._DoesPasswordMatch(ID, Password):
            self._db.cursor().execute('''DELETE FROM users WHERE id=? ''', (ID,))
            self._db.commit()
            return True
        return False
    
    @staticmethod
    def IsEmailValid(Email):
        Email = Email.lower()
        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', Email):
            return Email
        return False

    @staticmethod
    def IsPhoneValid(Phone):
        SanitizedValue = re.sub('[^0-9]','', Phone)
        if len(SanitizedValue) == 10:
            return SanitizedValue
        return False
    

