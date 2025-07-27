from course_parser import parse_timetable_from_xls

courses = parse_timetable_from_xls()
unique_courses = set(course.name for course in courses)

print(f'课程总数: {len(courses)}')
print(f'不同课程: {len(unique_courses)}')
print('\n不同课程列表:')
for i, course in enumerate(sorted(unique_courses), 1):
    print(f'{i:2d}. {course}')
