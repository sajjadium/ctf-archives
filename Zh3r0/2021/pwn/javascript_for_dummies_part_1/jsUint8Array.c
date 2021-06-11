#include "jsi.h"
#include "jsvalue.h"
#include "jsbuiltin.h"

void js_newUint8Array(js_State *J) 
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
            js_Object* this = jsV_newobject(J, JS_CUINT8ARRAY, J->Uint8Array_prototype);
            this->u.ta.mem = j->u.ab.backingStore;
            this->u.ta.length = j->u.ab.byteLength;
            js_pushobject(J,this);
            return ;
        }
    } else {
        size = js_tonumber(J, 1);
        if(size <= 0 && size > UINT32_MAX) {
            js_typeerror(J, "Invalid Length");
        }
        js_Object *this = jsV_newobject(J, JS_CUINT8ARRAY, J->Uint8Array_prototype);
        this->u.ta.mem = js_malloc(J, size);
        memset((void*)this->u.ta.mem,0,size);
        this->u.ta.length = size;
        js_pushobject(J, this);
    }
}


void js_Uint8ArrayFill(js_State *J)
{
    js_Object* this = js_toobject(J, 0);
    uint8_t fillNumber = js_tonumber(J, 1);
    if(this->type != JS_CUINT8ARRAY) {
        js_typeerror(J,"not an Uint8Array");
    }
    uint8_t* memref = (uint8_t*)this->u.ta.mem;
    for(int i = 0; i < this->u.ta.length; i++) {
        memref[i] = fillNumber;
    }
}

void js_Uint8ArraySet(js_State *J) 
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT8ARRAY) {
        js_typeerror(J,"not an Uint8Array");
    }
    uint32_t index = js_tonumber(J, 1);
    uint8_t value = js_tonumber(J, 2);
    if(index >= this->u.ta.length) {
        js_error(J,"Invalid Index");
    }
    uint8_t* memref = (uint8_t*)this->u.ta.mem;
    memref[index] = value;
}

void js_Uint8ArrayIncludes(js_State *J)
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT8ARRAY) {
        js_typeerror(J,"not an Uint8Array");
    }
    uint8_t f = js_tonumber(J, 1);
    uint8_t* memref = (uint8_t*)this->u.ta.mem;
    for(uint32_t i = 0; i < this->u.ta.length; i++) {
        if(memref[i] == f) {
            js_pushnumber(J,i);
            return;
        }
    }
    js_pushundefined(J);
}

void jsB_initUint8Array(js_State *J) {
    js_pushobject(J, J->Uint8Array_prototype);
    {        
        jsB_propf(J, "Uint8Array.prototype.fill",js_Uint8ArrayFill, 1);
        jsB_propf(J, "Uint8Array.prototype.set", js_Uint8ArraySet, 3);
        jsB_propf(J, "Uint8Array.prototype.Includes",js_Uint8ArrayIncludes,1);
    }
    js_newcconstructor(J, js_newUint8Array, js_newUint8Array, "Uint8Array", 0);
    js_defglobal(J, "Uint8Array",JS_DONTENUM);
}