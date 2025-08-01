import pandas as pd
import re
import glob
from data import Course, Weeks, OddWeeks, EvenWeeks, Geo

def normalize_course_name(course_name: str) -> str:
    """
    规范化课程名称，去除所有括号及其内容
    例如：电路（2） -> 电路
         大学英语（A）（2-2） -> 大学英语
    """
    if not course_name:
        return course_name
    
    normalized_name = course_name.strip()
    
    # 去除所有中文括号及其内容
    normalized_name = re.sub(r'（[^）]*）', '', normalized_name)
    
    # 去除所有英文括号及其内容
    normalized_name = re.sub(r'\([^)]*\)', '', normalized_name)
    
    # 去除多余的空格
    normalized_name = re.sub(r'\s+', ' ', normalized_name).strip()
    
    return normalized_name

def normalize_classroom_name(classroom: str) -> str:
    """
    规范化教室名称，处理不规范的写法
    例如：Js1-305室 -> S1-305室
    """
    if not classroom:
        return classroom
    
    classroom = classroom.strip()
    
    # 规范化教室名称 - 处理不规范的写法
    # Js1-305室 -> S1-305室
    classroom = re.sub(r'^Js(\d+)', r'S\1', classroom)
    
    return classroom

def classroom_to_location(classroom: str, course_name: str = "") -> str:
    """
    将教室名转换为地图位置格式
    例如：J7-106室 -> 山东科技大学J7
         品学楼B107 -> 山东科技大学品学楼
         线上虚拟教室 -> 返回空字符串（不设置位置）
         体育课程 -> 返回空字符串（不设置位置）
         未知教室 -> 返回空字符串（不设置位置）
    """
    if not classroom or classroom.strip() == "":
        return ""
    
    classroom = classroom.strip()
    course_name = course_name.strip()
    
    # 规范化教室名称 - 处理不规范的写法
    classroom = normalize_classroom_name(classroom)
    
    # 如果是未知教室，不设置位置
    if classroom == "未知教室":
        return ""
    
    # 如果是线上虚拟教室，不设置位置
    if classroom == "线上虚拟教室":
        return ""
    
    # 如果课程名包含"体育"，不设置位置
    if "体育" in course_name:
        return ""
    
    # 如果是其他线上课程，直接返回
    if "线上" in classroom or "虚拟" in classroom:
        return classroom
    
    # 提取建筑物名称
    building_patterns = [
        (r'^(J\d+)-\d+室?$', r'山东科技大学\1'),           # J7-106室 -> 山东科技大学J7
        (r'^(S\d+)-\d+室?$', r'山东科技大学\1'),           # S1-305室 -> 山东科技大学S1
        (r'^(JB区[^-室]+)', r'山东科技大学\1'),            # JB区乒乓球馆室 -> 山东科技大学JB区乒乓球馆
        (r'^实训.+-\d+室?$', r'山东科技大学工程实训大楼'),    # 实训6层-610室 -> 山东科技大学工程实训大楼
        (r'^([^-]*?[^\d-])[A-Z]?\d+.*$', r'山东科技大学\1'),  # 品学楼B107 -> 山东科技大学品学楼
    ]
    
    for pattern, replacement in building_patterns:
        match = re.match(pattern, classroom)
        if match:
            return re.sub(pattern, replacement, classroom)
    
    # 如果没有匹配到特定格式，添加默认前缀
    return f"山东科技大学{classroom}"

