from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .forms import *
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import json
import os
import requests
from datetime import datetime, timedelta
import pytz
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from log_app.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

def header_view(request):
    return render(request, 'header.html')

def make_sharesheet(request):
    if request.method == 'GET':
        return render(request, 'log_app/make_sharesheet.html')
    if request.method == 'POST':
        activity = request.POST.get('activity')
        student = request.POST.get('student')
        return render(request, 'log_app/make_sharesheet.html', {'activity': activity, 'student': student})

def make_caliculm(request):
    if request.method == 'GET':
        return render(request, 'log_app/make_caliculm.html')

def check_caliculm(request):
    OPENAI_API_KEY = 'FtNgvdPCxSPHqW17Tg1uQB1lZMJ-YllQk2r3eiz1pOlpBrXUmM5sgbHLOTxw76bUlTcs04Y6-jckkxM-Rykm5yQ'
    OPENAI_API_BASE = 'https://api.openai.iniad.org/api/v1'
    chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE, model_name='gpt-4o-mini', temperature=0)

    if request.method == 'POST':
        sendedform = SendedForm(request.POST)
        form = CaliculumForm(request.POST)
        if sendedform.is_valid():
            caliculum_text = sendedform.cleaned_data['sheet']
            message = sendedform.cleaned_data['message']
            talk = [
                HumanMessage(content=caliculum_text + message)
            ]
            return render(request, 'log_app/check_caliculm.html', {'caliculum': chat(talk).content})

        elif form.is_valid():
            date = form.cleaned_data['date']
            text = form.cleaned_data['objective']
            url = "https://api.openweathermap.org/data/2.5/forecast"
            api_key = "88024955f764f1628b85fc6e7177425d"
            result = ""
            params = {
                "APPID": api_key,
                "units": "metric",
                "zip": "167-0053,jp",
                "lang": "ja"
            }
            res = requests.get(url, params=params)
            if res.status_code == 200:
                weather_data = res.json()
                forecast_list = weather_data.get('list', [])
                utc_timezone = pytz.timezone("UTC")
                jst_timezone = pytz.timezone("Asia/Tokyo")
                for forecast in forecast_list[:3]:
                    dt_txt_utc = forecast.get('dt_txt', '情報なし')
                    dt_utc = datetime.strptime(dt_txt_utc, '%Y-%m-%d %H:%M:%S')
                    dt_utc = utc_timezone.localize(dt_utc)
                    dt_jst = dt_utc.astimezone(jst_timezone)
                    temp = forecast['main'].get('temp', '情報なし')
                    humidity = forecast['main'].get('humidity', '情報なし')
                    weather_description = forecast['weather'][0].get('main', '情報なし')
                    result += f"日時: {dt_jst.strftime('%Y-%m-%d %H:%M:%S')}, 気温: {temp}°C, 湿度: {humidity}%, 天気: {weather_description}\n"
            else:
                print(f"エラー: {res.status_code}, {res.json()}")

            caliculum = [
                HumanMessage(content=f"""
                            -今日の天気-{result}
                            -生徒の特長-
                            1. *春樹くん*: 元気に走り回っていることから、活発でエネルギッシュな性格を持っている。
                            2. *健くん*: 「今日も元気いっぱい」とあるように、常に元気で明るい性格の持ち主である。
                            3. *はるかちゃん*: お人形遊びをしていることから、想像力が豊かで、遊びや芸術的な活動を楽しむ傾向がある。
                            4. *唯ちゃん*: はるかちゃんと一緒にお人形遊びをしているため、友達と協力して遊ぶことを楽しむ社交的な性格が示唆される。
                            -狙い-{text}
                            今日の日付と天気、気温、生徒の性格を考慮して今日の保育園での授業内容を10個考えてください
                            """)
            ]
            return render(request, 'log_app/check_caliculm.html', {'caliculum': chat(caliculum).content})

    return render(request, 'log_app/make_caliculm.html')

def complate(request):
    if request.method == 'POST':
        caliculum = request.POST.get('sheet')
        student_info = request.POST.get('student_info')
    return render(request, 'log_app/complate_sharesheet.html')

