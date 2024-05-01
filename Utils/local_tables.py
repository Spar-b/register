class LocalTables:
    def __init__(self):

        self.user_subjects = []
        self.subject_departments = []
        self.subjects = []
        self.departments = []
        self.specializations = []
        self.years = []
        self.groups = []
        self.students = []

    def print_all(self):
        for name, value in vars(self).items():
            print(f"{name}: {value}")