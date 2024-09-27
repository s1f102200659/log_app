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

# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from log_app.models import Student, Kindergarten
# from accounts.models import User
# Create your views here.
# def login(request):
#     return render(request, 'log_app/login.html')

# def home(request):
#     return render(request, 'log_app/home.html')
from django.contrib.auth import get_user_model
User = get_user_model()

def header_view(request):
    return render(request, 'header.html')

def make_sharesheet(request):
    if request.method == 'GET':
        return render(request, 'log_app/make_sharesheet.html')
    if request.method == 'POST':
        # POSTリクエストから送信された変数を取得
        activity = request.POST.get('activity')
        student = request.POST.get('student')
        return render(request, 'log_app/make_sharesheet.html',{'activity':activity,'student':student})
def make_caliculm(request):
    if request.method == 'GET':
        return render(request, 'log_app/make_caliculm.html')
def check_caliculm(request):
    OPENAI_API_KEY = 'TDao2F3EyHP9wlw7unKFrZzwTdCXCmwg5ZrjgfwuDP8-u4H1bMvW2AmlDp6-3x8fuObJZ8bm0TwxrWFi2LMu3YA'
    OPENAI_API_BASE = 'https://api.openai.iniad.org/api/v1'
    chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE, model_name='gpt-4o-mini', temperature=0)
    if request.method == 'POST':
        sendedform = SendedForm(request.POST)
        form = CaliculumForm(request.POST)
        if sendedform.is_valid():
            caliculum_text = sendedform.cleaned_data['sheet']
            message = sendedform.cleaned_data['message']
            talk = [
                HumanMessage(content= caliculum_text + message)
            ]
            return render(request,'log_app/check_caliculm.html',{'caliculum':chat(talk).content})
        elif form.is_valid():
            # フォームの処理
            date = form.cleaned_data['date']
            text = form.cleaned_data['objective']
            # OpenWeatherMapのAPIエンドポイント
            url = "https://api.openweathermap.org/data/2.5/forecast"
            # 有効なAPIキーをここに入れてください
            api_key = "88024955f764f1628b85fc6e7177425d"
            result = ""
            # パラメータの設定
            params = {
                "APPID": api_key,
                "units": "metric",
                "zip": "167-0053,jp",
                "lang": "ja"  # 日本語のレスポンスを取得するためのパラメータ
            }
            # APIへのリクエストを送信
            res = requests.get(url, params=params)
            if res.status_code == 200:
                # レスポンスのJSONデータを取得
                weather_data = res.json()
                # 3時間ごとの予報リストを取得
                forecast_list = weather_data.get('list', [])
                # タイムゾーンの設定
                utc_timezone = pytz.timezone("UTC")
                jst_timezone = pytz.timezone("Asia/Tokyo")
                for forecast in forecast_list[:3]:
                    # UTC日時を取得し、日本時間に変換
                    dt_txt_utc = forecast.get('dt_txt', '情報なし')
                    dt_utc = datetime.strptime(dt_txt_utc, '%Y-%m-%d %H:%M:%S')
                    dt_utc = utc_timezone.localize(dt_utc)  # UTCタイムゾーンを付加
                    dt_jst = dt_utc.astimezone(jst_timezone)  # 日本時間に変換
                    # 他の情報を取得
                    temp = forecast['main'].get('temp', '情報なし')
                    humidity = forecast['main'].get('humidity', '情報なし')
                    weather_description = forecast['weather'][0].get('main', '情報なし')
                    result += f"日時: {dt_jst.strftime('%Y-%m-%d %H:%M:%S')}, 気温: {temp}°C, 湿度: {humidity}%, 天気: {weather_description}" + "\n"
            else:
                print(f"エラー: {res.status_code}, {res.json()}")
            caliculum = [
                HumanMessage(content= f"""
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
            return render(request,'log_app/check_caliculm.html',{'caliculum':chat(caliculum).content})
    return render(request, 'log_app/make_caliculm.html')

def complate(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            sheet = form.cleaned_data['sheet']
    return render(request,'log_app/complate_sharesheet.html')

def check_sharesheet(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            # フォームの処理
            activity = form.cleaned_data['activity']
            student = form.cleaned_data['student']
            # 何か処理を行う
            # OpenWeatherMapのAPIエンドポイント
            url = "https://api.openweathermap.org/data/2.5/forecast"
            # 有効なAPIキーをここに入れてください
            api_key = "88024955f764f1628b85fc6e7177425d"
            # パラメータの設定
            params = {
                "APPID": api_key,
                "units": "metric",
                "zip": "167-0053,jp",
                "lang": "ja"  # 日本語のレスポンスを取得するためのパラメータ
            }
            # APIへのリクエストを送信
            res = requests.get(url, params=params)
            if res.status_code == 200:
                # レスポンスのJSONデータを取得
                weather_data = res.json()
                # 3時間ごとの予報リストを取得
                forecast_list = weather_data.get('list', [])
                # タイムゾーンの設定
                utc_timezone = pytz.timezone("UTC")
                jst_timezone = pytz.timezone("Asia/Tokyo")
                result = ""
                for forecast in forecast_list[:3]:
                    # UTC日時を取得し、日本時間に変換
                    dt_txt_utc = forecast.get('dt_txt', '情報なし')
                    dt_utc = datetime.strptime(dt_txt_utc, '%Y-%m-%d %H:%M:%S')
                    dt_utc = utc_timezone.localize(dt_utc)  # UTCタイムゾーンを付加
                    dt_jst = dt_utc.astimezone(jst_timezone)  # 日本時間に変換
                    # 他の情報を取得
                    temp = forecast['main'].get('temp', '情報なし')
                    humidity = forecast['main'].get('humidity', '情報なし')
                    weather_description = forecast['weather'][0].get('main', '情報なし')
                    result += f"日時: {dt_jst.strftime('%Y-%m-%d %H:%M:%S')}, 気温: {temp}°C, 湿度: {humidity}%, 天気: {weather_description}" + "\n"
                today = f"日時: {dt_jst.strftime('%Y-%m-%d %H:%M:%S')}, 気温: {temp}°C, 湿度: {humidity}%, 天気: {weather_description}"
            else:
                print(f"エラー: {res.status_code}, {res.json()}")
            OPENAI_API_KEY = 'TDao2F3EyHP9wlw7unKFrZzwTdCXCmwg5ZrjgfwuDP8-u4H1bMvW2AmlDp6-3x8fuObJZ8bm0TwxrWFi2LMu3YA'
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
            -今日の日付と天気-で改行、-本日の授業内容-で改行、-生徒の活動-で改行を行うようにして、空白の行も1行だけ入れてください"""
            + "-今日の日付と天気-\n" + today
            + "-本日の授業内容-" + activity
            + "-生徒の活動-" + student)
            ]
            return render(request,'log_app/check_sharesheet.html',{'sheet':chat(kyouyuu).content,'activity':activity,'student':student})# 処理後のリダイレクト
    
    else:
        message = """今から送る情報を元に、以下の形式で生徒の情報を1つのjson形式のオブジェクトとしてまとめて返してください。まとめる際は、一つ一つの要素を,で分けてください。
        key:生徒の名前,データ:その生徒の特長 例）{"エリカ":"砂遊びが好き。", "ショウ":"本を読むのがすき", "ケン":"友達とサッカーをしていた", "美穂":"りかとあゆみと遊んでいた"}
        生徒の名前についている、くん、ちゃんは省いて下さい。返す値は1つのjsonのリストだけにして、ほかのもの(```jsonのようなもの)は付け加えないでください。
        """ + "\n" + chat(kyouyuu).content
        messages = [
            HumanMessage(content=message),
        ]
        result = chat(messages)
        print(result.content)
        try:
            data_dict = json.loads(result.content)
            for key, value in data_dict.items():
                print(f"{key}: {value}")
        except Exception as e:
            print("Error parsing the result content:", e)
        form = ActivityForm()
    return render(request, 'log_app/check_sharesheet.html', {'form': form})

    #else:
     #   form = ActivityForm()
    #return render(request, 'your_template.html', {'form': form})

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

