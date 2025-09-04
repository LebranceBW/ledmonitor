# /// script
# requires-python = ">=3.13"
# dependencies = [
# ]
# ///

"""
小屏幕 LCD 显示编码"""
small_codes = {
    "0": 0xFA,
    "1": 0x60,
    "2": 0xD6,
    "3": 0xF4,
    "4": 0x6C,
    "5": 0xBC,
    "6": 0xBE,
    "7": 0xE0,
    "8": 0xFE,
    "9": 0xFC,
    "A": 0xEE,
    "P": 0xCE,
    "C": 0x9A,
    "-": 0x04,
    "_": 0x10,
}

"""
    大数字LCD 显示编码
"""
big_codes = {
    "0": 0xF5,
    "1": 0x60,
    "2": 0xB6,
    "3": 0xF2,
    "4": 0x63,
    "5": 0xD3,
    "6": 0xD7,
    "7": 0x70,
    "8": 0xF7,
    "9": 0xF3,
    "A": 0x77,
    "P": 0x37,
    "C": 0x95,
    "-": 0x02,
    "_": 0x80,
    "10": 0xFD,
    "11": 0x68,
    "12": 0xBE,
    "13": 0xFA,
    "14": 0x6B,
    "15": 0xDB,
    "16": 0xDF,
    "17": 0x78,
    "18": 0xFF,
    "19": 0xFB,
}


def encode_lcd_display(bignum: float, smallnum: int, smail: bool = False) -> bytes:
    """
    将 0~199.9 的数字转换为 LCD 显示编码为 bytes，小端序，填充为 6 bytes。
    输出格式：小数位(带点) -> 个位 -> 十位 -> 百位 -> _ -> _

    Args:
        bignum: 大数字 (0~199.9)
        smallnum: 小数字
        smail: 是否显示小数点

    Returns:
        LCD显示编码的bytes

    Raises:
        ValueError: 当输入参数超出有效范围时
    """
    # 输入验证
    if not 0 <= bignum <= 199.9:
        raise ValueError("bignum must be between 0 and 199.9")

    if not 0 <= smallnum <= 99:
        raise ValueError("smallnum must be between 0 and 99")

    bigcodes = encode_big_num(bignum)
    smallcodes = encode_small_num(smallnum)
    appendix = 0x0C | (0x10 if smail else 0x00)
    return bytes([0x60, *smallcodes, appendix, *bigcodes])


def encode_small_num(num: int) -> bytes:
    """
     编码小数字为LCD显示格式

        7
      ┌───┐
    3 │   │ 6
      │ 2 │
      └───┘
    1 │   │ 5
      │ 4 │     0%
      └───┘
     小数字LCD 显示编码

     Args:
         num: 需要编码的数字 (0-99)

     Returns:
         编码后的bytes

     Raises:
         ValueError: 当输入参数超出有效范围时
    """
    # 输入验证
    if not 0 <= num <= 99:
        raise ValueError("num must be between 0 and 99")

    num = int(num % 100)
    # 拆解整数部分为十、个位
    ones = str(num % 10)
    tens = str((num // 10) % 10)

    return bytes([small_codes[ones], small_codes[tens]])


def encode_big_num(bignum: float) -> bytes:
    """
        编码大数字为LCD显示格式

           4
         ┌───┐
       0 │   │ 5
         │ 1 │
         └───┘
       2 │   │ 6
    3p   │ 7 │
         └───┘
        大数字LCD 显示编码

        Args:
            bignum: 需要编码的大数字 (0~199.9)

        Returns:
            编码后的bytes，按照小数位(带点) -> 个位 -> 十位 -> 百位的顺序

        Raises:
            ValueError: 当输入参数超出有效范围时
    """
    # 输入验证
    if not 0 <= bignum <= 199.9:
        raise ValueError("bignum must be between 0 and 199.9")

    bignum = round(bignum, 1)
    integer_part = int(bignum)
    decimal_part = str(int(round((bignum - integer_part) * 10)))  # 0~9
    ones = str(integer_part % 10)
    highs = str((integer_part // 10) % 20)

    return bytes([big_codes[decimal_part] | 0x08, big_codes[ones], big_codes[highs]])


if __name__ == "__main__":
    print(encode_lcd_display(123.4, 55).hex())
