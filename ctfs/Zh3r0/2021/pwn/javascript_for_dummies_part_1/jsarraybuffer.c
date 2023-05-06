#include "jsi.h"
#include "jsvalue.h"
#include "jsbuiltin.h"

void js_newArrayBuffer(js_State* J) 
{
    int top = js_gettop(J);
    size_t size;
    if(top != 2) {
        js_typeerror(
            J,
            "Expecting Byte length"
        );
    }
    size = js_tonumber(J, 1);
    if(size <= 0) {
        js_typeerror(
            J,
            "Invalid byte length"
        );
    }
    while((size%4)) {
        size += 1;
    }
    js_Object* this = jsV_newobject(J, JS_CARRAYBUFFER, J->ArrayBuffer_prototype);
    this->u.ab.backingStore = js_malloc(J, (size));
    memset((void*)this->u.ab.backingStore, 0, size);
    this->u.ab.byteLength = size;
    js_pushobject(J, this);
}

void jsB_initArrayBuffer(js_State *J) 
{
    js_pushobject(J, J->ArrayBuffer_prototype);
    {
    }
    js_newcconstructor(J, js_newArrayBuffer, js_newArrayBuffer, "ArrayBuffer", 0);
    js_defglobal(J, "ArrayBuffer",JS_DONTENUM);
}