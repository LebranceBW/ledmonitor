# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pydantic",
# ]
# ///

from pydantic import BaseModel, field_validator
import struct
from typing import Optional
from config import DEFAULT_DISPLAY_CONFIG

class ExtData(BaseModel):
    """扩展数据显示配置"""
    enable: bool
    """是否启用扩展功能"""
    
    bignumb: float
    """大数字显示值（主显示屏）"""
    
    smalnumb: float
    """小数字显示值（副显示屏）"""
    
    smiley: int
    """表情符号选择 (0-7)
    0: 空白
    1: ^_^ 
    2: -∧-
    3: Δ△Δ
    4: (   )
    5: (^_^)
    6: (-∧-)
    7: (Δ△Δ)"""
    
    battery: bool
    """是否显示电池缺电图标"""
    
    percent: bool
    """是否显示百分比符号"""
    
    tmpsmb: int
    """温度符号选择 (0-7)
    0: 空白
    1: °Г
    2: -
    3: °F
    4: _
    5: °C
    6: = (默认)
    7: °E"""
    
    vtimed: int
    """显示有效时间 (秒), 范围 2-65535"""

    @field_validator("smiley", "tmpsmb")
    def clamp_3bit(cls, v: int) -> int:
        """确保3-bit字段值在0-7范围内"""
        return max(0, min(v, 7))

    @field_validator("vtimed")
    def clamp_vtimed(cls, v: int) -> int:
        """确保显示时间在有效范围内"""
        return max(2, min(v, 65535))

def build_blk(ext_data: ExtData, hwver_id: int = 10) -> Optional[bytes]:
    """构建blk字节数组用于发送扩展数据
    
    Args:
        ext_data: 扩展数据配置
        hwver_id: 硬件版本ID
    
    Returns:
        构建的字节数组或None（当未启用时）
    """
    if not ext_data.enable:
        return None

    # 验证输入参数
    if not isinstance(hwver_id, int) or hwver_id < 0:
        raise ValueError("hwver_id must be a non-negative integer")

    # 构建配置字节 (1 byte)
    if hwver_id in (9, 12):  # 特定硬件版本
        cfg = (ext_data.smiley << 5) | (ext_data.battery << 4) | (ext_data.tmpsmb << 1) | ext_data.percent
    else:  # 其他硬件版本
        cfg = (ext_data.smiley << 5) | (ext_data.percent << 4) | (ext_data.battery << 3) | ext_data.tmpsmb

    # 处理大数字（根据硬件版本使用不同缩放比例）
    if hwver_id in (9, 12):
        big = int(round(ext_data.bignumb * 100))
        big = max(0, min(big, 0xFFFFFFFF))
    else:
        big = int(round(ext_data.bignumb * 10))
        big = max(0, min(big, 0xFFFF))

    # 处理小数字（仅非9/12设备需要）
    if hwver_id in (9, 12):
        # 硬件版本9/12：无小数字字段
        return struct.pack("<BIBH", 0x22, big, ext_data.vtimed, cfg)
    else:
        # 特定设备(CGG1 & CGDK2)需要乘以10
        if hwver_id in (2, 6, 7):
            small = int(round(ext_data.smalnumb * 10))
        else:
            small = int(ext_data.smalnumb)
        small = max(0, min(small, 0xFFFF))
        return struct.pack("<BHHHB", 0x22, big, small, ext_data.vtimed, cfg)