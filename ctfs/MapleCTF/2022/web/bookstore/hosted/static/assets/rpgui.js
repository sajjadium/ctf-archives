RPGUI = (function() {

/**
* init rpgui.
* this is the first file included in the compiled js.
*/

// rpgui global namespace
var RPGUI = RPGUI || {};

// lib version
RPGUI.version = 1.03;

// author
RPGUI.author = "Ronen Ness";

// if true, will init rpgui as soon as page loads
// if you set to false you need to call RPGUI.init(); yourself.
RPGUI.init_on_load = true;
window.addEventListener("load", function()
{
	if (RPGUI.init_on_load) {RPGUI.init();}
});

// init RPGUI and everything related
RPGUI.init = function()
{
	if (RPGUI._was_init) {throw "RPGUI was already init!";}
	for (var i = 0; i < RPGUI.__init_list.length; ++i)
	{
		RPGUI.__init_list[i]();
	}
	RPGUI._was_init = true;
}

// list of functions to run as part of the init process
RPGUI.__init_list = [];

// add a function to be called as part of the init process.
// note: order is preserve. you may use this function to init things after RPGUI is fully loaded, since
// all RPGUI will have its init functions during the inclusion of the script.
RPGUI.on_load = function(callback)
{
	// if was already init call immediately
	if (RPGUI._was_init) {callback();}
	
	// add to init list
	RPGUI.__init_list.push(callback);
}
/**
* Used to provide unified, easy javascript access to customized elements.
*/


// different callbacks for different methods and types
RPGUI.__update_funcs = {};
RPGUI.__create_funcs = {};
RPGUI.__get_funcs = {}
RPGUI.__set_funcs = {};

// create a customized rpgui element ("list", "dropbox", etc.)
// note: this function expect the original html element.
RPGUI.create = function(element, rpgui_type)
{
    // call the creation func and set type
    if (RPGUI.__create_funcs[rpgui_type])
    {
        element.dataset['rpguitype'] = rpgui_type;
        RPGUI.__create_funcs[rpgui_type](element);
    }
    // not a valid type? exception.
    else
    {
        throw "Not a valid rpgui type! options: " + Object.keys(RPGUI.__create_funcs);
    }
}

// update an element after you changed it manually via javascript.
// note: this function expect the original html element.
RPGUI.update = function(element)
{
    // if have update callback for this type, use it
    var type = element.dataset['rpguitype']
    if (RPGUI.__update_funcs[type])
    {
        RPGUI.__update_funcs[type](element);
    }
    // if not, use the default (firing update event)
    else
    {
        RPGUI.fire_event(element, "change");
    }
}


// set & update the value of an element.
// note: this function expect the original html element.
RPGUI.set_value = function(element, value)
{
    // if have set value callback for this type, use it
    var type = element.dataset['rpguitype'];
    if (RPGUI.__set_funcs[type])
    {
        RPGUI.__set_funcs[type](element, value);
    }
    // if not, use the default (setting "value" member)
    else
    {
        element.value = value;
    }

    // trigger update
    RPGUI.update(element);
}



// get the value of an element.
// note: this function expect the original html element.
RPGUI.get_value = function(element)
{
    // if have get value callback for this type, use it
    var type = element.dataset['rpguitype'];
    if (RPGUI.__get_funcs[type])
    {
        return RPGUI.__get_funcs[type](element);
    }
    // if not, use the default (getting the "value" member)
    else
    {
        return element.value;
    }
}
/**
* This script generate the rpgui checkbox class.
* This will replace automatically every <input> element that has the "rpgui-checkbox" class.
*/


// class name we will convert to special checkbox
var _checkbox_class = "rpgui-checkbox";

// create a rpgui-checkbox from a given element.
// note: element must be <input> of type "checkbox" for this to work properly.
RPGUI.__create_funcs["checkbox"] = function(element)
{
	RPGUI.add_class(element, _checkbox_class);
	create_checkbox(element);
};

// set function to set value of the checkbox
RPGUI.__set_funcs["checkbox"] = function(elem, value)
{
	elem.checked = value;
};

// set function to get value of the checkbox
RPGUI.__get_funcs["checkbox"] = function(elem)
{
	return elem.checked;
};

// init all checkbox elements on page load
RPGUI.on_load(function()
{
	// get all the input elements we need to upgrade
	var elems = document.getElementsByClassName(_checkbox_class);

	// iterate the selects and upgrade them
	for (var i = 0; i < elems.length; ++i)
	{
		RPGUI.create(elems[i], "checkbox");
	}
});

// upgrade a single "input" element to the beautiful checkbox class
function create_checkbox(elem)
{
	// get next sibling, assuming its the checkbox label.
	// this object will be turned into the new checkbox.
	var new_checkbox = elem.nextSibling;

	// validate
	if (!new_checkbox || new_checkbox.tagName !== "LABEL")
	{
		throw "After a '" + _checkbox_class + "' there must be a label!";
	}

	// copy all event listeners and events
	RPGUI.copy_event_listeners(elem, new_checkbox);

	// do the click event for the new checkbox
	(function(elem, new_checkbox)
	{
		new_checkbox.addEventListener("click", function()
		{
			if (!elem.disabled)
			{
				RPGUI.set_value(elem, !elem.checked);
			}

		});
	})(elem, new_checkbox);
}

/**
* Init rpgui content and what's inside.
*/

// init all the rpgui containers and their children
RPGUI.on_load(function()
{
	// get all containers and iterate them
	var contents = document.getElementsByClassName("rpgui-content");
	for (var i = 0; i < contents.length; ++i)
	{
		// get current container and init it
		var content = contents[i];

		// prevent dragging
		RPGUI.prevent_drag(content);

		// set default cursor
		RPGUI.set_cursor(content, "default");
	}
});

/**
* This script add the dragging functionality to all elements with "rpgui-draggable" class.
*/


// element currently dragged
var _curr_dragged = null;
var _curr_dragged_point = null;
var _dragged_z = 1000;

// class name we consider as draggable
var _draggable_class = "rpgui-draggable";

// set element as draggable
// note: this also add the "rpgui-draggable" css class to the element.
RPGUI.__create_funcs["draggable"] = function(element)
{
	// prevent forms of default dragging on this element
	element.draggable = false;
	element.ondragstart = function() {return false;}

	// add the mouse down event listener
	RPGUI.add_class(element, _draggable_class);
	element.addEventListener('mousedown', mouseDown);
};

// init all draggable elements (objects with "rpgui-draggable" class)
RPGUI.on_load(function()
{
	// init all draggable elements
	var elems = document.getElementsByClassName(_draggable_class);
	for (var i = 0; i < elems.length; ++i)
	{
		RPGUI.create(elems[i], "draggable");
	}

	// add mouseup event on window to stop dragging
	window.addEventListener('mouseup', mouseUp);
});

// stop drag
function mouseUp(e)
{
	_curr_dragged = null;
	window.removeEventListener('mousemove', divMove);
}

// start drag
function mouseDown(e){

	// set dragged object and make sure its really draggable
	var target = e.target || e.srcElement;
	if (!RPGUI.has_class(target, _draggable_class)) {return;}
		
	_curr_dragged = target;
	
	// set holding point
	var rect = _curr_dragged.getBoundingClientRect();
	_curr_dragged_point = {x: rect.left-e.clientX, y: rect.top-e.clientY};

	// add z-index to top this element
	target.style.zIndex = _dragged_z++;
	
	// begin dragging
	window.addEventListener('mousemove', divMove, true);

}

// dragging
function divMove(e){
	if (_curr_dragged)
	{
		_curr_dragged.style.position = 'absolute';
		_curr_dragged.style.left = (e.clientX + _curr_dragged_point.x) + 'px';
		_curr_dragged.style.top = (e.clientY + _curr_dragged_point.y) + 'px';
	}
}

/**
 * This script generate the rpgui progress-bar class.
 * This will replace automatically every <div> element that has the "rpgui-progress" class.
 */


// class name we will convert to special progress
var _progress_class = "rpgui-progress";

// create a rpgui-progress from a given element.
// note: element must be <input> of type "range" for this to work properly.
RPGUI.__create_funcs["progress"] = function(element)
{
	RPGUI.add_class(element, _progress_class);
	create_progress(element);
};

// set function to set value of the progress bar
// value should be in range of 0 - 1.0
RPGUI.__set_funcs["progress"] = function(elem, value)
{
	// get trackbar and progress bar elements
	var track = RPGUI.get_child_with_class(elem, "rpgui-progress-track");
	var progress = RPGUI.get_child_with_class(track, "rpgui-progress-fill");

	// get the two edges
	var edge_left = RPGUI.get_child_with_class(elem, "rpgui-progress-left-edge");
	var edge_right = RPGUI.get_child_with_class(elem, "rpgui-progress-right-edge");

	// set progress width
	progress.style.left = "0px";
	progress.style.width = (value * 100) + "%";
};

// init all progress elements on page load
RPGUI.on_load(function()
{
	// get all the select elements we need to upgrade
	var elems = document.getElementsByClassName(_progress_class);

	// iterate the selects and upgrade them
	for (var i = 0; i < elems.length; ++i)
	{
		RPGUI.create(elems[i], "progress");
	}
});

// upgrade a single "input" element to the beautiful progress class
function create_progress(elem)
{
	// create the containing div for the new progress
	progress_container = elem;

	// insert the progress container
	RPGUI.insert_after(progress_container, elem);

	// create progress parts (edges, track, thumb)

	// track
	var track = RPGUI.create_element("div");
	RPGUI.add_class(track, "rpgui-progress-track");
	progress_container.appendChild(track);

	// left edge
	var left_edge = RPGUI.create_element("div");
	RPGUI.add_class(left_edge, "rpgui-progress-left-edge");
	progress_container.appendChild(left_edge);

	// right edge
	var right_edge = RPGUI.create_element("div");
	RPGUI.add_class(right_edge, "rpgui-progress-right-edge");
	progress_container.appendChild(right_edge);

	// the progress itself
	var progress = RPGUI.create_element("div");
	RPGUI.add_class(progress, "rpgui-progress-fill");
	track.appendChild(progress);

	// set color
	if (RPGUI.has_class(elem, "blue")) {progress.className += " blue";}
	if (RPGUI.has_class(elem, "red")) {progress.className += " red";}
	if (RPGUI.has_class(elem, "green")) {progress.className += " green";}

	// set starting default value
	var starting_val = elem.dataset.value !== undefined ? parseFloat(elem.dataset.value) : 1;
	RPGUI.set_value(elem, starting_val);
}

/**
* This script generate the rpgui radio class.
* This will replace automatically every <input> element that has the "rpgui-radio" class.
*/


// class name we will convert to special radio
var _radio_class = "rpgui-radio";

// create a rpgui-radio from a given element.
// note: element must be <input> of type "radio" for this to work properly.
RPGUI.__create_funcs["radio"] = function(element)
{
	RPGUI.add_class(element, _radio_class);
	create_radio(element);
};

// set function to set value of the radio
RPGUI.__set_funcs["radio"] = function(elem, value)
{
	elem.checked = value;
};

// set function to get value of the radio button
RPGUI.__get_funcs["radio"] = function(elem)
{
	return elem.checked;
};

// init all radio elements on page load
RPGUI.on_load(function()
{
	// get all the input elements we need to upgrade
	var elems = document.getElementsByClassName(_radio_class);

	// iterate the selects and upgrade them
	for (var i = 0; i < elems.length; ++i)
	{
		RPGUI.create(elems[i], "radio");
	}
});

// upgrade a single "input" element to the beautiful radio class
function create_radio(elem)
{
	// get next sibling, assuming its the radio label.
	// this object will be turned into the new radio.
	var new_radio = elem.nextSibling;

	// validate
	if (!new_radio || new_radio.tagName !== "LABEL")
	{
		throw "After a '" + _radio_class + "' there must be a label!";
	}

	// copy all event listeners and events
	RPGUI.copy_event_listeners(elem, new_radio);

	// do the click event for the new radio
	(function(elem, new_radio)
	{
		new_radio.addEventListener("click", function()
		{
			if (!elem.disabled)
			{
				RPGUI.set_value(elem, true);
			}
		});
	})(elem, new_radio);
}

/**
* This script generate the rpgui dropdown <select>.
* This will replace automatically every <select> element that has the "rpgui-dropdown" class.
*/


// class name we will convert to dropdown
var _dropdown_class = "rpgui-dropdown";

// create a rpgui-dropdown from a given element.
// note: element must be <select> with <option> tags that will turn into the items
RPGUI.__create_funcs["dropdown"] = function(element)
{
	RPGUI.add_class(element, _dropdown_class);
	create_dropdown(element);
};

// init all dropdown elements on page load
RPGUI.on_load(function()
{
	// get all the select elements we need to upgrade
	var elems = document.getElementsByClassName(_dropdown_class);

	// iterate the selects and upgrade them
	for (var i = 0; i < elems.length; ++i)
	{
		RPGUI.create(elems[i], "dropdown");
	}
});

// upgrade a single "select" element to the beautiful dropdown
function create_dropdown(elem)
{
	// prefix to add arrow down next to selection header
	var arrow_down_prefix = "<label>&#9660;</label> ";

	// create the paragraph that will display the select_header option
	var select_header = RPGUI.create_element("p");
	if (elem.id) {select_header.id = elem.id + "-rpgui-dropdown-head"};
	RPGUI.add_class(select_header, "rpgui-dropdown-imp rpgui-dropdown-imp-header");
	RPGUI.insert_after(select_header, elem);

	// create the list to hold all the options
	var list = RPGUI.create_element("ul");
	if (elem.id) {list.id = elem.id + "-rpgui-dropdown"};
	RPGUI.add_class(list, "rpgui-dropdown-imp");
	RPGUI.insert_after(list, select_header);

	// set list top to be right under the select header
	var header_rect = select_header.getBoundingClientRect();
	list.style.position = "absolute";

	// set list width (-14 is to compensate borders)
	list.style.width = (header_rect.right - header_rect.left - 14) + "px";
	list.style.display = "none";

	// now hide the original select
	elem.style.display = "none";

	// iterate over all the options in this select
	for (var i = 0; i < elem.children.length; ++ i)
	{
		// if this child is not option, skip
		var option = elem.children[i];
		if (option.tagName != "OPTION") continue;

		// add the new option as list item
		var item = RPGUI.create_element("li");
		item.innerHTML = option.innerHTML;
		list.appendChild(item);

		// copy all event listeners from original option to the new item
		RPGUI.copy_event_listeners(option, item);

		// set option callback (note: wrapped inside namespace to preserve vars)
		(function(elem, option, item, select_header, list)
		{
			// when clicking the customized option
			item.addEventListener('click', function()
			{
				// set the header html and hide the list
				select_header.innerHTML = arrow_down_prefix + option.innerHTML;
				list.style.display = "none";

				// select the option in the original selection
				option.selected = true;
				RPGUI.fire_event(elem, "change");
			});

		})(elem, option, item, select_header, list);
	}

	// now set list and header callbacks
	// create a namespace to preserve variables
	(function(elem, list, select_header)
	{
		// when clicking the selected header show / hide the options list
		select_header.onclick = function()
		{
			if (!elem.disabled)
			{
				var prev = list.style.display;
				list.style.display = prev == "none" ? "block" : "none";
			}
		}

		// when mouse leave the options list, hide it
		list.onmouseleave = function()
		{
			list.style.display = "none";
		}

	})(elem, list, select_header);

	// lastly, listen to when the original select changes and update the customized list
	(function(elem, select_header, list)
	{
		// the function to update dropdown
		_on_change = function()
		{
			// set the header html and hide the list
			if (elem.selectedIndex != -1)
			{
				select_header.innerHTML = arrow_down_prefix + elem.options[elem.selectedIndex].text;
			}
			else
			{
				select_header.innerHTML = arrow_down_prefix;
			}
			list.style.display = "none";
		}

		// register the update function and call it to set initial state
		elem.addEventListener('change', _on_change);
		_on_change();
		
	})(elem, select_header, list);
}

/**
* This script generate the rpgui list <select>.
* This will replace automatically every <select> element that has the "rpgui-list" class.
*/


// class name we will convert to list
var _list_class = "rpgui-list";

// create a rpgui-list from a given element.
// note: element must be <select> with <option> tags that will turn into the items
RPGUI.__create_funcs["list"] = function(element)
{
	RPGUI.add_class(element, _list_class);
	create_list(element);
};

// init all list elements on page load
RPGUI.on_load(function()
{
	// get all the select elements we need to upgrade
	var elems = document.getElementsByClassName(_list_class);

	// iterate the selects and upgrade them
	for (var i = 0; i < elems.length; ++i)
	{
		RPGUI.create(elems[i], "list");
	}
});

// upgrade a single "select" element to the beautiful list
function create_list(elem)
{
	// default list size is 3
	if (!elem.size) elem.size = 3;

	// create the list to hold all the options
	var list = RPGUI.create_element("ul");
	if (elem.id) {list.id = elem.id + "-rpgui-list"};
	RPGUI.add_class(list, "rpgui-list-imp");
	elem.parentNode.insertBefore(list, elem.nextSibling);

	// now hide the original select
	elem.style.display = "none";

	// iterate over all the options in this select
	var all_items = [];
	for (var i = 0; i < elem.children.length; ++ i)
	{
		// if this child is not option, skip
		var option = elem.children[i];
		if (option.tagName != "OPTION") continue;

		// add the new option as list item
		var item = RPGUI.create_element("li");
		item.innerHTML = option.innerHTML;
		list.appendChild(item);

		// set dataset value
		item.dataset['rpguivalue'] = option.value;

		// add to list of all items
		all_items.push(item);

		// copy all event listeners from original option to the new item
		RPGUI.copy_event_listeners(option, item);

		// set option callback (note: wrapped inside namespace to preserve vars)
		(function(elem, option, item, list, all_items)
		{
			// when clicking the customized option
			item.addEventListener('click', function()
			{
				// select the option in the original selection
				if (!elem.disabled)
				{
					option.selected = true;
					RPGUI.fire_event(elem, "change");
				}
			});

		})(elem, option, item, list, all_items);
	}

	// if got any items set list height based on the size param
	if (all_items.length && elem.size)
	{
		
		// get the actual height of a single item in list
		var height = all_items[0].offsetHeight;

		// set list height based on size
		list.style.height = (height * elem.size) + "px";
		
	}
	
	// lastly, listen to when the original select changes and update the customized list
	(function(elem, all_items)
	{
		// handle value change
		elem.addEventListener('change', function()
		{
			_on_change(this);
		});
		function _on_change(elem)
		{
			for (var i = 0; i < all_items.length; ++i)
			{
				var item = all_items[i];
				if (item.dataset['rpguivalue'] == elem.value)
				{
					RPGUI.add_class(item, "rpgui-selected");
				}
				else
				{
					RPGUI.remove_class(item, "rpgui-selected");
				}
			}
		}

		// call the on-change on init to set initial state
		_on_change(elem);

	})(elem, all_items);
}

/**
* This script generate the rpgui slider class.
* This will replace automatically every <input> element that has the "rpgui-slider" class.
*/


// class name we will convert to special slider
var _slider_class = "rpgui-slider";

// create a rpgui-slider from a given element.
// note: element must be <input> of type "range" for this to work properly.
RPGUI.__create_funcs["slider"] = function(element)
{
	RPGUI.add_class(element, _slider_class);
	create_slider(element);
};

// init all slider elements on page load
RPGUI.on_load(function()
{
	// get all the select elements we need to upgrade
	var elems = document.getElementsByClassName(_slider_class);

	// iterate the selects and upgrade them
	for (var i = 0; i < elems.length; ++i)
	{
		RPGUI.create(elems[i], "slider");
	}
});

// upgrade a single "input" element to the beautiful slider class
function create_slider(elem)
{
	// check if should do it golden slider
	var golden = RPGUI.has_class(elem, "golden") ? " golden" : "";

	// create the containing div for the new slider
	var slider_container = RPGUI.create_element("div");
	if (elem.id) {slider_container.id = elem.id + "-rpgui-slider"};
	RPGUI.copy_css(elem, slider_container);
	RPGUI.add_class(slider_container, "rpgui-slider-container" + golden);

	// insert the slider container
	RPGUI.insert_after(slider_container, elem);

	// set container width based on element original width
	slider_container.style.width = elem.offsetWidth + "px";

	// create slider parts (edges, track, thumb)

	// track
	var track = RPGUI.create_element("div");
	RPGUI.add_class(track, "rpgui-slider-track" + golden);
	slider_container.appendChild(track);

	// left edge
	var left_edge = RPGUI.create_element("div");
	RPGUI.add_class(left_edge, "rpgui-slider-left-edge" + golden);
	slider_container.appendChild(left_edge);

	// right edge
	var right_edge = RPGUI.create_element("div");
	RPGUI.add_class(right_edge, "rpgui-slider-right-edge" + golden);
	slider_container.appendChild(right_edge);

	// thumb (slider value show)
	var thumb = RPGUI.create_element("div");
	RPGUI.add_class(thumb, "rpgui-slider-thumb" + golden);
	slider_container.appendChild(thumb);

	// hide original slider
	elem.style.display = "none";

	// copy events from original slider to container.
	// this will handle things like click, mouse move, mouse up, etc.
	// it will not handle things like "onchange".
	RPGUI.copy_event_listeners(elem, slider_container);

	// now set events (wrap them in anonymous function to preserve local vars)
	var state = {mouse_down: false};
	(function(elem, slider_container, thumb, track, state, right_edge, left_edge)
	{
		// get the range of the original slider (min and max)
		var min = parseFloat(elem.min);
		var max = parseFloat(elem.max);

		// calculate edges width and track actual width
		var edges_width = right_edge.offsetWidth + left_edge.offsetWidth;
		var track_width = track.offsetWidth - edges_width;

		// set state if moving slider or not
		slider_container.addEventListener('mouseup', function(e)
		{
			state.mouse_down = false;
		});
		window.addEventListener('mouseup', function(e)
		{
			state.mouse_down = false;
		});
		track.addEventListener('mousedown', function(e)
		{
			state.mouse_down = true;
			slide(e.offsetX || e.layerX);
		});
		slider_container.addEventListener('mousedown', function(e)
		{
			state.mouse_down = true;
		});

		// handle clicking on edges (set to min / max)
		left_edge.addEventListener('mousedown', function(e)
		{
			set_value(min);
		});
		right_edge.addEventListener('mousedown', function(e)
		{
			set_value(max);
		});
		left_edge.addEventListener('mousemove', function(e)
		{
			if (state.mouse_down) set_value(min);
		});
		right_edge.addEventListener('mousemove', function(e)
		{
			if (state.mouse_down) set_value(max);
		});

		// handle sliding
		function slide(pos)
		{
			// calc new slider value
			var new_val = min + Math.round((pos / track_width) * (max-min)) - 1;

			// set thumb position
			set_value(new_val);
		}

		// setting value
		function set_value(new_val)
		{
			if (!elem.disabled &&
				elem.value != new_val)
			{
				RPGUI.set_value(elem, new_val);
			}
		}

		// moving the slider
		track.addEventListener('mousemove', function(e)
		{
			if (state.mouse_down && !elem.disabled)
			{
				slide(e.offsetX || e.layerX);
			}
		});


		// when original slider value change update thumb position
		elem.addEventListener("change", function(e)
		{
			_onchange();
		});
		function _onchange()
		{
			// get the range of the original slider (min and max)
			var step = track_width / (max-min);
			var relative_val = Math.round(parseFloat(elem.value) - min);
			thumb.style.left = (Math.floor(edges_width * 0.25) + (relative_val * step)) + "px";
		}

		// call "_onchange()" to init the thumb starting position
		_onchange();

	})(elem, slider_container, thumb, track, state, right_edge, left_edge);

}
/**
* Some helpers and utils.
*/


// create and return html element for rpgui internal mechanisms
// element is string, element type (like "div" or "p")
RPGUI.create_element = function(element)
{
    // create element
    element = document.createElement(element);

    // return element
    return element;
};

// set cursor for given element
// element is element to set.
// cursor is string, what cursor to use (default / point / .. see cursor.css for more info ).
RPGUI.set_cursor = function(element, cursor)
{
    RPGUI.add_class(element, "rpgui-cursor-" + cursor);
};

// prevent element dragging
RPGUI.prevent_drag = function(element)
{
    /*
    // this code was removed because I found a cross-browser way to cover it all via css.
    element.draggable=false;
    element.ondrop=function(){return false;}
    element.ondragstart=function(){return false;}
    */
};

// copy the style of one element into another
RPGUI.copy_css = function(from, to)
{
    to.style.cssText = from.style.cssText;
};

// check if element have class
RPGUI.has_class = function(element, cls)
{
    return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
};

// add class to element (but only if don't already have it)
RPGUI.add_class = function(element, cls)
{
    if (!RPGUI.has_class(element, cls))
    {
        element.className += " " + cls;
    }
};

// get child element with classname
RPGUI.get_child_with_class = function(elem, cls)
{
    for (var i = 0; i < elem.childNodes.length; i++)
    {
        if (RPGUI.has_class(elem.childNodes[i], cls))
        {
          return elem.childNodes[i];
        }
    }
};

// remove a class from an element
RPGUI.remove_class = function(element, cls)
{
    element.className = (' ' + element.className + ' ').replace(cls, "");
    element.className = element.className.substring(1, element.className.length-1);
};

// fire event from element
// type should be string like "change", "click", "mouseup", etc.
RPGUI.fire_event = function(element, type)
{
    // firing the event properly according to StackOverflow
    // http://stackoverflow.com/questions/2856513/how-can-i-trigger-an-onchange-event-manually
    if ("createEvent" in document) {
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent(type, false, true);
        element.dispatchEvent(evt);
    }
    else {
        element.fireEvent("on" + type);
    }
};

// copy all event listeners from one element to the other
RPGUI.copy_event_listeners = function(from, to)
{
    // copy all event listeners
    if (typeof getEventListeners == "function")
    {
        var events = getEventListeners(from);
        for(var p in events) {
            events[p].forEach(function(ev) {
                // {listener: Function, useCapture: Boolean}
                to.addEventListener(p, ev.listener, ev.useCapture);
            });
        }
    }

    // now copy all attributes that start with "on"
    for (attr in from)
    {
        if (attr.indexOf("on") === 0)
        {
            to[attr] = from[attr];
        }
    }
};

// insert one html element after another given element
RPGUI.insert_after = function(to_insert, after_element)
{
    after_element.parentNode.insertBefore(to_insert, after_element.nextSibling);
};
return RPGUI;})();