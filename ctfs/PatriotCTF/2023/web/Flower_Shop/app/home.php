<?php

session_start();

if (!isset($_SESSION['userid'])) {
    header("Location: login.php");
    exit();
} 

?>


<?php include "templates/header.php"; ?>
    <div class="container">
        <h3>Buy seeds for the flowers of your dreams!</h3>

        <div class="flower-grid">
        <div class="flower-item">
                <div class="flower-image">
                    <img src="public/images/flower1.jpg" alt="Flower Image">
                    <div class="flower-name">
                        <h3>Aurelia Crimsonvale</h3>
                    </div>
                </div>
                <p>Price: $25.00</p>
                <button>Add to Cart</button>
            </div>

            <div class="flower-item">
                <div class="flower-image">
                    <img src="public/images/flower2.jpg" alt="Flower Image">
                    <div class="flower-name">
                        <h3>Blossomlush</h3>
                    </div>
                </div>
                <p>Price: $32.00</p>
                <button>Add to Cart</button>
            </div>

            <div class="flower-item">
                <div class="flower-image">
                    <img src="public/images/flower3.jpg" alt="Flower Image">
                    <div class="flower-name">
                        <h3>Lavendark</h3>
                    </div>
                </div>
                <p>Price: $17.00</p>
                <button>Add to Cart</button>
            </div>

            <div class="flower-item">
                <div class="flower-image">
                    <img src="public/images/flower4.jpg" alt="Flower Image">
                    <div class="flower-name">
                        <h3>Amethyst Thorn</h3>
                    </div>
                </div>
                <p>Price: $15.00</p>
                <button>Add to Cart</button>
            </div>

            <div class="flower-item">
                <div class="flower-image">
                    <img src="public/images/flower5.jpg" alt="Flower Image">
                    <div class="flower-name">
                        <h3>Azure Twistvine</h3>
                    </div>
                </div>
                <p>Price: $40.00</p>
                <button>Add to Cart</button>
            </div>

            <div class="flower-item">
                <div class="flower-image">
                    <img src="public/images/flower6.jpg" alt="Flower Image">
                    <div class="flower-name">
                        <h3>Sunfire</h3>
                    </div>
                </div>
                <p>Price: $30.00</p>
                <button>Add to Cart</button>
            </div>

            <div class="flower-item">
                <div class="flower-image">
                    <img src="public/images/flower7.jpg" alt="Flower Image">
                    <div class="flower-name">
                        <h3>Fuchsia Blaze</h3>
                    </div>
                </div>
                <p>Price: $28.00</p>
                <button>Add to Cart</button>
            </div>

            <div class="flower-item">
                <div class="flower-image">
                    <img src="public/images/flower8.jpg" alt="Flower Image">
                    <div class="flower-name">
                        <h3>Mossrose</h3>
                    </div>
                </div>
                <p>Price: $44.00</p>
                <button>Add to Cart</button>
            </div>

            <div class="flower-item">
                <div class="flower-image">
                    <img src="public/images/flower9.jpg" alt="Flower Image">
                    <div class="flower-name">
                        <h3>Amberwhisper</h3>
                    </div>
                </div>
                <p>Price: $50.00</p>
                <button>Add to Cart</button>
            </div>
        </div>
    </div>
<?php include "templates/footer.php"; ?>
