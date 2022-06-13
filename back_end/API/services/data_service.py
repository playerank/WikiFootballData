from data.users import User

def create_user(username: str, password: str) -> User:
    """
    Create User and add it to db
    """
    user= User()
    user.username=username
    user.password=password # TODO : hash function to password
    user.is_online=False # se è sempre così si può mettere default=False nella classe User
    #Valore is_editor e is_administrator sono di default settati a False
    user.save()
    return user

def find_user_by_username(username: str) -> User:
    """
    Return the User indentified by username
    """
    #query di oggetti user con username=username, io ne voglio solo uno, così indico di fermarsi al primo,
    #ovviamente esendo univoco ce n'è solo uno.
    #User.objects().filter(username=username).first() query vera, se c'è un solo filtro posso usare ->
    user= User.objects(username=username).first()
    return user

def log_user(username: str, password: str) -> str:
    """
    Return U if username is incorrect, P if password is incorrect, L if user already logged,
    A if user is admin, E if user is admin and S if is a simple user
    """
    user:User=User.objects(username=username).first()
    #L'operazione fallisce
    if not user:
        return "U"
    if user.password!=password: #TODO : hash function to password
        return "P"
    if user.is_online:
        return "L"
    #L'operazione ha successo
    user.update(is_online=True)
    if user.is_administrator:
        return "A"
    if user.is_editor:
        return "E"
    else:
        return "S"