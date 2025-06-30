from django.urls import path
from . import views  # 同じフォルダの views.py を読み込む

urlpatterns = [
    # records/ にアクセスが来たら、views.py の record_list という関数を呼び出す
    path("", views.home_view, name="home"),
    path("list/", views.record_list, name="record_list"),
    # グラフにアクセスしたら今月文を表示
    path("graph/", views.graph_redirect_view, name="graph_current"),
    # /graph/2025/7/ のようなURLに対応する
    path("graph/<int:year>/<int:month>/", views.graph_view, name="graph_detail"),
]
