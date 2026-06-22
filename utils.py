"""
24点求解器 - 工具函数模块
提供通用的辅助功能
"""

from typing import List, Tuple
import time
from functools import wraps

# 浮点数比较精度
EPSILON = 1e-6

def is_close(a: float, b: float, epsilon: float = EPSILON) -> bool:
    """
    安全地比较两个浮点数是否接近
    
    Args:
        a: 第一个浮点数
        b: 第二个浮点数
        epsilon: 允许的误差范围
        
    Returns:
        如果两个数足够接近返回True，否则返回False
    """
    return abs(a - b) < epsilon


def validate_input(numbers: List[int]) -> Tuple[bool, str]:
    """
    验证输入的数字是否合法
    
    Args:
        numbers: 输入的数字列表
        
    Returns:
        (是否合法, 错误信息) 的元组
    """
    if len(numbers) != 4:
        return False, "必须输入恰好4个数字"
    
    for num in numbers:
        if not isinstance(num, int):
            return False, f"数字 {num} 不是整数"
        if num < 1 or num > 13:
            return False, f"数字 {num} 不在1-13范围内"
    
    return True, ""


def timer(func):
    """
    装饰器：计算函数执行时间
    
    Args:
        func: 要计时的函数
        
    Returns:
        包装后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"函数 {func.__name__} 执行时间: {execution_time:.4f} 秒")
        return result
    return wrapper


def format_solutions(solutions: List[str], numbers: List[int]) -> str:
    """
    格式化输出解法
    
    Args:
        solutions: 解法列表
        numbers: 原始输入数字
        
    Returns:
        格式化后的字符串
    """
    if not solutions:
        return f"数字 {numbers} 无解"
    
    result = f"数字 {numbers} 的24点解法：\n"
    result += "=" * 40 + "\n"
    
    for i, solution in enumerate(solutions, 1):
        result += f"{i}. {solution}\n"
    
    result += f"\n共找到 {len(solutions)} 种解法"
    return result