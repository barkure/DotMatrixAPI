from fastapi import FastAPI, Query
import uvicorn
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fonts.SimSun.SimSun32x32 import font as SimSun32x32


app = FastAPI()

# 允许所有主机
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)




fonts = {
    "SimSun32x32": SimSun32x32,
}


# 获取字体中字符的大小
def get_char_size(font):
    first_key = next(iter(font))
    char_data_list = font[first_key]
    if len(char_data_list) == 256:
        char_width = 32
        char_height = 64
    elif len(char_data_list) == 144:
        char_width = 24  
        char_height = 48
    elif len(char_data_list) == 128:
        char_width = 32
        char_height = 32
    elif len(char_data_list) == 72:
        char_width = 24
        char_height = 24
    elif len(char_data_list) == 64:
        char_width = 16
        char_height = 32
    elif len(char_data_list) == 32:
        char_width = 16
        char_height = 16
    elif len(char_data_list) == 16:
        char_width = 8
        char_height = 16
    else:
        raise ValueError("字体数据长度错误")
    return char_width, char_height


# 获取直接可以用于显示的字节数组
# color: 文字颜色，十进制数字，颜色格式为 RGB565，例如蓝色为 31，白色为 65535
# background: 背景颜色，同上
@app.get("/bytes")
def get_bytes(font: str = Query, text: str = Query(...), color: int = Query(65535), background: int = Query(0)):
    font = fonts[font]
    # 获得字体中字符大小
    char_width, char_height = get_char_size(font)
    # 获得字符数目
    char_num = len(text)
    # 获得所有字符的数据
    char_data_list = [font[char] if char in font else font['？'] for char in text]
    # 最终的数据
    bytes_list = []
    # 得到每行的比特数据
    for i in range(char_height):
        row_data = []
        for char_data in char_data_list:
            for k in range(char_width // 8):
                item = bin(char_data[i + k * char_height])[2:].zfill(8)
                row_data.append(item)

        # 将所有行数据拼接成一个字符串
        row_data_str = ''.join(row_data)

        # 将本行的数据转换为字节
        for char in row_data_str:
            pixel_color = color if char == '1' else background
            # 将单个像素点的颜色（RGB565）转换为两个数字（256进制）存入列表
            # 将高字节添加到列表中
            bytes_list.append((pixel_color >> 8) & 0xFF)
            # 将低字节添加到列表中
            bytes_list.append(pixel_color & 0xFF)

    return {
        "char_width": char_width,
        "char_height": char_height,
        "char_num": char_num,
        "byte_list": bytes_list
    }


# 启动服务
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
