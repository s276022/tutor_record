from django.contrib import admin

# Register your models here.
from .models import Record  # この行を追加: 同じフォルダのmodels.pyからRecordモデルを読み込む

# Register your models here.
admin.site.register(Record)  # この行を追加: Recordモデルを管理サイトに登録する
