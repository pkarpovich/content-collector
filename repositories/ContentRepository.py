from .BaseRepository import BaseRepository

class ContentRepository(BaseRepository):
    def __init__(self, db_file):
        columns = ['id INTEGER PRIMARY KEY', 'title VARCHAR', 'artist VARCHAR', 'album VARCHAR', 'position VARCHAR', 'app_identifier VARCHAR', 'device VARCHAR', 'media_type VARCHAR', 'created_at TIMESTAMP']
        super().__init__(db_file, "content_history", columns)
        super().create_table()
        super().create_sequence()