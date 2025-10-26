## LIBERO-VERIFICATION：验证环境

本仓库是基于 LIBERO 项目构建的验证环境，旨在用于复现与验证下列工作中描述的实验：

- 参考论文： https://arxiv.org/abs/2510.14902

目的与范围：

- 提供一个轻量级的验证环境，保持与原始 LIBERO API 与接口的完全兼容。
- 保留原始任务套件，同时添加论文中用于难度分级的一些命名映射。

环境 / 任务命名与映射：

- 原始套件（不变）：`libero_spatial`、`libero_object`、`libero_goal`、`libero_long`。
- 附加的命名映射（与论文难度对应）：
  - `spatial-orange` → 对应论文中的 “easy”（简单）设置。
  - `goal-new` → 对应论文中的 “medium”（中等）设置。
  - `0` → 对应论文中的 “hard”（困难）设置。

注意：这些仅为命名层面的映射——内部任务定义、BDDL 文件与 API 保持与原始 LIBERO 项目一致。

使用与兼容性：

- 本仓库的使用、训练、评估和 API 接口与原始 LIBERO 项目完全相同。对于新加入的三种环境的使用也和原本的LIBERO相同，输入对应环境的名称即可使用。有关安装、数据集下载、示例和完整使用细节，请参照原始 LIBERO 仓库：

  https://github.com/Lifelong-Robot-Learning/LIBERO

引用：

- 主要参考（项目使用来源）： https://arxiv.org/abs/2510.14902

- 若使用了原始 LIBERO 的基线或数据集，请同时引用 LIBERO 项目（引用细节见原始仓库）。

许可证：

本仓库遵循与原始项目相同的代码许可（见仓库根目录下的 `LICENSE`）。数据集许可由各数据集定义（通常为 CC BY 4.0），请按需参阅相应说明。

变更记录（简要）：

- 将 README 重写为将本仓库定位为基于 LIBERO 的验证环境，添加论文难度级别的命名映射，并说明与原始 LIBERO 的兼容性。

如需我将此 README 与英文版合并为中英双语，或添加完整的 bibtex 引用，请告诉我，我会继续添加。