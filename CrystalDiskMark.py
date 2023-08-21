import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set(style="whitegrid")

mark_data = pd.read_excel("CrystalDiskMark.xlsx",
                          sheet_name="Mark", header=0, index_col=0)

# info_data = pd.read_excel("CrystalDiskMark.xlsx",sheet_name="Info")


print(mark_data)

# 绘制两个图，第一张是SEQ，第二张是RND
# 首先，将SEQ和RND的数据分别取出来
# SEQ的数据是column名称以SEQ开头的数据
# RND的数据是column名称以RND开头的数据
seq_data = mark_data.filter(regex="SEQ")
seq_data.columns = seq_data.columns.str.replace("SEQ ", "")
rnd_data = mark_data.filter(regex="RND")
rnd_data.columns = rnd_data.columns.str.replace("RND ", "")


def group_bar_draw(data, title):
    # 首先要先更改表格的结构
    data = data.stack().reset_index()
    data.columns = ["Disk", "Subject", "Speed"]
    # 绘制图形
    plt.figure()
    g = sns.catplot(x="Disk", y="Speed", hue="Subject", data=data,
                    kind="bar", legend=False, height=6, aspect=2.5)
    g.despine(left=True)
    g.set_ylabels("Speed (MB/s)", fontsize=12)
    g.set_xlabels("Disk Info", fontsize=12)
    plt.xticks(rotation=0, wrap=True)
    # 图内显示数值
    for p in g.ax.patches:
        g.ax.annotate("%.0f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()), ha="center",
                      va="center", fontsize=10, color="gray", xytext=(0, 10), textcoords="offset points")
    # 图内图例,字体大小
    g.ax.legend(ncol=1, fancybox=True, shadow=True, fontsize=12)
    g.fig.suptitle(title, fontsize=18)
    plt.savefig(title + ".png", dpi=600)


group_bar_draw(seq_data, "Sequential Read-Write Speed")
group_bar_draw(rnd_data, "Random Read-Write Speed")
