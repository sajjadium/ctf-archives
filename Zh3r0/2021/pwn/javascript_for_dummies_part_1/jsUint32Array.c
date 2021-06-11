#include "jsi.h"
#include "jsvalue.h"
#include "jsbuiltin.h"

void js_newUint32Array(js_State *J) 
{
    int top = js_gettop(J);
    size_t size;
    if(top != 2) {
        js_typeerror(J, "Expecting Size");    
    }
    if(js_isobject(J, 1)) {
        js_Object* j = js_toobject(J, 1);
        if(j->type != JS_CARRAYBUFFER) {
            js_typeerror(J, "Require ArrayBuffer as Object");
        } else {
            js_Object* this = jsV_newobject(J, JS_CUINT32ARRAY, J->Uint32Array_prototype);
            this->u.ta.mem = j->u.ab.backingStore;
            this->u.ta.length = j->u.ab.byteLength / sizeof(uint32_t);
            js_pushobject(J,this);
        }
    } else {
        size = js_tonumber(J, 1);
        if(size < 0) {
            js_typeerror(J, "Invalid Length");
        }
        js_Object *this = jsV_newobject(J, JS_CUINT32ARRAY, J->Uint32Array_prototype);
        this->u.ta.mem = js_malloc(J, (size * sizeof(uint32_t)) );
        memset((void*)this->u.ta.mem,0,size);
        this->u.ta.length = size;
        this->u.ta.type = JS_CUINT32ARRAY; 
        js_pushobject(J, this);
    }
}

void js_Uint32ArrayFill(js_State *J)
{
    js_Object* this = js_toobject(J, 0);
    uint32_t fillNumber = js_tonumber(J, 1);
    if(this->type != JS_CUINT32ARRAY) {
        js_typeerror(J,"not an Uint32Array");
    }
    uint32_t* memref = (uint32_t*)this->u.ta.mem;
    for(int i = 0; i < this->u.ta.length; i++) {
        memref[i] = fillNumber;
    }
}

void js_Uint32ArraySet(js_State *J) 
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT32ARRAY) {
        js_typeerror(J,"not an Uint32Array");
    }
    uint32_t index = js_tonumber(J, 1);
    uint32_t value = js_tonumber(J, 2);
    if(index >= this->u.ta.length) {
        js_error(J,"Invalid Index");
    }
    uint32_t* memref = (uint32_t*)this->u.ta.mem;
    memref[index] = value;
}

void js_Uint32ArrayIncludes(js_State *J)
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT32ARRAY) {
        js_typeerror(J,"not an Uint32Array");
    }
    uint32_t f = js_tonumber(J, 1);
    uint32_t* memref = (uint32_t*)this->u.ta.mem;
    for(uint32_t i = 0; i < this->u.ta.length; i++) {
        if(memref[i] == f) {
            js_pushnumber(J,i);
            return;
        }
    }
    js_pushundefined(J);
}

void jsB_initUint32Array(js_State *J) {
    js_pushobject(J, J->Uint32Array_prototype);
    {
        jsB_propf(J, "Uint32Array.prototype.fill",js_Uint32ArrayFill, 1);
        jsB_propf(J, "Uint32Array.prototype.set", js_Uint32ArraySet, 3);
        jsB_propf(J, "Uint32Array.prototype.Includes",js_Uint32ArrayIncludes,1);
    }
    js_newcconstructor(J, js_newUint32Array, js_newUint32Array, "Uint32Array", 0);
    js_defglobal(J, "Uint32Array",JS_DONTENUM);
}