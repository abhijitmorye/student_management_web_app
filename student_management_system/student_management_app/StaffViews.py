from django.shortcuts import render
from .models import SessionYearModel, Subjects, Students, Attendance, AttendanceReport, LeaveReportStaffs, Staffs, FeedbackStaffs
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
import json
from django.urls import reverse
from django.contrib import messages


def staff_home(request):
    return render(request, 'staff_template/staff_home_template.html')


def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    return render(request, 'staff_template/attendance_template.html', {"session_years": session_years, "subjects": subjects})


@csrf_exempt
def get_students(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        subject_id = request.POST.get("subject")
        session_id = request.POST.get("session_year")
        print(subject_id, session_id)
        subject = Subjects.objects.get(id=subject_id)
        session = SessionYearModel.objects.get(id=session_id)
        print(subject.course_id)
        students = Students.objects.filter(
            course_id=subject.course_id, session_year_id=session)
        # student_data = serializers.serialize("python", students)
        list_data = []
        for student in students:
            data_small = {
                "id": student.admin.id,
                "name": student.admin.first_name+" "+student.admin.last_name
            }
            list_data.append(data_small)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):
    student_ids = request.POST.get('student_ids')
    subject_id = request.POST.get("subject_ids")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")
    subject = Subjects.objects.get(id=subject_id)
    session_year = SessionYearModel.objects.get(id=session_year_id)
    try:

        attendance = Attendance(
            subject_id=subject, attendance_date=attendance_date, session_year_id=session_year)
        attendance.save()
        print(student_ids)
        dict_students = json.loads(student_ids)
        for stud in dict_students:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(
                student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def staff_update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    # attendance = Attendance.objects.all()
    return render(request, "staff_template/staff_update_attendance.html", {"subjects": subjects, "session_years": session_years})


@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(
        subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id,
                "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id
                }
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def get_attendance_students(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        # subject_id = request.POST.get("subject")
        # session_id = request.POST.get("session_year")
        # print(subject_id, session_id)
        # subject = Subjects.objects.get(id=subject_id)
        # session = SessionYearModel.objects.get(id=session_id)
        attendance_date = request.POST.get("attendance_date")
        attendanc_obj = Attendance.objects.get(id=attendance_date)
        attendance_data = AttendanceReport.objects.filter(
            attendance_id=attendanc_obj)
        # print(subject.course_id)
        # students = Students.objects.filter(
        #     course_id=subject.course_id, session_year_id=session)
        # student_data = serializers.serialize("python", students)
        list_data = []
        for attendance in attendance_data:
            data_small = {
                "id": attendance.student_id.admin.id,
                "name": attendance.student_id.admin.first_name+" "+attendance.student_id.admin.last_name,
                "status": attendance.status
            }
            list_data.append(data_small)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get('student_ids')
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    dict_students = json.loads(student_ids)
    try:
        for stud in dict_students:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(
                student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def staff_apply_leave(request):
    staff = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaffs.objects.filter(staff_if=staff)
    return render(request, 'staff_template/staff_apply_leave.html', {"leave_data": leave_data})


def apply_staff_leave_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_reason = request.POST.get("leave_reason")
        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave = LeaveReportStaffs(
                staff_if=staff_obj, leave_date=leave_date, leave_message=leave_reason, leave_status=0)
            leave.save()
            messages.success(request, "Leave applied successfully")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request, "Error while applying for leave")
            return HttpResponseRedirect(reverse("staff_leave_leave"))


def staff_feedback(request):
    staff = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedbackStaffs.objects.filter(staff_id=staff)
    return render(request, 'staff_template/staff_feedback.html', {"feedback_data": feedback_data})


def staff_feedback_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        staff_id = request.user.id
        staff = Staffs.objects.get(admin=staff_id)
        feedback = request.POST.get("feedback")
        try:
            feedabckStaff = FeedbackStaffs(staff_id=staff, feedback=feedback)
            feedabckStaff.save()
            messages.success(request, "Feedback sent succesfully")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Error while sending feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
