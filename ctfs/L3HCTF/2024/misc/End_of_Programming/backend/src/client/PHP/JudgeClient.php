<?php

class JudgeClient
{

    private $ch = null;
    private $serverBaseUrl = '';
    private $token;
    private static $languageConfigs = [];

    public function __construct($token, $serverBaseUrl)
    {
        $this->serverBaseUrl = rtrim($serverBaseUrl, '/');
        $this->token = hash('sha256', $token);
    }

    public function ping()
    {
        return $this->post($this->serverBaseUrl . '/ping');
    }

    /**
     * 调用判题 api
     * @param string $src 提交的源代码
     * @param string $language 使用的编程语言
     * @param string $testCaseId test_case_id
     * @param array $config 额外配置
     * @return array
     * @throws Exception
     */
    public function judge($src, $language, $testCaseId, $config = [])
    {
        $languageConfig = static::getLanguageConfigByLanguage($language);

        if (is_null($languageConfig)) {
            throw new Exception("don't support \"$language\" language!");
        }

        $default = [
            'language_config' => $languageConfig,
            'src' => $src,
            'test_case_id' => $testCaseId,
            'max_cpu_time' => $languageConfig['compile']['max_cpu_time'],
            'max_memory' => $languageConfig['compile']['max_memory'],
            'spj_version' => null,
            'spj_config' => null,
            'spj_compile_config' => null,
            'spj_src' => null,
            'output' => false
        ];
        return $this->post($this->serverBaseUrl . '/judge', array_merge($default, $config));
    }

    public function compileSpj($src, $spjVersion, $spjCompileConfig)
    {
        $data = [
            'src' => $src,
            'spj_version' => $spjVersion,
            'spj_compile_config' => $spjCompileConfig,
        ];
        return $this->post($this->serverBaseUrl . '/compile_spj', $data);
    }

    public static function loadLanguageConfigs()
    {
        if (empty(static::$languageConfigs))
            static::$languageConfigs = require('languages.php');
    }

    public static function getLanguageConfigByLanguage($language)
    {
        return static::getLanguageConfigByKey($language . '_lang_config');
    }

    public static function getLanguageConfigByKey($key)
    {
        return isset(static::$languageConfigs[$key]) ? static::$languageConfigs[$key] : null;
    }

    private function needCreateCurl()
    {
        return is_null($this->ch);
    }

    /**
     * 获取 curl 资源
     * @return null|resource
     */
    private function getCurl()
    {
        if ($this->needCreateCurl()) {
            $this->ch = curl_init();
            $defaults = [
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_HEADER => false,
                // set HTTP request header
                CURLOPT_HTTPHEADER => [
                    'Content-type: application/json',
                    'X-Judge-Server-Token: ' . $this->token
                ],
            ];
            curl_setopt_array($this->ch, $defaults);
        }

        return $this->ch;
    }

    /**
     * 发送 GET 请求
     * @param string $url 请求的url
     * @param array $data 请求参数
     * @return array
     */
    private function get($url, $data = [])
    {
        return $this->request('GET', $url, $data);
    }

    /**
     * 发送 POST 请求
     * @param string $url 请求的url
     * @param array $data 请求参数
     * @return array
     */
    private function post($url, $data = [])
    {
        return $this->request('POST', $url, $data);
    }

    /**
     * 发送 http 请求
     * @param string $method http method
     * @param string $url 请求的url
     * @param array $data 请求参数
     * @return array
     */
    private function request($method, $url, $data = [])
    {
        $ch = $this->getCurl();
        $method = strtoupper($method);
        if (in_array($method, ['GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH']))
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POSTFIELDS, empty($data) ? '{}' : json_encode($data));
        if (!$result = curl_exec($this->ch)) {
            trigger_error(curl_error($this->ch));
        }
        return json_decode($result, true);
    }


    /**
     * 关闭 curl 资源
     */
    public function close()
    {
        if (is_resource($this->ch)) {
            curl_close($this->ch);
        }
        $this->ch = null;
    }

    public function __destruct()
    {
        $this->close();
    }
}

JudgeClient::loadLanguageConfigs();