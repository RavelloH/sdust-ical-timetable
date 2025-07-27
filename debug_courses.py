from course_parser import parse_timetable_from_xls

# 测试解析的课程
courses = parse_timetable_from_xls()

print("解析的课程详情:")
for i, course in enumerate(courses[:5], 1):  # 只显示前5个课程
    print(f"{i}. 课程名: {course.name}")
    print(f"   教师: {course.teacher}")
    print(f"   教室: {course.classroom}")
    print(f"   星期: {course.weekday}")
    print(f"   周次: {course.weeks}")
    print(f"   节次: {course.indexes}")
    print()

print(f"最大节次索引: {max(max(course.indexes) for course in courses)}")
print(f"最小节次索引: {min(min(course.indexes) for course in courses)}")

# 统计所有使用的节次索引
all_indexes = set()
for course in courses:
    all_indexes.update(course.indexes)
print(f"所有使用的节次索引: {sorted(all_indexes)}")
