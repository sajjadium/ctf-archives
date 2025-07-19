package main

import (
	"bytes"
	cryptoRand "crypto/rand"
	"encoding/hex"
	"flag"
	"fmt"
	"image"
	"image/color"
	"image/jpeg"
	"io"
	"log/slog"
	mathRand "math/rand/v2"
	"net"
	"os"

	"github.com/tinyrange/tinyrange/pkg/filesystem"
	"github.com/tinyrange/tinyrange/pkg/filesystem/ext4"
	"github.com/tinyrange/tinyrange/pkg/filesystem/fsutil"
	"github.com/tinyrange/tinyrange/pkg/filesystem/vm"
	"github.com/tinyrange/tinyrange/pkg/path"
	gonbd "github.com/tinyrange/tinyrange/third_party/go-nbd"
	"github.com/tinyrange/tinyrange/third_party/go-nbd/backend"

	"golang.org/x/image/font"
	"golang.org/x/image/font/basicfont"
	"golang.org/x/image/math/fixed"
)

// GenerateTextPNG creates a PNG image with the given text string.
// filename: the name of the output PNG file.
// text: the string to draw on the image.
// width: the width of the image.
// height: the height of the image.
func generateTextPNG(text string, width int, height int) ([]byte, error) {
	// Create a new blank image
	img := image.NewRGBA(image.Rect(0, 0, width, height))

	// Fill the background with white
	bgColor := color.RGBA{255, 255, 255, 255}
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			img.Set(x, y, bgColor)
		}
	}

	// Set up a basic font
	face := basicfont.Face7x13

	// Create a drawer
	drawer := &font.Drawer{
		Dst:  img,
		Src:  image.NewUniform(color.Black), // Text color
		Face: face,
	}

	// Calculate the text size to position it in the center (approximately)
	textBounds, _ := drawer.BoundString(text)
	textWidth := (textBounds.Max.X - textBounds.Min.X).Ceil()
	textHeight := (textBounds.Max.Y - textBounds.Min.Y).Ceil()

	// Position the text
	// We'll center it horizontally and vertically as best as we can
	x := (width - textWidth) / 2
	y := (height-textHeight)/2 + face.Metrics().Ascent.Ceil() // Adjust for baseline

	drawer.Dot = fixed.Point26_6{
		X: fixed.I(x),
		Y: fixed.I(y),
	}

	// Draw the text
	drawer.DrawString(text)

	// Create the output file
	buf := bytes.NewBuffer(nil)

	// Encode the image as JPEG
	if err := jpeg.Encode(buf, img, nil); err != nil {
		return nil, err
	}

	return buf.Bytes(), nil
}

func generateFilename(prefix string, length int, suffix string) string {
	return prefix + generateRandomText(length) + suffix
}

func generateRandomText(length int) string {
	b := make([]byte, length)
	if _, err := cryptoRand.Read(b); err != nil {
		panic(fmt.Sprintf("failed to generate random bytes: %v", err))
	}
	return hex.EncodeToString(b)
}

func generateImageFile(text string) (filesystem.MutableFile, error) {
	// Generate the PNG image with the given text
	imageData, err := generateTextPNG(text, 400, 30)
	if err != nil {
		return nil, fmt.Errorf("failed to generate PNG: %w", err)
	}

	// Create a new file with the generated image data
	file := filesystem.Factory.NewMemoryFile()
	if err := file.Overwrite(imageData); err != nil {
		return nil, fmt.Errorf("failed to overwrite file with image data: %w", err)
	}

	return file, nil
}

