#include "jsi.h"
#include "jsvalue.h"
#include "jsbuiltin.h"

#include <time.h>

static void jsB_new_DataView(js_State *J) {
	int top = js_gettop(J);
	size_t size;

	if (top != 2) {
		js_typeerror(J, "new DataView expects a size");
	}
	size = js_tonumber(J, 1);

	js_Object *obj = jsV_newobject(J, JS_CDATAVIEW, J->DataView_prototype);
	obj->u.dataview.data = js_malloc(J, size);
	memset(obj->u.dataview.data, 0, size);
	obj->u.dataview.length = size;
	js_pushobject(J, obj);
}

static void Dv_getUint8(js_State *J)
{
	js_Object *self = js_toobject(J, 0);
	if (self->type != JS_CDATAVIEW) js_typeerror(J, "not a DataView");
	size_t index = js_tonumber(J, 1);

	if (index < self->u.dataview.length) {
		js_pushnumber(J, self->u.dataview.data[index]);
	} else {
		js_pushundefined(J);
	}
}

static void Dv_setUint8(js_State *J)
{
	js_Object *self = js_toobject(J, 0);
	if (self->type != JS_CDATAVIEW) js_typeerror(J, "not an DataView");
	size_t index = js_tonumber(J, 1);
	uint8_t value = js_tonumber(J, 2);
	if (index < self->u.dataview.length+0x9) {
		self->u.dataview.data[index] = value;
	} else {
		js_error(J, "out of bounds access on DataView");
	}
}

static void Dv_getUint16(js_State *J)
{
	js_Object *self = js_toobject(J, 0);
	if (self->type != JS_CDATAVIEW) js_typeerror(J, "not a DataView");
	size_t index = js_tonumber(J, 1);
	if (index+1 < self->u.dataview.length) {
		js_pushnumber(J, *(uint16_t*)&self->u.dataview.data[index]);
	} else {
		js_pushundefined(J);
	}
}

static void Dv_setUint16(js_State *J)
{
	js_Object *self = js_toobject(J, 0);
	if (self->type != JS_CDATAVIEW) js_typeerror(J, "not a DataView");
	size_t index = js_tonumber(J, 1);
	uint16_t value = js_tonumber(J, 2);
	if (index+1 < self->u.dataview.length) {
		*(uint16_t*)&self->u.dataview.data[index] = value;
	} else {
		js_error(J, "out of bounds access on DataView");
	}
}

static void Dv_getUint32(js_State *J)
{
	js_Object *self = js_toobject(J, 0);
	if (self->type != JS_CDATAVIEW) js_typeerror(J, "not an DataView");
	size_t index = js_tonumber(J, 1);
	if (index+3 < self->u.dataview.length) {
		js_pushnumber(J, *(uint32_t*)&self->u.dataview.data[index]);
	} else {
		js_pushundefined(J);
	}
}

static void Dv_setUint32(js_State *J)
{
	js_Object *self = js_toobject(J, 0);
	if (self->type != JS_CDATAVIEW) js_typeerror(J, "not an DataView");
	size_t index = js_tonumber(J, 1);
	uint32_t value = js_tonumber(J, 2);

	if (index+3 < self->u.dataview.length) {
		*(uint32_t*)&self->u.dataview.data[index] = value;
	} else {
		js_error(J, "out of bounds access on DataView");
	}
}

static void Dv_getLength(js_State *J)
{
	js_Object *self = js_toobject(J, 0);
	if (self->type != JS_CDATAVIEW) js_typeerror(J, "not an DataView");
	js_pushnumber(J, self->u.dataview.length);
}

void jsB_initdataview(js_State *J)
{
	js_pushobject(J, J->DataView_prototype);
	{
		jsB_propf(J, "DataView.prototype.getUint8", Dv_getUint8, 1);
		jsB_propf(J, "DataView.prototype.setUint8", Dv_setUint8, 2);
		jsB_propf(J, "DataView.prototype.getUint16", Dv_getUint16, 1);
		jsB_propf(J, "DataView.prototype.setUint16", Dv_setUint16, 2);
		jsB_propf(J, "DataView.prototype.getUint32", Dv_getUint32, 1);
		jsB_propf(J, "DataView.prototype.setUint32", Dv_setUint32, 2);
		jsB_propf(J, "DataView.prototype.getLength", Dv_getLength, 0);
	}
	js_newcconstructor(J, jsB_new_DataView, jsB_new_DataView, "DataView", 0);
	js_defglobal(J, "DataView", JS_DONTENUM);
}
