"""Users models."""

# Config
from app.config.mysql_connection import connect_to_mysql
from app.utils.regular_expresions import NAME_REGEX, EMAIL_REGEX, PASSWORD_REGEX


class User:
    """Modelo de la clase Users."""

    def __init__(self, data: dict) -> None:
        """
        Constructor de la clase `user`.

        Parámetros:
            - self (object): Objeto de tipo `user`.
            - data (dict): Diccionario con los datos de la usuario.
        
        Retorno:
            None: Retorna nada.
        """

        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data.get("email")
        self.password = data.get("password")
        self.created_at = data.get("created_at", None)
        self.updated_at = data.get("updated_at", None)

    @staticmethod
    def valida_user(data):
        """
        Funcion para validar datos recibidos
        """
        errores = []


        if not NAME_REGEX.match(data['first_name']):
            errores.append("El nombre al menos tiene que tener dos caracteres")

        if not NAME_REGEX.match(data['last_name']):
            errores.append("El apellido al menos tiene que tener dos caracteres")

        if not EMAIL_REGEX.match(data['email']):
            errores.append("Formato de correo invalido correo@correo.com")

        if not PASSWORD_REGEX.match(data['password']):
            errores.append("La contraseña debe tener una letra minuscula y mayuscula")


        return errores

    @classmethod
    def get_all(cls):
        """
        Obtener todas las usuarios de la tabla `users`.
        
        El método `get_all` es un método de clase, lo que significa que se
        puede llamar directamente desde la clase `user` sin necesidad de
        crear una instancia (objeto).

        Parámetros:
            - cls (object): Objeto de tipo `user`.

        Retorno:
            - users (list): Lista de usuarios.
        """

        query = """SELECT * FROM users;"""
        results = connect_to_mysql().query_db(query)

        users: list = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls, data: dict):
        """
        Obtener un usuario por id.

        El método `get_one` es un método de clase, lo que significa que se
        puede llamar directamente desde la clase `user` sin necesidad de
        crear una instancia (objeto).
        """

        query = """SELECT * FROM users WHERE id = %(id)s;"""
        result = connect_to_mysql().query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls, data):
        """
        Obtener un usuario por email.

        El método `get_one` es un método de clase, lo que significa que se
        puede llamar directamente desde la clase `user` sin necesidad de
        crear una instancia (objeto).
        """

        query = """SELECT * FROM users WHERE email = %(email)s;"""
        result = connect_to_mysql().query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def create(cls, data: dict):
        """
        Crear un nuevo usuario.

        El método `create` es un método de clase, lo que significa que se
        puede llamar directamente desde la clase `user` sin necesidad de
        crear una instancia (objeto).

        Ejemplo: user.create({"name": "Joe Doe", "comment": "This is a comment"})

        Parámetros:
            - cls (object): Objeto de tipo `user`
            - data (dict): Diccionario con los datos de la usuario.

        Retorno:
            - id 
        """

        query = """INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""  # noqa: E501
        return connect_to_mysql().query_db(query, data)
    

    @classmethod
    def update(cls, data: dict):
        """
        Metodo para editar un usuario

        Parámetros:
            - cls (object): Objeto de tipo `user`
            - data (dict): Diccionario con los datos a actualizar.

        Retorno:
            -
        """

        query = """
                    UPDATE users SET 
                    first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s 
                    WHERE id = %(id)s;
                """  # noqa: E501
        return connect_to_mysql().query_db(query, data)
    

    @classmethod
    def delete(cls, data: dict):
        """
        Eliminar usuario.

        El método `delete` es un método de clase, lo que significa que se
        puede llamar directamente desde la clase `user` sin necesidad de
        crear una instancia (objeto).

        Parámetros:
            - cls (object): Objeto de tipo `user`
            - data (dict): Diccionario con el id a eliminar

        Retorno:
            -
        """

        query = """DELETE FROM users where id = %(id)s;"""  # noqa: E501
        return connect_to_mysql().query_db(query, data)
