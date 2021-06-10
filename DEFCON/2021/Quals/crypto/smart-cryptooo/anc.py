#!/usr/bin/env python3

# This file is an implementation of Adversarial Neural CryptOOOgrapy

#pylint:disable=unexpected-keyword-arg,unused-import

import tensorflow.keras as keras
import tensorflow as tf
import itertools
import binascii
import random
import string
import struct
import numpy as np
import tqdm
import sys
import os

from tensorflow.keras import backend as K

# configurable stuff
bits = 64
bunch_size = 16
m_bits = bits
m_bytes = bits//8
k_bits = bits
c_bits = bits
pad = 'same'

#
# Meet Alice, your friendly neighborhood encryptor network.
#

alice_plain = keras.layers.Input(shape=(m_bits,))
alice_key = keras.layers.Input(shape=(k_bits,))
def make_alice(plaintext=alice_plain, key=alice_key, name='alice'):
    """
    Make Alice network, who encrypts messages with the key.
    """
    ainput = keras.layers.concatenate([plaintext, key], axis=1)
    adense1 = keras.layers.Dense(units=(m_bits + k_bits))(ainput)
    adense1a = keras.layers.Activation('sigmoid')(adense1)
    areshape = keras.layers.Reshape((m_bits + k_bits, 1,))(adense1a)
    aconv1 = keras.layers.Conv1D(filters=2, kernel_size=4, strides=1, padding=pad)(areshape)
    aconv1a = keras.layers.Activation('sigmoid')(aconv1)
    aconv2 = keras.layers.Conv1D(filters=4, kernel_size=2, strides=2, padding=pad)(aconv1a)
    aconv2a = keras.layers.Activation('sigmoid')(aconv2)
    aconv3 = keras.layers.Conv1D(filters=4, kernel_size=1, strides=1, padding=pad)(aconv2a)
    aconv3a = keras.layers.Activation('sigmoid')(aconv3)
    aconv4 = keras.layers.Conv1D(filters=1, kernel_size=1, strides=1, padding=pad)(aconv3a)
    aconv4a = keras.layers.Activation('tanh')(aconv4)
    aoutput = keras.layers.Flatten()(aconv4a)

    return keras.models.Model([plaintext, key], aoutput, name=name)

alice_model = make_alice()
alice_cipher = alice_model([alice_plain, alice_key]) # the symbolic encryption result, for later shenanigans

#
# Meet Bob, your devoted decryption network.
#

bob_cipher = keras.layers.Input(shape=(m_bits,))
bob_key = keras.layers.Input(shape=(k_bits,))
def make_bob(ciphertext=bob_cipher, key=bob_key, name='bob'):
    """
    Make bob network, who decrypts messages with the key.
    """
    binput = keras.layers.concatenate([ciphertext, key], axis=1)
    bdense1 = keras.layers.Dense(units=(m_bits + k_bits))(binput)
    bdense1a = keras.layers.Activation('sigmoid')(bdense1)
    breshape = keras.layers.Reshape((m_bits + k_bits, 1,))(bdense1a)
    bconv1 = keras.layers.Conv1D(filters=2, kernel_size=4, strides=1, padding=pad)(breshape)
    bconv1a = keras.layers.Activation('sigmoid')(bconv1)
    bconv2 = keras.layers.Conv1D(filters=4, kernel_size=2, strides=2, padding=pad)(bconv1a)
    bconv2a = keras.layers.Activation('sigmoid')(bconv2)
    bconv3 = keras.layers.Conv1D(filters=4, kernel_size=1, strides=1, padding=pad)(bconv2a)
    bconv3a = keras.layers.Activation('sigmoid')(bconv3)
    bconv4 = keras.layers.Conv1D(filters=1, kernel_size=1, strides=1, padding=pad)(bconv3a)
    bconv4a = keras.layers.Activation('tanh')(bconv4)
    boutput = keras.layers.Flatten()(bconv4a)

    return keras.models.Model([ciphertext, key], boutput, name=name)

bob_model = make_bob()
bob_plain = bob_model( [alice_cipher, bob_key] ) # symbolic decryption result for later shenanigans


#
# Meet Eve, your dastardly artificial busybody.
#

