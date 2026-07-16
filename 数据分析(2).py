import csv
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import numpy as np


file_path = "王者荣耀皮肤数据_标准化版.csv"

# 交叉统计：获取方式 × 付费层级
channel_pay = defaultdict(Counter)
with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["日期是否有效"] == "是":
            channel = row["获取方式分类"]
            pay_level = row["付费层级"]
            channel_pay[channel][pay_level] += 1

pay_levels = ["高端付费", "中端付费", "入门付费", "免费/其他"]
# 渠道按皮肤总数量降序排序
channels = sorted(channel_pay.keys(), key=lambda x: sum(channel_pay[x].values()), reverse=True)

# 转换为百分比数据（每个渠道内部占比，总和100%）
percent_data = []
for level in pay_levels:
    level_percents = []
    for ch in channels:
        ch_total = sum(channel_pay[ch].values())
        cnt = channel_pay[ch].get(level, 0)
        percent = cnt / ch_total * 100 if ch_total > 0 else 0
        level_percents.append(percent)
    percent_data.append(level_percents)

plt.figure(figsize=(10, 6), dpi=100)

colors = ["#C0392B", "#E67E22", "#F1C40F", "#27AE60"]

# 逐层绘制堆叠柱
bottom = np.zeros(len(channels))
for i in range(len(pay_levels)):
    bars = plt.bar(
        channels,
        percent_data[i],
        bottom=bottom,
        color=colors[i],
        label=pay_levels[i],
        edgecolor='white'  # 柱子分段加白边
    )
    for j in range(len(channels)):
        if percent_data[i][j] > 3:
            plt.text(
                j,
                bottom[j] + percent_data[i][j] / 2,
                f"{percent_data[i][j]:.1f}%",
                ha='center',
                va='center',
                fontsize=9,
                color='white' if i < 2 else 'black'
            )
    bottom += percent_data[i]

plt.title("各获取渠道的付费层级结构对比", fontsize=14, pad=20)
plt.ylabel("占比（%）", fontsize=11)
plt.xlabel("获取方式分类", fontsize=11)
plt.ylim(0, 100)
plt.yticks(range(0, 101, 20), [f"{x}%" for x in range(0, 101, 20)])
plt.legend(loc="upper right", bbox_to_anchor=(1.15, 1))
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()

plt.savefig("获取方式付费层级堆叠图.png", dpi=300, bbox_inches='tight')
plt.show()
