"""
Apply the Qing (blue-white porcelain) pattern onto the texture while preserving
the black boundary (0,0,0) in the target texture.

Saves the result next to the originals as `texture_qing_applied.png`.

Usage (from repo root):
/absolute/path/to/python scripts/apply_qing_to_texture.py
"""
from PIL import Image, ImageChops
import os
import sys

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "libero", "libero", "assets", "stable_scanned_objects", "blue_white_porcelain")
BASE_DIR = os.path.abspath(os.path.normpath(BASE_DIR))
QING_NAME = "texture_qing.png"
TEXTURE_NAME = "texture.png"
OUT_NAME = "texture_qing_applied.png"

qing_path = os.path.join(BASE_DIR, QING_NAME)
texture_path = os.path.join(BASE_DIR, TEXTURE_NAME)
out_path = os.path.join(BASE_DIR, OUT_NAME)

if not os.path.exists(qing_path):
    print(f"Qing file not found: {qing_path}")
    sys.exit(2)
if not os.path.exists(texture_path):
    print(f"Texture file not found: {texture_path}")
    sys.exit(2)

print(f"Loading qing: {qing_path}")
print(f"Loading texture: {texture_path}")

qing = Image.open(qing_path).convert("RGBA")
texture = Image.open(texture_path).convert("RGBA")

# Resize qing to texture size if different
if qing.size != texture.size:
    print(f"Resizing qing from {qing.size} to {texture.size}")
    qing = qing.resize(texture.size, resample=Image.LANCZOS)

# --- Build masks ---
# Mask A: where qing is not white (pattern)
qing_rgb = qing.convert("RGB")
qing_px = qing_rgb.load()
w, h = qing.size
mask_pattern = Image.new("L", (w, h), 0)
mask_pattern_px = mask_pattern.load()
threshold = 240
for y in range(h):
    for x in range(w):
        r, g, b = qing_px[x, y]
        if not (r > threshold and g > threshold and b > threshold):
            mask_pattern_px[x, y] = 255

# Mask B: texture non-black (protect black boundary)
texture_rgb = texture.convert("RGB")
tex_px = texture_rgb.load()
mask_protect = Image.new("L", (w, h), 0)
mask_protect_px = mask_protect.load()
for y in range(h):
    for x in range(w):
        r, g, b = tex_px[x, y]
        if not (r == 0 and g == 0 and b == 0):
            mask_protect_px[x, y] = 255

# Combined mask: apply pattern only where pattern exists AND texture is not black
combined_mask = Image.new("L", (w, h), 0)
combined_px = combined_mask.load()
for y in range(h):
    for x in range(w):
        if mask_pattern_px[x, y] and mask_protect_px[x, y]:
            combined_px[x, y] = 255

# --- Blend strategy ---
# To preserve the original skin texture details, create a blended image by
# multiplying the original texture with the pattern (this keeps texture
# luminance and applies pattern coloring). Then composite blended over the
# original texture using the combined mask.

qing_rgb = qing.convert("RGB")
texture_rgb = texture.convert("RGB")

# Multiply keeps texture details while applying pattern color
blended = ImageChops.multiply(texture_rgb, qing_rgb)

# Composite: where combined_mask is true, use blended; else keep texture
result_rgb = Image.composite(blended, texture_rgb, combined_mask)

# Reattach original alpha channel from texture
alpha = texture.split()[-1]
result = result_rgb.convert("RGBA")
result.putalpha(alpha)

# Save result without overwriting original texture
result.save(out_path)
print(f"Saved composited texture to: {out_path}")
