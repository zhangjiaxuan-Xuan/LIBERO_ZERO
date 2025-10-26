## LIBERO_ZERO: Verification Environment

This repository is a verification environment built on top of the LIBERO project. It is intended for reproducing and validating the experiments described in the following work:

- Source paper: https://arxiv.org/abs/2510.14902

Purpose and scope:

- Provide a lightweight verification environment that maintains full compatibility with the original LIBERO APIs and interfaces.
- Preserve the original task suites while adding a small set of naming mappings used in the paper for difficulty levels.

Environment / task naming and mapping:

- Original suites (unchanged): `libero_spatial`, `libero_object`, `libero_goal`, `libero_long`.
- Additional name mappings (paper difficulty correspondence):
  - `spatial_orange` → corresponds to the paper's "easy" setting.
  - `goal_new` → corresponds to the paper's "medium" setting.
  - `0` → corresponds to the paper's "hard" setting.

Note: these are naming-level mappings only — internal task definitions, BDDL files, and APIs remain the same as in the original LIBERO project.

Usage and compatibility:

- Usage, training, evaluation and API interfaces are identical to the original LIBERO project. For the new envs illustrated in this repository, usage is the same as the original LIBERO — simply input the name of the corresponding environment(e.g. libero_orange, libero_0). For installation, dataset download, examples, and full usage details, please refer to the original LIBERO repository:

  https://github.com/Lifelong-Robot-Learning/LIBERO

Citation:

- Primary reference (user-provided): https://arxiv.org/abs/2510.14902

- If you use the original LIBERO baselines or datasets, please also cite the LIBERO project as appropriate (see the original repository for citation details).

License:

This repository follows the same code license as the original project (see `LICENSE` in the repository). Dataset licenses are defined by each dataset and are noted where applicable (typically CC BY 4.0).

Change log (brief):

- README rewritten to present this repository as a LIBERO-based verification environment, add paper mapping for difficulty levels, and clarify compatibility with the original LIBERO project.

If you would like an English README with additional details (e.g., full bibtex entries, or an English+Chinese bilingual README), I can add those on request.
