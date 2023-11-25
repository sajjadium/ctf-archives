<?php
    include_once "includes/session.php";
?>
<!DOCTYPE html>
<html lang="en">
    <?php include_once "../includes/header.php"; ?>
    <body>
        <?php include_once "../includes/menu.php"; ?>
        
        <header class="hero bg-primary text-white text-center py-5">
            <div class="container">
                <h1>Edit map</h1>
                <p>Dev-Note: Please note editing map globally is currently not possible! We are working on it.<br>You can use this site to test out the coordinates for now.</p>
                <form method="post" action="/admin/map.php">
                    <div class="form-group">
                        <textarea class="form-control" name="data" rows="7"><?php $xmlFilePath="./data.example"; echo file_get_contents($xmlFilePath);?></textarea>
                    </div>
                    <br>
                    <button type="submit" class="btn btn-light btn-lg">Submit</button>
                </form>
            </div>
        </header>

        <section id="map" class="py-5">
            <div class="container">
                <div class="panel panel-default">
                        <div class="panel-body">
                            <div class="card header">
                                <div class="card-body">
                                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
                                    <div id="map" style="height: 500px;"/>
                                    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
                                    <script>
                                    var map = L.map('map').setView([0, 0], 12);
                                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
                                    <?php
                                    function parseXML($xmlData)
                                    {
                                        try
                                        {
                                            libxml_disable_entity_loader(false);
                                            $xml = simplexml_load_string($xmlData, 'SimpleXMLElement', LIBXML_NOENT);
                                            return $xml;
                                        }
                                        catch(Exception $ex)
                                        {
                                            return false;
                                        }
                                        return true;
                                    }
                                    
                                    try
                                    {
                                        $xmlData = "";
                                        if ($_SERVER["REQUEST_METHOD"] === "POST") 
                                        {
                                            $xmlData = $_POST["data"];
                                            if(!parseXML($xmlData))
                                                $xmlData = "";
                                        }
                                        if($xmlData === "")
                                        {
                                            $xmlData = file_get_contents($xmlFilePath);
                                        }
                                        $xml = parseXML($xmlData);
                                        foreach($xml->marker as $marker)
                                        {
                                            $name = str_replace("\n", "\\n", $marker->name);
                                            echo 'L.marker(["' . $marker->lat . '", "' . $marker->lon.'"]).addTo(map).bindPopup("'.  $name. '").openPopup();' . "\n";
                                            echo 'map.setView(["' . $marker->lat . '", "' . $marker->lon.'"], 9);' . "\n";
                                        }
                                    }
                                    catch(Exception $ex)
                                    {
                                        echo "Invalid xml data!";
                                    }
                                    ?>
                                    </script>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </section>
    </body>
</html>