# 園情報の編集
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

# 保育士管理ビュー
@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CaregiverList(ListView):
    model = User  # assuming Caregiver is a type of User
    template_name = 'log_app/caregiver_list.html'
    context_object_name = 'caregivers'

    def get_queryset(self):
        return User.objects.filter(role='caregiver')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CaregiverCreate(CreateView):
    model = User  # assuming Caregiver is a type of User
    fields = ['username', 'password', 'first_name', 'last_name', 'email']  # adjust fields as necessary
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
    fields = ['username', 'first_name', 'last_name', 'email']  # exclude password for security
    template_name = 'log_app/caregiver_form.html'
    success_url = reverse_lazy('caregiver_list')

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CaregiverDelete(DeleteView):
    model = User
    template_name = 'log_app/caregiver_confirm_delete.html'
    success_url = reverse_lazy('caregiver_list')

# 管理者ダッシュボードビュー
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    kindergarten = Kindergarten.objects.first()  # ここで複数の園がある場合は適切にフィルタリングする
    return render(request, 'log_app/admin_dashboard.html', {'kindergarten': kindergarten})

# 保育士ダッシュボードビュー
@login_required
@user_passes_test(lambda u: u.role == 'caregiver')
def caregiver_dashboard(request):
    return render(request, 'log_app/caregiver_dashboard.html')


#生徒一覧
#管理者用のStudentListView
@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class StudentList(ListView):
    model = Student
    template_name = 'log_app/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(
            kindergarten=user.kindergarten
        )

#保育士用のStudentListView
@method_decorator([login_required, user_passes_test(is_caregiver)], name='dispatch')
class CaregiverStudentList(ListView):
    model = Student
    template_name = 'log_app/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(
            caregiver=user
        )


#生徒の詳細ページ
# @method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class StudentDetail(DetailView):
    model = Student
    context_object_name = 'student'

#生徒の追加・編集
# @login_required
# @user_passes_test(lambda u: u.is_admin)
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
    fields = "__all__"
    success_url = reverse_lazy('students')
    context_object_name = 'student'

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CaregiverLoginView(LoginView):
    fields = "__all__"
    template_name = 'log_app/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'log_app/admin_dashboard.html')

from django.shortcuts import render
from .models import Student
from django.views.generic import ListView

class StudentList(ListView):
    template_name = 'log_app/student_list.html'  # テンプレート名を適宜変更
    context_object_name = 'students'  # テンプレート内での変数名

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            student_list = Student.objects.filter(name__icontains=query)
        else:
            student_list = Student.objects.all()
        return student_list




# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

@login_required
@user_passes_test(is_caregiver)
def caregiver_dashboard(request):
    return render(request, 'log_app/caregiver_dashboard.html')
