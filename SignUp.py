from tinydb import TinyDB, Query
import uuid
import pickle
from Exceptions import *
import hashlib
from abc import ABC,abstractmethod

class Person(ABC):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        return self

    def __str__(self):
        return f"Name: {self.first_name} {self.mid_name} {self.last_name} \n Gender: {self.gender}"


class Account(Person):
    def __init__(self, name, gender, address, email, username, password, acc_type):
        self.owner = super().__init__(name, gender)
        self.email = email
        self.username = username
        self.address = address
        self.password = password
        self.account_type = acc_type

    def GenToken(self):
        uuid_str = uuid.uuid1().urn
        self.__token = uuid_str[9:]
        return self.__token

    @property
    def token(self):
        self.__token
    
    @token.getter
    def token_get(self):
        return self.__token

    def __str__(self):
        self.GenToken()
        return self.__token

class AdminAccount(Account):
    pass

class MemberAccount(Account):
    pass

class Encrypt_Data:
    def __init__(self, token, obj):
        self.token = token
        self.obj = obj

class Signup:
    DB = TinyDB("database.json")
    User = Query()
    def __init__(self,name, address, gender, email, username, password, acc_type) -> None:
        self.name = name
        self.address = address
        self.gender = gender
        self.email = email
        self.username = username
        self.password = password
        self.acc_type = acc_type
        self.Regester()

    def Regester(self):
        accounts = {}
        self.email = self.email.lower()
        if '@' not in self.email and '.' not in self.email:
            raise InvalidEmailError("Invalid Email!")
        if len(self.password) < 5:
            raise InvalidPasswordError("Password too short")
        self.password = self.password.encode()
        hash = hashlib.sha256(self.password)
        self.hashpass = hash.hexdigest()
        account = Account(self.name, self.gender,
                                       self.address, self.email, self.username, self.hashpass, self.acc_type)
        # if acc_type == "Savings":
            
        #     account = Savings_Account(f_name, m_name, l_name, gender,
        #                               address, email, username, hashhex, acc_type)
        # else:
            
        #     account = Current_Account(f_name, m_name, l_name, gender,
        #                               address, email, username, hashhex, acc_type)

        if self.DB.search(self.User.username == self.username):
            raise AccountExistsError("This Account already Exits")
        else:
            token = account.GenToken()

        encrypt = Encrypt_Data(token, account)
        with open(f'{token}.pkl', 'wb') as enc_file:
            pickle.dump(encrypt, enc_file, None)

        accounts["username"] = self.username
        accounts["token"] = token
        accounts["email"] = self.email
        self.DB.insert(accounts)

    def Print_Account_Details(self):
        data = self.DB.search(self.User.username == self.username)
        for entry in data:
            for key in entry:
                print(f"{key}: {entry[key]}")
