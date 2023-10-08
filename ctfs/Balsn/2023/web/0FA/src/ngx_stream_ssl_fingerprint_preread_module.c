#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_stream.h>
#include <ngx_md5.h>

static ngx_int_t ngx_stream_ssl_fingerprint_preread_init(ngx_conf_t *cf);

static ngx_stream_module_t  ngx_stream_ssl_fingerprint_preread_module_ctx = {
    NULL,                                     /* preconfiguration */
    ngx_stream_ssl_fingerprint_preread_init,          /* postconfiguration */
    NULL,                                     /* create main configuration */
    NULL,                                     /* init main configuration */
    NULL,                                     /* create server configuration */
    NULL                                      /* merge server configuration */
};


ngx_module_t  ngx_stream_ssl_fingerprint_preread_module = {
    NGX_MODULE_V1,
    &ngx_stream_ssl_fingerprint_preread_module_ctx,      /* module context */
    NULL,                                        /* module directives */
    NGX_STREAM_MODULE,                           /* module type */
    NULL,                                        /* init master */
    NULL,                                        /* init module */
    NULL,                                        /* init process */
    NULL,                                        /* init thread */
    NULL,                                        /* exit thread */
    NULL,                                        /* exit process */
    NULL,                                        /* exit master */
    NGX_MODULE_V1_PADDING
};


static ngx_int_t
ngx_stream_ssl_fingerprint_preread_init(ngx_conf_t *cf)
{
    return NGX_OK;
}
