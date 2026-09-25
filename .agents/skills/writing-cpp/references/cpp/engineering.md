# 工程实践

> 项目布局 · 错误处理 · 测试

## 工程章特有要求

工程章先让读者看到一个可运行目标，再逐步引入目录、库、测试和安装等组织方式。通用教学顺序以 `teaching-method.md` 为准，本文件只补充工程示例和 CMake 的领域约束。

## 项目布局

多文件可执行工程的公共头文件和源文件放在顶层：

```
project/
├── CMakeLists.txt
├── include/
│   └── greeting.h
├── src/
│   ├── greeting.cpp
│   └── main.cpp
└── tests/   # 进阶
```

库工程把库的接口、实现和构建规则收在独立子目录，并与消费它的 `app/` 同级：

```
static-library/
├── CMakeLists.txt
├── main.cpp
└── greeting/
    ├── CMakeLists.txt
    ├── include/
    │   └── greeting.h
    └── src/
        └── greeting.cpp
```

只有一个可执行源文件时，`main.cpp` 直接放在工程根目录，与 `CMakeLists.txt` 同级。顶层 `CMakeLists.txt` 通过 `add_subdirectory(greeting)` 加载库目标，再创建和链接 `app`。`greeting/CMakeLists.txt` 只管理库自身，不同时声明应用目标。

消费端出现多个源文件或需要独立的目标规则后，再建立 `app/`，在其中放置 `CMakeLists.txt` 并迁移入口。不要为只有一个文件的消费端预留 `app/`，这会把冗余层级误当成目标边界。

## 错误处理

- 构造函数失败 → 异常。可预期失败 → `optional`/`expected`。
- 资源管理靠 RAII，见 `modern-cpp.md`。

## CMake 现代写法

- target-based：`target_link_libraries`、`target_compile_features`。
- CMake 工程名使用从目录名派生的 PascalCase，例如 `multi-file-project` 对应 `MultiFileProject`。
- 源文件收集方式、GLOB 适用分界、库目标写法、产物输出目录和 `target_include_directories` 的用法以 `cmake-teaching.md` 为准，本文件不重复命令级细节。
- 默认 CMake + Ninja 构建链的决策依据用 `run.ps1 kb-search "CMake Ninja 构建链" --domain writing-cpp` 取用。库与运行期查找依据检索 `cpp-library-and-executable-linking-v1`。

## 示例与章节落点

- 工程章正文落 `content/toolchain/cmake-targets.qmd`、`project-layout.qmd`。
- 需要重复编译运行的章节使用 `code/<part>/<chapter>/`，至少包含源码和一个 `build-and-run.sh`。直接编译脚本调用 `clang++`，CMake 工程脚本执行配置、构建和运行。只有不进入重复构建流程的片段或无工程文件可省略脚本。
- 多文件工程落 `code/<part>/<chapter>/`，库示例允许同一章节登记多个独立工程目录，并在任务矩阵中全部列出。
- 工程章示例至少包含 `CMakeLists.txt` 与一个可运行目标，禁止只给伪配置。
- 单文件、多文件和库工程分别用 `init_project.py --layout single|multi|static-library|shared-library` 生成。库工程生成根 `main.cpp` 与 `greeting/`，模板源在 `writing-cpp/templates/projects/`。
- 一个教学工程只突出一个中心。需要同时讲静态库和动态库时，使用两个独立工程，而不是在同一工程并列两种库目标。
- part 目录和章节文件使用 ASCII kebab-case，语义化命名，章节名不复述 part 名，也不加顺序数字。顺序只在 `_quarto.yml` 与索引页维护。文件名与 YAML `title` 各司其职：`title` 用中文短任务句并保持单行，不与文件名互相直译，路径由文件名承担。
- part 目录名不复述书名已经表达的主题。书名含 C++，工程背景分册因此用 `practice`，读者可见标题为“工程应用”，不写 `cpp-in-practice` 或与入门内容边界重叠的 `engineering-practice`。命名依据检索 `cpp-agent-repository-navigation-v1`。
- C++ 文件名使用 snake_case。完整源码文件的用途注释与重点注释以 `code-style.md` 为准，逻辑块之间留空行。
- 环境与工程章节只保留当前任务的最小成功路径。平台差异、命令案例与诊断依据从知识库检索。
- 改主题、全局配置或页面结构时再渲染整本 Book，日常改动只用 `run.py verify --changed`。

## 工具链写作路由
本文件只保留通用约束：先给当前任务的最小成功路径，环境、版本、平台、参数和诊断案例进入知识库。命令、说明与输出的排布细则见 `.agents/skills/writing-quarto/references/quarto/terminal-validation.md`。

预处理、头文件、声明与定义、编译和链接的概念边界见 `cpp-cpp-preprocessing-headers-linking-v1`。正文只保留当前示例需要的解释，标准边界和失败原因从该知识条目检索，不在多个 reference 中重复。

安装工具的标题和注释只描述当前动作与工具职责。未限定 Ubuntu 发行版版本，也未验证某个 C++ 标准时，不把安装步骤命名为具体标准版本的工具链。

工具是否安装可由命令查询确认，但命令路径不等于工具功能已经验证。编译器至少要通过最小程序的编译和运行确认；构建、调试和语言服务则留给各自实际执行的任务。未执行对应操作时，不扩展正文结论。

需要项目工具链依据时，运行 `& .agents/skills/governing-agents/scripts/run.ps1 kb-search "CMake Ninja 构建链" --domain writing-cpp`。
