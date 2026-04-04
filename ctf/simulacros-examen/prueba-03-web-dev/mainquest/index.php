<?php
echo "<h1>Portal de Subida de Imágenes</h1>";
echo "<form method='POST' enctype='multipart/form-data'>
        <input type='file' name='fileToUpload'>
        <input type='submit' value='Subir'>
      </form>";

if(isset($_FILES['fileToUpload'])) {
    $target_dir = "uploads/";
    $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
    
    // VULNERABILIDAD: Unrestricted file upload. No comprueba tipo de extensión.
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo "<p>El archivo ha sido subido a root /uploads/" . basename( $_FILES["fileToUpload"]["name"]). "</p>";
    } else {
        echo "<p>Error subiendo el archivo.</p>";
    }
}
?>
