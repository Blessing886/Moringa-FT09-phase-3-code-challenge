from database.connection import get_db_connection

class Author:
    def __init__(self, id = None, name = None):
        if id is not None and not isinstance(id, int):
            raise ValueError("ID must be an integer.")
        if name is not None and (not isinstance(name, str) or len(name.strip()) == 0):
            raise ValueError("Name must be a non-empty string.")
        if id is None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
            self._id = cursor.lastrowid
            self._name = name
            conn.commit()
            conn.close()
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM authors WHERE id = ?", (id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                self._id = id
                self._name = row["name"]
            else:
                raise ValueError(f"No author found with ID {id}.")

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @classmethod
    def find_by_id(cls, author_id):
        if not isinstance(author_id, int):
            raise ValueError("Author id must be an integer.")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(id=row["id"], name=row["name"])
        else:
            return None

