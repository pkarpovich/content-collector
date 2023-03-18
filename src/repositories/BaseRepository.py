import duckdb


class BaseRepository:
    def __init__(self, db_file, table_name, columns):
        self.con = duckdb.connect(db_file)
        self.cur = self.con.cursor()
        self.table_name = table_name
        self.columns = columns

    def create_sequence(self):
        self.cur.execute(f"CREATE SEQUENCE IF NOT EXISTS {self.table_name}_id_seq")
        self.con.commit()

    def create_table(self):
        columns_str = ", ".join(self.columns)
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_str})")
        self.con.commit()

    def insert_record(self, values):
        values_str = ", ".join(["?" for _ in values])
        self.cur.execute(f"INSERT INTO {self.table_name} VALUES (nextval('{self.table_name}_id_seq'), {values_str}, CURRENT_TIMESTAMP)", values)
        self.con.commit()

    def get_records(self):
        self.cur.execute(f"SELECT * FROM {self.table_name}")
        rows = self.cur.fetchall()
        return rows

    def update_record(self, record_id, values):
        values_str = ", ".join([f"{key}='{value}'" for key, value in values.items()])
        self.cur.execute(f"UPDATE {self.table_name} SET {values_str} WHERE id={record_id}")
        self.con.commit()

    def delete_record(self, record_id):
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE id={record_id}")
        self.con.commit()

    def __del__(self):
        self.con.close()