#!/usr/bin/env python
import sys

last_key = None
output_buffer = []

def output_unique_record(key, buffer):
    """当键改变时，输出缓冲区中的唯一记录并清空缓冲区"""
    if buffer:
        # 去重逻辑假设在Mapper阶段已按需筛选，Reducer只需选择缓冲区中的任意一条记录输出
        print(f"{key}\t{buffer[0]}")  # 输出第一行作为代表
    buffer.clear()

for line in sys.stdin:
    key, data = line.strip().split('\t', 1)  # 按\t分割，第0个元素为键，之后为值
    if last_key is not None and last_key != key:
        output_unique_record(last_key, output_buffer)  # 处理上一组数据
    output_buffer.append(data)  # 缓存当前记录
    last_key = key

# 确保处理完所有数据后输出最后一组
if last_key is not None:
    output_unique_record(last_key, output_buffer)
