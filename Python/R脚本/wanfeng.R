# 数据准备
info <- c(1, 2, 4, 8)

# 命名
names <- c("Google", "Runoob", "Taobao", "Weibo")

# 涂色（可选）
cols <- c("#ED1C24", "#22B14C", "#FFC90E", "#3f48CC")
# 计算百分比
piepercent <- paste(round(100 * info / sum(info)), "%")
# 绘图
pie(info, labels = piepercent, main = "网站分析", col = cols, family = "GB1")
# 添加颜色样本标注
legend("topright", names, cex = 0.8, fill = cols)