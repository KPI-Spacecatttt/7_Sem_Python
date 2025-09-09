import datetime
import uuid
from datetime import timedelta


class Person:
    """Базовий клас для Студента та Викладача."""

    def __init__(self, name, email):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email


class Instructor(Person):
    """Клас для представлення викладача."""

    def __init__(self, name, email, department, specialization):
        super().__init__(name, email)
        self.department = department
        self.specialization = specialization
        self.courses_taught = []


class Student(Person):
    """Клас для представлення студента."""

    def __init__(self, name, email, major, year_of_study):
        super().__init__(name, email)
        self.major = major
        self.year_of_study = year_of_study
        self.enrolled_courses = []
        self.grades = {}

    def get_gpa(self):
        """Розраховує GPA студента на основі оцінок."""
        if not self.grades:
            return 0.0
        total_percentage = sum(grade.get_percentage() for grade in self.grades.values())
        return round((total_percentage / len(self.grades) / 100) * 4, 2)


class Course:
    """Клас для представлення курсу."""

    def __init__(self, title, description, credits, instructor, max_students=30):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.credits = credits
        self.instructor = instructor
        self.max_students = max_students
        self.enrolled_students = []
        self.assignments = []
        self.schedule = []
        self.attendance = {}  # {date: {student_id: status}}

    def add_schedule(self, day, start_time, end_time, location):
        """Додає запис у розклад курсу."""
        self.schedule.append(
            {
                "day": day,
                "start_time": start_time,
                "end_time": end_time,
                "location": location,
            }
        )
        print(
            f"Додано розклад для курсу '{self.title}': {day}, {start_time}-{end_time} в {location}"
        )

    def mark_attendance(self, date, attendance_data):
        """Відмічає відвідуваність студентів за певну дату."""
        if not isinstance(date, datetime.date):
            print("Помилка: дата повинна бути об'єктом datetime.date.")
            return

        self.attendance[date.strftime("%Y-%m-%d")] = attendance_data
        print(
            f"Записано відвідуваність для курсу '{self.title}' за {date.strftime('%Y-%m-%d')}."
        )

    def get_statistics(self):
        """Отримує та повертає статистику по цьому курсу."""
        # Збираємо всі оцінки, що стосуються тільки цього курсу
        course_grades = []
        course_assignment_ids = {a.id for a in self.assignments}

        for student in self.enrolled_students:
            for assignment_id, grade in student.grades.items():
                if assignment_id in course_assignment_ids:
                    course_grades.append(grade)

        if not course_grades:
            return {
                "course_title": self.title,
                "instructor": self.instructor.name,
                "enrolled_students": len(self.enrolled_students),
                "assignments_count": len(self.assignments),
                "average_grade": 0,
                "completion_rate": 0,
            }

        total_percentage = sum(grade.get_percentage() for grade in course_grades)
        average_grade = total_percentage / len(course_grades)

        # Розрахунок рівня виконання
        total_possible_submissions = len(self.enrolled_students) * len(self.assignments)
        actual_submissions = len(course_grades)
        completion_rate = (
            (actual_submissions / total_possible_submissions) * 100
            if total_possible_submissions > 0
            else 0
        )

        return {
            "course_title": self.title,
            "instructor": self.instructor.name,
            "enrolled_students": len(self.enrolled_students),
            "assignments_count": len(self.assignments),
            "average_grade": round(average_grade, 2),
            "completion_rate": round(completion_rate, 2),
        }

    def print_course_schedule(self):
        """Функція для гарного виводу розкладу конкретного курсу."""

        print(f"Розклад для курсу: '{self.title}' (Викладач: {self.instructor.name})")
        if not self.schedule:
            print("  - Розклад ще не додано.")
            return
        for session in self.schedule:
            day = session["day"]
            start = session["start_time"]
            end = session["end_time"]
            location = session["location"]
            print(f"  - {day}: {start} - {end} ({location})")


class Assignment:
    """Клас для представлення завдання."""

    def __init__(self, course_id, title, description, max_points, due_date):
        self.id = str(uuid.uuid4())[:8]
        self.course_id = course_id
        self.title = title
        self.description = description
        self.max_points = max_points
        self.due_date = due_date  # Очікується об'єкт datetime


