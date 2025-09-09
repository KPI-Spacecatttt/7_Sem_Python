# Система управління курсами та оцінками
education_system = {
    "courses": {},  # ID курсу: інформація про курс
    "students": {},  # ID студента: інформація про студента
    "instructors": {},  # ID викладача: інформація про викладача
    "enrollments": {},  # ID запису: інформація про зарахування
    "grades": [],  # оцінки
    "assignments": {},  # завдання
}


def add_instructor(instructor_id, name, email, department, specialization):
    """Додає викладача до системи"""
    education_system["instructors"][instructor_id] = {
        "name": name,
        "email": email,
        "department": department,
        "specialization": specialization,
        "courses_taught": [],
    }
    print(f"Викладач {name} додан до системи")


def add_student(student_id, name, email, major, year_of_study):
    """Додає студента до системи"""
    education_system["students"][student_id] = {
        "name": name,
        "email": email,
        "major": major,
        "year_of_study": year_of_study,
        "enrolled_courses": [],
        "gpa": 0.0,
        "total_credits": 0,
    }
    print(f"Студент {name} зареєстрован у системі")


def create_course(
    course_id, title, description, credits, instructor_id, max_students=30
):
    """Створює новий курс"""
    if instructor_id not in education_system["instructors"]:
        print("Викладач не знайдений")
        return False
    education_system["courses"][course_id] = {
        "title": title,
        "description": description,
        "credits": credits,
        "instructor_id": instructor_id,
        "max_students": max_students,
        "enrolled_students": [],
        "assignments": [],
        "schedule": {},
    }
    education_system["instructors"][instructor_id]["courses_taught"].append(course_id)
    instructor_name = education_system["instructors"][instructor_id]["name"]
    print(f"Курс '{title}' створено, викладач: {instructor_name}")
    return True


def enroll_student(student_id, course_id):
    """Зараховує студента на курс"""
    if student_id not in education_system["students"]:
        print("Студент не знайдений")
        return False
    if course_id not in education_system["courses"]:
        print("Курс не знайдений")
        return False
    course = education_system["courses"][course_id]
    student = education_system["students"][student_id]
    if len(course["enrolled_students"]) >= course["max_students"]:
        print("Курс переповнений")
        return False
    if student_id in course["enrolled_students"]:
        print("Студент вже зарахований на цей курс")
        return False
    course["enrolled_students"].append(student_id)
    student["enrolled_courses"].append(course_id)
    enrollment_id = f"{student_id}_{course_id}"
    education_system["enrollments"][enrollment_id] = {
        "student_id": student_id,
        "course_id": course_id,
        "enrollment_date": "2024-01-15",
        "status": "active",
    }
    print(f"Студент {student['name']} зарахований на курс '{course['title']}'")
    return True


def create_assignment(
    assignment_id, course_id, title, description, max_points, due_date
):
    """Створює завдання для курсу"""
    if course_id not in education_system["courses"]:
        print("Курс не знайдений")
        return False
    education_system["assignments"][assignment_id] = {
        "course_id": course_id,
        "title": title,
        "description": description,
        "max_points": max_points,
        "due_date": due_date,
        "submissions": {},
    }
    education_system["courses"][course_id]["assignments"].append(assignment_id)
    course_title = education_system["courses"][course_id]["title"]
    print(f"Завдання '{title}' створено для курсу '{course_title}'")
    return True


def submit_grade(student_id, assignment_id, points_earned, feedback=""):
    """Виставляє оцінку за завдання"""
    if student_id not in education_system["students"]:
        print("Студент не знайдений")
        return False
    if assignment_id not in education_system["assignments"]:
        print("Завдання не знайдене")
        return False
    assignment = education_system["assignments"][assignment_id]
    course_id = assignment["course_id"]
    if student_id not in education_system["courses"][course_id]["enrolled_students"]:
        print("Студент не зарахований на цей курс")
        return False
    if points_earned > assignment["max_points"]:
        print("Оцінка перевищує максимальну кількість балів")
        return False
    grade_entry = {
        "student_id": student_id,
        "assignment_id": assignment_id,
        "course_id": course_id,
        "points_earned": float(points_earned),
        "max_points": assignment["max_points"],
        "percentage": (points_earned / assignment["max_points"]) * 100,
        "feedback": feedback,
        "date_graded": "2024-01-20",
    }
    education_system["grades"].append(grade_entry)
    assignment["submissions"][student_id] = {
        "points_earned": points_earned,
        "feedback": feedback,
        "date_submitted": "2024-01-19",
    }
    student_name = education_system["students"][student_id]["name"]
    assignment_title = assignment["title"]
    print(
        f"Оцінка {points_earned}/{assignment['max_points']} виставлена студенту {student_name} за '{assignment_title}'"
    )
    return True


