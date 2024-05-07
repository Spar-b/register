from Utils import stats


class SaveTable:
    def __init__(self):
        print("")

    @staticmethod
    def save(master):
        db = master.db
        data = stats.table_data[1:]
        print(f"save_data: {data}")
        match stats.current_table:
            case "subjects":
                from Classes.User_accounting.Subject import Subject
                from Classes.Misc.UserSubject import UserSubject
                for row in data:
                    subject = Subject(row[0], row[1])
                    user_subject = UserSubject(stats.current_user.id, row[0])
                    stats.local_tables.subjects.append(subject)
                    stats.local_tables.user_subjects.append(user_subject)

                    Subject.save_all(data, db)
                    stats.table_saved = True

            case "departments":
                from Classes.Student_accounting.Department import Department
                from Classes.Misc.SubjectDepartment import SubjectDepartment
                for row in data:
                    department = Department(row[0], row[1])
                    subject_department = SubjectDepartment(stats.current_parent_id, row[0])
                    stats.local_tables.departments.append(department)
                    stats.local_tables.subject_departments.append(subject_department)

                    Department.save_all(data, db)
                    stats.table_saved = True

            case "specializations":
                from Classes.Student_accounting.Specialization import Specialization
                for row in data:
                    specialization = Specialization(row[0], row[1], stats.current_parent_id)
                    stats.local_tables.specializations.append(specialization)

                    Specialization.save_all(data, db)
                    stats.table_saved = True

            case "years":
                from Classes.Student_accounting.Year import Year
                for row in data:
                    year = Year(row[0], stats.current_parent_id)
                    stats.local_tables.years.append(year)

                    Year.save_all(data, db)
                    stats.table_saved = True

            case "student_groups":
                import Classes.Student_accounting.Group as Group
                for row in data:
                    group = Group.Group(row[0], stats.current_parent_id)
                    stats.local_tables.groups.append(group)

                    Group.Group.save_all(data, db)
                    stats.table_saved = True

            case "students":
                from Classes.Student_accounting.Student import Student
                from Classes.Misc.RegisterHeading import RegisterHeading

                headings_data = stats.table_data[0][2:]
                print(f"Headings data: {headings_data}")
                RegisterHeading.save_all(headings_data, db)

                for row in data:
                    student = Student(row[0], row[1], stats.current_parent_id)
                    if len(row) == 4:
                        student.email = row[3]
                    stats.local_tables.students.append(student)

                from Classes.Student_accounting.Grade import Grade
                grade_id = 0
                grades_list = []
                for row in data:
                    student_id = row[0]
                    grade_num = 0
                    for cell in row:
                        if cell == row[0] or cell == row[1]:
                            continue
                        if cell is not None:
                            grade_value = cell
                            grade = [grade_id, student_id, grade_num, grade_value]
                            grades_list.append(grade)

                        grade_id += 1
                        grade_num += 1

                student_data = [row[0:2] for row in data]

                Student.save_all(student_data, db)
                Grade.save_all(grades_list, db)
                stats.table_saved = True

        stats.local_tables.print_all()
