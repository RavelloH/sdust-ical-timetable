from course_parser import parse_timetable_from_xls
from collections import defaultdict

print("=== 课表解析完成 ===")
print()

# 解析课程
courses = parse_timetable_from_xls()

# 按课程名统计
course_stats = defaultdict(list)
for course in courses:
    course_stats[course.name].append(course)

print(f"总共解析到 {len(courses)} 个课程时间段，包含 {len(course_stats)} 门不同的课程：")
print()

for course_name, course_list in course_stats.items():
    print(f"📚 {course_name}")
    print(f"   教师：{course_list[0].teacher}")
    
    # 统计上课时间
    schedules = []
    for course in course_list:
        weekdays = ["", "周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        time_slots = {
            (1, 2): "第一大节",
            (3, 4): "第二大节", 
            (5, 6): "第三大节",
            (7, 8): "第四大节",
            (9, 10): "第五大节"
        }
        slot_name = time_slots.get(tuple(course.indexes), f"第{course.indexes}节")
        schedules.append(f"{weekdays[course.weekday]}{slot_name}")
    
    print(f"   时间：{' | '.join(schedules)}")
    print(f"   教室：{course_list[0].classroom}")
    week_ranges = []
    for course in course_list:
        if course.weeks:
            week_ranges.append(f"{min(course.weeks)}-{max(course.weeks)}周")
    print(f"   周次：{' | '.join(set(week_ranges))}")
    print()

print("课表.ics 文件已生成完成！可以导入到日历应用中使用。")
