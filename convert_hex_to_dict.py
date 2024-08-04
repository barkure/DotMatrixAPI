
def parse_hex_file(file_path):
    hex_dict = {}
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
    
    for line in lines:
        if '#' in line:
            hex_data, comment = line.split('#')
            hex_values = [int(val, 16) for val in hex_data.strip().split(',') if val]  # 去掉空字符串
            chinese_char = comment[0]
            hex_dict[chinese_char] = hex_values
     
    return hex_dict

def save_dict_to_file(data_dict, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("font = {\n")
        for key, value in data_dict.items():
            hex_value_str = [f"0x{val:02X}" for val in value]  # 转换为十六进制表示
            file.write(f"    '{key}': [{', '.join(hex_value_str)}],\n")
        file.write("}\n")

# 示例调用
file_path = '3.TXT'
output_path = file_path.replace('.TXT', '.py')
hex_dict = parse_hex_file(file_path)
save_dict_to_file(hex_dict, output_path)
print(f"字典已保存到 {output_path}")