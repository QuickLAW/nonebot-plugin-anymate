import random

def generate_unique_random_numbers(n, max_value=20):
    # 确保请求的数量不超过最大可能的不同值数量
    if n > max_value:
        raise ValueError("The number of unique integers cannot exceed the maximum value.")
    
    # 使用集合来确保唯一性
    unique_numbers = set()
    
    # 当集合中的元素数量小于请求的数量时，继续添加
    while len(unique_numbers) < n:
        # 生成一个随机整数并添加到集合中
        # 注意：由于集合不允许重复，如果生成的数字已经存在，则会被忽略
        unique_numbers.add(random.randint(1, max_value))
    
    # 将集合转换为列表并返回
    # 如果需要保持特定的顺序（如升序），可以使用sorted()函数
    return sorted(list(unique_numbers))
