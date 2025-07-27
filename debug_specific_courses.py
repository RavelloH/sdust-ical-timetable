from course_parser import parse_timetable_from_xls

# 测试解析的课程
courses = parse_timetable_from_xls()

# 查看高等数学的详细信息
math_courses = [c for c in courses if "高等数学" in c.name]
print("高等数学课程详细信息:")
for i, course in enumerate(math_courses):
    print(f"{i+1}. 星期{course.weekday} 第{course.indexes}节")
    print(f"   周次: {course.weeks}")
    print(f"   教室: {course.classroom}")
    print()

# 统计所有高等数学的周次
all_weeks = set()
for course in math_courses:
    all_weeks.update(course.weeks)

print(f"高等数学总周次: {sorted(all_weeks)}")
print(f"高等数学总课时数: {len(all_weeks)}")

# 查看大学英语的详细信息
english_courses = [c for c in courses if "大学英语" in c.name]
print("\n大学英语课程详细信息:")
for i, course in enumerate(english_courses):
    print(f"{i+1}. 星期{course.weekday} 第{course.indexes}节")
    print(f"   周次: {course.weeks}")
    print(f"   教室: {course.classroom}")
    print()

# 统计所有大学英语的周次
all_weeks = set()
for course in english_courses:
    all_weeks.update(course.weeks)

print(f"大学英语总周次: {sorted(all_weeks)}")
print(f"大学英语总课时数: {len(all_weeks)}")
