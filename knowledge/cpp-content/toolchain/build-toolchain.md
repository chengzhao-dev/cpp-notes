---
kb_id: "cpp-tooling-build-chain-v2"
title: "C++ 构建与工具链决策依据"
domain: "cpp-content"
subdomain: "toolchain"
tags: [toolchain, clang, llvm, libcxx, lldb, cmake, ninja, ninja-build, generator, compiler_flags, sanitizer, warnings, optimization, header, translation_unit, include_path, include_directories, target_include_directories, source_glob, configure_depends, project_name, multi_file, clangd, compile_commands, verification]
level_range: [0, 9]
created: "2026-09-09"
updated: "2026-09-15"
chunk_strategy: "semantic_heading"
estimated_tokens: 680
---

# C++ 构建与工具链决策依据

## 最小构建链

本项目在 Windows 的 WSL2 Linux 环境中使用 Clang/LLVM、libc++、CMake 与 Ninja。先让最小程序编译和运行，再把命令固化为 CMake 目标。MSVC 仅作为对照，不是主线前置条件。

入门环境按“编译器 → CMake + Ninja → 调试器 → 语言服务”建立依赖层次。编译器把源码变成可执行文件，CMake 描述工程并生成构建规则，Ninja 执行这些规则，调试器服务运行期排查。`CMAKE_EXPORT_COMPILE_COMMANDS` 让配置阶段生成 `compile_commands.json`，记录每个源文件的实际编译参数。`.clangd` 的 `CompilationDatabase: build` 指向构建目录，语言服务据此提供代码提示与诊断。Ubuntu 环境安装 `clang`、`clangd`、`llvm`、`lldb`、`libc++-dev` 和 `libc++abi-dev`，分别提供编译器、语言服务、LLVM 工具、调试器和 libc++ 的编译与链接支持。Ubuntu 中的 Ninja 软件包名为 `ninja-build`，安装后执行命令为 `ninja`。默认 Ubuntu 是当前教程为降低选择成本采用的教学路径，不代表发行版优劣。

## 编译与诊断

示例使用 C++20、常见警告和可重复的构建配置。Sanitizer 用于调试和未定义行为专题。不要把未启用的诊断选项留在入门示例中。优化必须先测量基线，再报告收益、代价和适用范围。

`clang++` 是编译器命令，负责把源文件编译并链接为可执行文件。示例使用 `-stdlib=libc++` 选择 LLVM C++ 标准库，编译和链接阶段必须使用同一选项。CMake 读取 `CMakeLists.txt` 并生成底层构建规则，Ninja 执行这些编译和链接规则。`cmake --build <dir>` 是 CMake 提供的统一构建入口，会调用配置阶段已选定的 Ninja。配置时显式传入 `-DCMAKE_CXX_COMPILER=clang++`，避免 CMake 根据宿主环境选择其他编译器。教程应使用“通过 `clang++` 命令行编译，通过 CMake 配置 Ninja 并构建”的表述，避免把编译器、构建描述工具和规则执行工具写成同一层级的工具。

### 从源码到终端的主体链

向新手解释 `main.cpp` 如何变成终端输出时，要按执行主体拆开连续动作：终端执行 `clang++` 命令并启动编译器。`clang++` 编译并链接源码，生成可执行文件。终端发起运行请求，操作系统加载并执行该文件。程序写入标准输出，终端显示文本。读者据此能判断每一步由谁负责，也能在编译、链接、加载或运行失败时定位阶段。把整个过程压缩成“编译器把源码转换为可运行程序”会隐藏加载与执行环节。

### 首个程序与一键脚本

Hello World 的价值不是展示语言能力，而是用最少的输入、状态和数据验证工具链。源码经过编译、链接、加载和运行后产生稳定输出，任何一步失败都能直接暴露。首次解释入口函数时，要明确指出 `main()` 后面的花括号组成函数体，程序从函数体第一条语句开始执行，避免把花括号说成没有边界的占位符。

需要反复执行的编译命令可以沉淀为 `build-and-run.sh`。脚本减少手工命令漂移，也能让仓库验证统一入口。正文仍保留关键手工命令，让读者理解脚本封装的动作。直接编译脚本调用 `clang++`，CMake 工程脚本依次配置、构建和运行，两者都把生成物放进忽略的 `build/`。

## CMake

用目标属性表达语言版本、包含路径、编译选项和链接依赖，避免依赖全局变量。配置、构建和运行是独立步骤，每一步都应有可观察产物。项目默认以 `cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++` 配置，再以 `cmake --build build` 构建。`-G Ninja` 和编译器选择属于配置命令，不应写进 `CMakeLists.txt`，后者必须保持生成器和编译器无关。两阶段的重跑条件不同：配置读取 `CMakeLists.txt` 并生成构建规则与编译数据库，只有构建规则变化时才需要重跑。构建按规则增量编译，改源码时反复跑。把差异写清，读者才知道改一行源码不需要重新配置，也不需要删 `build/`。

