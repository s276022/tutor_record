from django.db import models

# Create your models here.
# records/models.py

from django.db import models


# Create your models here.
class Record(models.Model):
    date = models.DateField(verbose_name="指導日")
    student_name = models.CharField(verbose_name="生徒名", max_length=100)
    subject = models.CharField(verbose_name="教科", max_length=50)
    duration = models.IntegerField(verbose_name="指導時間（分）", help_text="分単位で入力")
    content = models.TextField(verbose_name="指導内容")
    homework = models.TextField(verbose_name="宿題", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="記録作成日", auto_now_add=True)

    def __str__(self):
        # 管理画面などで表示されるときの名前
        return f"{self.date} {self.student_name} ({self.subject})"
