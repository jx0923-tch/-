import requests
import csv
import json

# 王者荣耀皮肤数据接口地址
url = "https://pvp.qq.com/zlkdatasys/heroskinlist.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://pvp.qq.com/"
}

# 1. 请求并解析原始JSON
response = requests.get(url, headers=headers, timeout=10)
response.encoding = "utf-8"
full_data = response.json()

# 2. 提取真实的皮肤列表数组
skin_list = full_data["pflb20_3469"]
print(f"接口实际返回皮肤数量：{len(skin_list)}")

# 3. 字段重命名映射
field_map = {
    "pfidlb_3934": "皮肤ID",
    "pfmclb_7523": "皮肤名称",
    "yxmclb_9965": "英雄名称",
    "pfpzlb_3289": "皮肤品质",
    "sxsjlb_1516": "上线时间",
    "yjhjsl_5003": "皮肤简介",
    "hqfs_8609": "获取方式",
    "yxtxlb_8443": "宣传大图URL",
    "fmlb_4536": "封面图URL",
    "fmb1lb_5300": "Banner图URL",
    "pcljlb_9272": "PC详情页",
    "mdljlb_1924": "移动端详情页",
    "spvidl_6663": "视频ID",
    "pfgift_4455": "动态封面URL",
    "pfbqlb_1811": "分类编号"
}

#4.初步清洗数据
clean_data = []
for skin in skin_list:
    clean_skin = {}
    for en_key, cn_key in field_map.items():

        clean_skin[cn_key] = skin.get(en_key, "")
    clean_data.append(clean_skin)

# 5. 使用csv模块保存为CSV文件
output_file = "王者荣耀皮肤数据.csv"
csv_headers = list(field_map.values())

with open(output_file, "w", encoding="utf-8-sig", newline="") as f:

    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()       # 写入表头行
    writer.writerows(clean_data)  # 批量写入所有皮肤数据

print(f"数据已保存到 {output_file}，共 {len(clean_data)} 条记录")



