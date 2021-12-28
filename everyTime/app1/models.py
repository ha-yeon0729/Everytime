from django.db import models

class member(models.Model):
    name=models.CharField(max_length=20,null=True,default='')
    etaId=models.CharField(max_length=20)
    etaPw=models.CharField(max_length=200)
    ssgId=models.CharField(max_length=20)
    ssgPw=models.CharField(max_length=200)

    # 자동으로 시간 저장
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]{self.etaId}'

class friend(models.Model):
    my_name = models.CharField(max_length=20,null=True,default='')
    friend_name = models.CharField(max_length=20,null=True,default='')
    mon = models.CharField(max_length=50,null=True,default='')
    tue = models.CharField(max_length=50,null=True,default='')
    wed = models.CharField(max_length=50,null=True,default='')
    thu = models.CharField(max_length=50,null=True,default='')
    fri = models.CharField(max_length=50,null=True,default='')

    def __str__(self):
        return f'{self.pk}. {self.friend_name}'


class excel_db(models.Model):
    my_name = models.CharField(max_length=20,null=True,default='')
    friend_name = models.CharField(max_length=20,null=True,default='')
    mon = models.CharField(max_length=50,null=True,default='')
    tue = models.CharField(max_length=50,null=True,default='')
    wed = models.CharField(max_length=50,null=True,default='')
    thu = models.CharField(max_length=50,null=True,default='')
    fri = models.CharField(max_length=50,null=True,default='')

    def __str__(self):
        return f'{self.pk}. {self.friend_name}'