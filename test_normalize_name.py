#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试课程名称规范化功能
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.getcwd())

from course_parser import normalize_course_name

def test_normalize_course_name():
    """测试课程名称规范化功能"""
    test_cases = [
        ("电路（2）", "电路"),
        ("大学英语（A）", "大学英语"),
        ("高等数学（B）（2-1）", "高等数学"),
        ("线性代数", "线性代数"),  # 无括号的情况
        ("程序设计基础(C语言)", "程序设计基础"),
        ("数据结构（双语）", "数据结构"),
        ("概率论与数理统计（A）（3-1）", "概率论与数理统计"),
        ("大学物理 （实验）", "大学物理"),  # 有空格的情况
        ("", ""),  # 空字符串的情况
    ]
    
    print("📋 课程名称规范化测试")
    print("=" * 50)
    
    all_passed = True
    for i, (input_name, expected) in enumerate(test_cases, 1):
        result = normalize_course_name(input_name)
        status = "✅ 通过" if result == expected else "❌ 失败"
        print(f"{i:2d}. {status} | '{input_name}' -> '{result}'")
        if result != expected:
            print(f"     期望: '{expected}'")
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查代码。")
    
    return all_passed

if __name__ == "__main__":
    test_normalize_course_name()
