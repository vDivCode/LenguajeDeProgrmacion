# ============================================================
# clean.ps1 — Limpia archivos basura del proyecto Django
# Uso: .\clean.ps1
# ============================================================

Write-Host "🧹 Limpiando archivos basura..." -ForegroundColor Cyan

# Borrar carpetas __pycache__
$pycache = Get-ChildItem -Path . -Recurse -Filter "__pycache__" -Directory
foreach ($dir in $pycache) {
    Remove-Item -Recurse -Force $dir.FullName
    Write-Host "  ✓ Eliminado: $($dir.FullName)" -ForegroundColor Green
}

# Borrar archivos .pyc y .pyo
$pyc = Get-ChildItem -Path . -Recurse -Include "*.pyc", "*.pyo"
foreach ($file in $pyc) {
    Remove-Item -Force $file.FullName
    Write-Host "  ✓ Eliminado: $($file.FullName)" -ForegroundColor Green
}

# Borrar .pytest_cache
if (Test-Path ".pytest_cache") {
    Remove-Item -Recurse -Force ".pytest_cache"
    Write-Host "  ✓ Eliminado: .pytest_cache" -ForegroundColor Green
}

# Borrar db.sqlite3 (solo si no estás en producción)
if (Test-Path "db.sqlite3") {
    $respuesta = Read-Host "  ¿Eliminar db.sqlite3? (s/N)"
    if ($respuesta -eq "s" -or $respuesta -eq "S") {
        Remove-Item -Force "db.sqlite3"
        Write-Host "  ✓ Eliminado: db.sqlite3" -ForegroundColor Green
    } else {
        Write-Host "  ⏭ Conservado: db.sqlite3" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Limpieza completada." -ForegroundColor Cyan
