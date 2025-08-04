#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础示例代码
这里包含了Python编程的基础概念和代码示例
"""

def basic_variables_and_types():
    """变量和数据类型示例"""
    print("=== 变量和数据类型 ===")
    
    # 数字类型
    age = 25
    height = 1.75
    print(f"年龄: {age} (整数)")
    print(f"身高: {height} (浮点数)")
    
    # 字符串类型
    name = "Python学习者"
    greeting = f"你好, {name}!"
    print(f"问候: {greeting}")
    
    # 布尔类型
    is_student = True
    print(f"是学生: {is_student}")
    
    print()

def basic_lists_and_operations():
    """列表和基本操作示例"""
    print("=== 列表和操作 ===")
    
    # 创建列表
    fruits = ["苹果", "香蕉", "橙子"]
    print(f"水果列表: {fruits}")
    
    # 添加元素
    fruits.append("葡萄")
    print(f"添加葡萄后: {fruits}")
    
    # 访问元素
    print(f"第一个水果: {fruits[0]}")
    print(f"最后一个水果: {fruits[-1]}")
    
    # 列表长度
    print(f"水果总数: {len(fruits)}")
    
    # 列表切片
    print(f"前两个水果: {fruits[:2]}")
    
    print()

def basic_loops():
    """循环语句示例"""
    print("=== 循环语句 ===")
    
    # for循环 - 遍历数字
    print("数字循环:")
    for i in range(5):
        print(f"  第{i+1}次循环")
    
    # for循环 - 遍历列表
    print("遍历列表:")
    colors = ["红色", "绿色", "蓝色"]
    for color in colors:
        print(f"  颜色: {color}")
    
    # while循环
    print("while循环倒计时:")
    countdown = 3
    while countdown > 0:
        print(f"  {countdown}...")
        countdown -= 1
    print("  开始!")
    
    print()

def basic_conditionals():
    """条件语句示例"""
    print("=== 条件语句 ===")
    
    score = 85
    
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "D"
    
    print(f"分数: {score}, 等级: {grade}")
    
    # 多条件判断
    weather = "晴天"
    temperature = 25
    
    if weather == "晴天" and temperature > 20:
        print("适合外出活动!")
    else:
        print("建议室内活动")
    
    print()

def basic_functions():
    """函数定义和使用示例"""
    print("=== 函数定义 ===")
    
    def greet(name, language="中文"):
        """问候函数"""
        if language == "中文":
            return f"你好, {name}!"
        elif language == "英文":
            return f"Hello, {name}!"
        else:
            return f"Hi, {name}!"
    
    # 调用函数
    print(greet("小明"))
    print(greet("Tom", "英文"))
    print(greet("Alex", "其他"))
    
    # 计算函数
    def calculate_area(length, width):
        """计算矩形面积"""
        return length * width
    
    area = calculate_area(5, 3)
    print(f"矩形面积: {area}")
    
    print()

def basic_dictionaries():
    """字典操作示例"""
    print("=== 字典操作 ===")
    
    # 创建字典
    student = {
        "姓名": "小红",
        "年龄": 20,
        "专业": "计算机科学",
        "成绩": [85, 92, 78, 90]
    }
    
    # 访问字典值
    print(f"学生姓名: {student['姓名']}")
    print(f"学生年龄: {student['年龄']}")
    
    # 修改字典
    student["年龄"] = 21
    student["城市"] = "北京"
    
    # 遍历字典
    print("学生信息:")
    for key, value in student.items():
        print(f"  {key}: {value}")
    
    # 字典方法
    print(f"字典键: {list(student.keys())}")
    print(f"平均成绩: {sum(student['成绩']) / len(student['成绩']):.1f}")
    
    print()

def basic_list_comprehensions():
    """列表推导式示例"""
    print("=== 列表推导式 ===")
    
    # 基础列表推导式
    numbers = [1, 2, 3, 4, 5]
    squares = [x**2 for x in numbers]
    print(f"原数字: {numbers}")
    print(f"平方数: {squares}")
    
    # 带条件的列表推导式
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    print(f"偶数的平方: {even_squares}")
    
    # 字符串处理
    words = ["python", "java", "javascript", "go"]
    long_words = [word.upper() for word in words if len(word) > 4]
    print(f"长单词(大写): {long_words}")
    
    print()

def basic_file_operations():
    """文件操作示例"""
    print("=== 文件操作 ===")
    
    # 写入文件
    filename = "example.txt"
    
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("这是一个示例文件\n")
            file.write("Python文件操作很简单\n")
            file.write("记住要使用with语句\n")
        
        print(f"✅ 文件 {filename} 写入成功")
        
        # 读取文件
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            print("文件内容:")
            print(content)
        
        # 按行读取
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            print(f"文件共有 {len(lines)} 行")
        
        # 清理文件
        import os
        os.remove(filename)
        print(f"🗑️ 文件 {filename} 已删除")
        
    except Exception as e:
        print(f"❌ 文件操作失败: {e}")
    
    print()

def basic_error_handling():
    """异常处理示例"""
    print("=== 异常处理 ===")
    
    # 除零异常
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("❌ 不能除以零!")
        result = None
    
    # 类型转换异常
    try:
        number = int("abc")
    except ValueError:
        print("❌ 无法将字符串转换为数字!")
        number = 0
    
    # 多种异常处理
    def safe_divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            print("错误: 除数不能为零")
            return None
        except TypeError:
            print("错误: 参数类型不正确")
            return None
        except Exception as e:
            print(f"未知错误: {e}")
            return None
    
    print(f"10 / 2 = {safe_divide(10, 2)}")
    print(f"10 / 0 = {safe_divide(10, 0)}")
    print(f"'10' / 2 = {safe_divide('10', 2)}")
    
    print()

def main():
    """运行所有示例"""
    print("🐍 Python基础示例演示")
    print("=" * 50)
    
    basic_variables_and_types()
    basic_lists_and_operations()
    basic_loops()
    basic_conditionals()
    basic_functions()
    basic_dictionaries()
    basic_list_comprehensions()
    basic_file_operations()
    basic_error_handling()
    
    print("🎉 所有基础示例演示完成!")

if __name__ == "__main__":
    main()