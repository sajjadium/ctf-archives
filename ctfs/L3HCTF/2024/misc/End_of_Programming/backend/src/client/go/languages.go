package judge

type CompileConfig struct {
	SrcName        string `json:"src_name"`
	ExeName        string `json:"exe_name"`
	MaxCpuTime     int64  `json:"max_cpu_time"`
	MaxRealTime    int64  `json:"max_real_time"`
	MaxMemory      int64  `json:"max_memory"`
	CompileCommand string `json:"compile_command"`
}

var DefaultEnv = []string{"LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"}

type RunConfig struct {
	Command              string   `json:"command"`
	SeccompRule          string   `json:"seccomp_rule"`
	Env                  []string `json:"env"`
	MemoryLimitCheckOnly int      `json:"memory_limit_check_only"`
}

type LangConfig struct {
	CompileConfig CompileConfig `json:"compile"`
	RunConfig     RunConfig     `json:"run"`
}

type SPJConfig struct {
	ExeName     string `json:"exe_name"`
	Command     string `json:"command"`
	SeccompRule string `json:"seccomp_rule"`
}

var CLangConfig = &LangConfig{
	CompileConfig: CompileConfig{
		SrcName:        "main.c",
		ExeName:        "main",
		MaxCpuTime:     3000,
		MaxRealTime:    5000,
		MaxMemory:      128 * 1024 * 1024,
		CompileCommand: "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c99 {src_path} -lm -o {exe_path}",
	},
	RunConfig: RunConfig{
		Command:     "{exe_path}",
		SeccompRule: "c_cpp",
		Env:         DefaultEnv,
	},
}

var CLangSPJCompile = &CompileConfig{
	SrcName:        "spj-{spj_version}.c",
	ExeName:        "spj-{spj_version}",
	MaxCpuTime:     3000,
	MaxRealTime:    5000,
	MaxMemory:      1024 * 1024 * 1024,
	CompileCommand: "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c99 {src_path} -lm -o {exe_path}",
}

var CLangSPJConfig = &SPJConfig{
	ExeName:     "spj-{spj_version}",
	Command:     "{exe_path} {in_file_path} {user_out_file_path}",
	SeccompRule: "c_cpp",
}

var CPPLangConfig = &LangConfig{
	CompileConfig: CompileConfig{
		SrcName:        "main.cpp",
		ExeName:        "main",
		MaxCpuTime:     3000,
		MaxRealTime:    5000,
		MaxMemory:      128 * 1024 * 1024,
		CompileCommand: "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++11 {src_path} -lm -o {exe_path}",
	},
	RunConfig: RunConfig{
		Command:     "{exe_path}",
		SeccompRule: "c_cpp",
		Env:         DefaultEnv,
	},
}

var JavaLangConfig = &LangConfig{
	CompileConfig: CompileConfig{
		SrcName:        "Main.java",
		ExeName:        "Main",
		MaxCpuTime:     3000,
		MaxRealTime:    5000,
		MaxMemory:      -1,
		CompileCommand: "/usr/bin/javac {src_path} -d {exe_dir} -encoding UTF8",
	},
	RunConfig: RunConfig{
		Command:              "/usr/bin/java -cp {exe_dir} -XX:MaxRAM={max_memory}k -Djava.security.manager -Dfile.encoding=UTF-8 -Djava.security.policy==/etc/java_policy -Djava.awt.headless=true Main",
		SeccompRule:          "",
		Env:                  DefaultEnv,
		MemoryLimitCheckOnly: 1,
	},
}

var PY2LangConfig = &LangConfig{
	CompileConfig: CompileConfig{
		SrcName:        "solution.py",
		ExeName:        "solution.pyc",
		MaxCpuTime:     3000,
		MaxRealTime:    5000,
		MaxMemory:      128 * 1024 * 1024,
		CompileCommand: "/usr/bin/python -m py_compile {src_path}",
	},
	RunConfig: RunConfig{
		Command:     "/usr/bin/python {exe_path}",
		SeccompRule: "general",
		Env:         DefaultEnv,
	},
}

var PY3LangConfig = &LangConfig{
	CompileConfig: CompileConfig{
		SrcName:        "solution.py",
		ExeName:        "__pycache__/solution.cpython-35.pyc",
		MaxCpuTime:     3000,
		MaxRealTime:    5000,
		MaxMemory:      128 * 1024 * 1024,
		CompileCommand: "/usr/bin/python3 -m py_compile {src_path}",
	},
	RunConfig: RunConfig{
		Command:     "/usr/bin/python3 {exe_path}",
		SeccompRule: "general",
		Env:         append(DefaultEnv, "PYTHONIOENCODING=UTF-8"),
	},
}
