# build-and-run.sh 步骤清单

示例与模板的 `build-and-run.sh` 遵循固定骨架：`set -euo pipefail` 严格模式、`header()` / `err()` / `trap ERR` 输出辅助、`main()` 按编号步骤执行、末行 `main "$@"`。CMake 项目步骤为 1 配置 → 2 构建 → 3 运行；单文件示例为 1 编译 → 2 运行；带测试的工程在构建后插入 `ctest --test-dir build --output-on-failure`。

步骤次序与验收清单的唯一权威是姊妹仓库 cpp-board-games 中 `cpp-development` 技能的 `build-and-run` reference；两仓只同步步骤骨架，注释外形各随本仓约定。
