from database.connection import get_db_connection

from models.author import Author

class Magazine:
    def __init__(self, id = None, name = None, category = None):
        if id is not None and not isinstance(id, int):
            raise ValueError("id must be an integer.")
        if name is not None and (not isinstance(name,str) or not (2 <= len(name.strip()) <= 16)):
            raise ValueError("name must be a string between 2 and 16 characters.")
        if category is not None and (not isinstance(category, str) or len(category.strip()) == 0):
            raise ValueError("category must be a non empty string.")
        
        if id is None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO magazines (nae, category) VALUES (?, ?), (name, category)"
            )
            self._id = cursor.lastrowid
            self._name = name
            self._category = category
            conn.commit()
            conn.close()
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name, category FROM magazines WHERE id = ?", (id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                self._id = id
                self._name = row["name"]
                self._category = row["category"]
            else:
                raise ValueError(f"No magazine found with ID {id}.")
            
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value.strip()) <= 16):
            raise ValueError("name must be a string between 2 and 16 characters.")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE magazines SET name = ? WHERE id = ?", (value, self._id))
        conn.commit()
        conn.close()
        self._name = value

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len (value.strip()) == 0:
            raise ValueError("category must be a non empty string.")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE magazines SET category = ? WHERE id = ?", (value, self._id))
        conn.commit()
        conn.close()
        self._category = value

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    def articles(self):
        from models.article import Article

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT article.id, article.title, article.author_id, article.magazine_id
            FROM articles article
            JOIN magazines magazine ON article.magazine_id = magazine_id
            WHERE magazine.id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()

        return [
            Article(id=row["id"], title=row["title"], author=row["author_id"],
            magazine=row["magazine_id"]) for row in rows
            ]
    
    def contributors(self):
        from models.author import Author
        from models.article import Article

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT DISTINCT author.id, author.name
        FROM authors author
        JOIN articles article ON author.id = article.aurtor_id
        JOIN magazines magazine ON article.magazine_id = magazine.id
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()

        return [
            Article(id=row["id"], title=row["title"], author=row["author_id"],
            magazine=row["magazine_id"]) for row in rows
            ]

