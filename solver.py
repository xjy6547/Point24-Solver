"""
24点游戏求解器 - 核心算法模块
使用回溯算法和"两数合并"策略，穷举所有可能的解法
"""

from typing import List, Tuple, Set
import itertools

# 浮点数比较的误差范围
EPSILON = 1e-6

class Point24Solver:
    """24点求解器类"""
    
    def __init__(self, target: float = 24.0):
        """
        初始化求解器
        
        Args:
            target: 目标值，默认为24
        """
        self.target = target
        self.solutions = []  # 存储所有找到的解法
        self.operators = ['+', '-', '*', '/']
    
    def solve(self, numbers: List[int]) -> List[str]:
        """
        求解24点问题的主函数
        
        Args:
            numbers: 包含4个整数的列表，每个数范围1-13
            
        Returns:
            所有解法的字符串列表，每个字符串是完整的表达式
        """
        self.solutions = []
        # 将整数转换为浮点数，便于计算
        nums_float = [float(n) for n in numbers]
        # 使用集合去重（因为可能有重复数字导致相同解法）
        self._backtrack(nums_float, [str(n) for n in numbers])
        
        # 去重并格式化输出
        unique_solutions = list(set(self.solutions))
        return unique_solutions
    
    def _backtrack(self, values: List[float], expressions: List[str]):
        """
        回溯搜索所有可能的运算组合
        
        Args:
            values: 当前数字列表
            expressions: 对应的表达式字符串列表
        """
        n = len(values)
        
        # 递归终止条件：只剩一个数字
        if n == 1:
            if abs(values[0] - self.target) < EPSILON:
                self.solutions.append(expressions[0])
            return
        
        # 选择两个不同的数字进行运算
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                
                # 创建新的数字和表达式列表（不包含i和j位置的元素）
                new_values = []
                new_exprs = []
                for k in range(n):
                    if k != i and k != j:
                        new_values.append(values[k])
                        new_exprs.append(expressions[k])
                
                # 尝试6种运算（加减乘除，考虑交换律）
                a, b = values[i], values[j]
                expr_a, expr_b = expressions[i], expressions[j]
                
                # 1. 加法 a + b
                self._try_operation(new_values, new_exprs, 
                                   a + b, f"({expr_a} + {expr_b})")
                
                # 2. 乘法 a * b
                self._try_operation(new_values, new_exprs, 
                                   a * b, f"({expr_a} × {expr_b})")
                
                # 3. 减法 a - b
                self._try_operation(new_values, new_exprs, 
                                   a - b, f"({expr_a} - {expr_b})")
                
                # 4. 减法 b - a (减法的另一种顺序)
                self._try_operation(new_values, new_exprs, 
                                   b - a, f"({expr_b} - {expr_a})")
                
                # 5. 除法 a / b (需要检查除数不为0)
                if abs(b) > EPSILON:
                    self._try_operation(new_values, new_exprs, 
                                       a / b, f"({expr_a} / {expr_b})")
                
                # 6. 除法 b / a (除法的另一种顺序)
                if abs(a) > EPSILON:
                    self._try_operation(new_values, new_exprs, 
                                       b / a, f"({expr_b} / {expr_a})")
    
    def _try_operation(self, values: List[float], expressions: List[str], 
                       result: float, new_expr: str):
        """
        尝试一种运算，将结果加入列表并继续递归
        
        Args:
            values: 当前值列表（不包含参与运算的两个数）
            expressions: 当前表达式列表
            result: 运算结果
            new_expr: 新的表达式字符串
        """
        new_values = values.copy()
        new_exprs = expressions.copy()
        new_values.append(result)
        new_exprs.append(new_expr)
        self._backtrack(new_values, new_exprs)


def solve_24(numbers: List[int]) -> List[str]:
    """
    便捷函数：求解24点问题
    
    Args:
        numbers: 4个数字的列表
        
    Returns:
        所有解法的列表
        
    Example:
        >>> solutions = solve_24([3, 3, 8, 8])
        >>> for s in solutions:
        ...     print(s)
        ((8 / (3 - (8 / 3))))
    """
    solver = Point24Solver()
    return solver.solve(numbers)


def main():
    """命令行交互入口"""
    print("=" * 50)
    print("          24点游戏求解器")
    print("=" * 50)
    print("请输入4个数字（1-13），用空格分隔")
    print("输入 'q' 退出程序")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n请输入数字: ").strip()
            
            if user_input.lower() == 'q':
                print("感谢使用，再见！")
                break
            
            # 解析输入
            numbers = [int(x) for x in user_input.split()]
            
            # 输入验证
            if len(numbers) != 4:
                print("错误：请输入恰好4个数字！")
                continue
            
            if any(n < 1 or n > 13 for n in numbers):
                print("错误：数字范围应在1-13之间！")
                continue
            
            # 求解
            print(f"\n正在计算 {numbers} 的24点解法...")
            solutions = solve_24(numbers)
            
            if solutions:
                print(f"\n找到 {len(solutions)} 种解法：")
                for i, solution in enumerate(solutions, 1):
                    print(f"  {i}. {solution}")
            else:
                print(f"\n抱歉，{numbers} 无解！")
                
        except ValueError:
            print("错误：请输入有效的整数！")
        except KeyboardInterrupt:
            print("\n\n程序被中断，再见！")
            break


if __name__ == "__main__":
    main()