class Workout:
    def __init__(self, workout_id, title,
                 content, sent_at,
                 workout_level, sport,
                 user_id= None, username =None,
                 comments=None,):
        self.id = workout_id
        self.title = title
        self.content = content
        self.sent_at = sent_at
        self.workout_level = workout_level
        self.sport = sport
        self.user_id = user_id
        self.username = username
        self.comments = comments or []
        
    def add_comment(self, comment):
        self.comments.append(comment)
             
    def get_comments(self):
        return self.comments
    