#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试未知教室处理功能
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.getcwd())

from course_parser import classroom_to_location
from data import Course

def test_unknown_classroom():
    """测试未知教室处理功能"""
    print("📋 未知教室处理测试")
    print("=" * 50)
    
    # 测试 classroom_to_location 函数
    print("🏫 测试位置生成功能：")
    test_cases = [
        ("J7-106室", "高等数学", "山东科技大学J7"),
        ("品学楼B107", "线性代数", "山东科技大学品学楼"),
        ("未知教室", "概率论", ""),
        ("线上虚拟教室", "网课", ""),
        ("", "空教室", ""),
    ]
    
    for i, (classroom, course_name, expected) in enumerate(test_cases, 1):
        result = classroom_to_location(classroom, course_name)
        status = "✅ 通过" if result == expected else "❌ 失败"
        print(f"{i:2d}. {status} | '{classroom}' + '{course_name}' -> '{result}'")
        if result != expected:
            print(f"     期望: '{expected}'")
    
    print("\n📚 测试课程标题生成功能：")
    
    # 测试 Course.title() 方法
    courses = [
        Course("高等数学", "张老师", "J7-106室", "山东科技大学J7", 1, [1, 2, 3], [1, 2]),
        Course("线性代数", "李老师", "未知教室", "", 2, [1, 2, 3], [3, 4]),
        Course("概率论", "王老师", "品学楼B107", "山东科技大学品学楼", 3, [1, 2, 3], [5, 6]),
    ]
    
    expected_titles = [
        "高等数学 - J7-106室",
        "线性代数",  # 不显示"未知教室"
        "概率论 - 品学楼B107"
    ]
    
    for i, (course, expected_title) in enumerate(zip(courses, expected_titles), 1):
        result_title = course.title()
        status = "✅ 通过" if result_title == expected_title else "❌ 失败"
        print(f"{i:2d}. {status} | '{course.name}' 在 '{course.classroom}' -> '{result_title}'")
        if result_title != expected_title:
            print(f"     期望: '{expected_title}'")
    
    print("=" * 50)
    print("🎉 测试完成！")

if __name__ == "__main__":
    test_unknown_classroom()