def calculate_student_gpa(student_id):
    """Розраховує GPA студента"""
    if student_id not in education_system["students"]:
        return None
    student_grades = [
        grade
        for grade in education_system["grades"]
        if grade["student_id"] == student_id
    ]
    if not student_grades:
        return 0.0
    course_grades = {}
    for grade in student_grades:
        course_id = grade["course_id"]
        if course_id not in course_grades:
            course_grades[course_id] = []
        course_grades[course_id].append(grade["percentage"])
    total_grade_points = 0
    total_credits = 0
    for course_id, grades in course_grades.items():
        course_average = sum(grades) / len(grades)
        course_credits = education_system["courses"][course_id]["credits"]
        if course_average >= 90:
            grade_point = 4.0
        elif course_average >= 80:
            grade_point = 3.0
        elif course_average >= 70:
            grade_point = 2.0
        elif course_average >= 60:
            grade_point = 1.0
        else:
            grade_point = 0.0
        total_grade_points += grade_point * course_credits
        total_credits += course_credits
    gpa = total_grade_points / total_credits if total_credits > 0 else 0.0
    education_system["students"][student_id]["gpa"] = round(gpa, 2)
    education_system["students"][student_id]["total_credits"] = total_credits
    return round(gpa, 2)


def get_course_statistics(course_id):
    """Отримує статистику по курсу"""
    if course_id not in education_system["courses"]:
        return None
    course = education_system["courses"][course_id]
    course_grades = [
        grade for grade in education_system["grades"] if grade["course_id"] == course_id
    ]
    if not course_grades:
        return {
            "course_title": course["title"],
            "enrolled_students": len(course["enrolled_students"]),
            "assignments_count": len(course["assignments"]),
            "average_grade": 0,
            "grade_distribution": {},
            "completion_rate": 0,
        }
    total_percentage = sum(grade["percentage"] for grade in course_grades)
    average_grade = total_percentage / len(course_grades)
    grade_distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for grade in course_grades:
        percentage = grade["percentage"]
        if percentage >= 90:
            grade_distribution["A"] += 1
        elif percentage >= 80:
            grade_distribution["B"] += 1
        elif percentage >= 70:
            grade_distribution["C"] += 1
        elif percentage >= 60:
            grade_distribution["D"] += 1
        else:
            grade_distribution["F"] += 1
    total_assignments = len(course["assignments"])
    total_possible_submissions = len(course["enrolled_students"]) * total_assignments
    actual_submissions = len(course_grades)
    completion_rate = (
        (actual_submissions / total_possible_submissions) * 100
        if total_possible_submissions > 0
        else 0
    )
    return {
        "course_title": course["title"],
        "instructor": education_system["instructors"][course["instructor_id"]]["name"],
        "enrolled_students": len(course["enrolled_students"]),
        "assignments_count": total_assignments,
        "average_grade": round(average_grade, 2),
        "grade_distribution": grade_distribution,
        "completion_rate": round(completion_rate, 2),
    }


def generate_student_transcript(student_id):
    """Генерує академічну довідку студента"""
    if student_id not in education_system["students"]:
        return None
    student = education_system["students"][student_id]
    student_courses = []
    for course_id in student["enrolled_courses"]:
        course = education_system["courses"][course_id]
        course_grades = [
            grade
            for grade in education_system["grades"]
            if grade["student_id"] == student_id and grade["course_id"] == course_id
        ]
        if course_grades:
            course_average = sum(grade["percentage"] for grade in course_grades) / len(
                course_grades
            )
            if course_average >= 90:
                letter_grade = "A"
            elif course_average >= 80:
                letter_grade = "B"
            elif course_average >= 70:
                letter_grade = "C"
            elif course_average >= 60:
                letter_grade = "D"
            else:
                letter_grade = "F"
        else:
            course_average = 0
            letter_grade = "N/A"
        student_courses.append(
            {
                "course_title": course["title"],
                "credits": course["credits"],
                "grade_percentage": round(course_average, 1),
                "letter_grade": letter_grade,
                "instructor": education_system["instructors"][course["instructor_id"]][
                    "name"
                ],
            }
        )
    gpa = calculate_student_gpa(student_id)
    return {
        "student_name": student["name"],
        "major": student["major"],
        "year_of_study": student["year_of_study"],
        "gpa": gpa,
        "total_credits": student["total_credits"],
        "courses": student_courses,
    }


def find_at_risk_students(min_grade_threshold=60):
    """Знаходить студентів з ризиком академічної неуспішності"""
    at_risk_students = []
    for student_id, student in education_system["students"].items():
        student_grades = [
            grade
            for grade in education_system["grades"]
            if grade["student_id"] == student_id
        ]
        if student_grades:
            average_grade = sum(grade["percentage"] for grade in student_grades) / len(
                student_grades
            )
            total_assignments = 0
            completed_assignments = len(student_grades)
            for course_id in student["enrolled_courses"]:
                total_assignments += len(
                    education_system["courses"][course_id]["assignments"]
                )
            completion_rate = (
                (completed_assignments / total_assignments) * 100
                if total_assignments > 0
                else 0
            )
            if average_grade < min_grade_threshold or completion_rate < 70:
                risk_factors = []
                if average_grade < min_grade_threshold:
                    risk_factors.append(f"низька середня оцінка ({average_grade:.1f}%)")
                if completion_rate < 70:
                    risk_factors.append(
                        f"низький рівень виконання завдань ({completion_rate:.1f}%)"
                    )
                at_risk_students.append(
                    {
                        "student_name": student["name"],
                        "student_id": student_id,
                        "major": student["major"],
                        "average_grade": round(average_grade, 1),
                        "completion_rate": round(completion_rate, 1),
                        "risk_factors": risk_factors,
                    }
                )
    return sorted(at_risk_students, key=lambda x: x["average_grade"])


