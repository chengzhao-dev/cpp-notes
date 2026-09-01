# 相邻段落示例 / 案例（writing-style.md 配套）

本文件是 `writing-style.md`「相邻段落（内容重复 / 接近时合并）」的 before/after 案例库。规则见 `../writing-style.md`。

反面例子（来自 setup-wsl2.qmd「启动与关闭」初稿，段落主线被 STATE 反客为主）：

```markdown
# 避免：标题是「启动与关闭」，段落却都围着查状态转，主旨动作没有独立成段
启动就是进入 Ubuntu 的 shell，关闭就是停掉整个环境、释放内存。WSL2 没有单独的「关闭」按钮，所以要看当前处于哪种状态，在 PowerShell 中运行 `wsl --list --verbose`：

…（输出块）…

STATE 一列是 Running 就关掉并释放内存，是 Stopped 就启动并进入。对应命令如下：

…（状态 → 命令表格）…
```

# 推荐：标题承诺的动作各占一段先行、命令入散文；查状态降为末尾支撑段（隔块：引出一句 + 输出块）
启动就是进入 Ubuntu 的 shell，在 PowerShell 中运行 `wsl`，或直接打开 Ubuntu 应用。进入后终端停在你启动时的 Windows 目录。要回到 Linux 主目录，进入后运行 `cd ~`，或启动时就运行 `wsl ~`。

关闭就是停掉整个环境、释放内存，在 PowerShell 中运行 `wsl --shutdown` 终止所有 Linux 系统及底层轻量虚拟机。只终止指定的系统时，改用 `wsl --terminate <distro>`，如 `wsl --terminate Ubuntu`。

不确定处于哪种状态时，在 PowerShell 中运行 `wsl --list --verbose`，看 STATE 一列：Running 表示运行中，Stopped 表示已停止。

…（输出块）…
```

要点：主旨对齐——小节段落顺序跟随标题主旨，主旨动作（启动/关闭）各占一段先行、命令直接入句（规则见 `../writing-style.md`「去重与主题聚焦·主旨对齐」）；支撑信息（查状态）后置为一段引出 + 输出块，隔块各一句、后段不重复框架；状态值/列名用正文（Running/STATE 非代码）。原「STATE → 命令」表格在命令入散文后与之全量重复，删除（速查表形态见 `list.md`）。

## 软件源：三段合并为一段

反面例子（来自 setup-wsl2.qmd「软件源」，三段都讲换源，信息重叠）：

```markdown
# 避免：三段同主题，背景/触发/步骤各写一段，回看才发现重复
Ubuntu 的默认软件源就是官方源 `http://archive.ubuntu.com/ubuntu`，通常无需改动就能正常更新。

若你执行更新或下载时明显卡顿，多半是官方源在所在网络偏慢，可换用清华大学开源软件镜像站的 Ubuntu 镜像 `https://mirrors.tuna.tsinghua.edu.cn/ubuntu` 加速。

具体做法以 [清华镜像帮助页](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/) 为准：按你的 Ubuntu 版本复制对应的 `sources.list` 内容覆盖 `/etc/apt/sources.list`，再刷新索引。

# 推荐：合并为一段（默认句 + 「再」衔接的例外句 + 出处），步骤交给权威页面
默认情况下，Ubuntu 使用[官方源](http://archive.ubuntu.com/ubuntu)。更新或下载明显卡顿时，再换用[清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/ubuntu)加速，做法以[清华镜像帮助页](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)为准。
```

要点：三段合一段，默认句一句收住（「一般不用改」尾注删除，由注意块承载）；例外句用「再」衔接；换源步骤随 Ubuntu 版本漂移、权威页面已承载，正文只留决策 + 「做法以 X 为准」出处，不转抄（规则见 `../writing-style.md` 详略与衔接）；caveat 仍用 `>` 引用块单列。

## 迁移段：两段合并为一段，术语就地讲清

反面（来自 setup-wsl2.qmd「延伸内容」初稿：两段讲同一件事的递进「问题 → 方案」，但方案突然甩出未解释的术语，还塞了示例盘符与举例）：

```markdown
# 避免：术语突兀 + 示例指代 + 例如举例 + 两段过散
WSL 里的 Linux 系统默认装在 `C:\Users\<user>\AppData\Local\Packages\`，会随使用增长持续占用系统盘。C 盘空间紧张时，可整体迁移到 D 盘，例如迁到 D:\ProgramData\WSL\Ubuntu。

兼容性最好的是导出再导入，可在任意 WSL2 版本间迁移。以管理员身份打开 PowerShell 后执行：
```

正面（合并为一段，只留关键：问题直陈 → 方法就地讲清 → 落到动作）：

```markdown
# 推荐
Ubuntu 系统默认装在系统盘的用户目录 `C:\Users\<user>\AppData\Local\Packages\` 里，会随使用增长持续占用系统盘空间。系统盘空间不足时，可把 Ubuntu 整体迁移到其他磁盘，使用以下方法之一。

**方法 1：导出再导入（通用）。** 以管理员身份打开 PowerShell 后运行：
```

要点：两段递进合一段、只留关键（版本兼容说明删去，由命令块自明）；方法名就地命名（**方法 1：导出再导入（通用）**），步骤细节由命令块注释承载；「C 盘/D 盘」示例指代改直陈「系统盘空间不足 → 迁移到其他磁盘」；「例如迁到…」删去，具体路径由下方命令块承载（见 `../writing-style.md` 详略与衔接）。

## 引用块 `>` 的克制使用 / 段落去冗余

「延伸内容」与正文里常出现两类冗余：① 有序内容中间插 `>` 引用块，把先后步骤切断；② 导语 / 回环反复说同一句，尤其标题已表「按需」却仍用「是否…不影响」收尾。

- **注意块跟所属方法**：注意块归属哪个方法，就紧跟该方法的代码块之后放，位置本身承载归属；不写「方法 X 的」文字标注，也不必甩到全段末；caveat 只留必要 1 个 `>`（与 命名 callout 节「简短提醒用 `>` 引用块」一致，但「简短提醒」≠「每条提醒」）。
- **段落去冗余**：导语只给核心框架句，不预演 `###` 首条；标题已表「延伸/按需」时，块末不再叠「是否迁移按需…不影响」这类语气，读者自知可跳过。

迷你 before/after（取自 `### 迁移 WSL2 系统到其他磁盘`）：

```markdown
# 避免：注意块甩到全段末，还用「方法 1 的」文字标注归属
…（方法 1 代码）…
…（方法 2 代码）…
> 注意：方法 1 的 `wsl --import` 不保留原有用户…
```

```markdown
# 推荐：注意块紧跟方法 1 的代码块之后，归属由位置承载
…（方法 1 代码）…
> 注意：`wsl --import` 不保留原有用户…
…（方法 2 代码）…
以后重装系统时，也能用 `wsl --install … --location` 一步指定位置，免去再迁移。
```

完整「延伸内容」 before/after 见 cases/supplementary.md。
