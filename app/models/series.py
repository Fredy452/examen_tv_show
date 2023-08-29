"""Series models."""

# Config
from app.config.mysql_connection import connect_to_mysql
from app.utils.regular_expresions import TITLE_REGEX, NETWORK_REGEX, DESCRIPTION_REGEX # noqa: E501


class Serie:
    """Modelo de la clase Series."""

    def __init__(self, data: dict) -> None:
        """
        Constructor de la clase `serie`.

        Parámetros:
            - self (object): Objeto de tipo `serie`.
            - data (dict): Diccionario con los datos de la serie.
        
        Retorno:
            None: Retorna nada.
        """

        self.first_name = data["first_name"]
        self.last_name = data["last_name"]

        self.id = data["id"]
        self.user_id = data["user_id"]
        self.title = data["title"]
        self.network = data["network"]
        self.release_date = data.get("release_date")
        self.description = data.get("description")
        self.created_at = data.get("created_at", None)
        self.updated_at = data.get("updated_at", None)

    @staticmethod
    def validar_serie(data):
        """
        Funcion para validar datos recibidos
        """
        errores = []


        if not TITLE_REGEX.match(data['title']):
            errores.append("El titulo al menos tiene que tener tres caracter")

        if not NETWORK_REGEX.match(data['network']):
            errores.append("El network al menos tiene que tener tres caracter")

        if not DESCRIPTION_REGEX.match(data['description']):
            errores.append("La descripción al menos tiene que tener tres caracters")

        return errores

    @classmethod
    def get_serie_whit_user(cls):
        """
        Obtener todas las series y el usuario de la tabla `series`.
        
        El método `get_all` es un método de clase, lo que significa que se
        puede llamar directamente desde la clase `serie` sin necesidad de
        crear una instancia (objeto).

        Parámetros:
            - cls (object): Objeto de tipo `serie`.

        Retorno:
            - series (list): Lista de series.
        """

        query = """
                SELECT series.id, series.title, series.network, series.release_date, users.first_name, users.last_name, users.id as user_id 
                FROM series
                JOIN users ON users.id = series.user_id;
        """  # noqa: E501
        results = connect_to_mysql().query_db(query)
        return results

    @classmethod
    def get_one(cls, data: dict):
        """
        Obtener una serie por id.

        El método `get_one` es un método de clase, lo que significa que se
        puede llamar directamente desde la clase `serie` sin necesidad de
        crear una instancia (objeto).
        """

        query = """
                SELECT *, users.first_name, users.last_name 
                FROM series
                join users on users.id = series.user_id 
                WHERE series.id = %(id)s; 
                """
        result = connect_to_mysql().query_db(query, data)
        return cls(result[0])

    @classmethod
    def create(cls, data: dict):
        """
        Crear una nuevo serie.

        El método `create` es un método de clase, lo que significa que se
        puede llamar directamente desde la clase `serie` sin necesidad de
        crear una instancia (objeto).


        Parámetros:
            - cls (object): Objeto de tipo `serie`
            - data (dict): Diccionario con los datos de la serie.

        Retorno:
            - id 
        """

        query = """INSERT INTO series (user_id, title, network, release_date, description) VALUES (%(user_id)s, %(title)s, %(network)s, %(release_date)s, %(description)s);"""  # noqa: E501
        return connect_to_mysql().query_db(query, data)
    

    @classmethod
    def update(cls, data: dict):
        """
        Metodo para editar un serie

        Parámetros:
            - cls (object): Objeto de tipo `serie`
            - data (dict): Diccionario con los datos a actualizar.

        Retorno:
            -
        """

        query = """
                    UPDATE series SET 
                    title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, user_id = %(user_id)s
                    WHERE id = %(id)s;
                """  # noqa: E501
        return connect_to_mysql().query_db(query, data)
    

    @classmethod
    def delete(cls, data: dict):
        """
        Eliminar serie.

        El método `delete` es un método de clase, lo que significa que se
        puede llamar directamente desde la clase `serie` sin necesidad de
        crear una instancia (objeto).

        Parámetros:
            - cls (object): Objeto de tipo `serie`
            - data (dict): Diccionario con el id a eliminar

        Retorno:
            -
        """

        query = """DELETE FROM series where id = %(id)s;"""  # noqa: E501
        return connect_to_mysql().query_db(query, data)

    @classmethod
    def like(cls, data: dict):
        """
        Agregar like.
        """

        query = """insert into likes(user_id, serie_id) values(%(user_id)s, %(serie_id)s);"""  # noqa: E501
        return connect_to_mysql().query_db(query, data)


    @classmethod
    def get_like(cls, data: list):
        """
        Obtener likes
        """

        query = """
                SELECT users.id as user_id, users.first_name, series.id as series_id, series.title
                FROM users
                LEFT JOIN likes ON users.id = likes.user_id
                LEFT JOIN series ON likes.serie_id = series.id
                WHERE users.id = %(id)s;
        """  # noqa: E501
        results = connect_to_mysql().query_db(query, data)
        return results