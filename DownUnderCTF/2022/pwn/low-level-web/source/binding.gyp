{
  "targets": [
    {
      "target_name": "fast_convert",
      "cflags": ["-fno-exceptions", "-U_FORTIFY_SOURCE"],
      "sources": [
        "./src/encoder.cpp",
        "./src/index.cpp"
      ],
      "include_dirs": [
        "<!@(node -p \"require('node-addon-api').include\")"
      ],
      "defines": ["NAPI_DISABLE_CPP_EXCEPTIONS"],
    }
  ]
}
