<?php include_once("include/html_head.php") ?>

<main class="container">
    <h1>StylePen Spooktober Competition 2023</h1>
    <p>Compete with other CSS wizards to create the spookiest CSS snippet!</p>
    <div class="grid">
        <div>
            <form id="submission-form" method="POST" action="/submit.php">
                <textarea id="submission-code" class="code-area" name="css" required></textarea>
                <label for="email">Email</label>
                <input type="email" name="email" required>
            </form>
            <button id="submission-button">Submit</button>
        </div>
        <div>
            <div id="code-output"></div>
        </div>
    </div>
</main>

<script src="/static/purify.min.js"></script>
<script src="/static/widget.module.min.js"></script>
<script src="/static/app.js"></script>
</body>