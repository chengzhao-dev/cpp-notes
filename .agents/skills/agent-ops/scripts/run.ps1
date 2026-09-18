<#
.SYNOPSIS
仓库维护命令的 Windows 入口。

.DESCRIPTION
只读取 .agents/manifest.json 的 mcp.command，验证指定解释器后执行同目录的 run.py。
不从 PATH、环境变量或其他运行时配置选择 Python。
#>

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Arguments
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
$manifestPath = Join-Path $root '.agents\manifest.json'
$runnerPath = Join-Path $PSScriptRoot 'run.py'

try {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $python = [string]$manifest.mcp.command
} catch {
    Write-Error "无法读取 .agents/manifest.json；请修复该文件后重试。"
    exit 1
}

if ([string]::IsNullOrWhiteSpace($python) -or -not (Test-Path -LiteralPath $python -PathType Leaf)) {
    Write-Error "manifest.mcp.command 不可执行：$python；请修复 .agents/manifest.json。"
    exit 1
}

$versionText = & $python -c 'import sys; print(sys.version_info[0], sys.version_info[1], sep=chr(46))' 2>$null
if ($LASTEXITCODE -ne 0 -or $versionText -notmatch '^3\.(\d+)$' -or [int]$Matches[1] -lt 12) {
    Write-Error "manifest.mcp.command 必须指向 Python >= 3.12：$python"
    exit 1
}

& $python $runnerPath @Arguments
exit $LASTEXITCODE
