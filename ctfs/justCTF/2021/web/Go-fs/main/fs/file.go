package fs

import (
	"fmt"
	"io"
	"os"
)

// implements http.File for a file
type File struct {
	fs *FileServFS
	name string
	offset *int
}

func (f File) Close() error {
	fmt.Printf("File.Close(file=`%s`)\n", f.name)
	return nil
}

func (f File) Read(p []byte) (n int, err error) {
	off := f.fs.files[f.name].offset + *f.offset
	fsize := int(f.fs.files[f.name].info.Size())
	//fsize := f.fs.files[f.name].encodedSize
	n = min(len(p), fsize)
	fmt.Printf("File.Read(file=%s@[%d-%d), len(p)=%d): off=%d, n=%d\n", f.name,
		f.fs.files[f.name].offset, f.fs.files[f.name].offset+fsize, len(p), off, n)
	src := f.fs.data[off:off+n]
	n = copy(p, src)
	*f.offset += n

	if *f.offset >= fsize {
		return n, io.EOF
	}

	return n, nil
}


func (f File) WriteTo(w io.Writer) (n int64, err error) {
	trace2()
	return 0, nil
}

func (f *FileServFS) WriteTo(w io.Writer) (n int64, err error) {
	trace2()
	return 0, nil

}

func (f File) Seek(offset int64, whence int) (int64, error) {
	fmt.Printf("File.Seek(file=`%s`, offset=%d, whence=%d)\n", f.name, offset, whence)

	if whence == io.SeekStart {
		*f.offset = int(offset)
	} else if whence == io.SeekEnd {
		*f.offset = int(f.fs.files[f.name].info.Size() - offset)
	} else if whence == io.SeekCurrent {
		*f.offset += int(offset)
	}
	return int64(*f.offset), nil
}

func (f File) Readdir(count int) ([]os.FileInfo, error) {
	trace2()
	return nil, NotImplementedError
}

func (f File) Stat() (os.FileInfo, error) {
	fmt.Printf("File.Stat(file=`%s`)\n", f.name)
	return f.fs.files[f.name].info, nil
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}