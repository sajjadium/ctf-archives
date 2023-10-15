<div class="d-flex align-items-center justify-content-center" style="height: 90vh;">
    <form class="form w-50">
        <legend>Login</legend>
        <div class="mb-1">
            <label for="usernameInput" class="form-label">Username</label>
            <input type="text" class="form-control" id="usernameInput" name="username">
        </div>
        <div class="mb-1">
            <label for="InputPassword" class="form-label">Password</label>
            <input type="password" class="form-control" id="InputPassword" name="password">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
        <div class="alert alert-danger" role="alert" id="errorMessage" style="display: none;">
            <?php if(isset($_GET['message'])){echo $_GET['message'];};?>
        </div>
    </form>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<script>
    $(document).ready(function() {
        $('form.form').on('submit', function(e) {
            e.preventDefault(); // Prevent form submission

            // Get form data
            var formData = $(this).serialize();

            // Send AJAX request
            $.ajax({
                url: '/login',
                type: 'POST',
                data: formData,
                success: function(response) {
                    document.location.replace("/pdf-maker")
                },
                error: function(error) {
                    var messages = error.responseJSON;
                    var errorMessage = '';
                    console.log(messages)
                    // Generate error message from key-value pairs
                    for (var key in messages) {
                        errorMessage += key + ': ' + messages[key] + '<br>';
                    }

                    // Display the error message in the danger box
                    $('#errorMessage').html(errorMessage).show();
                }
            });
        });
    });
</script>
