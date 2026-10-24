# Dot-source this file from the project folder: . .\activate.ps1
$condaExe = Join-Path $env:USERPROFILE 'miniforge3\Scripts\conda.exe'
if (-not (Test-Path -LiteralPath $condaExe)) {
    throw 'Miniforge was not found. Use your own Conda installation to activate 290A.'
}
(& $condaExe 'shell.powershell' 'hook') | Out-String | Invoke-Expression
conda activate 290A
if ($LASTEXITCODE -ne 0) { throw 'Could not activate environment 290A.' }
python -c "import sys; print(sys.executable)"
