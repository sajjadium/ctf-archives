package main

import (
	"github.com/QingdaoU/JudgeServer/client/go"
	"fmt"
)

var (
	cSrc = `
#include <stdio.h>
int main(){
	int a, b;
	scanf("%d%d", &a, &b);
	printf("%d\n", a+b);
	return 0;
}
`
	cSPJSrc = `
#include <stdio.h>
int main(){
	return 1;
}
`
	cppSrc = `
#include <iostream>

using namespace std;

int main()
{
	int a,b;
	cin >> a >> b;
	cout << a+b << endl;
	return 0;
}
`
	javaSrc = `
import java.util.Scanner;
public class Main{
	public static void main(String[] args){
		Scanner in=new Scanner(System.in);
		int a=in.nextInt();
		int b=in.nextInt();
		System.out.println(a + b);
	}
}
`
	py2Src = `
s = raw_input()
s1 = s.split(" ")
print int(s1[0]) + int(s1[1])
`
	py3Src = `
s = input()
s1 = s.split(" ")
print(int(s1[0]) + int(s1[1]))
`
)

func main() {
	// 创建一个client。 这句代码等价于

	// 1.
	//client := judge.NewClient(
	//	judge.WithEndpointURL("http://127.0.0.1:12358"),
	//	judge.WithToken("YOUR_TOKEN_HERE"),
	//	judge.WithTimeout(0),
	//)

	// 2.
	// client := judge.New("http://127.0.0.1:12358", "YOUR_TOKEN_HERE", 0)

	// 3.
	client := judge.NewClient(judge.WithTimeout(0))
	client.SetOptions(judge.WithEndpointURL("http://127.0.0.1:12358"), judge.WithToken("YOUR_TOKEN_HERE"))

	fmt.Println("ping:")
	resp, err := client.Ping()
	if err != nil {
		// 这个 err 是发生在 client 这边的错误。 例如json编码失败
		fmt.Printf("ping client error. error is: %v.\n", err)
	} else if resp.Err() != nil {
		// 这个 resp.Err() 是 JudgeServer 响应的错误。 例如token错误 TokenVerificationFailed
		fmt.Printf("ping server error. error is: %v.\n", resp.Err().Error())
	} else {
		fmt.Println(resp.Data())
	}
	fmt.Println()

	fmt.Println("cpp_judge")
	resp, _ = client.JudgeWithRequest(&judge.JudgeRequest{
		Src:            cppSrc,
		LanguageConfig: judge.CPPLangConfig,
		MaxCpuTime:     1000,
		MaxMemory:      128 * 1024 * 1024,
		TestCaseId:     "normal",
	})
	printSliceData(resp.SliceData())
	fmt.Println()

	fmt.Println("java_judge")
	resp, _ = client.JudgeWithRequest(&judge.JudgeRequest{
		Src:            javaSrc,
		LanguageConfig: judge.JavaLangConfig,
		MaxCpuTime:     1000,
		MaxMemory:      256 * 1024 * 1024,
		TestCaseId:     "normal",
	})
	printSliceData(resp.SliceData())
	fmt.Println()

	fmt.Println("c_spj_judge")
	resp, _ = client.JudgeWithRequest(&judge.JudgeRequest{
		Src:              cSrc,
		LanguageConfig:   judge.CLangConfig,
		MaxCpuTime:       1000,
		MaxMemory:        128 * 1024 * 1024,
		TestCaseId:       "spj",
		SPJVersion:       "3",
		SPJConfig:        judge.CLangSPJConfig,
		SPJCompileConfig: judge.CLangSPJCompile,
		SPJSrc:           cSPJSrc,
	})
	printSliceData(resp.SliceData())
	fmt.Println()

	fmt.Println("py2_judge")
	resp, _ = client.JudgeWithRequest(&judge.JudgeRequest{
		Src:            py2Src,
		LanguageConfig: judge.PY2LangConfig,
		MaxCpuTime:     1000,
		MaxMemory:      128 * 1024 * 1024,
		TestCaseId:     "normal",
	})
	printSliceData(resp.SliceData())
	fmt.Println()

	fmt.Println("py3_judge")
	resp, _ = client.JudgeWithRequest(&judge.JudgeRequest{
		Src:            py3Src,
		LanguageConfig: judge.PY3LangConfig,
		MaxCpuTime:     1000,
		MaxMemory:      128 * 1024 * 1024,
		TestCaseId:     "normal",
	})
	printSliceData(resp.SliceData())
	fmt.Println()

	// CompileError example
	fmt.Println("CompileError example")
	resp, err = client.JudgeWithRequest(&judge.JudgeRequest{
		Src:            "this bad code",
		LanguageConfig: judge.JavaLangConfig,
		MaxCpuTime:     1000,
		MaxMemory:      256 * 1024 * 1024,
		TestCaseId:     "normal",
	})
	// fmt.Println(resp.RespErr) // "CompileError"
	fmt.Println(resp.StringData()) // 错误信息
}

func printSliceData(slice []*judge.Data) {
	fmt.Print("[\n")
	for _, item := range slice {
		fmt.Printf("\t%#v,\n", item)
	}
	fmt.Print("]\n")
}
