# 工程实践

> 项目布局 · 错误处理 · 测试

## 工程讲解顺序

工程章节按“源码 → 构建目标 → 构建规则 → 构建命令 → 生成结果 → 验证”展开。先让读者看到一个可运行目标，再逐步引入目录、库、测试和安装等组织方式。

## 项目布局

```
project/
├── CMakeLists.txt
├── src/
├── include/
└── tests/   # 进阶
```

## 错误处理

- 构造函数失败 → 异常；可预期失败 → `optional`/`expected`。
- 资源管理靠 RAII，见 `modern-cpp.md`。

## CMake 现代写法

- target-based：`target_link_libraries`、`target_compile_features`。
- 构建决策依据用 `run.py kb-search "C++ 构建 工具链" --domain cpp-content` 取用。

## 示例与章节落点

- 工程章正文落 `content/toolchain/cmake-targets.qmd`、`project-layout.qmd`。
- 单文件示例落 `code/<part>/<name>.cpp`，多文件工程落 `code/<part>/<chapter>/`，与 `content/<part>/` 三级对齐。
- 工程章示例至少包含 `CMakeLists.txt` 与一个可运行目标，禁止只给伪配置。
- 文件名使用 ASCII；注释放在代码上一行，逻辑块之间留空行。
- 环境与工程章节只保留当前任务的最小成功路径；平台差异、命令案例与诊断依据从知识库检索。
- 改主题、全局配置或页面结构时再渲染整本 Book，日常改动只用 `run.py verify --changed`。

## 工具链写作路由
本文件只保留通用约束：先给当前任务的最小成功路径，命令前说明目的，命令后给出成功判据；环境、版本、平台、参数和诊断案例进入知识库。

需要项目工具链依据时，运行 `python .cursor/skills/agent-ops/scripts/run.py kb-search "C++ 构建 工具链" --domain cpp-content`。
