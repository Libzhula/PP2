#lambda with sorted

students = [
    ("Alex", 21),
    ("Maria", 19),
    ("John", 23)
]

sorted_students = sorted(students, key=lambda student: student[1])

print("Sorted by age:")
for student in sorted_students:
    print(student)

