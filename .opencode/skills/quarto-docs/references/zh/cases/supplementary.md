# 延伸内容示例 / 案例（writing-style.md 配套）

本文件是 `writing-style.md`「延伸内容环节」的格式示例库。规则见 `../writing-style.md`。

定位：章末「延伸内容」收录按需查阅、非必读、非排错的内容（如系统迁移、进阶技巧），与「常见问题」（排错/速查）互补；两者 `##` 导语都只写核心框架句。

## 写作要点（提炼自既有规则）

1. **`##` 导语**：核心框架句带过「按需查阅」，不预演 `###` 首条、不冗余（同 FAQ 层级分工）。
2. **段落去冗余（相邻段落 / 去重）**：导语不重复 `###` 已交代的内容；标题已表「延伸/按需」，块末不再用「是否…不影响」这类语气收尾——读者自知可跳过。
3. **注意块跟所属方法（`>` 克制）**：注意块归属哪个方法，就紧跟该方法的代码块之后放，位置本身承载归属；不写「方法 X 的」文字标注；caveat 只保留真正必要的 1 个 `>`。
4. **列表与代码（列表三步 / 代码分工）**：命令单独放代码块；并列方法用 `###` 同级或段落分隔，保持顺序可见。
5. **末尾呼应**：块末一句呼应「按需」，但不与导语复述，也不带「是否…不影响」语气。

## 反面：导语三句冗余 + 两个 `>` 插在序列中间 + 「是否…不影响」收尾

```markdown
## 补充内容

环境就绪后，下面收录一些按需查阅的补充内容。平时不必通读，遇到对应场景时再搜索。先放一个最常见的 Linux 系统迁移场景。

### 迁移 WSL 系统到其他磁盘

WSL 里的 Linux 系统默认装在 `C:\Users\<user>\AppData\Local\Packages\`，会随使用增长持续占用系统盘。若 C 盘空间紧张，可整体迁移到 D 盘（如 `D:\ProgramData\WSL\Ubuntu`）。

在 PowerShell（管理员）中，导出再导入兼容所有 WSL2 版本，最通用：

```powershell
wsl --shutdown
wsl --export Ubuntu "D:\ProgramData\WSL\ubuntu-backup.tar"
wsl --unregister Ubuntu
wsl --import Ubuntu "D:\ProgramData\WSL\Ubuntu" "D:\ProgramData\WSL\ubuntu-backup.tar" --version 2
wsl --set-default Ubuntu
```

> 注意：`wsl --import` 不保留原有用户，首次进入会以 `root` 登录。若需恢复普通用户，在 Linux 系统内编辑 `/etc/wsl.conf`，写入 `[user]` 与 `default=<user>`，再执行 `wsl --terminate Ubuntu` 后重新进入。

若 WSL 版本不低于 2.3.11，可用一步法迁移，在 PowerShell 中执行，自动保留用户与注册表项：

```powershell
wsl --manage Ubuntu --move "D:\ProgramData\WSL\Ubuntu"
```

> 提示：以后重装 Linux 系统时，直接用 `wsl --install Ubuntu --location "D:\ProgramData\WSL\Ubuntu"` 一步到位，免去迁移。

是否迁移按需，跳过这一步也不影响你用 WSL2 编写、构建与调试 C++ 程序。
```

## 推荐：导语一句 + 仅 1 个 `>` 且置段末 + 删「是否…不影响」

```markdown
## 延伸内容

环境就绪后，还有几个按需查阅的延伸内容，遇到对应场景再来看。

### 迁移 WSL2 系统到其他磁盘

Ubuntu 系统默认装在系统盘的用户目录 `C:\Users\<user>\AppData\Local\Packages\` 里，会随使用增长持续占用系统盘空间。系统盘空间不足时，可把 Ubuntu 整体迁移到其他磁盘，使用以下方法之一。

**方法 1：导出再导入（通用）。** 以管理员身份打开 PowerShell 后运行：

```powershell
# 先关闭所有 WSL2 实例，确保导出时文件不被占用
wsl --shutdown

# 把 Ubuntu 导出为 tar 备份包
wsl --export Ubuntu "D:\ProgramData\WSL\ubuntu-backup.tar"

# 注销原发行版，释放 C 盘空间
wsl --unregister Ubuntu

# 从备份包导入到 D 盘新位置，并指定 WSL2
wsl --import Ubuntu "D:\ProgramData\WSL\Ubuntu" "D:\ProgramData\WSL\ubuntu-backup.tar" --version 2

# 设为默认发行版
wsl --set-default Ubuntu
```

> 注意：`wsl --import` 不保留原有用户，首次进入会以 root 登录。若需恢复普通用户，进入 Ubuntu 后编辑 `/etc/wsl.conf`，在 `[user]` 段下写入 `default=<user>`，再终止 Ubuntu 后重新进入。

**方法 2：一步迁移（需 `wsl` 2.3.11+，推荐）。** 自动保留用户与注册表项。在 PowerShell 中运行：

```powershell
wsl --manage Ubuntu --move "D:\ProgramData\WSL\Ubuntu"
```

以后重装系统时，也能用 `wsl --install Ubuntu --location "D:\ProgramData\WSL\Ubuntu"` 一步指定位置，免去再迁移。
```
