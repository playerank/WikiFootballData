from data.users import User
from typing import List
from passlib.context import CryptContext

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

#USERS_API
def get_user(username: str) -> User:
    """
    Return the User indentified by username
    """
    #query di oggetti user con username=username, io ne voglio solo uno, così indico di fermarsi al primo,
    #ovviamente esendo univoco ce n'è solo uno.
    #User.objects().filter(username=username).first() query vera, se c'è un solo filtro posso usare ->
    user: User=User.objects(username=username).first()
    return user

def hash_password(password):
    """
    Return the hashed password
    """
    return pwd_context.hash(password)

def create_user(username: str, password) -> User:
    """
    Create User and add it to db, return True if operation is successful, False otherwise
    """
    user= User()
    user.username=username
    user.password=hash_password(password)
    user.is_online=False
    #Valore is_editor e is_administrator sono di default settati a False
    user.save()
    return user

def log_user(username: str, password: str):
    """
    Log a User verifying its password.
    Return U if username is incorrect, P if password is incorrect, L if user already logged,
    A if user is admin, E if user is admin and S if is a simple user
    """
    user:User=User.objects(username=username).first()
    #L'operazione fallisce
    if not user:
        return "U"
    if not pwd_context.verify(password, user.password):
        return "P"
    if user.is_online:
        return "L"
    #L'operazione ha successo
    user.update(is_online=True)
    if user.is_administrator:
        return "A"
    if user.is_editor:
        return "E"
    return "S"

def verify_role(username: str):
    """
    Return the role of the User identified by username
    """
    user=get_user(username)
    if not user:
        return "U"
    if not user.is_online:
        return "M" #mistake
    if user.is_administrator:
        return "A"
    if user.is_editor:
        return "E"
    return "S" #simple User

def add_editor(username: str) -> bool:
    """
    Change the role of a User to editor.
    Return True if operation is successful, False otherwise
    """
    new_editor:User=User.objects(username=username).first()
    #L'operazione fallisce
    if not new_editor:
        return False
    new_editor.update(is_editor=True)
    return True

def get_users(n: int) -> List[User]:
    """
    Return the list of n Users from the db (clearly not the passwords)
    """
    if n==0:
        users:List[User]=list(User.objects().only('username','is_online','is_editor','is_administrator').all())
    else:
        users:List[User]=list(User.objects[:n].only('username','is_online','is_editor','is_administrator'))
    #debug
    # for u in users:
    #     print("Utente {}: online {}, editor {}, administrator {}".format(u.username,u.is_online,u.is_editor,u.is_administrator))
    return users

def get_online_users(n: int) -> List[User]:
    """
    Retrun the list of online Users (clearly not the passwords)
    """
    if n==0:
        online_users:List[User]=list(User.objects().filter(is_online=True).only('username','is_editor','is_administrator').all())
    else:
        online_users:List[User]=list(User.objects[:n].filter(is_online=True).only('username','is_editor','is_administrator'))
    return online_users