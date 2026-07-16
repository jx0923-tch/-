import csv
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 存放CSV数据
data = []

# 读取数据
with open("王者荣耀皮肤数据_清洗.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

print("皮肤总数：", len(data))


# 统计指定字段出现次数
def statistics(column):
    result = {}

    for row in data:
        value = row[column]

        if value in result:
            result[value] += 1
        else:
            result[value] = 1

    return result


# 绘制柱状图
def draw_bar(dic, title, xlabel, ylabel):

    names = list(dic.keys())
    counts = list(dic.values())

    plt.figure(figsize=(8, 5))
    plt.bar(names, counts)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # 在柱子顶部显示数量
    for i, value in enumerate(counts):
        plt.text(i, value + 0.3, str(value), ha="center")

    plt.tight_layout()
    plt.show()


# 绘制折线图
def draw_line(dic, title):

    x = sorted(dic.keys())
    y = []

    for item in x:
        y.append(dic[item])

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o")

    plt.title(title)
    plt.xlabel("年份")
    plt.ylabel("皮肤数量")

    plt.grid(True)

    plt.tight_layout()
    plt.show()


# 基础品质分析
quality = statistics("基础品质")

print("\n基础品质统计：")
for k, v in quality.items():
    print(k, v)

draw_bar(
    quality,
    "基础品质分布",
    "基础品质",
    "数量"
)


# 获取方式分析
method = statistics("获取方式分类")

print("\n获取方式分类统计：")
for k, v in method.items():
    print(k, v)

draw_bar(
    method,
    "获取方式分类统计",
    "获取方式",
    "数量"
)


# 付费层级分析
pay = statistics("付费层级")

print("\n付费层级统计：")
for k, v in pay.items():
    print(k, v)

draw_bar(
    pay,
    "付费层级统计",
    "付费层级",
    "数量"
)


# 上线年份分析
year = statistics("上线年份")

print("\n上线年份统计：")
for k, v in year.items():
    print(k, v)

draw_line(
    year,
    "上线年份变化趋势"
)