import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt


file_path = "王者荣耀皮肤数据_标准化版.csv"
DATE_FORMAT = "%Y%m%d"

hero_date_map = defaultdict(list)
with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["日期是否有效"] == "是":
            hero_name = row["英雄名称"].strip()
            date_str = row["原始上线时间"].strip()
            try:
                skin_date = datetime.strptime(date_str, DATE_FORMAT).date()
                hero_date_map[hero_name].append(skin_date)
            except ValueError:
                continue

update_cycle_result = []
for hero, date_list in hero_date_map.items():
    skin_total = len(date_list)
    if skin_total < 2:
        continue
    date_sorted = sorted(date_list)
    interval_days = [(date_sorted[i] - date_sorted[i-1]).days for i in range(1, len(date_sorted))]
    update_cycle_result.append({
        "英雄名称": hero,
        "皮肤总数": skin_total,
        "平均周期(天)": round(sum(interval_days) / len(interval_days)),
        "平均周期(月)": round(sum(interval_days) / len(interval_days) / 30, 1),
        "最短间隔(天)": min(interval_days),
        "最长间隔(天)": max(interval_days)
    })


update_cycle_result.sort(key=lambda x: x["平均周期(天)"])

all_avg_days = sum([x["平均周期(天)"] for x in update_cycle_result]) / len(update_cycle_result)

print("=" * 80)
print("【英雄皮肤更新频率排行榜 Top20】（周期越短，更新频率越高）")
print("=" * 80)
print(f"{'排名':<4}{'英雄名称':<12}{'皮肤总数':<8}{'平均周期(天)':<14}{'平均周期(月)':<14}{'最短间隔(天)':<12}")
print("-" * 80)
for rank, item in enumerate(update_cycle_result[:20], 1):
    print(f"{rank:<6}{item['英雄名称']:<14}{item['皮肤总数']:<10}{item['平均周期(天)']:<16}{item['平均周期(月)']:<16}{item['最短间隔(天)']:<12}")
print("-" * 80)
print(f"统计范围：共 {len(update_cycle_result)} 位英雄拥有2款及以上皮肤")
print(f"全英雄平均更新周期：{round(all_avg_days)} 天，约 {round(all_avg_days/30,1)} 个月")
print("=" * 80)

top20 = update_cycle_result[:20][::-1]
hero_names = [x["英雄名称"] for x in top20]
skin_counts = [x["皮肤总数"] for x in top20]
avg_days = [x["平均周期(天)"] for x in top20]
avg_months = [x["平均周期(月)"] for x in top20]

plt.figure(figsize=(10, 8), dpi=100)
colors = ["#E67E22"] * 17 + ["#C0392B"] * 3
bars = plt.barh(hero_names, avg_days, color=colors, edgecolor='white')

plt.axvline(
    x=all_avg_days,
    color="#2C3E50",
    linestyle="--",
    linewidth=1.5,
    label=f"全英雄平均周期 {round(all_avg_days)}天"
)

for bar, days, months, count in zip(bars, avg_days, avg_months, skin_counts):
    plt.text(
        bar.get_width() + 3,
        bar.get_y() + bar.get_height()/2,
        f"{days}天 / {months}月 ({count}款)",
        va='center',
        fontsize=9
    )

plt.title("英雄皮肤更新频率 Top20（周期越短更新越快）", fontsize=14, pad=20)
plt.xlabel("平均更新周期（天）", fontsize=11)
plt.ylabel("英雄名称", fontsize=11)
plt.legend(loc="lower right")
plt.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()


plt.savefig("英雄更新频率排行.png", dpi=300, bbox_inches='tight')
plt.show()
