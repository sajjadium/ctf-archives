package judge

import (
	"net/http"
	"io/ioutil"
	"io"
	"encoding/json"
	"time"
	"bytes"
	"fmt"
)

// Data 成员的类型参考 https://github.com/QingdaoU/Judger/blob/b6414e7a6715eb013b1ffeb7cfb04626a3ff5b4e/src/runner.h#L73
type Data struct {
	CpuTime   int
	Result    int
	Memory    int64 // https://github.com/QingdaoU/Judger/blob/b6414e7a6715eb013b1ffeb7cfb04626a3ff5b4e/src/runner.h#L76
	RealTime  int
	Signal    int
	Error     int
	ExitCode  int
	OutputMd5 string
	Output    interface{}
	TestCase  string
}

type Resp struct {
	RespData interface{} `json:"data"`
	RespErr  string      `json:"err"`
	err      error       `json:"-"`
}

func (resp *Resp) Data() interface{} {
	if resp == nil {
		return nil
	}
	return resp.RespData
}

func (resp *Resp) StringData() string {
	if resp == nil {
		return ""
	}
	str, _ := resp.RespData.(string)
	return str
}

func (resp *Resp) SliceData() []*Data {
	if resp == nil {
		return nil
	}
	slice, _ := resp.RespData.([]interface{})
	data := make([]*Data, 0, len(slice))
	for _, s := range slice {
		item, ok := s.(map[string]interface{})
		if ok {
			cpuTimeF64, _ := item["cpu_time"].(float64)
			resultF64, _ := item["result"].(float64)
			memoryF64, _ := item["memory"].(float64)
			realTimeF64, _ := item["real_time"].(float64)
			signalF64, _ := item["signal"].(float64)
			errorF64, _ := item["error"].(float64)
			exitCodeF64, _ := item["exit_code"].(float64)
			outputMd5, _ := item["output_md5"].(string)
			testCase, _ := item["test_case"].(string)
			data = append(data, &Data{
				CpuTime:   int(cpuTimeF64),
				Result:    int(resultF64),
				Memory:    int64(memoryF64),
				RealTime:  int(realTimeF64),
				Signal:    int(signalF64),
				Error:     int(errorF64),
				ExitCode:  int(exitCodeF64),
				OutputMd5: outputMd5,
				Output:    item["output"],
				TestCase:  testCase,
			})
		}

	}
	return data
}

func (resp *Resp) Err() error {
	if resp == nil {
		return nil
	}
	return resp.err
}

func parseResp(body []byte) (*Resp, error) {
	resp := &Resp{}
	err := json.Unmarshal(body, resp)
	if err != nil {
		return nil, err
	}
	// 有错误的响应了
	if resp.RespErr != "" {
		resp.err = fmt.Errorf("err: %s, data: %s", resp.RespErr, resp.RespData)
	}

	return resp, nil
}

type Client struct {
	opts       *options
	httpClient *http.Client
}

func (c *Client) request(method, path string, body io.Reader) (resp *Resp, err error) {
	req, err := http.NewRequest("POST", c.opts.EndpointURL+"/"+path, body)
	if err != nil {
		return
	}
	req.Header.Set("X-Judge-Server-Token", c.opts.sha256Token)
	req.Header.Set("Content-Type", "application/json")

	httpResp, err := c.httpClient.Do(req)
	if err != nil {
		return
	}
	b, err := ioutil.ReadAll(httpResp.Body)
	if err != nil {
		return
	}
	httpResp.Body.Close()
	return parseResp(b)
}

func (c *Client) post(path string, body io.Reader) (resp *Resp, err error) {
	return c.request("POST", path, body)
}

// Ping Judge server
func (c *Client) Ping() (resp *Resp, err error) {
	resp, err = c.post("ping", nil)
	return
}

func (c *Client) CompileSpj(src, spjVersion string, spjCompileConfig *CompileConfig) (resp *Resp, err error) {
	data := map[string]interface{}{
		"src":                src,
		"spj_version":        spjVersion,
		"spj_compile_config": spjCompileConfig,
	}
	b, err := json.Marshal(data)
	if err != nil {
		return
	}
	resp, err = c.post("compile_spj", bytes.NewReader(b))
	return
}

func New(endpointURL, token string, timeout time.Duration) *Client {
	return NewClient(
		WithEndpointURL(endpointURL),
		WithToken(token),
		WithTimeout(timeout),
	)
}

func (c *Client) SetOptions(options ...Option) {
	originTimeout := c.opts.Timeout
	for _, o := range options {
		o(c.opts)
	}
	if c.opts.Timeout != originTimeout {
		c.httpClient.Timeout = c.opts.Timeout
	}
}

func NewClient(options ...Option) *Client {
	opts := DefaultOptions
	for _, o := range options {
		o(opts)
	}

	return &Client{
		opts: opts,
		httpClient: &http.Client{
			Timeout: opts.Timeout,
		},
	}
}
