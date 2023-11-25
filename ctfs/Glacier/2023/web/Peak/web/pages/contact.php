<!DOCTYPE html>
<html lang="en">
    <?php
        include_once "../includes/session.php";
        include_once "../includes/header.php";
        include_once "../includes/csp.php";
    ?>
    <head>
    <style>
        body, html {
            height: 100%;
            overflow: hidden;
        }
        #contact {
            min-height: 100%;
            overflow: hidden;
        }
    </style>
    </head>
    <body>
        <?php include_once "../includes/menu.php"; ?>
        <header class="hero bg-primary text-white text-center py-5">
            <div class="container">
                <h1>Contact Us</h1>
                <p>We're here to help! </p>
            </div>
        </header>

    <section id="contact" class="py-5">
    <div class="container">
        <div class="row">
            <h2>Contact Us</h2>
            <div class="col-md-6">
                <form method="post" action="/actions/contact.php" enctype="multipart/form-data">
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" class="form-control" name="title" placeholder="Title" required <?php if(!isset($_SESSION['user'])) echo "disabled"?>>
                    </div>
                    <div class="form-group">
                        <label>Message</label>
                        <textarea class="form-control" name="content" rows="4"
                                  placeholder="Your Message" required <?php if(!isset($_SESSION['user'])) echo "disabled"?>></textarea>
                    </div>
                    <div class="mb-3">
                        <label>Choose Image</label>
                        <input type="file" class="form-control" id="image" name="image" accept="image/*" <?php if(!isset($_SESSION['user'])) echo "disabled"?>>
                    </div>
                    
                    <button type="submit" class="btn btn-primary" <?php if(!isset($_SESSION['user'])) echo "disabled"?>>Submit</button>
                    <?php if(!isset($_SESSION['user'])) : ?>
                        <h5>Please register/login first to issue requests!</h5>
                    <?php endif;?>
                </form>
                <?php include_once "../includes/error.php"; ?>
            </div>
            <div class="col-md-6">
            <p>Your experience on our website is important to us, and we want to ensure it's as smooth and enjoyable as possible. If you have any questions, concerns, or issues while using our site, don't hesitate to reach out to us. Our dedicated team is ready to assist you and will make sure to address your request as soon as possible.</p>
        
            <h3>Why Contact Us?</h3>
            <ul>
                <li><strong>Questions:</strong> Whether you're curious about the history, directions, or activities, we're here to provide answers.</li>
                <li><strong>Technical Issues:</strong> If you encounter any technical errors, or difficulties navigating our site, let us know so we can swiftly address them.</li>
                <li><strong>Feedback:</strong> Your feedback helps us improve. Share your thoughts, suggestions, or ideas to make our website even better.</li>
            </ul>
            </div>
        </div>
    </div>
</section>
</body>
<?php include "../includes/footer.php"?>
</html>