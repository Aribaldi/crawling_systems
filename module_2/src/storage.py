import psycopg2

from src.post import Post


class Storage:

    def store_post(self, post: Post):
        raise NotImplementedError

    def load_posts(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class PostgresDB(Storage):
    def __init__(self, crawler_name, host, db_name, user_name, password):
        self.conn = psycopg2.connect(
            host=host,
            database=db_name,
            user=user_name,
            password=password)
        self.db = self.conn.cursor()
        self.crawler_name = crawler_name

    def store_post(self, post):
        self.db.execute("INSERT INTO post(post_id, group_id, publisher_id, date_unix, text, " +
                        "comments, likes, reports, views, crawler_name)\n" +
                        f"VALUES ({post.post_id}, {post.group_id}, {post.publisher_id}, {post.date}, {post.text}" +
                        f"{post.comments}, {post.likes}, {post.reposts}, {post.views}, {self.crawler_name});")

    def load_posts(self):
        self.db.execute("SELECT post_id, group_id, publisher_id, date_unix, text, " +
                        "comments, likes, reports, views, crawler_name FROM post")

        posts = self.db.fetchall()
        posts = [Post(*post) for post in posts]
        return posts

    def store_cache(self, cache):
        if len(cache) > 0:
            query = "INSERT INTO group_cache(group_id, crawler_name) VALUES " + \
                    ", ".join([f"({item}, '{self.crawler_name}')" for item in cache])
            self.db.execute(query)

    def load_cache(self):
        self.db.execute("SELECT group_id FROM group_cache")
        cache = self.db.fetchall()
        return cache

    def close(self):
        self.conn.commit()
        self.conn.close()




