# 📚 SDUST 课表 (.ics) 生成工具
> 本工具基于 [junyilou/python-ical-timetable](https://github.com/junyilou/python-ical-timetable) 修改。

![sdust](image/sdust.jpg)

两步即可生成你的课表日历文件 (.ics)，支持 iOS、Android 等手机日历导入。  
其中，地图定位及预测出发时间功能依赖于 iOS 的 Apple Maps，安卓无法使用。

相比原项目，增加了以下功能：
- 适配 SDUST 课表格式
- 支持从 Excel 文件导入课表
- 支持手机扫描二维码快速导入课表
- 打包为exe

## 使用
1. 前往[Releases](https://github.com/junyilou/python-ical-timetable/releases)下载最新版本的可执行文件。
2. 运行此文件，随后完成以下步骤：
  1. 前往[教务系统的学期理论课表](https://jwgl.sdust.edu.cn/jsxsd/xskb/xskb_list.do)页面，点击打印，下载生成的xls文件
  2. 将下载的文件拖入程序，或者放在程序同目录下，再重新运行程序
  3. 输入学期开始日期（格式如2025-09-01）
  4. 导入生成的课表即可。可直接扫描生成的二维码来导入

如果你是Mac、Linux用户，或者想要酷炫的命令行体验:

```
git clone https://github.com/RavelloH/sdust-ical-timetable
cd sdust-ical-timetable
pip install -r requirements.txt
python main.py
```

## 开发
项目在以下方面有改进空间。如果你想为项目做贡献，可以从以下几个方面入手：
- 自动获取学期开始时间。也许可以直接读取excel里的学期信息，例如2025-2026-1，这个大概是2025年9月1日开学。
- 优化打包大小。现在这么简单的程序打包后有40M，虽说确实包含了整个python运行环境，但太不优雅了。
- 创建完整的地图系统。详见原项目，如果你有充足的时间，可以把全校所有建筑物的信息录入到程序，之后映射一下。这样在Android上应该也能用地图了。（不过安卓似乎没有预计到达时间的功能，有地图也用处不大）
