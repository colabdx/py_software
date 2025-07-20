import tkinter as tk
import random
import pygame
from pygame import joystick
import datetime
import json
import os

# 初始化pygame和手柄
pygame.init()
joystick.init()
if joystick.get_count() > 0:
    controller = joystick.Joystick(0)
    controller.init()

# 定义项目列表
items = [
    "五大本质 氢", "本质 氦", "通用种子 锂", "斯通 铍", "硼砂 硼", "碳",
    "硝石 氮", "氧气 氧", "混合物 氟", "精神 氖", "素迪姆 钠", "镁",
    "明矾 铝", "退火 硅", "磷", "硫磺 硫", "盐 氯", "氨水 氩", "钾",
    "查了 钙", "莱姆 钪", "沙 钛", "玻璃 钒", "黏土 铬", "锈 锰", "铁",
    "钴", "镍", "铜", "锌", "烧明矾 镓", "黄铜 锗", "砷", "砷硫 硒",
    "海盐 溴", "岩盐 氪", "醋 铷", "蒸馏醋 锶", "生石灰 钇", "碱石灰 镐",
    "木材 铌", "烟雾 钼", "余烬 锝", "钢 钌", "马加西特 铑", "铜绿 钯",
    "银", "辰砂 镉", "汽油罐 铟", "锡", "锑", "硫磺酸 碲", "东方水 碘",
    "王水 氙", "油 铯", "硫酸油 钡", "硫酸 镧系", "火 镧", "水 铈",
    "星座标记与工艺 镨", "白羊座 煅烧 钕", "金牛座 凝固 钷", "双子座 固着 钐",
    "巨蟹座 解决方案 铕", "狮子座 消化 钆", "处女座 蒸馏 铽", "天秤座 升华 镝",
    "天蝎座 分离 钬", "射手座 蜡化 铒", "魔羯座 发酵 铥", "水瓶座 乘法 镱",
    "双鱼座 投影 镥", "蛋壳 铪", "小体 钽", "灯芯 钨", "牛脂 铼", "肥皂 锇",
    "肥皂 铱", "铂", "金色的 金", "水星 汞", "精神融合 铊", "草地 铅",
    "铋", "雄黄 钋", "阿卡维纳 砹", "水浴 氡", "反驳 钫", "坩埚 镭",
    "空气 锕", "地球 钍", "其他工艺 镤", "白羊宫 组成 铀", "金牛宫 腐烂 镎", "双子宫 煮 钚",
    "巨蟹宫 解决 镅", "狮子宫 合并 锔", "处女宫 拿 锫", "天秤宫 净化 锎", "天蝎宫 蒸馏 锿", "射手宫 筛选 镄",
    "摩羯宫 沉淀物 钔", "水瓶宫 升华 锘", "双鱼宫 粉碎 铹", "品脱 𬬻", "顾虑 罕", "微量",
    "盎司", "英镑", "小时"
]

# NOTE: 价格数据存储文件路径
PRICE_DATA_FILE = "item_prices.json"

def load_price_data():
    """加载或初始化价格数据"""
    if os.path.exists(PRICE_DATA_FILE):
        with open(PRICE_DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        # NOTE: 初始化所有物品价格，范围1-200
        return {item: random.randint(1, 200) for item in items}

def save_price_data(prices):
    """保存价格数据"""
    with open(PRICE_DATA_FILE, 'w') as f:
        json.dump(prices, f)

def get_daily_price(item, prices):
    """获取每日价格，考虑10%以内的波动"""
    today = datetime.date.today().isoformat()
    last_update = prices.get(f"{item}_last_update")
    
    # NOTE: 保存原始价格用于计算变动幅度
    original_price = prices[item]
    
    if last_update != today:
        # NOTE: 每日更新价格，波动范围在10%以内
        base_price = prices[item]
        fluctuation = random.uniform(-0.1, 0.1)
        new_price = round(base_price * (1 + fluctuation))
        new_price = max(1, min(200, new_price))  # 确保价格在1-200之间
        
        # 更新价格和最后更新时间
        prices[item] = new_price
        prices[f"{item}_last_update"] = today
        prices[f"{item}_original_price"] = original_price  # 存储原始价格
        save_price_data(prices)
    
    return prices[item], prices.get(f"{item}_original_price", prices[item])

# 加载价格数据
item_prices = load_price_data()

# 创建主窗口
root = tk.Tk()
root.title("Random Item Selector")

# 创建一个标签用于显示所选项目
selected_item_label = tk.Label(root, text="", font=("微软雅黑", 16))
selected_item_label.pack(pady=20)

# NOTE: 新增价格显示标签
price_label = tk.Label(root, text="", font=("微软雅黑", 12))
price_label.pack(pady=5)

# NOTE: 新增价格变动幅度显示标签
change_label = tk.Label(root, text="", font=("微软雅黑", 10))
change_label.pack(pady=2)

# NOTE: 新增搜索框和搜索按钮
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, font=("微软雅黑", 12))
search_entry.pack(side=tk.LEFT, padx=5)

def search_item():
    """搜索并显示匹配的元素价格信息"""
    search_text = search_entry.get().strip().lower()
    if not search_text:
        return
    
    # NOTE: 查找包含搜索文本的元素
    matched_items = [item for item in items if search_text in item.lower()]
    if not matched_items:
        selected_item_label.config(text="未找到匹配元素")
        price_label.config(text="")
        change_label.config(text="")
        return
    
    # NOTE: 显示第一个匹配项的价格信息
    selected_item = matched_items[0]
    current_price, original_price = get_daily_price(selected_item, item_prices)
    price_change = ((current_price - original_price) / original_price) * 100
    change_text = f"{price_change:+.2f}%"
    
    selected_item_label.config(text=selected_item)
    price_label.config(text=f"价格: ¥{current_price}")
    change_label.config(text=f"变动: {change_text}")

search_button = tk.Button(
    search_frame, 
    text="搜索", 
    command=search_item,
    font=("微软雅黑", 12)
)
search_button.pack(side=tk.LEFT)

def select_item():
    """选择随机项目并显示其价格和变动幅度"""
    selected_item = random.choice(items)
    current_price, original_price = get_daily_price(selected_item, item_prices)
    
    # 计算价格变动百分比
    price_change = ((current_price - original_price) / original_price) * 100
    change_text = f"{price_change:+.2f}%"  # 格式化为带符号的百分比
    
    selected_item_label.config(text=selected_item)
    price_label.config(text=f"价格: ¥{current_price}")
    # NOTE: 显示价格变动百分比
    change_label.config(text=f"变动: {change_text}")

# 创建一个按钮用于触发选择事件
select_button = tk.Button(root, text="Select an Item", command=select_item)
select_button.pack(pady=10)

# NOTE: 修改为单行显示所有物品标签，用逗号分隔
items_label = tk.Label(
    root, 
    text=", ".join(items), 
    font=("微软雅黑", 10), 
    wraplength=800,
    justify=tk.LEFT  # 确保左对齐
)
items_label.pack(pady=10)

def check_controller():
    """检查手柄输入"""
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            # A按钮(0)或B按钮(1)按下时触发选择
            if event.button in [0, 1]:
                select_item()
    root.after(50, check_controller)  # 每50ms检查一次手柄输入

# 启动手柄检测
root.after(50, check_controller)

# 运行主循环
root.mainloop()
