<?php
echo "<h1>Herramienta de Diagnóstico de Red</h1>";
echo "<p>Verifica si un host está vivo:</p>";
echo "<form method='GET'>
        <input type='text' name='ip' placeholder='8.8.8.8'>
        <input type='submit' value='Ping'>
      </form>";

if (isset($_GET['ip'])) {
    $target = $_GET['ip'];
    echo "<pre>";
    // VULNERABILIDAD: CMDi Directo por falta de sanitización
    system("ping -c 3 " . $target);
    echo "</pre>";
}
?>
