#include <string>
#include <napi.h>
#include "encoder.h"

Napi::String hex_to_base64(const Napi::CallbackInfo& args)
{
    Napi::Env env = args.Env();
    if (args.Length() != 1) {
        Napi::TypeError::New(env, "Wrong number of arguments.").ThrowAsJavaScriptException();
        return Napi::String::New(env, "");
    }
    if (!args[0].IsString()) {
        Napi::TypeError::New(env, "Wrong argument types.").ThrowAsJavaScriptException();
        return Napi::String::New(env, "");
    }

    std::string str = args[0].As<Napi::String>();
    if (str.size() >= 1000) {
        Napi::TypeError::New(env, "Length must be less than 1000 characters.").ThrowAsJavaScriptException();
        return Napi::String::New(env, "");
    }

    return Napi::String::New(env, hex_to_base64_impl(str));
}

Napi::String base64_to_hex(const Napi::CallbackInfo& args)
{
    Napi::Env env = args.Env();
    if (args.Length() != 1) {
        Napi::TypeError::New(env, "Wrong number of arguments.").ThrowAsJavaScriptException();
        return Napi::String::New(env, "");
    }
    if (!args[0].IsString()) {
        Napi::TypeError::New(env, "Wrong argument types.").ThrowAsJavaScriptException();
        return Napi::String::New(env, "");
    }

    std::string str = args[0].As<Napi::String>();
    if (str.size() >= 1000) {
        Napi::TypeError::New(env, "Length must be less than 1000 characters.").ThrowAsJavaScriptException();
        return Napi::String::New(env, "");
    }

    return Napi::String::New(env, base64_to_hex_impl(str));
}

Napi::Object Init(Napi::Env env, Napi::Object exports)
{
    exports.Set(
        Napi::String::New(env, "hex_to_base64"),
        Napi::Function::New(env, hex_to_base64)
    );
    exports.Set(
        Napi::String::New(env, "base64_to_hex"),
        Napi::Function::New(env, base64_to_hex)
    );
    return exports;
}

NODE_API_MODULE(fast_convert, Init);
