#!/usr/bin/env python3
"""
批量创建 LIBERO_0 的所有10个任务文件
基于 libero_goal 的任务，替换物品名称
"""

import os
import sys

# 添加 LIBERO 路径
sys.path.insert(0, '/home/x/anaconda3/envs/openvla-oft/LIBERO')

def create_libero_0_tasks():
    """创建所有 LIBERO_0 任务"""
    
    # 原始和目标目录
    goal_dir = "/home/x/anaconda3/envs/openvla-oft/LIBERO/libero/libero/bddl_files/libero_goal"
    libero_0_dir = "/home/x/anaconda3/envs/openvla-oft/LIBERO/libero/libero/bddl_files/libero_0"
    
    # 物品映射关系
    object_mappings = {
        'akita_black_bowl': 'blue_white_porcelain_bowl',
        'wine_bottle': 'moutai',
        'cream_cheese': 'butter',
        'plate': 'saucer',
        'wooden_cabinet': 'white_cabinet'
    }
    
    # 任务映射关系 (原始任务名 -> 新任务名)
    task_mappings = {
        'open_the_middle_drawer_of_the_cabinet.bddl': 'open_the_middle_drawer_of_the_white_cabinet.bddl',
        'open_the_top_drawer_and_put_the_bowl_inside.bddl': 'open_the_top_drawer_and_put_the_blue_white_porcelain_bowl_inside.bddl',
        'push_the_plate_to_the_front_of_the_stove.bddl': 'push_the_saucer_to_the_front_of_the_stove.bddl',
        'put_the_bowl_on_the_plate.bddl': 'put_the_blue_white_porcelain_bowl_on_the_saucer.bddl',
        'put_the_bowl_on_the_stove.bddl': 'put_the_blue_white_porcelain_bowl_on_the_stove.bddl',
        'put_the_bowl_on_top_of_the_cabinet.bddl': 'put_the_blue_white_porcelain_bowl_on_top_of_the_white_cabinet.bddl',
        'put_the_cream_cheese_in_the_bowl.bddl': 'put_the_butter_in_the_blue_white_porcelain_bowl.bddl',
        'put_the_wine_bottle_on_the_rack.bddl': 'put_the_moutai_on_the_rack.bddl',
        'put_the_wine_bottle_on_top_of_the_cabinet.bddl': 'put_the_moutai_on_top_of_the_white_cabinet.bddl',
        'turn_on_the_stove.bddl': 'turn_on_the_stove.bddl'  # 这个任务不需要改名
    }
    
    print("🚀 开始创建 LIBERO_0 的所有10个任务...")
    
    # 处理每个任务
    for original_task, new_task in task_mappings.items():
        original_path = os.path.join(goal_dir, original_task)
        new_path = os.path.join(libero_0_dir, new_task)
        
        if not os.path.exists(original_path):
            print(f"❌ 原始任务文件不存在: {original_path}")
            continue
            
        print(f"📝 处理任务: {original_task} -> {new_task}")
        
        # 读取原始文件
        with open(original_path, 'r') as f:
            content = f.read()
        
        # 替换物品名称
        for old_name, new_name in object_mappings.items():
            content = content.replace(old_name, new_name)
        
        # 写入新文件
        with open(new_path, 'w') as f:
            f.write(content)
        
        print(f"✅ 已创建: {new_task}")
    
    print(f"\n🎉 成功创建了 {len(task_mappings)} 个 LIBERO_0 任务文件!")
    
    # 更新 tasks_info.txt
    update_tasks_info(libero_0_dir, list(task_mappings.values()))

def update_tasks_info(libero_0_dir, task_list):
    """更新 tasks_info.txt 文件"""
    tasks_info_path = os.path.join(libero_0_dir, "tasks_info.txt")
    
    print(f"\n📋 更新 tasks_info.txt...")
    
    content = "# LIBERO_0 Zero-shot Learning Environment Tasks\\n"
    content += "# Based on libero_goal with object substitutions\\n\\n"
    
    for i, task in enumerate(task_list, 1):
        task_name = task.replace('.bddl', '')
        content += f"{i:2d}. {task_name}\\n"
    
    content += f"\\nTotal: {len(task_list)} tasks\\n"
    content += "\\n# Object Mappings:\\n"
    content += "# akita_black_bowl → blue_white_porcelain_bowl\\n"
    content += "# wine_bottle → moutai\\n"  
    content += "# cream_cheese → butter\\n"
    content += "# plate → saucer\\n"
    content += "# wooden_cabinet → white_cabinet\\n"
    
    with open(tasks_info_path, 'w') as f:
        f.write(content)
    
    print(f"✅ 已更新 tasks_info.txt")

if __name__ == "__main__":
    create_libero_0_tasks()
    print("\\n🎯 LIBERO_0 环境创建完成！")
