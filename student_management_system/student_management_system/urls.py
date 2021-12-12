"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student_management_system import settings
from student_management_app import views
from student_management_app import HodViews, StaffViews, StudentViews

# app_name = "student_management_app"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.sampleDemo, name='demo'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.showLoginPage, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('get_user_details', views.GetUserDetails, name='getUserDetails'),
    path('logout_user', views.logoutUser, name='logoutUser'),
    path('admin_home/', HodViews.adminHome, name='adminHome'),
    path('manage_staff/', HodViews.manage_staff, name='manage_staff'),
    path('add_student/', HodViews.add_student, name="add_student"),
    path('manage_student', HodViews.manage_student, name="manage_student"),
    path('add_course', HodViews.add_course, name="add_course"),
    path('manage_course', HodViews.manage_course, name="manage_course"),
    path('manage_subject', HodViews.manage_subject, name='manage_subject'),
    path('add_staff', HodViews.add_staff, name="add_staff"),
    path('add_staff_save', HodViews.add_staff_save, name="add_staff_save"),
    path('add_course_save', HodViews.add_course_save, name="add_course_save"),
    path('add_student_save', HodViews.add_student_save, name="add_student_save"),
    path('add_subject', HodViews.add_subject, name="add_subject"),
    path('add_subject_save', HodViews.add_subject_save, name="add_subject_save"),
    path('manage_staff', HodViews.manage_staff, name="manage_staff"),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff, name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save, name="edit_staff_save"),
    path('edit_student/<str:student_id>',
         HodViews.edit_student, name="edit_student"),
    path('edit_student_save',
         HodViews.edit_student_save, name="edit_student_save"),
    path('edit_course/<str:course_id>', HodViews.edit_course, name="edit_course"),
    path('edit_course_save', HodViews.edit_course_save, name="edit_course_save"),
    path('edit_subject/<str:subject_id>',
         HodViews.edit_subject, name="edit_subject"),
    path('edit_subject_save', HodViews.edit_subject_save, name='edit_subject_save'),
    path('manage_session/', HodViews.manage_session, name="manage_session"),
    path('add_session_save', HodViews.add_session_save, name="add_session_save"),
    path('check_email_exist/', HodViews.check_email_exist,
         name="check_email_exist"),
    path('check_username_exist/', HodViews.check_username_exist,
         name="check_username_exist"),
    path('student_feedback_message', HodViews.student_feedback_message,
         name="student_feedback_message"),
    path('staff_feedback_message', HodViews.staff_feedback_message,
         name="staff_feedback_message"),
    path('student_feedback_message_reply', HodViews.student_feedback_message_reply,
         name="student_feedback_message_reply"),
    path('staff_feedback_message_reply', HodViews.staff_feedback_message_reply,
         name="staff_feedback_message_reply"),
    path('student_leave_view/', HodViews.student_leave_view,
         name="student_leave_view"),
    path('student_leave_approve/<leave_id>/',
         HodViews.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/',
         HodViews.student_leave_reject, name="student_leave_reject"),
    path('staff_leave_view/', HodViews.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/',
         HodViews.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/',
         HodViews.staff_leave_reject, name="staff_leave_reject"),
    path('admin_view_attendance/', HodViews.admin_view_attendance,
         name="admin_view_attendance"),
    path('admin_get_attendance_dates/', HodViews.admin_get_attendance_dates,
         name="admin_get_attendance_dates"),
    path('admin_get_attendance_student/', HodViews.admin_get_attendance_student,
         name="admin_get_attendance_student"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update,
         name="admin_profile_update"),


    #   staff url path
    path('staff_home/', StaffViews.staff_home, name='staff_home'),
    path('staff_take_attendance/', StaffViews.staff_take_attendance,
         name='staff_take_attendance'),
    path('get_students/', StaffViews.get_students, name="get_students"),
    path('save_attendance_data', StaffViews.save_attendance_data,
         name="save_attendance_data"),
    path('staff_update_attendance/', StaffViews.staff_update_attendance,
         name='staff_update_attendance'),
    path('get_attendance_dates/', StaffViews.get_attendance_dates,
         name='get_attendance_dates'),
    path('get_attendance_students', StaffViews.get_attendance_students,
         name='get_attendance_students'),
    path('update_attendance_data', StaffViews.update_attendance_data,
         name="update_attendance_data"),
    path('staff_apply_leave', StaffViews.staff_apply_leave,
         name="staff_apply_leave"),
    path('apply_staff_leave_save', StaffViews.apply_staff_leave_save,
         name="apply_staff_leave_save"),
    path('staff_feedback', StaffViews.staff_feedback,
         name="staff_feedback"),
    path('staff_feedback_save', StaffViews.staff_feedback_save,
         name="staff_feedback_save"),
    path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_update/', StaffViews.staff_profile_update,
         name="staff_profile_update"),
    path('staff_add_result/', StaffViews.staff_add_result, name="staff_add_result"),
    path('staff_add_result_save/', StaffViews.staff_add_result_save,
         name="staff_add_result_save"),

    #   student url path
    path('student_home/', StudentViews.student_home, name='student_home'),
    path('student_view_attendance/', StudentViews.student_view_attendance,
         name='student_view_attendance'),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post,
         name='student_view_attendance_post'),
    path('student_apply_leave', StudentViews.student_apply_leave,
         name="student_apply_leave"),
    path('apply_student_leave_save', StudentViews.apply_student_leave_save,
         name="apply_student_leave_save"),
    path('student_feedback', StudentViews.student_feedback,
         name="student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save,
         name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update,
         name="student_profile_update"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
