param()
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$releaseVersion = (Get-Content -LiteralPath (Join-Path $projectRoot 'theme.json') -Raw | ConvertFrom-Json).version
$bundleFolder = Join-Path $projectRoot "dist/$releaseVersion/zen-notes"
New-Item -ItemType Directory -Force -Path $bundleFolder | Out-Null
$bundleFiles = @('zen-notes-core.uc.js','zen-notes-editor.uc.js','zen-notes-ui.uc.js','style.css','theme.json','mod.json','preferences.json','LICENSE','README.md','install.md','PERSONAL-INSTALL.md')
foreach ($bundleFile in $bundleFiles) {
    Copy-Item -LiteralPath (Join-Path $projectRoot $bundleFile) -Destination $bundleFolder -Force
}
$bundleArchive = Join-Path $projectRoot "zen-notes-$releaseVersion.zip"
Compress-Archive -LiteralPath $bundleFolder -DestinationPath $bundleArchive -Force
Write-Output $bundleArchive
