import os

import xlrd
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from country.models import countrys
from country.models import firstshow
from country.models import firstcollege
import json
from django.db.models import Q, Count
from itertools import chain
from listmap.settings import BASE_DIR


def showall(request):
    cou = countrys.objects.all()
    return render(request, 'show.html', {'cou': cou})


def get_color(value):
    switch = {
        0: '#f5f5dc',
        1: '#f5deb3',
        2: '#deb887',
        3: '#f4a460',
        4: '#d2b48c',
        5: '#cd853f',
        6: '#a0522d',
        7: '#d2691e',
        8: '#8b4513',
        9: '#b22222',
        10: '#a52a2a'
    }
    return switch.get(value, '#a52a2a')


def show(request):
    subject = request.GET.get('id')
    if subject is None:
        subject = '机械工程'
    # 用来获取有高校的国家数量
    value_list = []
    value_ = []

    out = countrys.objects.values('cname').distinct()
    out = list(out)
    for o in out:
        value_dict = {}
        cx = countrys.objects.filter(cname=o['cname']).filter(subject_name=subject).values('college_name').distinct()
        cy = firstcollege.objects.filter(cname=o['cname']).filter(subject_name=subject).values('college_name').distinct()
        cx = list(cx)
        cy = list(cy)
        a = []
        for i in cx:
            for key, item in i.items():
                a.append(item)
        for j in cy:
            for key, item in j.items():
                a.append(item)
        c = len(list(set(a)))
        c1 = countrys.objects.filter(cname=o['cname']).filter(subject_name=subject).filter(~Q(lead_name='否')).distinct().count()
        c2 = countrys.objects.filter(cname=o['cname']).filter(subject_name=subject).filter(~Q(young_name='否')).distinct().count()

        value_dict['name'] = o['cname']
        value_dict['value_num'] = c
        value_dict['lead_num'] = c1
        value_dict['young_num'] = c2
        value_list.append(value_dict)
        out = value_list
        value_.append(c)

    # 去重
    value_ = list(set(value_))
    value_.sort()
    # 插入颜色
    for i in value_list:
        if i['value_num'] != 0:
            id = value_.index(i['value_num'])
            i['itemStyle'] = {'color': get_color(id)}  # 添加
    # with open("zzz.json", "w") as fp:
    #     # fp.write(json.dumps(data, indent=4, ensure_ascii=False))
    #     fp.write(json.dumps(out, indent=4))
    # print(out)
    subject = [subject]
    return render(request, 'index.html', {'out': out, 'subject': subject})


def show1(request):
    city = request.GET.get('id')
    # city = request.GET.get('country')
    cou1 = countrys.objects.filter(~Q(lead_name='NULL')).filter(cname=city).values('id', 'cname', 'lead_name',
                                                                                   'college_name', 'field_name')
    cou2 = countrys.objects.filter(cname=city).filter(~Q(young_name='NULL')).values('id', 'cname', 'young_name',
                                                                                    'college_name', 'field_name')
    result1 = list(cou1)
    result2 = list(cou2)
    return render(request, 'country.html', {'cou1': cou1, 'cou2': cou2, 'leader': result1, 'young': result2})


def school(request):
    data = []
    country = request.GET.get('id')
    subject = request.GET.get('subject')

    #print(subject)
    # country = '中国'
    school = countrys.objects.filter(cname=country).filter(subject_name=subject).values('college_name').distinct()
    # 获取一流学科列表
    first_college = firstcollege.objects.filter(cname=country).filter(subject_name=subject).values('college_name')
    first_college = list(first_college)
    print(first_college)
    schools = list(school)
    for school in schools:
        school = school['college_name']
        lead_num = countrys.objects.filter(cname=country).filter(~Q(lead_name='NULL')).filter(
            college_name=school).filter(subject_name=subject).count()
        young_num = countrys.objects.filter(cname=country).filter(~Q(young_name='NULL')).filter(
            college_name=school).filter(subject_name=subject).count()
        # print(school,lead_num,young_num)
        is_first = "×"
        if {'college_name': school} in first_college:
            is_first = "√"
        data.append({'college_name': school, 'lead_num': lead_num, 'young_num': young_num, 'is_first': is_first})
    subject = [subject]
    return render(request, 'school.html', {'data': data, 'subject':subject})


