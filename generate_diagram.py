# -*- coding: utf-8 -*-
"""
智慧宠物店管理系统 - 功能模块关系图
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as path_effects

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建画布
fig, ax = plt.subplots(1, 1, figsize=(20, 16))
ax.set_xlim(0, 20)
ax.set_ylim(0, 16)
ax.axis('off')

# 标题
title = ax.text(10, 15.3, '智慧宠物店管理系统 - 功能模块关系图',
                fontsize=20, fontweight='bold', ha='center', va='center',
                color='#2c3e50')
title.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])

# 定义颜色
colors = {
    'module1': '#e74c3c',   # 红色 - 宠物管理
    'module2': '#9b59b6',   # 紫色 - 识别模块
    'module3': '#f39c12',   # 橙色 - 服务管理
    'module4': '#1abc9c',   # 青色 - 领养管理
    'module5': '#e67e22',   # 深橙 - 商品管理
    'module6': '#2ecc71',   # 绿色 - 会员管理
    'module7': '#34495e',   # 深灰 - 统计
    'module8': '#95a5a6',   # 灰色 - 系统管理
    'arrow': '#7f8c8d',
}

def draw_module(ax, x, y, width, height, title, features, color, title_color='white'):
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.05,rounding_size=0.2",
                         facecolor=color, edgecolor='white',
                         linewidth=2, alpha=0.9, zorder=2)
    ax.add_patch(box)
    
    ax.text(x + width/2, y + height - 0.4, title,
            fontsize=11, fontweight='bold', ha='center', va='center',
            color=title_color, zorder=3)
    
    ax.plot([x + 0.2, x + width - 0.2], [y + height - 0.7, y + height - 0.7],
            color='white', linewidth=1, alpha=0.5, zorder=3)
    
    feature_text = '\n'.join([f'• {f}' for f in features])
    ax.text(x + 0.3, y + height - 1.0, feature_text,
            fontsize=8, ha='left', va='top',
            color=title_color, linespacing=1.4, zorder=3)

def draw_arrow(ax, start, end, color='#7f8c8d', label='', offset=(0, 0)):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5,
                               connectionstyle="arc3,rad=0"))
    if label:
        mid_x = (start[0] + end[0]) / 2 + offset[0]
        mid_y = (start[1] + end[1]) / 2 + offset[1]
        ax.text(mid_x, mid_y, label, fontsize=7, ha='center', va='center',
               color=color, bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

def draw_dashed_arrow(ax, start, end, color='#95a5a6', label=''):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2,
                               linestyle='dashed',
                               connectionstyle="arc3,rad=0"))
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y, label, fontsize=7, ha='center', va='center',
               color=color, style='italic')

# 第一行模块
draw_module(ax, 0.5, 11.5, 4.2, 2.8,
            '宠物档案管理',
            ['档案创建/修改/删除', '宠物信息查询', '健康记录管理', '服务历史查看', '照片档案管理'],
            colors['module1'])

draw_module(ax, 5.3, 11.5, 4.2, 2.8,
            '品种智能识别',
            ['图像采集上传', 'AI品种识别', '识别结果展示', '档案自动填充', '识别记录查询'],
            colors['module2'])

draw_module(ax, 10.1, 11.5, 4.2, 2.8,
            '服务工单管理',
            ['工单创建与分配', '服务进度跟踪', '状态流转管理', '费用结算', '服务评价反馈'],
            colors['module3'])

draw_module(ax, 14.9, 11.5, 4.6, 2.8,
            '领养中心管理',
            ['领养信息发布', '领养申请提交', '审核流程管理', '状态跟踪查询', '回访记录管理'],
            colors['module4'])

# 第二行模块
draw_module(ax, 0.5, 7.5, 4.2, 2.8,
            '商品商城管理',
            ['商品分类浏览', '购物车管理', '订单创建处理', '支付结算', '物流跟踪'],
            colors['module5'])

draw_module(ax, 5.3, 7.5, 4.2, 2.8,
            '会员中心管理',
            ['会员注册登录', '个人信息维护', '积分查询管理', '消费记录查看', '会员等级权益'],
            colors['module6'])

draw_module(ax, 10.1, 7.5, 4.2, 2.8,
            '数据统计看板',
            ['业务数据汇总', '图表可视化', '趋势分析展示', '报表导出', '经营数据洞察'],
            colors['module7'])

draw_module(ax, 14.9, 7.5, 4.6, 2.8,
            '系统管理设置',
            ['用户权限管理', '参数配置', '操作日志审计', '数据备份恢复', '系统公告发布'],
            colors['module8'])

# 基础数据层
draw_module(ax, 0.5, 4.0, 19, 2.5,
            '基础数据层',
            ['客户数据  |  宠物数据  |  商品数据  |  服务项目数据  |  库存数据  |  领养规则配置'],
            '#34495e')

# 技术支撑层
draw_module(ax, 0.5, 1.2, 19, 2.0,
            '技术支撑层',
            ['用户认证与权限  |  AI图像识别引擎  |  消息通知服务  |  支付网关集成  |  数据分析引擎  |  日志监控'],
            '#2c3e50')

# 绘制连接箭头
# 品种识别 -> 宠物档案 (虚线)
draw_dashed_arrow(ax, (7.4, 13.0), (4.7, 13.0), '#9b59b6', '自动填充')

# 宠物档案 -> 会员中心
draw_arrow(ax, (4.7, 11.5), (7.4, 10.3), colors['arrow'], '档案归属', (0, 0.3))

# 服务工单 -> 数据统计
draw_arrow(ax, (12.2, 11.5), (12.2, 10.3), colors['arrow'], '工单数据')

# 领养中心 -> 数据统计
draw_arrow(ax, (17.2, 11.5), (14.9, 10.3), colors['arrow'], '领养数据')

# 商品商城 -> 数据统计
draw_arrow(ax, (12.2, 7.5), (12.2, 10.3), colors['arrow'], '销售数据')

# 会员中心 -> 商品商城
draw_arrow(ax, (4.7, 7.5), (4.7, 10.3), colors['arrow'], '客户下单')

# 第二行 -> 基础数据层
draw_arrow(ax, (2.6, 7.5), (2.6, 6.5), colors['arrow'])
draw_arrow(ax, (7.4, 7.5), (7.4, 6.5), colors['arrow'])
draw_arrow(ax, (12.2, 7.5), (12.2, 6.5), colors['arrow'])
draw_arrow(ax, (17.2, 7.5), (17.2, 6.5), colors['arrow'])

# 基础数据层 -> 技术支撑层
draw_arrow(ax, (10, 4.0), (10, 3.2), colors['arrow'])

# 图例说明
legend_text = "模块关系说明:\n  -> 实线箭头: 业务调用/数据流向\n  - - 虚线箭头: 自动处理/数据填充\n  每个模块独立运作，通过数据层实现信息共享"
ax.text(0.5, 0.3, legend_text, fontsize=8, ha='left', va='bottom',
        color='#7f8c8d', style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8f9fa', alpha=0.8))

# 保存图片
plt.tight_layout()
plt.savefig('system_module_diagram.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('图片已生成: system_module_diagram.png')
