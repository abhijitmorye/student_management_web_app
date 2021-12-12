from django.shortcuts import render
from .models import Subjects, Students, Courses, CustomUser, Attendance, AttendanceReport, LeaveReportStudent, FeedbackStudent
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.urls import reverse
from django.contrib import messages


def student_home(request):
    return render(request, 'student_template/student_home_template.html')


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    course = student.course.id
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, 'student_template/student_view_attendance.html', {"subjects": subjects})


def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    start_date_parse = datetime.datetime.strptime(
        start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.datetime.strptime(
        end_date, '%Y-%m-%d').date()
    print(start_date_parse, end_date_parse)
    subject_obj = Subjects.objects.get(id=subject_id)
    user_object = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user_object)

    attendance = Attendance.objects.filter(
        attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(
        attendance_id__in=attendance, student_id=student)

    # for attendance_report in attendance_reports:
    #     print(f"Date: {attendance_report.attendance_id.attendance_date}")
    #     print(f"Status: {attendance_report.status}")
    return render(request, 'student_template/student_attendance_data.html', {"attendance_reports": attendance_reports})


def student_apply_leave(request):
    student = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student)
    return render(request, 'student_template/student_apply_leave.html', {"leave_data": leave_data})


def apply_student_leave_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_reason = request.POST.get("leave_reason")
        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave = LeaveReportStudent(
                student_id=student_obj, leave_date=leave_date, leave_message=leave_reason, leave_status=0)
            leave.save()
            messages.success(request, "Leave applied successfully")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Error while applying for leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    student = Students.objects.get(admin=request.user.id)
    feedback_data = FeedbackStudent.objects.filter(student_id=student)
    return render(request, 'student_template/student_feedback.html', {"feedback_data": feedback_data})


def student_feedback_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        student_id = request.user.id
        student = Students.objects.get(admin=student_id)
        feedback = request.POST.get("feedback")
        try:
            feedabckStudent = FeedbackStudent(
                student_id=student, feedback=feedback)
            feedabckStudent.save()
            messages.success(request, "Feedback sent succesfully")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Error while sending feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context = {
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()

            messages.success(request, "Profile Updated Successfully")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))
