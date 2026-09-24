---
kb_id: "cpp-library-and-executable-linking-v1"
title: "可执行文件与静态库、动态库的链接边界"
domain: "cpp-content"
subdomain: "toolchain"
tags: [cpp, executable, static_library, shared_library, linker, loader, rpath, archive, shared_object, cmake, target_link_libraries, output_directory, teaching_example, single_file_layout, android, ndk, jni, abi, sdk, simulation, mobile_imaging, artifact_delivery]
level_range: [0, 5]
dependencies: ["cpp-tooling-build-chain-v2"]
created: "2026-09-15"
updated: "2026-09-16"
chunk_strategy: "semantic_heading"
estimated_tokens: 1280
---

# 可执行文件与静态库、动态库的链接边界

## 可执行文件的职责

可执行文件是操作系统可以直接加载和运行的程序。源码经过编译和链接后，程序入口、项目代码和运行所需的依赖关系才被组织成可执行文件。源文件本身没有加载入口，不能替代可执行文件。

在一个 CMake 工程中，`app` 通常代表最终交付给用户运行的程序。它既可以由多个源文件直接构建，也可以链接一个或多个库。无论采用哪种方式，读者最终执行的仍是 `app`。

## 静态库的链接边界

静态库在 Linux 上通常使用 `.a` 扩展名。它是目标代码的归档文件，本身不能被操作系统直接运行。链接器构建 `app` 时，只从归档中取出当前程序实际引用的目标代码，并把它们合并进最终可执行文件。

因此，静态链接完成后运行 `app` 不再需要原始 `.a` 文件。这简化了单文件部署，但库代码会进入每个使用它的可执行文件。库发生变化后，需要重新链接所有消费者。

## 动态库的链接边界

动态库在 Linux 上通常使用 `.so` 扩展名，文件类型是共享对象。链接 `app` 时，链接器主要记录程序对动态库的依赖，而不是把全部库代码复制进可执行文件。

程序启动时，操作系统的动态加载器读取这些依赖并查找对应的 `.so`。因此，动态链接只是让构建阶段成功还不够，部署和运行阶段仍要让加载器找到匹配的库文件。

动态链接允许多个程序共享同一份库文件，也允许在接口兼容的前提下独立更新库。代价是程序带有运行时依赖，发布时必须同时管理可执行文件和动态库的版本关系。

## 库模块与消费程序的分工

库的公开接口、实现和构建规则应进入同一个库模块目录。这样从源码树就能看出哪组文件和哪个库目标属于同一模块。消费端只有一个 `main.cpp` 时，入口直接放在工程根目录，与顶层 `CMakeLists.txt` 同级，不额外建立只容纳一个文件的 `app/`。

根工程的 `CMakeLists.txt` 负责项目级设置、`add_subdirectory(greeting)`、`add_executable(app main.cpp)` 和应用链接关系，库模块的 `CMakeLists.txt` 负责 `add_library()`、公开头文件目录和库自身选项。新增库源文件或调整库选项时，不需要修改应用入口。这个边界也解释了为什么库的 `include/` 与 `src/` 应该随库目标一起移动，而不是继续悬在工程根目录。

消费端增长为多个源文件，或需要独立的目录级构建规则后，再建立 `app/`，在其中放置 `CMakeLists.txt` 并迁移入口。目录应表达真实职责，而不是提前预留一层；否则初学者容易把只有 `main.cpp` 的包装目录误认为库边界或目标边界。

入门工程仍只保留一个库目标和一个消费者。这里的目录边界用于建立“应用依赖库模块”的心智模型，不延伸到安装、导出或包管理。

## RPATH 与运行期查找

构建目录把 `app` 放在 `build/bin/`、库放在 `build/lib/` 后，动态加载器不会因为目录相邻就自动找到 `libgreeting.so`。`BUILD_RPATH "$ORIGIN/../lib"` 把查找位置记录进构建出来的 `app`。

`$ORIGIN` 表示可执行文件自身所在目录，因此该路径不依赖启动程序时的当前工作目录。教学示例使用相对 RPATH，是为了让构建树可移动、运行命令稳定，并把“链接成功”和“运行期查找成功”是两个阶段的事实展示出来。安装后的 RPATH、系统库目录和包管理边界留给后续工程主题。

## 产物目录的分工

可执行文件统一输出到 `build/bin/`，静态库和动态库统一输出到 `build/lib/`，使读者可以从产物路径直接判断文件职责。CMake 中静态库使用 `CMAKE_ARCHIVE_OUTPUT_DIRECTORY`，动态库使用 `CMAKE_LIBRARY_OUTPUT_DIRECTORY`，两者都不应和 `app` 的输出变量混用。

这种布局也让运行依赖更容易观察：`app` 位于 `bin/`，动态库位于相邻的 `lib/`，RPATH 只需表达稳定的相对关系。

## 教学工程的一个中心

静态链接和动态链接改变的是构建产物、链接关系和运行依赖。把它们放在同一个入门工程中并同时生成 `app-static`、`app-shared` 等目标，会一次引入多个中心，读者难以判断某条命令和某个产物之间的因果。

因此，入门阶段使用两个独立工程分别演示 `.a` 与 `.so`，每个工程只保留一个库目标和一个消费它的 `app`。实际项目当然可以组合多种库和多个可执行目标。拆开是为了隔离学习变量，不是生产工程的结构限制。

## 验收观察点

`file` 可以区分可执行文件、归档和共享对象。`ldd` 可以观察动态链接程序的运行期依赖，也可以确认动态版 `app` 是否通过 RPATH 找到工程内的 `.so`。

静态版 `app` 的 `ldd` 输出不应出现 `.a`，因为归档只参与链接阶段。动态版应出现 `libgreeting.so => .../build/bin/../lib/libgreeting.so` 一类结果，证明加载器已经找到构建树中的动态库。
