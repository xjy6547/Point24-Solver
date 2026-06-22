"""
24点游戏求解器 - 图形用户界面
使用Tkinter构建，提供友好的交互体验
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from solver import solve_24
from typing import List

class Point24GUI:
    """24点求解器GUI类"""
    
    def __init__(self, root: tk.Tk):
        """
        初始化GUI界面
        
        Args:
            root: Tkinter根窗口
        """
        self.root = root
        self.root.title("24点游戏求解器")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # 存储当前输入的数字
        self.input_numbers = []
        
        # 设置样式
        self.root.configure(bg='#f0f0f0')
        
        # 创建界面组件
        self._create_widgets()
    
    def _create_widgets(self):
        """创建所有界面组件"""
        
        # 标题
        title_label = tk.Label(
            self.root,
            text="24点游戏求解器",
            font=("Arial", 20, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=20)
        
        # 说明文字
        instruction = tk.Label(
            self.root,
            text="请输入4个数字（1-13），然后点击求解",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        instruction.pack(pady=5)
        
        # 数字显示框
        self.display_var = tk.StringVar()
        self.display_var.set("选择的数字：")
        display_label = tk.Label(
            self.root,
            textvariable=self.display_var,
            font=("Arial", 14),
            bg='#ffffff',
            fg='#333333',
            relief=tk.SUNKEN,
            bd=2,
            padx=10,
            pady=10,
            width=30
        )
        display_label.pack(pady=20)
        
        # 数字按钮框架
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        # 创建数字按钮（1-13）
        for i in range(1, 14):
            btn = tk.Button(
                button_frame,
                text=str(i),
                font=("Arial", 12),
                width=4,
                height=2,
                command=lambda x=i: self._add_number(x),
                bg='#4CAF50',
                fg='white',
                activebackground='#45a049'
            )
            # 每行放7个按钮
            row = (i - 1) // 7
            col = (i - 1) % 7
            btn.grid(row=row, column=col, padx=3, pady=3)
        
        # 控制按钮框架
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=20)
        
        # 求解按钮
        solve_btn = tk.Button(
            control_frame,
            text="求解",
            font=("Arial", 12, "bold"),
            width=10,
            height=2,
            command=self._solve,
            bg='#2196F3',
            fg='white',
            activebackground='#1976D2'
        )
        solve_btn.grid(row=0, column=0, padx=10)
        
        # 清除按钮
        clear_btn = tk.Button(
            control_frame,
            text="清除",
            font=("Arial", 12),
            width=10,
            height=2,
            command=self._clear,
            bg='#FF9800',
            fg='white',
            activebackground='#F57C00'
        )
        clear_btn.grid(row=0, column=1, padx=10)
        
        # 结果显示区域
        result_label = tk.Label(
            self.root,
            text="求解结果：",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        result_label.pack(pady=(20, 5))
        
        # 滚动文本框显示结果
        self.result_text = scrolledtext.ScrolledText(
            self.root,
            width=50,
            height=12,
            font=("Courier", 10),
            bg='#ffffff',
            fg='#333333'
        )
        self.result_text.pack(pady=5)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg='#e0e0e0',
            fg='#666666',
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _add_number(self, number: int):
        """
        添加数字到输入列表
        
        Args:
            number: 要添加的数字
        """
        if len(self.input_numbers) < 4:
            self.input_numbers.append(number)
            self._update_display()
            self.status_var.set(f"已选择 {len(self.input_numbers)}/4 个数字")
        else:
            messagebox.showwarning("提示", "已经选择了4个数字，请先清除再添加")
    
    def _update_display(self):
        """更新数字显示"""
        if self.input_numbers:
            display_text = "选择的数字：" + " ".join(map(str, self.input_numbers))
        else:
            display_text = "选择的数字："
        self.display_var.set(display_text)
    
    def _clear(self):
        """清除所有输入"""
        self.input_numbers.clear()
        self._update_display()
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("已清除，请重新输入")
    
    def _solve(self):
        """求解24点问题"""
        # 检查是否输入了4个数字
        if len(self.input_numbers) != 4:
            messagebox.showwarning("提示", "请先选择4个数字！")
            return
        
        # 清空之前的结果
        self.result_text.delete(1.0, tk.END)
        
        # 显示计算中状态
        self.status_var.set("正在计算...")
        self.root.update()
        
        try:
            # 调用求解器
            numbers = self.input_numbers.copy()
            solutions = solve_24(numbers)
            
            # 显示结果
            if solutions:
                self.result_text.insert(tk.END, f"数字 {numbers} 的24点解法：\n")
                self.result_text.insert(tk.END, "=" * 40 + "\n\n")
                
                for i, solution in enumerate(solutions, 1):
                    self.result_text.insert(tk.END, f"{i}. {solution}\n")
                
                self.status_var.set(f"求解完成！共找到 {len(solutions)} 种解法")
            else:
                self.result_text.insert(tk.END, f"数字 {numbers} 无解！\n")
                self.result_text.insert(tk.END, "\n请尝试其他数字组合")
                self.status_var.set("该组合无解")
                
        except Exception as e:
            messagebox.showerror("错误", f"求解过程中出现错误：{str(e)}")
            self.status_var.set("求解失败")


def main():
    """启动GUI程序"""
    root = tk.Tk()
    app = Point24GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()