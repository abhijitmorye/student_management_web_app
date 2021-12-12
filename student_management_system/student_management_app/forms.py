from django import forms
from .models import CustomUser, Courses, Staffs, Subjects, Students, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.CharField(max_length=100, label="Email",
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        max_length=100, label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, label="First Name", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label="Last Name",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=100, label="Address",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    courses = Courses.objects.all()
    courseList = []
    try:
        for course in courses:
            single_course = (course.id, course.course_name)
            courseList.append(single_course)
    except:
        courseList = []
    course = forms.ChoiceField(label="Course", choices=courseList,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    gender = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    sessionList = []
    try:
        sessions = SessionYearModel.objects.all()
        for session in sessions:
            smallSession = (
                session.id, str(session.session_start_year)+"-"+str(session.session_end_year))
            sessionList.append(smallSession)
    except:
        sessionList = []
    sex = forms.ChoiceField(choices=gender, label="Sex",
                            widget=forms.Select(attrs={'class': 'form-control'}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=sessionList,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    profile_image = forms.FileField(max_length=100, label="profile Pic",
                                    widget=forms.FileInput(attrs={'class': 'form-control'}))


class EditStudentForm(forms.Form):
    email = forms.CharField(max_length=100, label="Email",
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, label="First Name", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label="Last Name",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=100, label="Address",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    courses = Courses.objects.all()
    courseList = []
    try:
        for course in courses:
            single_course = (course.id, course.course_name)
            courseList.append(single_course)
    except:
        courseList = []
    course = forms.ChoiceField(label="Course", choices=courseList,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    gender = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    sessionList = []
    try:
        sessions = SessionYearModel.objects.all()
        for session in sessions:
            smallSession = (
                session.id, str(session.session_start_year)+"-"+str(session.session_end_year))
            sessionList.append(smallSession)
    except:
        sessionList = []
    sex = forms.ChoiceField(choices=gender, label="Sex",
                            widget=forms.Select(attrs={'class': 'form-control'}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=sessionList,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    profile_image = forms.FileField(max_length=100, label="profile Pic",
                                    widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
