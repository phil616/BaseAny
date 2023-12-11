

def read_cp():
    with open("bacl.txt",'r',encoding='utf8') as f:
        data = f.read()
    return data
char_string = read_cp()
# 假设我们有3500个汉字的字符串
hanzi_string = read_cp()

# 创建映射表
map_bin_to_hanzi = {}
for i in range(0, len(hanzi_string)):
    binary_representation = format(i, '012b')  # 将索引转换为12位二进制
    map_bin_to_hanzi[binary_representation] = hanzi_string[i]

# 给定128位的数据（16字节）
data_128bit = "9AFC3D4E7891BCD5E6F7A8C9DEADBEEF"

# 将128位数据转换为二进制表示
data_bin = bin(int(data_128bit, 16))[2:].zfill(128)

# 将二进制数据分割为12位的小段
segments = [data_bin[i:i+12] for i in range(0, len(data_bin), 12)]

# 使用映射表将二进制段转换为汉字
hanzi_representation = ""
for segment in segments:
    if len(segment) < 12:
        # 如果不足12位，右侧填充0
        segment = segment.ljust(12, '0')
    hanzi = map_bin_to_hanzi[segment]
    hanzi_representation += hanzi

# 输出结果
print(hanzi_representation)
