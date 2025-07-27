import requests
import qrcode
import json
import os
from io import BytesIO
from typing import Optional

def upload_ics_file(file_path: str, expired_hours: int = 24) -> dict:
    """
    上传ics文件到远程存储并返回相关信息
    
    Args:
        file_path: ics文件路径
        expired_hours: 过期时间（小时），默认24小时
    
    Returns:
        包含上传结果的字典
    """
    try:
        # 读取ics文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            ics_content = f.read()
        
        # 准备上传数据
        upload_data = {
            "data": ics_content,
            "safeIP": "*.*.*.*",
            "expiredTime": expired_hours * 60 * 60 * 1000,  # 转换为毫秒
        }
        
        # 发送POST请求
        response = requests.post(
            'https://cache.ravelloh.top/api?mode=set',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(upload_data),
            timeout=30
        )
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 200:
                return {
                    'success': True,
                    'uuid': result.get('uuid'),
                    'expired_at': result.get('expiredAt'),
                    'download_url': f"https://cache.ravelloh.top/file.ics?uuid={result.get('uuid')}",
                    'message': result.get('message', '上传成功')
                }
            else:
                return {
                    'success': False,
                    'error': f"服务器返回错误：{result.get('message', '未知错误')}"
                }
        else:
            return {
                'success': False,
                'error': f"HTTP错误：{response.status_code}"
            }
            
    except requests.RequestException as e:
        return {
            'success': False,
            'error': f"网络请求失败：{str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"上传过程中发生错误：{str(e)}"
        }

def generate_qr_code(url: str, save_path: Optional[str] = None) -> str:
    """
    生成二维码
    
    Args:
        url: 要生成二维码的URL
        save_path: 保存路径，如果不提供则保存到默认位置
    
    Returns:
        二维码文件的保存路径
    """
    try:
        # 创建二维码实例
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # 添加数据
        qr.add_data(url)
        qr.make(fit=True)
        
        # 创建二维码图片
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # 确定保存路径
        if save_path is None:
            save_path = "课表二维码.png"
        
        # 保存图片
        with open(save_path, 'wb') as f:
            qr_img.save(f, 'PNG')
        return save_path
        
    except Exception as e:
        raise Exception(f"生成二维码失败：{str(e)}")

def display_qr_in_terminal(url: str):
    """在命令行中显示二维码"""
    try:
        # 创建简化的二维码用于命令行显示
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.ERROR_CORRECT_L,
            box_size=1,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # 打印二维码到终端
        qr.print_ascii(out=None, tty=False, invert=True)
        
    except Exception as e:
        print(f"❌ 无法在终端显示二维码: {str(e)}")
        print("📱 请查看保存的二维码图片文件")

def upload_and_generate_qr(ics_file_path: str, expired_hours: int = 24) -> dict:
    """
    上传ics文件并生成二维码的完整流程
    
    Args:
        ics_file_path: ics文件路径
        expired_hours: 过期时间（小时）
    
    Returns:
        包含完整结果的字典
    """
    print("🚀 正在上传课表文件...")
    
    # 上传文件
    upload_result = upload_ics_file(ics_file_path, expired_hours)
    
    if not upload_result['success']:
        return {
            'success': False,
            'error': upload_result['error']
        }
    
    print(f"✅ 上传成功！UUID: {upload_result['uuid']}")
    print(f"📅 过期时间: {upload_result['expired_at']}")
    print(f"🔗 下载链接: {upload_result['download_url']}")
    
    # 生成二维码
    print("📱 正在生成二维码...")
    try:
        qr_path = generate_qr_code(upload_result['download_url'])
        print(f"🖼️  二维码已保存到: {qr_path}")
        
        return {
            'success': True,
            'uuid': upload_result['uuid'],
            'download_url': upload_result['download_url'],
            'expired_at': upload_result['expired_at'],
            'qr_code_path': qr_path,
            'message': '课表文件已上传并生成二维码'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"二维码生成失败：{str(e)}"
        }

def display_results(result: dict):
    """显示上传和二维码生成结果"""
    if result['success']:
        print("\n" + "="*60)
        print("🎉 课表上传和二维码生成完成！")
        print("="*60)
        print(f"📱 扫描下方二维码或使用链接下载课表：")
        print(f"🔗 {result['download_url']}")
        print(f"📅 文件过期时间：{result['expired_at']}")
        print(f"🖼️  二维码文件：{result['qr_code_path']}")
        print("\n� 命令行二维码（请用手机扫描）：")
        print("-" * 60)
        
        # 在命令行显示二维码
        display_qr_in_terminal(result['download_url'])
        
        print("-" * 60)
        print("\n�💡 使用说明：")
        print("   1. 扫描上方二维码或点击链接下载 .ics 文件")
        print("   2. 在手机日历应用中导入该文件")
        print("   3. 课程将自动添加到你的日历中")
        print("📱 IOS用户请勿使用相机直接扫码，这样会自动订阅此地址，无法自己修改课程信息。")
        print("📱 请在主屏幕下滑，搜索“扫码器”，添加到日历即可")
        print("="*60)
    else:
        print(f"\n❌ 操作失败: {result['error']}")

if __name__ == "__main__":
    # 测试功能
    ics_file = "课表.ics"
    if os.path.exists(ics_file):
        result = upload_and_generate_qr(ics_file, expired_hours=48)  # 48小时后过期
        display_results(result)
    else:
        print(f"❌ 找不到文件: {ics_file}")
