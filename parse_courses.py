import pandas as pd
import re
import glob
from data import Course, Weeks, OddWeeks, EvenWeeks

def parse_course_info(course_text):
    """解析课程信息文本，提取课程名、教师、周次、教室等信息"""
    if pd.isna(course_text) or not course_text.strip():
        return []
    
    courses = []
    # 按换行符分割，然后按模式匹配
    lines = course_text.strip().split('\n')
    
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
            
        # 课程名
        course_name = lines[i].strip()
        if i + 1 < len(lines):
            # 教师信息，格式：姓名(职称)
            teacher_info = lines[i + 1].strip()
            teacher_match = re.match(r'([^(]+)\([^)]*\)', teacher_info)
            teacher = teacher_match.group(1) if teacher_match else teacher_info
            
        if i + 2 < len(lines):
            # 周次信息，格式：1-12[周] 或 1,3,5[周] 等
            week_info = lines[i + 2].strip()
            weeks = parse_weeks(week_info)
            
        if i + 3 < len(lines):
            # 教室信息
            classroom = lines[i + 3].strip()
            
            courses.append({
                'name': course_name,
                'teacher': teacher,
                'weeks': weeks,
                'classroom': classroom
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
    # 处理范围，如 1-12
    range_matches = re.findall(r'(\d+)-(\d+)', week_text)
    for start, end in range_matches:
        weeks.extend(range(int(start), int(end) + 1))
    
    # 处理单独的数字，如 1,3,5
    single_matches = re.findall(r'(?<!\d)(\d+)(?![-\d])', week_text)
    for week in single_matches:
        weeks.append(int(week))
    
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

def parse_timetable_from_xls():
    """从xls文件解析课表"""
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
            
        print(f"处理时间段: {time_slot} -> 索引: {time_indexes}")
        
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
                print(f"解析到课程: {course_info}")
                courses.append({
                    'name': course_info['name'],
                    'teacher': course_info['teacher'],
                    'classroom': course_info['classroom'],
                    'weekday': weekday_num,
                    'weeks': course_info['weeks'],
                    'indexes': time_indexes
                })
    
    return courses

if __name__ == "__main__":
    courses = parse_timetable_from_xls()
    print(f"\n总共解析到 {len(courses)} 门课程:")
    for i, course in enumerate(courses, 1):
        print(f"{i}. {course['name']} - {course['teacher']} - 星期{course['weekday']} - 第{course['indexes']}节 - 周次{course['weeks']} - {course['classroom']}")
