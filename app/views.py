
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from reportlab.pdfgen import canvas

from .models import Attendance, Faculty, Fees, Result, Student, Timetable


def _clean_value(request, key):
    return (request.POST.get(key) or '').strip()


def _require_fields(request, required_fields):
    missing = [label for label, value in required_fields.items() if not value]

    if missing:
        messages.error(request, f"{', '.join(missing)} cannot be empty.")
        return False

    return True


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = _clean_value(request, 'username')
        email = _clean_value(request, 'email')
        password = _clean_value(request, 'password')

        if not _require_fields(
            request,
            {
                'Username': username,
                'Email': email,
                'Password': password,
            },
        ):
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        messages.success(request, 'Account created successfully.')
        return redirect('login')

    return render(request, 'register.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = _clean_value(request, 'username')
        password = _clean_value(request, 'password')

        if not _require_fields(
            request,
            {
                'Username': username,
                'Password': password,
            },
        ):
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard(request):
    total_students = Student.objects.count()
    total_faculty = Faculty.objects.count()
    total_results = Result.objects.count()
    total_fees = Fees.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_results': total_results,
        'total_fees': total_fees,
        'recent_students': Student.objects.order_by('-id')[:5],
    }

    return render(request, 'dashboard.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def students(request):
    query = (request.GET.get('search') or '').strip()
    data = Student.objects.all().order_by('-id')

    if query:
        data = Student.objects.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(roll__icontains=query)
            | Q(department__icontains=query)
        ).order_by('-id')

    return render(request, 'students.html', {'data': data})


@login_required(login_url='login')
def add_student(request):
    if request.method == 'POST':
        name = _clean_value(request, 'name')
        email = _clean_value(request, 'email')
        roll = _clean_value(request, 'roll')
        department = _clean_value(request, 'department')
        semester = _clean_value(request, 'semester')

        if not _require_fields(
            request,
            {
                'Student name': name,
                'Email': email,
                'Roll number': roll,
                'Department': department,
                'Semester': semester,
            },
        ):
            return redirect('add_student')

        if not semester.isdigit():
            messages.error(request, 'Semester must be a valid number.')
            return redirect('add_student')

        Student.objects.create(
            name=name,
            email=email,
            roll=roll,
            department=department,
            semester=int(semester),
        )

        messages.success(request, 'Student added successfully.')
        return redirect('students')

    return render(request, 'add_student.html')


@login_required(login_url='login')
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        name = _clean_value(request, 'name')
        email = _clean_value(request, 'email')
        roll = _clean_value(request, 'roll')
        department = _clean_value(request, 'department')
        semester = _clean_value(request, 'semester')

        if not _require_fields(
            request,
            {
                'Student name': name,
                'Email': email,
                'Roll number': roll,
                'Department': department,
                'Semester': semester,
            },
        ):
            return redirect('edit_student', id=id)

        if not semester.isdigit():
            messages.error(request, 'Semester must be a valid number.')
            return redirect('edit_student', id=id)

        student.name = name
        student.email = email
        student.roll = roll
        student.department = department
        student.semester = int(semester)
        student.save()

        messages.success(request, 'Student updated successfully.')
        return redirect('students')

    return render(request, 'edit_student.html', {'student': student})


@login_required(login_url='login')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('students')


@login_required(login_url='login')
def attendance(request):
    students = Student.objects.all().order_by('name')
    return render(request, 'attendance.html', {'students': students})


@login_required(login_url='login')
def mark_attendance(request, id):
    student = get_object_or_404(Student, id=id)
    Attendance.objects.create(student=student, status='Present')
    messages.success(request, f'{student.name} marked present.')
    return redirect('attendance')


@login_required(login_url='login')
def mark_absent(request, id):
    student = get_object_or_404(Student, id=id)
    Attendance.objects.create(student=student, status='Absent')
    messages.success(request, f'{student.name} marked absent.')
    return redirect('attendance')


@login_required(login_url='login')
def attendance_history(request):
    data = Attendance.objects.select_related('student').all().order_by('-id')
    return render(request, 'attendance_history.html', {'data': data})


@login_required(login_url='login')
def results(request):
    data = Result.objects.select_related('student').all().order_by('-id')
    return render(request, 'results.html', {'data': data})


@login_required(login_url='login')
def add_result(request):
    students = Student.objects.all().order_by('name')

    if request.method == 'POST':
        student_id = _clean_value(request, 'student')
        subject = _clean_value(request, 'subject')
        marks = _clean_value(request, 'marks')
        cgpa = _clean_value(request, 'cgpa')

        if not _require_fields(
            request,
            {
                'Student': student_id,
                'Subject': subject,
                'Marks': marks,
                'CGPA': cgpa,
            },
        ):
            return redirect('add_result')

        if not marks.isdigit():
            messages.error(request, 'Marks must be a valid number.')
            return redirect('add_result')

        try:
            cgpa_value = float(cgpa)
        except ValueError:
            messages.error(request, 'CGPA must be a valid decimal number.')
            return redirect('add_result')

        student = get_object_or_404(Student, id=student_id)
        Result.objects.create(
            student=student,
            subject=subject,
            marks=int(marks),
            cgpa=cgpa_value,
        )

        messages.success(request, 'Result added successfully.')
        return redirect('results')

    return render(request, 'add_result.html', {'students': students})


