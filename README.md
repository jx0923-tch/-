代码架构
wzry_skin_analysis/
├── crawl_wzry_skin.py          # 1. 爬虫采集模块
├── data_standardize.py         # 2. 数据标准化模块
├── data_analysis.py            # 3. 统计分析模块
├── data_visualization.py       # 4. 可视化模块
├── data/                       # 数据文件存放目录
│   ├── first_wzry_skin_data.xls    # 爬虫输出的原始数据
│   └── 王者荣耀皮肤数据_标准化版.csv  # 清洗后的主分析数据
└── pic/                        # 可视化图表输出目录
    ├── 基础品质分布.png             # 皮肤品质档位数量分布柱状图
    ├── 月度节点投放规律.png         # 月度上线量/限定占比/高端占比多指标趋势图
    └── 英雄皮肤更新频率排行.png     # 皮肤更新周期Top20横向条形图