def school_detail(request):
    school = request.GET.get('id')
    subject = request.GET.get('subject')
    # school = '清华大学'
    lead = countrys.objects.filter(~Q(lead_name='NULL')).filter(college_name=school).filter(subject_name=subject).values('cname', 'lead_name',
                                                                                            'college_name',
                                                                                            'subject_name',
                                                                                            'field_name')
    young = countrys.objects.filter(college_name=school).filter(~Q(young_name='NULL')).filter(subject_name=subject).values('cname', 'young_name',
                                                                                              'college_name',
                                                                                              'subject_name',
                                                                                              'field_name')
    lead = list(lead)
    young = list(young)
    subject = [subject]
    return render(request, 'school_detail.html', {'lead': lead, 'young': young})


def login_admin(request):
    if request.method == "POST":
        name = request.POST.get("uname")
        pwd = request.POST.get("upass")
        if name == "admin" and pwd == "admin":
            # request.session['user='] = name;
            return render(request, 'admin.html')
        else:
            return render(request, 'login_admin.html')
    return render(request, 'login_admin.html')


def admin(request):
    return render(request, 'admin.html')


def leader(request):
    cou = countrys.objects.filter(Q(young_name='否')).values('id', 'cname', 'lead_name', 'college_name',
                                                               'subject_name')
    result = list(cou)
    return render(request, 'leader.html', {'data': result})


def young(request):
    cou = countrys.objects.filter(Q(lead_name='否')).values('id', 'cname', 'young_name', 'college_name',
                                                              'subject_name')
    result = list(cou)
    return render(request, 'young.html', {'data': result})


def addPerson(request):
    if request.method == "POST":
        name = request.POST.get("name")
        lead_name = name
        young_name = name
        person_type = request.POST.get("person_type")
        if person_type == "领军人才":
            young_name = 'NULL'
        else:
            lead_name = "NULL"
        country = request.POST.get("country")
        college = request.POST.get("college")
        research = request.POST.get("research")
        field = request.POST.get("field")
        countrys.objects.create(  # 数据库插入语句
            cname=country,
            lead_name=lead_name,
            young_name=young_name,
            college_name=college,
            subject_name=field,
            field_name=research
        )
        if young_name == "NULL":
            return redirect("/country/leader/")
        else:
            return redirect("/country/young/")
    else:
        return render(request, 'addPerson.html')


def delPerson(request):
    id = request.GET.get('delete_id')
    option = request.GET.get('option')
    countrys.objects.filter(id=id).delete()
    if option == "1":
        return redirect("/country/leader/")
    else:
        return redirect("/country/young/")


def updatePerson(request):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        lead_name = name
        young_name = name
        country = request.POST.get("country")
        person_type = request.POST.get("person_type")
        if person_type == "领军人才":
            young_name = '无'
        elif person_type == "青年人才":
            lead_name = "无"
        college = request.POST.get("college")
        research = request.POST.get("research")
        field = request.POST.get("field")
        countrys.objects.filter(id=id).update(  # 数据库插入语句
            cname=country,
            lead_name=lead_name,
            young_name=young_name,
            college_name=college,
            subject_name=field,
            field_name=research
        )
        return redirect("/country/leader/")
    id = request.GET.get('update_id')
    option = request.GET.get('option')
    print(type(option))
    if option == "1":
        cou1 = countrys.objects.filter(id=id).values('id', 'cname', 'lead_name', 'college_name', 'subject_name',
                                                     'field_name')
        result1 = list(cou1)
        return render(request, 'updatePerson.html', {'data': result1})
    else:
        cou1 = countrys.objects.filter(id=id).values('id', 'cname', 'young_name', 'college_name', 'subject_name',
                                                     'field_name')
        result1 = list(cou1)
        return render(request, 'updatePerson.html', {'data': result1})