def check_sharesheet(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.cleaned_data['activity']
            student = form.cleaned_data['student']
            url = "https://api.openweathermap.org/data/2.5/forecast"
            api_key = "88024955f764f1628b85fc6e7177425d"
            params = {
                "APPID": api_key,
                "units": "metric",
                "zip": "167-0053,jp",
                "lang": "ja"
            }
            res = requests.get(url, params=params)
            if res.status_code == 200:
                weather_data = res.json()
                forecast_list = weather_data.get('list', [])
                utc_timezone = pytz.timezone("UTC")
                jst_timezone = pytz.timezone("Asia/Tokyo")
                result = ""
                for forecast in forecast_list[:3]:
                    dt_txt_utc = forecast.get('dt_txt', '情報なし')
                    dt_utc = datetime.strptime(dt_txt_utc, '%Y-%m-%d %H:%M:%S')
                    dt_utc = utc_timezone.localize(dt_utc)
                    dt_jst = dt_utc.astimezone(jst_timezone)
                    temp = forecast['main'].get('temp', '情報なし')
                    humidity = forecast['main'].get('humidity', '情報なし')
                    weather_description = forecast['weather'][0].get('main', '情報なし')
                    result += f"日時: {dt_jst.strftime('%Y-%m-%d %H:%M:%S')}, 気温: {temp}°C, 湿度: {humidity}%, 天気: {weather_description}\n"
                today = f"日時: {dt_jst.strftime('%Y-%m-%d %H:%M:%S')}, 気温: {temp}°C, 湿度: {humidity}%, 天気: {weather_description}"
            else:
                print(f"エラー: {res.status_code}, {res.json()}")

            OPENAI_API_KEY = 'FtNgvdPCxSPHqW17Tg1uQB1lZMJ-YllQk2r3eiz1pOlpBrXUmM5sgbHLOTxw76bUlTcs04Y6-jckkxM-Rykm5yQ'
            OPENAI_API_BASE = 'https://api.openai.iniad.org/api/v1'
            chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE, model_name='gpt-4o-mini', temperature=0)
            kyouyuu = [
                HumanMessage(content=f"""**クラス日誌作成のためのガイドライン**
                1 -今日の日付と天気-
                -今から渡す日付と天気のデータを元の文章のまま１行目に記載してください
                2. -本日の授業内容-
                - 本日の主なトピックを書かれた内容からより具体的に書いてください
                3. -生徒の活動-
                - 生徒が本日どんな様子だったかを記載。記載内容は本文のままにしてください。
                下記の情報のみを記載してまとめてください、嘘や憶測の情報は絶対に何があっても追加しないでください、ただし文章をうまいことつなげるなど添削はしてください
                全体の出力例：
                -今日の日付と天気-\n
                2024年9月24日、厚い雲
                -本日の授業内容-\n
                今日は雨が降っていたので、ピクニックは中止にして絵本の読み聞かせを行いました。１００万生きた猫を読み聞かせし、みんな楽しんでくれていた様子でした。(この例は実際の共有シートには書き込まないでください。)
                -生徒の活動-\n
                例：はるかちゃんは雷が怖くて泣き出してしまいました。(この例は実際の共有シートには書き込まないでください。)
                授業内容にはクラス全体がどのような様子だったかを記載して、生徒の活動の欄には具体的にどの生徒が何をしていたのかまで記載してください。
                -今日の日付と天気-\n{today}
                -本日の授業内容-\n{activity}
                -生徒の活動-\n{student}
                """)
            ]
            student_info = [
                HumanMessage(content=f"""
                            **以下の情報から生徒の性格を抜き出してください**
                            例：はるかちゃん：活発な性格、ゆうきくん少し寂しがり屋
                            {student}
                             """)
            ]
            print(chat(student_info).content)
            return render(request, 'log_app/check_sharesheet.html', {'sheet': chat(kyouyuu).content, 'activity': activity, 'student': student, 'student_info':chat(student_info).content})
    
    else:
        form = ActivityForm()
    return render(request, 'log_app/check_sharesheet.html', {'form': form})

def is_admin(user):
    return user.role == 'admin'

def is_caregiver(user):
    return user.role == 'caregiver'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class KindergartenList(ListView):
    model = Kindergarten
    template_name = 'log_app/kindergarten_list.html'
    context_object_name = 'kindergartens'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class KindergartenCreate(CreateView):
    model = Kindergarten
    fields = ['name', 'postal_code', 'policy']
    template_name = 'log_app/kindergarten_form.html'
    success_url = reverse_lazy('kindergarten_list')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class KindergartenUpdate(UpdateView):
    model = Kindergarten
    fields = ['name', 'postal_code', 'policy']
    template_name = 'log_app/kindergarten_form.html'
    success_url = reverse_lazy('kindergarten_list')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class KindergartenDelete(DeleteView):
    model = Kindergarten
    template_name = 'log_app/kindergarten_confirm_delete.html'
    success_url = reverse_lazy('kindergarten_list')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CaregiverList(ListView):
    model = User
    template_name = 'log_app/caregiver_list.html'
    context_object_name = 'caregivers'

    def get_queryset(self):
        return User.objects.filter(role='caregiver')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CaregiverCreate(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'email']
    template_name = 'log_app/caregiver_form.html'
    success_url = reverse_lazy('caregiver_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'caregiver'
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CaregiverUpdate(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'log_app/caregiver_form.html'
    success_url = reverse_lazy('caregiver_list')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CaregiverDelete(DeleteView):
    model = User
    template_name = 'log_app/caregiver_confirm_delete.html'
    success_url = reverse_lazy('caregiver_list')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    kindergarten = Kindergarten.objects.first()
    return render(request, 'log_app/admin_dashboard.html', {'kindergarten': kindergarten})

@login_required(login_url='/login/') 
@user_passes_test(is_caregiver)
def caregiver_dashboard(request):
    print(request.user.kindergarten_id)
    return render(request, 'log_app/caregiver_dashboard.html')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class StudentList(ListView):
    model = Student
    template_name = 'log_app/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(kindergarten=user.kindergarten)

@method_decorator([login_required, user_passes_test(is_caregiver)], name='dispatch')
class CaregiverStudentList(ListView):
    model = Student
    template_name = 'log_app/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(caregiver=user)

class StudentDetail(DetailView):
    model = Student
    context_object_name = 'student'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class StudentCreate(CreateView):
    model = Student
    fields = "__all__"
    success_url = reverse_lazy('students')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class StudentUpdate(UpdateView):
    model = Student
    fields = "__all__"
    success_url = reverse_lazy('students')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('students')
    context_object_name = 'student'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CaregiverLoginView(LoginView):
    fields = "__all__"
    template_name = 'log_app/login.html'

    def get_success_url(self):
        return reverse_lazy('home')