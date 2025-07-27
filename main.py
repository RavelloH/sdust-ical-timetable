# Edited by: RavelloH
## 山东科技大学版
## 使用方式：在强制教育系统中，选择打印课表，将下载的xls文件放在此文件夹中，运行start.cmd即可

from data import AppleMaps, Course, EvenWeeks, Geo, OddWeeks, School, Weeks
from course_parser import parse_timetable_from_xls
from upload_and_qr import upload_and_generate_qr, display_results
import glob
import os
import shutil
import re
from datetime import datetime

# 检查是否存在xls文件
xls_files = glob.glob("*.xls") + glob.glob("*.xlsx")
print(f"SDUST 课表生成器")
print(f"https://github.com/RavelloH/sdust-ical-timetable")
print("")

def show_help_and_get_file():
    """显示帮助信息并获取文件路径"""
    print("❌ 错误：未找到Excel课表文件！")
    print("\n" + "="*60)
    print("📚 课表生成器使用说明")
    print("="*60)
    print("📋 使用步骤：")
    print("1. 前往强智教务系统的学期理论课表")
    print("   链接：https://jwgl.sdust.edu.cn/jsxsd/xskb/xskb_list.do")
    print("   点击【打印】按钮，此时会下载一个xls文件")
    print()
    print("2. 将下载的文件放在与此程序同级的文件夹下")
    print("   如果不知道此程序的同级文件夹是什么，")
    print("   请直接将下载好的文件拖入此窗口")
    print()
    print("3. 重新运行此程序")
    print("="*60)
    print()
    
    while True:
        file_path = input("💡 请将Excel文件拖入此窗口，或输入文件完整路径，随后回车（输入q退出）：").strip()
        
        if file_path.lower() == 'q':
            print("👋 程序已退出")
            exit(0)
        
        # 移除可能的引号
        file_path = file_path.strip('"\'')
        
        # 检查文件是否存在
        if os.path.exists(file_path) and (file_path.endswith('.xls') or file_path.endswith('.xlsx')):
            # 复制文件到当前目录
            filename = os.path.basename(file_path)
            try:
                shutil.copy2(file_path, filename)
                print(f"✅ 文件已复制到当前目录：{filename}")
                return filename
            except Exception as e:
                print(f"❌ 文件复制失败：{e}")
                continue
        else:
            print("❌ 文件不存在或格式不正确，请确保文件是.xls或.xlsx格式")
            continue

if not xls_files:
    target_file = show_help_and_get_file()
    xls_files = [target_file]

print(f"找到课表文件: {xls_files[0]}")
print("正在解析课表...")

# 自动解析课程
auto_courses = parse_timetable_from_xls()

if not auto_courses:
    print("错误：未能解析到任何课程信息！")
    exit(1)

print(f"成功解析到 {len(auto_courses)} 个课程时间段")

# 统计课程数量
course_names = set(course.name for course in auto_courses)
print(f"包含 {len(course_names)} 门不同的课程")
print()

# 获取开学时间
def get_start_date():
    """获取开学日期"""
    print("📅 请输入开学日期")
    print("📋 格式：YYYY-MM-DD 或 YYYY/MM/DD 或 YYYY.MM.DD")
    print("📋 示例：2025-09-01 或 2025/9/1 或 2025.9.1")
    print()
    
    while True:
        date_input = input("请输入开学日期：").strip()
        
        if not date_input:
            print("❌ 日期不能为空，请重新输入")
            continue
            
        # 尝试多种日期格式
        
        # 替换分隔符为统一的横线
        date_input = re.sub(r'[/.]', '-', date_input)
        
        try:
            # 解析日期
            date_obj = datetime.strptime(date_input, '%Y-%m-%d')
            year = date_obj.year
            month = date_obj.month
            day = date_obj.day
            
            # 验证日期合理性
            if year < 2020 or year > 2030:
                print("❌ 年份应在2020-2030之间，请重新输入")
                continue
                
            print(f"✅ 开学日期设置为：{year}年{month}月{day}日")
            return (year, month, day)
            
        except ValueError:
            print("❌ 日期格式错误，请使用正确格式（如：2025-09-01）")
            continue

start_date = get_start_date()
print()

# 定位靠IOS了，安卓不支持

school = School(
    duration=110,   # 每节课时间为 110 分钟
    timetable=[
        (8, 0),     # 第1节课开始时间
        (8, 0),     # 第2节课开始时间（第一大节的第二节）
        (10, 10),   # 第3节课开始时间  
        (10, 10),   # 第4节课开始时间（第二大节的第二节）
        (14, 0),    # 第5节课开始时间
        (14, 0),    # 第6节课开始时间（第三大节的第二节）
        (16, 10),   # 第7节课开始时间
        (16, 10),   # 第8节课开始时间（第四大节的第二节）
        (19, 0),    # 第9节课开始时间
        (19, 0),    # 第10节课开始时间（第五大节的第二节）
    ],
    start=start_date,  # 使用用户输入的开学时间
    courses=auto_courses  # 使用自动解析的课程列表
)

with open("课表.ics", "w", encoding = "utf-8") as w:
    w.write(school.generate())

print("✅ 课表.ics 文件生成成功！")
print("📅 现在可以将此文件导入到你的日历应用中（如手机日历、Outlook等）")
print("📚 课程信息已按照实际的上课时间和周次安排好")
print("📱 IOS用户请勿使用相机直接扫码，这样会自动订阅此地址，无法自己修改课程信息。")
print("📱 请在主屏幕下滑，搜索“扫码器”，添加到日历即可")

# 自动上传并生成二维码
print("\n🚀 正在上传课表并生成二维码...")
upload_result = upload_and_generate_qr("课表.ics", expired_hours=168)  # 7天后过期
display_results(upload_result)

print("\n" + "="*60)
print("🎉 所有任务完成！")
print("📁 生成的文件：")
print("   - 课表.ics：可导入日历的课表文件")
print("   - 课表二维码.png：扫码导入用的二维码图片")
print("="*60)
input("\n📱 按回车键退出程序...")
