#!/usr/bin/env python
import sys

# 定义处理CSV标题与实际列名的映射关系
COLUMN_MAPPING = {
    'Column1': 'Video_Name',
    'Column3': 'Video_Address',
    'Column5': 'Video_language',
    'Column8': 'Video_Time',
}

THRESHOLD_MINUTES = 110  # 假定筛选时间大于0分钟的记录

def parse_csv_line(line):
    """解析CSV行并返回一个字典，键为映射后的列名"""
    columns = line.strip().split(',')
    return {COLUMN_MAPPING.get(col, col): value for col, value in zip(COLUMN_MAPPING, columns)}

for line in sys.stdin:
    if line.startswith('Column'):  # 跳过CSV首行标题
        continue
    record = parse_csv_line(line)
    try:
        video_time_minutes = int(record['Video_Time'].split('分钟')[0])
        if video_time_minutes > THRESHOLD_MINUTES:
            print(f"{record['Video_Name_CN']}\t{record['Video_Address']\t{record['Video_language']}\t{record['Video_Time']}")
    except (KeyError, ValueError):
        # 如果列不存在或转换时间出错，则忽略该行
        pass
