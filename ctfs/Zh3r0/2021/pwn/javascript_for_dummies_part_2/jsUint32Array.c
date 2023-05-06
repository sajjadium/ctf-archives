#include "jsi.h"
#include "jsvalue.h"
#include "jsbuiltin.h"

/*
var a = new ArrayBuffer(100);
var b = new Uint32Array(a);

*/


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
            return;
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

void js_Uint32ArrayAt(js_State *J) 
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT32ARRAY) {
        js_typeerror(J, "not an Uint32Array");
    }
    uint32_t index = js_tonumber(J, 1);
    uint32_t* memref = (uint32_t*)this->u.ta.mem;
    if(index >= this->u.ta.length) {
        js_error(J, "Invalid Index");
    }
    js_pushnumber(J, memref[index]);
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

void js_Uint32ArrayFind(js_State *J)
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT32ARRAY) {
        js_typeerror(J,"not an Uint32Array");
    }
    uint32_t f = js_tonumber(J, 1);
    uint32_t* memref = (uint32_t*)this->u.ta.mem;
    uint32_t idx = 0;
    uint8_t found = 0;
    for(; idx < this->u.ta.length; idx++) {
        if(memref[idx] == f) {
            found = 1;
            break;
        }
    }
    if(found) {
        js_pushnumber(J, idx); 
    } else {
        js_pushundefined(J);
    }
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
            js_pushboolean(J,1);
            return;
        }
    }
    js_pushboolean(J,0);
}

void js_Uint32ArrayReverse(js_State *J)
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT32ARRAY) {
        js_typeerror(J,"not an Uint32Array");
    }
    uint32_t* memref = (uint32_t*)this->u.ta.mem;
    uint32_t tmp;
    uint32_t i = 0, j = this->u.ta.length-1;
    while(i < j) {
        tmp = memref[i];
        memref[i] = memref[j];
        memref[j] = tmp;
        i++;
        j--;
    }
}

void js_Uint32ArrayGet(js_State *J)
{
    js_Object* this = js_toobject(J, 0);
    if(this->type != JS_CUINT32ARRAY) {
        js_typeerror(J,"not an Uint32Array");
    }
    uint32_t index = js_touint32(J, 1);
    if(index >= this->u.ta.length) {
        js_error(J, "Invalid Index");
    }
    uint32_t* memref = (uint32_t*)this->u.ta.mem;
    js_pushnumber(J, memref[index]);
}

void jsB_initUint32Array(js_State *J) {
    js_pushobject(J, J->Uint32Array_prototype);
    {
        jsB_propf(J, "Uint32Array.prototype.fill",js_Uint32ArrayFill, 1);
        jsB_propf(J, "Uint32Array.prototype.at", js_Uint32ArrayAt, 1);
        jsB_propf(J, "Uint32Array.prototype.set", js_Uint32ArraySet, 3);
        jsB_propf(J, "Uint32Array.prototype.find", js_Uint32ArrayFind, 1);
        jsB_propf(J, "Uint32Array.prototype.Includes",js_Uint32ArrayIncludes,1);
        jsB_propf(J, "Uint32Array.prototype.reverse", js_Uint32ArrayReverse, 1);
        jsB_propf(J, "Uint32Array.prototype.get", js_Uint32ArrayGet, 1);
    }
    js_newcconstructor(J, js_newUint32Array, js_newUint32Array, "Uint32Array", 0);
    js_defglobal(J, "Uint32Array",JS_DONTENUM);
}