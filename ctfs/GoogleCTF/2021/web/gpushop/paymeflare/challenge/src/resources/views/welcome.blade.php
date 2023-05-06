<html>
<head>
   <title>paymeflare</title>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <meta name="csrf-token" content="{{csrf_token()}}">
   <link href="{{ mix('css/app.css') }}" rel="stylesheet">
   <style>
       .bd-placeholder-img {
         font-size: 1.125rem;
         text-anchor: middle;
         -webkit-user-select: none;
         -moz-user-select: none;
         user-select: none;
       }

       @media (min-width: 768px) {
         .bd-placeholder-img-lg {
           font-size: 3.5rem;
         }
       }
       #app {
          
       }
   </style>
</head>
<body>
   <div id="app">
      <app></app>
   </div>
<script>var client_id = @json($client_id);</script>
<script src="{{ mix('js/app.js') }}"></script>
</body>
</html>
