#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
课表程序打包脚本
使用PyInstaller将Python程序打包成exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装")
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装 PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller 安装失败: {e}")
        return False

def create_spec_file():
    """创建PyInstaller配置文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'xlrd',
        'qrcode',
        'PIL',
        'requests',
        're',
        'glob',
        'datetime',
        'hashlib',
        'uuid',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='sdust-ical-timetable-generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    cofile=None,
    icon=None,
)
'''
    
    with open('sdust-ical-timetable-generator.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✅ 创建配置文件 sdust-ical-timetable-generator.spec")

def build_exe():
    """执行打包"""
    print("🚀 开始打包程序...")
    try:
        # 使用spec文件打包
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "sdust-ical-timetable-generator.spec"]
        subprocess.check_call(cmd)
        print("✅ 打包完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        return False

def create_release_folder():
    """创建发布文件夹"""
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # 复制exe文件
    exe_path = Path("dist") / "sdust-ical-timetable-generator.exe"
    if exe_path.exists():
        shutil.copy2(exe_path, release_dir / "sdust-ical-timetable-generator.exe")
        print(f"✅ 复制可执行文件到 {release_dir}")
    
    # 创建使用说明
    readme_content = """# 课表生成器使用说明

## 使用步骤

1. 从教务系统下载课表Excel文件(.xls或.xlsx格式)
2. 将课表文件放在与本程序相同的文件夹中
3. 双击运行"课表生成器.exe"
4. 程序会自动解析课表并生成以下文件：
   - 课表.ics：可导入到手机日历的课表文件
   - 课表二维码.png：用于手机扫码导入的二维码

## 注意事项

- 确保Excel文件格式正确（山东科技大学教务系统格式）
- 程序运行时请保持网络连接（用于上传和生成二维码）
- iOS用户建议使用"扫码器"应用导入，不要直接用相机扫码

## 技术支持

如有问题请联系开发者或查看项目GitHub页面。
"""
    
    with open(release_dir / "使用说明.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # 创建启动批处理文件
    bat_content = """@echo off
chcp 65001 >nul
echo 课表生成器
echo ====================
echo 请确保将课表Excel文件放在此文件夹中
echo ====================
pause
sdust-ical-timetable-generator.exe
pause
"""
    
    with open(release_dir / "运行程序.bat", "w", encoding="gbk") as f:
        f.write(bat_content)
    
    print(f"✅ 创建发布文件夹: {release_dir.absolute()}")

def cleanup():
    """清理临时文件"""
    cleanup_dirs = ["build", "dist", "__pycache__"]
    cleanup_files = ["sdust-ical-timetable-generator.spec"]
    
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 清理临时文件夹: {dir_name}")
    
    for file_name in cleanup_files:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🧹 清理临时文件: {file_name}")

def main():
    """主函数"""
    print("=" * 50)
    print("📦 课表程序打包工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists("main.py"):
        print("❌ 错误：请在项目根目录运行此脚本")
        return False
    
    # 检查并安装PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False
    
    try:
        # 创建配置文件
        create_spec_file()
        
        # 执行打包
        if not build_exe():
            return False
        
        # 创建发布文件夹
        create_release_folder()
        
        print("\n" + "=" * 50)
        print("🎉 打包完成！")
        print("=" * 50)
        print("📁 可执行文件位置: release/sdust-ical-timetable-generator.exe")
        print("📋 使用说明: release/使用说明.txt")
        print("🚀 快速启动: release/运行程序.bat")
        print("=" * 50)
        
        # 询问是否清理临时文件
        choice = input("\n是否清理临时文件？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是']:
            cleanup()
        
        return True
        
    except Exception as e:
        print(f"❌ 打包过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        input("\n按回车键退出...")
        sys.exit(1)
    else:
        input("\n按回车键退出...")
