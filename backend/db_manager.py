import sqlite3


class DatabaseManager:

    def __init__(self, db_name="/data/jobs.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.create_table()

    def execute(self, query, params=(), fetchone=False, fetchall=False):

        cursor = self.connection.cursor()
        cursor.execute(query, params)

        result = None

        if fetchone:
            result = cursor.fetchone()

        if fetchall:
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def create_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS jobs(
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_name TEXT UNIQUE,
            image TEXT,
            command TEXT,
            namespace TEXT,
            status TEXT,
            start_time TEXT,
            completion_time TEXT
        )
        """

        self.execute(query)

    def save_job(self, job_name, image, command, namespace):

        query = """
        INSERT INTO jobs (job_name, image, command, namespace, status)
        VALUES (?, ?, ?, ?, ?)
        """

        self.execute(query, (job_name, image, command, namespace, "Running"))

    def update_job_status(self, job_name, status, start_time, completion_time):

        query = """
        UPDATE jobs
        SET status=?, start_time=?, completion_time=?
        WHERE job_name=?
        """

        self.execute(query, (status, start_time, completion_time, job_name))

    def get_job(self, job_name):

        query = "SELECT * FROM jobs WHERE job_name=?"

        return self.execute(query, (job_name,), fetchone=True)

    def get_all_jobs(self):

        query = "SELECT * FROM jobs"

        return self.execute(query, fetchall=True)

    def delete_job(self, job_name):

        query = "DELETE FROM jobs WHERE job_name=?"

        self.execute(query, (job_name,))