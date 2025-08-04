#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python高级示例代码
这里包含了Python编程的高级概念和代码示例
"""

import functools
import itertools
import collections
from typing import List, Dict, Optional, Union
import json
import datetime

def advanced_decorators():
    """装饰器示例"""
    print("=== 装饰器 ===")
    
    # 计时装饰器
    def timing_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"函数 {func.__name__} 执行时间: {end - start:.4f}秒")
            return result
        return wrapper
    
    # 日志装饰器
    def log_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"调用函数: {func.__name__}")
            print(f"参数: args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"返回值: {result}")
            return result
        return wrapper
    
    @timing_decorator
    @log_decorator
    def slow_function(n):
        """模拟耗时函数"""
        import time
        time.sleep(0.1)
        return sum(range(n))
    
    slow_function(1000)
    print()

def advanced_generators():
    """生成器示例"""
    print("=== 生成器 ===")
    
    # 基础生成器
    def fibonacci_generator():
        """斐波那契数列生成器"""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    # 使用生成器
    fib = fibonacci_generator()
    print("前10个斐波那契数:")
    for i, num in enumerate(fib):
        if i >= 10:
            break
        print(f"  F({i}) = {num}")
    
    # 生成器表达式
    squares_gen = (x**2 for x in range(10))
    print(f"前10个平方数: {list(squares_gen)}")
    
    # 文件处理生成器
    def process_lines(lines):
        """处理文本行的生成器"""
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                yield line.upper()
    
    sample_lines = ["python", "# 这是注释", "java", "", "javascript"]
    processed = list(process_lines(sample_lines))
    print(f"处理后的行: {processed}")
    
    print()

def advanced_context_managers():
    """上下文管理器示例"""
    print("=== 上下文管理器 ===")
    
    # 自定义上下文管理器
    class TimingContext:
        def __init__(self, name):
            self.name = name
        
        def __enter__(self):
            import time
            self.start_time = time.time()
            print(f"开始执行: {self.name}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            import time
            end_time = time.time()
            print(f"结束执行: {self.name}, 耗时: {end_time - self.start_time:.4f}秒")
            if exc_type:
                print(f"发生异常: {exc_type.__name__}: {exc_val}")
            return False  # 不抑制异常
    
    # 使用上下文管理器
    with TimingContext("示例操作"):
        import time
        time.sleep(0.1)
        result = sum(range(1000))
        print(f"计算结果: {result}")
    
    # 使用contextlib
    from contextlib import contextmanager
    
    @contextmanager
    def database_transaction():
        print("开始数据库事务")
        try:
            yield "db_connection"
            print("提交事务")
        except Exception as e:
            print(f"回滚事务: {e}")
            raise
        finally:
            print("关闭数据库连接")
    
    with database_transaction() as db:
        print(f"使用数据库连接: {db}")
        # 模拟数据库操作
    
    print()

def advanced_classes_and_inheritance():
    """类和继承示例"""
    print("=== 类和继承 ===")
    
    # 基础类
    class Animal:
        def __init__(self, name, species):
            self.name = name
            self.species = species
        
        def speak(self):
            return f"{self.name} 发出声音"
        
        def __str__(self):
            return f"{self.species}: {self.name}"
        
        def __repr__(self):
            return f"Animal('{self.name}', '{self.species}')"
    
    # 继承类
    class Dog(Animal):
        def __init__(self, name, breed):
            super().__init__(name, "狗")
            self.breed = breed
        
        def speak(self):
            return f"{self.name} 汪汪叫"
        
        def fetch(self):
            return f"{self.name} 去捡球"
    
    class Cat(Animal):
        def __init__(self, name, color):
            super().__init__(name, "猫")
            self.color = color
        
        def speak(self):
            return f"{self.name} 喵喵叫"
        
        def hunt(self):
            return f"{self.name} 在捕猎"
    
    # 使用类
    animals = [
        Dog("旺财", "金毛"),
        Cat("咪咪", "橙色"),
        Animal("鹦鹉", "鸟类")
    ]
    
    for animal in animals:
        print(f"{animal}: {animal.speak()}")
    
    # 多态性
    dog = animals[0]
    if hasattr(dog, 'fetch'):
        print(dog.fetch())
    
    print()

def advanced_metaclasses():
    """元类示例"""
    print("=== 元类 ===")
    
    # 简单元类
    class SingletonMeta(type):
        """单例模式元类"""
        _instances = {}
        
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]
    
    class DatabaseConnection(metaclass=SingletonMeta):
        def __init__(self):
            self.connection_id = id(self)
            print(f"创建数据库连接: {self.connection_id}")
        
        def query(self, sql):
            return f"执行查询: {sql}"
    
    # 测试单例
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1.connection_id: {db1.connection_id}")
    print(f"db2.connection_id: {db2.connection_id}")
    
    print()

def advanced_async_programming():
    """异步编程示例"""
    print("=== 异步编程 ===")
    
    import asyncio
    
    async def fetch_data(url, delay):
        """模拟异步获取数据"""
        print(f"开始获取: {url}")
        await asyncio.sleep(delay)  # 模拟网络延迟
        data = f"来自 {url} 的数据"
        print(f"完成获取: {url}")
        return data
    
    async def process_data(data):
        """模拟异步处理数据"""
        print(f"开始处理: {data}")
        await asyncio.sleep(0.1)
        result = f"处理后的 {data}"
        print(f"完成处理: {result}")
        return result
    
    async def main_async():
        """主异步函数"""
        # 并发获取数据
        tasks = [
            fetch_data("API-1", 0.2),
            fetch_data("API-2", 0.3),
            fetch_data("API-3", 0.1)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # 处理数据
        processed_results = []
        for data in results:
            processed = await process_data(data)
            processed_results.append(processed)
        
        return processed_results
    
    # 运行异步代码
    try:
        import asyncio
        results = asyncio.run(main_async())
        print(f"最终结果: {results}")
    except Exception as e:
        print(f"异步执行失败: {e}")
    
    print()

def advanced_data_structures():
    """高级数据结构示例"""
    print("=== 高级数据结构 ===")
    
    # Counter
    text = "hello world hello python"
    counter = collections.Counter(text.split())
    print(f"词频统计: {counter}")
    print(f"最常见的2个词: {counter.most_common(2)}")
    
    # defaultdict
    dd = collections.defaultdict(list)
    data = [("果类", "苹果"), ("果类", "香蕉"), ("蔬菜", "胡萝卜"), ("蔬菜", "白菜")]
    for category, item in data:
        dd[category].append(item)
    print(f"分类数据: {dict(dd)}")
    
    # namedtuple
    Point = collections.namedtuple('Point', ['x', 'y'])
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    print(f"点1: {p1}, 点2: {p2}")
    print(f"距离: {((p2.x - p1.x)**2 + (p2.y - p1.y)**2)**0.5:.2f}")
    
    # deque
    dq = collections.deque([1, 2, 3])
    dq.appendleft(0)
    dq.append(4)
    print(f"双端队列: {list(dq)}")
    
    print()

def advanced_functional_programming():
    """函数式编程示例"""
    print("=== 函数式编程 ===")
    
    # map, filter, reduce
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # map示例
    squares = list(map(lambda x: x**2, numbers))
    print(f"平方数: {squares}")
    
    # filter示例
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"偶数: {evens}")
    
    # reduce示例
    product = functools.reduce(lambda x, y: x * y, range(1, 6))
    print(f"1到5的乘积: {product}")
    
    # 偏函数
    multiply = lambda x, y: x * y
    double = functools.partial(multiply, 2)
    triple = functools.partial(multiply, 3)
    
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")
    
    # 高阶函数
    def compose(*functions):
        """函数组合"""
        def inner(arg):
            for func in reversed(functions):
                arg = func(arg)
            return arg
        return inner
    
    add_one = lambda x: x + 1
    multiply_by_two = lambda x: x * 2
    
    composed = compose(multiply_by_two, add_one)
    print(f"compose(multiply_by_two, add_one)(5) = {composed(5)}")
    
    print()

def advanced_type_hints():
    """类型提示示例"""
    print("=== 类型提示 ===")
    
    def process_user_data(
        name: str, 
        age: int, 
        scores: List[float], 
        metadata: Optional[Dict[str, Union[str, int]]] = None
    ) -> Dict[str, Union[str, int, float]]:
        """处理用户数据，返回统计信息"""
        
        if metadata is None:
            metadata = {}
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        result = {
            "name": name,
            "age": age,
            "avg_score": round(avg_score, 2),
            "total_scores": len(scores),
            "metadata": metadata
        }
        
        return result
    
    # 使用函数
    user_result = process_user_data(
        "张三", 
        25, 
        [85.5, 92.0, 78.5, 90.0], 
        {"city": "北京", "level": 3}
    )
    
    print(f"用户数据处理结果: {json.dumps(user_result, ensure_ascii=False, indent=2)}")
    
    # 类型别名
    UserID = int
    UserName = str
    UserRegistry = Dict[UserID, UserName]
    
    users: UserRegistry = {1: "Alice", 2: "Bob", 3: "Charlie"}
    print(f"用户注册表: {users}")
    
    print()

def main():
    """运行所有高级示例"""
    print("🚀 Python高级示例演示")
    print("=" * 50)
    
    advanced_decorators()
    advanced_generators()
    advanced_context_managers()
    advanced_classes_and_inheritance()
    advanced_metaclasses()
    advanced_async_programming()
    advanced_data_structures()
    advanced_functional_programming()
    advanced_type_hints()
    
    print("🎉 所有高级示例演示完成!")

if __name__ == "__main__":
    main()