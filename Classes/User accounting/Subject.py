class Subject:
    def __init__(self, id, subject_name):
        self.id = id
        self.subject_name = subject_name
        self.users = []
        self.departments = []