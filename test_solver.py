"""
24点求解器 - 单元测试模块
测试核心算法的正确性和鲁棒性
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from solver import solve_24, Point24Solver
from utils import validate_input, is_close

class TestPoint24Solver(unittest.TestCase):
    """测试24点求解器"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.solver = Point24Solver()
    
    def test_classic_solutions(self):
        """测试经典有解情况"""
        test_cases = [
            [1, 2, 3, 4],    # 经典简单情况
            [5, 5, 5, 1],    # 需要分数运算
            [3, 3, 8, 8],    # 经典难题
            [2, 2, 2, 2],    # 重复数字
        ]
        
        for numbers in test_cases:
            with self.subTest(numbers=numbers):
                solutions = solve_24(numbers)
                self.assertTrue(len(solutions) > 0, 
                              f"数字 {numbers} 应该有解")
    
    def test_no_solution(self):
        """测试无解情况"""
        test_cases = [
            [1, 1, 1, 1],
            [1, 1, 1, 2],
            [13, 13, 13, 13],
        ]
        
        for numbers in test_cases:
            with self.subTest(numbers=numbers):
                solutions = solve_24(numbers)
                self.assertEqual(len(solutions), 0, 
                               f"数字 {numbers} 应该无解")
    
    def test_solution_correctness(self):
        """测试解法的正确性"""
        numbers = [1, 2, 3, 4]
        solutions = solve_24(numbers)
        
        for solution in solutions:
            # 移除表达式中的空格和特殊字符，然后求值
            try:
                # 将表达式转换为可求值的形式
                expr = solution.replace('×', '*').replace(' ', '')
                # 注意：这里使用eval是为了测试，实际项目中应使用更安全的方法
                result = eval(expr)
                self.assertTrue(is_close(result, 24.0), 
                              f"解法 {solution} 的结果不是24")
            except Exception as e:
                self.fail(f"解法 {solution} 求值失败: {e}")
    
    def test_duplicate_solutions_removed(self):
        """测试重复解法是否被正确去重"""
        numbers = [2, 2, 2, 2]
        solutions = solve_24(numbers)
        
        # 检查是否有重复
        self.assertEqual(len(solutions), len(set(solutions)), 
                       "存在重复的解法")
    
    def test_edge_cases(self):
        """测试边缘情况"""
        # 测试包含0的情况（虽然输入范围是1-13，但内部运算可能产生0）
        solver = Point24Solver()
        
        # 测试除零处理
        # 这个测试确保程序不会因为除零而崩溃
        try:
            solutions = solve_24([1, 1, 1, 13])
            # 只要能正常返回（无论有解无解），就算通过
            self.assertIsInstance(solutions, list)
        except ZeroDivisionError:
            self.fail("程序遇到除零错误")
    
    def test_input_validation(self):
        """测试输入验证"""
        # 测试数字个数
        valid, msg = validate_input([1, 2, 3])
        self.assertFalse(valid)
        self.assertIn("4个", msg)
        
        # 测试数字范围
        valid, msg = validate_input([1, 2, 3, 14])
        self.assertFalse(valid)
        self.assertIn("范围", msg)
        
        # 测试合法输入
        valid, msg = validate_input([1, 2, 3, 4])
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_all_numbers_1_to_13(self):
        """测试所有1-13的数字组合（抽样测试）"""
        import random
        
        # 随机测试100组数字
        for _ in range(100):
            numbers = [random.randint(1, 13) for _ in range(4)]
            try:
                solutions = solve_24(numbers)
                # 验证返回类型
                self.assertIsInstance(solutions, list)
                # 验证解法数量合理（最多几百种）
                self.assertLess(len(solutions), 1000, 
                              f"数字 {numbers} 的解法数量异常多")
            except Exception as e:
                self.fail(f"数字 {numbers} 求解失败: {e}")


class TestFloatingPointPrecision(unittest.TestCase):
    """测试浮点数精度处理"""
    
    def test_is_close_function(self):
        """测试浮点数比较函数"""
        self.assertTrue(is_close(24.0, 24.0))
        self.assertTrue(is_close(24.0, 24.0000001))
        self.assertFalse(is_close(24.0, 24.1))
        self.assertTrue(is_close(0.1 + 0.2, 0.3))  # 经典的浮点数精度问题


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestPoint24Solver))
    suite.addTests(loader.loadTestsFromTestCase(TestFloatingPointPrecision))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    print(f"运行测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)