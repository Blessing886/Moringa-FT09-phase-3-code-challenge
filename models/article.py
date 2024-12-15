from database.connection import get_db_connection


class Article:
    def __init__(self, title, author, magazine):
        from models.author import Author
        from models.magazine import Magazine

        if not isinstance(author, Author):
            raise ValueError("Author must be an instance of the Author class.")
        if not isinstance (magazine, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        if not isinstance(title, str) or not (5 <= len(title.strip()) <= 50):
            raise ValueError("title must be a string between 5 and 50 characters.")
        
        self._author = author
        self._magazine = magazine

        conn = get_db_connection()
        cursor = conn.cursor()

        if not hasattr(self, '_id'):
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (title, author.id, magazine.id),
            )
            self._id = cursor.lastrowid
            self._title = title
            conn.commit()
        else:
            cursor.execute(
                "SELECT title FROM articles WHERE id = ?", (self._id,)
            )
            row = cursor.fetchone()
            if row:
                self._title = row["title"]
            else:
                raise ValueError(f"No article found with id {self._id}.")
            conn.close()
        
    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT author.id, author.name
            FROM authors author
            JOIN articles article ON author.id = article.author_id
            WHERE article.id = ?
        """, (self.id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Author(id=row["id"], name=row["name"])
        else:
            raise ValueError(f"No author found for article ID {self.id}.")
    
    @property
    def magazine(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT magazine.id, magazine.name, magazine.category
        FROM magazines magazine
        JOIN articles article ON magazine.id = article.magazine_id
        WHERE article.id = ?
        """, (self.id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Magazine(id=row["id"], name=row["name"], category=row["category"])
        else:
            raise ValueError(f"No magazine found for article ID {self.id}.")

    def __repr__(self):
        return f'<Article {self.title}>'
