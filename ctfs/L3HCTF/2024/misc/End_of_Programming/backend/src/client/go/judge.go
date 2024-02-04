package judge

import (
	"time"
	"bytes"
	"encoding/json"
)

type JudgeRequest struct {
	Src              string         `json:"src"`
	LanguageConfig   *LangConfig    `json:"language_config"`
	MaxCpuTime       int64          `json:"max_cpu_time"`
	MaxMemory        int64          `json:"max_memory"`
	TestCaseId       string         `json:"test_case_id"`
	SPJVersion       string         `json:"spj_version"`
	SPJConfig        *SPJConfig     `json:"spj_config"`
	SPJCompileConfig *CompileConfig `json:"spj_compile_config"`
	SPJSrc           string         `json:"spj_src"`
	Output           bool           `json:"output"`
}

// 这个方法为了模仿 php 和 python client 不推荐使用
func (c *Client) Judge(src string, languageConfig *LangConfig, maxCpuTime time.Duration, maxMemory int64, testCaseId,
spjVersion string, spjConfig *SPJConfig, spjCompileConfig *CompileConfig, spjSrc string, output bool) (resp *Resp, err error) {
	return c.JudgeWithRequest(&JudgeRequest{
		Src:              src,
		LanguageConfig:   languageConfig,
		MaxCpuTime:       int64(maxCpuTime),
		MaxMemory:        maxMemory,
		TestCaseId:       testCaseId,
		SPJVersion:       spjVersion,
		SPJConfig:        spjConfig,
		SPJCompileConfig: spjCompileConfig,
		SPJSrc:           spjSrc,
		Output:           output,
	})
}

func (c *Client) JudgeWithRequest(req *JudgeRequest) (resp *Resp, err error) {
	b, err := json.Marshal(req)
	if err != nil {
		return
	}
	resp, err = c.post("judge", bytes.NewReader(b))
	return
}
