$inputFile = "urlvalidar.txt"
$outputFile = "url.txt"
$pythonScript = "validacc.py"
$blockSize = 10

# Leer todas las líneas no vacías del archivo
$lines = Get-Content $inputFile | Where-Object { $_.Trim() -ne "" }

# Filtrar solo las líneas que no están marcadas como *a
$pendingUrls = @()
foreach ($line in $lines) {
    if (-not $line.Trim().EndsWith("*a")) {
        $pendingUrls += $line.Trim()
    }
}

for ($i = 0; $i -lt $pendingUrls.Count; $i += $blockSize) {
    $block = $pendingUrls[$i..([Math]::Min($i + $blockSize - 1, $pendingUrls.Count - 1))]

    foreach ($url in $block) {
        $urlTrim = $url.Trim()

        # Marcar la URL con *a en el archivo original
        $lines = $lines | ForEach-Object {
            if ($_ -eq $urlTrim) { "$_ *a" } else { $_ }
        }
        Set-Content -Path $inputFile -Value $lines

        try {
            $response = Invoke-WebRequest -Uri $urlTrim -Method Head -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Add-Content -Path $outputFile -Value $urlTrim
                Write-Host "✅ Válida: $urlTrim"
            }
        } catch {
            # Silenciar errores
        }

        Start-Sleep -Seconds (Get-Random -Minimum 1 -Maximum 3)
    }

    # Ejecutar el script Python en nueva consola de PowerShell
    if (Test-Path ".\$pythonScript") {
        Write-Host "🚀 Ejecutando '$pythonScript' en nueva consola..."
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "python `"$PWD\$pythonScript`""
    } else {
        Write-Host "⚠️ No se encontró el archivo '$pythonScript'"
    }
}

Write-Host "`n✅ Proceso completo. Las URLs válidas están en '$outputFile'"
