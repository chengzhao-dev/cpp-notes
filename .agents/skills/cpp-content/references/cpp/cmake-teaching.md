# CMake 章节教学流程

CMake 章节先让目标运行，再逐步把命令行参数固化为目标属性。不要从完整工程模板或所有变量开始。

## 推荐顺序

```text
源码 → 可执行目标 → 最小 CMakeLists.txt
→ 配置 → 构建 → 运行 → 编译数据库
→ 多文件可执行目标 → 库 → 测试与安装
```

每一步承接前一步的文件和生成结果。命令前说明它要完成什么，命令后说明成功时应看到什么。读者未使用的缓存和内部文件不放进目录树。

## 默认构建参数

示例工程与脚手架统一使用 `cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++` 配置，再用 `cmake --build build` 编译目标。`-G Ninja` 与编译器选择只写在配置命令里，`CMakeLists.txt` 保持生成器与编译器无关，构建统一从 `cmake --build` 进入。`.clangd` 用 `CompilationDatabase: build` 指向根构建目录，clangd、脚本和编辑器读取同一份数据。发布构建在同一目录改用 `-DCMAKE_BUILD_TYPE=Release`，入门章节不展开。参数取舍与两阶段重跑条件的依据检索 `cpp-tooling-build-chain-v2`。

## 目标导向

使用 `add_executable`、`add_library`、`target_sources`、`target_include_directories` 和 `target_compile_features` 表达目标关系。优先设置 target 属性，不用全局变量掩盖依赖关系。多文件入门先让多个源文件进入同一个可执行目标，再用 `target_include_directories` 暴露工程头文件目录。库目标留到读者能区分接口与实现之后。

## 工程名与源文件集合

CMake 工程名与仓库目录名分工不同：目录用 kebab-case，`project()` 名用 PascalCase，由脚手架模板替换生成，派生依据见 `cpp-tooling-build-chain-v2`。源文件收集按目标规模分界：

- 单文件目标显式列出，例如 `add_executable(app main.cpp)`、库子目录的 `add_library(greeting STATIC src/greeting.cpp)`，读者能直接看到源文件边界。
- `src/` 有多个实现文件的教学工程用 GLOB 收集直属 `.cpp`，新增源文件后不必改 `CMakeLists.txt`：

```cmake
# 收集 src/ 下的直属源文件，新增 .cpp 后重新构建即可进入目标。
file(GLOB APP_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

# 创建 app 可执行目标，并收集 src/ 下的直属源文件。
add_executable(app ${APP_SOURCES})
```

`CONFIGURE_DEPENDS` 让 Ninja 在构建前检查目录变化，新增源文件后自动重新配置。GLOB 会隐藏源文件边界，也可能受生成器差异影响，因此只用于小工程教学。分层目录、多个目标或需要精确依赖时改用显式 `target_sources`。`include_directories` 作用于目录内后续目标，容易让依赖外溢。工程头文件继续由 `target_include_directories(app PRIVATE include)` 绑定到目标。

库工程把同一段源文件收集规则放进 `greeting/CMakeLists.txt`。此时 `CMAKE_CURRENT_SOURCE_DIR` 是库目录，GLOB 只收集 `greeting/src/`，不会误收工程根的入口文件；库子目录只有单个源文件时保持显式列出。消费端增长为多个源文件后，再把目标规则移入 `app/CMakeLists.txt`。

## 编译数据库

配置阶段生成 `compile_commands.json` 时，说明它记录每个源文件的真实编译参数，供 clangd、脚本和编辑器使用。它是构建结果，不是手写配置。删除后可通过重新配置生成。

## 可执行文件与库

库章节先让读者看懂可执行文件由 `main()` 和项目代码组成，再分别构建静态库与动态库。每个入门工程只保留一个库目标和一个消费它的 `app`。静态库与动态库拆成两个独立工程，避免同时引入多个中心。

静态工程在 `greeting/CMakeLists.txt` 使用 `add_library(greeting STATIC ${LIBRARY_SOURCES})`。库的公共头文件目录使用 `target_include_directories(greeting PUBLIC include)`，让消费者通过目标依赖获得接口目录。顶层 `CMakeLists.txt` 用 `add_subdirectory(greeting)` 加载库，再创建 `app` 并调用 `target_link_libraries(app PRIVATE greeting)`。动态工程使用 `SHARED`，并为构建树中的 `app` 设置 `BUILD_RPATH "$ORIGIN/../lib"`。教学时先展示顶层如何组合项目，再展示库文件如何定义自身目标；链接边界与运行期查找的原因检索 `cpp-library-and-executable-linking-v1`。

可执行文件输出到 `build/bin/`，静态库和动态库输出到 `build/lib/`，分别使用 `CMAKE_ARCHIVE_OUTPUT_DIRECTORY` 与 `CMAKE_LIBRARY_OUTPUT_DIRECTORY`。

## 实际交付背景

可执行文件和动态库主线跑通后，可各追加一个精简 `##`，用一个 `###` 说明可执行文件用于仿真验证、动态库用于上线 SDK 交付。正文只保留用途、典型流程和关键限制；ABI、JNI、SDK 组成和收益的系统依据检索 `cpp-library-and-executable-linking-v1`，不复制完整段落。

## Clang/LLVM 工具链一致性

编译、语言服务和调试统一使用 Clang/LLVM 工具链：CMake 显式选择 `clang++`，目标编译与链接同时配置 `-stdlib=libc++`，`.clangd` 的兜底参数也选择 libc++。切换编译器或标准库时在新的构建目录重新配置，不能只运行 `cmake --build`。迁移背景与诊断依据检索 `cpp-tooling-build-chain-v2`。

## 章节落点

先验证单文件目标，再引入多文件可执行目标、库、测试和安装。每个新增概念都应有对应源码、构建命令、生成结果和验证步骤。多文件工程的验收必须复用 `CMakeLists.txt` 配置并构建完整目标，不能把各 `.cpp` 单独编译后冒充工程可用。