def query(request):
    query = request.GET.get("query")
    option = request.GET.get('option')
    print(query,option)
    if option == "1":
        cou1 = countrys.objects.filter(~Q(lead_name="NULL")).filter(Q(lead_name=query) | Q(college_name=query) | Q(subject_name=query)).values(
            'id', 'cname', 'lead_name',
            'college_name', 'subject_name')
        result = list(cou1)
        return render(request, 'leader.html', {'data': result})
    else:
        cou1 = countrys.objects.filter(~Q(young_name="NULL")).filter(
            Q(young_name=query) | Q(college_name=query) | Q(subject_name=query)).values('id', 'cname', 'young_name',
                                                                'college_name', 'subject_name')
        result = list(cou1)
        return render(request, 'young.html', {'data': result})


# def up_excel(request):
#     if request.method == "POST":
#         File = request.FILES.get("files", None)
#         if File is None:
#             return HttpResponse("请选择需要上传的文件")
#         else:
#             josn_data = []
#             index = request.POST.get("index")
#             index = int(index) - 1
#             person_type = request.POST.get("person_type")
#             subject = request.POST.get("subject")
#             country = request.POST.get("country")
#             # 保存本地
#             u = os.path.join(BASE_DIR, 'static\\files')
#             url = os.path.join(u, File.name)
#             with open(url, 'wb')as f:
#                 for data in File.chunks():
#                     f.write(data)
#             # 读取数据
#             readbook = xlrd.open_workbook(url)
#             # 打开第一张表（一个Excel文件可以有多张表）
#             sheet = readbook.sheet_by_index(index)
#             # 获取行数
#             nrows = sheet.nrows
#             for x in range(2, nrows):
#                 # row表示某一行的所有数据，是一个列表
#                 row = sheet.row_values(x)
#                 # print(row)
#                 # 处理数据
#                 name = row[1].strip()
#                 young_name = name
#                 lead_name = name
#                 if person_type == "领军人才":
#                     young_name = 'NULL'
#                 else:
#                     lead_name = "NULL"
#                 college = row[2].strip()
#                 research = ""
#                 field = request.POST.get("subject")
#                 if country == "中国":
#                     research = row[3].strip()
#                 else:
#                     country = row[3].strip()
#                     research = request.POST.get("field")
#                     field = research
#                 # 先判断是否重复
#                 find_repeat = countrys.objects.filter(cname=country).filter(lead_name=lead_name).filter(
#                     young_name=young_name).filter(college_name=college).filter(subject_name=field)
#                 if find_repeat is not None:
#                     continue
#                 countrys.objects.create(  # 数据库插入语句
#                     cname=country,
#                     lead_name=lead_name,
#                     young_name=young_name,
#                     college_name=college,
#                     subject_name=field,
#                     field_name=research
#                 )
#                 josn_data.append(
#                     {"cname": country, "lead_name": lead_name, "young_name": young_name, "college_name": college,
#                      "subject_name": field, "field_name": research})
#             # print(josn_data)
#             return render(request, 'up_excel.html', {'data': josn_data})
#     else:
#         return render(request, 'up_excel.html')
def up_excel(request):
    if request.method == "POST":
        File = request.FILES.get("files", None)
        if File is None:
            return HttpResponse("请选择需要上传的文件")
        else:
            josn_data = []
            index = request.POST.get("index")
            index = int(index) - 1
            # print(index)
            # person_type = request.POST.get("person_type")
            subject = request.POST.get("subject")
            # print(subject)
            # country = request.POST.get("country")
            # 保存本地
            # print(subject)
            u = os.path.join(BASE_DIR, 'static\\files')
            url = os.path.join(u, File.name)
            with open(url, 'wb')as f:
                for data in File.chunks():
                    f.write(data)
            # 读取数据
            readbook = xlrd.open_workbook(url)
            # 打开第一张表（一个Excel文件可以有多张表）
            sheet = readbook.sheet_by_index(index)
            # 获取行数
            nrows = sheet.nrows
            for x in range(1, nrows):
                # row表示某一行的所有数据，是一个列表
                row = sheet.row_values(x)
                # 处理数据
                # print(row[0])
                name = row[0].strip()
                college = row[1].strip()
                country = row[2].strip()
                person_type = row[3].strip()
                young_name = name
                lead_name = name
                # print(name, school, country, lead_young)
                if person_type == "领":
                    young_name = '否'
                elif person_type == "青":
                    lead_name = "否"
                field = "无"
                print(country,lead_name,young_name,college,subject,field)
                # 先判断是否重复
                find_repeat = countrys.objects.filter(cname=country).filter(lead_name=lead_name).filter(
                    young_name=young_name).filter(college_name=college).filter(subject_name=subject)
                find_repeat = list(find_repeat)
                if len(find_repeat) == 0:
                    print("数据添加")

                else:
                    print("result:",find_repeat)
                    print("数据重复")
                    continue
                countrys.objects.create(  # 数据库插入语句
                    cname=country,
                    lead_name=lead_name,
                    young_name=young_name,
                    college_name=college,
                    subject_name=subject,
                    field_name=field
                )
                josn_data.append(
                    {"cname": country, "lead_name": lead_name, "young_name": young_name, "college_name": college,
                     "subject_name": subject, "field_name": field})
            print(josn_data)
            return render(request, 'up_excel.html', {'data': josn_data})
    else:
        return render(request, 'up_excel.html')

