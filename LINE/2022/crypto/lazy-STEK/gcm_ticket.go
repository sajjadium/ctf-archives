//This patch is provided under the 3-Clause BSD License, the original license of Golang.

/*
Copyright (c) 2009 The Go Authors. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

   * Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
   * Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution.
   * Neither the name of Google Inc. nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

// This code was created based on src/crypto/tls/ticket.go (L131-L200) in Go1.7.1.
// original: https://github.com/golang/go/blob/go1.7.1/src/crypto/tls/ticket.go#L132-L200
// If you want to experiment with this patch, please use a virtual environment that you can throw away, such as Docker.
// e.g. https://hub.docker.com/layers/golang/library/golang/1.17.1/images/sha256-8f4773d3be4e83da2198ae437191f8d9dffb30507714f0b727d0daf222377886

const FLAG string = "LINECTF{...}"

func (c *Conn) encryptTicket(state []byte) ([]byte, error) {
	fmt.Println("called custom encryptTicket function!")
	if len(c.ticketKeys) == 0 {
		return nil, errors.New("tls: internal error: session ticket keys unavailable")
	}

	// write FLAG in certicicate
	new_state := make([]byte, len(state)+len([]byte(FLAG)))
	sessionState := new(sessionStateTLS13)
	if ok := sessionState.unmarshal(state); !ok {
		return nil, errors.New("tls: failed to unmarshal ticket data")
	}
	sessionState.certificate.Certificate = append(sessionState.certificate.Certificate, []byte(FLAG))
	new_state = sessionState.marshal()

	// allocate memory
	encrypted := make([]byte, ticketKeyNameLen+aes.BlockSize+len(new_state)+sha256.Size)
	keyName := encrypted[:ticketKeyNameLen]
	iv := make([]byte, aes.BlockSize)

	// Select Session Ticket Encryption Key (STEK).
	// aesKey is generated with following formula
	// aesKey = SHA512(STEK)[16:32]
	// ref: https://github.com/golang/go/blob/go1.17.1/src/crypto/tls/common.go#L758-L764
	rand.Seed(time.Now().UnixNano())
	index := rand.Intn(2)
	key := c.ticketKeys[index]

	copy(keyName, key.keyName[:])
	block, err := aes.NewCipher(key.aesKey[:])
	if err != nil {
		return nil, errors.New("tls: failed to create cipher while encrypting ticket: " + err.Error())
	}

	// I'm lazy, so I generate IV from aesKey.
	h := sha256.New()
	h.Write(key.aesKey[:])
	iv = h.Sum(nil)[:16]
	if 0 == index {
		copy(iv[12:], []byte{0xaa, 0xaa, 0xaa, 0xaa})
	} else {
		copy(iv[12:], []byte{0xbb, 0xbb, 0xbb, 0xbb})
	}
	copy(encrypted[ticketKeyNameLen:ticketKeyNameLen+aes.BlockSize], iv[:16])

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, errors.New("tls: failed to create cipher while GCM session for encrypting ticket: " + err.Error())
	}

	// AES-128-GCM_ENC(nonce=iv[:12](12-octet), plaintext=raw_ticket, aad=keyName(16-octet)+iv(16-octet))
	ciphertext := aesgcm.Seal(nil, iv[:12], new_state, encrypted[:ticketKeyNameLen+aes.BlockSize])
	copy(encrypted[ticketKeyNameLen+aes.BlockSize:], ciphertext)
	return encrypted, nil
}

func (c *Conn) decryptTicket(encrypted []byte) (plaintext []byte, usedOldKey bool) {
	if len(encrypted) < ticketKeyNameLen+aes.BlockSize+sha256.Size {
		return nil, false
	}
	tagsize := 16
	keyName := encrypted[:ticketKeyNameLen]
	iv := encrypted[ticketKeyNameLen : ticketKeyNameLen+aes.BlockSize]
	ciphertext := encrypted[ticketKeyNameLen+aes.BlockSize : len(encrypted)-sha256.Size+tagsize]

	keyIndex := -1
	for i, candidateKey := range c.ticketKeys {
		if bytes.Equal(keyName, candidateKey.keyName[:]) {
			keyIndex = i
			break
		}
	}
	if keyIndex == -1 {
		return nil, false
	}
	key := &c.ticketKeys[keyIndex]

	block, err := aes.NewCipher(key.aesKey[:])
	if err != nil {
		return nil, false
	}

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, false
	}

	pt, err := aesgcm.Open(nil, iv[:12], ciphertext, encrypted[:ticketKeyNameLen+aes.BlockSize])
	if err != nil {
		return nil, false
	}

	return pt, keyIndex > 0
}
