# 工程实践

> 项目布局 · 错误处理 · 测试

## 工程讲解顺序

工程章节按“源码 → 构建目标 → 构建规则 → 构建命令 → 生成结果 → 验证”展开。先让读者看到一个可运行目标，再逐步引入目录、库、测试和安装等组织方式。

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
- 多文件入门用 `file(GLOB APP_SOURCES CONFIGURE_DEPENDS "src/*.cpp")` 收集直属源文件，再交给 `add_executable(app ${APP_SOURCES})`。新增 `.cpp` 后重新配置即可进入目标。
- 库入门在 `greeting/CMakeLists.txt` 用 `add_library(greeting STATIC|SHARED ...)` 和 `target_include_directories(greeting PUBLIC include)` 定义库目标，顶层用 `add_executable(app main.cpp)`、`add_subdirectory(greeting)` 与 `target_link_libraries(app PRIVATE greeting)` 表达消费者关系。
- 可执行文件输出到 `build/bin/`，库输出到 `build/lib/`。动态库工程的构建树运行依赖用 `BUILD_RPATH "$ORIGIN/../lib"` 绑定。
- GLOB 只用于教学模板。目录分层或目标增多后改用显式 `target_sources`，让依赖和源文件边界可见。
- 头文件目录用 `target_include_directories(app PRIVATE include)` 声明。不要退回目录级的 `include_directories`。
- 默认 CMake + Ninja 构建链的决策依据用 `run.ps1 kb-search "CMake Ninja 构建链" --domain cpp-content` 取用。库与运行期查找依据检索 `cpp-library-and-executable-linking-v1`。

## 示例与章节落点

- 工程章正文落 `content/toolchain/cmake-targets.qmd`、`project-layout.qmd`。
- 需要重复编译运行的章节使用 `code/<part>/<chapter>/`，至少包含源码和一个 `build-and-run.sh`。直接编译脚本调用 `clang++`，CMake 工程脚本执行配置、构建和运行。只有不进入重复构建流程的片段或无工程文件可省略脚本。
- 多文件工程落 `code/<part>/<chapter>/`，库示例允许同一章节登记多个独立工程目录，并在任务矩阵中全部列出。
- 工程章示例至少包含 `CMakeLists.txt` 与一个可运行目标，禁止只给伪配置。
- 单文件、多文件和库工程分别用 `init_project.py --layout single|multi|static-library|shared-library` 生成。库工程生成根 `main.cpp` 与 `greeting/`，模板源在 `cpp-content/templates/projects/`。
- 一个教学工程只突出一个中心。需要同时讲静态库和动态库时，使用两个独立工程，而不是在同一工程并列两种库目标。
- part 目录和章节文件使用 ASCII kebab-case，章节名不复述 part 名，也不加顺序数字。顺序只在 `_quarto.yml` 与索引页维护。
- C++ 文件名使用 snake_case。完整源码文件的用途注释与重点注释以 `code-style.md` 为准，逻辑块之间留空行。
- 环境与工程章节只保留当前任务的最小成功路径。平台差异、命令案例与诊断依据从知识库检索。
- 改主题、全局配置或页面结构时再渲染整本 Book，日常改动只用 `run.py verify --changed`。

## 工具链写作路由
本文件只保留通用约束：先给当前任务的最小成功路径，环境、版本、平台、参数和诊断案例进入知识库。命令、说明与输出的排布细则见 `.agents/skills/quarto-docs/references/quarto/terminal-validation.md`。

需要项目工具链依据时，运行 `& .agents/skills/agent-ops/scripts/run.ps1 kb-search "CMake Ninja 构建链" --domain cpp-content`。