构建类型、编译器路径和生成器记录在 `CMake` 缓存里。已有 `build/` 时，CMake 不会把已配置的生成器自动替换为 Ninja，读者只重跑构建仍会使用旧规则。这类“值与产物不一致”的坑用一条判据收束：缓存文件里的记录才是当前生效的配置。

### 多文件工程的目标边界

多文件程序把接口声明放在头文件，把实现放在源文件，再由一个目标统一编译和链接。头文件让每个翻译单元在编译期看到相同的声明，源文件提供定义，CMake 的 `add_executable` 收集所有实现文件，`target_include_directories` 告诉编译器从哪里查找工程头文件。缺少任一环节时，失败阶段不同：找不到头文件发生在编译期，找不到函数定义发生在链接期。

验证多文件示例时必须按 `CMakeLists.txt` 配置并构建完整目标。逐个调用 `clang++` 不仅无法还原目标的包含路径、源文件集合和链接参数，还可能把编译成功的单个翻译单元误判为工程可用。CMake 构建成功才同时证明源文件、头文件、包含路径和链接关系一致。

可执行文件、静态库和动态库的链接与运行期边界见标识 `cpp-library-and-executable-linking-v1` 的知识文件，本文件不重复库产物规则。

### CMake 工程名与目录名

仓库目录名服务于路径和 URL，使用简短 kebab-case。`project()` 名称是 CMake 变量前缀、生成器展示名和未来包配置的命名入口，入门模板从目录名派生 PascalCase，例如 `multi-file-project` 生成 `MultiFileProject`。两者职责不同，不需要为了表面一致让 CMake 工程名携带连字符。派生规则由脚手架集中实现，模板不手写两个名称。

### 源文件收集与重新配置

教学多文件工程可以用 `file(GLOB APP_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")` 收集 `src/` 的直属实现文件，再交给 `add_executable(app ${APP_SOURCES})`。`CONFIGURE_DEPENDS` 让支持的生成器在构建前检查文件集合变化，新增 `.cpp` 后无需手改源文件列表。该便利以隐藏依赖图为代价，不适用于目录分层、生成源码或需要精确控制多个目标的大型工程。这些场景应改用显式 `target_sources`。库工程在 `greeting/CMakeLists.txt` 中使用相同的收集方式时，`CMAKE_CURRENT_SOURCE_DIR` 已切换到库目录。

### 目标包含路径

`target_include_directories(app PRIVATE include)` 把包含目录绑定到具体目标，并要求使用该目标的编译步骤读取这条属性。`PRIVATE` 表示目录服务 `app` 自身而不向消费者传播，适合可执行目标。`include_directories()` 作用于当前目录中随后创建的目标，容易让无关目标继承路径并掩盖依赖。当目录开始提供公共头文件时，库目标才应把接口目录改为 `PUBLIC`。

### Clang 工具链一致性

编译、语言服务和调试统一使用 Clang/LLVM 工具链。此前由 GCC 生成编译数据库时，GCC 专用模块扫描参数会进入 `compile_commands.json`，而 clangd 不识别这些参数。迁移后，`clang++`、`clangd` 和 `lldb` 属于同一工具链，CMake 又显式选择 `clang++`，因此不需要 `CXX_SCAN_FOR_MODULES OFF`，也不需要过滤 `-fmodules-ts`、`-fmodule-mapper=*` 或 `-fdeps-format=*`。

`.clangd` 用 `CompilationDatabase: build` 指向根构建目录，兜底参数使用 `-stdlib=libc++`，并只把 `/usr/bin/clang++` 作为查询驱动。旧构建目录可能缓存过其他编译器。切换编译器或标准库时应在新的构建目录重新配置，不能只运行 `cmake --build`。项目不保留 GCC 编译器作为后备路径。

### 旧构建目录的诊断顺序

`cmake --build <dir> --target clean` 只清理目标产物，不删除 `CMakeCache.txt` 中的编译器、生成器和路径缓存。解决旧构建目录造成的配置问题时，应先用新的目录执行 `cmake -S . -B build-fresh -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++`，而不是把 clean 误当成清空配置。随后执行 `cmake --build build-fresh` 并运行 `build-fresh/bin/app` 验证新链路。诊断时同时切换构建类型会把工具链问题与优化、调试信息差异混在一起，因此保持 Debug，确认新目录可用后再处理旧目录。

### 版本要求只写在构建配置里

`cmake_minimum_required` 是版本要求的唯一落点。构建配置、脚手架模板和示例脚本不写宿主发行版名与其版本号。发行版会随时间升级，写死的名称与版本在读者照着操作时必然过期，还会让同一条要求同时存在于正文、脚本和模板三处，三份记录很容易互相矛盾。

版本号的取值与本机实测的 CMake 基线保持一致，正文、示例和脚手架使用同一个数字，避免读者按环境章节完成安装后又遇到版本分叉。需要交代某条要求来自哪个环境时，写“与本机实测基线一致”，真正的版本号留在一次实测输出的 `text` 块里，不复制进配置文件。
