from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser, Courses, Staffs, Subjects, Students
from django.contrib import messages
import datetime
from django.core.files.storage import FileSystemStorage


def adminHome(request):
    return render(request, 'hod_template/home_content.html')


def add_staff(request):
    return render(request, 'hod_template/add_staff_template.html')


def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, 'Staff addedd successfully')
            return HttpResponseRedirect('/add_staff')
        except:
            messages.error(request, "Failed to add staff")
            return HttpResponse("Something went wrong")


def add_course(request):
    return render(request, 'hod_template/add_course_template.html')


def add_course_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        course_name = request.POST.get('course')
        try:
            course = Courses(course_name=course_name)
            course.save()
            messages.success(request, "Course added successfully")
            return HttpResponseRedirect('/add_course')
        except:
            messages.error(request, "Failed to add course")
            return HttpResponseRedirect('/add_course')


def add_student(request):
    courses = Courses.objects.all()
    return render(request, 'hod_template/add_student_template.html', {"courses": courses})


def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        course_id = request.POST.get('course')
        sex = request.POST.get('sex')
        profile_image = request.FILES['profile_image']
        fs = FileSystemStorage()
        filename = fs.save(profile_image.name, profile_image)
        profile_image_url = fs.url(filename)
        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=3)
            user.students.address = address
            course_object = Courses.objects.get(id=course_id)
            user.students.course = course_object
            user.students.session_start_year = session_start
            user.students.session_end_year = session_end
            user.students.gender = sex
            user.students.profile_pic = profile_image_url
            user.save()
            messages.success(request, "Student added successfully")
            return HttpResponseRedirect('/add_student')
        except:
            messages.error(request, "Failed to add student")
            return HttpResponseRedirect('/add_student')


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/add_subject_template.html", {"staffs": staffs, "courses": courses})


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subjects(subjects_name=subject_name,
                               course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, 'Subject added successfully')
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request, "Failed to add subject")
            return HttpResponseRedirect("/add_subject")


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, 'hod_template/manage_staff_template.html', {"staffs": staffs})


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, 'hod_template/edit_staff_template.html', {"staff": staff})


def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        new_username = request.POST.get('username')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_email = request.POST.get('email')
        new_address = request.POST.get('address')
        staff_id = request.POST.get('staff_id')
        try:
            user = CustomUser.objects.get(id=staff_id)
            old_username = user.username
            old_first_name = user.first_name
            old_last_name = user.last_name
            old_email = user.email
            staff = Staffs.objects.get(admin=staff_id)
            old_address = staff.address

            if new_username == "":
                user.username = old_username
            else:
                user.username = new_username
            if new_first_name == "":
                user.first_name = old_first_name
            else:
                user.first_name = new_first_name
            if new_last_name == "":
                user.last_name = old_last_name
            else:
                user.last_name = new_last_name
            if new_email == "":
                user.email = old_email
            else:
                user.email = new_email
            if new_address == "":
                staff.address = old_address
            else:
                staff.address = new_address
            user.save()
            staff.save()
            messages.success(request, "Updated successfully")
            return HttpResponseRedirect(f'/edit_staff/{staff_id}')
        except:
            messages.error(request, "Error updating staff")
            return HttpResponseRedirect(f'/edit_staff/{staff_id}')


def manage_student(request):
    students = Students.objects.all()
    return render(request, 'hod_template/manage_student_template.html', {"students": students})


def edit_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    courses = Courses.objects.all()
    return render(request, "hod_template/edit_student_template.html", {"student": student, "courses": courses})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        address = request.POST.get('address')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        gender = request.POST.get('sex')
        course_id = request.POST.get('course')
        if request.FILES.get('profile_image', False):
            profile_image = request.FILES['profile_image']
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            profile_image_url = fs.url(filename)
        else:
            profile_image_url = None

        try:
            user = CustomUser.objects.get(id=student_id)
            student = Students.objects.get(admin=student_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            course = Courses.objects.get(id=course_id)
            student.gender = gender
            student.address = address
            student.course = course
            student.session_start_year = session_start
            student.session_end_year = session_end
            if profile_image_url != None:
                student.profile_pic = profile_image_url
            user.save()
            student.save()
            messages.success(request, "Updated successfully")
            return HttpResponseRedirect(f'/edit_student/{student_id}')
        except:
            messages.error(request, "Failed to update")
            return HttpResponseRedirect(f'/edit_student/{student_id}')


def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'hod_template/manage_course_template.html', {"courses": courses})


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, 'hod_template/edit_course_template.html', {"course": course})


def edit_course_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", 404)
    else:
        course_name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')
        print(course_id)
        print(course_name)
        # try:
        course = Courses.objects.get(id=course_id)
        course.course_name = course_name
        course.save()
        messages.success(request, "Updated successfully")
        return HttpResponseRedirect(f'/edit_course/{course_id}')
        # except:
        #     messages.error(request, "Failed to update")
        #     return HttpResponseRedirect(f'/edit_course/{course_id}')


def manage_subject(request):
    subjects = Subjects.objects.all()
    # for subject in subjects:
    #     print(subject.subjects_name)
    return render(request, 'hod_template/manage_subject_template.html', {"subjects": subjects})


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = Staffs.objects.all()
    # print(staffs.admin.first_name)
    # for staff in staffs:
    #     print(staff.admin.first_name)
    return render(request, 'hod_template/edit_subject_template.html', {"subject": subject, "courses": courses, "staffs": staffs})


def edit_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", 404)
    else:
        subject_id = request.POST.get('subject_id')
        subjects_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')
        print(subject_id, subjects_name, course_id, staff_id)

        try:
            subject = Subjects.objects.get(id=subject_id)
            print(subject.id)
            subject.subjects_name = subjects_name
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            subject.save()
            messages.success(request, "Updated successfully")
            return HttpResponseRedirect(f'/edit_subject/{subject_id}')
        except:
            messages.error(request, 'Failed to update subject')
            return HttpResponseRedirect(f'/edit_subject/{subject_id}')
