<div class="d-flex align-items-center justify-content-center" style="height: 90vh;">
    <form class="form w-50">
        <legend>Register</legend>
        <div class="mb-1">
            <label for="usernameInput" class="form-label">Username</label>
            <input type="text" class="form-control" id="usernameInput" name="username">
        </div>
        <div class="mb-1">
            <label for="exampleInputEmail1" class="form-label">Email address</label>
            <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" name="email">
            <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
        </div>
        <div class="mb-1">
            <label for="InputPassword" class="form-label">Password</label>
            <input type="password" class="form-control" id="InputPassword" name="password">
        </div>
        <div class="mb-1">
            <label for="confirmPassword" class="form-label">Confirm Password</label>
            <input type="password" class="form-control" id="confirmPassword" name="pass_confirm">
        </div>
        <div class="mb-1">
            <div class="alert alert-danger" role="alert" id="passwordMatchAlert" style="display: none;">
                Password and confirmation do not match!
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
        <div class="alert alert-danger" role="alert" id="errorMessage" style="display: none;"></div>
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
                url: '/register',
                type: 'POST',
                data: formData,
                success: function(response) {
                    document.location.replace("/pdf-maker")
                },
                error: function(error) {
                    var messages = error.responseJSON.messages;
                    var errorMessage = '';

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