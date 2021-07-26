from django.db import models

# Create your models here.
from django.http import HttpResponse, JsonResponse


class countrys(models.Model):
    cname = models.CharField(max_length=100)
    lead_name = models.CharField(max_length=100)
    young_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cname


class firstshow(models.Model):
    name = models.CharField(max_length=100)
    lead_num = models.FloatField()
    young_num = models.FloatField()
    value_num = models.FloatField()


class firstcollege(models.Model):
    college_name = models.CharField(max_length=100)
    college_nameE = models.CharField(max_length=100)
    cname = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=100)


def listcountry(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = countrys.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


def addcountry(request):
    info = request.params['data']

    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = countrys.objects.create(cname=info['cname'],
                                     college_name=info['college_name'],
                                     lead_name=info['lead_name'],
                                     young_name=info['young_name'],
                                     subject_name=info['subject_name'],
                                     field_name=info['field_name'])

    return JsonResponse({'ret': 0, 'id': record.id})


def modifycountry(request):
    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作

    countryid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        country = countrys.objects.get(id=countryid)
    except countrys.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{countryid}`的客户不存在'
        }

    if 'cname' in newdata:
        country.name = newdata['cname']
    if 'college_name' in newdata:
        country.college_name = newdata['college_name']
    if 'lead_name' in newdata:
        country.lead_name = newdata['lead_name']
    if 'young_name' in newdata:
        country.lead_name = newdata['young_name']
    if 'subject_name' in newdata:
        country.lead_name = newdata['subject_name']
    if 'field_name' in newdata:
        country.lead_name = newdata['field_name']

    # 注意，一定要执行save才能将修改信息保存到数据库
    country.save()

    return JsonResponse({'ret': 0})


def deletecountry(request):
    countryid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        country = countrys.objects.get(id=countryid)
    except countrys.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{countryid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    country.delete()

    return JsonResponse({'ret': 0})

# 用例文件
# class CaseFile(models.Model):
#     case_class = models.ForeignKey(CaseClass)
#     file_name = models.FileField(upload_to='case/%Y/%m/%d/', verbose_name=u"文件名称")
#
#     # 不注释会报错
#     # def __str__(self):
#     #     return self.file_name
#
#     # 定义表名称
#     class Meta:
#         verbose_name = "用例文件管理"
#         verbose_name_plural = "用例文件管理"
