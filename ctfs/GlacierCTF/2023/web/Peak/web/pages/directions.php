<?php
    include_once "../includes/session.php";
?>
<!DOCTYPE html>
<html lang="en">
	<?php include_once "../includes/header.php"; ?>
    <body>
        <?php include_once "../includes/menu.php"; ?>

        <header class="hero bg-primary text-white text-center py-5">
            <div class="container">
                <h1>Directions to the Großglockner Peak</h1>
                <p>Reach the peak by car</p>
            </div>
        </header>

        <section id="directions" class="py-5">
            <div class="container">
            <h2>About the journey:</h2>
                <ol>
                    <li><strong>Starting Point:</strong> Vienna, Austria (This is a commonly used starting point, but you can adapt these directions based on your specific location)</li>
                    <li><strong>Destination:</strong> Grossglockner High Alpine Road, Grossglockner Mountain, Austria</li>
                    <li><strong>Distance:</strong> Approximately 340 kilometers (211 miles)</li>
                    <li><strong>Estimated Time:</strong> About 4.5 to 5.5 hours, depending on traffic and road conditions</li>
                </ol>

                <h2>Directions:</h2>

                <ol>
                    <li><strong>Head South on A2:</strong> Start your journey by driving south on the A2 Autobahn (motorway) from Vienna. Follow the signs for "Graz" and "Klagenfurt."</li>
                    <li><strong>Continue on A2:</strong> Stay on the A2 Autobahn for about 240 kilometers (149 miles) until you reach the city of Villach.</li>
                    <li><strong>Take Exit 364-Villach-Ossiacher See:</strong> Take the exit onto the A10 Autobahn (Tauern Autobahn) toward "Spittal/Drau" and "Lienz."</li>
                    <li><strong>Continue on A10:</strong> Drive on the A10 Autobahn for approximately 100 kilometers (62 miles) in the direction of Spittal an der Drau and Lienz.</li>
                    <li><strong>Exit at Spittal-Millstätter See:</strong> Take exit 139-Spittal-Millstätter See from A10.</li>
                    <li><strong>Follow B106:</strong> After exiting the A10, follow the B106 road signs toward "Lienz" and "Möllbrücke."</li>
                    <li><strong>Continue on B106:</strong> Stay on the B106 road as it winds through picturesque landscapes. You'll pass towns like Mühldorf, Flattach, and Heiligenblut.</li>
                    <li><strong>Arrival at Grossglockner High Alpine Road:</strong> Eventually, you'll arrive at the entrance to the Grossglockner High Alpine Road. Pay the toll fee (if applicable) and start your scenic drive up the Grossglockner mountain.</li>
                    <li><strong>Taking the High Alpine Road:</strong> Be prepared for steep and winding roads as you ascend the Grossglockner. Enjoy the breathtaking Alpine scenery and make stops at designated viewpoints to capture the stunning vistas.</li>
                    <li><strong>Arrival at the Summit:</strong> Follow the road until you reach the Grossglockner summit area. There, you can explore various viewpoints, visit the visitor center, and take in the magnificent views of the surrounding mountains.</li>
                </ol>
            </div>
        </section>

        <section id="map" class="py-5">
            <div class="container">
                <div class="panel panel-default">
                        <div class="panel-body">
                            <div class="card header">
                                <div class="card-body">
                                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
                                    <div id="map" style="height: 500px;"/>
                                    <script>var map = L.map('map').setView([0, 0], 9);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);L.marker(["47.0748663672","12.695247219"]).addTo(map).bindPopup("Großglockner").openPopup();map.setView(["47.0748663672","12.695247219"], 9);</script>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </body>
<?php include "../includes/footer.php"?>
</html>