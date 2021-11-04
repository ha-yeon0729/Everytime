from django.db import models

class member(models.Model):
    etaId=models.CharField(max_length=20)
    etaPw=models.CharField(max_length=30)
    ssgId=models.CharField(max_length=20)
    ssgPw=models.CharField(max_length=30)

    # 자동으로 시간 저장
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]{self.etaId}'