func generateFilesystem(flag string, levels int, dummyFilesPerDirectory int, dummyImagesPerDir int, spreadDirectoriesPerDirectory int) (filesystem.Directory, error) {
	var bottomDirs []struct {
		path string
		dir  filesystem.MutableDirectory
	}

	var generateFiles func(p string, levelsLeft int) (filesystem.MutableDirectory, error)

	generateFiles = func(p string, levelsLeft int) (filesystem.MutableDirectory, error) {
		newDir := filesystem.Factory.NewMemoryDirectory()

		// generate a series of dummy files
		for range dummyFilesPerDirectory {
			fileName := generateFilename("f", 4, ".txt")
			fileContent := generateRandomText(10)
			file, err := generateImageFile(fileContent)
			if err != nil {
				return nil, fmt.Errorf("failed to generate dummy file %s: %w", fileName, err)
			}
			if _, err := newDir.Create(fileName, file); err != nil {
				return nil, fmt.Errorf("failed to create dummy file %s: %w", fileName, err)
			}
		}

		// generate a series of dummy images
		for range dummyImagesPerDir {
			fileName := generateFilename("f", 4, ".jpg")
			file, err := generateImageFile(generateRandomText(10))
			if err != nil {
				return nil, fmt.Errorf("failed to generate dummy file %s: %w", fileName, err)
			}
			if _, err := newDir.Create(fileName, file); err != nil {
				return nil, fmt.Errorf("failed to create dummy file %s: %w", fileName, err)
			}
		}

		if levelsLeft == 0 {
			bottomDirs = append(bottomDirs, struct {
				path string
				dir  filesystem.MutableDirectory
			}{
				path: p,
				dir:  newDir,
			})

			return newDir, nil
		}

		// generate a series of subdirectories
		for range spreadDirectoriesPerDirectory {
			subDirName := generateFilename("d", 4, "")
			subDirPath := path.Unix.Join(p, subDirName)
			subDir, err := generateFiles(subDirPath, levelsLeft-1)
			if err != nil {
				return nil, fmt.Errorf("failed to generate subdirectory %s: %w", subDirPath, err)
			}
			if _, err := newDir.Create(subDirName, subDir); err != nil {
				return nil, fmt.Errorf("failed to create subdirectory %s: %w", subDirName, err)
			}
		}

		return newDir, nil
	}

	challengeDir, err := generateFiles(".", levels)
	if err != nil {
		return nil, fmt.Errorf("failed to generate filesystem: %w", err)
	}

	// pick a random bottom directory to place the flag
	if len(bottomDirs) == 0 {
		return nil, fmt.Errorf("no bottom directories available to place the flag")
	}
	randomIndex := mathRand.Int32N(int32(len(bottomDirs)))
	bottomDir := bottomDirs[randomIndex]
	flagFileName := generateFilename("f", 4, ".jpg")

	// generate the flag file
	flagFile, err := generateImageFile(flag)
	if err != nil {
		return nil, fmt.Errorf("failed to generate image file for flag: %w", err)
	}

	// add the flag file to the chosen bottom directory
	if _, err := bottomDir.dir.Create(flagFileName, flagFile); err != nil {
		return nil, fmt.Errorf("failed to add flag file to bottom directory: %w", err)
	}

	// make a symlink to the flag file in the challenge directory
	symlink := filesystem.Factory.NewSymlink(path.Unix.Join(bottomDir.path, flagFileName))
	if _, err := challengeDir.Create("flag.jpg", symlink); err != nil {
		return nil, fmt.Errorf("failed to create symlink to flag file: %w", err)
	}

	return challengeDir, nil
}

type BlockDevice interface {
	io.ReaderAt
	io.WriterAt
	Size() int64
}

func filesystemToExt4(fs filesystem.Directory) (BlockDevice, error) {
	// calculate the size of the filesystem
	totalSize, err := fsutil.GetTotalSize(fs)
	if err != nil {
		return nil, fmt.Errorf("failed to calculate total size of filesystem: %w", err)
	}

	// double the estimate and round up to the nearest 16MB
	totalSize = (totalSize*2 + 0xFFFFFF) &^ 0xFFFFFF

	// create the new virtual memory
	vmem := vm.NewVirtualMemory(totalSize, 4096)

	// format the new ext4 filesystem
	efs, err := ext4.CreateExt4Filesystem(vmem, 0, totalSize)
	if err != nil {
		return nil, fmt.Errorf("failed to create ext4 filesystem: %w", err)
	}

	// write the filesystem to the ext4 filesystem
	if err := efs.AddDirectory(nil, fs, nil, nil); err != nil {
		return nil, fmt.Errorf("failed to add directory to ext4 filesystem: %w", err)
	}

	return vmem, nil
}

type blockDeviceBackend struct {
	BlockDevice
}

// Size implements backend.Backend.
// Subtle: this method shadows the method (BlockDevice).Size of blockDeviceBackend.BlockDevice.
func (b *blockDeviceBackend) Size() (int64, error) {
	return b.BlockDevice.Size(), nil
}

// Sync implements backend.Backend.
func (b *blockDeviceBackend) Sync() error {
	return nil
}

var (
	_ backend.Backend = &blockDeviceBackend{}
)

type connWrap struct {
	net.Conn
}