def parse_course_info(course_text):
    """解析课程信息文本，提取课程名、教师、周次、教室等信息"""
    if pd.isna(course_text) or not course_text.strip():
        return []
    
    courses = []
    # 按换行符分割课程信息
    lines = [line.strip() for line in course_text.strip().split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        # 课程名
        course_name = lines[i]
        
        if i + 1 < len(lines):
            # 教师信息，格式：姓名(职称)
            teacher_info = lines[i + 1]
            teacher_match = re.match(r'([^(]+)\([^)]*\)', teacher_info)
            teacher = teacher_match.group(1) if teacher_match else teacher_info
        else:
            teacher = "未知教师"
            
        if i + 2 < len(lines):
            # 周次信息，格式：1-12[周] 或 1,3,5[周] 等
            week_info = lines[i + 2]
            weeks = parse_weeks(week_info)
        else:
            weeks = []
            
        if i + 3 < len(lines):
            # 教室信息
            classroom = lines[i + 3]
        else:
            classroom = "未知教室"
            
        if course_name and weeks:  # 只有有效的课程名和周次才添加
            courses.append({
                'name': normalize_course_name(course_name),  # 使用规范化的课程名
                'teacher': teacher,
                'weeks': weeks,
                'classroom': normalize_classroom_name(classroom)  # 使用规范化的教室名
            })
        
        i += 4  # 跳过已处理的4行
    
    return courses

def parse_weeks(week_text):
    """解析周次信息"""
    if not week_text:
        return []
    
    # 移除[周]或[单周]或[双周]标记
    week_text = re.sub(r'\[(单|双)?周\]', '', week_text)
    
    weeks = []
    
    # 处理复杂的周次表达式，如 "1-11,13-14"
    parts = week_text.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            # 处理范围，如 1-12
            range_match = re.match(r'(\d+)-(\d+)', part)
            if range_match:
                start, end = range_match.groups()
                weeks.extend(range(int(start), int(end) + 1))
        else:
            # 处理单独的数字
            number_match = re.match(r'(\d+)', part)
            if number_match:
                weeks.append(int(number_match.group(1)))
    
    return sorted(list(set(weeks)))  # 去重并排序

def time_slot_to_index(slot_name):
    """将时间段名称转换为索引"""
    slot_mapping = {
        '第一大节': [1, 2],
        '第二大节': [3, 4], 
        '第三大节': [5, 6],
        '第四大节': [7, 8],
        '第五大节': [9, 10]
    }
    return slot_mapping.get(slot_name, [])

def weekday_name_to_number(weekday_name):
    """将星期名称转换为数字"""
    weekday_mapping = {
        '星期一': 1,
        '星期二': 2,
        '星期三': 3,
        '星期四': 4,
        '星期五': 5,
        '星期六': 6,
        '星期日': 7
    }
    return weekday_mapping.get(weekday_name, 0)

def merge_duplicate_courses(courses):
    """合并相同课程的不同时间段"""
    merged = {}
    
    for course in courses:
        # 创建课程的唯一标识
        key = (course['name'], course['teacher'], course['classroom'])
        
        if key in merged:
            # 如果是同一门课程，添加新的时间段信息
            merged[key]['schedules'].append({
                'weekday': course['weekday'],
                'weeks': course['weeks'],
                'indexes': course['indexes']
            })
        else:
            # 新课程
            merged[key] = {
                'name': course['name'],
                'teacher': course['teacher'],
                'classroom': course['classroom'],
                'schedules': [{
                    'weekday': course['weekday'],
                    'weeks': course['weeks'],
                    'indexes': course['indexes']
                }]
            }
    
    # 转换为Course对象列表
    result = []
    for course_info in merged.values():
        for schedule in course_info['schedules']:
            result.append(Course(
                name=course_info['name'],
                teacher=course_info['teacher'],
                classroom=course_info['classroom'],
                location=classroom_to_location(course_info['classroom'], course_info['name']),  # 传入课程名用于判断
                weekday=schedule['weekday'],
                weeks=schedule['weeks'],
                indexes=schedule['indexes']
            ))
    
    return result

def parse_timetable_from_xls():
    """从xls文件解析课表并返回Course对象列表"""
    xls_files = glob.glob("*.xls") + glob.glob("*.xlsx")
    if not xls_files:
        print("未找到Excel文件")
        return []
    
    file_path = xls_files[0]
    print(f"正在解析文件: {file_path}")
    
    df = pd.read_excel(file_path, sheet_name=0)
    
    courses = []
    
    # 从第2行开始（索引1），第1行是星期标题
    weekdays = []
    for col in range(1, len(df.columns)):
        cell_value = df.iloc[1, col]
        if pd.notna(cell_value) and '星期' in str(cell_value):
            weekdays.append((col, str(cell_value)))
    
    print(f"发现的星期列: {weekdays}")
    
    # 从第3行开始解析课程（索引2），因为第1行是标题，第2行是星期
    for row_idx in range(2, len(df)):
        time_slot = df.iloc[row_idx, 0]
        if pd.isna(time_slot) or '第' not in str(time_slot):
            continue
            
        time_indexes = time_slot_to_index(str(time_slot))
        if not time_indexes:
            continue
        
        # 遍历每个星期列
        for col_idx, weekday_name in weekdays:
            if col_idx >= len(df.columns):
                continue
                
            cell_content = df.iloc[row_idx, col_idx]
            if pd.isna(cell_content):
                continue
                
            weekday_num = weekday_name_to_number(weekday_name)
            if weekday_num == 0:
                continue
                
            # 解析该单元格中的课程信息
            course_infos = parse_course_info(str(cell_content))
            
            for course_info in course_infos:
                courses.append({
                    'name': course_info['name'],
                    'teacher': course_info['teacher'],
                    'classroom': course_info['classroom'],
                    'weekday': weekday_num,
                    'weeks': course_info['weeks'],
                    'indexes': time_indexes
                })
    
    # 合并重复课程并转换为Course对象
    merged_courses = merge_duplicate_courses(courses)
    
    print(f"总共解析到 {len(merged_courses)} 门课程")
    print_course_summary(merged_courses)
    return merged_courses

def print_course_summary(courses):
    """打印课程总结信息"""
    print("\n" + "="*50)
    print("📚 课程总结")
    print("="*50)
    
    # 按课程名分组统计
    course_stats = {}
    for course in courses:
        key = (course.name, course.teacher)
        if key not in course_stats:
            course_stats[key] = {
                'name': course.name,
                'teacher': course.teacher,
                'total_classes': 0,
                'weekdays': set(),
                'classrooms': set(),
                'weeks_range': set()
            }
        
        # 计算每个时间段的总课时数
        course_stats[key]['total_classes'] += len(course.weeks)
        course_stats[key]['weekdays'].add(course.weekday)
        course_stats[key]['classrooms'].add(course.classroom)
        course_stats[key]['weeks_range'].update(course.weeks)
    
    weekday_names = {1: '周一', 2: '周二', 3: '周三', 4: '周四', 5: '周五', 6: '周六', 7: '周日'}
    
    total_courses = len(course_stats)
    total_classes = sum(stats['total_classes'] for stats in course_stats.values())
    
    print(f"📊 课程数量：{total_courses} 门课程")
    print(f"📅 总课时数：{total_classes} 次课")
    print()
    
    # 按课程名排序显示详细信息
    for i, (key, stats) in enumerate(sorted(course_stats.items()), 1):
        name, teacher = key
        weekdays_str = '、'.join(sorted([weekday_names[wd] for wd in stats['weekdays']]))
        weeks_list = sorted(stats['weeks_range'])
        weeks_str = f"{min(weeks_list)}-{max(weeks_list)}周" if weeks_list else "无"
        classrooms_str = '、'.join(sorted(stats['classrooms']))
        
        print(f"{i:2d}. 📖 {name}")
        print(f"    👨‍🏫 教师：{teacher}")
        print(f"    📅 上课时间：{weekdays_str}")
        print(f"    🏫 教室：{classrooms_str}")
        print(f"    📊 课时安排：{stats['total_classes']} 次课 ({weeks_str})")
        print()
    
    print("="*50)
