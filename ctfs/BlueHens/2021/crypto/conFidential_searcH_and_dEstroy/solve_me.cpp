#include <tfhe/tfhe.h>
#include <tfhe/tfhe_io.h>
#include <cstdio>
#include <algorithm>
#include <cstdlib>
#include <string>
#include <unistd.h>
#include <sstream>
#include <iostream>
#include "base64.h"

#define X_SIZE 7
#define Y_SIZE 7
#define Z_SIZE 7
#define IDX_SIZE 3

using namespace std;

// Circuit that performs an addition by 1 (i.e. ctxt++)
void increment(LweSample* result, const TFheGateBootstrappingCloudKeySet* bk) {

    // Declare intermediate ctxt arrays
    LweSample* carry = new_gate_bootstrapping_ciphertext_array(IDX_SIZE, bk->params);
    LweSample* temp_result = new_gate_bootstrapping_ciphertext_array(IDX_SIZE, bk->params);

    // Set first carry bit to 1
    bootsCONSTANT(&carry[0], 1, bk);

    // Clear temp_result
    for (int i = 0; i < IDX_SIZE; i++) {
      bootsCONSTANT(&temp_result[i], 0, bk);
    }

    // Perform cascaded 1-bit incrementers
    for (int i = 0; i < (IDX_SIZE - 1); i++) {
      bootsXOR(&temp_result[i], &carry[i], &result[i], bk);
      bootsAND(&carry[i+1], &carry[i], &result[i], bk);
    }

    // For the last stage, no need to compute an output carry
    bootsXOR(&temp_result[IDX_SIZE-1], &carry[IDX_SIZE-1], &result[IDX_SIZE-1], bk);

    // Copy temp_result to result bit by bit
    for (int i = 0; i < (IDX_SIZE); i++) {
      bootsCOPY(&result[i], &temp_result[i], bk);
    }

    // Clean up intermediate ctxt structures
    delete_gate_bootstrapping_ciphertext_array(IDX_SIZE, carry);
    delete_gate_bootstrapping_ciphertext_array(IDX_SIZE, temp_result);
}

void search_and_destroy(LweSample* result[3], LweSample* ocean[X_SIZE][Y_SIZE][Z_SIZE], const TFheGateBootstrappingCloudKeySet* bk) {
  // FIXME: Compute the encrypted coordinates
  // The "ocean" is a 3D array of encrypted 0's and a single encrypted 1.
  // This single encrypted 1 represents the location of the enemy submarine.
  // Compute the X, Y, and Z coordinates of this submarine homomorphically.
}

int main() {

  // read eval key (Download and place in same dir)
  FILE* cloud_key = fopen("eval.key","rb");
  TFheGateBootstrappingCloudKeySet* bk = new_tfheGateBootstrappingCloudKeySet_fromFile(cloud_key);
  fclose(cloud_key);
  const TFheGateBootstrappingParameterSet* params = bk->params;

  string ctxts = ""; // FIXME: PASTE CTXT ARRAY HERE

  replace( ctxts.begin(), ctxts.end(), ' ', '\n' ); // add newline after each ctxt
  istringstream ctxts_ss(ctxts); // TFHE supports reading from streams

  macaron::Base64 encoder; // compress/decompress ctxts when sending/receiving

  // import 3D array (encrypted map of ocean)
  LweSample* ctxt[X_SIZE][Y_SIZE][Z_SIZE];
  for (int i = 0; i < X_SIZE; i++) {
    for (int j = 0; j < Y_SIZE; j++) {
      for (int k = 0; k < Z_SIZE; k++) {
        string single_ctxt;
        string decoded_ctxt;
        getline(ctxts_ss, single_ctxt); // fetch a single ctxt from stream
        single_ctxt = encoder.Decode(single_ctxt, decoded_ctxt); // decode base64
        istringstream ctxt_ss(decoded_ctxt); // new stream with one ctxt
        ctxt[i][j][k] = new_gate_bootstrapping_ciphertext(params);
        import_gate_bootstrapping_ciphertext_fromStream(ctxt_ss, ctxt[i][j][k], params);
      }
    }
  }

  // result is a set of coordinates (X,Y,Z) where each subcoordinate is 3 bits
  LweSample* result[3];
  for (int i = 0; i < 3; i++) {
    result[i] = new_gate_bootstrapping_ciphertext_array(IDX_SIZE, params);
  }

  search_and_destroy(result, ctxt, bk); // do the work

  stringstream ss;

  // print X coordinate starting at bit 0
  for (int j = 0; j < IDX_SIZE; j++) {
    export_gate_bootstrapping_ciphertext_toStream(ss, &result[0][j], params);
    cout << encoder.Encode(ss.str()) << endl;
    ss.str( string() );
    ss.clear();
  }

  // print Y coordinate starting at bit 0
  for (int j = 0; j < IDX_SIZE; j++) {
    export_gate_bootstrapping_ciphertext_toStream(ss, &result[1][j], params);
    cout << encoder.Encode(ss.str()) << endl;
    ss.str( string() );
    ss.clear();
  }

  // print Z coordinate starting at bit 0
  for (int j = 0; j < IDX_SIZE; j++) {
    export_gate_bootstrapping_ciphertext_toStream(ss, &result[2][j], params);
    cout << encoder.Encode(ss.str()) << endl;
    ss.str( string() );
    ss.clear();
  }

  // clean up
  delete_gate_bootstrapping_cloud_keyset(bk);

  for (int i = 0; i < X_SIZE; i++) {
    for (int j = 0; j < Y_SIZE; j++) {
      for (int k = 0; k < Z_SIZE; k++) {
        delete_gate_bootstrapping_ciphertext(ctxt[i][j][k]);
      }
    }
  }

  for (int i = 0; i < 3; i++) {
    delete_gate_bootstrapping_ciphertext_array(IDX_SIZE, result[i]);
  }
}
