from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.utils.timezone import now

# ▼ langchain ではなく langchain_community に変更
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

import json
import os
import requests
from datetime import datetime, timedelta
import pytz

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from log_app.models import *
from accounts.models import *
from .forms import *

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
   # 1. 今ログインしているユーザーの担当している生徒の情報を取得
    user_id = request.user.id
    journals = Journal.objects.filter(caregiver_id=user_id)
    docs = []
    for journal_entry in journals:
        content_str = str(journal_entry.students_condition)
        doc = Document(
            page_content=content_str,
            metadata={
                "journal_id": journal_entry.id,
                "caregiver_id": journal_entry.caregiver_id,
            }
        )
        docs.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=settings.OPENAI_API_KEY,
        openai_api_base='https://api.openai.iniad.org/api/v1'
    )
    embedding = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY,
        openai_api_base='https://api.openai.iniad.org/api/v1'
    )

    vector_store = Chroma.from_documents(documents=split_docs, embedding=embedding)

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever())
    # 今ログインしているユーザーの保育園の郵便番号を取得
    Kindergarten_id = request.user.kindergarten_id
    Kindergarten_info = Kindergarten.objects.get(id = Kindergarten_id)
    chat = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, openai_api_base=settings.OPENAI_API_BASE, model_name='gpt-4o-mini', temperature=0)
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
                "zip": "167-0053" + ",jp",
                "lang": "ja"
            }
            res = requests.get(url, params=params)
            if res.status_code == 200:
                weather_data = res.json()
                forecast_list = weather_data.get('list', [])
                for forecast in forecast_list[:3]:
                    temp = forecast['main'].get('temp', '情報なし')
                    humidity = forecast['main'].get('humidity', '情報なし')
                    weather_description = forecast['weather'][0].get('main', '情報なし')
                    result += f"日時: {date}, 気温: {temp}°C, 湿度: {humidity}%, 天気: {weather_description}\n"
                query=f"""
                        -授業の日付、{date}、 今日の天気-{result}、 -本日の狙い-{text}、 -園の方針-{Kindergarten_info.policy}
                        今日の日付と天気、気温、与えられた生徒の性格を考慮して今日の保育園での授業内容を10個考えてください.
                        生徒の情報が不足している場合には一般的な授業を考えてください。
                        """
                answer = qa.run(query)
                return render(request, 'log_app/check_caliculm.html', {'caliculum': answer})
            else:
                print(f"エラー: {res.status_code}, {res.json()}")

    return render(request, 'log_app/make_caliculm.html')

def complate(request):
    if request.method == 'POST':
        sharesheet = request.POST.get('sheet')
        student_info = request.POST.get('student_info')
        kindergarden_id = request.user.kindergarten_id
        caregiver_id = request.user.id
        Journal.objects.create(  
            date=now().date(),
            shared_sheet = sharesheet,
            caregiver_id=caregiver_id,
            kindergarten_id=kindergarden_id,
            students_condition=student_info
        )

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
            chat = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, openai_api_base=settings.OPENAI_API_BASE, model_name='gpt-4o-mini', temperature=0)
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
                            文脈から察することができる性格も抜き出してください。
                            {student}性格を抜き出すだけにしてそれ以外の情報は一切載せないようにしてください。
                            """)
            ]
            return render(request, 'log_app/check_sharesheet.html', {'sheet': chat(kyouyuu).content, 'activity': activity, 'student': student, 'student_info':chat(student_info).content})
    
    else:
        form = ActivityForm()
    return render(request, 'log_app/check_sharesheet.html', {'form': form})

def student_detail(request, pk):    

    # 今ログインしているユーザーの担当している Journal を取得
    user_id = request.user.id
    journals = Journal.objects.filter(caregiver_id=user_id)

    docs = []
    for journal_entry in journals:
        content_str = str(journal_entry.students_condition)
        doc = Document(
            page_content=content_str,
            metadata={
                "journal_id": journal_entry.id,
                # もし Journal に student_id があるならここで入れる
                # 例: "student_id": journal_entry.student_id
            }
        )
        docs.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=settings.OPENAI_API_KEY,
        openai_api_base="https://api.openai.iniad.org/api/v1"
    )
    embedding = OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY,
        openai_api_base="https://api.openai.iniad.org/api/v1"
    )
    vector_store = Chroma.from_documents(split_docs, embedding=embedding)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever()
    )

    student = Student.objects.get(pk=pk)

    query = f"""
    {student.name}の性格に関する情報を教えてください。
    生徒の性格に関する情報以外が入っていないかを再度確認して入っていなければ送ってください。
    """

    answer = qa.run(query)
    print(answer)
    return render(request, 'log_app/student_detail.html', {'student': student,'answer': answer})

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