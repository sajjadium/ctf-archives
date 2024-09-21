<?php
$allowed_ip = ['localhost', '127.0.0.1'];

if (isset($_SERVER['HTTP_X_FORWARDED_FOR']) && in_array($_SERVER['HTTP_X_FORWARDED_FOR'], $allowed_ip)) {
    $allowed = true;
} else {
    $allowed = false;
}
?>

<!DOCTYPE html>
<html>

<head>
    <title>Giraffe Notes</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.tailwindcss.com?plugins=forms,typography,aspect-ratio,line-clamp"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        primary: {
                            "50": "#eff6ff",
                            "100": "#dbeafe",
                            "200": "#bfdbfe",
                            "300": "#93c5fd",
                            "400": "#60a5fa",
                            "500": "#3b82f6",
                            "600": "#2563eb",
                            "700": "#1d4ed8",
                            "800": "#1e40af",
                            "900": "#1e3a8a"
                        }
                    }
                },
                fontFamily: {
                    'body': [
                        'Inter',
                        'ui-sans-serif',
                        'system-ui',
                        '-apple-system',
                        'system-ui',
                        'Segoe UI',
                        'Roboto',
                        'Helvetica Neue',
                        'Arial',
                        'Noto Sans',
                        'sans-serif',
                        'Apple Color Emoji',
                        'Segoe UI Emoji',
                        'Segoe UI Symbol',
                        'Noto Color Emoji'
                    ],
                    'sans': [
                        'Inter',
                        'ui-sans-serif',
                        'system-ui',
                        '-apple-system',
                        'system-ui',
                        'Segoe UI',
                        'Roboto',
                        'Helvetica Neue',
                        'Arial',
                        'Noto Sans',
                        'sans-serif',
                        'Apple Color Emoji',
                        'Segoe UI Emoji',
                        'Segoe UI Symbol',
                        'Noto Color Emoji'
                    ]
                }
            }
        }
    </script>
</head>

<body class="bg-gray-900 grid h-screen place-items-center">
    <?php
    if (!$allowed) {
    ?>
        <div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
            <div class="mx-auto text-center">
                <h1 class="mb-4 text-7xl tracking-tight font-extrabold lg:text-9xl text-primary-600 text-primary-500">
                🦒
                </h1>
                <p class="mb-4 text-3xl tracking-tight font-bold text-gray-900 md:text-4xl text-white">
                    Hah! Bet you cant access my notes on giraffes! They're super secure!
                </p>
            </div>
        </div>
    <?php
    } else {
    ?>
        <section class="bg-gray-900 antialiased">
            <div class="max-w-screen-xl px-4 py-8 mx-auto lg:px-6 sm:py-16 lg:py-24">
                <div class="max-w-3xl mx-auto text-center">
                    <h2 class="text-4xl font-extrabold leading-tight tracking-tight text-gray-900 text-white">
                        Notes
                    </h2>
                    <div class="mt-4">
                        <span class="inline-flex items-center text-lg font-medium text-primary-600 dark:text-primary-500">
                            I like giraffes
                        </span>
                    </div>
                </div>
                <div class="flow-root max-w-3xl mx-auto mt-8 sm:mt-12 lg:mt-16">
                    <div class="-my-4 divide-y divide-gray-200 divide-gray-700">
                        <div class="flex flex-col gap-2 py-4 sm:gap-6 sm:flex-row sm:items-center">
                            <p class="w-32 text-lg font-normal text-gray-500 sm:text-right text-gray-400 shrink-0">
                                08:00 - 09:00
                            </p>
                            <h3 class="text-lg font-semibold text-gray-900 text-white">
                                <span>Look at giraffes</span>
                            </h3>
                        </div>

                        <div class="flex flex-col gap-2 py-4 sm:gap-6 sm:flex-row sm:items-center">
                            <p class="w-32 text-lg font-normal text-gray-500 sm:text-right text-gray-400 shrink-0">
                                09:00 - 10:00
                            </p>
                            <h3 class="text-lg font-semibold text-gray-900 text-white">
                                <span>Think about giraffes</span>
                            </h3>
                        </div>

                        <div class="flex flex-col gap-2 py-4 sm:gap-6 sm:flex-row sm:items-center">
                            <p class="w-32 text-lg font-normal text-gray-500 sm:text-right text-gray-400 shrink-0">
                                10:00 - 11:00
                            </p>
                            <h3 class="text-lg font-semibold text-gray-900 text-white">
                                <span>Learn about giraffes</span>
                            </h3>
                        </div>

                        <div class="flex flex-col gap-2 py-4 sm:gap-6 sm:flex-row sm:items-center">
                            <p class="w-32 text-lg font-normal text-gray-500 sm:text-right text-gray-400 shrink-0">
                                11:00 - Infinity
                            </p>
                            <h3 class="text-lg font-semibold text-gray-900 text-white">
                                <span>CACI{placeholder}</span>
                            </h3>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    <?php
    }
    ?>
</body>

</html>