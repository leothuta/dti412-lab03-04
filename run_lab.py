# run_lab.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "training_system.settings")
django.setup()

import django.db
from django.db.models import F, Q
from core.models import Course, Department, Employee, TrainingRecord

print("--- 1. Seeding Data ---")
hr, _ = Department.objects.get_or_create(code="HR", defaults={"name": "Human Resources"})
it, _ = Department.objects.get_or_create(code="IT", defaults={"name": "Information Technology"})
fin, _ = Department.objects.get_or_create(code="FIN", defaults={"name": "Finance"})

e1, _ = Employee.objects.get_or_create(
    employee_code="EMP001",
    defaults={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "salary": 65000.00,
        "department": it,
    },
)
e2, _ = Employee.objects.get_or_create(
    employee_code="EMP002",
    defaults={
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "salary": 75000.00,
        "department": it,
    },
)
e3, _ = Employee.objects.get_or_create(
    employee_code="EMP003",
    defaults={
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice@example.com",
        "salary": 55000.00,
        "department": hr,
    },
)
e4, _ = Employee.objects.get_or_create(
    employee_code="EMP004",
    defaults={
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bob@example.com",
        "salary": 60000.00,
        "department": fin,
    },
)

c1, _ = Course.objects.get_or_create(
    code="SEC101",
    defaults={"title": "Cybersecurity Essentials", "capacity": 25},
)
c2, _ = Course.objects.get_or_create(
    code="DEV201",
    defaults={"title": "Advanced Django ORM", "capacity": 30},
)

TrainingRecord.objects.get_or_create(
    employee=e1, course=c1, defaults={"completion_status": "COMPLETED", "score": 88.50}
)
TrainingRecord.objects.get_or_create(
    employee=e1, course=c2, defaults={"completion_status": "IN_PROGRESS"}
)
TrainingRecord.objects.get_or_create(
    employee=e2, course=c2, defaults={"completion_status": "COMPLETED", "score": 95.00}
)
TrainingRecord.objects.get_or_create(
    employee=e3, course=c1, defaults={"completion_status": "REGISTERED"}
)
print("Seed complete.")

print("\n--- 2. Task 4.1: Q Objects ---")
query_or = Employee.objects.filter(Q(department__code="IT") | Q(salary__gt=70000))
print("OR Query Results:", list(query_or))

query_not = Employee.objects.filter(Q(first_name__icontains="John") & ~Q(department__code="HR"))
print("AND NOT Query Results:", list(query_not))

print("\n--- 3. Task 4.2: F() Expressions ---")
Employee.objects.filter(department__code="IT").update(salary=F("salary") * 1.10)
for emp in Employee.objects.filter(department__code="IT"):
    print(f"{emp.first_name} New Salary: {emp.salary}")

print("\n--- 4. Task 4.3: N+1 vs select_related() ---")
django.db.reset_queries()
for emp in Employee.objects.all():
    print(f"Employee: {emp.first_name}, Department: {emp.department.name}")
print("Total Queries (Unoptimized):", len(django.db.connection.queries))

django.db.reset_queries()
for emp in Employee.objects.select_related("department").all():
    print(f"Employee: {emp.first_name}, Department: {emp.department.name}")
print("Total Queries (select_related):", len(django.db.connection.queries))

print("\n--- 5. Task 4.4: prefetch_related() ---")
django.db.reset_queries()
for course in Course.objects.prefetch_related("attendees").all():
    attendee_names = [emp.first_name for emp in course.attendees.all()]
    print(f"Course: {course.code}, Attendees: {', '.join(attendee_names)}")
print("Total Queries (prefetch_related):", len(django.db.connection.queries))