eve_cipher = keras.layers.Input(shape=(c_bits,))
def make_eve(ciphertext=eve_cipher, name='eve'):
    """
    Make Eve network, who tries to decrypt messages without the key.
    """
    edense1 = keras.layers.Dense(units=(c_bits + k_bits))(ciphertext)
    edense1a = keras.layers.Activation('sigmoid')(edense1)
    edense2 = keras.layers.Dense(units=(c_bits + k_bits))(edense1a)
    edense2a = keras.layers.Activation('sigmoid')(edense2)
    ereshape = keras.layers.Reshape((c_bits + k_bits, 1,))(edense2a)
    econv1 = keras.layers.Conv1D(filters=2, kernel_size=4, strides=1, padding=pad)(ereshape)
    econv1a = keras.layers.Activation('sigmoid')(econv1)
    econv2 = keras.layers.Conv1D(filters=4, kernel_size=2, strides=2, padding=pad)(econv1a)
    econv2a = keras.layers.Activation('sigmoid')(econv2)
    econv3 = keras.layers.Conv1D(filters=4, kernel_size=1, strides=1, padding=pad)(econv2a)
    econv3a = keras.layers.Activation('sigmoid')(econv3)
    econv4 = keras.layers.Conv1D(filters=1, kernel_size=1, strides=1, padding=pad)(econv3a)
    econv4a = keras.layers.Activation('tanh')(econv4)
    eoutput = keras.layers.Flatten()(econv4a)# Eve's attempt at guessing the plaintext

    return keras.models.Model(eve_cipher, eoutput, name=name)

eve_model = make_eve()
eve_out = eve_model( alice_cipher ) # symbolic cracked result for later shenanigans


#
# Build and compile the composite model, used for training Alice-Bob networks against Eve
#

