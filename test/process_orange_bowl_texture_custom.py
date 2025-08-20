#!/usr/bin/env python3
"""
根据用户要求自定义橙色分布的Orange Bowl纹理处理脚本
"""
import numpy as np
from PIL import Image
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def process_orange_bowl_texture_custom():
    assets_dir = os.path.join(REPO_ROOT, 'libero', 'libero', 'assets', 'stable_scanned_objects', 'orange_bowl')
    input_path = os.path.join(assets_dir, 'texture_original_backup.png')
    output_path = os.path.join(assets_dir, 'texture.png')
    preview_path = os.path.join(REPO_ROOT, 'test', 'orange_bowl_texture_custom_preview.png')
    print(f"📁 输入文件: {input_path}")
    if not os.path.exists(input_path):
        print(f"❌ 错误: 文件不存在 {input_path}")
        return False
    img = Image.open(input_path)
    img_array = np.array(img)
    processed = img_array.copy()
    # 定义颜色
    orange_light = np.array([255, 180, 80])   # 浅橘色
    orange_medium = np.array([255, 140, 0])   # 中等橙色
    orange_standard = np.array([255, 165, 0]) # 标准橙色
    h, w = img_array.shape[:2]
    changed = 0
    for i in range(h):
        for j in range(w):
            r, g, b = img_array[i, j, :3]
            # 纯黑色背景
            if r == 0 and g == 0 and b == 0:
                continue
            # 深色区域（都小于100）
            if r < 100 and g < 100 and b < 100:
                processed[i, j, :3] = orange_light
                changed += 1
            # 白色区域（都大于200）
            elif r > 200 and g > 200 and b > 200:
                processed[i, j, :3] = orange_medium
                changed += 1
            # 其他区域
            else:
                processed[i, j, :3] = orange_standard
                changed += 1
    print(f"✅ 处理完成，变色像素数: {changed}")
    out_img = Image.fromarray(processed)
    out_img.save(output_path)
    out_img.resize((512,512), Image.LANCZOS).save(preview_path)
    print(f"✅ 新纹理已保存至: {output_path}")
    print(f"🖼️ 预览图片已保存至: {preview_path}")
    return True

if __name__ == "__main__":
    success = process_orange_bowl_texture_custom()
    if success:
        print("\n🎉 Orange Bowl 自定义纹理处理成功!")
    else:
        print("\n❌ Orange Bowl 自定义纹理处理失败!")
