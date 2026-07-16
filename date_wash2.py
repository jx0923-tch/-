import csv

input_file = "王者荣耀皮肤数据_.csv"
output_file = "王者荣耀皮肤数据__.csv"
keep_columns = ["英雄名称", "皮肤名称", "皮肤品质", "上线时间", "获取方式"]
fill_value = "无官方数据"

# 统计变量
replace_count = 0
total_rows = 0

# 读取原文件 + 处理数据
processed_data = []
with open(input_file, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:

        new_row = {col: row[col].strip() for col in keep_columns}

        if new_row["获取方式"] == "":
            new_row["获取方式"] = fill_value
            replace_count += 1

        processed_data.append(new_row)
        total_rows += 1

# 写入新文件
with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=keep_columns)
    writer.writeheader()  # 写入表头
    writer.writerows(processed_data)

# 输出处理结果
print(f"处理完成，共处理 {total_rows} 条数据")
print(f"已保留列：{keep_columns}")
print(f"获取方式空值填充数量：{replace_count} 条")
print(f"新文件已保存为：{output_file}")