def subjects(request):
    cou1 = firstcollege.objects.values("id", "college_name", "college_nameE", "cname", "subject_name")
    result = list(cou1)
    return render(request, 'subjects.html', {'data': result})

def querysubjects(request):
    query = request.GET.get("querysubjects")
    print(query)
    cou1 = firstcollege.objects.filter(Q(cname=query) | Q(subject_name=query) | Q(college_name=query) | Q(college_nameE=query)).values(
            'college_name', 'college_nameE', 'cname', 'subject_name').distinct()
    result = list(cou1)
    return render(request, 'subjects.html', {'data': result})

def addsubjects(request):
    if request.method == "POST":
        country = request.POST.get("country")
        college = request.POST.get("college")
        collegeE = request.POST.get('collegeE')
        research = request.POST.get("research")
        if firstcollege.objects.filter(Q(cname=country) & Q(college_name=college) & Q(subject_name=research) & Q(college_nameE=collegeE)):
            messages.success(request, "您输入的信息已经存在，请重新输入！")
            return render(request, 'addsubjects.html')

        else:
            firstcollege.objects.create(  # 数据库插入语句
                cname=country,
                college_name=college,
                college_nameE=collegeE,
                subject_name=research,
            )
            return render(request, 'addsubjects.html')
    else:
        return render(request, 'addsubjects.html')

def updatesubjects(request):
    if request.method == "POST":
        id = request.POST.get("id")
        country = request.POST.get("country")
        college = request.POST.get("college")
        collegeE = request.POST.get('collegeE')
        research = request.POST.get("research")
        firstcollege.objects.filter(id=id).update(  # 数据库插入语句
            cname=country,
            college_name=college,
            college_nameE=collegeE,
            subject_name=research
        )
        return redirect("/country/updatesubjects/")
    id = request.GET.get('update_id')
    cou1 = firstcollege.objects.filter(id=id).values('id', 'cname',  'college_name', 'college_nameE', 'subject_name')
    result1 = list(cou1)
    return render(request, 'updatesubjects.html', {'data': result1})
def delsubjects(request):
    id = request.GET.get('delete_id')
    firstcollege.objects.filter(id=id).delete()
    return redirect("/country/subjects/")
def sub_select_subject(request):
    return render(request, 'sub_select_subject.html')
