import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def draw_graph():
    # 读取 CSV 文件
    df = pd.read_csv('results.csv')

    # 按 userName 和 Time 分组，并对 Score 和 TimeUsed 进行求和
    grouped = df.groupby(['Time', 'userName']).agg({'Score': 'sum', 'TimeUsed': 'sum'}).reset_index()

    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 创建一个新的图形
    plt.figure(figsize=(14, 6))

    # 绘制 Score 图表
    plt.subplot(1, 2, 1)
    for date, group in grouped.groupby('Time'):
        plt.bar(group['userName'], group['Score'], label=group['userName'].iloc[0])
        # 标注数值
        for index, row in group.iterrows():
            plt.text(index, row['Score'], str(row['Score']), ha='center', va='bottom')
    plt.title(f'Cumulative Score by User on {grouped["Time"].iloc[0]} (Generated on {current_date})')
    plt.xlabel('User Name')
    plt.ylabel('Cumulative Score')
    #plt.legend(title='User Name')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 绘制 TimeUsed 图表
    plt.subplot(1, 2, 2)
    for date, group in grouped.groupby('Time'):
        plt.bar(group['userName'], group['TimeUsed'], label=group['userName'].iloc[0])
        # 标注数值
        for index, row in group.iterrows():
            plt.text(index, row['TimeUsed'], f'{row["TimeUsed"]:.2f}', ha='center', va='bottom')
    plt.title(f'Cumulative Time Used by User on {grouped["Time"].iloc[0]} (Generated on {current_date})')
    plt.xlabel('User Name')
    plt.ylabel('Cumulative Time Used (seconds)')
    #plt.legend(title='User Name')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存图表为图片
    plt.savefig('cumulative_results.png')

    # 显示图形
    #plt.show()