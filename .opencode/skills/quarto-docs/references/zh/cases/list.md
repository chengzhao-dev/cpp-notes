# 列表示例 / 案例（writing-style.md 配套）

本文件是 `writing-style.md`「列表（bullet）的中心结构 / 列表项要短」的 before/after 案例库。规则见 `../writing-style.md`。

## 嵌套列表 → 三列表格

示例（状态 → 命令速查表：嵌套列表 → 三列表格，适用于速查项较多的参考场景）：

```markdown
# 避免：长说明塞进二级 bullet
- 状态是 `Running`：不用时记得关掉，把内存释放出来。
  - **`wsl --shutdown`**：终止所有 Linux 系统及底层轻量虚拟机。
  - **`wsl --terminate <distro>`**：只终止指定的 Linux 系统，例如 `wsl --terminate Ubuntu`。
- 状态是 `Stopped`：用这条命令启动并进入：
  - **`wsl`**：启动 WSL 并进入默认的 Linux 系统。进入后终端停在你启动 `wsl` 时所在的 Windows 目录；想回到 Linux 主目录，用 `cd ~` 或一开始就 `wsl ~`（主目录固定是 `/home/<用户名>`）。

# 推荐：成对信息用表格，长说明移出，加「适用状态」列

| 适用状态 | 命令 | 作用 |
|---|---|---|
| 运行中（Running） | `wsl --shutdown` | 终止所有 Linux 系统及底层轻量虚拟机 |
| 运行中（Running） | `wsl --terminate <distro>` | 只终止指定的 Linux 系统，如 `wsl --terminate Ubuntu` |
| 已停止（Stopped） | `wsl` | 启动默认系统并进入 shell |
```

要点：嵌套 bullet 改三列表格后扫读更快；「适用状态」列标明依赖的前置状态（何时用 vs 做什么）。注：环境章「启动与关闭」现按动作直陈、命令入散文（见 `adjacent-paragraphs.md`「主旨对齐」案例）；本表形态保留为速查项较多的场景（工具选项、容器清单等）的范式演示，命令已入散文时不再重复建表。
```

## 本章目标：三步 + 多种开头写法

示例（WSL2 环境章「本章目标」，三步 + 多种开头写法混用，源细节已下沉正文）：

```markdown
学完本章，你就能：
- 装好并启用 WSL2，让 Ubuntu 成为开发环境；
- 在 WSL2 Ubuntu 环境里装好并验证 C++ 构建工具链；
```

要点：引导句点题 → 两条按「装环境 → 在环境里装工具」推进、开头写法不同（动词起头 / 环境状语前置）→ 与引言「装好 Ubuntu，并配齐编译、构建与调试工具链」的推进呼应。对有序列表（1. 2. 3.）同样适用，推进更显式。

## 列表项：先讲核心用途，不提前抛未引入的术语

反面例子（来自 setup-wsl2.qmd「安装编译器」步骤 4，子弹直接抛出尚未介绍的 `CMakeLists.txt`/`Makefile`，新手不知所云）：

```markdown
# 避免
- `cmake`：构建系统生成器——读你的 `CMakeLists.txt`，自动产出 Makefile 或 Ninja 脚本，你只写「描述」不必手写编译命令。
- `ninja-build`：高速构建后端，常配合 `cmake -G Ninja` 使用，比 `make` 编译更快（Ubuntu 上包名即 `ninja-build`）。
```

# 推荐：每条先点明「它是什么、最大用途」，细节留给对应专题章节
- `cmake`：当前主流的 C++ 构建系统，用来把源码组织、编译成可执行程序。
- `ninja-build`：配合 cmake 使用的高速构建工具，能明显加快编译（Ubuntu 上包名即 `ninja-build`）。

要点：子弹先给「核心身份 + 主要用途」，避免一上来抛未出现的专有名词（`CMakeLists.txt`/`Makefile`/`Ninja 脚本`）；具体机制留给对应章节（如 cmake 专题）细讲。
