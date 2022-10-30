class Post:
    def __init__(
            self,
            post_id: int,
            group_id: int,
            publisher_id: int,
            date: int,
            text: str,
            comments: int,
            likes: int,
            reposts: int,
            views: int,
    ):
        self.post_id = post_id
        self.group_id = group_id
        self.publisher_id = publisher_id
        self.date = date
        self.text = text
        self.comments = comments
        self.likes = likes
        self.reposts = reposts
        self.views = views