# Приклад використання
add_instructor(
    "INST001",
    "Др. Іван Петренко",
    "petrov@uni.edu",
    "Комп'ютерні науки",
    "Програмування",
)
add_instructor(
    "INST002", "Др. Марія Коваленко", "maria@uni.edu", "Математика", "Алгебра"
)
add_instructor(
    "INST003", "Др. Олег Шевченко", "oleg@uni.edu", "Фізика", "Квантова механіка"
)

add_student("STU001", "Анна Іваненко", "anna@student.edu", "Комп'ютерні науки", 2)
add_student("STU002", "Микола Сидоров", "mykola@student.edu", "Математика", 1)
add_student("STU003", "Олеся Петрова", "olesya@student.edu", "Фізика", 3)
add_student("STU004", "Дмитро Коваль", "dmytro@student.edu", "Комп'ютерні науки", 2)

create_course(
    "CS101",
    "Основи програмування",
    "Вступний курс з програмування на Python",
    4,
    "INST001",
)
create_course(
    "MATH201",
    "Лінійна алгебра",
    "Векторні простори та лінійні перетворення",
    3,
    "INST002",
)
create_course("PHYS301", "Квантова фізика", "Основи квантової механіки", 4, "INST003")

enroll_student("STU001", "CS101")
enroll_student("STU002", "CS101")
enroll_student("STU003", "CS101")
enroll_student("STU004", "CS101")
enroll_student("STU001", "MATH201")
enroll_student("STU003", "PHYS301")

create_assignment(
    "ASG001", "CS101", "Лабораторна робота 1", "Основи Python", 100, "2024-02-01"
)
create_assignment("ASG002", "CS101", "Проект", "Фінальний проект", 200, "2024-02-15")
create_assignment(
    "ASG003", "MATH201", "Контрольна робота 1", "Векторні операції", 100, "2024-02-10"
)

submit_grade("STU001", "ASG001", 85, "Відмінна робота!")
submit_grade("STU002", "ASG001", 72, "Добре, але потрібно покращити коментарі")
submit_grade("STU003", "ASG001", 95, "Ідеальне виконання")
submit_grade("STU004", "ASG001", 58, "Потрібно доопрацювати")
submit_grade("STU001", "ASG002", 180, "Креативний підхід")
submit_grade("STU002", "ASG002", 145, "Функціонально, але можна краще")
submit_grade("STU003", "ASG002", 190, "Відмінний результат")
submit_grade("STU001", "ASG003", 88, "Добре розуміння матеріалу")

print("=== СТАТИСТИКА КУРСУ ===")
course_stats = get_course_statistics("CS101")
if course_stats:
    print(f"Курс: {course_stats['course_title']}")
    print(f"Викладач: {course_stats['instructor']}")
    print(f"Зараховано студентів: {course_stats['enrolled_students']}")
    print(f"Кількість завдань: {course_stats['assignments_count']}")
    print(f"Середня оцінка: {course_stats['average_grade']}%")
    print(f"Рівень виконання: {course_stats['completion_rate']}%")
    print("Розподіл оцінок:")
    for grade, count in course_stats["grade_distribution"].items():
        print(f" {grade}: {count} студентів")

print("\n=== АКАДЕМІЧНА ДОВІДКА ===")
transcript = generate_student_transcript("STU001")
if transcript:
    print(f"Студент: {transcript['student_name']}")
    print(f"Спеціальність: {transcript['major']}")
    print(f"Рік навчання: {transcript['year_of_study']}")
    print(f"GPA: {transcript['gpa']}")
    print(f"Загальна кількість кредитів: {transcript['total_credits']}")
    print("Курси:")
    for course in transcript["courses"]:
        print(
            f" {course['course_title']}: {course['letter_grade']} ({course['grade_percentage']}%), {course['credits']} кредитів"
        )

print("\n=== СТУДЕНТИ В ЗОНІ РИЗИКУ ===")
at_risk = find_at_risk_students()
if at_risk:
    for student in at_risk:
        print(
            f"{student['student_name']} ({student['major']}): середня {student['average_grade']}%, виконання {student['completion_rate']}%"
        )
        print(f" Фактори ризику: {', '.join(student['risk_factors'])}")
else:
    print("Немає студентів в зоні ризику")

print("\n=== GPA СТУДЕНТІВ ===")
for student_id, student in education_system["students"].items():
    gpa = calculate_student_gpa(student_id)
    print(f"{student['name']}: GPA {gpa}")
