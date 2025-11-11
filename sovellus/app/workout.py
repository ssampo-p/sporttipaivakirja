class Workout:
    def __init__(self,id , title, content, sent_at, workout_level, user_id= None, username =None, comments=None):
        self.id = id
        self.title = title
        self.content = content
        self.sent_at = sent_at
        self.workout_level = workout_level
        self.user_id = user_id
        self.username = username
        self.comments = comments or []
        
    def add_comment(self, comment):
        self.comments.append(comment)   
        
    def get_comments(self):
        return self.comments
    