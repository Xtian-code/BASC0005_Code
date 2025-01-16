import pandas as pd
import matplotlib.pyplot as plt

# 加载上传的 Excel 文件
file_path = 'reviewscore.xlsx'
data = pd.ExcelFile(file_path)

# 读取第一个工作表的数据
df = data.parse('Sheet1')

# 将数据从宽格式转换为长格式，方便绘制箱线图
df_long = df.melt(var_name="genre", value_name="reviewscore", value_vars=["Independent", "Casual", "Action"])

# 清理数据：移除包含 NaN 值的行
df_long = df_long.dropna()

# 绘制箱线图
plt.figure(figsize=(8, 6))
df_long.boxplot(column="reviewscore", by="genre", grid=False)
plt.title("Review Score Comparison by Genre")
plt.suptitle("")  # 移除默认的副标题
plt.xlabel("Genre")
plt.ylabel("Review Score")
plt.show()