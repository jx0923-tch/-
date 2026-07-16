import csv
from collections import Counter


INPUT_FILE = "王者荣耀皮肤数据__1.csv"
OUTPUT_FILE = "王者荣耀皮肤数据_标准化版.csv"

ENABLE_YEAR_FILTER = False
START_YEAR = 2024
END_YEAR = 2025

# 获取方式分类匹配规则（关键词匹配，优先级从上到下）
GET_TYPE_RULES = [
    ("限定返场类", ["返场"]),
    ("抽奖类", ["夺宝", "祈愿", "抽奖", "积分", "荣耀典藏", "无双"]),
    ("战令类", ["战令"]),
    ("免费福利类", ["赛季", "免费", "活动", "碎片", "签到", "兑换", "任务"]),
    ("直售类", ["点券", "商城", "直售", "首周", "购买"])
]
# 付费层级对应规则
PAY_LEVEL_MAP = {
    "荣耀典藏": "高端付费",
    "无双": "高端付费",
    "珍品传说": "高端付费",
    "传说": "高端付费",
    "史诗": "中端付费",
    "勇者": "入门付费",
    "伴生": "入门付费"
}



processed_data = []
# 统计变量
total_raw = 0
invalid_date_count = 0
replace_null_count = 0

# 1. 读取原始数据并逐行处理
with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_raw += 1
        clean_row = {
            "英雄名称": row["英雄名称"].strip(),
            "皮肤名称": row["皮肤名称"].strip(),
            "原始品质": row["皮肤品质"].strip(),
            "原始上线时间": row["上线时间"].strip(),
            "原始获取方式": row["获取方式"].strip()
        }
        if clean_row["原始获取方式"] == "":
            clean_row["原始获取方式"] = "无官方数据"
            replace_null_count += 1

        quality_raw = clean_row["原始品质"]
        is_limited = "是" if "限定" in quality_raw else "否"
        # 剔除“限定”字样，得到基础品质
        base_quality = quality_raw.replace("限定", "").strip()
        clean_row["基础品质"] = base_quality
        clean_row["是否限定"] = is_limited
--
        get_type_raw = clean_row["原始获取方式"]
        final_type = "无官方数据"
        for type_name, keywords in GET_TYPE_RULES:
            if any(keyword in get_type_raw for keyword in keywords):
                final_type = type_name
                break
        clean_row["获取方式分类"] = final_type

        date_str = clean_row["原始上线时间"]
        year = ""
        month = ""
        date_valid = "否"
        # 适配8位数字日期格式（如20240125）
        if len(date_str) == 8 and date_str.isdigit():
            year = date_str[:4]
            month = date_str[4:6]
            # 校验日期合理性
            if 1 <= int(month) <= 12 and 2015 <= int(year) <= 2030:
                date_valid = "是"
            else:
                invalid_date_count += 1
        else:
            invalid_date_count += 1
        clean_row["上线年份"] = year
        clean_row["上线月份"] = month
        clean_row["日期是否有效"] = date_valid

        # ---------- 步骤5：衍生付费层级标签 ----------
        clean_row["付费层级"] = PAY_LEVEL_MAP.get(base_quality, "免费/其他")

        # ---------- 可选：近两年数据过滤 ----------
        if ENABLE_YEAR_FILTER and date_valid == "是":
            if not (START_YEAR <= int(year) <= END_YEAR):
                continue

        processed_data.append(clean_row)

output_columns = [
    "英雄名称", "皮肤名称",
    "基础品质", "是否限定", "原始品质",
    "获取方式分类", "原始获取方式",
    "上线年份", "上线月份", "日期是否有效", "原始上线时间",
    "付费层级"
]

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=output_columns)
    writer.writeheader()
    writer.writerows(processed_data)

print("=" * 50)
print("【数据标准化处理完成报告】")
print("=" * 50)
print(f"原始数据总条数：{total_raw}")
print(f"处理后有效数据条数：{len(processed_data)}")
print(f"获取方式空值填充数量：{replace_null_count} 条")
print(f"日期格式异常数量：{invalid_date_count} 条")
print(f"输出文件：{OUTPUT_FILE}")
print("-" * 50)

quality_counter = Counter([row["基础品质"] for row in processed_data])
get_type_counter = Counter([row["获取方式分类"] for row in processed_data])
limited_count = sum(1 for row in processed_data if row["是否限定"] == "是")

print(f"【基础品质分布预览】")
for q, cnt in sorted(quality_counter.items(), key=lambda x:x[1], reverse=True):
    print(f"  {q}：{cnt} 款")
print(f"\n【获取方式分类预览】")
for t, cnt in sorted(get_type_counter.items(), key=lambda x:x[1], reverse=True):
    print(f"  {t}：{cnt} 款")
print(f"\n限定皮肤总数量：{limited_count} 款，占比 {limited_count/len(processed_data)*100:.2f}%")
print("=" * 50)