class Grade:
    """Клас для представлення оцінки."""

    def __init__(self, student, assignment, points_earned, feedback=""):
        self.student_id = student.id
        self.assignment_id = assignment.id
        self.points_earned = float(points_earned)
        self.max_points = assignment.max_points
        self.feedback = feedback
        self.date_graded = datetime.datetime.now()

    def get_percentage(self):
        """Повертає оцінку у відсотках."""
        return (
            (self.points_earned / self.max_points) * 100 if self.max_points > 0 else 0
        )


class EducationSystem:
    """Клас для керування всією освітньою системою."""

    def __init__(self):
        self.courses = {}
        self.students = {}
        self.instructors = {}
        self.assignments = {}

    def add_instructor(self, name, email, department, specialization):
        instructor = Instructor(name, email, department, specialization)
        self.instructors[instructor.id] = instructor
        print(f"Викладач {name} доданий до системи з ID: {instructor.id}")
        return instructor

    def add_student(self, name, email, major, year_of_study):
        student = Student(name, email, major, year_of_study)
        self.students[student.id] = student
        print(f"Студент {name} зареєстрований у системі з ID: {student.id}")
        return student

    def create_course(
        self, title, description, credits, instructor_id, max_students=30
    ):
        if instructor_id not in self.instructors:
            print("Помилка: Викладач не знайдений")
            return None
        instructor = self.instructors[instructor_id]
        course = Course(title, description, credits, instructor, max_students)
        self.courses[course.id] = course
        instructor.courses_taught.append(course)
        print(f"Курс '{title}' створено з ID: {course.id}")
        return course

    def enroll_student(self, student_id, course_id):
        student = self.students.get(student_id)
        course = self.courses.get(course_id)
        if not student or not course:
            print("Помилка: Студент або курс не знайдені.")
            return False
        if len(course.enrolled_students) >= course.max_students:
            print("Помилка: Курс переповнений.")
            return False
        if student in course.enrolled_students:
            print("Помилка: Студент вже зарахований на цей курс.")
            return False

        course.enrolled_students.append(student)
        student.enrolled_courses.append(course)
        print(f"Студент {student.name} зарахований на курс '{course.title}'")
        return True

    def create_assignment(self, course_id, title, description, max_points, due_date):
        if course_id not in self.courses:
            print("Помилка: Курс не знайдений.")
            return None
        assignment = Assignment(course_id, title, description, max_points, due_date)
        self.assignments[assignment.id] = assignment
        self.courses[course_id].assignments.append(assignment)
        print(
            f"Завдання '{title}' створено для курсу '{self.courses[course_id].title}'"
        )
        return assignment

    def submit_grade(self, student_id, assignment_id, points_earned, feedback=""):
        student = self.students.get(student_id)
        assignment = self.assignments.get(assignment_id)
        if not student or not assignment:
            print("Помилка: Студент або завдання не знайдені.")
            return False

        grade = Grade(student, assignment, points_earned, feedback)
        student.grades[assignment.id] = grade
        print(
            f"Оцінка {points_earned}/{assignment.max_points} виставлена студенту {student.name}"
        )
        return True

    def check_deadline_reminders(self, days_in_advance=7):
        """Знаходить завдання з наближенням дедлайну."""
        print(f"\n Перевірка дедлайнів (за {days_in_advance} днів)...")
        upcoming_deadlines = []
        now = datetime.datetime.now()

        for assignment in self.assignments.values():
            time_left = assignment.due_date - now
            if timedelta(days=0) < time_left <= timedelta(days=days_in_advance):
                course = self.courses[assignment.course_id]
                upcoming_deadlines.append(
                    {
                        "assignment_title": assignment.title,
                        "course_title": course.title,
                        "due_date": assignment.due_date.strftime("%Y-%m-%d %H:%M"),
                        "students_enrolled": len(course.enrolled_students),
                    }
                )

        if not upcoming_deadlines:
            print("Немає завдань з наближенням дедлайну.")
            return

        for deadline in upcoming_deadlines:
            print(
                f"  - Курс: '{deadline['course_title']}', Завдання: '{deadline['assignment_title']}'"
            )
            print(
                f"    Дедлайн: {deadline['due_date']}. Зараховано студентів: {deadline['students_enrolled']}"
            )