// Override the Write method to enforce a write limit per client.
func (c *connWrap) Write(b []byte) (int, error) {
	n, err := c.Conn.Write(b)
	if err != nil {
		return n, err
	}

	return n, nil
}

func (c *connWrap) Close() error {
	slog.Info("closing connection", "remote", c.Conn.RemoteAddr())
	if c.Conn != nil {
		if err := c.Conn.Close(); err != nil {
			slog.Error("failed to close connection", "err", err)
			return err
		}
		c.Conn = nil
	}
	return nil
}

var (
	_ net.Conn = &connWrap{}
)

var (
	writeFile                     = flag.String("write-file", "", "Write the generated filesystem to a file instead of stdout")
	listenNbd                     = flag.String("listen-nbd", "", "Listen for NBD connections on this address (e.g., 0.0.0.0:5123)")
	levels                        = flag.Int("levels", 3, "Number of levels in the filesystem")
	dummyFilesPerDirectory        = flag.Int("dummy-files-per-directory", 8, "Number of dummy files per directory")
	dummyImagesPerDir             = flag.Int("dummy-images-per-dir", 1, "Number of dummy images per directory")
	spreadDirectoriesPerDirectory = flag.Int("spread-directories-per-directory", 3, "Number of directories to spread per directory")
)

func appMain() error {
	flag.Parse()

	ctfFlag := os.Getenv("FLAG")
	if ctfFlag == "" {
		ctfFlag = "FLAG{dummy}"
	}

	if *writeFile != "" {
		dir, err := generateFilesystem(
			ctfFlag,                        // the flag to be placed in the filesystem
			*levels,                        // number of levels in the filesystem
			*dummyFilesPerDirectory,        // number of dummy files per directory
			*dummyImagesPerDir,             // number of dummy images per directory
			*spreadDirectoriesPerDirectory, // number of directories to spread per directory
		)
		if err != nil {
			return fmt.Errorf("failed to generate filesystem: %w", err)
		}

		// convert the filesystem to an ext4 block device
		blockDevice, err := filesystemToExt4(dir)
		if err != nil {
			return fmt.Errorf("failed to convert filesystem to ext4 block device: %w", err)
		}

		// write the block device to a file
		f, err := os.Create(*writeFile)
		if err != nil {
			return fmt.Errorf("failed to create output file %s: %w", *writeFile, err)
		}
		defer f.Close()

		if _, err := io.Copy(f, io.NewSectionReader(blockDevice, 0, blockDevice.Size())); err != nil {
			return fmt.Errorf("failed to write block device to file %s: %w", *writeFile, err)
		}
	}

	if *listenNbd != "" {
		listen, err := net.Listen("tcp", *listenNbd)
		if err != nil {
			return fmt.Errorf("failed to listen on %s: %w", *listenNbd, err)
		}
		defer listen.Close()

		slog.Info("listening for NBD connections", "address", *listenNbd)

		for {
			conn, err := listen.Accept()
			if err != nil {
				slog.Error("failed to accept connection", "err", err)
				continue
			}

			go func(c net.Conn) {
				wrap := &connWrap{
					Conn: c,
				}
				defer wrap.Close()

				// generate the filesystem
				dir, err := generateFilesystem(
					ctfFlag,                        // the flag to be placed in the filesystem
					*levels,                        // number of levels in the filesystem
					*dummyFilesPerDirectory,        // number of dummy files per directory
					*dummyImagesPerDir,             // number of dummy images per directory
					*spreadDirectoriesPerDirectory, // number of directories to spread per directory
				)
				if err != nil {
					slog.Error("failed to generate filesystem", "err", err)
					return
				}

				// convert the filesystem to an ext4 block device
				blockDevice, err := filesystemToExt4(dir)
				if err != nil {
					slog.Error("failed to convert filesystem to ext4 block device", "err", err)
					return
				}

				slog.Info("handling NBD connection", "remote", c.RemoteAddr())

				if err := gonbd.Handle(wrap, []gonbd.Export{
					{
						Name:    "root",
						Backend: &blockDeviceBackend{BlockDevice: blockDevice},
					},
				}, &gonbd.Options{}); err != nil {
					slog.Error("failed to handle NBD connection", "remote", c.RemoteAddr(), "err", err)
					return
				}
			}(conn)
		}
	}

	return fmt.Errorf("no action specified, use -write-file or -listen-nbd")
}

func main() {
	if err := appMain(); err != nil {
		slog.Error("fatal", "err", err)
		os.Exit(1)
	}
}
