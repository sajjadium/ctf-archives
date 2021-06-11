#include "jsi.h"
#include "jsvalue.h"
#include "jsbuiltin.h"

void js_newUint16Array(js_State *J) 
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
            js_Object* this = jsV_newobject(J, JS_CUINT16ARRAY, J->Uint16Array_prototype);
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
        js_Object *this = jsV_newobject(J, JS_CUINT16ARRAY, J->Uint16Array_prototype);
        this->u.ta.mem = js_malloc(J, (size * sizeof(uint16_t)));
        memset((void*)this->u.ta.mem,0,size);
        this->u.ta.length = size;
        js_pushobject(J, this);
    }
}

void js_Uint16ArrayFill(js_State *J)
{
    js_Object* this = js_toobject(J, 0);
    uint16_t fillNumber = js_tonumber(J, 1);
    if(this->type != JS_CUINT16ARRAY) {
        js_typeerror(J,"not an Uint16Array");
    }
    uint16_t* memref = (uint16_t*)this->u.ta.mem;
    for(int i = 0; i < this->u.ta.length; i++) {
        memref[i] = fillNumber;
    }
}

void js_Uint16ArraySet(js_State *J) 
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT16ARRAY) {
        js_typeerror(J,"not an Uint8Array");
    }
    uint32_t index = js_tonumber(J, 1);
    uint16_t value = js_tonumber(J, 2);
    if(index >= this->u.ta.length) {
        js_error(J,"Invalid Index");
    }
    uint16_t* memref = (uint16_t*)this->u.ta.mem;
    memref[index] = value;
}

void js_Uint16ArrayIncludes(js_State *J)
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT16ARRAY) {
        js_typeerror(J,"not an Uint16Array");
    }
    uint16_t f = js_tonumber(J, 1);
    uint16_t* memref = (uint16_t*)this->u.ta.mem;
    for(uint32_t i = 0; i < this->u.ta.length; i++) {
        if(memref[i] == f) {
            js_pushnumber(J,i);
            return;
        }
    }
    js_pushundefined(J);
}

void jsB_initUint16Array(js_State *J) 
{
    js_pushobject(J, J->Uint16Array_prototype);
    {
        jsB_propf(J, "Uint16Array.prototype.fill",js_Uint16ArrayFill, 1);
        jsB_propf(J, "Uint16Array.prototype.set", js_Uint16ArraySet, 3);
        jsB_propf(J, "Uint16Array.prototype.Includes",js_Uint16ArrayIncludes,1);
    }
    js_newcconstructor(J, js_newUint16Array, js_newUint16Array, "Uint16Array", 0);
    js_defglobal(J, "Uint16Array",JS_DONTENUM);
}