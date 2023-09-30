<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/style.css">
    <style>
        header {
            position: absolute;
            width: 100%;
        }

        #main {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }

        form {
            margin-top: 2rem;
            display: flex;
        }

        form input[type=text] {
            background: transparent;
            color: white;
            border-style: solid;
            border-width: 2px 0 2px 2px;
            border-color: white transparent white white;
            border-radius: 14px 0 0 14px;
            padding: 0.75rem 1.25rem;
            font-size: 1.25rem;
            line-height: 1.75rem;
        }

        form input[type=text]::placeholder {
            color: #ccc;
        }

        form input[type=submit] {
            background-color: rgba(var(--accent-color), .8);
            transition: background-color 75ms ease-in-out;
            border: solid 2px var(--accent);
            color: #101011;
            font-weight: bold;
            border-radius: 0 14px 14px 0;
            cursor: pointer;
            padding: 0 1.25rem;
            font-size: 1.25rem;
            line-height: 1.75rem;
        }

        form input[type=submit]:hover {
            background-color: var(--accent);
        }
    </style>
    <title>TrashBin</title>
</head>

<body>
    <header>
        <nav>
            <a href="/">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                </svg>
                <div>
                    TrashBin
                </div>
            </a>

            <?php
            if (isset($_SESSION['username'])) {
            ?>
                <a href="/m/<?php echo $_SESSION['id']; ?>">
                    <div>
                        Welcome back, <u><?php echo $_SESSION['username']; ?></u>!
                    </div>
                </a>
            <?php
            }
            ?>
        </nav>
    </header>

    <section id="main">
        <h1>Welcome to <span class="accent">TrashBin</span>!</h1>
        <h2 style="margin-top: 3rem;">Test your APIs easily with this <s>request</s> trash bin.</h2>
        <h2>Put in your username to check out our demo!</h2>

        <form action="/" method="POST">
            <input type="text" name="username">
            <input type="submit" value="Start now!">
        </form>

        <?php
        if (isset($_GET['error'])) {
        ?>
            <small style="margin-top: 1rem; color: #ff8282;">Username must be at least 5 characters long</small>
        <?php
        }
        ?>
        <small style="margin-top: 1rem;">The free demo version has a limit of 20 logs per endpoint.</small>
    </section>


</body>

</html>