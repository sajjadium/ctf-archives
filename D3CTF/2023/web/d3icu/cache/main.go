package main

import (
	"fmt"
	"hash/crc32"
	"io"
	"io/fs"
	"net/http"
	"os"
	"time"

	"github.com/flamego/flamego"
	"github.com/go-redis/redis/v8"
	"org.d3ctf.app/static"
)

func crc32Hash(str string) string {
	return fmt.Sprint(crc32.ChecksumIEEE([]byte(str)))
}

func main() {

	f := flamego.Classic()
	f.Map(
		Cache{
			client: redis.NewClient(&redis.Options{
				Addr: os.ExpandEnv("127.0.0.1:6379"),
			}),
		},
	)
	staticFS, _ := fs.Sub(static.FS, "dist")
	f.Use(flamego.Static(flamego.StaticOptions{
		FileSystem: http.FS(staticFS),
	}))
	f.Get("/fetch", func(ctx flamego.Context, cache Cache, r *http.Request, rw http.ResponseWriter) {
		url := ctx.Query("url")
		cacheKey := crc32Hash(url)
		if buf, err := cache.Get(r.Context(), cacheKey); err == nil {
			ctx.ResponseWriter().Write(buf)
			return
		}
		resp, _ := http.Get(url)
		buf, _ := io.ReadAll(resp.Body)
		cache.Set(r.Context(), cacheKey, buf, time.Minute*10)
		rw.Write(buf)
	})
	f.Run()
}
