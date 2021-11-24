from django.db import models

class member(models.Model):
    name=models.CharField(max_length=20,null=True,default='')
    etaId=models.CharField(max_length=20)
    etaPw=models.CharField(max_length=30)
    ssgId=models.CharField(max_length=20)
    ssgPw=models.CharField(max_length=30)

    # 자동으로 시간 저장
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]{self.etaId}'

class friend(models.Model):
    my_name = models.CharField(max_length=20,null=True,default='')
    friend_name = models.CharField(max_length=20,null=True,default='')
    mon = models.CharField(max_length=20,null=True,default='')
    tue = models.CharField(max_length=20,null=True,default='')
    wed = models.CharField(max_length=20,null=True,default='')
    thu = models.CharField(max_length=20,null=True,default='')
    fri = models.CharField(max_length=20,null=True,default='')

    #my_name=models.CharField(max_length=20)
    #friend_name=models.CharField(max_length=20)
    #mon=models.CharField(max_length=100)
    #tue=models.CharField(max_length=100)
    #wed=models.CharField(max_length=100)
    #thu=models.CharField(max_length=100)
    #fri=models.CharField(max_length=100)


class excel_db(models.Model):
    my_name = models.CharField(max_length=20,null=True,default='')
    friend_name = models.CharField(max_length=20,null=True,default='')
    mon = models.CharField(max_length=50,null=True,default='')
    tue = models.CharField(max_length=50,null=True,default='')
    wed = models.CharField(max_length=50,null=True,default='')
    thu = models.CharField(max_length=50,null=True,default='')
    fri = models.CharField(max_length=50,null=True,default='')