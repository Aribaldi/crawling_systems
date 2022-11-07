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

    def __eq__(self, other):
        if not isinstance(other, Post):
            return False

        return (
            self.post_id == other.post_id and
            self.group_id == other.group_id and
            self.publisher_id == other.publisher_id and
            self.date == other.date and
            self.text == other.text and
            self.comments == other.comments and
            self.likes == other.likes and
            self.reposts == other.reposts and
            self.views == other.views
        )