if __name__ == "__main__":
    system = EducationSystem()

    # 1. Створення викладачів та студентів
    print("--- 1. Створення користувачів ---")
    inst1 = system.add_instructor(
        "Др. Іван Петренко", "petrov@uni.edu", "Комп'ютерні науки", "Програмування"
    )
    inst2 = system.add_instructor(
        "Др. Марія Коваленко", "maria@uni.edu", "Математика", "Алгебра"
    )

    stu1 = system.add_student(
        "Анна Іваненко", "anna@student.edu", "Комп'ютерні науки", 2
    )
    stu2 = system.add_student("Микола Сидоров", "mykola@student.edu", "Математика", 1)

    # 2. Створення курсів та зарахування студентів
    print("\n--- 2. Створення курсів та зарахування ---")
    cs_course = system.create_course(
        "Основи програмування", "Вступ до Python", 4, inst1.id
    )
    math_course = system.create_course(
        "Лінійна алгебра", "Векторні простори", 3, inst2.id
    )

    if not (cs_course and math_course):
        print("Помилка при створенні курсів. Завершення роботи.")
        exit(1)

    system.enroll_student(stu1.id, cs_course.id)
    system.enroll_student(stu2.id, cs_course.id)
    system.enroll_student(stu1.id, math_course.id)

    # 3. Додавання розкладу до курсу (НОВА ФУНКЦІЯ)
    print("\n--- 3. Створення розкладу занять ---")
    cs_course.add_schedule("Понеділок", "10:00", "11:30", "Аудиторія 101")
    cs_course.add_schedule("Середа", "10:00", "11:30", "Аудиторія 101")
    math_course.add_schedule("Вівторок", "14:00", "15:30", "Аудиторія 205")

    # 4. Створення завдань та виставлення оцінок
    print("\n--- 4. Створення завдань та оцінювання ---")
    asg1 = system.create_assignment(
        cs_course.id,
        "Лаб 1",
        "Основи Python",
        100,
        datetime.datetime(2025, 9, 20, 23, 59),
    )
    # Завдання з дедлайном, що наближається (необхідно для пункту 6)
    asg2 = system.create_assignment(
        cs_course.id,
        "Лаб 2",
        "Функції",
        150,
        datetime.datetime.now() + timedelta(days=5),
    )

    if not (asg1 and asg2):
        print("Помилка при створенні завдань. Завершення роботи.")
        exit(1)

    system.submit_grade(stu1.id, asg1.id, 95, "Відмінно!")
    system.submit_grade(stu2.id, asg1.id, 78, "Добре, але є помилки.")

    # 5. Електронний журнал відвідуваності
    print("\n--- 5. Журнал відвідуваності ---")
    attendance_today = {stu1.id: "present", stu2.id: "absent"}
    cs_course.mark_attendance(datetime.datetime.now().date(), attendance_today)

    # Виведемо журнал для перевірки
    print("Записи відвідуваності для курсу 'Основи програмування':")
    print(cs_course.attendance)

    # 6. Автоматичні нагадування про дедлайни
    print("\n--- 6. Нагадування про дедлайни ---")
    system.check_deadline_reminders(days_in_advance=7)

    # 7. Перегляд інформації
    print("\n--- 7. Перегляд інформації ---")
    print(f"GPA Анни Іваненко: {stu1.get_gpa()}")
    print(f"GPA Миколи Сидорова: {stu2.get_gpa()}")

    cs_course = system.courses.get(cs_course.id)

    # 8. Статистика курсу
    print("\n--- 8. Перегляд cтатистики для курсу ---")
    if cs_course:
        stats = cs_course.get_statistics()
        print(f"Статистика для курсу '{stats['course_title']}':")
        print(f"  - Середня оцінка: {stats['average_grade']}%")
        print(f"  - Рівень виконання завдань: {stats['completion_rate']}%")

    # 9. Вивід розкладу
    print("\n--- 9. Вивід розкладу ---")
    if cs_course:
        cs_course.print_course_schedule()
    else:
        print("Курс не знайдено, неможливо вивести розклад.")

