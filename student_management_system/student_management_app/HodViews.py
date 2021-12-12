from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import CustomUser, Courses, Staffs, Subjects, Students, SessionYearModel, FeedbackStudent, FeedbackStaffs, LeaveReportStudent, LeaveReportStaffs, Attendance, AttendanceReport
from django.contrib import messages
import datetime
from django.core.files.storage import FileSystemStorage
from .forms import AddStudentForm, EditStudentForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json


def adminHome(request):
    all_student_count = Students.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    staff_count = Staffs.objects.all().count()

    # Total Subjects and students in Each Course
    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []

    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subjects_name)
        student_count_list_in_subject.append(student_count)

    # For Saffs
    staff_attendance_present_list = []
    staff_attendance_leave_list = []
    staff_name_list = []

    staffs = Staffs.objects.all()
    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(
            subject_id__in=subject_ids).count()
        leaves = LeaveReportStaffs.objects.filter(
            staff_if=staff.id, leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)

    # For Students
    student_attendance_present_list = []
    student_attendance_leave_list = []
    student_name_list = []

    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(
            student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(
            student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(
            student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)

    context = {
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "course_count": course_count,
        "staff_count": staff_count,
        "course_name_list": course_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_course": student_count_list_in_course,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
    }
    return render(request, "hod_template/home_content.html", context)


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
            return HttpResponseRedirect(reverse('add_staff'))
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
            return HttpResponseRedirect(reverse('add_course'))
        except:
            messages.error(request, "Failed to add course")
            return HttpResponseRedirect(reverse('add_course'))


def add_student(request):
    # courses = Courses.objects.all()
    form = AddStudentForm()
    return render(request, 'hod_template/add_student_template.html', {"form": form})


def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_id = form.cleaned_data['session_year_id']
            # session_end = form.cleaned_data['session_end']
            course_id = form.cleaned_data['course']
            sex = form.cleaned_data['sex']
            profile_image = request.FILES['profile_image']
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            profile_image_url = fs.url(filename)
            # try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=3)
            user.students.address = address
            course_object = Courses.objects.get(id=course_id)
            user.students.course = course_object
            session = SessionYearModel.objects.get(id=session_id)
            user.students.session_year_id = session
            # user.students.session_end_year = session_end
            user.students.gender = sex
            user.students.profile_pic = profile_image_url
            user.save()
            messages.success(request, "Student added successfully")
            return HttpResponseRedirect(reverse('add_student'))
            # except:
            #     messages.error(request, "Failed to add student")
            #     return HttpResponseRedirect(reverse('add_student'))
        else:
            form = AddStudentForm(request.POST)
            # course = Courses.objects.all()
            return render(request, 'hod_template/add_student_template.html', {"form": form})


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
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to add subject")
            return HttpResponseRedirect(reverse("add_subject"))


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
            return HttpResponseRedirect(reverse('edit_staff', kwargs={"staff_id": staff_id}))
        except:
            messages.error(request, "Error updating staff")
            return HttpResponseRedirect(reverse('edit_staff', kwargs={"staff_id": staff_id}))


def manage_student(request):
    students = Students.objects.all()
    return render(request, 'hod_template/manage_student_template.html', {"students": students})


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    courses = Courses.objects.all()
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course.id
    form.fields['sex'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id
    return render(request, "hod_template/edit_student_template.html", {"id": student_id, "form": form, "first_name": student.admin.first_name, "last_name": student.admin.last_name})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            # messages.error(request, "Failed to update")
            return HttpResponseRedirect(reverse('edit_student', kwargs={"student_id": student_id}))
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            session_id = form.cleaned_data['session_year_id']
            gender = form.cleaned_data['sex']
            course_id = form.cleaned_data['course']
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
                session = SessionYearModel.objects.get(id=session_id)
                student.session_year_id = session
                if profile_image_url != None:
                    student.profile_pic = profile_image_url
                user.save()
                student.save()
                del request.session['student_id']
                messages.success(request, "Updated successfully")
                return HttpResponseRedirect(reverse('edit_student', kwargs={"student_id": student_id}))
            except:
                messages.error(request, "Failed to update")
                return HttpResponseRedirect(reverse('edit_student', kwargs={"student_id": student_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Students.object.get(admin=student_id)
            return render(request, "hod_template/edit_student_template.html", {"id": student_id, "form": form, "first_name": student.admin.first_name, "last_name": student.admin.last_name})


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
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Updated successfully")
            return HttpResponseRedirect(reverse('edit_course', kwargs={"course_id": course_id}))
        except:
            messages.error(request, "Failed to update")
            return HttpResponseRedirect(reverse('edit_course', kwargs={"course_id": course_id}))


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
            staff_temp = Staffs.objects.get(id=staff_id)
            print(staff_temp.admin_id)
            staff = CustomUser.objects.get(id=staff_temp.admin_id)
            subject.staff_id = staff
            subject.save()
            messages.success(request, "Updated successfully")
            return HttpResponseRedirect(reverse('edit_subject', kwargs={"subject_id": subject_id}))
        except:
            messages.error(request, 'Failed to update subject')
            return HttpResponseRedirect(reverse('edit_subject', kwargs={"subject_id": subject_id}))


def manage_session(request):
    return render(request, "hod_template/manage_session_template.html")


def add_session_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('manage_session'))
    else:
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        try:

            session = SessionYearModel(
                session_start_year=session_start, session_end_year=session_end)
            session.save()
            messages.success(request, "Successfully added session")
            return HttpResponseRedirect(reverse('manage_session'))
        except:
            messages.error(request, "Failed to add session")
            return HttpResponseRedirect(reverse('manage_session'))


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_message(request):
    feedbacks = FeedbackStudent.objects.all()
    return render(request, 'hod_template/student_feedback_template.html', {"feedbacks": feedbacks})


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedbackStaffs.objects.all()
    return render(request, 'hod_template/staff_feedback_template.html', {"feedbacks": feedbacks})


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedbackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)


def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportStaffs.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaffs.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaffs.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(
        subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small = {"id": attendance_single.id, "attendance_date": str(
            attendance_single.attendance_date), "session_year_id": attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id, "name": student.student_id.admin.first_name +
                      " "+student.student_id.admin.last_name, "status": student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
