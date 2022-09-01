from random import randint
# from time import sleep

import pool

# 一系列要用到的变量
result = []  # 储存抽卡结果
dic = {}  # 定义空字典以共享引用卡池的字典
six, five, four, three = 0, 0, 0, 0  # 用于判断各个星级出现的总数
five_new = True  # 判断首次五星保底
first_recharge = False  # 判断首充
counter1 = 1
counter2 = 0
n = 0  # 用于判断保底次数
# 初始化至纯源石数和合成玉数，选择卡池，展示概率
print("欢迎来到Allen寻访模拟器！\n合成玉不足时，至纯源石会自动转换成合成玉！(1至纯源石=180合成玉)")
while 1:
    try:
        stone = input('请输入初始至纯源石数：')
        stone = int(stone)
        jade = input('请输入初始合成玉数：')
        jade = int(jade)
        break
    except ValueError:
        print('请正确输入数值！')
show_pools = "请选择卡池:\n"  # 卡池展示与选择
for i in pool.pools:
    show_pools += f'{counter1}.{i}\n'
    counter1 += 1
while 1:
    tip = input('\n' + show_pools)
    try:
        dic = eval(f'pool.{pool.pools[int(tip) - 1]}')
        break
    except:
        print("请正确选择卡池!")
# 将六星和五星分别整理到一个集合中,以便展示结果时使用
six_up_result = set(dic['six_up'])
six_up_result.remove(0)
five_up_result = set(dic['five_up'])
five_up_result.remove(0)
six_stars_result = set(dic['six_stars']) | six_up_result
five_stars_result = set(dic['five_stars']) | five_up_result
# 打印卡池
print(f"已选择卡池：{pool.pools[int(tip) - 1]}\n★★★★★★ 六星(2%)：", end='')
for i in six_stars_result:
    print(i, end=',')
print("\n★★★★★ 五星(8%)：", end='')
for i in five_stars_result:
    print(i, end=',')
print("\n★★★★ 四星(50%)：", end='')
for i in dic['four_stars']:
    print(i, end=',')
print("\n★★★ 三星(40%)：", end='')
for i in dic['three_stars']:
    print(i, end=',')
print(f"\n\n描述:{dic['description']}\n")


def one():
    """判断抽卡结果"""
    global six, five, four, three, n, five_new, counter2  # 定义全局变量
    # sleep(0.5)
    n += 1
    if n <= 50:
        num = 50
    else:
        num = n  # 判断抽卡次数
    if five_new:
        counter2 += 1  # 判断首次五星保底
    if five_new is True and counter2 == 10:
        new_operator = dic['five_up'][randint(0, len(dic['five_up'])) - 1]
        if new_operator != 0:
            result.append(new_operator)
            print(f'★★★★★ {new_operator}')
        else:
            new_operator = dic['five_stars'][randint(0, len(dic['five_stars'])) - 1]
            result.append(new_operator)
            print(f'★★★★★ {new_operator}')
        five += 1
        five_new = False
    else:
        b = randint(1, 1000)
        if 1 <= b <= 20 + (num - 50) * 20:  # 六星
            new_operator = dic['six_up'][randint(0, len(dic['six_up'])) - 1]
            if new_operator != 0:
                result.append(new_operator)
                print(f'★★★★★★ {new_operator}')
            else:
                new_operator = dic['six_stars'][randint(0, len(dic['six_stars'])) - 1]
                result.append(new_operator)
                print(f'★★★★★★ {new_operator}')
            six += 1
            n = 0  # 重置抽卡次数
            five_new = False
        elif 921 <= b <= 1000:  # 五星
            new_operator = dic['five_up'][randint(0, len(dic['five_up'])) - 1]
            if new_operator != 0:
                result.append(new_operator)
                print(f'★★★★★ {new_operator}')
            else:
                new_operator = dic['five_stars'][randint(0, len(dic['five_stars'])) - 1]
                result.append(new_operator)
                print(f'★★★★★ {new_operator}')
            five += 1
            five_new = False
        elif 421 <= b <= 920:  # 四星
            new_operator = dic['four_stars'][randint(0, len(dic['four_stars'])) - 1]
            four += 1
            result.append(new_operator)
            print(f'★★★★ {new_operator}')
        else:  # 三星
            new_operator = dic['three_stars'][randint(0, len(dic['three_stars'])) - 1]
            three += 1
            result.append(new_operator)
            print(f'★★★ {new_operator}')


def ten():
    """十连"""
    for _ in range(10):
        one()


# 主程序部分
active = True
while active:
    a = input(f"\n至纯源石数：{stone} 合成玉数：{jade}\n输入1单抽，输入2十连:\n(输入'q'以退出)")
    while a == '1':
        if jade >= 600:  # 判断合成玉是否足够
            jade -= 600
            one()
            break
        else:  # 尝试将至纯源石转换成合成玉
            if stone >= 1:
                stone -= 1
                jade += 180
            else:  # 至纯源石不足
                break
    while a == '2':
        if jade >= 6000:  # 判断合成玉是否足够
            jade -= 6000
            ten()
            break
        else:
            if stone >= (6000 - jade) / 180:  # 尝试将至纯源石转换成合成玉
                if (6000 - jade) % 180 == 0:  # 当所需合成玉数能转换成整数颗至纯源石时
                    stone -= int((6000 - jade) / 180)
                    jade = 6000
                else:  # 当所需合成玉数不能转换成整数颗至纯源石时
                    stone -= int((6000 - jade) // 180 + 1)
                    jade += int(((6000 - jade) // 180 + 1) * 180)
            else:
                print('至纯源石不足！请单抽！')
                break
    if a == 'q':  # 退出主程序
        break
    while stone * 180 + jade < 600:  # 氪金系统
        tip = input(f'\n至纯源石数：{stone} 合成玉数：{jade}\n至纯源石不足，是否氪金？首充双倍！(￥648=130至纯源石)(y/n)')
        if tip == 'y':  # 确认氪金
            if not first_recharge:
                stone += 260
            else:
                stone += 130
            print('氪金成功！')
        if tip == 'n':  # 取消氪金并退出主程序
            active = False
            break
# 抽卡结果展示
print(f'\n抽卡数：{len(result)}')
# 打印抽卡结果
print("★★★★★★六星：", end="")
for i in six_stars_result:
    if i in result:  # 判断抽卡结果
        print(f"{i}:{(result.count(i))}", end=" ")
print(f"总数:{six}")

print("★★★★★五星：", end="")
for i in five_stars_result:
    if i in result:  # 判断抽卡结果
        print(f"{i}:{(result.count(i))}", end=" ")
print(f"总数:{five}")

print("★★★★四星：", end="")
for i in dic['four_stars']:
    if i in result:  # 判断抽卡结果
        print(f"{i}:{(result.count(i))}", end=" ")
print(f"总数:{four}")

print("★★★三星：", end="")
for i in dic['three_stars']:
    if i in result:  # 判断抽卡结果
        print(f"{i}:{(result.count(i))}", end=" ")
# 打印总览
print(f"总数:{three}\n消耗合成玉：{len(result) * 600}")
try:  # 防止抽卡数为零时报错
    luck = six / len(result)
except ZeroDivisionError:
    luck = 0.000
print(f"\n六星出货占比：{'%.3f' % luck}")
# if float(luck) > 0.03:
#     print("双黄出货全满潜")
# else:
#     print("醒来枕边泪点点")
# print('\n已退出模拟器！')

input("\n输入任意值以退出......")

