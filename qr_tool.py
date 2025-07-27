#!/usr/bin/env python3
"""
课表上传和二维码生成工具
支持将本地 .ics 课表文件上传到云端并生成二维码
"""

import argparse
import os
from upload_and_qr import upload_and_generate_qr, display_results

def main():
    parser = argparse.ArgumentParser(
        description="上传课表文件并生成二维码",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  python qr_tool.py                    # 上传默认的课表.ics文件
  python qr_tool.py my_schedule.ics    # 上传指定的课表文件
  python qr_tool.py -t 48              # 设置48小时后过期
  python qr_tool.py --help             # 显示帮助信息
        """
    )
    
    parser.add_argument(
        'file', 
        nargs='?', 
        default='课表.ics',
        help='要上传的 .ics 文件路径 (默认: 课表.ics)'
    )
    
    parser.add_argument(
        '-t', '--time',
        type=int,
        default=168,  # 7天
        help='文件过期时间（小时）(默认: 168小时即7天)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='课表二维码.png',
        help='二维码输出文件名 (默认: 课表二维码.png)'
    )
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.file):
        print(f"❌ 错误：找不到文件 '{args.file}'")
        print("请确保文件路径正确，或先生成课表文件。")
        return 1
    
    # 检查文件扩展名
    if not args.file.lower().endswith('.ics'):
        print("❌ 错误：只支持 .ics 格式的日历文件")
        return 1
    
    # 显示操作信息
    print("📋 课表上传工具")
    print("=" * 40)
    print(f"📁 文件: {args.file}")
    print(f"⏰ 过期时间: {args.time} 小时")
    print(f"🖼️  二维码输出: {args.output}")
    print("=" * 40)
    
    # 执行上传和二维码生成
    try:
        result = upload_and_generate_qr(args.file, expired_hours=args.time)
        
        # 如果指定了自定义输出文件名，重命名二维码文件
        if result['success'] and args.output != '课表二维码.png':
            if os.path.exists('课表二维码.png'):
                os.rename('课表二维码.png', args.output)
                result['qr_code_path'] = args.output
        
        display_results(result)
        return 0 if result['success'] else 1
        
    except KeyboardInterrupt:
        print("\n❌ 操作被用户取消")
        return 1
    except Exception as e:
        print(f"❌ 发生未知错误: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
