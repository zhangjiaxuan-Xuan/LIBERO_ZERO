# Init Files Fix Summary

## 问题诊断
原始错误是由于 init_states 文件缺失或命名不匹配导致的 `FileNotFoundError`。

## 根本原因
1. **缺少 libero_goal_new 的 init 文件**
2. **缺少 libero_spatial_orange 的 init 文件** 
3. **文件名不匹配**: 复制的 init 文件保持原始名称（black_bowl），但 BDDL 文件已更新为新名称（orange_bowl, blue_bottle）

## 解决方案

### 1. 创建 libero_goal_new init 文件
```bash
cp -r libero_goal libero_goal_new
# 重命名 wine_bottle 相关文件为 blue_bottle
mv put_the_wine_bottle_on_the_rack.pruned_init put_the_blue_bottle_on_the_rack.pruned_init
mv put_the_wine_bottle_on_top_of_the_cabinet.pruned_init put_the_blue_bottle_on_top_of_the_cabinet.pruned_init
```

### 2. 创建 libero_spatial_orange init 文件
```bash
cp -r libero_spatial libero_spatial_orange
# 重命名所有 black_bowl 的 pruned_init 文件为 orange_bowl
for file in pick_up_the_black_bowl_*.pruned_init; do 
    mv "$file" "${file/black_bowl/orange_bowl}"
done
```

## 技术要点

### Init 文件类型
- **libero_goal**: 只使用 `.pruned_init` 文件
- **libero_spatial**: 同时有 `.init` 和 `.pruned_init` 文件（保留所有文件以避免破坏兼容性）

### 命名规则
系统使用固定的命名模式：`{task_name}.pruned_init`
- Task 类构造时设置：`init_states_file=f"{task}.pruned_init"`
- 必须与 BDDL 文件名严格对应

### 文件内容
Init 文件包含数值状态数据（numpy.ndarray），不包含对象名称，因此可以安全复制。

## 验证结果
- ✅ **libero_goal_new**: 10/10 tasks verified
- ✅ **libero_spatial_orange**: 10/10 tasks verified
- ✅ **所有 init 文件路径正确且存在**

## 文件结构
```
libero/libero/init_files/
├── libero_goal/              # 原始 goal 任务
├── libero_goal_new/          # 新的 goal 任务（blue_bottle替换wine_bottle）
├── libero_spatial/           # 原始 spatial 任务（black_bowl）
├── libero_spatial_orange/    # 新的 spatial 任务（orange_bowl替换black_bowl）
├── libero_object/
├── libero_10/
└── libero_90/
```

## 经验教训
1. **不要删除任何文件** - 保持所有 `.init` 和 `.pruned_init` 文件以避免破坏兼容性
2. **严格匹配命名** - Init 文件名必须与 BDDL 文件名完全对应
3. **验证脚本有用** - 创建自动验证脚本确保配置正确

现在系统应该能够正常加载所有环境的初始化状态！
