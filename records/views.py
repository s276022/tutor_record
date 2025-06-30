from django.shortcuts import render, redirect

# Create your views here.
from .models import Record  # Recordモデルを読み込む

from django.http import JsonResponse
from django.db.models import Sum
import calendar
from datetime import datetime


def record_list(request):
    # データベースから全てのRecordオブジェクトを取得する
    records = Record.objects.all().order_by("-date")  # order_byで日付の新しい順に並び替え

    # recordsという名前でHTMLにデータを渡し、表示を依頼する
    return render(request, "records/record_list.html", {"records": records})


def graph_redirect_view(request):
    today = datetime.now()
    # 今現在の年月のグラフページへリダイレクトする
    return redirect("graph_detail", year=today.year, month=today.month)


def graph_view(request, year, month):
    # 存在しない月が指定されたときのエラーを防ぐ
    if not 1 <= month <= 12:
        return redirect("graph_current")  # エラーなら今月のグラフへ

    # その月の日数を取得 (例: 6月なら30日)
    _, num_days = calendar.monthrange(year, month)

    # 日ごとの指導時間を格納するリストを準備（最初は全て0）
    daily_durations = [0] * num_days

    # 指定した月の記録を取得
    records_in_month = Record.objects.filter(date__year=year, date__month=month)

    # 日ごとの合計時間を計算
    daily_sums = records_in_month.values("date__day").annotate(total_duration=Sum("duration"))

    # 計算結果をリストに反映
    for item in daily_sums:
        # 日にちは1から始まるので、インデックスは-1する
        day_index = item["date__day"] - 1
        daily_durations[day_index] = item["total_duration"]

    # 総勉強時間（分）を計算
    total_minutes = sum(daily_durations)
    # 時間と分に変換
    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60

    # グラフのラベル（1日, 2日, ...）を作成
    labels = [f"{i+1}日" for i in range(num_days)]

    # 前の月を計算
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    # 次の月を計算
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1

    context = {
        "labels": labels,
        "data": daily_durations,
        "year": year,
        "month": month,
        "total_hours": total_hours,
        "remaining_minutes": remaining_minutes,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
    }
    return render(request, "records/graph.html", context)


def home_view(request):
    return render(request, "records/home.html")
