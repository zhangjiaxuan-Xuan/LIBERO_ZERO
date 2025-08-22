#!/usr/bin/env python3
"""
Create a white-base porcelain texture and overlay qinghuaci pattern.
Saves backups for original files and writes updated `texture.png`.
Also writes a new XML `blue_white_porcelain.xml` based on `akita_black_bowl.xml` with updated names.
"""
from PIL import Image, ImageOps
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1] / "libero/libero/assets/stable_scanned_objects/blue_white_porcelain"
qing = ROOT / "qinghuaci.png"
tex = ROOT / "texture.png"
xml_src = ROOT / "akita_black_bowl.xml"
xml_dst = ROOT / "blue_white_porcelain.xml"

if not qing.exists() or not tex.exists() or not xml_src.exists():
    print("Required files missing:")
    for p in (qing, tex, xml_src):
        print(p, "->", p.exists())
    sys.exit(1)

# Backups
qing_backup = ROOT / "qinghuaci_orig.png"
tex_backup = ROOT / "texture_orig.png"
xml_backup = ROOT / "akita_black_bowl.xml.bak"

if not qing_backup.exists():
    Image.open(str(qing)).save(str(qing_backup))
    print("Backed up qinghuaci to", qing_backup)
else:
    print("Backup exists for qinghuaci", qing_backup)

if not tex_backup.exists():
    Image.open(str(tex)).save(str(tex_backup))
    print("Backed up texture to", tex_backup)
else:
    print("Backup exists for texture", tex_backup)

if not xml_backup.exists():
    # copy xml to backup
    with open(xml_src, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(xml_backup, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Backed up xml to", xml_backup)
else:
    print("Backup exists for xml", xml_backup)

# Load images
qing_img = Image.open(str(qing_backup)).convert('RGBA')
tex_img = Image.open(str(tex_backup)).convert('RGBA')

w, h = tex_img.size
if qing_img.size != tex_img.size:
    # resize qinghuaci to texture size
    qing_img = qing_img.resize((w, h), resample=Image.LANCZOS)
    print("Resized qinghuaci to", (w,h))

# Process texture: preserve (0,0,0) areas, make non-(0,0,0) areas white-series background
import numpy as np
tex_arr = np.array(tex_img)

# Find areas that are NOT (0,0,0) - these are the valid mesh areas
valid_mask = ~((tex_arr[:,:,0] == 0) & (tex_arr[:,:,1] == 0) & (tex_arr[:,:,2] == 0))

# Create white base from texture luminance but only for valid areas
gray = ImageOps.grayscale(tex_img)
lum = np.array(gray).astype('float32') / 255.0
# Create white base: value range 230..255 depending on luminance (preserve subtle shading)
base_vals = (230 + lum * 25).clip(0,255).astype('uint8')
base_rgb = np.stack([base_vals]*3, axis=2)

# Start with original texture
result_arr = tex_arr.copy()

# Replace non-(0,0,0) areas with white base
result_arr[valid_mask] = np.column_stack([base_rgb[valid_mask], tex_arr[valid_mask,3]])

# Extract pattern from qinghuaci: non-white pixels
qarr = np.array(qing_img)
white_thresh = 240
qing_pattern_mask = (qarr[:,:,0] < white_thresh) | (qarr[:,:,1] < white_thresh) | (qarr[:,:,2] < white_thresh)

# Apply qinghuaci pattern only to valid mesh areas (not (0,0,0))
final_pattern_mask = valid_mask & qing_pattern_mask

# Overlay qinghuaci colors where both valid mesh area AND qinghuaci has pattern
result_arr[final_pattern_mask] = np.column_stack([qarr[final_pattern_mask,:3], tex_arr[final_pattern_mask,3]])

result = Image.fromarray(result_arr, mode='RGBA')

# Save result as texture.png (overwrite)
result.save(str(tex))
print("Wrote updated texture to", tex)

# Create new xml file based on original but with new model/material/texture names
with open(str(xml_src), 'r', encoding='utf-8') as f:
    xml = f.read()

new_xml = xml.replace('mujoco model="akita_black_bowl"', 'mujoco model="blue_white_porcelain"')
new_xml = new_xml.replace('texture file="texture.png" name="tex-akita_black_bowl"', 'texture file="texture.png" name="tex-blue_white_porcelain"')
new_xml = new_xml.replace('material name="akita_black_bowl"', 'material name="blue_white_porcelain"')
new_xml = new_xml.replace('mesh file="visual/akita_black_bowl_vis.msh" name="akita_black_bowl_vis"', 'mesh file="visual/akita_black_bowl_vis.msh" name="blue_white_porcelain_vis"')

with open(str(xml_dst), 'w', encoding='utf-8') as f:
    f.write(new_xml)
print('Wrote new xml', xml_dst)

print('Done.')