eve_loss = K.mean(  K.sum(K.abs(alice_plain - eve_out), axis=-1) )
bob_loss = K.mean(  K.sum(K.abs(alice_plain - bob_plain), axis=-1) )
abe_loss = bob_loss + K.square(m_bits/2 - eve_loss)/( (m_bits//2)**2 )

abeoptim = keras.optimizers.Adam(lr=0.0008)
abe_model = keras.models.Model([alice_plain, alice_key, bob_key], bob_plain, name='abemodel')
abe_model.add_loss(abe_loss)
abe_model.compile(optimizer=abeoptim)

#
# Build and compile the Eve model, used for training Eve net (with Alice frozen)
#

alice_model.trainable = False
eveoptim = keras.optimizers.Adam(lr=0.0008) #default 0.001
eve_model = keras.models.Model([alice_plain, alice_key], eve_out, name='evemodel')
eve_model.add_loss(eve_loss)
eve_model.compile(optimizer=eveoptim)

#
# We'll try to load networks if we have them!
#

try:
    alice_model.load_weights(f"alice-{bits}-weights.h5")
    bob_model.load_weights(f"bob-{bits}-weights.h5")
    eve_model.load_weights(f"eve-{bits}-weights.h5")
except OSError as _e:
    print("[!]")
    print(f"[!] MODEL WEIGHTS NOT LOADED: {_e}")
    print("[!]")

def encode_message(m):
    """
    Encodes bytes into ML inputs.
    """
    n = int(binascii.hexlify(m).ljust(m_bytes*2, b'0'), 16)
    encoded = [ (-1 if b == '0' else 1 ) for b in bin(n)[2:].rjust(m_bits, '0') ]
    assert decode_message(encoded) == m
    return encoded

def decode_message(a, threshold=0):
    """
    Decodes ML output into bytes.
    """
    i = int(''.join('0' if b < threshold else '1' for b in a), 2)
    return binascii.unhexlify(hex(i)[2:].rjust(m_bytes*2, '0'))

def encrypt_messages(messages, initial_key):
    encoded_key = encode_message(initial_key)
    encoded_messages = [ encode_message(m) for m in messages ]

    encrypted_messages = [ ]
    while encoded_messages:
        next_bunch, encoded_messages = encoded_messages[:bunch_size], encoded_messages[bunch_size:]
        if len(next_bunch) == bunch_size:
            next_key = encode_message(''.join(random.choice(string.ascii_letters+string.digits+string.punctuation) for _ in range(bits//8)).encode('latin1'))
            next_bunch += [next_key]

        next_bunch = np.array(next_bunch, dtype=np.float32)
        keys = np.array([encoded_key]*next_bunch.shape[0], dtype=np.float32)
        encrypted_bunch = alice_model.predict([next_bunch, keys])

        encrypted_messages += encrypted_bunch.tolist()
        encoded_key = next_key

    return encrypted_messages

def encrypt_bytes(text, initial_key):
    assert type(text) is bytes
    assert type(initial_key) is bytes
    messages = [ text[i:i+m_bytes].ljust(m_bytes) for i in range(0, len(text), m_bytes) ]
    encrypted_messages = encrypt_messages(messages, initial_key)
    encrypted_text = b"".join(struct.pack(f"{bits}d", *m) for m in encrypted_messages)
    return encrypted_text

def decrypt_bytes(text, initial_key):
    encrypted_messages = [ struct.unpack(f"{bits}d", text[i:i+bits*8]) for i in range(0, len(text), bits*8) ]
    decoded_messages = decrypt_messages(encrypted_messages, initial_key)
    decrypted_text = b"".join(decode_message(m) for m in decoded_messages)
    return decrypted_text

def decrypt_messages(messages, initial_key):
    assert type(initial_key) == bytes
    encoded_key = encode_message(initial_key)

    decrypted_messages = [ ]
    while messages:
        next_bunch, messages = messages[:bunch_size+1], messages[bunch_size+1:]
        next_bunch = np.array(next_bunch, dtype=np.float32)
        keys = np.array([encoded_key]*next_bunch.shape[0], dtype=np.float32)
        decrypted_bunch = bob_model.predict([next_bunch, keys]).tolist()
        if len(decrypted_bunch) == bunch_size + 1:
            encoded_key = encode_message(decode_message(decrypted_bunch[-1]))
            decrypted_messages += decrypted_bunch[:bunch_size]

    return decrypted_messages

def encrypt_file(src_file, dst_file, initial_key):
    with open(src_file, "rb") as sf:
        m = sf.read()
    c = encrypt_bytes(m, initial_key)
    with open(dst_file, "wb") as df:
        df.write(c)

def decrypt_file(src_file, dst_file, initial_key):
    with open(src_file, "rb") as sf:
        c = sf.read()
    m = decrypt_bytes(c, initial_key)
    with open(dst_file, "wb") as df:
        df.write(m)

def do_train(batch_size=4096):
    try:
        for step in itertools.count():
            # Train the A-B+E network
            alice_model.trainable = True
            m_batch = K.random_uniform((batch_size, k_bits), minval=-1, maxval=1, dtype=tf.dtypes.float32)
            k_batch = K.random_uniform((batch_size, k_bits), minval=-1, maxval=1, dtype=tf.dtypes.float32)
            latest_abe_loss = abe_model.train_on_batch([m_batch, k_batch, k_batch], None)

            # Train the EVE network
            alice_model.trainable = False
            for _ in range(2):
                m_batch = K.random_uniform((batch_size, k_bits), minval=-1, maxval=1, dtype=tf.dtypes.float32)
                k_batch = K.random_uniform((batch_size, k_bits), minval=-1, maxval=1, dtype=tf.dtypes.float32)
                latest_eve_loss = eve_model.train_on_batch([m_batch, k_batch], None)

            print(f"Step {step}: ABE:{latest_abe_loss} vs EVE:{latest_eve_loss}")
    except KeyboardInterrupt:
        alice_model.save(f"alice-{bits}.h5")
        alice_model.save_weights(f"alice-{bits}-weights.h5")
        bob_model.save(f"bob-{bits}.h5")
        bob_model.save_weights(f"bob-{bits}-weights.h5")
        eve_model.save(f"eve-{bits}.h5")
        eve_model.save_weights(f"eve-{bits}-weights.h5")

if __name__ == '__main__':
    if sys.argv[1] == 'train':
        do_train()
    if sys.argv[1] == 'encrypt':
        encrypt_file(sys.argv[2], sys.argv[3], sys.argv[4].encode('latin1'))
    if sys.argv[1] == 'decrypt':
        decrypt_file(sys.argv[2], sys.argv[3], sys.argv[4].encode('latin1'))
