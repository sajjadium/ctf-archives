#include <stdio.h>
#include <string.h>

#include <wasmedge/wasmedge.h>

#define MAX_HEX_LEN 4096

// Convert hex string to binary. Return length of binary.
size_t from_hex(char *hex, uint8_t *data) {
  size_t len;
  for (len = 0; len < MAX_HEX_LEN; len++) {
    // only hex chars allowed
    if (!((hex[len] >= '0' && hex[len] <= '9') ||
          (hex[len] >= 'a' && hex[len] <= 'f') ||
          (hex[len] >= 'A' && hex[len] <= 'F'))) {
      break;
    }
  }
  // must have even number of hex chars for valid hex string
  if (len % 2 != 0) {
    return 0;
  }

  // convert to bytes using sscanf
  size_t i, j;
  for (i = 0, j = 0; i < len; i += 2, j++) {
    sscanf(hex + i, "%2hhx", &data[j]);
  }
  // return the final length
  return j;
}

int main() {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);

  printf("--- WASM as a service ---\n");
  printf("We run any WASM code you provide.\n");
  printf("This is a secure sandbox.\n");
  printf("The wasm file must have a main function that takes a 32-bit integer and returns\n");
  printf("a 32-bit integer\n\n");

  while(1) {
    printf("Enter a hex encoded WASM file (max %d hex chars):\n", MAX_HEX_LEN - 1);

    char buf[MAX_HEX_LEN];
    if (fgets(buf, MAX_HEX_LEN, stdin) == NULL) {
      printf("Error reading input\n");
      return 1;
    }
    uint8_t wasm_data[MAX_HEX_LEN/2];
    size_t len = from_hex(buf, wasm_data);

    printf("Enter a 32-bit integer input: ");
    uint32_t input;
    if (scanf("%d", &input) != 1) {
      printf("Error reading input\n");
      return 1;
    }

    WasmEdge_VMContext *VMCxt = WasmEdge_VMCreate(NULL, NULL);
    WasmEdge_Value Params[1] = { WasmEdge_ValueGenI32(input) };
    WasmEdge_Value Returns[1];
    WasmEdge_String FuncName = WasmEdge_StringCreateByCString("main");
    WasmEdge_Result Res;

    Res = WasmEdge_VMRunWasmFromBuffer(VMCxt, wasm_data, len, FuncName, Params, 1, Returns, 1);

    if (WasmEdge_ResultOK(Res)) {
      printf("Output: %d\n", WasmEdge_ValueGetI32(Returns[0]));
    } else {
      printf("Error.\n");
      return 1;
    }

    // cleanup
    WasmEdge_VMDelete(VMCxt);
    WasmEdge_StringDelete(FuncName);

    int c;
    // flush newlines
    while ((c = getchar()) != '\n' && c != EOF) { }

    printf("Run another file? (y/n): ");
    char go_again;
    if (scanf("%c", &go_again) != 1) {
      printf("Error reading input\n");
      return 1;
    }
    if (go_again != 'y') {
      break;
    }

    // flush newlines
    while ((c = getchar()) != '\n' && c != EOF) { }
  }

  return 0;
}
