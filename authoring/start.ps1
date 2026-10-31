param(
    [string]$Workspace,
    [string]$Module,
    [string]$Prototyper = "C:\Users\pniu\Projects\niu-prototyper",
    [switch]$NoOpen
)
$ErrorActionPreference = "Stop"
if ($Module -and $Module -cnotmatch '^[a-z0-9]+(-[a-z0-9]+)*$') { throw "Invalid module ID. Run python authoring/catalog.py list." }
if (-not $Workspace) {
    $workspaceName = if ($Module) { "modules\$Module" } else { "grounded-workspace" }
    $Workspace = Join-Path $env:LOCALAPPDATA "STEMAuthoring\$workspaceName"
}
$repoPath = Split-Path $PSScriptRoot -Parent
$workspaceLinux = (& wsl.exe -e wslpath -a -u $Workspace).Trim()
$repoLinux = (& wsl.exe -e wslpath -a -u $repoPath).Trim()
$engineLinux = (& wsl.exe -e wslpath -a -u $Prototyper).Trim()
if ($LASTEXITCODE -ne 0) { throw "WSL path conversion failed." }
$launchArgs = @("-e", "python3", "$repoLinux/authoring/start.py", "--workspace", $workspaceLinux, "--repo", $repoLinux, "--engine", $engineLinux)
if ($NoOpen) { $launchArgs += "--no-open" }
if ($Module) { $launchArgs += @("--module", $Module) }
& wsl.exe @launchArgs
if ($LASTEXITCODE -ne 0) { throw "Authoring launch failed. See the error above." }
