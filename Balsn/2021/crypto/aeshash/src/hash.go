package main

import "unsafe"

//go:linkname memhash runtime.memhash
func memhash(p unsafe.Pointer, h, s uintptr) uintptr

//go:linkname useAeshash runtime.useAeshash
var useAeshash bool

//go:linkname aeskeysched runtime.aeskeysched
var aeskeysched [512]byte

type stringStruct struct {
	str unsafe.Pointer
	len int
}

func MemHash(data []byte) uint64 {
	ss := (*stringStruct)(unsafe.Pointer(&data))
	return uint64(memhash(ss.str, 0xdeadbeef, uintptr(ss.len)))
}
