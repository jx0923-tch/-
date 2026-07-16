import csv


input_file = "王者荣耀皮肤数据.csv"
output_file = "王者荣耀皮肤数据_.csv"
keep_rows = 156
# 读取并截取前N行写入新文件
with open(input_file, "r", encoding="utf-8-sig", newline="") as f_in:
    reader = csv.reader(f_in)
    rows = []
    for idx, row in enumerate(reader):
        if idx >= keep_rows:
            break
        rows.append(row)

# 写入新文件
with open(output_file, "w", encoding="utf-8-sig", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerows(rows)

print(f"处理完成，已保留前 {len(rows)} 行数据，新文件已保存为：{output_file}")