@login_required(login_url='login')
def fees(request):
    data = Fees.objects.select_related('student').all().order_by('-id')
    return render(request, 'fees.html', {'data': data})


@login_required(login_url='login')
def add_fees(request):
    students = Student.objects.all().order_by('name')

    if request.method == 'POST':
        student_id = _clean_value(request, 'student')
        amount = _clean_value(request, 'amount')
        status = _clean_value(request, 'status')

        if not _require_fields(
            request,
            {
                'Student': student_id,
                'Amount': amount,
                'Status': status,
            },
        ):
            return redirect('add_fees')

        if not amount.isdigit():
            messages.error(request, 'Amount must be a valid number.')
            return redirect('add_fees')

        student = get_object_or_404(Student, id=student_id)
        Fees.objects.create(student=student, amount=int(amount), status=status)

        messages.success(request, 'Fees record added successfully.')
        return redirect('fees')

    return render(request, 'add_fees.html', {'students': students})


@login_required(login_url='login')
def download_result(request, id):
    result = get_object_or_404(Result.objects.select_related('student'), id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="marksheet.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setFont('Helvetica-Bold', 22)
    pdf.drawString(180, 800, 'University Marksheet')

    pdf.setFont('Helvetica', 14)
    pdf.drawString(100, 730, f'Student : {result.student.name}')
    pdf.drawString(100, 700, f'Subject : {result.subject}')
    pdf.drawString(100, 670, f'Marks : {result.marks}')
    pdf.drawString(100, 640, f'CGPA : {result.cgpa}')
    pdf.drawString(100, 600, 'Status : PASS')

    pdf.save()
    return response


@login_required(login_url='login')
def faculty(request):
    data = Faculty.objects.all().order_by('-id')
    return render(request, 'faculty.html', {'data': data})


@login_required(login_url='login')
def add_faculty(request):
    if request.method == 'POST':
        name = _clean_value(request, 'name')
        email = _clean_value(request, 'email')
        department = _clean_value(request, 'department')
        subject = _clean_value(request, 'subject')

        if not _require_fields(
            request,
            {
                'Faculty name': name,
                'Email': email,
                'Department': department,
                'Subject': subject,
            },
        ):
            return redirect('add_faculty')

        Faculty.objects.create(
            name=name,
            email=email,
            department=department,
            subject=subject,
        )

        messages.success(request, 'Faculty added successfully.')
        return redirect('faculty')

    return render(request, 'add_faculty.html')


@login_required(login_url='login')
def student_profile(request, id):
    student = get_object_or_404(Student, id=id)
    attendance = Attendance.objects.filter(student=student).count()
    results = Result.objects.filter(student=student).order_by('-id')
    fees = Fees.objects.filter(student=student).order_by('-id')

    return render(
        request,
        'student_profile.html',
        {
            'student': student,
            'attendance': attendance,
            'results': results,
            'fees': fees,
        },
    )


@login_required(login_url='login')
def timetable(request):
    data = Timetable.objects.all().order_by('day', 'time')
    return render(request, 'timetable.html', {'data': data})


@login_required(login_url='login')
def add_timetable(request):
    if request.method == 'POST':
        day = _clean_value(request, 'day')
        subject = _clean_value(request, 'subject')
        faculty = _clean_value(request, 'faculty')
        time = _clean_value(request, 'time')

        if not _require_fields(
            request,
            {
                'Day': day,
                'Subject': subject,
                'Faculty': faculty,
                'Time': time,
            },
        ):
            return redirect('add_timetable')

        Timetable.objects.create(
            day=day,
            subject=subject,
            faculty=faculty,
            time=time,
        )

        messages.success(request, 'Timetable entry added successfully.')
        return redirect('timetable')

    return render(request, 'add_timetable.html')


@login_required(login_url='login')
def settings_view(request):
    if request.method == 'POST':
        username = _clean_value(request, 'username')
        email = _clean_value(request, 'email')
        old_password = _clean_value(request, 'old_password')
        new_password = _clean_value(request, 'new_password')
        confirm_password = _clean_value(request, 'confirm_password')

        if not _require_fields(
            request,
            {
                'Username': username,
                'Email': email,
            },
        ):
            return redirect('settings')

        request.user.username = username
        request.user.email = email
        request.user.save()

        if old_password or new_password or confirm_password:
            if not _require_fields(
                request,
                {
                    'Current password': old_password,
                    'New password': new_password,
                    'Confirm password': confirm_password,
                },
            ):
                return redirect('settings')

            if not request.user.check_password(old_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('settings')

            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return redirect('settings')

            if len(new_password) < 8:
                messages.error(request, 'New password must be at least 8 characters long.')
                return redirect('settings')

            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)

        messages.success(request, 'Profile updated successfully.')
        return redirect('settings')

    return render(request, 'settings.html', {'user_profile': request.user})
