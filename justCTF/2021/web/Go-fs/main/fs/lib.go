package fs

import (
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

var NotImplementedError = errors.New("feature not implemented")

// debug only
func trace2() {
	pc := make([]uintptr, 15)
	n := runtime.Callers(2, pc)
	frames := runtime.CallersFrames(pc[:n])
	frame, _ := frames.Next()
	fmt.Printf("%s:%d %s\n", frame.File, frame.Line, frame.Function)
}

type FileServFS struct {
	files map[string]struct {
		offset      int
		info        os.FileInfo
		encodedSize int
	}
	data []uint8
	root string
}

type FileInfo struct {
	info os.FileInfo
	encodedSize int64
}
func (fi FileInfo) Name() string       { return fi.info.Name() }
func (fi FileInfo) Mode() os.FileMode  { return fi.info.Mode() }
func (fi FileInfo) Size() int64        { return fi.encodedSize }
func (fi FileInfo) ModTime() time.Time { return fi.info.ModTime() }
func (fi FileInfo) IsDir() bool        { return fi.info.IsDir() }
func (fi FileInfo) Sys() interface{}   { return fi.info.Sys() }


func (fs *FileServFS) Open(name string) (http.File, error) {
	fmt.Printf("FileServFS.Open(name=`%s`)\n", name)
	if f, ok := fs.files[name]; ok {
		off := 0
		if !f.info.IsDir() {
			return File{fs, name, &off}, nil
		} else {
			return os.Open(fs.root + name)
		}
	}
	return nil, os.ErrNotExist
}

func newFileServFS(root string) *FileServFS {
	return &FileServFS{
		files: make(map[string]struct {
			offset      int
			info        os.FileInfo
			encodedSize int}),
		data: make([]byte, 0),
		root: root,
	}
}

func (fs *FileServFS) addFile(root, path string, info os.FileInfo, encoder func(data []byte) []byte) {
	content, err := ioutil.ReadFile(path)

	var data []byte
	if err != nil {
		//panic(fmt.Errorf("could not read file: %v", err))
		data = []byte(fmt.Sprintf("Could not read file %v: %v", path, err))
	} else {
		data = encoder(content)
	}

	urlpath := strings.TrimPrefix(path, root)
	if urlpath[0] != '/' {
		urlpath = "/" + urlpath
	}

	fileInfo := FileInfo{info, int64(len(data))}

	fmt.Printf("Add file url=`%s`\n", urlpath)
	fs.files[urlpath] = struct {
		offset      int
		info        os.FileInfo
		encodedSize int
	}{len(fs.data), fileInfo, len(data)}

	fs.data = append(fs.data, data...)
}

func (fs *FileServFS) addDir(root string, path string, info os.FileInfo /*, renderDir func(contents []os.FileInfo) []byte*/) {
	//contents, err := ioutil.ReadDir(path)
	//
	//var data []byte
	//if err != nil {
	//	data = []byte(fmt.Sprintf("could not read directory %v: %v", path, err))
	//} else {
	//	data = renderDir(contents)
	//}

	urlpath := strings.TrimPrefix(path, root)
	if len(urlpath) == 0 || urlpath[0] != '/' {
		urlpath = "/" + urlpath
	}

	//fileInfo := FileInfo{info, int64(len(data))}

	fmt.Printf("Add directory url=`%s` from root=`%s`\n", urlpath, root)
	fs.files[urlpath] = struct {
		offset      int
		info        os.FileInfo
		encodedSize int
	}{len(fs.data), info, -1}

	//fs.data = append(fs.data, data...)
}

func CreateFileServFS(root string, encoder func(data []byte) []byte, /*renderDir func(contents []os.FileInfo) []byte*/) *FileServFS {
	fs := newFileServFS(root)

	err := filepath.Walk(root,
		func(path string, info os.FileInfo, err error) error {
			fullPath := filepath.Join(root, path)
			fmt.Printf("walk at path=`%s`\n", fullPath)

			if !info.IsDir() {
				fs.addFile(root, path, info, encoder)
			} else {
				fs.addDir(root, path, info/*, renderDir*/)
			}
			if err != nil {
				return err
			}

			return nil
		})

	if err != nil {
		panic(fmt.Errorf("could not create fs: %v", err))
	}

	return fs
}