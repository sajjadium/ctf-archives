package judge

import (
	"testing"
)

var client *Client

func TestMain(m *testing.M) {
	// 创建一个client。 这句代码等价于  New("http://127.0.0.1:12358", "YOUR_TOKEN_HERE", 0)
	client = NewClient(
		WithEndpointURL("http://127.0.0.1:12358"),
		WithToken("YOUR_TOKEN_HERE"),
		WithTimeout(0),
	)
	m.Run()
}

func TestClient_Ping(t *testing.T) {
	resp, err := client.Ping()
	if err != nil {
		t.Errorf("unexpected error. error: %+v", err)
		return
	}
	if resp.Err() != nil {
		t.Errorf("unexpected error. error: %+v", resp.Err())
		return
	}

	if resp.RespData == nil {
		t.Error("resp.RespData unexpected nil")
		return
	}
}

func TestClient_CompileSpj(t *testing.T) {
	cSpjSrc := `
#include <stdio.h>
int main(){
    return 1;
}
`
	resp, err := client.CompileSpj(cSpjSrc, "2", CLangSPJCompile)
	if err != nil {
		t.Errorf("unexpected error. error: %+v", err)
		return
	}
	if resp.Err() != nil {
		t.Errorf("unexpected error. error: %+v", resp.Err())
		return
	}
	if resp.RespData == nil {
		t.Error("resp.RespData unexpected nil")
		return
	}
}
