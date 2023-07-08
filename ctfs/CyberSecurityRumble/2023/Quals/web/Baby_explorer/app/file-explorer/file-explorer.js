// Folder and File Explorer.  A pure, zero-dependencies Javascript widget.
// (C) 2020 CubicleSoft.  All Rights Reserved.

(function() {
	// Prevent multiple instances.
	if (window.hasOwnProperty('FileExplorer'))  return;

	var EscapeHTML = function(text) {
		var map = {
			'&': '&amp;',
			'<': '&lt;',
			'>': '&gt;',
			'"': '&quot;',
			"'": '&#039;'
		};

		return text.replace(/[&<>"']/g, function(m) { return map[m]; });
	}

	var FormatStr = function(format) {
		var args = Array.prototype.slice.call(arguments, 1);

		return format.replace(/{(\d+)}/g, function(match, number) {
			return (typeof args[number] != 'undefined' ? args[number] : match);
		});
	};

	var GetDisplayFilesize = function(numbytes, adjustprecision, units) {
		if (numbytes == 0)  return '0 Bytes';
		if (numbytes == 1)  return '1 Byte';

		numbytes = Math.abs(numbytes);
		var magnitude, abbreviations;
		if (units && units.toLowerCase() === 'iec_formal')
		{
			magnitude = Math.pow(2, 10);
			abbreviations = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
		}
		else if (units && units.toLowerCase() === 'si')
		{
			magnitude = Math.pow(10, 3);
			abbreviations = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
		}
		else
		{
			magnitude = Math.pow(2, 10);
			abbreviations = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
		}

		var pos = Math.floor(Math.log(numbytes) / Math.log(magnitude));
		var result = (numbytes / Math.pow(magnitude, pos));

		return (pos == 0 || (adjustprecision && result >= 99.995) ? result.toFixed(0) : result.toFixed(2)) + ' ' + abbreviations[pos];
	};

	var CreateNode = function(tag, classes, attrs, styles) {
		var elem = document.createElement(tag);

		if (classes)
		{
			if (typeof classes === 'string')  elem.className = classes;
			else  elem.className = classes.join(' ');
		}

		if (attrs)  Object.assign(elem, attrs);

		if (styles)  Object.assign(elem.style, styles);

		return elem;
	};

	var DebounceAttributes = function(options) {
		if (!(this instanceof DebounceAttributes))  return new DebounceAttributes(options);

		var intervaltimer = null, numsame;
		var $this = this;

		var defaults = {
			watchers: [],
			interval: 50,
			stopsame: 1,

			callback: null,
			intervalcallback: null
		};

		$this.settings = Object.assign({}, defaults, options);

		var MainIntervalHandler = function() {
			var nummatches = 0;

			for (var x = 0; x < $this.settings.watchers.length; x++)
			{
				var watcher = $this.settings.watchers[x];

				if (watcher.val === watcher.elem[watcher.attr])  nummatches++;
				else  watcher.val = watcher.elem[watcher.attr];
			}

			if (nummatches < $this.settings.watchers.length)
			{
				numsame = 0;

				if ($this.settings.intervalcallback)  $this.settings.intervalcallback.call($this);
			}
			else
			{
				numsame++;

				if (numsame >= $this.settings.stopsame)
				{
					$this.Stop();

					if ($this.settings.intervalcallback)  $this.settings.intervalcallback.call($this);

					if ($this.settings.callback)  $this.settings.callback.call($this);
				}
			}
		};


		// Public functions.

		$this.Start = function() {
			if (!intervaltimer)
			{
				numsame = 0;

				intervaltimer = setInterval(MainIntervalHandler, $this.settings.interval);
			}
		};

		$this.Stop = function() {
			if (intervaltimer)
			{
				clearInterval(intervaltimer);

				intervaltimer = null;
			}
		};

		$this.Destroy = function() {
			$this.Stop();

			$this = null;
		}
	};

	function GetScrollLineHeight() {
		var iframe = document.createElement('iframe');
		iframe.src = '#';
		document.body.appendChild(iframe);
		var iwin = iframe.contentWindow;
		var idoc = iwin.document;
		idoc.open();
		idoc.write('<!DOCTYPE html><html><head></head><body><span>a</span></body></html>');
		idoc.close();
		var span = idoc.body.firstElementChild;
		var r = span.offsetHeight;
		document.body.removeChild(iframe);

		return r;
	}

	var scrolllineheight = GetScrollLineHeight();

	// Clean up history stack.
	var capturingrefs = 0, prevscrollrestore;
	function HistoryPopStateHandler(e) {
		if (!capturingrefs)
		{
			if (e.state && e.state._fileexplorer)
			{
				var prevscrollstatecopy = e.state._fileexplorerprevscroll;

				window.history.back();

				if (prevscrollstatecopy)  prevscrollrestore = prevscrollstatecopy;
			}
			else if (prevscrollrestore)
			{
				setTimeout(function() {
					window.history.scrollRestoration = prevscrollrestore;

					prevscrollrestore = null;
				}, 20);
			}
		}
	}

	window.addEventListener('popstate', HistoryPopStateHandler, true);

	if (window.history.state && window.history.state._fileexplorer)
	{
		var prevscrollstatecopy = window.history.state._fileexplorerprevscroll;

		window.history.back();

		if (prevscrollstatecopy)  prevscrollrestore = prevscrollstatecopy;
	}

	// Extracts and returns global drag group icon data for drag-and-drop operations.
	function GetFileExplorerDragIconData(e, group) {
		if (!e.dataTransfer)  return false;

		for (var x = 0; x < e.dataTransfer.types.length; x++)
		{
			if (e.dataTransfer.types[x].startsWith('application/file-explorer-icon;'))
			{
				try
				{
					var icondata = JSON.parse(e.dataTransfer.types[x].substring(31));

					return (!group || group === icondata.group ? icondata : false);
				}
				catch (e)
				{
				}
			}
		}

		return false;
	}

	// Creates a custom overlay that tracks with the position when entering the window.
	var fe_numdragenters = 0, fe_dragiconoverlay, fe_dragiconoverlaypos = {};
	function OverlayDragEnterHandler(e) {
		if (!fe_numdragenters)
		{
			var icondata = GetFileExplorerDragIconData(e);

			if (icondata !== false)
			{
				// Create the floating icon tracking overlay.
				fe_dragiconoverlay = CreateNode('div', ['fe_fileexplorer_floating_drag_icon_wrap']);
				var innernode = CreateNode('div', ['fe_fileexplorer_floating_drag_icon_wrap_inner']);
				var iconnode = CreateNode('div', ['fe_fileexplorer_item_icon']);

				if (icondata.numitems > 1)  innernode.dataset.numitems = icondata.numitems;

				iconnode.classList.add('fe_fileexplorer_item_icon_' + icondata.type);

				innernode.appendChild(iconnode);
				fe_dragiconoverlay.appendChild(innernode);
				document.body.appendChild(fe_dragiconoverlay);

				fe_dragiconoverlaypos = {
					lastx: -9999,
					lasty: 0,
					xdiff: Math.floor(fe_dragiconoverlay.offsetWidth / 2),
					ydiff: Math.floor(fe_dragiconoverlay.offsetHeight - 8)
				};
			}
		}

		fe_numdragenters++;
	}

	// Moves the overlay to the drag position.
	function OverlayDragOverHandler(e) {
		if (fe_dragiconoverlay && (fe_dragiconoverlaypos.lastx !== e.clientX || fe_dragiconoverlaypos.lasty !== e.clientY))
		{
			fe_dragiconoverlaypos.lastx = e.clientX;
			fe_dragiconoverlaypos.lasty = e.clientY;

			// Update the overlay position.
			fe_dragiconoverlay.style.left = (e.clientX - fe_dragiconoverlaypos.xdiff) + 'px';
			fe_dragiconoverlay.style.top = (e.clientY - fe_dragiconoverlaypos.ydiff) + 'px';
		}
	}

	// Removes the custom overlay when leaving the window.
	function OverlayDragLeaveHandler(e) {
		fe_numdragenters--;

		if (fe_numdragenters < 1)
		{
			fe_numdragenters = 0;

			if (fe_dragiconoverlay)
			{
				fe_dragiconoverlay.parentNode.removeChild(fe_dragiconoverlay);
				fe_dragiconoverlay = null;
			}

			fe_dragiconoverlaypos = {};
		}
	}

	window.addEventListener('dragenter', OverlayDragEnterHandler, true);
	window.addEventListener('dragover', OverlayDragOverHandler, true);
	window.addEventListener('dragleave', OverlayDragLeaveHandler, true);
	window.addEventListener('drop', OverlayDragLeaveHandler, true);


	// Basic XMLHttpRequest (XHR) wrapper.
	var PrepareXHR = function(options) {
		if (!(this instanceof PrepareXHR))  return new PrepareXHR(options);

		var sent = false;
		var $this = this;

		$this.xhr = new XMLHttpRequest();

		var RequestEndedHandler = function(e) {
			if ($this)  $this.xhr = null;
		};

		$this.xhr.addEventListener('loadend', RequestEndedHandler);

		if (options.onsuccess || options.onload)  $this.xhr.addEventListener('load', options.onsuccess || options.onload);
		if (options.onerror)
		{
			$this.xhr.addEventListener('error', options.onerror);

			if (!options.onabort)  $this.xhr.addEventListener('abort', options.onerror);
			if (!options.ontimeout)  $this.xhr.addEventListener('timeout', options.onerror);
		}
		if (options.onabort)  $this.xhr.addEventListener('abort', options.onabort);
		if (options.onloadstart)  $this.xhr.addEventListener('loadstart', options.onloadstart);
		if (options.onprogress)  $this.xhr.addEventListener('progress', options.onprogress);
		if (options.ontimeout)  $this.xhr.addEventListener('timeout', options.ontimeout);
		if (options.onloadend)  $this.xhr.addEventListener('loadend', options.onloadend);


		// Public functions.

		// Transparently route event listener registration/removals.
		$this.upload = {};
		$this.upload.addEventListener = function(type, listener, options) {
			if (!sent && $this && $this.xhr)  $this.xhr.upload.addEventListener(type, listener, options);
		};

		$this.upload.removeEventListener = function(type, listener, options) {
			if ($this && $this.xhr)  $this.xhr.upload.removeEventListener(type, listener, options);
		};

		$this.addEventListener = function(type, listener, options) {
			if (!sent && $this && $this.xhr)  $this.xhr.addEventListener(type, listener, options);
		};

		$this.removeEventListener = function(type, listener, options) {
			if ($this && $this.xhr)  $this.xhr.removeEventListener(type, listener, options);
		};

		// Returns the calculated method.
		$this.GetMethod = function() {
			return (options.method || (options.params || options.body ? 'POST' : 'GET'));
		};

		$this.PrepareBody = function() {
			if (options.body)  return options.body;

			var method = $this.GetMethod();

			// Build a FormData object.
			var xhrbody = (options.params || method === 'POST' ? new FormData() : null);

			if (options.params)
			{
				if (options.params instanceof FormData)
				{
					xhrbody = options.params;
				}
				else if (Array.isArray(options.params))
				{
					for (var x = 0; x < options.params.length; x++)  xhrbody.append(options.params[x].name, options.params[x].value);
				}
				else
				{
					for (var x in options.params)
					{
						if (options.params.hasOwnProperty(x))
						{
							if (typeof options.params[x] === 'string' || typeof options.params[x] === 'number')  xhrbody.append(x, options.params[x]);
						}
					}
				}
			}

			return xhrbody;
		};

		$this.Send = function(xhrbody) {
			if (sent || !$this || !$this.xhr)  return;

			sent = true;

			$this.xhr.open($this.GetMethod(), options.url);

			// Set request headers.
			if (options.headers)
			{
				for (var x in options.headers)
				{
					if (options.headers.hasOwnProperty(x) && typeof options.headers[x] === 'string')  $this.xhr.setRequestHeader(x, options.headers[x]);
				}
			}

			if (!xhrbody)  xhrbody = $this.PrepareBody();

			// Send the XHR request.
			$this.xhr.send(xhrbody);
		};

		$this.Abort = function() {
			if (!$this || !$this.xhr)  return;

			var tempxhr = $this.xhr;

			$this.xhr = null;

			if (sent)  tempxhr.abort();
		};

		$this.Destroy = function() {
			$this.Abort();

			$this = null;
		};
	};


	// Image loader.  Items can be cancelled.
	var ImageLoader = function(options) {
		if (!(this instanceof ImageLoader))  return new ImageLoader(options);

		var activequeue = {}, numactive = 0, queue = {}, numqueued = 0, minqueueid = 1, nextid = 1;
		var $this = this;

		var defaults = {
			maxactive: 10
		};

		$this.settings = Object.assign({}, defaults, options);

		var ImgLoadHandler = function(e) {
			var id = e.target._ilid;

			var opts = activequeue[id];

			delete activequeue[id];

			numactive--;

			opts.img.onload = null;
			opts.img.onerror = null;

			if (opts.callback)  opts.callback.call($this, opts, true, e);

			$this.ProcessQueue();
		};

		var ImgErrorHandler = function(e) {
			var id = e.target._ilid;

			var opts = activequeue[id];

			delete activequeue[id];

			numactive--;

			opts.img.onload = null;
			opts.img.onerror = null;

			if (opts.callback)  opts.callback.call($this, opts, false, e);

			$this.ProcessQueue();
		};

		// Public functions.

		// Adds an image request to the queue.
		// Required opts keys:  src (image URL).
		// Optional opts keys:  width, height, callback.
		// Reserved opts keys:  id, started, img.
		$this.AddToQueue = function(opts) {
			// Ignore if an existing ID is already in a queue.
			if (opts.id && ((opts.id in activequeue) || (opts.id in queue)))  return;

			opts.id = nextid;

			queue[nextid] = opts;
			numqueued++;

			nextid++;
		};

		// Starts the next images in the queue up to maxactive.
		$this.ProcessQueue = function() {
			while (numactive < $this.settings.maxactive && numqueued)
			{
				while (minqueueid < nextid && !queue.hasOwnProperty(minqueueid))  minqueueid++;

				// Move an item from the waiting queue to the active queue.
				var opts = queue[minqueueid];
				delete queue[minqueueid];
				numqueued--;

				activequeue[opts.id] = opts;
				numactive++;

				// Create the image.
				var imgnode = (opts.width && opts.height ? new Image(opts.width, opts.height) : new Image());

				imgnode._ilid = opts.id;

				opts.started = Date.now();
				opts.img = imgnode;

				imgnode.onload = ImgLoadHandler;
				imgnode.onerror = ImgErrorHandler;
				imgnode.src = opts.src;
			}
		};

		// Checks to see if the supplied ID is in the active queue.
		$this.IsActive = function(id) {
			return (id in activequeue);
		};

		// Remove an item from the queue it is in.
		$this.RemoveFromQueue = function(id) {
			if (id in queue)
			{
				delete queue[id];

				numqueued--;
			}
			else if (id in activequeue)
			{
				var opts = activequeue[id];

				// Cancel an active image download.
				opts.img.onload = null;
				opts.img.onerror = null;
				opts.img.src = '';

				delete opts.img;

				delete activequeue[id];

				numactive--;
			}
		};

		$this.Destroy = function() {
			for (var x in activequeue)
			{
				if (activequeue.hasOwnProperty(x))
				{
					activequeue[x].img.onload = null;
					activequeue[x].img.onerror = null;
					activequeue[x].img.src = '';

					delete activequeue[x].img;
				}
			}

			activequeue = {};
			numactive = 0;
			queue = {};
			numqueued = 0;

			$this = null;
		};
	};

	// Single instance of ImageLoader for loading thumbnails.
	var fe_thumbnailloader = new ImageLoader();


	// Folder tracking.  Manages information related to folders and files in the defined folder.
	// Pass in an array of path segments to define the path.  Each path segment is an array consisting of [id, value, attrs].
	var Folder = function(path) {
		if (!(this instanceof Folder))  return new Folder(path);

		var triggers = {}, entries = [], entryidmap = {}, busyref = 0, busyqueue = [], autosort = true;
		var $this = this;

		if (!path[path.length - 1][2])  path[path.length - 1][2] = {};

		// Internal functions.
		var DispatchEvent = function(eventname, params) {
			if (!triggers[eventname])  return;

			triggers[eventname].forEach(function(callback) {
				if (Array.isArray(params))  callback.apply($this, params);
				else  callback.call($this, params);
			});
		};

		// Public DOM-style functions.
		$this.addEventListener = function(eventname, callback) {
			if (!triggers[eventname])  triggers[eventname] = [];

			for (var x in triggers[eventname])
			{
				if (triggers[eventname][x] === callback)  return;
			}

			triggers[eventname].push(callback);
		};

		$this.removeEventListener = function(eventname, callback) {
			if (!triggers[eventname])  return;

			for (var x in triggers[eventname])
			{
				if (triggers[eventname][x] === callback)
				{
					triggers[eventname].splice(x, 1);

					return;
				}
			}
		};

		$this.hasEventListener = function(eventname) {
			return (triggers[eventname] && triggers[eventname].length);
		};

		// Internal variables.
		$this.lastrefresh = 0;
		$this.waiting = true;
		$this.refs = 0;

		// Public functions.

		// Add the value of newval to the folder busy state.  Any queued changes will be applied when cleared.
		$this.SetBusyRef = function(newval) {
			busyref += newval;
			if (busyref < 0)  busyref = 0;

			while (!busyref && busyqueue.length)
			{
				var item = busyqueue.shift();

				item.callback.apply($this, item.callbackopts);
			}
		};

		$this.IsBusy = function() {
			return (busyref > 0);
		};

		$this.AddBusyQueueCallback = function(callback, callbackopts) {
			busyqueue.push({ callback: callback, callbackopts: callbackopts });

			$this.SetBusyRef(0);
		};

		// Internal function to only be used by FileExplorer.
		$this.ClearBusyQueueCallbacks = function() {
			busyqueue = [];
		};

		$this.GetPath = function() {
			return path;
		};

		$this.GetPathIDs = function() {
			var result = [];

			for (var x = 0; x < path.length; x++)  result.push(path[x][0]);

			return result;
		};

		// Sets an object containing optional attributes for the path.
		// Used primarily to disable some/all tools from functioning for specific folders.
		$this.SetAttributes = function(newattrs) {
			path[path.length - 1][2] = newattrs;

			DispatchEvent('set_attributes');
		};

		$this.SetAttribute = function(key, value) {
			path[path.length - 1][2][key] = value;

			DispatchEvent('set_attributes', key);
		};

		$this.GetAttributes = function() {
			return path[path.length - 1][2];
		};

		$this.SetAutoSort = function(newautosort) {
			autosort = (newautosort ? true : false);
		};

		$this.SortEntries = function() {
			if ($this.busy)
			{
				$this.busyqueue.push({ callback: $this.SortEntries, callbackopts: [] });

				return;
			}

			var localeopts = { numeric: true, sensitivity: 'base' };

			entries.sort(function(a, b) {
				if (a.type !== b.type)  return (a.type === 'folder' ? -1 : 1);

				return a.name.localeCompare(b.name, undefined, localeopts);
			});
		};

		// Sets an array of objects containing the folder entries.
		// Required per-item object keys:  id (unique string), name, type ('folder' or 'file'), hash (unique string).
		// Optional per-item object keys:  attrs, size, tooltip (tooltip string), thumb (thumbnail image URL), overlay (class name).
		$this.SetEntries = function(newentries) {
			if ($this.busy)
			{
				$this.busyqueue.push({ callback: $this.SetEntries, callbackopts: [newentries] });

				return;
			}

			entries = newentries;

			if (autosort)  $this.SortEntries();

			entryidmap = {};
			for (var x = 0; x < entries.length; x++)
			{
				entryidmap[entries[x].id] = x;
			}

			$this.waiting = false;

			DispatchEvent('set_entries');
		};

		// Creates/Updates multiple entries.
		$this.UpdateEntries = function(updatedentries) {
			if ($this.busy)
			{
				$this.busyqueue.push({ callback: $this.UpdateEntries, callbackopts: [updatedentries] });

				return;
			}

			for (var x = 0; x < updatedentries.length; x++)
			{
				var entry = updatedentries[x];

				if (!(entry.id in entryidmap))  entries.push(entry);
				else  entries[entryidmap[entry.id]] = entry;
			}

			if (autosort)  $this.SortEntries();

			entryidmap = {};
			for (var x = 0; x < entries.length; x++)
			{
				entryidmap[entries[x].id] = x;
			}

			$this.waiting = false;

			DispatchEvent('set_entries');
		};

		// Sets a single entry and triggers a full refresh.
		$this.SetEntry = function(entry) {
			if ($this.busy)
			{
				$this.busyqueue.push({ callback: $this.SetEntry, callbackopts: [entry] });

				return;
			}

			if (!(entry.id in entryidmap))  entries.push(entry);
			else  entries[entryidmap[entry.id]] = entry;

			if (autosort)  $this.SortEntries();

			entryidmap = {};
			for (var x = 0; x < entries.length; x++)
			{
				entryidmap[entries[x].id] = x;
			}

			$this.waiting = false;

			DispatchEvent('set_entries');
		};

		$this.RemoveEntry = function(id) {
			if ($this.busy)
			{
				$this.busyqueue.push({ callback: $this.RemoveEntry, callbackopts: [id] });

				return;
			}

			if (!(id in entryidmap))  return;

			var pos = entryidmap[id];

			delete entryidmap[id];

			entries.splice(pos, 1);

			for (var x = pos; x < entries.length; x++)
			{
				entryidmap[entries[x].id] = x;
			}

			DispatchEvent('remove_entry', pos);
		};

		$this.GetEntries = function() {
			return entries;
		};

		$this.GetEntryIDMap = function() {
			return entryidmap;
		};

		$this.Destroy = function() {
			DispatchEvent('destroy');

			triggers = {};
			entries = [];
			entryidmap = {};
			busyref = 0
			busyqueue = [];

			$this.lastrefresh = 0;
			$this.waiting = true;
			$this.refs = 0;

			$this = null;
			path = null;
		};
	};


	// Attaches a popup menu to the DOM.
	var PopupMenu = function(parentelem, options) {
		if (!(this instanceof PopupMenu))  return new PopupMenu(parentelem, options);

		var triggers = {};
		var $this = this;

		var defaults = {
			items: [],

			resizewatchers: null,

			onposition: null,
			onselchanged: null,
			onselected: null,
			oncancel: null,

			onleft: null,
			onright: null,

			ondestroy: null
		};

		$this.settings = Object.assign({}, defaults, options);

		// Initialize the UI elements.
		var elems = {
			popupwrap: CreateNode('div', ['fe_fileexplorer_popup_wrap'], { tabIndex: 0 }),
			innerwrap: CreateNode('div', ['fe_fileexplorer_popup_inner_wrap'])
		};

		// Track the last hovered/focused item.
		var lastitem = false, itemidmap = {};

		// Attach elements to DOM.
		for (var x = 0; x < $this.settings.items.length; x++)
		{
			var item = $this.settings.items[x];

			if (item === 'split')
			{
				var itemnode = CreateNode('div', ['fe_fileexplorer_popup_item_split']);

				elems.innerwrap.appendChild(itemnode);
			}
			else
			{
				var itemnode = CreateNode('div', ['fe_fileexplorer_popup_item_wrap'], { tabIndex: -1 });
				var itemicon = CreateNode('div', ['fe_fileexplorer_popup_item_icon']);
				var itemiconinner = CreateNode('div', ['fe_fileexplorer_popup_item_icon_inner']);
				var itemtext = CreateNode('div', ['fe_fileexplorer_popup_item_text']);
				var enabled = (!('enabled' in item) || item.enabled);

				if (!enabled)  itemnode.classList.add('fe_fileexplorer_popup_item_disabled');

				if ('icon' in item)  itemiconinner.classList.add(item.icon);

				itemtext.innerHTML = item.name;

				itemicon.appendChild(itemiconinner);
				itemnode.appendChild(itemicon);
				itemnode.appendChild(itemtext);

				itemnode.dataset.itemid = item.id;
				itemidmap[item.id] = item;

				elems.innerwrap.appendChild(itemnode);
			}
		}

		elems.popupwrap.appendChild(elems.innerwrap);

		parentelem.appendChild(elems.popupwrap);

		// Internal functions.
		var DispatchEvent = function(eventname, params) {
			if (!triggers[eventname])  return;

			triggers[eventname].forEach(function(callback) {
				if (Array.isArray(params))  callback.apply($this, params);
				else  callback.call($this, params);
			});
		};

		// Public DOM-style functions.
		$this.addEventListener = function(eventname, callback) {
			if (!triggers[eventname])  triggers[eventname] = [];

			for (var x in triggers[eventname])
			{
				if (triggers[eventname][x] === callback)  return;
			}

			triggers[eventname].push(callback);
		};

		$this.removeEventListener = function(eventname, callback) {
			if (!triggers[eventname])  return;

			for (var x in triggers[eventname])
			{
				if (triggers[eventname][x] === callback)
				{
					triggers[eventname].splice(x, 1);

					return;
				}
			}
		};

		$this.hasEventListener = function(eventname) {
			return (triggers[eventname] && triggers[eventname].length);
		};

		// Register settings callbacks.
		if ($this.settings.onposition)  $this.addEventListener('position', $this.settings.onposition);
		if ($this.settings.onselchanged)  $this.addEventListener('selection_changed', $this.settings.onselchanged);
		if ($this.settings.onselected)  $this.addEventListener('selected', $this.settings.onselected);
		if ($this.settings.oncancel)  $this.addEventListener('cancelled', $this.settings.oncancel);
		if ($this.settings.onleft)  $this.addEventListener('left', $this.settings.onleft);
		if ($this.settings.onright)  $this.addEventListener('right', $this.settings.onright);
		if ($this.settings.ondestroy)  $this.addEventListener('destroy', $this.settings.ondestroy);

		// Set up focus changing closing rules.
		var MainFocusHandler = function(e) {
			if (!e.isTrusted)  return;

			var node = e.target;
			while (node && node !== elems.popupwrap)  node = node.parentNode;

			if (node !== elems.popupwrap && allowcancel)
			{
				lastactiveelem = e.target;

				$this.Cancel(e.type === 'focus' ? 'focus' : 'mouse');
			}
		};

		window.addEventListener('mousedown', MainFocusHandler, true);
		window.addEventListener('focus', MainFocusHandler, true);

		var MainWindowBlurHander = function(e) {
			if (e.target === window || e.target === document)  $this.Cancel('blur');
		};

		window.addEventListener('blur', MainWindowBlurHander, true);

		// Track mouse movement to update the last hovered/focused item.
		var InnerWrapMoveHandler = function(e) {
			if (!e.isTrusted)  return;

			e.preventDefault();

			var node = e.target;
			while (node && node.parentNode !== elems.innerwrap)  node = node.parentNode;

			if (node && (lastitem !== node || lastitem !== document.activeElement))
			{
				if (node.classList.contains('fe_fileexplorer_popup_item_wrap'))
				{
					node.tabIndex = 0;
					node.focus();

					if (lastitem !== false)  lastitem.tabIndex = -1;

					if (lastitem !== node)  DispatchEvent('selection_changed', [node.dataset.itemid, itemidmap[node.dataset.itemid]]);

					lastitem = node;
				}
				else if (elems.popupwrap !== document.activeElement)
				{
					elems.popupwrap.focus();
				}
			}
		};

		elems.innerwrap.addEventListener('mousemove', InnerWrapMoveHandler);

		var InnerWrapLeaveHandler = function(e) {
			if (!e.isTrusted)  return;

			elems.popupwrap.focus();
		};

		elems.innerwrap.addEventListener('mouseleave', InnerWrapLeaveHandler);

		// Notify listeners that the last item was selected.
		var lastactiveelem = document.activeElement;
		var NotifySelected = function(etype) {
			allowcancel = false;

			DispatchEvent('selected', [itemidmap[lastitem.dataset.itemid].id, itemidmap[lastitem.dataset.itemid], lastactiveelem, etype]);
		};

		// Handle clicks.
		var MainClickHandler = function(e) {
			if (!e.isTrusted)  return;

			e.preventDefault();

			if (e.button == 0 && lastitem !== false && lastitem === document.activeElement && !lastitem.classList.contains('fe_fileexplorer_popup_item_disabled'))  NotifySelected('mouse');
		};

		elems.innerwrap.addEventListener('mouseup', MainClickHandler);

		var StopContextMenu = function(e) {
			if (!e.isTrusted)  return;

			e.preventDefault();
		};

		elems.innerwrap.addEventListener('contextmenu', StopContextMenu);

		// Handle keyboard navigation.
		var MainKeyHandler = function(e) {
			// The keyboard is modal while the mouse is not.  Stop propagation of all keyboard actions.
			e.stopPropagation();

			if (!e.isTrusted)  return;

			if (e.keyCode == 37)
			{
				// Left Arrow.  Send event to registered caller (if any).
				e.preventDefault();

				DispatchEvent('left', lastactiveelem);
			}
			else if (e.keyCode == 39)
			{
				// Right Arrow.  Send event to registered caller (if any).
				e.preventDefault();

				DispatchEvent('right', lastactiveelem);
			}
			else if (e.keyCode == 38)
			{
				// Up Arrow.  Move to previous or last item.
				e.preventDefault();

				var node = (lastitem === false ? elems.innerwrap.lastChild : lastitem.previousSibling);

				while (node && !node.classList.contains('fe_fileexplorer_popup_item_wrap'))  node = node.previousSibling;

				if (!node)  node = elems.innerwrap.lastChild;

				if (node)
				{
					node.tabIndex = 0;
					node.focus();

					if (lastitem !== false)  lastitem.tabIndex = -1;

					if (lastitem !== node)  DispatchEvent('selection_changed', [node.dataset.itemid, itemidmap[node.dataset.itemid]]);

					lastitem = node;
				}

				if (lastitem !== false)  lastitem.focus();
			}
			else if (e.keyCode == 40)
			{
				// Down Arrow.  Move to next or first item.
				e.preventDefault();

				var node = (lastitem === false ? elems.innerwrap.firstChild : lastitem.nextSibling);

				while (node && !node.classList.contains('fe_fileexplorer_popup_item_wrap'))  node = node.nextSibling;

				if (!node)  node = elems.innerwrap.firstChild;

				if (node)
				{
					node.tabIndex = 0;
					node.focus();

					if (lastitem !== false)  lastitem.tabIndex = -1;

					if (lastitem !== node)  DispatchEvent('selection_changed', [node.dataset.itemid, itemidmap[node.dataset.itemid]]);

					lastitem = node;
				}

				if (lastitem !== false)  lastitem.focus();
			}
			else if (e.keyCode == 13)
			{
				// Enter.  Select item or cancel the popup if the item is disabled.
				e.preventDefault();

				if (lastitem === false || lastitem !== document.activeElement || lastitem.classList.contains('fe_fileexplorer_popup_item_disabled'))  $this.Cancel('key');
				else  NotifySelected('key');
			}
			else if (e.keyCode == 27 || e.keyCode == 9 || e.altKey)
			{
				// Escape, Tab, or Alt.  Cancel the popup.
				e.preventDefault();

				$this.Cancel('key');
			}
		};

		elems.popupwrap.addEventListener('keydown', MainKeyHandler);

		var IgnoreKeyHandler = function(e) {
			e.stopPropagation();

			if (!e.isTrusted)  return;
		};

		elems.popupwrap.addEventListener('keyup', IgnoreKeyHandler);
		elems.popupwrap.addEventListener('keypress', IgnoreKeyHandler);


		// Public functions.

		// Updates the position of the popup menu.
		$this.UpdatePosition = function() {
			elems.popupwrap.style.left = '-9999px';

			DispatchEvent('position', elems.popupwrap);
		};

		$this.UpdatePosition();

		// Set up a debounced element attribute watcher on window resize.
		var updatepositionwatcher;
		if (Array.isArray($this.settings.resizewatchers) && $this.settings.resizewatchers.length)
		{
			updatepositionwatcher = new DebounceAttributes({
				watchers: $this.settings.resizewatchers,
				interval: 100,
				stopsame: 5,
				callback: $this.UpdatePosition,
				intervalcallback: $this.UpdatePosition
			});

			window.addEventListener('resize', updatepositionwatcher.Start, true);
		}

		// Dispatches the cancelled event.
		var allowcancel = false;
		$this.Cancel = function(etype) {
			if (allowcancel)
			{
				allowcancel = false;

				DispatchEvent('cancelled', [lastactiveelem, etype]);
			}
		};

		// Prevents Cancel() from having any effect.
		$this.PreventCancel = function() {
			allowcancel = false;
		};

		// Destroys the popup menu.
		$this.Destroy = function() {
			DispatchEvent('destroy');

			window.removeEventListener('mousedown', MainFocusHandler, true);
			window.removeEventListener('focus', MainFocusHandler, true);
			window.removeEventListener('blur', MainWindowBlurHander, true);

			elems.innerwrap.removeEventListener('mousemove', InnerWrapMoveHandler);
			elems.innerwrap.removeEventListener('mouseleave', InnerWrapLeaveHandler);
			elems.innerwrap.removeEventListener('mouseup', MainClickHandler);
			elems.innerwrap.removeEventListener('contextmenu', StopContextMenu);

			elems.popupwrap.removeEventListener('keydown', MainKeyHandler);
			elems.popupwrap.removeEventListener('keyup', IgnoreKeyHandler);
			elems.popupwrap.removeEventListener('keypress', IgnoreKeyHandler);

			if (Array.isArray($this.settings.resizewatchers) && $this.settings.resizewatchers.length)
			{
				window.removeEventListener('resize', updatepositionwatcher.Start, true);

				updatepositionwatcher.Destroy();
			}

			for (var node in elems)
			{
				if (elems[node].parentNode)  elems[node].parentNode.removeChild(elems[node]);
			}

			// Remaining cleanup.
			elems = null;
			lastactiveelem = null;

			$this.settings = Object.assign({}, defaults);

			$this = null;
			parentelem = null;
			options = null;
		};

		// Focus on the popup menu but do not select anything.
		elems.popupwrap.focus();
		allowcancel = true;
	};


	// Overlays a textarea placed into a parent element.
	var TextareaOverlay = function(parentelem, options) {
		if (!(this instanceof TextareaOverlay))  return new TextareaOverlay(parentelem, options);

		var triggers = {};
		var $this = this;

		var defaults = {
			capturetab: false,
			multiline: false,

			initvalue: '',
			initselstart: -1,
			initselend: -1,

			resizewatchers: null,

			onposition: null,
			ondone: null,
			oncancel: null,

			ondestroy: null
		};

		$this.settings = Object.assign({}, defaults, options);

		// Initialize the UI elements.
		var elems = {
			maintext: CreateNode('textarea', ['fe_fileexplorer_textarea'])
		};

		// Attach elements to DOM.
		elems.maintext.value = $this.settings.initvalue;

		parentelem.appendChild(elems.maintext);

		// Internal functions.
		var DispatchEvent = function(eventname, params) {
			if (!triggers[eventname])  return;

			triggers[eventname].forEach(function(callback) {
				if (Array.isArray(params))  callback.apply($this, params);
				else  callback.call($this, params);
			});
		};

		// Public DOM-style functions.
		$this.addEventListener = function(eventname, callback) {
			if (!triggers[eventname])  triggers[eventname] = [];

			for (var x in triggers[eventname])
			{
				if (triggers[eventname][x] === callback)  return;
			}

			triggers[eventname].push(callback);
		};

		$this.removeEventListener = function(eventname, callback) {
			if (!triggers[eventname])  return;

			for (var x in triggers[eventname])
			{
				if (triggers[eventname][x] === callback)
				{
					triggers[eventname].splice(x, 1);

					return;
				}
			}
		};

		$this.hasEventListener = function(eventname) {
			return (triggers[eventname] && triggers[eventname].length);
		};

		// Register settings callbacks.
		if ($this.settings.onposition)  $this.addEventListener('position', $this.settings.onposition);
		if ($this.settings.ondone)  $this.addEventListener('done', $this.settings.ondone);
		if ($this.settings.oncancel)  $this.addEventListener('cancelled', $this.settings.oncancel);
		if ($this.settings.ondestroy)  $this.addEventListener('destroy', $this.settings.ondestroy);

		// Set up focus changing closing rules.
		var MainFocusHandler = function(e) {
			if (!e.isTrusted)  return;

			var node = e.target;
			while (node && node !== elems.maintext)  node = node.parentNode;

			if (node !== elems.maintext && allowcanceldone)
			{
				lastactiveelem = e.target;

				$this.Done(e.type === 'focus' ? 'focus' : 'mouse');
			}
		};

		window.addEventListener('mousedown', MainFocusHandler, true);
		window.addEventListener('focus', MainFocusHandler, true);

		var MainWindowBlurHander = function(e) {
			if (e.target === window || e.target === document)  $this.Done('blur');
		};

		window.addEventListener('blur', MainWindowBlurHander, true);

		var lastactiveelem = document.activeElement;

		// Handle keyboard navigation.
		var MainKeyHandler = function(e) {
			// The keyboard is modal while the mouse is not.  Stop propagation of all keyboard actions.
			e.stopPropagation();

			if (!e.isTrusted)  return;

			if (e.keyCode == 8)
			{
				// Backspace.
				$this.UpdatePosition();
				setTimeout($this.UpdatePosition, 0);
			}
			if (e.keyCode == 46)
			{
				// Delete.
				$this.UpdatePosition();
				setTimeout($this.UpdatePosition, 0);
			}
			else if (e.keyCode == 9)
			{
				// Tab.
				e.preventDefault();

				if (!$this.settings.capturetab || e.shiftKey)  $this.Done('key');
				else
				{
					var pos = elems.maintext.selectionStart;
					elems.maintext.value = elems.maintext.value.substring(0, pos) + '\t' + elems.maintext.value.substring(elems.maintext.selectionEnd);
					elems.maintext.selectionEnd = pos + 1;

					$this.UpdatePosition();
					setTimeout($this.UpdatePosition, 0);
				}
			}
			else if (e.keyCode == 13)
			{
				// Enter.  Complete the entry if not multiline.
				if (!$this.settings.multiline)
				{
					e.preventDefault();

					$this.Done('key');
				}
			}
			else if (e.keyCode == 27)
			{
				// Escape.  Cancel the textarea.
				e.preventDefault();

				$this.Cancel('key');
			}
		};

		elems.maintext.addEventListener('keydown', MainKeyHandler);

		var MainKeypressHandler = function(e) {
			e.stopPropagation();

			$this.UpdatePosition();
		};

		elems.maintext.addEventListener('keyup', MainKeypressHandler);
		elems.maintext.addEventListener('keypress', MainKeypressHandler);


		// Public functions.

		// Updates the position of the textarea.
		$this.UpdatePosition = function() {
			elems.maintext.style.height = '1px';

			DispatchEvent('position', elems.maintext);
		};

		$this.UpdatePosition();

		// Set up a debounced element attribute watcher on window resize.
		var updatepositionwatcher;
		if (Array.isArray($this.settings.resizewatchers) && $this.settings.resizewatchers.length)
		{
			updatepositionwatcher = new DebounceAttributes({
				watchers: $this.settings.resizewatchers,
				interval: 100,
				stopsame: 5,
				callback: $this.UpdatePosition,
				intervalcallback: $this.UpdatePosition
			});

			window.addEventListener('resize', updatepositionwatcher.Start, true);
		}

		// Dispatches the done event if the content has changed.
		var allowcanceldone = false;
		$this.Done = function(etype) {
			if ($this.settings.initvalue === elems.maintext.value)  $this.Cancel(etype);
			else if (allowcanceldone)
			{
				allowcanceldone = false;
				elems.maintext.readOnly = true;

				DispatchEvent('done', [elems.maintext.value, lastactiveelem, etype]);
			}
		};

		// Dispatches the cancelled event.
		$this.Cancel = function(etype) {
			if (allowcanceldone)
			{
				allowcanceldone = false;
				elems.maintext.readOnly = true;

				DispatchEvent('cancelled', [lastactiveelem, etype]);
			}
		};

		// Resets the cancel/done status to true so another event can be dispatched.
		$this.ResetAllowCancelDone = function() {
			setTimeout(function() {
				elems.maintext.readOnly = false;
				elems.maintext.focus();

				allowcanceldone = true;
			}, 0);
		};

		// Destroys the textarea.
		$this.Destroy = function() {
			DispatchEvent('destroy');

			window.removeEventListener('mousedown', MainFocusHandler, true);
			window.removeEventListener('focus', MainFocusHandler, true);
			window.removeEventListener('blur', MainWindowBlurHander, true);

			elems.maintext.removeEventListener('keydown', MainKeyHandler);
			elems.maintext.removeEventListener('keyup', MainKeypressHandler);
			elems.maintext.removeEventListener('keypress', MainKeypressHandler);

			if (Array.isArray($this.settings.resizewatchers) && $this.settings.resizewatchers.length)
			{
				window.removeEventListener('resize', updatepositionwatcher.Start, true);

				updatepositionwatcher.Destroy();
			}

			for (var node in elems)
			{
				if (elems[node].parentNode)  elems[node].parentNode.removeChild(elems[node]);
			}

			// Remaining cleanup.
			elems = null;
			lastactiveelem = null;

			$this.settings = Object.assign({}, defaults);

			$this = null;
			parentelem = null;
			options = null;
		};

		// Focus on the textarea.
		elems.maintext.focus();
		elems.maintext.setSelectionRange(($this.settings.initselstart > -1 ? $this.settings.initselstart : elems.maintext.value.length), ($this.settings.initselend > -1 ? $this.settings.initselend : elems.maintext.value.length));
		allowcanceldone = true;
	};


	// File Explorer.
	var nextmain_id = 1, coretools = [];
	window.FileExplorer = function(parentelem, options) {
		if (!(this instanceof FileExplorer))  return new FileExplorer(parentelem, options);

		var triggers = {}, historystack = [], currhistory = -1, foldermap = {}, currfolder = false, destroyinprogress = false;
		var $this = this;

		// The internal ID needs to be fairly unique to identify source for clipboard paste and drag/drop targets.
		var main_id = nextmain_id + '_fileexplorer_js_' + Date.now() + '_' + (window.crypto && window.crypto.getRandomValues ? window.crypto.getRandomValues(new Uint32Array(1))[0] : Math.random());
		nextmain_id++;

		var defaults = {
			group: null,

			alwaysfocused: false,
			capturebrowser: false,

			messagetimeout: 2000,

			displayunits: 'iec_windows',
			adjustprecision: true,

			initpath: null,

			onfocus: null,
			onblur: null,

			onrefresh: null,
			onselchanged: null,

			onrename: null,
			onopenfile: null,
			oninitupload: null,
			onfinishedupload: null,
			onuploaderror: null,
			concurrentuploads: 4,

			tools: {},

			onnewfolder: null,
			onnewfile: null,
			oninitdownload: null,
			ondownloadstarted: null,
			ondownloaderror: null,

			ondownloadurl: null,

			oncopy: null,
			onmove: null,
			ondelete: null,

			langmap: {}
		};

		$this.settings = Object.assign({}, defaults, options);

		// If the group is not specified, set it to the unique main ID + the current time.
		var main_group = (typeof $this.settings.group === 'string' ? $this.settings.group : main_id);

		// Multilingual translation.
		$this.Translate = function(str) {
			return ($this.settings.langmap[str] ? $this.settings.langmap[str] : str);
		};

		// Initialize the UI elements.
		var elems = {
			mainwrap: CreateNode('div', ['fe_fileexplorer_wrap']),
			dropzonewrap: CreateNode('div', ['fe_fileexplorer_dropzone_wrap']),
			innerwrap: CreateNode('div', ['fe_fileexplorer_inner_wrap']),

			toolbar: CreateNode('div', ['fe_fileexplorer_toolbar']),
			navtools: CreateNode('div', ['fe_fileexplorer_navtools']),
			navtool_back: CreateNode('button', ['fe_fileexplorer_navtool_back', 'fe_fileexplorer_disabled'], { title: $this.Translate('Back (Alt + Left Arrow)'), tabIndex: -1 }),
			navtool_forward: CreateNode('button', ['fe_fileexplorer_navtool_forward', 'fe_fileexplorer_disabled'], { title: $this.Translate('Forward (Alt + Right Arrow)'), tabIndex: -1 }),
			navtool_history: CreateNode('button', ['fe_fileexplorer_navtool_history'], { title: $this.Translate('Recent locations') }),
			navtool_up: CreateNode('button', ['fe_fileexplorer_navtool_up', 'fe_fileexplorer_disabled'], { title: $this.Translate('Up (Alt + Up Arrow)'), tabIndex: -1 }),

			pathwrap: CreateNode('div', ['fe_fileexplorer_path_wrap']),
			pathicon: CreateNode('div', ['fe_fileexplorer_path_icon']),
			pathiconinner: CreateNode('div', ['fe_fileexplorer_path_icon_inner']),
			pathsegmentsscrollwrap: CreateNode('div', ['fe_fileexplorer_path_segments_scroll_wrap']),
			pathsegmentswrap: CreateNode('div', ['fe_fileexplorer_path_segments_wrap']),

			bodywrapouter: CreateNode('div', ['fe_fileexplorer_body_wrap_outer']),
			bodywrap: CreateNode('div', ['fe_fileexplorer_body_wrap']),

			bodytoolsscrollwrap: CreateNode('div', ['fe_fileexplorer_folder_tools_scroll_wrap', 'fe_fileexplorer_hidden']),
			bodytoolbar: CreateNode('div', ['fe_fileexplorer_folder_tools']),
			bodytools: [],

			itemsscrollwrap: CreateNode('div', ['fe_fileexplorer_items_scroll_wrap'], { tabIndex: 0 }),
			itemsscrollwrapinner: CreateNode('div', ['fe_fileexplorer_items_scroll_wrap_inner']),
			itemsmessagewrap: CreateNode('div', ['fe_fileexplorer_items_message_wrap']),
			itemswrap: CreateNode('div', ['fe_fileexplorer_items_wrap', 'fe_fileexplorer_hidden']),

			itemsclipboardoverlaypastewrap: CreateNode('div', ['fe_fileexplorer_items_clipboard_overlay_paste_wrap', 'fe_fileexplorer_hidden']),
			itemsclipboardoverlaypasteinnerwrap: CreateNode('div', ['fe_fileexplorer_items_clipboard_overlay_paste_inner_wrap']),
			itemsclipboardoverlaypastetextwrap: CreateNode('div', ['fe_fileexplorer_items_clipboard_overlay_paste_text_wrap']),
			itemsclipboardoverlaypastetext: CreateNode('div', ['fe_fileexplorer_items_clipboard_overlay_paste_text']),
			itemsclipboardoverlaypastetextline: CreateNode('div', ['fe_fileexplorer_items_clipboard_overlay_paste_text_big'], { innerHTML: $this.Translate('Paste here') }),
			itemsclipboardoverlaypastetexthint: CreateNode('div', ['fe_fileexplorer_items_clipboard_overlay_paste_text_small']),
			itemsclipboardoverlay: CreateNode('textarea', ['fe_fileexplorer_items_clipboard_overlay'], { tabIndex: -1, inputMode: 'none', autocomplete: 'off', autocorrect: 'off', autocapitalize: 'off', spellcheck: false }),

			statusbar: CreateNode('div', ['fe_fileexplorer_statusbar_wrap']),
			statusbarmeasuresize: CreateNode('div', ['fe_fileexplorer_statusbar_measure_em_size']),
			statusbartextwrap: CreateNode('div', ['fe_fileexplorer_statusbar_text_wrap']),
			statusbartextsegments: [],
			statusbartextsegmentmap: {},
			statusbaractionwrap: CreateNode('div', ['fe_fileexplorer_action_wrap']),
			statusbaractionprogresswrap: CreateNode('div', ['fe_fileexplorer_action_progress_wrap', 'fe_fileexplorer_hidden']),
			statusbaractionprogressmessagewrap: CreateNode('div', ['fe_fileexplorer_action_progress_msg_wrap']),
			statusbaractionprogressmessagewrap2: CreateNode('div', ['fe_fileexplorer_action_progress_msg_wrap', 'fe_fileexplorer_action_progress_msg_wrap_last']),
			statusbaractionprogresscancelwrap: CreateNode('div', ['fe_fileexplorer_action_progress_cancel_wrap'], { title: $this.Translate('Cancel all'), tabIndex: 0 }),
		};

		// Sets a text segment's displayed text in the status bar.
		$this.SetNamedStatusBarText = function(name, text, timeout) {
			if (destroyinprogress)  return;

			if (!(name in elems.statusbartextsegmentmap))
			{
				elems.statusbartextsegmentmap[name] = { pos: elems.statusbartextsegments.length, timeout: null };

				var node = CreateNode('div', ['fe_fileexplorer_statusbar_text_segment_wrap']);

				elems.statusbartextsegments.push(node);
				elems.statusbartextwrap.appendChild(node);
			}

			var currsegment = elems.statusbartextsegmentmap[name];

			if (currsegment.timeout)
			{
				clearTimeout(currsegment.timeout);

				currsegment.timeout = null;
			}

			var elem = elems.statusbartextsegments[currsegment.pos];

			if (text === '')
			{
				elem.innerHTML = '';
				elem.classList.add('fe_fileexplorer_hidden');
			}
			else
			{
				elem.innerHTML = text;
				elem.classList.remove('fe_fileexplorer_hidden');

				if (timeout)
				{
					elems.statusbartextsegmentmap[name].timeout = setTimeout(function() {
						$this.SetNamedStatusBarText(name, '');
					}, timeout);

					// Recalculate widths.
					var widthmap = [], totalwidth = 1.5 * elems.statusbarmeasuresize.offsetWidth;
					for (var x = 0; x < elems.statusbartextsegments.length; x++)
					{
						var elem2 = elems.statusbartextsegments[x];

						if (elem2.classList.contains('fe_fileexplorer_hidden'))  widthmap.push(0);
						else
						{
							var currstyle = elem2.currentStyle || window.getComputedStyle(elem2);
							var elemwidth = elem2.offsetWidth + parseFloat(currstyle.marginLeft) + parseFloat(currstyle.marginRight);

							widthmap.push(elemwidth);

							totalwidth += elemwidth;
						}
					}

					for (var x = elems.statusbartextsegments.length; totalwidth >= elems.statusbartextwrap.offsetWidth && x; x--)
					{
						if (widthmap[x - 1] && elem !== elems.statusbartextsegments[x - 1])
						{
							elems.statusbartextsegments[x - 1].classList.add('fe_fileexplorer_hidden');

							totalwidth -= widthmap[x - 1];
						}
					}
				}
			}

			// Adjust the last visible class.
			elem = null;
			elems.statusbartextsegments.forEach(function(elem2) {
				if (!timeout && elem2.innerHTML !== '')  elem2.classList.remove('fe_fileexplorer_hidden');

				if (!elem2.classList.contains('fe_fileexplorer_hidden'))
				{
					elem2.classList.remove('fe_fileexplorer_statusbar_text_segment_wrap_last');

					elem = elem2;
				}
			});

			if (elem)  elem.classList.add('fe_fileexplorer_statusbar_text_segment_wrap_last');
		};

		$this.SetNamedStatusBarText('folder', '');
		$this.SetNamedStatusBarText('selected', '');
		$this.SetNamedStatusBarText('message', '');

		elems.itemsmessagewrap.innerHTML = EscapeHTML($this.Translate('Loading...'));

		// Determine what text should show to the user when displaying the paste box.
		if (matchMedia('(pointer: coarse)').matches)  elems.itemsclipboardoverlaypastetexthint.innerHTML = EscapeHTML($this.Translate('Long-press + paste'));
		else if (navigator.platform.indexOf('Mac') > -1)  elems.itemsclipboardoverlaypastetexthint.innerHTML = EscapeHTML($this.Translate('\u2318 + V\u00A0\u00A0\u00A0/\u00A0\u00A0\u00A0Right-click + Paste'));
		else  elems.itemsclipboardoverlaypastetexthint.innerHTML = EscapeHTML($this.Translate('Ctrl + V\u00A0\u00A0\u00A0/\u00A0\u00A0\u00A0Right-click + Paste'));

		// Attach elements to DOM.
		elems.navtools.appendChild(elems.navtool_back);
		elems.navtools.appendChild(elems.navtool_forward);
		elems.navtools.appendChild(elems.navtool_history);
		elems.navtools.appendChild(elems.navtool_up);

		elems.pathicon.appendChild(elems.pathiconinner);
		elems.pathwrap.appendChild(elems.pathicon);

		elems.pathsegmentsscrollwrap.appendChild(elems.pathsegmentswrap);
		elems.pathwrap.appendChild(elems.pathsegmentsscrollwrap);

		elems.toolbar.appendChild(elems.navtools);
		elems.toolbar.appendChild(elems.pathwrap);

		elems.bodytoolsscrollwrap.appendChild(elems.bodytoolbar);
		elems.itemsscrollwrapinner.appendChild(elems.itemsmessagewrap);
		elems.itemsscrollwrapinner.appendChild(elems.itemswrap);
		elems.itemsscrollwrap.appendChild(elems.itemsscrollwrapinner);

		elems.itemsclipboardoverlaypastetext.appendChild(elems.itemsclipboardoverlaypastetextline);
		elems.itemsclipboardoverlaypastetext.appendChild(elems.itemsclipboardoverlaypastetexthint);
		elems.itemsclipboardoverlaypastetextwrap.appendChild(elems.itemsclipboardoverlaypastetext);
		elems.itemsclipboardoverlaypasteinnerwrap.appendChild(elems.itemsclipboardoverlaypastetextwrap);
		elems.itemsclipboardoverlaypasteinnerwrap.appendChild(elems.itemsclipboardoverlay);
		elems.itemsclipboardoverlaypastewrap.appendChild(elems.itemsclipboardoverlaypasteinnerwrap);

		elems.bodywrap.appendChild(elems.bodytoolsscrollwrap);
		elems.bodywrap.appendChild(elems.itemsscrollwrap);
		elems.bodywrapouter.appendChild(elems.bodywrap);
		elems.bodywrapouter.appendChild(elems.itemsclipboardoverlaypastewrap);

		elems.statusbaractionprogresswrap.appendChild(elems.statusbaractionprogressmessagewrap);
		elems.statusbaractionprogresswrap.appendChild(elems.statusbaractionprogressmessagewrap2);
		elems.statusbaractionprogresswrap.appendChild(elems.statusbaractionprogresscancelwrap);
		elems.statusbaractionwrap.appendChild(elems.statusbaractionprogresswrap);

		elems.statusbar.appendChild(elems.statusbarmeasuresize);
		elems.statusbar.appendChild(elems.statusbartextwrap);
		elems.statusbar.appendChild(elems.statusbaractionwrap);

		elems.innerwrap.appendChild(elems.toolbar);
		elems.innerwrap.appendChild(elems.bodywrapouter);
		elems.innerwrap.appendChild(elems.statusbar);
		elems.dropzonewrap.appendChild(elems.innerwrap);
		elems.mainwrap.appendChild(elems.dropzonewrap);

		parentelem.appendChild(elems.mainwrap);

		$this.SetNamedStatusBarText('folder', EscapeHTML($this.Translate('Loading...')));

		// Adjusts the status bar based on how large/small the mainwrap element is.
		var CalculateUpdateMultilineStatus = function() {
			if (elems.mainwrap.offsetWidth / elems.statusbarmeasuresize.offsetWidth < 58)  elems.statusbar.classList.add('fe_fileexplorer_statusbar_wrap_multiline');
			else  elems.statusbar.classList.remove('fe_fileexplorer_statusbar_wrap_multiline');
		};

		CalculateUpdateMultilineStatus();

		// Set up an offsetWidth attribute watcher that calls CalculateUpdateMultilineStatus.
		var statusbarresizewatch = new DebounceAttributes({
			watchers: [
				{ elem: elems.mainwrap, attr: 'offsetWidth', val: -1 }
			],
			interval: 50,
			stopsame: 5,
			callback: CalculateUpdateMultilineStatus,
			intervalcallback: CalculateUpdateMultilineStatus
		});

		window.addEventListener('resize', statusbarresizewatch.Start, true);

		// Internal DOM-style function.
		var DispatchEvent = function(eventname, params) {
			if (!triggers[eventname])  return;

			triggers[eventname].forEach(function(callback) {
				if (Array.isArray(params))  callback.apply($this, params);
				else  callback.call($this, params);
			});
		};

		// Public DOM-style functions.
		$this.addEventListener = function(eventname, callback) {
			if (!triggers[eventname])  triggers[eventname] = [];

			for (var x in triggers[eventname])
			{
				if (triggers[eventname][x] === callback)  return;
			}

			triggers[eventname].push(callback);
		};

		$this.removeEventListener = function(eventname, callback) {
			if (!triggers[eventname])  return;

			for (var x in triggers[eventname])
			{
				if (triggers[eventname][x] === callback)
				{
					triggers[eventname].splice(x, 1);

					return;
				}
			}
		};

		$this.hasEventListener = function(eventname) {
			return (triggers[eventname] && triggers[eventname].length);
		};

		// Dispatches a tool-specific event to listeners.
		$this.DispatchToolEvent = function(eventname, params) {
			DispatchEvent('tool_' + eventname, params);
		};

		// Public DOM-style functions for tools.
		$this.addToolEventListener = function(eventname, callback) {
			$this.addEventListener('tool_' + eventname, callback);
		};

		$this.removeToolEventListener = function(eventname, callback) {
			$this.removeEventListener('tool_' + eventname, callback);
		};

		$this.hasToolEventListener = function(eventname, callback) {
			return $this.hasEventListener('tool_' + eventname);
		};

		// Register settings callbacks.
		if ($this.settings.onfocus)  $this.addEventListener('focus', $this.settings.onfocus);
		if ($this.settings.onblur)  $this.addEventListener('blur', $this.settings.onblur);
		if ($this.settings.onrefresh)  $this.addEventListener('refresh_folder', $this.settings.onrefresh);
		if ($this.settings.onselchanged)  $this.addEventListener('selections_changed', $this.settings.onselchanged);
		if ($this.settings.onrename)  $this.addEventListener('rename', $this.settings.onrename);
		if ($this.settings.onopenfile)  $this.addEventListener('open_file', $this.settings.onopenfile);
		if ($this.settings.oninitupload)  $this.addEventListener('init_upload', $this.settings.oninitupload);
		if ($this.settings.onuploaderror)  $this.addEventListener('upload_error', $this.settings.onuploaderror);
		if ($this.settings.onfinishedupload)  $this.addEventListener('upload_done', $this.settings.onfinishedupload);
		if ($this.settings.ondownloadurl)  $this.addEventListener('get_download_url', $this.settings.ondownloadurl);
		if ($this.settings.oncopy)  $this.addEventListener('copy', $this.settings.oncopy);
		if ($this.settings.onmove)  $this.addEventListener('move', $this.settings.onmove);
		if ($this.settings.ondelete)  $this.addEventListener('delete', $this.settings.ondelete);

		// Capture browser-level back/forward buttons.  Alters browser history.
		var CapturePopStateHandler = function(e) {
			if (e.state && e.state._fileexplorer)
			{
				if (e.state._fileexplorer === 'back')
				{
					window.history.forward();

					$this.HistoryBack();
					$this.Focus(true);
				}
				else if (e.state._fileexplorer === 'forward')
				{
					window.history.back();

					$this.HistoryForward();
					$this.Focus(true);
				}
			}
		};

		// Sets up three history items and places the user in the middle of those three.
		var internalcapturerefs = 0;
		var CaptureMouseEnterHandler = function(e) {
			if (!capturingrefs)  prevscrollrestore = window.history.scrollRestoration;

			capturingrefs++;
			internalcapturerefs++;

			if (internalcapturerefs === 1)
			{
				window.history.scrollRestoration = 'manual';
				window.history.pushState({ _fileexplorer: 'back', _fileexplorerprevscroll: prevscrollrestore }, document.title);
				window.history.scrollRestoration = 'manual';
				window.history.pushState({ _fileexplorer: 'main' }, document.title);
				window.history.scrollRestoration = 'manual';
				window.history.pushState({ _fileexplorer: 'forward' }, document.title);
				window.history.scrollRestoration = 'manual';
				window.history.back();

				window.addEventListener('popstate', CapturePopStateHandler, true);
			}
		};

		// Restores the browser history as best as possible.
		var CaptureMouseLeaveHandler = function(e) {
			capturingrefs--;
			internalcapturerefs--;

			if (!internalcapturerefs)
			{
				window.removeEventListener('popstate', CapturePopStateHandler, true);

				if (window.history.state && window.history.state._fileexplorer)  window.history.back();
			}
		};

		if ($this.settings.capturebrowser)
		{
			elems.mainwrap.addEventListener('mouseenter', CaptureMouseEnterHandler);
			elems.mainwrap.addEventListener('mouseleave', CaptureMouseLeaveHandler);
		}

		// Handle main wrap focus.
		var MainWrapFocusMouseHandler = function(e) {
			elems.innerwrap.classList.add('fe_fileexplorer_inner_wrap_focused');

			var node = document.activeElement;
			while (node && node !== elems.mainwrap)  node = node.parentNode;

			if (node !== elems.mainwrap)  elems.itemsscrollwrap.focus();
		};

		elems.mainwrap.addEventListener('mousedown', MainWrapFocusMouseHandler);
		elems.mainwrap.addEventListener('mouseup', MainWrapFocusMouseHandler);
		elems.mainwrap.addEventListener('click', MainWrapFocusMouseHandler);

		// Set up focusing rules.
		if ($this.settings.alwaysfocused)  elems.innerwrap.classList.add('fe_fileexplorer_inner_wrap_focused');

		var hasfocus = false;
		var InnerWrapBlurHandler = function(e) {
			var node = e.target;
			while (node && node !== elems.mainwrap)  node = node.parentNode;

			if (node !== elems.mainwrap)
			{
				if (!$this.settings.alwaysfocused)  elems.innerwrap.classList.remove('fe_fileexplorer_inner_wrap_focused');

				if (hasfocus)  DispatchEvent('blur', e);

				hasfocus = false;
			}
		};

		window.addEventListener('mousedown', InnerWrapBlurHandler, true);

		// Trigger window blur visual appearance changes.
		var InnerWrapWindowBlurHandler = function(e) {
			if (e.target === window || e.target === document)
			{
				if (!$this.settings.alwaysfocused)  elems.innerwrap.classList.remove('fe_fileexplorer_inner_wrap_focused');
			}
		};

		window.addEventListener('blur', InnerWrapWindowBlurHandler, true);

		// When the tab key is pressed, adjust the focus.
		var FocusKeyHandler = function(e) {
			// Handle window-level focus events specially.  There will be another focus event if actually focused.
			if (e.target === window || e.target === document)
			{
				var node = document.activeElement;
				while (node && node !== elems.mainwrap)  node = node.parentNode;

				if (node === elems.mainwrap)  elems.innerwrap.classList.add('fe_fileexplorer_inner_wrap_focused');

				return;
			}

			var node = e.target;
			while (node && node !== elems.itemsscrollwrap && node !== elems.mainwrap)  node = node.parentNode;

			if (node === elems.itemsscrollwrap || e.target === elems.itemsclipboardoverlay)  elems.itemswrap.classList.add('fe_fileexplorer_items_focus');
			else  elems.itemswrap.classList.remove('fe_fileexplorer_items_focus');

			while (node && node !== elems.mainwrap)  node = node.parentNode;

			if (node === elems.mainwrap)
			{
				elems.innerwrap.classList.add('fe_fileexplorer_inner_wrap_focused');

				DispatchEvent('focus', e);

				hasfocus = true;
			}
			else
			{
				if (!$this.settings.alwaysfocused)  elems.innerwrap.classList.remove('fe_fileexplorer_inner_wrap_focused');

				if (hasfocus)  DispatchEvent('blur', e);

				hasfocus = false;
			}
		};

		window.addEventListener('focus', FocusKeyHandler, true);

		// If the device has a coarse pointer (e.g. touch), show checkboxes.
		if (matchMedia('(pointer: coarse)').matches)  elems.innerwrap.classList.add('fe_fileexplorer_show_item_checkboxes');

		// Toolbar button keyboard navigation.
		var ToolbarKeyHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.target.tagName === 'BUTTON')
			{
				if (e.keyCode == 38)
				{
					// Up arrow.
					var lastelem = null;
					for (var x = 0; x < elems.bodytools.length; x++)
					{
						if (elems.bodytools[x].tabIndex == 0)
						{
							if (!lastelem)  elems.bodytools[x].focus();
							else
							{
								e.preventDefault();

								lastelem.tabIndex = 0;
								lastelem.focus();
								elems.bodytools[x].tabIndex = -1;
							}

							break;
						}

						if (!elems.bodytools[x].classList.contains('fe_fileexplorer_disabled'))  lastelem = elems.bodytools[x];
					}
				}
				else if (e.keyCode == 40)
				{
					// Down arrow.
					for (var x = elems.bodytools.length; x; x--)
					{
						if (elems.bodytools[x - 1].tabIndex == 0)
						{
							if (!lastelem)  elems.bodytools[x - 1].focus();
							else
							{
								e.preventDefault();

								lastelem.tabIndex = 0;
								lastelem.focus();
								elems.bodytools[x - 1].tabIndex = -1;
							}

							break;
						}

						if (!elems.bodytools[x - 1].classList.contains('fe_fileexplorer_disabled'))  lastelem = elems.bodytools[x - 1];
					}
				}
			}
		};

		elems.bodytoolbar.addEventListener('keydown', ToolbarKeyHandler);

		var ToolbarToolFocusHandler = function(e) {
			var node = e.target;

			if (node.parentNode === elems.bodytoolbar)
			{
				if (node.offsetTop - 1 < elems.bodytoolsscrollwrap.scrollTop)  elems.bodytoolsscrollwrap.scrollTop = node.offsetTop - 1;
				else if (node.offsetTop + node.offsetHeight + 1 > elems.bodytoolsscrollwrap.scrollTop + elems.bodytoolsscrollwrap.clientHeight)  elems.bodytoolsscrollwrap.scrollTop = (node.offsetTop + node.offsetHeight + 1) - elems.bodytoolsscrollwrap.clientHeight;
			}
		};

		elems.bodytoolsscrollwrap.addEventListener('focus', ToolbarToolFocusHandler, true);

		var toolupdated = false;
		$this.ToolStateUpdated = function() {
			toolupdated = true;
		};

		var UpdateToolbarIcons = function() {
			toolupdated = false;

			DispatchEvent('update_tool', [currfolder, currfolder.GetAttributes()]);

			if (toolupdated)
			{
				// Find the tab-focus element.
				var found = false;
				for (var x = 0; x < elems.bodytools.length; x++)
				{
					if (elems.bodytools[x].tabIndex == 0)
					{
						// If the tool is disabled, attempt to find a nearby tool that isn't disabled and update the tab index.
						if (!elems.bodytools[x].classList.contains('fe_fileexplorer_disabled'))  found = true;
						else
						{
							for (var x2 = x; x2; x2--)
							{
								if (!elems.bodytools[x2 - 1].classList.contains('fe_fileexplorer_disabled'))
								{
									elems.bodytools[x2 - 1].tabIndex = 0;
									if (document.activeElement === elems.bodytools[x])  elems.bodytools[x2 - 1].focus();

									found = true;

									break;
								}
							}

							if (!found)
							{
								for (var x2 = x + 1; x2 < elems.bodytools.length; x2++)
								{
									if (!elems.bodytools[x2].classList.contains('fe_fileexplorer_disabled'))
									{
										found = true;

										elems.bodytools[x2].tabIndex = 0;
										if (document.activeElement === elems.bodytools[x])  elems.bodytools[x2].focus();

										break;
									}
								}
							}

							if (!found && document.activeElement === elems.bodytools[x])  $this.Focus(true);
							elems.bodytools[x].tabIndex = -1;
						}

						break;
					}
				}

				if (!found)
				{
					for (var x = 0; x < elems.bodytools.length; x++)
					{
						if (!elems.bodytools[x].classList.contains('fe_fileexplorer_disabled'))
						{
							elems.bodytools[x].tabIndex = 0;

							break;
						}
					}
				}
			}
		};


		var selecteditemsmap = {}, numselecteditems = 0, focuseditem = false, lastanchorpos = 0, popupmenu = null;

		// Clear selected items.
		$this.ClearSelectedItems = function(ignorebusy, skipuiupdate) {
			// If the current folder is busy, then queue the change for later.
			if (currfolder && currfolder.IsBusy() && !ignorebusy)
			{
				currfolder.AddBusyQueueCallback($this.ClearSelectedItems, [ignorebusy, skipuiupdate]);

				return;
			}

			if (!currfolder || currfolder.waiting)  return;

			// Clear selected.
			var node;
			for (var x in selecteditemsmap)
			{
				if (selecteditemsmap.hasOwnProperty(x))
				{
					node = elems.itemswrap.children[selecteditemsmap[x]];

					if (node)
					{
						node.classList.remove('fe_fileexplorer_item_selected');
						node.firstChild.firstChild.checked = false;
					}
				}
			}

			selecteditemsmap = {};
			numselecteditems = 0;

			if (!skipuiupdate)
			{
				// Update toolbar icons.
				UpdateToolbarIcons();

				// Update the status bar and notify listeners.
				UpdateSelectionsChanged();
			}
		};

		// Select all items.  Does not dispatch selection change events.
		$this.SelectAllItems = function(skipuiupdate) {
			// If the current folder is busy, then queue the change for later.
			if (currfolder && currfolder.IsBusy())
			{
				currfolder.AddBusyQueueCallback($this.SelectAllItems, [skipuiupdate]);

				return;
			}

			if (!currfolder || currfolder.waiting)  return;

			for (var x = 0; x < elems.itemswrap.children.length; x++)
			{
				var node = elems.itemswrap.children[x];

				if (!(node.dataset.feid in selecteditemsmap))
				{
					node.classList.add('fe_fileexplorer_item_selected');
					node.firstChild.firstChild.checked = true;

					selecteditemsmap[node.dataset.feid] = x;
				}
			}

			numselecteditems = elems.itemswrap.children.length;

			if (!skipuiupdate)
			{
				// Update toolbar icons.
				UpdateToolbarIcons();

				// Update the status bar and notify listeners.
				UpdateSelectionsChanged();
			}
		};

		// Toggles selection of a specific item.
		$this.ToggleItemSelection = function(elem, ignorebusy, skipuiupdate) {
			if (!currfolder || currfolder.waiting || (!ignorebusy && currfolder.IsBusy()))  return;

			if (typeof elem === 'string')
			{
				var entryidmap = currfolder.GetEntryIDMap();

				if (!(elem in entryidmap))  return;

				elem = elems.itemswrap.children[entryidmap[elem]];
			}

			if (elem.dataset.feid in selecteditemsmap)
			{
				elem.classList.remove('fe_fileexplorer_item_selected');
				elem.firstChild.firstChild.checked = false;

				delete selecteditemsmap[elem.dataset.feid];

				numselecteditems--;
			}
			else
			{
				var entryidmap = currfolder.GetEntryIDMap();
				if (elem.dataset.feid in entryidmap)
				{
					var entrynum = entryidmap[elem.dataset.feid];

					elem.classList.add('fe_fileexplorer_item_selected');
					elem.firstChild.firstChild.checked = true;

					selecteditemsmap[elem.dataset.feid] = entrynum;
					numselecteditems++;
				}
			}

			if (!skipuiupdate)
			{
				// Update toolbar icons.
				UpdateToolbarIcons();

				// Update the status bar and notify listeners.
				UpdateSelectionsChanged();
			}
		};

		// Selects all items from the last anchor to the focused item.
		$this.SelectItemsFromLastAnchor = function(ignorebusy, skipuiupdate) {
			if (!currfolder || currfolder.waiting || (!ignorebusy && currfolder.IsBusy()))  return;

			if (focuseditem === false)  return;

			var entryidmap = currfolder.GetEntryIDMap();
			var entrynum = entryidmap[focuseditem.dataset.feid];

			$this.ClearSelectedItems(ignorebusy, true);

			var pos = lastanchorpos;
			var pos2 = entrynum;

			if (pos > pos2)
			{
				var pos3 = pos;
				pos = pos2;
				pos2 = pos3;
			}

			for (; pos <= pos2; pos++)
			{
				var elem = elems.itemswrap.children[pos];

				elem.classList.add('fe_fileexplorer_item_selected');
				elem.firstChild.firstChild.checked = true;

				selecteditemsmap[elem.dataset.feid] = pos;
				numselecteditems++;
			}

			if (!skipuiupdate)
			{
				// Update toolbar icons.
				UpdateToolbarIcons();

				// Update the status bar and notify listeners.
				UpdateSelectionsChanged();
			}
		};

		// Sets the item that has focus.
		$this.SetFocusItem = function(id, updateanchor) {
			if (!currfolder || currfolder.waiting)  return;

			var node = null;
			if (typeof id === 'string')
			{
				var entryidmap = currfolder.GetEntryIDMap();

				if (id in entryidmap)
				{
					node = elems.itemswrap.children[entryidmap[id]];

					if (node)
					{
						node.classList.add('fe_fileexplorer_item_focused');
						node.firstChild.tabIndex = 0;
						node.firstChild.focus();

						if (updateanchor)  lastanchorpos = entryidmap[id];
					}
				}
			}

			if (focuseditem !== false && focuseditem !== node)
			{
				focuseditem.classList.remove('fe_fileexplorer_item_focused');
				focuseditem.firstChild.tabIndex = -1;

				focuseditem = false;
			}

			if (node)  focuseditem = node;
		};

		// Scrolls the view so the focused item is fully viewable.
		$this.ScrollToFocusedItem = function() {
			if (focuseditem !== false)
			{
				if (focuseditem.offsetTop - 1 < elems.itemsscrollwrap.scrollTop)  elems.itemsscrollwrap.scrollTop = focuseditem.offsetTop - 1;
				else if (focuseditem.offsetTop + focuseditem.offsetHeight + 1 > elems.itemsscrollwrap.scrollTop + elems.itemsscrollwrap.clientHeight)  elems.itemsscrollwrap.scrollTop = (focuseditem.offsetTop + focuseditem.offsetHeight + 1) - elems.itemsscrollwrap.clientHeight;
			}
		};

		// Opens selected items.
		$this.OpenSelectedItems = function() {
			if (!currfolder || currfolder.waiting || currfolder.IsBusy())  return;

			var entries = currfolder.GetEntries();
			var selnums = [];
			var numfolders = 0, folderentry = null;

			for (var x in selecteditemsmap)
			{
				if (selecteditemsmap.hasOwnProperty(x))  selnums.push(selecteditemsmap[x]);
			}

			selnums.sort(function(a, b) { return (a < b ? -1 : 1); });

			for (var x = 0; x < selnums.length; x++)
			{
				var entry = entries[selnums[x]];

				if (entry.type === 'folder')
				{
					folderentry = entry;

					numfolders++;
				}
				else
				{
					DispatchEvent('open_file', [currfolder, entry]);
				}
			}

			if (numfolders === 1)
			{
				$this.Focus(true);

				var newpath = currfolder.GetPath().slice();

				// Append the new path segment.
				var pathitem = [folderentry.id, folderentry.name];
				if ('attrs' in folderentry)  pathitem.push(folderentry.attrs);

				newpath.push(pathitem);

				$this.SetPath(newpath);
			}
		};

		// Adjusts images in the thumbnail loading queue.
		var queuedthumbs = {}, queuedthumbfailed = {}, queuedthumbfolder, queuedthumbstartrow, queuedthumbendrow;

		var ThumbnailDisplayHandler = function(opts, success) {
			if (queuedthumbfolder !== currfolder)  return;

			if (!success)  queuedthumbfailed[opts.src] = true;
			else
			{
				var entries = currfolder.GetEntries();
				var entryidmap = currfolder.GetEntryIDMap();

				if ((opts.id in queuedthumbs) && (queuedthumbs[opts.id] in entryidmap))
				{
					var pos = entryidmap[queuedthumbs[opts.id]];
					var node = elems.itemswrap.children[pos].firstChild.firstChild.nextSibling;

					node.className = 'fe_fileexplorer_item_icon fe_fileexplorer_item_icon_img';
					node.appendChild(opts.img);

					entries[pos].thumb = false;
				}
			}
		};

		var ThumbnailQueueUpdate = function() {
			UpdateCurrFolderItemCache(false);

			// Clear the thumbnail queue if the folder changed since the last call.
			if (queuedthumbfolder !== currfolder)
			{
				if (queuedthumbfolder)  DecrementMappedFolderRefCount(queuedthumbfolder);

				for (var x in queuedthumbs)
				{
					if (queuedthumbs.hasOwnProperty(x))
					{
						fe_thumbnailloader.RemoveFromQueue(x);

						delete queuedthumbs[x];
					}
				}

				queuedthumbfailed = {};

				queuedthumbfolder = currfolder;
				queuedthumbfolder.refs++;

				queuedthumbstartrow = 0;
				queuedthumbendrow = (folderitemcache.rows.length ? folderitemcache.rows.length - 1 : 0);
			}

			// Remove non-active items and removed folder entries from the thumbnail queue.
			var entryidmap = currfolder.GetEntryIDMap();
			for (var x in queuedthumbs)
			{
				if (!fe_thumbnailloader.IsActive(x) || !(queuedthumbs[x] in entryidmap))
				{
					fe_thumbnailloader.RemoveFromQueue(x);

					delete queuedthumbs[x];
				}
			}

			if (!folderitemcache.size)  return;

			// Calculate the new start and end row item cache positions.
			var miny = elems.itemsscrollwrap.scrollTop;
			var maxy = miny + elems.itemsscrollwrap.offsetHeight;

			// Adjust start and end row until they fall within two tops.
			while (queuedthumbstartrow && (queuedthumbstartrow > folderitemcache.rows.length - 1 || miny < folderitemcache.rows[queuedthumbstartrow].top))  queuedthumbstartrow--;
			while (queuedthumbstartrow < folderitemcache.rows.length - 1 && miny >= folderitemcache.rows[queuedthumbstartrow + 1].top)  queuedthumbstartrow++;

			while (queuedthumbendrow && (queuedthumbendrow > folderitemcache.rows.length - 1 || maxy < folderitemcache.rows[queuedthumbendrow].top))  queuedthumbendrow--;
			if (queuedthumbendrow < queuedthumbstartrow)  queuedthumbendrow = queuedthumbstartrow;
			while (queuedthumbendrow < folderitemcache.rows.length - 1 && maxy >= folderitemcache.rows[queuedthumbendrow + 1].top)  queuedthumbendrow++;

			// Add items to the thumbnail queue.
			var entries = currfolder.GetEntries();
			var y = (queuedthumbendrow + 1) * folderitemcache.cols.length;
			if (y > entries.length)  y = entries.length;
			for (var x = queuedthumbstartrow * folderitemcache.cols.length; x < y; x++)
			{
				if (entries[x].thumb && (typeof entries[x].thumb !== 'string' || !queuedthumbfailed[entries[x].thumb]))
				{
					// Build the thumbnail queue options.
					if (typeof entries[x].thumb === 'string')
					{
						entries[x].thumb = {
							src: entries[x].thumb,
							callback: ThumbnailDisplayHandler
						};
					}

					fe_thumbnailloader.AddToQueue(entries[x].thumb);

					queuedthumbs[entries[x].thumb.id] = entries[x].id;
				}
			}

			fe_thumbnailloader.ProcessQueue();
		};

		// Set up a scrollTop/clientWidth attribute watcher that calls ThumbnailQueueUpdate after 10 identical scrollTop and clientWidth values over a period of 500ms.
		var thumbnailscrollwatch = new DebounceAttributes({
			watchers: [
				{ elem: elems.itemsscrollwrap, attr: 'scrollTop', val: -1 },
				{ elem: elems.itemsscrollwrapinner, attr: 'clientWidth', val: -1 }
			],
			interval: 50,
			stopsame: 10,
			callback: ThumbnailQueueUpdate
		});

		elems.itemsscrollwrap.addEventListener('scroll', thumbnailscrollwatch.Start);
		window.addEventListener('resize', thumbnailscrollwatch.Start, true);

		// Track the position information of each item in the current folder.
		var folderitemcache;
		var UpdateCurrFolderItemCache = function(forcerefresh) {
			if (!forcerefresh && folderitemcache && folderitemcache.lastinnerwidth === elems.itemsscrollwrapinner.clientWidth && folderitemcache.size === elems.itemswrap.children.length)  return;

			folderitemcache = {
				lastinnerwidth: elems.itemsscrollwrapinner.clientWidth,
				size: elems.itemswrap.children.length,
				cols: [],
				rows: []
			};

			if (!folderitemcache.size)  return;

			var node = elems.itemswrap.firstChild;
			var basey = node.firstChild.offsetTop;
			var currrow = { top: basey, bottoms: [] };
			while (node)
			{
				var childnode = node.firstChild;

				// Calculate column boundaries of the items in the first row.
				if (childnode.offsetTop === basey)  folderitemcache.cols.push({ left: childnode.offsetLeft, right: childnode.offsetLeft + childnode.offsetWidth });

				// Calculate row boundaries of each item.
				if (childnode.offsetTop !== currrow.top)
				{
					folderitemcache.rows.push(currrow);

					currrow = { top: childnode.offsetTop, bottoms: [] };
				}

				currrow.bottoms.push(currrow.top + childnode.offsetHeight);

				node = node.nextSibling;
			}

			if (currrow.bottoms.length)  folderitemcache.rows.push(currrow);
		};

		// Update the selected items status bar and notify selection change listeners.
		var UpdateSelectionsChanged = function() {
			// Calculate the total size for all selected items.  Set the last selected item as well.
			var totalsize = 0, numfound = 0, sizestr, entries = currfolder.GetEntries();
			historystack[currhistory].lastselected = false;
			for (var x in selecteditemsmap)
			{
				if (selecteditemsmap.hasOwnProperty(x))
				{
					if (numselecteditems == 1)  historystack[currhistory].lastselected = x;

					if ('size' in entries[selecteditemsmap[x]])
					{
						totalsize += entries[selecteditemsmap[x]].size;
						numfound++;
					}
				}
			}

			if (numfound)  sizestr = GetDisplayFilesize(totalsize, $this.settings.adjustprecision, $this.settings.displayunits);

			// Update the status bar.
			if (numselecteditems == 0)  $this.SetNamedStatusBarText('selected', '');
			else if (numselecteditems > 1)
			{
				if (numfound)  $this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate('{0} items selected {1}'), numselecteditems, sizestr)));
				else  $this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate('{0} items selected'), numselecteditems)));
			}
			else
			{
				if (numfound)  $this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate('1 item selected {0}'), sizestr)));
				else  $this.SetNamedStatusBarText('selected', EscapeHTML($this.Translate('1 item selected')));
			}

			// Notify selection change listeners.
			DispatchEvent('selections_changed', [currfolder, selecteditemsmap, numselecteditems]);
		};

		// Rare update attributes callback.  Just updates tools for now.
		var SetFolderAttributesHandler = function() {
			// Update toolbar icons.
			UpdateToolbarIcons();
		};

		// Efficiently synchronizes the current folder entries to the DOM.
		var SyncCurrFolderToDOM = function() {
			var entries = currfolder.GetEntries();

			// Create a mapping from ids to existing DOM nodes.
			var x, elemmap = {};
			var nodes = elems.itemswrap.children;
			for (x = 0; x < nodes.length; x++)
			{
				elemmap[nodes[x].dataset.feid] = [x, nodes[x].dataset.fehash, nodes[x], false];
			}

			// If moved forward to an earlier folder, select the subfolder item ID.
			if (currhistory > 0 && currhistory === historystack.length - 1 && historystack[currhistory].lastselected === true)
			{
				var currkey = historystack[currhistory].folderkeys[historystack[currhistory].folderkeys.length - 1];

				for (x = 0; x < historystack[currhistory - 1].folderkeys.length - 1; x++)
				{
					if (currkey === historystack[currhistory - 1].folderkeys[x])
					{
						var temppath = foldermap[historystack[currhistory - 1].folderkeys[x + 1]].GetPath();

						historystack[currhistory].lastselected = temppath[temppath.length - 1][0];

						break;
					}
				}
			}

			// Skip any starting matching nodes.
			var node, historyselected = false, selchanged = false;
			for (x = 0; x < entries.length && elemmap[entries[x].id] && entries[x].hash === elemmap[entries[x].id][1]; x++)
			{
				node = elemmap[entries[x].id][2];

				elemmap[entries[x].id][3] = true;

				// Select item if it matches last selection.
				if (!selchanged && historystack[currhistory].lastselected === node.dataset.feid && !(node.dataset.feid in selecteditemsmap))
				{
					node.classList.add('fe_fileexplorer_item_selected');
					node.firstChild.firstChild.checked = true;

					selecteditemsmap[node.dataset.feid] = x;
					numselecteditems++;

					historyselected = true;
					selchanged = true;
				}
			}

			var tempscroll = elems.itemsscrollwrap.scrollTop;

			// Append new nodes and update existing nodes that have changed.
			for (; x < entries.length; x++)
			{
				var itemicon, itemtext;

				if (entries[x].id in elemmap)
				{
					// Found an existing item.
					node = elemmap[entries[x].id][2];
					elemmap[entries[x].id][3] = true;

					itemicon = node.firstChild.children[1];
					itemtext = node.firstChild.lastChild;
				}
				else
				{
					// Create a new item.
					node = CreateNode('div', ['fe_fileexplorer_item_wrap']);
					var iteminner = CreateNode('div', ['fe_fileexplorer_item_wrap_inner'], { tabIndex: -1, draggable: true });
					var itemcheckbox = CreateNode('input', ['fe_fileexplorer_item_checkbox'], { type: 'checkbox', tabIndex: -1 });

					itemicon = CreateNode('div', ['fe_fileexplorer_item_icon']);
					itemtext = CreateNode('div', ['fe_fileexplorer_item_text']);

					iteminner.appendChild(itemcheckbox);
					iteminner.appendChild(itemicon);
					iteminner.appendChild(itemtext);

					node.appendChild(iteminner);

					node.dataset.feid = entries[x].id;
					node.dataset.fehash = '';
				}

				// Select item if it matches last selection.
				if (!selchanged && historystack[currhistory].lastselected === node.dataset.feid && !(node.dataset.feid in selecteditemsmap))
				{
					node.classList.add('fe_fileexplorer_item_selected');
					node.firstChild.firstChild.checked = true;

					selecteditemsmap[node.dataset.feid] = x;
					numselecteditems++;

					historyselected = true;
					selchanged = true;
				}

				// Update the node.
				if (entries[x].hash !== node.dataset.fehash)
				{
					itemicon.className = 'fe_fileexplorer_item_icon';
					delete itemicon.dataset.ext;

					if (entries[x].type === 'folder')
					{
						node.classList.add('fe_fileexplorer_item_folder');

						itemicon.classList.add('fe_fileexplorer_item_icon_folder');
					}
					else
					{
						itemicon.classList.add('fe_fileexplorer_item_icon_file');

						var ext = entries[x].name;
						var pos = ext.lastIndexOf('.');
						if (pos < 0)  itemicon.classList.add('fe_fileexplorer_item_icon_file_no_ext');
						else
						{
							ext = ext.substring(pos + 1).toUpperCase();

							itemicon.dataset.ext = ext.substring(0, 4);

							if (ext === '')  itemicon.classList.add('fe_fileexplorer_item_icon_file_no_ext');
							else
							{
								var cc = ext.charCodeAt(0);

								if ((cc >= 48 && cc < 58) || (cc >= 64 && cc < 91))  itemicon.classList.add('fe_fileexplorer_item_icon_ext_' + ext.substring(0, 1).toLowerCase());
							}
						}
					}

					node.firstChild.className = 'fe_fileexplorer_item_wrap_inner';

					if ('overlay' in entries[x])
					{
						if (typeof entries[x].overlay === 'string')  entries[x].overlay = [entries[x].overlay];

						for (var x2 = 0; x2 < entries[x].overlay.length; x2++)  node.firstChild.classList.add(entries[x].overlay[x2]);
					}

					if ('tooltip' in entries[x])  node.firstChild.title = entries[x].tooltip;
					else  node.firstChild.title = '';

					itemtext.innerHTML = EscapeHTML(entries[x].name);

					node.dataset.fehash = entries[x].hash;
				}

				// Move node to the end of the list so it ends up in the correct order.
				elems.itemswrap.appendChild(node);
			}

			// Remove deleted nodes.
			for (var id in elemmap)
			{
				if (elemmap.hasOwnProperty(id) && !elemmap[id][3])
				{
					if (elemmap[id][2].dataset.feid in selecteditemsmap)
					{
						delete selecteditemsmap[elemmap[id][2].dataset.feid];

						numselecteditems--;
						selchanged = true;
					}

					if (focuseditem === elemmap[id][2])
					{
						if ($this.HasFocus(true))  elems.itemsscrollwrap.focus();

						focuseditem.classList.remove('fe_fileexplorer_item_focused');
						focuseditem.firstChild.tabIndex = -1;

						focuseditem = false;
					}

					elemmap[id][2].parentNode.removeChild(elemmap[id][2]);
				}
			}

			elems.itemsscrollwrap.scrollTop = tempscroll;

			// Finalize the synchronization operation.
			FinalizeSyncCurrFolderToDOM(historyselected, selchanged);
		};

		var FinalizeSyncCurrFolderToDOM = function(historyselected, selchanged) {
			var entries = currfolder.GetEntries();
			var entryidmap = currfolder.GetEntryIDMap();

			// Fix selection items map.
			for (var x in selecteditemsmap)
			{
				if (selecteditemsmap.hasOwnProperty(x) && (x in entryidmap))  selecteditemsmap[x] = entryidmap[x];
			}

			// Update the main area.
			if (entries.length)
			{
				elems.itemsmessagewrap.classList.add('fe_fileexplorer_hidden');
				elems.itemswrap.classList.remove('fe_fileexplorer_hidden');
			}
			else
			{
				if (currfolder.waiting)  elems.itemsmessagewrap.innerHTML = EscapeHTML($this.Translate('Loading...'));
				else  elems.itemsmessagewrap.innerHTML = EscapeHTML($this.Translate('This folder is empty.'));

				elems.itemsmessagewrap.classList.remove('fe_fileexplorer_hidden');
				elems.itemswrap.classList.add('fe_fileexplorer_hidden');
			}

			// Update the folder item position cache.
			UpdateCurrFolderItemCache(true);

			// Set the focus item and scroll to it.
			if (historyselected)
			{
				$this.SetFocusItem(historystack[currhistory].lastselected, true);
				$this.ScrollToFocusedItem();
			}
			else if (focuseditem !== false)
			{
				$this.SetFocusItem(focuseditem.dataset.feid, false);
			}

			// Trigger thumbnail queue update.
			ThumbnailQueueUpdate();

			// Update the status bar.
			if (currfolder.waiting)  $this.SetNamedStatusBarText('folder', EscapeHTML($this.Translate('Loading...')));
			else  $this.SetNamedStatusBarText('folder', EscapeHTML(FormatStr($this.Translate('{0} items'), entries.length)));

			// Update toolbar icons.
			UpdateToolbarIcons();

			// If selections changed, update the status bar and notify listeners.
			if (selchanged)  UpdateSelectionsChanged();
		};

		// Set up handlers for current folder entry changes.
		var SetFolderEntriesHandler = function() {
			if (this === currfolder)  SyncCurrFolderToDOM();
		};

		var RemoveFolderEntryHandler = function(pos) {
			var node = elems.itemswrap.children[pos];
			var selchanged = false;

			if (node.dataset.feid in selecteditemsmap)
			{
				delete selecteditemsmap[node.dataset.feid];

				numselecteditems--;
				selchanged = true;
			}

			if (focuseditem === node)
			{
				if ($this.HasFocus(true))  elems.itemsscrollwrap.focus();

				focuseditem.classList.remove('fe_fileexplorer_item_focused');
				focuseditem.firstChild.tabIndex = -1;

				focuseditem = false;
			}

			var tempscroll = elems.itemsscrollwrap.scrollTop;

			node.parentNode.removeChild(node);

			elems.itemsscrollwrap.scrollTop = tempscroll;

			// Finalize the synchronization operation.
			FinalizeSyncCurrFolderToDOM(false, selchanged);
		};

		var ConvertVertToHorzScroll = function(e) {
			var mult = (e.deltaMode == 1 ? scrolllineheight * 2 : (e.deltaMode == 2 ? document.documentElement.clientHeight - (2 * scrolllineheight) : 1));
			if (e.deltaY)  e.currentTarget.scrollLeft += e.deltaY * mult;

			// Only viable option is to completely prevent scrolling.  Very strange behavior occurs otherwise in all browsers.
			if (e.currentTarget.scrollWidth > e.currentTarget.clientWidth)  e.preventDefault();
		};

		elems.pathsegmentsscrollwrap.addEventListener('wheel', ConvertVertToHorzScroll);

		// Set the current path.
		$this.IsValidPath = function(path) {
			if (!path || !Array.isArray(path) || !path.length)  return false;

			for (var x = 0; x < path.length; x++)
			{
				if (!Array.isArray(path[x]) || path[x].length < 2 || typeof path[x][0] !== 'string' || typeof path[x][1] !== 'string')  return false;
			}

			return true;
		};

		$this.RefreshFolders = function(forcecurrfolder) {
			if (forcecurrfolder)  currfolder.lastrefresh = 0;

			var historyentry = historystack[currhistory];
			var ts = Date.now();
			var ts2 = ts - 300 * 1000;

			for (var x = historyentry.folderkeys.length; x; x--)
			{
				if (foldermap[historyentry.folderkeys[x - 1]].lastrefresh < ts2)
				{
					DispatchEvent('refresh_folder', [foldermap[historyentry.folderkeys[x - 1]], !foldermap[historyentry.folderkeys[x - 1]].lastrefresh]);

					foldermap[historyentry.folderkeys[x - 1]].lastrefresh = ts;
				}
			}
		};

		// Update navigation and toolabar icons.
		var NavigationChanged = function() {
			// Back button.
			if (currhistory <= 0)
			{
				if (document.activeElement === elems.navtool_back)
				{
					if (currhistory >= historystack.length - 1)  elems.navtool_history.focus();
					else
					{
						elems.navtool_forward.tabIndex = 0;
						elems.navtool_forward.focus();
					}
				}

				elems.navtool_back.classList.add('fe_fileexplorer_disabled');
				elems.navtool_back.tabIndex = -1;

				elems.navtool_back.title = $this.Translate('Back (Alt + Left Arrow)');
			}
			else
			{
				elems.navtool_back.classList.remove('fe_fileexplorer_disabled');
				elems.navtool_back.tabIndex = 0;

				var prevpath = foldermap[historystack[currhistory - 1].folderkeys[historystack[currhistory - 1].folderkeys.length - 1]].GetPath();

				elems.navtool_back.title = FormatStr($this.Translate('Back to "{0}" (Alt + Left Arrow)'), prevpath[prevpath.length - 1][1]);
			}

			// Forward button.
			if (currhistory >= historystack.length - 1)
			{
				if (document.activeElement === elems.navtool_forward)
				{
					if (currhistory <= 0)  elems.navtool_history.focus();
					else  elems.navtool_back.focus();
				}

				elems.navtool_forward.classList.add('fe_fileexplorer_disabled');
				elems.navtool_forward.tabIndex = -1;

				elems.navtool_forward.title = $this.Translate('Forward (Alt + Right Arrow)');
			}
			else
			{
				elems.navtool_forward.classList.remove('fe_fileexplorer_disabled');
				elems.navtool_forward.tabIndex = 0;

				var nextpath = foldermap[historystack[currhistory + 1].folderkeys[historystack[currhistory + 1].folderkeys.length - 1]].GetPath();

				elems.navtool_forward.title = FormatStr($this.Translate('Forward to "{0}" (Alt + Right Arrow)'), nextpath[nextpath.length - 1][1]);
			}

			// Up button.
			var currpath = currfolder.GetPath();

			if (currpath.length <= 1)
			{
				if (document.activeElement === elems.navtool_up)  elems.navtool_history.focus();

				elems.navtool_up.classList.add('fe_fileexplorer_disabled');
				elems.navtool_up.tabIndex = -1;

				elems.navtool_up.title = $this.Translate('Up (Alt + Up Arrow)');
			}
			else
			{
				elems.navtool_up.classList.remove('fe_fileexplorer_disabled');
				elems.navtool_up.tabIndex = 0;

				elems.navtool_up.title = FormatStr($this.Translate('Up to "{0}" (Alt + Up Arrow)'), currpath[currpath.length - 2][1]);
			}

			DispatchEvent('navigated');

			// Update toolbar icons.
			UpdateToolbarIcons();
		};

		var NavToolsKeyHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.keyCode == 37)
			{
				// Left Arrow.  Move to previous nav tool.
				e.preventDefault();

				if (document.activeElement && document.activeElement.parentNode === elems.navtools)
				{
					var node = document.activeElement.previousSibling;
					while (node && node.classList.contains('fe_fileexplorer_disabled'))  node = node.previousSibling;

					if (node)  node.focus();
				}
			}
			else if (e.keyCode == 39)
			{
				// Right Arrow.  Move to next nav tool.
				e.preventDefault();

				if (document.activeElement && document.activeElement.parentNode === elems.navtools)
				{
					var node = document.activeElement.nextSibling;
					while (node && node.classList.contains('fe_fileexplorer_disabled'))  node = node.nextSibling;

					if (node)  node.focus();
				}
			}
			else if (e.keyCode == 40)
			{
				// Down Arrow.  Focus on the history tool and open it.
				e.preventDefault();

				elems.navtool_history.focus();

				RecentLocationsHandler(e);
			}
		};

		elems.navtools.addEventListener('keydown', NavToolsKeyHandler);

		// Returns a path key for the folder map.
		var GetMappedPathKey = function(path) {
			// Build the path key.
			var pathkey = '';

			for (var x = 0; x < path.length; x++)
			{
				pathkey += '/' + path[x][0];
			}

			return pathkey;
		};

		// Attempts to return a mapped folder from a calculated path.
		$this.GetMappedFolderFromPath = function(path) {
			return foldermap[GetMappedPathKey(path)];
		};

		var DecrementMappedFolderRefCount = function(folder) {
			folder.refs--;

			if (!folder.refs)
			{
				var pathkey = GetMappedPathKey(folder.GetPath());

				folder.Destroy();

				delete foldermap[pathkey];
			}
		};

		$this.GetPathIDs = function(path) {
			var result = [];

			for (var x = 0; x < path.length; x++)  result.push(path[x][0]);

			return result;
		};

		$this.SetPath = function(newpath) {
			// If the current folder is busy, then queue the change for later.
			if (currfolder && currfolder.IsBusy())
			{
				currfolder.AddBusyQueueCallback($this.SetPath, [newpath]);

				return;
			}

			if (!$this.IsValidPath(newpath))  return;

			// Cancel any active popup menu.
			if (popupmenu)  popupmenu.Cancel();

			// Unregister events for the current folder.
			if (currfolder)
			{
				currfolder.removeEventListener('set_attributes', SetFolderAttributesHandler);
				currfolder.removeEventListener('set_entries', SetFolderEntriesHandler);
				currfolder.removeEventListener('remove_entry', RemoveFolderEntryHandler);
			}

			// Clear existing DOM path segments.
			while (elems.pathsegmentswrap.firstChild)  elems.pathsegmentswrap.removeChild(elems.pathsegmentswrap.lastChild);

			// Calculate path keys for a new history stack entry.
			var historyentry = { folderkeys: [], lastselected: true };
			var pathkey = '';

			for (var x = 0; x < newpath.length; x++)
			{
				// Create/Update folder cache entries.
				pathkey += '/' + newpath[x][0];

				if (!foldermap[pathkey])  foldermap[pathkey] = new Folder(newpath.slice(0, x + 1));

				foldermap[pathkey].refs++;

				historyentry.folderkeys.push(pathkey);

				// Create new DOM path segment.
				var segmentwrap = CreateNode('div', ['fe_fileexplorer_path_segment_wrap'], { tabIndex: (x < newpath.length - 1 ? -1 : 0) });
				var segmentpathname = CreateNode('button', ['fe_fileexplorer_path_name'], { tabIndex: -1 });
				var segmentpathopts = CreateNode('button', ['fe_fileexplorer_path_opts'], { tabIndex: -1 });

				segmentwrap._fepos = x;

				segmentpathname.innerHTML = EscapeHTML(newpath[x][1]);

				segmentwrap.appendChild(segmentpathname);
				segmentwrap.appendChild(segmentpathopts);

				elems.pathsegmentswrap.appendChild(segmentwrap);
			}

			// Scroll the path segment scroll view to the end.
			elems.pathsegmentsscrollwrap.scrollLeft = elems.pathsegmentsscrollwrap.scrollWidth;
			elems.pathsegmentswrap._fepos = newpath.length - 1;

			// Register events for the new current folder.
			var prevfolder = currfolder;
			currfolder = foldermap[pathkey];
			currfolder.addEventListener('set_attributes', SetFolderAttributesHandler);
			currfolder.addEventListener('set_entries', SetFolderEntriesHandler);
			currfolder.addEventListener('remove_entry', RemoveFolderEntryHandler);

			// Clear selected and focused items if the folder is the same.
			if (prevfolder === currfolder)
			{
				$this.ClearSelectedItems(false, true);
				$this.SetFocusItem(false, false);
			}

			// Scroll view to top.
			elems.itemsscrollwrap.scrollTop = 0;

			// Force a refresh and clear selections and focus.
			currfolder.lastrefresh = 0;
			selecteditemsmap = {};
			numselecteditems = 0;
			focuseditem = false;
			lastanchorpos = 0;

			// Clear DOM items if the folder changed.
			if (prevfolder !== currfolder)
			{
				while (elems.itemswrap.firstChild)
				{
					if (document.activeElement === elems.itemswrap.lastChild.firstChild)  elems.itemsscrollwrap.focus();

					elems.itemswrap.removeChild(elems.itemswrap.lastChild);
				}
			}

			// Adjust history stack.
			if (currhistory < 0 || pathkey !== historystack[currhistory].folderkeys[historystack[currhistory].folderkeys.length - 1])
			{
				// Clear any subsequent history stack entries.
				currhistory++;
				for (var x = currhistory; x < historystack.length; x++)
				{
					for (var x2 = 0; x2 < historystack[x].folderkeys.length; x2++)
					{
						DecrementMappedFolderRefCount(foldermap[historystack[x].folderkeys[x2]]);
					}
				}

				historystack = historystack.slice(0, currhistory);

				// Create a new history stack entry.
				historystack.push(historyentry);

				DispatchEvent('history_changed');
			}
			else if (currhistory > -1)
			{
				// Decrement folder references for the current path.
				for (var x = 0; x < historystack[currhistory].folderkeys.length; x++)
				{
					DecrementMappedFolderRefCount(foldermap[historystack[currhistory].folderkeys[x]]);
				}
			}

			// Save last selected item.
			var lastselected = historystack[currhistory].lastselected;

			// Create/Update DOM items.
			SyncCurrFolderToDOM();

			// Update the status bar and notify listeners.
			if (!numselecteditems)  UpdateSelectionsChanged();

			// Restore last selected item.
			historystack[currhistory].lastselected = lastselected;

			// Update folders that haven't been refreshed in the last 5 minutes.
			$this.RefreshFolders(true);

			// Notify navigation completed.
			NavigationChanged();
		};


		// Handle mouse and touch selections for the current folder.
		var selectanchorpos = null, prevselectrect = null, selectbox = null, selectchangeinvert = false, autoscrolltimer = null, lastmouseevent = null;
		var lastselecttouch = null, lastmousedownevent = null, selectmodemulti = false;

		// Updates the specified rectangle with start/end row/column numbers from the folder item cache.  The hint start/end row/column info is optional.
		var UpdateCalculatedSelectedItemsRect = function(rect, hintrect) {
			rect.startrow = (hintrect ? hintrect.startrow : 0);
			rect.startcol = (hintrect ? hintrect.startcol : 0);
			rect.endrow = (hintrect ? hintrect.endrow : (folderitemcache.rows.length ? folderitemcache.rows.length - 1 : 0));
			rect.endcol = (hintrect ? hintrect.endcol : (folderitemcache.rows.length ? folderitemcache.cols.length - 1 : 0));

			// Adjust startrow and endrow until they fall within two tops.
			while (rect.startrow && rect.top < folderitemcache.rows[rect.startrow].top)  rect.startrow--;
			while (rect.startrow < folderitemcache.rows.length - 1 && rect.top >= folderitemcache.rows[rect.startrow + 1].top)  rect.startrow++;

			while (rect.endrow && rect.bottom < folderitemcache.rows[rect.endrow].top)  rect.endrow--;
			if (rect.endrow < rect.startrow)  rect.endrow = rect.startrow;
			while (rect.endrow < folderitemcache.rows.length - 1 && rect.bottom >= folderitemcache.rows[rect.endrow + 1].top)  rect.endrow++;

			// Adjust startcol and endcol until they fall within two lefts.
			while (rect.startcol && rect.left < folderitemcache.cols[rect.startcol].left)  rect.startcol--;
			while (rect.startcol < folderitemcache.cols.length - 1 && rect.left >= folderitemcache.cols[rect.startcol + 1].left)  rect.startcol++;

			while (rect.endcol && rect.right < folderitemcache.cols[rect.endcol].left)  rect.endcol--;
			if (rect.endcol < rect.startcol)  rect.endcol = rect.startcol;
			while (rect.endcol < folderitemcache.cols.length - 1 && rect.right >= folderitemcache.cols[rect.endcol + 1].left)  rect.endcol++;
		};

		var DoesRectOverlapItemRect = function(rect, x, y) {
			return (folderitemcache.size && rect.left < folderitemcache.cols[x].right && rect.right >= folderitemcache.cols[x].left && rect.bottom >= folderitemcache.rows[y].top && rect.top < folderitemcache.rows[y].bottoms[x]);
		};

		// Updates information and selected items for SelectBoxDragHandler().
		var UpdateSelectBoxDragInfoItems = function(currselectrect, newpos, newwidth, newheight, scrolling) {
			if (!scrolling)  currselectrect.left = (newpos.x < selectanchorpos.x ? newpos.x : selectanchorpos.x);
			currselectrect.top = (newpos.y < selectanchorpos.y ? newpos.y : selectanchorpos.y);
			if (!scrolling)  currselectrect.right = currselectrect.left + newwidth;
			currselectrect.bottom = currselectrect.top + newheight;

			// Calculate rough position info.
			UpdateCalculatedSelectedItemsRect(currselectrect, prevselectrect);

			if (!scrolling)  selectbox.style.left = currselectrect.left + 'px';
			selectbox.style.top = currselectrect.top + 'px';
			if (!scrolling)  selectbox.style.width = newwidth + 'px';
			selectbox.style.height = newheight + 'px';

			// Apply item selection changes.
			var updateitems = {}, selchanged = false;
			if (!scrolling)
			{
				var minrow = (currselectrect.startrow < prevselectrect.startrow ? currselectrect.startrow : prevselectrect.startrow);
				var maxrow = (currselectrect.endrow > prevselectrect.endrow ? currselectrect.endrow : prevselectrect.endrow);

				if (currselectrect.left < prevselectrect.left)
				{
					for (var y = minrow; y <= maxrow; y++)
					{
						for (var x = currselectrect.startcol; x <= prevselectrect.startcol; x++)
						{
							if (!DoesRectOverlapItemRect(prevselectrect, x, y) && DoesRectOverlapItemRect(currselectrect, x, y))
							{
								updateitems[y * folderitemcache.cols.length + x] = true;

								selchanged = true;
							}
						}
					}
				}
				else if (currselectrect.left > prevselectrect.left)
				{
					for (var y = minrow; y <= maxrow; y++)
					{
						for (var x = prevselectrect.startcol; x <= currselectrect.startcol; x++)
						{
							if (DoesRectOverlapItemRect(prevselectrect, x, y) && !DoesRectOverlapItemRect(currselectrect, x, y))
							{
								updateitems[y * folderitemcache.cols.length + x] = false;

								selchanged = true;
							}
						}
					}
				}

				if (currselectrect.right > prevselectrect.right)
				{
					for (var y = minrow; y <= maxrow; y++)
					{
						for (var x = prevselectrect.endcol; x <= currselectrect.endcol; x++)
						{
							if (!DoesRectOverlapItemRect(prevselectrect, x, y) && DoesRectOverlapItemRect(currselectrect, x, y))
							{
								updateitems[y * folderitemcache.cols.length + x] = true;

								selchanged = true;
							}
						}
					}
				}
				else if (currselectrect.right < prevselectrect.right)
				{
					for (var y = minrow; y <= maxrow; y++)
					{
						for (var x = currselectrect.endcol; x <= prevselectrect.endcol; x++)
						{
							if (DoesRectOverlapItemRect(prevselectrect, x, y) && !DoesRectOverlapItemRect(currselectrect, x, y))
							{
								updateitems[y * folderitemcache.cols.length + x] = false;

								selchanged = true;
							}
						}
					}
				}
			}

			var mincol = (currselectrect.startcol < prevselectrect.startcol ? currselectrect.startcol : prevselectrect.startcol);
			var maxcol = (currselectrect.endcol > prevselectrect.endcol ? currselectrect.endcol : prevselectrect.endcol);

			if (currselectrect.top < prevselectrect.top)
			{
				for (var y = currselectrect.startrow; y <= prevselectrect.startrow; y++)
				{
					for (var x = mincol; x <= maxcol; x++)
					{
						if (!DoesRectOverlapItemRect(prevselectrect, x, y) && DoesRectOverlapItemRect(currselectrect, x, y))
						{
							updateitems[y * folderitemcache.cols.length + x] = true;

							selchanged = true;
						}
					}
				}
			}
			else if (currselectrect.top > prevselectrect.top)
			{
				for (var y = prevselectrect.startrow; y <= currselectrect.startrow; y++)
				{
					for (var x = mincol; x <= maxcol; x++)
					{
						if (DoesRectOverlapItemRect(prevselectrect, x, y) && !DoesRectOverlapItemRect(currselectrect, x, y))
						{
							updateitems[y * folderitemcache.cols.length + x] = false;

							selchanged = true;
						}
					}
				}
			}

			if (currselectrect.bottom > prevselectrect.bottom)
			{
				for (var y = prevselectrect.endrow; y <= currselectrect.endrow; y++)
				{
					for (var x = mincol; x <= maxcol; x++)
					{
						if (!DoesRectOverlapItemRect(prevselectrect, x, y) && DoesRectOverlapItemRect(currselectrect, x, y))
						{
							updateitems[y * folderitemcache.cols.length + x] = true;

							selchanged = true;
						}
					}
				}
			}
			else if (currselectrect.bottom < prevselectrect.bottom)
			{
				for (var y = currselectrect.endrow; y <= prevselectrect.endrow; y++)
				{
					for (var x = mincol; x <= maxcol; x++)
					{
						if (DoesRectOverlapItemRect(prevselectrect, x, y) && !DoesRectOverlapItemRect(currselectrect, x, y))
						{
							updateitems[y * folderitemcache.cols.length + x] = false;

							selchanged = true;
						}
					}
				}
			}

			// Update items.
			if (selchanged)
			{
				for (var x in updateitems)
				{
					if (updateitems.hasOwnProperty(x))
					{
						var elem = elems.itemswrap.children[x];

						if (selectchangeinvert)
						{
							// Invert the selection.
							if (elem.dataset.feid in selecteditemsmap)
							{
								elem.classList.remove('fe_fileexplorer_item_selected');
								elem.firstChild.firstChild.checked = false;

								delete selecteditemsmap[elem.dataset.feid];

								numselecteditems--;
							}
							else
							{
								elem.classList.add('fe_fileexplorer_item_selected');
								elem.firstChild.firstChild.checked = true;

								selecteditemsmap[elem.dataset.feid] = x;
								numselecteditems++;
							}
						}
						else if (updateitems[x])
						{
							// Add the selection.
							elem.classList.add('fe_fileexplorer_item_selected');
							elem.firstChild.firstChild.checked = true;

							selecteditemsmap[elem.dataset.feid] = x;
							numselecteditems++;
						}
						else
						{
							// Remove the selection.
							elem.classList.remove('fe_fileexplorer_item_selected');
							elem.firstChild.firstChild.checked = false;

							delete selecteditemsmap[elem.dataset.feid];

							numselecteditems--;
						}
					}
				}

				// Update toolbar icons.
				UpdateToolbarIcons();

				// Update the status bar and notify listeners.
				UpdateSelectionsChanged();
			}

			Object.assign(prevselectrect, currselectrect);
		};

		// Resize, autoscroll, and select highlighted items using a selection box.
		var SelectBoxDragHandler = function(e) {
			if (!e.isTrusted)  return;

			// Perform our own much smoother scrolling and avoid item selections.
			e.preventDefault();

			lastmouseevent = e;

			var rect = elems.itemsscrollwrapinner.getBoundingClientRect();

			var newpos = {
				x: e.clientX - rect.left,
				y: e.clientY - rect.top
			};

			if (newpos.x < 0)  newpos.x = 0;
			if (newpos.x > rect.width)  newpos.x = rect.width;
			if (newpos.y < 0)  newpos.y = 0;
			if (newpos.y > rect.height)  newpos.y = rect.height;

			var newwidth = Math.abs(newpos.x - selectanchorpos.x);
			var newheight = Math.abs(newpos.y - selectanchorpos.y);

			if (!selectbox && (newwidth > 8 || newheight > 8))
			{
				selectbox = CreateNode('div', ['fe_fileexplorer_select_box']);
				elems.itemsscrollwrapinner.appendChild(selectbox);
			}

			if (selectbox)
			{
				if (e.ctrlKey)  selectchangeinvert = true;
				else if (e.shiftKey)  selectchangeinvert = false;

				var currselectrect = {};

				// Update information and selected items.
				UpdateSelectBoxDragInfoItems(currselectrect, newpos, newwidth, newheight, false);

				// Handle scrolling of the view.
				var rect2 = elems.itemsscrollwrap.getBoundingClientRect();

				if (autoscrolltimer)
				{
					clearInterval(autoscrolltimer);

					autoscrolltimer = null;
				}

				if (e.clientY < rect2.top)
				{
					// Scroll up.
					var scrollspeed = Math.floor((rect2.top - e.clientY) / 10) + 1;

					var TempScrollUp = function(e) {
						elems.itemsscrollwrap.scrollTop -= scrollspeed;

						newpos.y -= scrollspeed;
						if (newpos.y < 0)  newpos.y = 0;

						newheight = Math.abs(newpos.y - selectanchorpos.y);

						// Update information and selected items.
						UpdateSelectBoxDragInfoItems(currselectrect, newpos, newwidth, newheight, true);

						if (elems.itemsscrollwrap.scrollTop <= 0)
						{
							clearInterval(autoscrolltimer);

							autoscrolltimer = null;
						}
					};

					autoscrolltimer = setInterval(TempScrollUp, 10);

					TempScrollUp();
				}
				else if (e.clientY > rect2.bottom)
				{
					// Scroll down.
					var scrollspeed = (Math.floor((e.clientY - rect2.bottom) / 10) + 1);

					var TempScrollDown = function(e) {
						elems.itemsscrollwrap.scrollTop += scrollspeed;

						newpos.y += scrollspeed;
						if (newpos.y > rect.height)  newpos.y = rect.height;

						newheight = Math.abs(newpos.y - selectanchorpos.y);

						// Update information and selected items.
						UpdateSelectBoxDragInfoItems(currselectrect, newpos, newwidth, newheight, true);

						if (elems.itemsscrollwrap.scrollTop >= elems.itemsscrollwrap.scrollHeight - elems.itemsscrollwrap.clientHeight)
						{
							clearInterval(autoscrolltimer);

							autoscrolltimer = null;
						}
					};

					autoscrolltimer = setInterval(TempScrollDown, 10);

					TempScrollDown();
				}
			}
		};

		// Handle scrolling using the wheel while selecting items.
		var SelectBoxScrollWheelHandler = function(e) {
			if (!e.isTrusted)  return;

			var lastscrolltop = -1;
			var numsame = 0;

			var TempWheelScrollHandler = function() {
				SelectBoxDragHandler(lastmouseevent);

				if (autoscrolltimer)  clearInterval(autoscrolltimer);

				autoscrolltimer = setInterval(TempWheelScrollHandler, 10);

				if (lastscrolltop !== elems.itemsscrollwrap.scrollTop)  numsame = 0;
				else
				{
					numsame++;

					if (numsame >= 5)
					{
						clearInterval(autoscrolltimer);

						autoscrolltimer = null;
					}
				}

				lastscrolltop = elems.itemsscrollwrap.scrollTop;
			};

			TempWheelScrollHandler();
		};

		// Handle starting a clipboard operation.
		var clipboardmenutimout, clipboardcontextmenu;
		var ClipboardOverlayKeyHandler = function(e) {
			// If the context menu key was pressed, don't change focus until the menu has appeared, otherwise change focus now.
			if (!e.ctrlKey && !e.metaKey && e.keyCode != 93)
			{
				ClipboardOverlayExitContextMenuHandler(e);
			}
		};

		var ClipboardOverlayExitContextMenuHandler = function(e) {
			// Clean up event handlers.
			window.removeEventListener('focus', ClipboardOverlayExitContextMenuHandler, true);
			elems.itemsclipboardoverlay.removeEventListener('keyup', ClipboardOverlayKeyHandler);
			window.removeEventListener('mousedown', ClipboardOverlayExitContextMenuHandler, true);
			elems.itemsclipboardoverlay.removeEventListener('input', ClipboardOverlayExitContextMenuHandler, true);
			elems.itemsclipboardoverlay.removeEventListener('select', ClipboardOverlayExitContextMenuHandler, true);
			window.removeEventListener('keydown', ClipboardPasteBoxKeyHandler, true);
			window.removeEventListener('mousedown', ClipboardPasteBoxMouseHandler, true);

			if (clipboardmenutimout)
			{
				clearTimeout(clipboardmenutimout);
				clipboardmenutimout = null;
			}

			// Move the focus back to the main area if the target is the clipboard overlay.
			if (e && e.target === elems.itemsclipboardoverlay)  $this.Focus(true, true);

			elems.itemsclipboardoverlaypastewrap.classList.add('fe_fileexplorer_hidden');
			elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_items_show_clipboard_overlay_paste');
			elems.itemsclipboardoverlay.tabIndex = -1;

			clipboardcontextmenu = false;
		};

		var ClipboardOverlayContextMenuHandler = function(e) {
			// Remove the pointer events class after the context menu shows BUT there is no standard event available for it after this one.
			if (clipboardmenutimout)  clearTimeout(clipboardmenutimout);

			clipboardmenutimout = setTimeout(function() {
				clipboardmenutimout = null;

				elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_items_clipboard_contextmenu');

				elems.itemsclipboardoverlay.addEventListener('input', ClipboardOverlayExitContextMenuHandler, true);
				elems.itemsclipboardoverlay.addEventListener('select', ClipboardOverlayExitContextMenuHandler, true);
			}, 0);

			// Track when the context menu exits.
			window.addEventListener('focus', ClipboardOverlayExitContextMenuHandler, true);
			elems.itemsclipboardoverlay.addEventListener('keyup', ClipboardOverlayKeyHandler);
			window.addEventListener('mousedown', ClipboardOverlayExitContextMenuHandler, true);

			// Remove the event handler for the context menu.
			window.removeEventListener('contextmenu', ClipboardOverlayContextMenuHandler, true);

			clipboardcontextmenu = true;
		};

		var StartClipboardOverlayMenu = function() {
			if (elems.itemsclipboardoverlaypastewrap.classList.contains('fe_fileexplorer_items_clipboard_contextmenu'))
			{
				// Temporarily enable an event handler for opening a context menu.
				window.addEventListener('contextmenu', ClipboardOverlayContextMenuHandler, true);

				elems.itemsclipboardoverlay.focus();
				elems.itemsclipboardoverlay.setSelectionRange((numselecteditems ? 1 : 2), 2);
			}
		};

		var ClipboardPasteBoxKeyHandler = function(e) {
			elems.itemsclipboardoverlay.value = '   ';
			elems.itemsclipboardoverlay.setSelectionRange(2, 2);

			if (e.keyCode == 27)  ClipboardOverlayExitContextMenuHandler(e);
		};

		var ClipboardPasteBoxMouseHandler = function(e) {
			if (e.target !== elems.itemsclipboardoverlay)  ClipboardOverlayExitContextMenuHandler(e);
		};

		$this.ShowClipboardPasteBox = function() {
			elems.itemsclipboardoverlaypastewrap.classList.add('fe_fileexplorer_items_show_clipboard_overlay_paste');
			elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_hidden');
			elems.itemsclipboardoverlay.tabIndex = 0;

			window.addEventListener('keydown', ClipboardPasteBoxKeyHandler, true);
			window.addEventListener('mousedown', ClipboardPasteBoxMouseHandler, true);
		};

		$this.HideClipboardPasteBox = function(e) {
			ClipboardOverlayExitContextMenuHandler(e);
		};

		// Stop selecting items, clears event handlers, and decrements busy state.
		var SelectBoxEndHandler = function(e) {
			if (selectbox)
			{
				selectbox.parentNode.removeChild(selectbox);
				selectbox = null;

				clearInterval(autoscrolltimer);
				autoscrolltimer = null;
			}

			elems.itemswrap.classList.remove('fe_fileexplorer_items_selecting');

			// Disable clipboard overlay.
			StartClipboardOverlayMenu();

			window.removeEventListener('mousemove', SelectBoxDragHandler, true);
			window.removeEventListener('mouseup', SelectBoxEndHandler, true);
			window.removeEventListener('blur', SelectBoxEndHandler, true);
			elems.itemsscrollwrap.removeEventListener('wheel', SelectBoxScrollWheelHandler);

			currfolder.SetBusyRef(-1);
		};

		// Handle rename start from click.
		var startrename = false, startrenamefolder, startrenameid, startrenametimeout;
		var StartRenameHandler = function() {
			startrenametimeout = null;

			CancelRenameHandler();

			if (startrenamefolder === currfolder && !currfolder.IsBusy() && numselecteditems === 1 && (startrenameid in selecteditemsmap))  $this.RenameSelectedItem();
		};

		var CancelRenameHandler = function(e) {
			window.removeEventListener('touchstart', CancelRenameHandler, true);
			window.removeEventListener('mousedown', CancelRenameHandler, true);
			window.removeEventListener('keydown', CancelRenameHandler, true);

			if (startrenametimeout)
			{
				clearTimeout(startrenametimeout);
				startrenametimeout = null;
			}
		};

		// Scrolls the main view if the focused item is released before a move/copy operation starts.
		var scrollnomoveinfo = null;
		var ScrollNoMoveHandler = function(e) {
			e.preventDefault();

			if (scrollnomoveinfo)
			{
				if (scrollnomoveinfo.origevent.button == 2)
				{
					// Ignore selection changes since the right-click context menu will be showing in a moment.
				}
				else if (scrollnomoveinfo.origevent.ctrlKey || scrollnomoveinfo.origevent.target.tagName === 'INPUT' || selectmodemulti)
				{
					// Toggle item selection.
					$this.ToggleItemSelection(scrollnomoveinfo.origelem, true);
				}
				else if (!scrollnomoveinfo.origevent.shiftKey)
				{
					// Select items starting at the last anchor position.
					$this.SelectItemsFromLastAnchor(true);
				}

				if (!numselecteditems)  selectmodemulti = false;
				else if (lastselecttouch && scrollnomoveinfo.origevent.target.tagName === 'INPUT')  selectmodemulti = true;

				scrollnomoveinfo = null;
			}

			$this.ScrollToFocusedItem();

			window.removeEventListener('mouseup', ScrollNoMoveHandler, true);

			StartClipboardOverlayMenu();

			// Rename the selected item if the user started the selection on the text but didn't actually move the item.
			if (startrename)
			{
				startrenametimeout = setTimeout(StartRenameHandler, 500);

				window.addEventListener('touchstart', CancelRenameHandler, true);
				window.addEventListener('mousedown', CancelRenameHandler, true);
				window.addEventListener('keydown', CancelRenameHandler, true);
			}
		};

		// Start a drag operation.
		var MoveCopyDragStartHandler = function(e) {
			if (!e.isTrusted)  return;

			// Stop the no move/copy handler since a move/copy operation has started.
			if (scrollnomoveinfo)
			{
				if (scrollnomoveinfo.origevent.ctrlKey || scrollnomoveinfo.origevent.target.tagName === 'INPUT' || scrollnomoveinfo.origevent.button == 2 || selectmodemulti)
				{
					$this.SetSelectedItems([scrollnomoveinfo.origelem.dataset.feid], true);
				}

				scrollnomoveinfo = null;
			}

			window.removeEventListener('mouseup', ScrollNoMoveHandler, true);

			// Disable clipboard overlay.
			elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_items_clipboard_contextmenu');
			elems.itemsclipboardoverlaypastewrap.classList.add('fe_fileexplorer_hidden');

			if (!numselecteditems)
			{
				e.preventDefault();

				return;
			}

			// Allow for same-instance drop target detection.
			elems.innerwrap.classList.add('fe_fileexplorer_drag_source');

			var icontype, ids = [];

			if (focuseditem === false)  icontype = 'file';
			else
			{
				var entries = currfolder.GetEntries();
				var entryidmap = currfolder.GetEntryIDMap();
				var entry = entries[entryidmap[focuseditem.dataset.feid]];

				icontype = entry.type;
			}

			for (var x in selecteditemsmap)
			{
				if (selecteditemsmap.hasOwnProperty(x))  ids.push(x);
			}

			e.dataTransfer.setDragImage(new Image(), 9999, 0);

			e.dataTransfer.setData('application/file-explorer-icon;' + JSON.stringify({ group: main_group, numitems: numselecteditems, type: icontype }), '');
			e.dataTransfer.setData('application/file-explorer-folder', JSON.stringify({ source: main_id, path: currfolder.GetPath(), ids: ids }));

			// Chromium DownloadURL support.
			if ($this.hasEventListener('get_download_url'))
			{
				// Synchronous call only.
				var entries = currfolder.GetEntries();
				var entryidmap = currfolder.GetEntryIDMap();
				var entry = entries[entryidmap[ids[0]]];
				var result = {};

				DispatchEvent('get_download_url', [result, currfolder, ids, entry]);

				if (result && result.name && result.url)  e.dataTransfer.setData('DownloadURL', 'application/octet-stream:' + result.name + ':' + result.url);
			}
		};

		var MoveCopyDragEndHandler = function(e) {
			elems.innerwrap.classList.remove('fe_fileexplorer_drag_source');
		};

		elems.itemswrap.addEventListener('dragstart', MoveCopyDragStartHandler);
		elems.itemswrap.addEventListener('dragend', MoveCopyDragEndHandler);

		// Handle drop target operations.  When the drag source is the same as the drop target (i.e. the same instance), treat selected items a bit differently.
		var movecopyenters = 0, movecopydata = false;
		var GetMoveCopyDragNodeInfo = function(e) {
			var node = e.target;
			while (node && node.parentNode && node.parentNode !== elems.pathsegmentswrap && node.parentNode.parentNode !== elems.itemswrap && node !== elems.innerwrap)  node = node.parentNode;

			if (!node)  return { node: null, type: 'error' };

			if (node === elems.innerwrap)  return { node: null, type: 'currfolder' };

			if (!node.parentNode)  return { node: null, type: 'error' };

			if (node.parentNode.parentNode === elems.itemswrap)
			{
				if (node.parentNode.classList.contains('fe_fileexplorer_item_folder'))  return { node: node.parentNode, type: 'item' };
				else  return { node: null, type: 'currfolder' };
			}

			if (node.parentNode === elems.pathsegmentswrap)  return { node: node, type: 'path' };
		};

		var MoveCopyDragUpdateStatusText = function(e, final) {
			if (movecopydata.dropeffect === 'none')  return;

			var str = (e.ctrlKey || movecopydata.dropeffect === 'copy' ? (final ? 'Copying' : 'Copy') : (final ? 'Moving' : 'Move'));

			str += (movecopydata.numitems === 1 ? ' 1 item' : ' {0} items');

			if (!movecopydata.dropallowed)  $this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate(str + '...'), movecopydata.numitems)));
			else if (movecopydata.lasttype === 'currfolder')
			{
				var path = currfolder.GetPath();

				$this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate(str + ' to "{1}"...'), movecopydata.numitems, path[path.length - 1][1])));
			}
			else if (movecopydata.lasttype === 'path')
			{
				var path = currfolder.GetPath();

				$this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate(str + ' to "{1}"...'), movecopydata.numitems, path[movecopydata.lastnode._fepos][1])));
			}
			else
			{
				var entries = currfolder.GetEntries();
				var entryidmap = currfolder.GetEntryIDMap();
				var entry = entries[entryidmap[movecopydata.lastnode.dataset.feid]];

				$this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate(str + ' to "{1}"...'), movecopydata.numitems, entry.name)));
			}
		};

		var MoveCopyDragEnterHandler = function(e) {
			if (!e.isTrusted)  return;

			if (!movecopyenters)
			{
				// See if the source is from File Explorer.
				movecopydata = GetFileExplorerDragIconData(e, main_group);

				if (movecopydata !== false)
				{
					movecopydata.issource = elems.innerwrap.classList.contains('fe_fileexplorer_drag_source');
					movecopydata.lastnode = null;
					movecopydata.lasttype = 'error';
					movecopydata.dropallowed = false;
					movecopydata.dropeffect = 'auto';

					MoveCopyDragUpdateStatusText(e);

					// Deny folder changes.
					currfolder.SetBusyRef(1);
				}
				else
				{
					// See if the dataTransfer contains files (from the desktop).
					for (var x = 0; x < e.dataTransfer.types.length; x++)
					{
						if (e.dataTransfer.types[x] === 'Files')
						{
							// Create a fake move/copy structure.
							movecopydata = {
								group: main_group,
								numitems: '',
								type: 'file',
								issource: false,
								lastnode: null,
								lasttype: 'error',
								dropallowed: false,
								dropeffect: ($this.hasEventListener('init_upload') ? 'copy' : 'none')
							};

							MoveCopyDragUpdateStatusText(e);

							// Deny folder changes.
							currfolder.SetBusyRef(1);

							break;
						}
					}
				}
			}

			if (movecopydata !== false)
			{
				e.preventDefault();

				// Apply hover effect if the node changed.
				if (movecopydata.dropeffect !== 'none')
				{
					var nodeinfo = GetMoveCopyDragNodeInfo(e);

					if (nodeinfo.node !== movecopydata.lastnode || nodeinfo.type !== movecopydata.lasttype)
					{
						if (movecopydata.lastnode)  movecopydata.lastnode.classList.remove('fe_fileexplorer_drag_hover');

						movecopydata.lastnode = nodeinfo.node;
						movecopydata.lasttype = nodeinfo.type;

						if (!movecopydata.lastnode)  movecopydata.dropallowed = (!movecopydata.issource && movecopydata.lasttype === 'currfolder');
						else
						{
							movecopydata.lastnode.classList.add('fe_fileexplorer_drag_hover');

							movecopydata.dropallowed = (!movecopydata.issource || movecopydata.lasttype != 'item' || !(movecopydata.lastnode.dataset.feid in selecteditemsmap));
						}

						MoveCopyDragUpdateStatusText(e);
					}
				}
			}

			movecopyenters++;
		};

		var MoveCopyDragOverHandler = function(e) {
			if (!e.isTrusted)  return;

			if (movecopydata !== false)
			{
				e.preventDefault();

				var origeffect = e.dataTransfer.dropEffect;

				if (movecopydata.dropeffect !== 'auto')  e.dataTransfer.dropEffect = movecopydata.dropeffect;
				else if (e.ctrlKey)  e.dataTransfer.dropEffect = ($this.hasEventListener('copy') ? 'copy' : 'none');
				else  e.dataTransfer.dropEffect = ($this.hasEventListener('move') ? 'move' : 'none');

				if (origeffect !== e.dataTransfer.dropEffect)  MoveCopyDragUpdateStatusText(e);
			}
		};

		var MoveCopyDragLeaveHandler = function(e) {
			if (!e.isTrusted)  return;

			movecopyenters--;

			if (movecopyenters < 1)
			{
				movecopyenters = 0;

				if (movecopydata.lastnode)  movecopydata.lastnode.classList.remove('fe_fileexplorer_drag_hover');

				// Restore the status bar.
				UpdateSelectionsChanged();

				// Allow folder changes.
				currfolder.SetBusyRef(-1);

				movecopydata = false;
			}
		};

		// Semi-reusable code for both drag-and-drop and clipboard paste.
		var PerformFinalMoveCopy = function(issource, lasttype, lastnode, optype, dropdata) {
			// Copy existing information for later use.
			var origcurrfolder = currfolder;
			var targetfolder;
			var selecteditemsmap2 = Object.assign({}, selecteditemsmap);
			var numselecteditems2 = numselecteditems;

			// Determine the target folder, creating it if necessary.  Path is only used for drag-and-drop.
			if (lasttype === 'currfolder')  targetfolder = currfolder;
			else if (lasttype === 'path')  targetfolder = $this.GetMappedFolderFromPath(currfolder.GetPath().slice(0, lastnode._fepos + 1));
			else if (lasttype === 'item')
			{
				var entries = currfolder.GetEntries();
				var entryidmap = currfolder.GetEntryIDMap();
				var entry = entries[entryidmap[lastnode.dataset.feid]];
				var path = currfolder.GetPath().slice();

				// Append the selected path segment.
				var pathitem = [entry.id, entry.name];
				if ('attrs' in entry)  pathitem.push(entry.attrs);

				path.push(pathitem);

				// Create/Update the target folder.
				var pathkey = GetMappedPathKey(path);

				if (!foldermap[pathkey])  foldermap[pathkey] = new Folder(path);

				targetfolder = foldermap[pathkey];
			}

			targetfolder.refs++;

			var calledback = false;
			var movecopycallback = function(success, selectentries) {
				if (calledback || destroyinprogress)  return;

				calledback = true;

				$this.StopOperationIndicator();

				DecrementMappedFolderRefCount(targetfolder);

				// Restore the status bar.
				UpdateSelectionsChanged();

				if (optype === 'move')  currfolder.SetBusyRef(-1);

				if (success === true)
				{
					// If the target folder was also the source folder and the same folder is being viewed and performing a move operation, remove the previously selected item(s).
					if (issource && currfolder === origcurrfolder && targetfolder !== currfolder && optype === 'move')
					{
						var entries = currfolder.GetEntries();
						var entries2 = [];
						for (var x = 0; x < entries.length; x++)
						{
							if (!(entries[x].id in selecteditemsmap2))  entries2.push(entries[x]);
						}

						// Adjust the focused item.
						if (focuseditem !== false && (focuseditem.dataset.feid in selecteditemsmap2))
						{
							var node = focuseditem.nextSibling;
							while (node && (node.dataset.feid in selecteditemsmap2))  node = node.nextSibling;

							if (!node)
							{
								node = focuseditem.previousSibling;
								while (node && (node.dataset.feid in selecteditemsmap2))  node = node.previousSibling;
							}

							if (node)
							{
								$this.SetFocusItem(node.dataset.feid, true);
								$this.ScrollToFocusedItem();
							}
						}

						currfolder.SetEntries(entries2);
					}
				}
				else
				{
					$this.SetNamedStatusBarText('message', EscapeHTML(FormatStr($this.Translate((optype === 'copy' ? 'Copying' : 'Moving') + ' items failed.' + (typeof success === 'string' ? '  {0}' : '')), success)), $this.settings.messagetimeout);
				}

				// Handle entries.
				if ($this.IsMappedFolder(targetfolder) && selectentries && Array.isArray(selectentries))
				{
					// Merge items into the target folder.
					var entries = targetfolder.GetEntries();
					var entryidmap = targetfolder.GetEntryIDMap();

					for (var x = 0; x < selectentries.length; x++)
					{
						if (selectentries[x].id in entryidmap)  entries[entryidmap[selectentries[x].id]] = selectentries[x];
						else  entries.push(selectentries[x]);
					}

					targetfolder.SetEntries(entries);

					// If the target folder is visible, set selections to the IDs moved/copied.
					if (targetfolder === currfolder)
					{
						var selectids = [];

						for (var x = 0; x < selectentries.length; x++)
						{
							selectids.push(selectentries[x].id);
						}

						$this.SetSelectedItems(selectids);
					}
				}

				// Handle all scenarios with a forced refresh.
				$this.RefreshFolders(true);
			};

			// Release busy status for copy operations.
			if (optype === 'copy')  currfolder.SetBusyRef(-1);

			$this.StartOperationIndicator();

			DispatchEvent(optype, [movecopycallback, dropdata.path, dropdata.ids, targetfolder]);
		};


		// Reusable progress tracker.
		var progresstrackers = [], progresstrackerinterval;

		var InitProgressTracker = function() {
			var tracker = {
				started: Date.now(),
				totalbytes: 0,
				showbyterate: false,
				uploading: false,
				queueditems: 0,
				queuesizeunknown: false,
				itemsdone: 0,
				faileditems: 0,
				cancelcallback: null
			};

			return tracker;
		};

		$this.UpdateProgressText = function() {
			if (!progresstrackers || !progresstrackers.length)  return;

			// Combine all progress tracker info.
			var tracker = InitProgressTracker();

			var currts = tracker.started;

			for (var x = 0; x < progresstrackers.length; x++)
			{
				tracker.totalbytes += progresstrackers[x].totalbytes;

				if (progresstrackers[x].showbyterate !== false)
				{
					tracker.showbyterate = true;

					if (tracker.started > progresstrackers[x].started)  tracker.started = progresstrackers[x].started;
				}

				if (progresstrackers[x].uploading !== false)
				{
					if (tracker.uploading === false)  tracker.uploading = 0;

					tracker.uploading += progresstrackers[x].uploading;
				}

				tracker.queueditems += progresstrackers[x].queueditems;

				if (progresstrackers[x].queuesizeunknown !== false)  tracker.queuesizeunknown = true;

				tracker.itemsdone += progresstrackers[x].itemsdone;
				tracker.faileditems += progresstrackers[x].faileditems;
			}

			var totalbytesstr = GetDisplayFilesize(tracker.totalbytes, $this.settings.adjustprecision, $this.settings.displayunits);

			// Wait a few seconds before calculating the byte rate.
			if (tracker.showbyterate && currts > tracker.started + 3000)
			{
				var byterate = tracker.totalbytes / ((currts - tracker.started) / 1000);

				var byteratestr = FormatStr($this.Translate('{0}/s'), GetDisplayFilesize(byterate, $this.settings.adjustprecision, $this.settings.displayunits));

				elems.statusbaractionprogressmessagewrap.innerHTML = EscapeHTML(FormatStr('{0}\u00A0\u00A0\u00A0{1}', byteratestr, totalbytesstr));
			}
			else
			{
				elems.statusbaractionprogressmessagewrap.innerHTML = EscapeHTML(FormatStr('{0}', totalbytesstr));
			}

			var stropts = [];
			var titleopts = [];

			if (tracker.uploading !== false)
			{
				stropts.push($this.Translate('{0} <span class="fe_fileexplorer_action_progress_msg_icon fe_fileexplorer_action_progress_msg_icon_uploads_in_progress"></span>'));
				titleopts.push($this.Translate('{0} uploading'));
			}

			if (tracker.queueditems)
			{
				stropts.push($this.Translate((tracker.queuesizeunknown ? '{1}+ ' : '{1} ') + '<span class="fe_fileexplorer_action_progress_msg_icon fe_fileexplorer_action_progress_msg_icon_queued"></span>'));
				titleopts.push($this.Translate(tracker.queuesizeunknown ? '{1}+ queued' : '{1} queued'));
			}

			if (tracker.itemsdone)
			{
				stropts.push($this.Translate('{2} <span class="fe_fileexplorer_action_progress_msg_icon fe_fileexplorer_action_progress_msg_icon_done"></span>'));
				titleopts.push($this.Translate('{2} done'));
			}

			if (tracker.faileditems)
			{
				stropts.push($this.Translate('{3} <span class="fe_fileexplorer_action_progress_msg_icon fe_fileexplorer_action_progress_msg_icon_errors"></span>'));
				titleopts.push($this.Translate('{3} failed'));
			}

			elems.statusbaractionprogressmessagewrap2.innerHTML = FormatStr(stropts.join('\u00A0\u00A0\u00A0'), tracker.uploading, tracker.queueditems, tracker.itemsdone, tracker.faileditems);
			elems.statusbaractionprogressmessagewrap2.title = EscapeHTML(FormatStr(titleopts.join(', '), tracker.uploading, tracker.queueditems, tracker.itemsdone, tracker.faileditems));
		};

		// Stop all progress callbacks.
		var ProgressCancelAllHandler = function(e) {
			if (e)
			{
				if (!e.isTrusted)  return;

				e.preventDefault();
			}

			$this.SetNamedStatusBarText('message', EscapeHTML($this.Translate('Stopping...')), $this.settings.messagetimeout);

			for (var x = 0; x < progresstrackers.length; x++)
			{
				if (progresstrackers[x].cancelcallback)  progresstrackers[x].cancelcallback.call($this, e);
			}

			$this.Focus(true, true);

			elems.statusbaractionprogresscancelwrap.classList.add('fe_fileexplorer_hidden');
		};

		elems.statusbaractionprogresscancelwrap.addEventListener('click', ProgressCancelAllHandler);

		var ProgressCancelKeydownHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.keyCode == 13 || e.keyCode == 32)  ProgressCancelAllHandler(e);
		};

		elems.statusbaractionprogresscancelwrap.addEventListener('keydown', ProgressCancelKeydownHandler);

		var FinishProgressDisplay = function() {
			elems.statusbaractionprogresswrap.classList.add('fe_fileexplorer_hidden');

			elems.statusbaractionprogressmessagewrap.innerHTML = '';

			$this.SetNamedStatusBarText('message', '');

			clearInterval(progresstrackerinterval);
			progresstrackerinterval = null;
		};

		// When a touch, mouse, or keyboard event happens after the last tracker is finished, start a short timeout to clean up the remaining bits.
		var PreFinishProgressDisplay = function(e) {
			window.removeEventListener('touchstart', PreFinishProgressDisplay, true);
			window.removeEventListener('mousemove', PreFinishProgressDisplay, true);
			window.removeEventListener('mousedown', PreFinishProgressDisplay, true);
			window.removeEventListener('keydown', PreFinishProgressDisplay, true);

			if (e)  progresstrackerinterval = setInterval(FinishProgressDisplay, 1000);
		};

		$this.CreateProgressTracker = function(cancelcallback) {
			var tracker = InitProgressTracker();

			tracker.cancelcallback = cancelcallback;

			progresstrackers.push(tracker);

			if (progresstrackerinterval)  clearInterval(progresstrackerinterval);

			progresstrackerinterval = setInterval($this.UpdateProgressText, 1000);

			PreFinishProgressDisplay();

			$this.UpdateProgressText();

			if (cancelcallback)  elems.statusbaractionprogresscancelwrap.classList.remove('fe_fileexplorer_hidden');
			elems.statusbaractionprogresswrap.classList.remove('fe_fileexplorer_hidden');

			return tracker;
		};

		$this.RemoveProgressTracker = function(tracker, finishmessage) {
			$this.UpdateProgressText();

			for (var x = 0; x < progresstrackers.length; x++)
			{
				if (progresstrackers[x] === tracker)
				{
					progresstrackers.splice(x, 1);

					break;
				}
			}

			var found = false;
			for (var x = 0; x < progresstrackers.length; x++)
			{
				if (progresstrackers[x].cancelcallback)  found = true;
			}

			if (!found)  elems.statusbaractionprogresscancelwrap.classList.add('fe_fileexplorer_hidden');

			if (!progresstrackers.length)
			{
				if (progresstrackerinterval)
				{
					clearInterval(progresstrackerinterval);
					progresstrackerinterval = null;
				}

				window.addEventListener('touchstart', PreFinishProgressDisplay, true);
				window.addEventListener('mousemove', PreFinishProgressDisplay, true);
				window.addEventListener('mousedown', PreFinishProgressDisplay, true);
				window.addEventListener('keydown', PreFinishProgressDisplay, true);

				if (finishmessage)  $this.SetNamedStatusBarText('message', $this.Translate(finishmessage));
			}
		};


		// Manages active uploads.
		var uploadactivequeue = [], uploadqueue = [], uploaddirentries = [], uploadqueuestarted = false, uploadprogresstracker = false, uploadfolderinterval, uploadcancel = false;

		var BlobSlice = function() {
			var tempslice = this.slice || this.webkitSlice || this.mozSlice;

			return tempslice.apply(this, arguments);
		};

		// Forcefully stop all uploads and clear out the queue.
		var UploadCancelAllHandler = function(e) {
			if (e)
			{
				if (!e.isTrusted)  return;

				e.preventDefault();
			}

			uploadcancel = true;

			for (var x = uploadactivequeue.length; x; x--)
			{
				if (uploadactivequeue[x - 1].xhr)  uploadactivequeue[x - 1].xhr.Abort();
			}

			if (uploadfolderinterval)
			{
				clearInterval(uploadfolderinterval);
				uploadfolderinterval = null;
			}
		};

		// Refreshes the current folder every 30 seconds while uploading.
		var UpdateUploadRefreshFolder = function() {
			$this.RefreshFolders(true);
		};

		var UpdateUploadProgressInfo = function() {
			if (!uploadprogresstracker)  return;

			uploadprogresstracker.uploading = uploadactivequeue.length;
			uploadprogresstracker.queueditems = uploadqueue.length;
			uploadprogresstracker.queuesizeunknown = (uploaddirentries.length > 0);
		};

		// Remove the item from the active queue and start the next upload item.
		var RemoveUploadActiveQueueItem = function(fileinfo) {
			for (var x = 0; x < uploadactivequeue.length; x++)
			{
				if (uploadactivequeue[x] === fileinfo)
				{
					DecrementMappedFolderRefCount(fileinfo.folder);

					uploadactivequeue.splice(x, 1);

					if (fileinfo.xhr)
					{
						fileinfo.xhr.Destroy();

						delete fileinfo.xhr;
					}

					break;
				}
			}

			UpdateUploadProgressInfo();

			StartNextUpload();
		};

		var FailUpload = function(fileinfo, newstatus, e) {
			fileinfo.status = newstatus;

			uploadprogresstracker.faileditems++;

			DispatchEvent('upload_error', [fileinfo, e]);

			RemoveUploadActiveQueueItem(fileinfo);
		};

		// Builds a chunk and an upload request object and starts the upload.
		var StartUploadChunk = function(fileinfo) {
			if (uploadcancel)
			{
				FailUpload(fileinfo, 'request_aborted');

				return;
			}

			// Calculate the chunk size.
			var chunksize = (fileinfo.chunksize ? (typeof fileinfo.chunksize === 'function' ? fileinfo.chunksize(fileinfo) : fileinfo.chunksize) : fileinfo.sizebytes - fileinfo.currchunkstart);

			if (fileinfo.currchunkstart + chunksize > fileinfo.sizebytes)  chunksize = fileinfo.sizebytes - fileinfo.currchunkstart;

			// When sending chunked data, make the first chunk fairly small so if the the upload is going to fail for whatever reason (e.g. an invalid file extension), it will fail quickly.
			if (!fileinfo.currchunkstart && chunksize < fileinfo.sizebytes && chunksize > 4096)  chunksize = 4096;

			if (fileinfo.type === 'file')
			{
				fileinfo.currblob = BlobSlice.call(fileinfo.file, fileinfo.currchunkstart, fileinfo.currchunkstart + chunksize, fileinfo.file.type);

				chunksize = fileinfo.currblob.size;
			}

			fileinfo.currchunksize = chunksize;

			// Set up various callbacks.
			var uploadstarthandler = function(e) {
				fileinfo.status = 'upload_started';
				fileinfo.progress.uploadedchunkbytes = 0;
			};

			var uploadprogresshandler = function(e) {
				fileinfo.status = 'upload_in_progress';

				var diffsize = (e.loaded - fileinfo.progress.uploadedchunkbytes);

				uploadprogresstracker.totalbytes += diffsize;
				fileinfo.progress.uploadedbytes += diffsize;

				fileinfo.progress.uploadedchunkbytes = e.loaded;

				var currts = Date.now();

				// Wait a few seconds before calculating the byterate.
				if (currts > fileinfo.progress.started + 3000)  fileinfo.progress.byterate = fileinfo.progress.uploadedbytes / (currts - fileinfo.progress.started);

				fileinfo.progress.percent = (e.lengthComputable ? e.loaded / e.total * 100 : (fileinfo.currchunksize ? e.loaded / fileinfo.currchunksize : 0));
			};

			var uploadcompletehandler = function(e) {
				fileinfo.status = 'upload_complete';

				if (fileinfo.progress.uploadedbytes < fileinfo.currchunksize)  uploadprogresstracker.trackerbytes += (fileinfo.currchunksize - fileinfo.progress.uploadedbytes);
			};

			var origcurrfolder = currfolder;
			var requestcompletehandler = function(e) {
				try
				{
					var response = JSON.parse(e.target.responseText);

					fileinfo.currchunkstart += fileinfo.currchunksize;

					if (!response.success)
					{
						$this.SetNamedStatusBarText('message', EscapeHTML(FormatStr($this.Translate('Error uploading "{0}" ({1})'), fileinfo.fullPath, response.errorcode)), $this.settings.messagetimeout * 5);

						FailUpload(fileinfo, 'request_error', e);
					}
					else if (fileinfo.currchunkstart < fileinfo.sizebytes)
					{
						// Start the next upload chunk.
						fileinfo.retriesleft = fileinfo.retries;

						StartUploadChunk(fileinfo);
					}
					else if (!$this.hasEventListener('upload_done'))
					{
						if (response.entry && $this.IsMappedFolder(origcurrfolder))  origcurrfolder.SetEntry(response.entry);

						uploadprogresstracker.itemsdone++;

						RemoveUploadActiveQueueItem(fileinfo);
					}
					else
					{
						// Finalize the upload.
						if (response.entry && $this.IsMappedFolder(origcurrfolder))  origcurrfolder.SetEntry(response.entry);

						origcurrfolder = currfolder;

						var calledback = false;
						var finalizecallback = function(success, entry) {
							if (calledback)  return;

							calledback = true;

							if (entry && $this.IsMappedFolder(origcurrfolder))  origcurrfolder.SetEntry(entry);

							if (success === true)
							{
								uploadprogresstracker.itemsdone++;

								RemoveUploadActiveQueueItem(fileinfo);
							}
							else
							{
								$this.SetNamedStatusBarText('message', EscapeHTML(FormatStr($this.Translate('Finalizing "{0}" failed.' + (typeof success === 'string' ? '  {1}' : '')), fileinfo.fullPath, success)), $this.settings.messagetimeout);

								FailUpload(fileinfo, 'finalize_failed');
							}
						};

						DispatchEvent('upload_done', [finalizecallback, fileinfo]);
					}
				}
				catch(e)
				{
					requesterrorhandler(e);
				}
			};

			var requesterrorhandler = function(e) {
				if (!fileinfo.retriesleft)  FailUpload(fileinfo, 'request_failed', e);
				else
				{
					// Retry.
					fileinfo.retriesleft--;

					StartUploadChunk(fileinfo);
				}
			};

			var requestabortedhandler = function(e) {
				FailUpload(fileinfo, 'request_aborted', e);
			};

			fileinfo.xhr = new PrepareXHR(fileinfo);

			// Allow headers/params to be modified for the current chunk and/or add listeners to the xhr object.
			DispatchEvent('update_upload_fileinfo', fileinfo);

			fileinfo.xhr.upload.addEventListener('loadstart', uploadstarthandler);
			fileinfo.xhr.upload.addEventListener('progress', uploadprogresshandler);
			fileinfo.xhr.upload.addEventListener('load', uploadcompletehandler);

			fileinfo.xhr.addEventListener('load', requestcompletehandler);
			fileinfo.xhr.addEventListener('error', requesterrorhandler);
			fileinfo.xhr.addEventListener('timeout', requesterrorhandler);
			fileinfo.xhr.addEventListener('abort', requestabortedhandler);

			fileinfo.method = 'POST';
			fileinfo.headers = fileinfo.headers || {};

			// Set the Content-Range request header for chunked file transfers.
			if (fileinfo.type === 'file' && (fileinfo.currchunkstart || fileinfo.currchunksize < fileinfo.sizebytes))
			{
				// Handle zero byte chunks gracefully (0 - 1 + 1 = 0).
				if (!fileinfo.currchunksize)  fileinfo.headers['Content-Range'] = 'bytes 1-0/' + fileinfo.sizebytes;
				else  fileinfo.headers['Content-Range'] = 'bytes ' + fileinfo.currchunkstart + '-' + (fileinfo.currchunkstart + fileinfo.currchunksize - 1) + '/' + fileinfo.sizebytes;

				// Enable FileUploadHelper compatibility.  Only really needs to exist.
				fileinfo.headers['Content-Disposition'] = 'attachment; filename="' + encodeURI(fileinfo.name || fileinfo.file.name) + '"';
			}

			fileinfo.headers['Accept'] = 'application/json';

			// When using FormData for params, the FormData object has to be rebuilt with each request.
			var formdata = fileinfo.xhr.PrepareBody();

			// Append current path.  Useful for returning an entry from the server.
			if (fileinfo.currpathparam)
			{
				formdata.append(fileinfo.currpathparam, JSON.stringify(currfolder.GetPathIDs()));
			}

			// Append the file data.
			if (fileinfo.type === 'file')
			{
				formdata.append(fileinfo.fileparam, fileinfo.currblob, fileinfo.name || fileinfo.file.name);
			}

			// Start the upload.
			fileinfo.xhr.Send(formdata);
		};

		var InitializeUpload = function(fileinfo) {
			var calledback = false;
			var startuploadcallback = function(process) {
				if (calledback)  return;

				calledback = true;

				if (process === true && !destroyinprogress)
				{
					// Initialize the fileinfo data.
					fileinfo.status = 'upload_start';

					fileinfo.progress = {
						started: Date.now(),
						uploadedbytes: 0,
						byterate: 0,
						percent: 0
					};

					fileinfo.sizebytes = (fileinfo.type === 'file' ? fileinfo.file.size : 0);
					fileinfo.currchunkstart = 0;
					if (!fileinfo.retries)  fileinfo.retries = 0;
					fileinfo.retriesleft = fileinfo.retries;

					if (!uploadcancel)  $this.SetNamedStatusBarText('message', EscapeHTML(FormatStr($this.Translate('Uploading "{0}"...'), fileinfo.fullPath)), $this.settings.messagetimeout * 5);

					// Set up initial progress tracker info.
					if (!uploadprogresstracker)
					{
						uploadprogresstracker = $this.CreateProgressTracker(UploadCancelAllHandler);
						uploadprogresstracker.showbyterate = true;
					}

					if (!uploadfolderinterval)  uploadfolderinterval = setInterval(UpdateUploadRefreshFolder, 30000);

					UpdateUploadProgressInfo();

					$this.UpdateProgressText();

					// Start the first chunk.
					StartUploadChunk(fileinfo);
				}
				else if (typeof process === 'string')
				{
					$this.SetNamedStatusBarText('message', EscapeHTML(FormatStr($this.Translate('Starting "{0}" failed.  {1}'), fileinfo.fullPath, process)), $this.settings.messagetimeout);

					// Set up initial progress tracker info.
					if (!uploadprogresstracker)
					{
						uploadprogresstracker = $this.CreateProgressTracker(UploadCancelAllHandler);
						uploadprogresstracker.showbyterate = true;
					}

					FailUpload(fileinfo, 'start_failed');
				}
				else
				{
					RemoveUploadActiveQueueItem(fileinfo);
				}
			};

			UpdateUploadProgressInfo();

			$this.UpdateProgressText();

			if (!uploadqueuestarted)  uploadqueuestarted = Date.now();

			DispatchEvent('init_upload', [startuploadcallback, fileinfo, uploadqueuestarted]);
		};

		// Uses a FileReader object to determine if a File blob is readable or not.
		var TestUnknownTypeUpload = function(fileinfo) {
			fileinfo.status = 'waiting';

			var fr = new FileReader();

			// Early terminate reading files.
			fr.addEventListener('progress', function(e) {
				fr.abort();

				fileinfo.status = 'init';
				fileinfo.type = 'file';

				StartNextUpload();
			});

			// The whole file loaded.
			fr.addEventListener('load', function(e) {
				fileinfo.status = 'init';
				fileinfo.type = 'file';

				StartNextUpload();
			});

			// Not a usable file.  Possibly a directory.
			fr.addEventListener('error', function(e) {
				fileinfo.status = 'invalid_item';

				DispatchEvent('upload_error', [fileinfo, e]);

				StartNextUpload();
			});

			fr.readAsArrayBuffer(fileinfo.file);
		};

		var QueueUploadEntry = function(targetfolder, entry) {
			if (entry.isDirectory)
			{
				var reader = entry.createReader();

				var dirinfo = {
					entry: entry,
					reader: reader,
					folder: targetfolder,
					type: 'direntry',
					size: 0,
					fullPath: entry.fullPath,
					busy: false
				};

				targetfolder.refs++;

				uploaddirentries.push(dirinfo);
			}
			else if (entry.isFile)
			{
				var fileinfo = {
					status: 'init',
					folder: targetfolder,
					type: 'file',
					file: null,
					fullPath: entry.fullPath
				};

				targetfolder.refs++;

				entry.file(function(file) {
					fileinfo.file = file;

					uploadqueue.push(fileinfo);

					StartNextUpload();
				}, function(e) {
					fileinfo.status = 'invalid_file';

					DispatchEvent('upload_error', [fileinfo, e]);

					DecrementMappedFolderRefCount(targetfolder);

					StartNextUpload();
				});
			}
		};

		var StartNextUpload = function() {
			if (!$this.hasEventListener('init_upload'))  uploadcancel = true;

			if (uploadcancel && uploaddirentries.length && !uploaddirentries[0].busy)  uploaddirentries = [];

			// Queue up some items from directory entries.
			if (!uploadcancel && uploadqueue.length < 100 && uploaddirentries.length && !uploaddirentries[0].busy)
			{
				var targetfolder = uploaddirentries[0].folder;

				uploaddirentries[0].busy = true;

				// May only read up to 100 entries on some browsers (e.g. Chromium-based).
				uploaddirentries[0].reader.readEntries(function(entries) {
					uploaddirentries[0].busy = false;

					if (uploadcancel)
					{
						uploaddirentries.shift();

						UpdateUploadProgressInfo();
					}
					else if (!entries.length)
					{
						// Add empty directory to the queue.
						if (!uploaddirentries[0].size)
						{
							var fileinfo = {
								status: 'init',
								folder: targetfolder,
								type: 'dir',
								fullPath: uploaddirentries[0].fullPath
							};

							targetfolder.refs++;

							uploadqueue.push(fileinfo);
						}

						// No more entries.
						DecrementMappedFolderRefCount(targetfolder);

						uploaddirentries.shift();

						UpdateUploadProgressInfo();
					}
					else
					{
						uploaddirentries[0].size += entries.length;

						entries.forEach(function(entry) {
							QueueUploadEntry(targetfolder, entry);
						});
					}

					StartNextUpload();
				}, function(e) {
					// An error occurred.  Remove the directory.
					DispatchEvent('upload_error', [uploaddirentries[0], e]);

					DecrementMappedFolderRefCount(targetfolder);

					uploaddirentries.shift();

					UpdateUploadProgressInfo();

					StartNextUpload();
				});
			}

			// Trigger concurrent upload start.
			if (uploadactivequeue.length < $this.settings.concurrentuploads && uploadqueue.length)
			{
				// Find something to do.
				var waiting = 0, found = false;
				for (var x = 0; x < uploadqueue.length; x++)
				{
					if (uploadqueue[x].status === 'waiting')  waiting++;
					else if (uploadcancel || uploadqueue[x].status === 'invalid_item')
					{
						if (uploadqueue[x].status === 'invalid_item')  console.error('Removed \'' + uploadqueue[x].fullPath + '\' from the upload queue due to an error - it is probably a directory.');

						DecrementMappedFolderRefCount(uploadqueue[x].folder);

						uploadqueue.splice(x, 1);

						x--;

						UpdateUploadProgressInfo();

						found = true;
					}
					else if (uploadqueue[x].status === 'init')
					{
						if (uploadqueue[x].type === 'file' || uploadqueue[x].type === 'dir')
						{
							if (uploadactivequeue.length < $this.settings.concurrentuploads)
							{
								var fileinfo = uploadqueue[x];

								uploadactivequeue.push(fileinfo);

								uploadqueue.splice(x, 1);

								x--;

								InitializeUpload(fileinfo);

								found = true;
							}
						}
						else if (uploadqueue[x].type === '' && waiting < 10)
						{
							TestUnknownTypeUpload(uploadqueue[x]);

							waiting++;

							found = true;
						}
					}
				}

				if (found)  StartNextUpload();
			}

			// Nothing left to do in any queue.  Clean up.
			if (uploadprogresstracker && !uploadactivequeue.length && !uploadqueue.length && !uploaddirentries.length && !destroyinprogress)
			{
				$this.RemoveProgressTracker(uploadprogresstracker, (uploadcancel || destroyinprogress ? 'Uploading stopped' : 'Uploading done'));

				if (uploadfolderinterval)
				{
					clearInterval(uploadfolderinterval);
					uploadfolderinterval = null;
				}

				$this.RefreshFolders(true);

				uploadqueuestarted = false;
				uploadprogresstracker = false;
				uploadcancel = false;

				// May trigger garbage collection.
				uploadactivequeue = [];
				uploadqueue = [];
				uploaddirentries = [];
			}
		};

		// Upload files specified by dataTransfer or clipboardData.
		$this.ProcessFilesAndUpload = function(targettype, targetnode, dt) {
			var targetfolder;

			// Determine the target folder, creating it if necessary.  Path is only used for drag-and-drop.
			if (targettype === 'currfolder')  targetfolder = currfolder;
			else if (targettype === 'path')  targetfolder = $this.GetMappedFolderFromPath(currfolder.GetPath().slice(0, targetnode._fepos + 1));
			else if (targettype === 'item')
			{
				var entries = currfolder.GetEntries();
				var entryidmap = currfolder.GetEntryIDMap();
				var entry = entries[entryidmap[targetnode.dataset.feid]];
				var path = currfolder.GetPath().slice();

				// Append the selected path segment.
				var pathitem = [entry.id, entry.name];
				if ('attrs' in entry)  pathitem.push(entry.attrs);

				path.push(pathitem);

				// Create/Update the target folder.
				var pathkey = GetMappedPathKey(path);

				if (!foldermap[pathkey])  foldermap[pathkey] = new Folder(path);

				targetfolder = foldermap[pathkey];
			}
			else
			{
				return;
			}

			if (dt.items && dt.items.length)
			{
				// Browser has 'items' support.
				var entry;

				for (var x = 0; x < dt.items.length; x++)
				{
					if (typeof dt.items[x].getAsEntry === 'function' && (entry = dt.items[x].getAsEntry()))  QueueUploadEntry(targetfolder, entry);
					else if (typeof dt.items[x].webkitGetAsEntry === 'function' && (entry = dt.items[x].webkitGetAsEntry()))  QueueUploadEntry(targetfolder, entry);
					else
					{
						// The item may be File-compatible.
						var file = dt.items[x].getAsFile();

						if (file)
						{
							var fileinfo = {
								status: 'init',
								folder: targetfolder,
								type: '',
								file: file
							};

							targetfolder.refs++;

							fileinfo.fullPath = '/' + fileinfo.file.name;

							uploadqueue.push(fileinfo);
						}
					}
				}
			}
			else if (dt.files && dt.files.length)
			{
				// Browser has 'files' support.
				for (var x = 0; x < dt.files.length; x++)
				{
					var file = dt.files[x];

					var fileinfo = {
						status: 'init',
						folder: targetfolder,
						type: '',
						file: file
					};

					targetfolder.refs++;

					fileinfo.fullPath = '/' + fileinfo.file.name;

					uploadqueue.push(fileinfo);
				}
			}

			StartNextUpload();
		};

		var MoveCopyDropHandler = function(e) {
			if (!e.isTrusted)  return;

			if (movecopydata !== false)
			{
				e.preventDefault();

				if (movecopydata.lasttype !== 'error')
				{
					if (movecopydata.lastnode)  movecopydata.lastnode.classList.remove('fe_fileexplorer_drag_hover');

					// Grab the drop data.
					var dropdata;
					try
					{
						dropdata = JSON.parse(e.dataTransfer.getData('application/file-explorer-folder'));
					}
					catch(e)
					{
					}

					// Update the drop effect.
					MoveCopyDragOverHandler(e);

					if (dropdata && movecopydata.dropallowed)
					{
						MoveCopyDragUpdateStatusText(e, true);

						// The current folder is already marked busy when MoveCopyDragEnterHandler() was called.
						PerformFinalMoveCopy(movecopydata.issource, movecopydata.lasttype, movecopydata.lastnode, e.dataTransfer.dropEffect, dropdata);
					}
					else if ((e.dataTransfer.files && e.dataTransfer.files.length) && movecopydata.dropallowed)
					{
						// Restore the status bar.
						UpdateSelectionsChanged();

						$this.ProcessFilesAndUpload(movecopydata.lasttype, movecopydata.lastnode, e.dataTransfer);

						currfolder.SetBusyRef(-1);
					}
					else
					{
						// Restore the status bar.
						UpdateSelectionsChanged();

						currfolder.SetBusyRef(-1);
					}
				}
				else
				{
					// Restore the status bar.
					UpdateSelectionsChanged();

					currfolder.SetBusyRef(-1);
				}

				movecopydata = false;
			}

			movecopyenters = 0;
		};

		elems.innerwrap.addEventListener('dragenter', MoveCopyDragEnterHandler);
		elems.innerwrap.addEventListener('dragover', MoveCopyDragOverHandler);
		elems.innerwrap.addEventListener('dragleave', MoveCopyDragLeaveHandler);
		elems.innerwrap.addEventListener('drop', MoveCopyDropHandler);

		// Handle moving/copying items and autoscroll.
// Probably obsolete code but possibly useful for mobile drag-and-drop IF that even makes sense to implement.
/*
		// Return the target entry (if any) for the supplied rectangle.
		var GetMoveCopyItemTarget = function(rect) {
			var entries = currfolder.GetEntries();

			return (DoesRectOverlapItemRect(rect, rect.startcol, rect.startrow) ? entries[rect.startrow * folderitemcache.cols.length + rect.startcol] : false);
		};

		var movingitems = false, copyitems = false;
		var UpdateMoveCopyItemsDisplay = function(newpos, forcemessage, final) {
			if (forcemessage)
			{
				if (copyitems)  elems.itemswrap.classList.add('fe_fileexplorer_items_copy');
				else  elems.itemswrap.classList.remove('fe_fileexplorer_items_copy');
			}

			var str = (copyitems ? (final ? 'Copying' : 'Copy') : (final ? 'Moving' : 'Move'));

			str += (numselecteditems === 1 ? ' 1 item' : ' {0} items');

			var currselectrect = {
				left: newpos.x,
				top: newpos.y,
				right: newpos.x,
				bottom: newpos.y
			};

			// Calculate rough position info.
			UpdateCalculatedSelectedItemsRect(currselectrect, prevselectrect);

			// If the point is inside an item, apply a different message if the message should change.
			var preventry = (forcemessage ? false : GetMoveCopyItemTarget(prevselectrect));
			var currentry = GetMoveCopyItemTarget(currselectrect);

			if (forcemessage || preventry !== currentry)
			{
				if (currentry && currentry.type === 'folder' && (!(currentry.id in selecteditemsmap)))  $this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate(str + ' to "{1}"...'), numselecteditems, currentry.name)));
				else  $this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate(str + '...'), numselecteditems)));
			}

			Object.assign(prevselectrect, currselectrect);

			if (final)  return { folder: folder, entry: currentry };
		};

		var movenewpos = {}, movecopyoverlay, movecopyoverlaysize = {};
		var MoveCopyHandler = function(e) {
			e.preventDefault();

			lastmouseevent = e;

			var rect = elems.itemsscrollwrapinner.getBoundingClientRect();

			movenewpos = {
				x: e.clientX - rect.left,
				y: e.clientY - rect.top
			};

			if (movenewpos.x < 0)  movenewpos.x = 0;
			if (movenewpos.x > rect.width)  movenewpos.x = rect.width;
			if (movenewpos.y < 0)  movenewpos.y = 0;
			if (movenewpos.y > rect.height)  movenewpos.y = rect.height;

			if (!movingitems && (Math.abs(movenewpos.x - selectanchorpos.x) > 8 || Math.abs(movenewpos.y - selectanchorpos.y) > 8))
			{
				// Initialize the move/copy operation.
				movingitems = true;
				copyitems = ('_fe_ctrl' in e ? e._fe_ctrl : e.ctrlKey);

				elems.itemswrap.classList.add('fe_fileexplorer_items_move_copy');

				UpdateMoveCopyItemsDisplay(movenewpos, true);

				// Stop the no move/copy handler since a move/copy operation has started.
				if (scrollnomoveinfo)
				{
					if (scrollnomoveinfo.origevent.ctrlKey || scrollnomoveinfo.origevent.target.tagName === 'INPUT' || scrollnomoveinfo.origevent.button == 2 || selectmodemulti)
					{
						$this.SetSelectedItems([scrollnomoveinfo.origelem.dataset.feid], true);
					}

					scrollnomoveinfo = null;
				}

				window.removeEventListener('mouseup', ScrollNoMoveHandler, true);

				// Disable clipboard overlay.
				elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_items_clipboard_contextmenu');
				elems.itemsclipboardoverlaypastewrap.classList.add('fe_fileexplorer_hidden');

				// Create the floating icon tracking overlay.
				movecopyoverlay = CreateNode('div', ['fe_fileexplorer_floating_drag_icon_wrap']);
				var innernode = CreateNode('div', ['fe_fileexplorer_floating_drag_icon_wrap_inner']);
				var iconnode = CreateNode('div', ['fe_fileexplorer_item_icon']);

				if (numselecteditems > 1)  innernode.dataset.numitems = numselecteditems;

				if (focuseditem === false)  iconnode.classList.add('fe_fileexplorer_item_icon_file');
				else
				{
					var entries = currfolder.GetEntries();
					var entryidmap = currfolder.GetEntryIDMap();
					var entry = entries[entryidmap[focuseditem.dataset.feid]];

					if (entry.type === 'folder')  iconnode.classList.add('fe_fileexplorer_item_icon_folder');
					else  iconnode.classList.add('fe_fileexplorer_item_icon_file');
				}

				innernode.appendChild(iconnode);
				movecopyoverlay.appendChild(innernode);
				document.body.appendChild(movecopyoverlay);

				movecopyoverlaysize = {
					xdiff: Math.floor(movecopyoverlay.offsetWidth / 2),
					ydiff: Math.floor(movecopyoverlay.offsetHeight - 8)
				};

				// Deny folder changes.
				currfolder.SetBusyRef(1);
			}

			if (movingitems)
			{
				// Update the status bar.
				var prevcopyitems = copyitems;

				copyitems = ('_fe_ctrl' in e ? e._fe_ctrl : e.ctrlKey);

				UpdateMoveCopyItemsDisplay(movenewpos, (prevcopyitems !== copyitems));

				// Update the overlay position.
				movecopyoverlay.style.left = (e.clientX - movecopyoverlaysize.xdiff) + 'px';
				movecopyoverlay.style.top = (e.clientY - movecopyoverlaysize.ydiff) + 'px';


// Implement similar auto-scroll behavior to selection boxes.
			}
		};

		// Handle scrolling using the wheel while moving/copying items.
		var MoveCopyScrollWheelHandler = function(e) {
			var lastscrolltop = -1;
			var numsame = 0;

			var TempWheelScrollHandler = function(e) {
				MoveCopyHandler(lastmouseevent);

				if (autoscrolltimer)  clearInterval(autoscrolltimer);

				autoscrolltimer = setInterval(TempWheelScrollHandler, 10);

				if (lastscrolltop !== elems.itemsscrollwrap.scrollTop)  numsame = 0;
				else
				{
					numsame++;

					if (numsame >= 5)
					{
						clearInterval(autoscrolltimer);

						autoscrolltimer = null;
					}
				}

				lastscrolltop = elems.itemsscrollwrap.scrollTop;
			};

			TempWheelScrollHandler();
		};

		// Alter the move/copy state on keydown/keyup.
		var MoveCopyCtrlKeyHandler = function(e) {
			if (!e.isTrusted)  return;

			if (movingitems)
			{
				e.preventDefault();

				var prevcopyitems = copyitems;

				lastmouseevent._fe_ctrl = e.ctrlKey;
				copyitems = e.ctrlKey;

				UpdateMoveCopyItemsDisplay(movenewpos, (prevcopyitems !== copyitems));
			}
		};

		var MoveCopyEndHandler = function(e) {
			if (e)
			{
				if (!e.isTrusted)  return;

				e.preventDefault();
			}
console.log('MoveCopyEndHandler');

			clearInterval(autoscrolltimer);
			autoscrolltimer = null;

			window.removeEventListener('mousemove', MoveCopyHandler, true);
			window.removeEventListener('mouseup', MoveCopyEndHandler, true);
			window.removeEventListener('blur', MoveCopyEndHandler, true);
			elems.itemsscrollwrap.removeEventListener('wheel', MoveCopyScrollWheelHandler);
			window.removeEventListener('keydown', MoveCopyCtrlKeyHandler, true);
			window.removeEventListener('keyup', MoveCopyCtrlKeyHandler, true);

			if (movecopyoverlay)
			{
				movecopyoverlay.parentNode.removeChild(movecopyoverlay);
				movecopyoverlay = null;
			}

			if (movingitems)
			{
				// Update the status bar with the final message and get the drop location.
				var droptarget = UpdateMoveCopyItemsDisplay(movenewpos, true, true);

				elems.itemswrap.classList.remove('fe_fileexplorer_items_move_copy');
				elems.itemswrap.classList.remove('fe_fileexplorer_items_copy');

//				// Restore the status bar to its previous state.
//				UpdateSelectionsChanged();

				currfolder.SetBusyRef(-1);
			}
		};
*/

		var StartSelectionHandler = function(e) {
			if (!e.isTrusted)  return;

			// Ignore when the target does not trace to the items wrapper.
			var node = e.target;

			while (node && node !== elems.itemsscrollwrap)  node = node.parentNode;

			if (!node)  return;

			// Don't start a selection operation if the folder is updating or busy.
			if (!currfolder || currfolder.waiting)  return;

			if (e.type === 'touchstart')
			{
				var rect = elems.itemsscrollwrapinner.getBoundingClientRect();

				lastselecttouch = {
					x: e.touches[0].clientX - rect.left,
					y: e.touches[0].clientY - rect.top,

					processed: false
				};

				selectanchorpos = lastselecttouch;
			}
			else
			{
				UpdateCurrFolderItemCache(false);

				// If the user has selected an item, focus it.
				if (e.target.classList.contains('fe_fileexplorer_item_wrap_inner') || e.target.closest('.fe_fileexplorer_item_wrap_inner'))
				{
					var elem = e.target.closest('.fe_fileexplorer_item_wrap');
					var orignumselected = numselecteditems;
					var origselecteditem = (elem.dataset.feid in selecteditemsmap);

					if (e.ctrlKey || e.target.tagName === 'INPUT' || e.button == 2 || selectmodemulti)
					{
						// Ctrl or checkbox.
						startrename = false;

						$this.SetFocusItem(elem.dataset.feid, true);
					}
					else
					{
						startrename = (!currfolder.IsBusy() && !e.shiftKey && $this.hasEventListener('rename') && numselecteditems === 1 && (elem.dataset.feid in selecteditemsmap) && e.target.classList.contains('fe_fileexplorer_item_text'));

						if (startrename)
						{
							startrenamefolder = currfolder;
							startrenameid = elem.dataset.feid;
						}

						$this.SetFocusItem(elem.dataset.feid, !e.shiftKey);

						// Select items starting at the last anchor position.
						if (e.shiftKey || !(elem.dataset.feid in selecteditemsmap))  $this.SelectItemsFromLastAnchor(true);
					}

					// Scroll the view to show the entire row containing the selected item.
					scrollnomoveinfo = { origelem: elem, origevent: e };
					window.addEventListener('mouseup', ScrollNoMoveHandler, true);

					// Enable right-click context menu.
					if (e.button == 2)
					{
						elems.itemsclipboardoverlay.value = '   ';
						elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_hidden');
						elems.itemsclipboardoverlaypastewrap.classList.add('fe_fileexplorer_items_clipboard_contextmenu');
					}

					if (orignumselected && (e.detail > 1 || (lastselecttouch && origselecteditem && lastmousedownevent && e.timeStamp - lastmousedownevent.timeStamp < 500)))
					{
						// Open selected items on double-click.
						$this.OpenSelectedItems();
					}
/*
					else if ($this.hasEventListener('move') || $this.hasEventListener('copy'))
					{
						// Start a move/copy operation.
						movingitems = false;

						lastmouseevent = e;

						var rect = elems.itemsscrollwrapinner.getBoundingClientRect();

						selectanchorpos = {
							x: e.clientX - rect.left,
							y: e.clientY - rect.top
						};
console.log(selectanchorpos);

						copyitems = e.ctrlKey;

						prevselectrect = {
							left: selectanchorpos.x,
							top: selectanchorpos.y,
							right: selectanchorpos.x,
							bottom: selectanchorpos.y
						};

						UpdateCalculatedSelectedItemsRect(prevselectrect);

						window.addEventListener('mousemove', MoveCopyHandler, true);
						window.addEventListener('mouseup', MoveCopyEndHandler, true);
						window.addEventListener('blur', MoveCopyEndHandler, true);
						elems.itemsscrollwrap.addEventListener('wheel', MoveCopyScrollWheelHandler);
						window.addEventListener('keydown', MoveCopyCtrlKeyHandler, true);
						window.addEventListener('keyup', MoveCopyCtrlKeyHandler, true);
					}
*/
				}
				else if (lastselecttouch && !lastselecttouch.processed)
				{
					if (e.detail == 2 || (e.detail < 2 && (!selectmodemulti || numselecteditems === 1)))
					{
						$this.ClearSelectedItems(true);
					}
					else if (e.detail == 3)
					{
						$this.SelectAllItems();

						selectmodemulti = (numselecteditems > 0);
					}
				}
				else
				{
					lastmouseevent = e;

					elems.itemsscrollwrap.focus();
					elems.itemswrap.classList.add('fe_fileexplorer_items_selecting');

					// Enable right-click context menu.
					if (e.button == 2)
					{
						elems.itemsclipboardoverlay.value = '   ';
						elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_hidden');
						elems.itemsclipboardoverlaypastewrap.classList.add('fe_fileexplorer_items_clipboard_contextmenu');
					}

					var rect = elems.itemsscrollwrapinner.getBoundingClientRect();

					selectanchorpos = {
						x: e.clientX - rect.left,
						y: e.clientY - rect.top
					};

					if (!e.ctrlKey && !e.shiftKey)  $this.ClearSelectedItems(true);

					selectchangeinvert = e.ctrlKey;

					currfolder.SetBusyRef(1);

					prevselectrect = {
						left: selectanchorpos.x,
						top: selectanchorpos.y,
						right: selectanchorpos.x,
						bottom: selectanchorpos.y
					};

					UpdateCalculatedSelectedItemsRect(prevselectrect);

					window.addEventListener('mousemove', SelectBoxDragHandler, true);
					window.addEventListener('mouseup', SelectBoxEndHandler, true);
					window.addEventListener('blur', SelectBoxEndHandler, true);
					elems.itemsscrollwrap.addEventListener('wheel', SelectBoxScrollWheelHandler);
				}

				lastmousedownevent = e;

				if (lastselecttouch)
				{
					if (!lastselecttouch.processed)  lastselecttouch.processed = true;
					else  lastselecttouch = null;
				}
			}
		};

		elems.itemsscrollwrapinner.addEventListener('mousedown', StartSelectionHandler);
		elems.itemsscrollwrapinner.addEventListener('touchstart', StartSelectionHandler);

		var CheckboxSelectedFixHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.target.tagName === 'INPUT')
			{
				// Make the checkmark match the selected status.  The browser tends to invert it when the checkbox is clicked.
				e.target.checked = e.target.parentNode.parentNode.classList.contains('fe_fileexplorer_item_selected');
			}
		};

		elems.itemsscrollwrapinner.addEventListener('click', CheckboxSelectedFixHandler);

		// Recent locations popup menu handler.
		var RecentLocationsHandler = function(e) {
			if (!e.isTrusted)  return;

			// Stop the button from stealing focus.
			e.preventDefault();

			// Cancel any existing popup menu.
			if (popupmenu)  popupmenu.Cancel();

			// Force focus for mousedown to the main area.
			if (e.type === 'mousedown')
			{
				var blockpopup = elems.navtool_history.classList.contains('fe_fileexplorer_block_popup');

				if (blockpopup)  elems.navtool_history.classList.remove('fe_fileexplorer_block_popup');

				if (!$this.HasFocus())  $this.Focus(true, true);
				else if (document.activeElement === elems.navtool_history)
				{
					// Keep the popup closed if it was open.
					$this.Focus(true, true);

					if (blockpopup)  return;
				}
			}

			// Setup popup menu options.
			var options = {
				items: [],

				onposition: function(popupelem) {
					popupelem.style.left = '1px';
					popupelem.style.top = (elems.toolbar.offsetTop + elems.toolbar.offsetHeight + 1) + 'px';
				},

				onselected: function(id, item, lastelem, etype) {
					popupmenu = null;
					$this.Focus(true);
					this.Destroy();

					currhistory = id;

					var newpath = foldermap[historystack[currhistory].folderkeys[historystack[currhistory].folderkeys.length - 1]].GetPath();

					$this.SetPath(newpath);
				},

				oncancel: function(lastelem, etype) {
					popupmenu = null;

					if (lastelem)  lastelem.focus();

					if (etype === 'mouse' && lastelem === elems.navtool_history)  elems.navtool_history.classList.add('fe_fileexplorer_block_popup');

					this.Destroy();
				}
			};

			// Set up menu items.
			var minnum = currhistory - 4;
			var maxnum = currhistory + 4;

			if (minnum < 0)
			{
				maxnum += -minnum;
				minnum = 0;
			}

			if (maxnum > historystack.length - 1)
			{
				minnum -= maxnum - (historystack.length - 1);
				if (minnum < 0)  minnum = 0;
				maxnum = historystack.length - 1;
			}

			for (var x = minnum; x <= maxnum; x++)
			{
				var temppath = foldermap[historystack[x].folderkeys[historystack[x].folderkeys.length - 1]].GetPath();
				var item = { id: x, name: EscapeHTML(temppath[temppath.length - 1][1]) };

				if (x < currhistory)  item.icon = 'fe_fileexplorer_popup_item_icon_back';
				else if (x > currhistory)  item.icon = 'fe_fileexplorer_popup_item_icon_forward';
				else  item.icon = 'fe_fileexplorer_popup_item_icon_check';

				options.items.unshift(item);
			}

			popupmenu = new PopupMenu(elems.mainwrap, options);
		};

		elems.navtool_history.addEventListener('mousedown', RecentLocationsHandler);

		var RecentLocationsKeyHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.keyCode == 13 || e.keyCode == 32)  RecentLocationsHandler(e);
		};

		elems.navtool_history.addEventListener('keydown', RecentLocationsKeyHandler);

		// Path segment handlers.
		var GetCurrentPathSegmentPos = function() {
			return elems.pathsegmentswrap._fepos;
		};

		var StartPathSegmentFolderSelection = function(node) {
			var posx = node.lastChild.offsetLeft - elems.pathsegmentsscrollwrap.scrollLeft + elems.pathsegmentsscrollwrap.offsetLeft - 18;
			var basepath = currfolder.GetPath();

			// Adjust basepath.
			basepath = basepath.slice(0, GetCurrentPathSegmentPos() + 1);

			// Apply styles.
			node.classList.add('fe_fileexplorer_path_segment_wrap_focus');
			node.classList.add('fe_fileexplorer_path_segment_wrap_down');

			// Cancel any existing popup menu.
			if (popupmenu)  popupmenu.Cancel();

			// Setup popup menu options.
			var options = {
				items: [],

				resizewatchers: [
					{ elem: document.body, attr: 'offsetWidth', val: -1 }
				],

				onposition: function(popupelem) {
					var posx2 = (posx + popupelem.offsetWidth < document.body.offsetWidth ? posx : document.body.offsetWidth - popupelem.offsetWidth - 1);

					popupelem.style.left = posx2 + 'px';
					popupelem.style.top = (elems.toolbar.offsetTop + elems.toolbar.offsetHeight) + 'px';
				},

				onselected: function(id, item, lastelem, etype) {
					popupmenu = null;
					$this.Focus(true);
					this.Destroy();

					// Append the selected path segment.
					var pathitem = [item.info.id, item.name];
					if ('attrs' in item.info)  pathitem.push(item.info.attrs);

					basepath.push(pathitem);

					$this.SetPath(basepath);
				},

				oncancel: function(lastelem, etype) {
					popupmenu = null;

					node.classList.remove('fe_fileexplorer_path_segment_wrap_focus');
					node.classList.remove('fe_fileexplorer_path_segment_wrap_down');

					if (lastelem)  lastelem.focus();

					if (etype === 'mouse' && lastelem.classList.contains('fe_fileexplorer_path_opts'))  node.classList.add('fe_fileexplorer_block_popup');

					this.Destroy();
				},

				onleft: function(lastelem) {
					var pos = GetCurrentPathSegmentPos();

					if (pos)
					{
						popupmenu = null;

						node.classList.remove('fe_fileexplorer_path_segment_wrap_focus');
						node.classList.remove('fe_fileexplorer_path_segment_wrap_down');

						// Don't let oncancel be called because it steals focus to the wrong element.
						this.PreventCancel();

						elems.pathsegmentswrap.children[pos - 1].focus();

						this.Destroy();

						StartPathSegmentFolderSelection(elems.pathsegmentswrap.children[pos - 1]);
					}
				},

				onright: function(lastelem) {
					var pos = GetCurrentPathSegmentPos();

					if (pos < elems.pathsegmentswrap.children.length - 1)
					{
						popupmenu = null;

						node.classList.remove('fe_fileexplorer_path_segment_wrap_focus');
						node.classList.remove('fe_fileexplorer_path_segment_wrap_down');

						// Don't let oncancel be called because it steals focus to the wrong element.
						this.PreventCancel();

						elems.pathsegmentswrap.children[pos + 1].focus();

						this.Destroy();

						StartPathSegmentFolderSelection(elems.pathsegmentswrap.children[pos + 1]);
					}
				}
			};

			// Set up menu items.
			var entries = $this.GetMappedFolderFromPath(basepath);

			if (entries)
			{
				entries = entries.GetEntries();

				for (var x = 0; x < entries.length; x++)
				{
					if (entries[x].type === 'folder')
					{
						var item = { id: options.items.length, name: EscapeHTML(entries[x].name), icon: 'fe_fileexplorer_popup_item_icon_folder', info: entries[x] };

						options.items.push(item);
					}
				}

				popupmenu = new PopupMenu(elems.mainwrap, options);
			}
		};

		var PathSegmentMouseFocusHandler = function(e) {
			if (!e.isTrusted)  return;

			// Provide our own focus handling.
			e.preventDefault();

			// Find the node with a valid tab index.
			var tabnode = elems.pathsegmentswrap.children[elems.pathsegmentswrap._fepos];

			var node = e.target;
			while (node && node !== elems.pathsegmentsscrollwrap)
			{
				if (node.parentNode === elems.pathsegmentswrap)
				{
					node.focus();

					break;
				}

				node = node.parentNode;
			}

			if (node && node === elems.pathsegmentsscrollwrap && tabnode)  tabnode.focus();

			// Open the menu if the collapse button was not clicked.
			if (node && e.target.classList.contains('fe_fileexplorer_path_opts'))
			{
				var blockpopup = node.classList.contains('fe_fileexplorer_block_popup');

				if (blockpopup)  node.classList.remove('fe_fileexplorer_block_popup');
				else  StartPathSegmentFolderSelection(node);
			}
		};

		elems.pathsegmentsscrollwrap.addEventListener('mousedown', PathSegmentMouseFocusHandler);

		var PathSegmentFocusScrollHandler = function(e) {
			var node = e.target;

			if (node.parentNode === elems.pathsegmentswrap)
			{
				if (elems.pathsegmentswrap._fepos !== node._fepos)
				{
					node.tabIndex = 0;

					elems.pathsegmentswrap.children[elems.pathsegmentswrap._fepos].tabIndex = -1;

					elems.pathsegmentswrap._fepos = node._fepos;
				}

				if (node.offsetLeft - 1 < elems.pathsegmentsscrollwrap.scrollLeft)  elems.pathsegmentsscrollwrap.scrollLeft = node.offsetLeft - 1;
				else if (node.offsetLeft + node.offsetWidth + 1 > elems.pathsegmentsscrollwrap.scrollLeft + elems.pathsegmentsscrollwrap.clientWidth)  elems.pathsegmentsscrollwrap.scrollLeft = (node.offsetLeft + node.offsetWidth + 1) - elems.pathsegmentsscrollwrap.clientWidth;
			}
		};

		elems.pathsegmentsscrollwrap.addEventListener('focus', PathSegmentFocusScrollHandler, true);

		var PathSegmentClickHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.target.classList.contains('fe_fileexplorer_path_name'))
			{
				// Go to the selected folder.
				var currpath = currfolder.GetPath();

				$this.SetPath(currpath.slice(0, GetCurrentPathSegmentPos() + 1));

				$this.Focus(true);
			}
		};

		elems.pathsegmentsscrollwrap.addEventListener('click', PathSegmentClickHandler);

		var PathSegmentKeyHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.keyCode == 37)
			{
				// Left Arrow.  Move to previous path segment.
				e.preventDefault();

				var pos = GetCurrentPathSegmentPos();

				if (pos)  elems.pathsegmentswrap.children[pos - 1].focus();
			}
			else if (e.keyCode == 39)
			{
				// Right Arrow.  Move to next path segment.
				var pos = GetCurrentPathSegmentPos();

				if (pos < elems.pathsegmentswrap.children.length - 1)
				{
					e.preventDefault();

					elems.pathsegmentswrap.children[pos + 1].focus();
				}
			}
			else if (e.keyCode == 13)
			{
				// Enter.  Go to path.
				e.preventDefault();

				// Go to the selected folder.
				var currpath = currfolder.GetPath();

				$this.SetPath(currpath.slice(0, GetCurrentPathSegmentPos() + 1));

				$this.Focus(true);
			}
			else if (e.keyCode == 40)
			{
				// Down Arrow.  Show the subfolder selection menu.
				e.preventDefault();

				var node = elems.pathsegmentswrap.children[GetCurrentPathSegmentPos()];

				node.focus();

				StartPathSegmentFolderSelection(node);
			}
		};

		elems.pathsegmentsscrollwrap.addEventListener('keydown', PathSegmentKeyHandler);

		// Clipboard cut/copy handler.
		var ClipboardCutCopyHandler = function(e) {
			if (!e.isTrusted)  return;

			// Do not handle cut/copy when the paste box is showing.
			if (elems.itemsclipboardoverlaypastewrap.classList.contains('fe_fileexplorer_items_show_clipboard_overlay_paste'))  return;

			e.preventDefault();

			if (numselecteditems)
			{
				var ids = [];

				for (var x in selecteditemsmap)
				{
					if (selecteditemsmap.hasOwnProperty(x))  ids.push(x);
				}

				var dropeffect = (e.type === 'copy' ? 'copy' : 'move');

				e.clipboardData.dropEffect = dropeffect;
				e.clipboardData.setData('application/file-explorer-clipboard', JSON.stringify({ type: dropeffect, source: main_id, group: main_group, path: currfolder.GetPath(), ids: ids }));
				e.clipboardData.setData('text/plain', JSON.stringify({ 'application/file-explorer-clipboard' : { type: dropeffect, source: main_id, group: main_group, path: currfolder.GetPath(), ids: ids } }));

				// Chromium DownloadURL support.
				if (e.type === 'copy' && $this.hasEventListener('get_download_url'))
				{
					// Synchronous call only.
					var entries = currfolder.GetEntries();
					var entryidmap = currfolder.GetEntryIDMap();
					var entry = entries[entryidmap[ids[0]]];
					var result = {};

					DispatchEvent('get_download_url', [result, currfolder, ids, entry]);

					if (result && result.name && result.url)  e.clipboardData.setData('DownloadURL', 'application/octet-stream:' + result.name + ':' + result.url);
				}

				$this.SetNamedStatusBarText('message', EscapeHTML($this.Translate((e.type === 'copy' ? 'Copy' : 'Cut') + ' to clipboard completed')), $this.settings.messagetimeout);
			}

			ClipboardOverlayExitContextMenuHandler(e);
		};

		// Clipboard paste handler.
		var ClipboardPasteHandler = function(e) {
			if (!e.isTrusted)  return;

			e.preventDefault();

			// Attempt to read the dropped clipboard data.
			var dropdata;
			try
			{
				dropdata = JSON.parse(e.clipboardData.getData('application/file-explorer-clipboard'));
			}
			catch(err)
			{
				try
				{
					// Attempt to extract a text/plain variant.
					var data = JSON.parse(e.clipboardData.getData('text/plain'));

					if (data['application/file-explorer-clipboard'])  dropdata = data['application/file-explorer-clipboard'];
				}
				catch(err)
				{
				}
			}

			if (dropdata && dropdata.group === main_group && Array.isArray(dropdata.path) && Array.isArray(dropdata.ids) && dropdata.ids.length && ((dropdata.type === 'copy' && $this.hasEventListener('copy')) || (dropdata.type === 'move' && $this.hasEventListener('move'))))
			{
				var lasttype = 'currfolder', lastnode = null;

				// If the clipboard context menu was used and the target focused item is a folder, then copy/move to the folder.
				if (clipboardcontextmenu && focuseditem !== false && focuseditem.classList.contains('fe_fileexplorer_item_folder'))
				{
					lasttype = 'item';
					lastnode = focuseditem;
				}

				// Update the status bar with a description of the operation.
				var str = (dropdata.type === 'copy' ? 'Copying' : 'Moving');

				str += (dropdata.ids.length === 1 ? ' 1 item' : ' {0} items');

				if (lasttype === 'currfolder')
				{
					var path = currfolder.GetPath();

					$this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate(str + ' to "{1}"...'), dropdata.ids.length, path[path.length - 1][1])));
				}
				else
				{
					var entries = currfolder.GetEntries();
					var entryidmap = currfolder.GetEntryIDMap();
					var entry = entries[entryidmap[lastnode.dataset.feid]];

					$this.SetNamedStatusBarText('selected', EscapeHTML(FormatStr($this.Translate(str + ' to "{1}"...'), dropdata.ids.length, entry.name)));
				}

				currfolder.SetBusyRef(1);

				PerformFinalMoveCopy((dropdata.source === main_id), lasttype, lastnode, dropdata.type, dropdata);
			}
			else if (!dropdata && e.clipboardData.files && e.clipboardData.files.length)
			{
				// Pasted a browser-compatible file blob (e.g. an image).
				$this.ProcessFilesAndUpload('currfolder', null, e.clipboardData);
			}
			else
			{
				if (dropdata && dropdata.group !== main_group)  $this.SetNamedStatusBarText('message', EscapeHTML($this.Translate('Paste operation failed due to mismatched group name')), $this.settings.messagetimeout);
				else  $this.SetNamedStatusBarText('message', EscapeHTML($this.Translate('Paste operation failed')), $this.settings.messagetimeout);
			}

			ClipboardOverlayExitContextMenuHandler(e);
		};

		elems.itemsclipboardoverlay.addEventListener('cut', ClipboardCutCopyHandler);
		elems.itemsclipboardoverlay.addEventListener('copy', ClipboardCutCopyHandler);
		elems.itemsclipboardoverlay.addEventListener('paste', ClipboardPasteHandler);

		// Item selection keyboard handler.
		var lasttypingts = 0, lasttypingstr = '';
		var ItemsKeyHandler = function(e) {
			if (!e.isTrusted || e.altKey)  return;

			var updatefocus = false;

			if (e.keyCode == 37)
			{
				// Left Arrow.  Move item selection left.
				e.preventDefault();

				UpdateCurrFolderItemCache(false);

				// Change focus to the previous item.
				if (focuseditem !== false)
				{
					if (focuseditem.previousSibling)
					{
						$this.SetFocusItem(focuseditem.previousSibling.dataset.feid, (!e.ctrlKey && !e.shiftKey));

						updatefocus = true;
					}
				}
				else if (folderitemcache.size)
				{
					$this.SetFocusItem(elems.itemswrap.firstChild.dataset.feid, (!e.ctrlKey && !e.shiftKey));

					updatefocus = true;
				}
			}
			else if (e.keyCode == 39)
			{
				// Right Arrow.  Move item selection right.
				e.preventDefault();

				UpdateCurrFolderItemCache(false);

				// Change focus to the next item.
				if (focuseditem !== false)
				{
					if (focuseditem.nextSibling)
					{
						$this.SetFocusItem(focuseditem.nextSibling.dataset.feid, (!e.ctrlKey && !e.shiftKey));

						updatefocus = true;
					}
				}
				else if (folderitemcache.size)
				{
					$this.SetFocusItem(elems.itemswrap.firstChild.dataset.feid, (!e.ctrlKey && !e.shiftKey));

					updatefocus = true;
				}
			}
			else if (e.keyCode == 38)
			{
				// Up Arrow.  Move item selection up.
				e.preventDefault();

				UpdateCurrFolderItemCache(false);

				// Change focus to the next row.
				if (focuseditem !== false)
				{
					if (focuseditem.offsetTop !== folderitemcache.rows[0].top)
					{
						var num = folderitemcache.cols.length;
						var node = focuseditem;

						while (node.previousSibling && num)
						{
							node = node.previousSibling;

							num--;
						}

						if (node !== focuseditem)
						{
							$this.SetFocusItem(node.dataset.feid, (!e.ctrlKey && !e.shiftKey));

							updatefocus = true;
						}
					}
				}
				else if (folderitemcache.size)
				{
					$this.SetFocusItem(elems.itemswrap.firstChild.dataset.feid, (!e.ctrlKey && !e.shiftKey));

					updatefocus = true;
				}
			}
			else if (e.keyCode == 40)
			{
				// Down Arrow.  Move item selection down.
				e.preventDefault();

				UpdateCurrFolderItemCache(false);

				// Change focus to the next row.
				if (focuseditem !== false)
				{
					if (focuseditem.offsetTop !== folderitemcache.rows[folderitemcache.rows.length - 1].top)
					{
						var num = folderitemcache.cols.length;
						var node = focuseditem;

						while (node.nextSibling && num)
						{
							node = node.nextSibling;

							num--;
						}

						if (node !== focuseditem)
						{
							$this.SetFocusItem(node.dataset.feid, (!e.ctrlKey && !e.shiftKey));

							updatefocus = true;
						}
					}
				}
				else if (folderitemcache.size)
				{
					$this.SetFocusItem(elems.itemswrap.firstChild.dataset.feid, (!e.ctrlKey && !e.shiftKey));

					updatefocus = true;
				}
			}
			else if (e.keyCode == 36)
			{
				// Home.  Move to first item.
				UpdateCurrFolderItemCache(false);

				// Change focus to the first item.
				if (folderitemcache.size)
				{
					$this.SetFocusItem(elems.itemswrap.firstChild.dataset.feid, (!e.ctrlKey && !e.shiftKey));

					updatefocus = true;
				}
			}
			else if (e.keyCode == 35)
			{
				// End.  Move to last item.
				UpdateCurrFolderItemCache(false);

				// Change focus to the first item.
				if (folderitemcache.size)
				{
					$this.SetFocusItem(elems.itemswrap.lastChild.dataset.feid, (!e.ctrlKey && !e.shiftKey));

					updatefocus = true;
				}
			}
			else if (e.keyCode == 32)
			{
				// Space.  Select currently focused item OR find an item if typing.
				e.preventDefault();

				UpdateCurrFolderItemCache(false);

				var ts = Date.now() - 1000;

				if (lasttypingts > ts)
				{
					// The preventDefault() stops the keypress event, so fake it.
					e.key = ' ';
					ItemsKeypressHandler(e);
				}
				else
				{
					if (focuseditem === false && folderitemcache.size)
					{
						$this.SetFocusItem(elems.itemswrap.firstChild.dataset.feid, (!e.ctrlKey && !e.shiftKey));

						updatefocus = true;
					}

					if (focuseditem !== false)
					{
						if (e.ctrlKey)
						{
							$this.SetFocusItem(focuseditem.dataset.feid, true);

							// Toggle item selection.  Skip toolbar and status bar update.
							$this.ToggleItemSelection(focuseditem, false, true);
						}

						updatefocus = true;
					}
				}
			}
			else if (e.keyCode == 13)
			{
				// Enter.
				e.preventDefault();

				$this.OpenSelectedItems();
			}
			else if (e.keyCode == 46)
			{
				// Delete.
				e.preventDefault();

				$this.DeleteSelectedItems(!e.shiftKey);
			}
			else if ((e.ctrlKey || e.metaKey) && (e.keyCode == 88 || e.keyCode == 67))
			{
				// Ctrl/Meta + X/C.  Cut/Copy selections onto the clipboard.
				if (numselecteditems)
				{
					elems.itemsclipboardoverlay.value = '';
					elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_hidden');
					elems.itemsclipboardoverlay.focus();

					elems.itemsclipboardoverlay.addEventListener('keyup', ClipboardOverlayKeyHandler);
				}
			}
			else if ((e.ctrlKey || e.metaKey) && e.keyCode == 86)
			{
				// Ctrl/Meta + V.  Paste content from the clipboard.
				elems.itemsclipboardoverlay.value = '';
				elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_hidden');
				elems.itemsclipboardoverlay.focus();

				elems.itemsclipboardoverlay.addEventListener('keyup', ClipboardOverlayKeyHandler);
			}
			else if (e.keyCode == 93)
			{
				// Context Menu.  Alternative method to Cut/Copy/Paste selections onto/from the clipboard.
				elems.itemsclipboardoverlay.value = '   ';
				elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_hidden');
				elems.itemsclipboardoverlay.classList.add('fe_fileexplorer_items_clipboard_contextmenu');

				StartClipboardOverlayMenu();
			}

			// Update scroll position and selections if the focus changed.
			if (updatefocus)
			{
				$this.ScrollToFocusedItem();

				// Update selections.
				if (focuseditem !== false)
				{
					// Select items starting at the last anchor position.  Skip updating the toolbar and selections.
					if (!e.ctrlKey)  $this.SelectItemsFromLastAnchor(false, true);

					// Update toolbar icons.
					UpdateToolbarIcons();

					// Update the status bar and notify listeners.
					UpdateSelectionsChanged();
				}
			}
		};

		elems.itemsscrollwrap.addEventListener('keydown', ItemsKeyHandler);

		var lastkey = '';
		var ItemsKeypressHandler = function(e) {
			if (!elems.itemswrap.children.length)  return;

			var ts = Date.now();

			if (lasttypingts > ts - 1000)  lasttypingstr += e.key;
			else  lasttypingstr = e.key;

			lasttypingts = ts;

			// Attempt to find the next match.
			var found = false;
			var entries = currfolder.GetEntries();
			var entryidmap = currfolder.GetEntryIDMap();
			var node = (focuseditem !== false && focuseditem.nextSibling ? focuseditem.nextSibling : elems.itemswrap.firstChild);
			var pos = entryidmap[node.dataset.feid];

			while (node)
			{
				if (lasttypingstr.localeCompare(entries[pos].name.substring(0, lasttypingstr.length), undefined, { sensitivity: 'base' }) === 0)
				{
					found = true;

					break;
				}

				node = node.nextSibling;
				pos++;
			}

			if (!found && focuseditem !== false)
			{
				node = elems.itemswrap.firstChild;
				pos = 0;
				while (node && node !== focuseditem)
				{
					if (lasttypingstr.localeCompare(entries[pos].name.substring(0, lasttypingstr.length), undefined, { sensitivity: 'base' }) === 0)
					{
						found = true;

						break;
					}

					node = node.nextSibling;
					pos++;
				}
			}

			// If the same starting key is pressed multiple times, attempt to start over.
			if (!found && lasttypingstr.length == 2 && lastkey === e.key)
			{
				lasttypingstr = '';
				ItemsKeypressHandler(e);
			}

			if (found)
			{
				// Focus on the node.
				$this.SetFocusItem(node.dataset.feid, true);

				$this.ScrollToFocusedItem();

				// Select items starting at the last anchor position.
				$this.SelectItemsFromLastAnchor();
			}

			lastkey = e.key;
		};

		elems.itemsscrollwrap.addEventListener('keypress', ItemsKeypressHandler);

		// Global keyboard handler.
		var MainKeyHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.ctrlKey && e.keyCode == 65)
			{
				// Ctrl + A.  Select all items.
				e.preventDefault();

				$this.Focus(true);

				$this.SelectAllItems();
			}
			else if ((e.altKey && e.keyCode == 37) || e.keyCode == 8)
			{
				// Backspace or Alt + Left Arrow.  Navigate back.
				e.preventDefault();

				$this.HistoryBack();
			}
			else if (e.altKey && e.keyCode == 39)
			{
				// Alt + Right Arrow.  Navigate forward.
				e.preventDefault();

				$this.HistoryForward();
			}
			else if (e.altKey && e.keyCode == 38)
			{
				// Alt + Up Arrow.  Set the path to the parent folder.
				e.preventDefault();

				$this.NavigateUp();
			}
			else if (e.keyCode == 113)
			{
				// F2.  Start renaming a selected item.
				if ($this.hasEventListener('rename'))
				{
					e.preventDefault();

					$this.RenameSelectedItem();
				}
			}

			// Re-dispatch this event to tools.
			DispatchEvent('keydown', e);
		};

		elems.innerwrap.addEventListener('keydown', MainKeyHandler);


		// Public functions.

		// Checks to see if the active element is part of the main UI.
		$this.HasFocus = function(itemsonly) {
			var node = document.activeElement;

			if (itemsonly)
			{
				while (node && node !== elems.itemsscrollwrap)  node = node.parentNode;

				return (node === elems.itemsscrollwrap);
			}
			else
			{
				while (node && node !== elems.mainwrap)  node = node.parentNode;

				return (node === elems.mainwrap);
			}
		};

		// Triggers focusing of the main UI.  Useful for popups.
		$this.Focus = function(itemsonly, alwaysfocus) {
			var node = document.activeElement;

			if (alwaysfocus)
			{
			}
			else if (itemsonly)
			{
				while (node && node !== elems.itemsscrollwrap)  node = node.parentNode;

				if (node !== elems.itemsscrollwrap)  alwaysfocus = true;
			}
			else
			{
				while (node && node !== elems.mainwrap)  node = node.parentNode;

				if (node !== elems.mainwrap)  alwaysfocus = true;
			}

			if (alwaysfocus)
			{
				if (focuseditem !== false)  focuseditem.firstChild.focus();
				else  elems.itemsscrollwrap.focus();
			}
		};

		// Checks to see if the active element is an item.
		$this.HasItemFocus = function() {
			var node = document.activeElement;

			return (focuseditem !== false && node && node.parentNode === focuseditem);
		};

		// Returns the currently focused item node.
		$this.GetFocusedItem = function() {
			return focuseditem;
		};

		// Returns the currently focused item ID.
		$this.GetFocusedItemID = function() {
			return (focuseditem !== false ? focuseditem.dataset.feid : false);
		};

		// Returns whether or not the specified folder is in the refcounted folder map.
		// This can return false if the user navigated back during a complex operation (e.g. rename, Destroy() called).
		$this.IsMappedFolder = function(folder) {
			if (currfolder === folder)  return true;

			for (var x in foldermap)
			{
				if (foldermap.hasOwnProperty(x) && folder === foldermap[x])  return true;
			}

			return false;
		};

		// Returns the current folder.
		$this.GetCurrentFolder = function() {
			return currfolder;
		};

		// Returns selected item IDs.
		$this.GetSelectedItemIDs = function() {
			var result = [];

			for (var x in selecteditemsmap)
			{
				if (selecteditemsmap.hasOwnProperty(x))  result.push(x);
			}

			return result;
		};

		$this.GetSelectedFolderEntries = function() {
			var entries = currfolder.GetEntries();
			var result = [];

			for (var x = 0; x < entries.length; x++)
			{
				if (entries[x].id in selecteditemsmap)  result.push(entries[x]);
			}

			return result;
		};

		// Returns whether or not the specified item is selected.
		$this.IsSelectedItem = function(id) {
			return (id in selecteditemsmap);
		};

		// Sets selected items.
		$this.SetSelectedItems = function(ids, keepprev, skipuiupdate) {
			// If the current folder is busy, then queue the change for later.
			if (currfolder && currfolder.IsBusy())
			{
				currfolder.AddBusyQueueCallback($this.SetSelectedItems, [ids]);

				return;
			}

			if (!currfolder || currfolder.waiting)  return;

			if (!Array.isArray(ids))  return;

			if (!keepprev)  $this.ClearSelectedItems(false, true);

			var entryidmap = currfolder.GetEntryIDMap();

			for (var x = 0; x < ids.length; x++)
			{
				if ((ids[x] in entryidmap) && !(ids[x] in selecteditemsmap))
				{
					var entrynum = entryidmap[ids[x]];
					var elem = elems.itemswrap.children[entrynum];

					elem.classList.add('fe_fileexplorer_item_selected');
					elem.firstChild.firstChild.checked = true;

					selecteditemsmap[elem.dataset.feid] = entrynum;
					numselecteditems++;
				}
			}

			if (!skipuiupdate)
			{
				// Update toolbar icons.
				UpdateToolbarIcons();

				// Update the status bar and notify listeners.
				UpdateSelectionsChanged();
			}
		};

		// Get the number of selected items.
		$this.GetNumSelectedItems = function() {
			return numselecteditems;
		};

		// Navigates to the parent folder.
		$this.NavigateUp = function(e) {
			if (e)  e.preventDefault();

			if (!currfolder)  return;

			var currpath = currfolder.GetPath();

			if (currpath.length > 1)  $this.SetPath(currpath.slice(0, -1));
		};

		var ClickNavigateUpHandler = function(e) {
			if (!e.isTrusted)  return;

			$this.NavigateUp(e);
			$this.Focus(true);
		};

		elems.navtool_up.addEventListener('mouseup', ClickNavigateUpHandler);

		var NavigateUpKeyHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.keyCode == 13 || e.keyCode == 32)
			{
				$this.NavigateUp(e);

				// Steal focus back from the main area.  This needs to happen to allow focused item scrolling to take place.
				if (elems.navtool_up.tabIndex == 0)  elems.navtool_up.focus();
				else  elems.navtool_history.focus();
			}
		};

		elems.navtool_up.addEventListener('keydown', NavigateUpKeyHandler);

		// Navigates back one history level.
		$this.HistoryBack = function(e) {
			if (e)  e.preventDefault();

			if (currhistory > 0)
			{
				currhistory--;

				var newpath = foldermap[historystack[currhistory].folderkeys[historystack[currhistory].folderkeys.length - 1]].GetPath();

				$this.SetPath(newpath);
			}
		};

		var ClickHistoryBackHandler = function(e) {
			if (!e.isTrusted)  return;

			$this.HistoryBack(e);
			$this.Focus(true);
		};

		elems.navtool_back.addEventListener('mouseup', ClickHistoryBackHandler);

		var HistoryBackKeyHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.keyCode == 13 || e.keyCode == 32)
			{
				$this.HistoryBack(e);

				// Steal focus back from the main area.  This needs to happen to allow focused item scrolling to take place.
				if (currhistory > 0)  elems.navtool_back.focus();
				else if (currhistory < historystack.length - 1)  elems.navtool_forward.focus();
				else  elems.navtool_history.focus();
			}
		};

		elems.navtool_back.addEventListener('keydown', HistoryBackKeyHandler);

		// Navigates forward one history level.
		$this.HistoryForward = function(e) {
			if (e)  e.preventDefault();

			if (currhistory > -1 && currhistory < historystack.length - 1)
			{
				currhistory++;

				var newpath = foldermap[historystack[currhistory].folderkeys[historystack[currhistory].folderkeys.length - 1]].GetPath();

				$this.SetPath(newpath);
			}
		};

		var ClickHistoryForwardHandler = function(e) {
			if (!e.isTrusted)  return;

			$this.HistoryForward(e);
			$this.Focus(true);
		};

		elems.navtool_forward.addEventListener('mouseup', ClickHistoryForwardHandler);

		var HistoryForwardKeyHandler = function(e) {
			if (!e.isTrusted)  return;

			if (e.keyCode == 13 || e.keyCode == 32)
			{
				$this.HistoryForward(e);

				// Steal focus back from the main area.  This needs to happen to allow focused item scrolling to take place.
				if (currhistory < historystack.length - 1)  elems.navtool_forward.focus();
				else if (currhistory > 0)  elems.navtool_back.focus();
				else  elems.navtool_history.focus();
			}
		};

		elems.navtool_forward.addEventListener('keydown', HistoryForwardKeyHandler);

		// Returns the internal elements object for use with certain tools.
		$this.GetElements = function() {
			return elems;
		};

		// Export internal functions.  Useful for creating custom tools.
		$this.EscapeHTML = EscapeHTML;
		$this.FormatStr = FormatStr;
		$this.GetDisplayFilesize = GetDisplayFilesize;
		$this.CreateNode = CreateNode;
		$this.DebounceAttributes = DebounceAttributes;
		$this.PrepareXHR = PrepareXHR;

		$this.GetScrollLineHeight = function() {
			return scrolllineheight;
		};

		// Starts an indicator for a long-running operation (e.g rename).
		var operationtimeout = null, operationrefs = 0;
		$this.StartOperationIndicator = function() {
			operationrefs++;

			elems.innerwrap.classList.add('fe_fileexplorer_operation_in_progress');

			if (operationtimeout)  clearTimeout(operationtimeout);

			operationtimeout = setTimeout(function() {
				elems.innerwrap.classList.remove('fe_fileexplorer_operation_in_progress');

				operationtimeout = null;

				operationrefs = 0;
			}, 15000);
		};

		// Stops the indicator used for long-running operations (e.g. rename).
		$this.StopOperationIndicator = function() {
			operationrefs--;

			if (operationrefs <= 0)
			{
				elems.innerwrap.classList.remove('fe_fileexplorer_operation_in_progress');

				if (operationtimeout)
				{
					clearTimeout(operationtimeout);

					operationtimeout = null;
				}

				operationrefs = 0;
			}
		};

		// Renames the selected item if only one item is selected.
		var textareaoverlayinst;
		$this.RenameSelectedItem = function() {
			if (currfolder && currfolder.IsBusy())
			{
				currfolder.AddBusyQueueCallback($this.RenameSelectedItem, []);

				return;
			}

			if (!currfolder || currfolder.waiting || (('canmodify' in currfolder.GetAttributes()) && !currfolder.GetAttributes().canmodify))  return;

			if (!$this.hasEventListener('rename') || numselecteditems !== 1)  return;

			var pos = -1;
			var node = null;
			for (var x in selecteditemsmap)
			{
				if (selecteditemsmap.hasOwnProperty(x))
				{
					pos = selecteditemsmap[x];
					node = elems.itemswrap.children[pos];
				}
			}

			if (!node)  return;

			$this.SetFocusItem(node.dataset.feid, true);

			node.firstChild.lastChild.classList.add('fe_fileexplorer_invisible');

			var origfolder = currfolder;
			var entries = currfolder.GetEntries();
			var origentry = entries[pos];
			var pos2 = origentry.name.lastIndexOf('.');

			currfolder.SetBusyRef(1);

			var options = {
				initvalue: origentry.name,
				initselstart: 0,
				initselend: (origentry.type === 'file' && pos2 > 0 ? pos2 : -1),

				resizewatchers: [
					{ elem: node, attr: 'offsetLeft', val: -1 },
					{ elem: elems.itemsscrollwrap, attr: 'offsetHeight', val: -1 }
				],

				onposition: function(textelem) {
					// Size the textarea so it expands first toward the bottom of the scroll region and then toward the top of the scroll region.
					textelem.style.left = node.offsetLeft + 'px';
					textelem.style.width = node.offsetWidth + 'px';

					var finalheight = Math.min(elems.itemsscrollwrap.offsetHeight - 1, textelem.scrollHeight + 2);
					textelem.style.top = (node.offsetTop + node.firstChild.lastChild.offsetTop - 2 + finalheight <= elems.itemsscrollwrap.scrollTop + elems.itemsscrollwrap.offsetHeight - 2 ? node.offsetTop + node.firstChild.lastChild.offsetTop - 2 : elems.itemsscrollwrap.scrollTop + elems.itemsscrollwrap.offsetHeight - 2 - finalheight) + 'px';
					textelem.style.height = finalheight + 'px';
				},

				ondone: function(val, lastelem, etype) {
					var $this2 = this;

					var calledback = false;
					var renamecallback = function(newentry) {
						if (calledback || destroyinprogress)  return;

						calledback = true;

						$this.StopOperationIndicator();

						if (typeof newentry === 'object')
						{
							node.firstChild.lastChild.classList.remove('fe_fileexplorer_invisible');

							$this.SetNamedStatusBarText('message', '');

							if (lastelem && focuseditem && lastelem === focuseditem.firstChild)
							{
								lastelem.focus();

								$this.ScrollToFocusedItem();
							}

							textareaoverlayinst = null;

							// May trigger various changes including folder navigation.
							currfolder.SetBusyRef(-1);

							if ($this.IsMappedFolder(origfolder))
							{
								origfolder.SetEntry(newentry);

								// If the item ID changed, then update focus and selection information and remove the original entry.
								if (origentry.id !== newentry.id)
								{
									if (currfolder === origfolder)
									{
										if (focuseditem !== false && origentry.id === focuseditem.dataset.feid)
										{
											$this.SetFocusItem(newentry.id, true);

											$this.ScrollToFocusedItem();
										}

										if (origentry.id in selecteditemsmap)  $this.SetSelectedItems([newentry.id], true);
									}

									origfolder.RemoveEntry(origentry.id);
								}

								$this2.Destroy();
							}
						}
						else
						{
							// Reset the widget status.
							$this2.ResetAllowCancelDone();

							$this.SetNamedStatusBarText('message', EscapeHTML(FormatStr($this.Translate('Renaming "{0}" to "{1}" failed.' + (typeof newentry === 'string' ? '  {2}' : '')), origentry.name, val, newentry)), $this.settings.messagetimeout);
						}
					};

					$this.StartOperationIndicator();

					$this.SetNamedStatusBarText('message', EscapeHTML(FormatStr($this.Translate('Renaming "{0}" to "{1}"...'), origentry.name, val)), $this.settings.messagetimeout);

					// Creates a copy of the original entry to pass to the rename event handler.
					DispatchEvent('rename', [renamecallback, currfolder, Object.assign({}, origentry), val]);
				},

				oncancel: function(lastelem, etype) {
					node.firstChild.lastChild.classList.remove('fe_fileexplorer_invisible');

					if (lastelem && focuseditem && lastelem === focuseditem.firstChild)
					{
						lastelem.focus();

						$this.ScrollToFocusedItem();
					}

					textareaoverlayinst = null;

					this.Destroy();

					currfolder.SetBusyRef(-1);
				},
			};

			textareaoverlayinst = new TextareaOverlay(elems.itemsscrollwrapinner, options);
		};

		// Deletes selected items.
		$this.DeleteSelectedItems = function(recycle) {
			if (currfolder && currfolder.IsBusy())
			{
				currfolder.AddBusyQueueCallback($this.DeleteSelectedItems, [recycle]);

				return;
			}

			if (!currfolder || currfolder.waiting || (('canmodify' in currfolder.GetAttributes()) && !currfolder.GetAttributes().canmodify))  return;

			if (!$this.hasEventListener('delete') || !numselecteditems)  return;

			currfolder.SetBusyRef(1);

			// Copy existing objects for later use.
			var origfolder = currfolder;
			var selecteditemsmap2 = Object.assign({}, selecteditemsmap);
			var numselecteditems2 = numselecteditems;

			var calledback = false;
			var deletecallback = function(success) {
				if (calledback || destroyinprogress)  return;

				calledback = true;

				$this.StopOperationIndicator();

				if (!$this.IsMappedFolder(origfolder))  return;

				if (success === true)
				{
					$this.SetNamedStatusBarText('message', '');

					currfolder.SetBusyRef(-1);

					if (currfolder === origfolder)
					{
						if (numselecteditems2 === 1)
						{
							// Removing a single entry is slightly less expensive than removing multiple entries.
							for (var x in selecteditemsmap2)
							{
								if (selecteditemsmap2.hasOwnProperty(x))
								{
									if (focuseditem !== false && focuseditem.dataset.feid === x)
									{
										if (focuseditem.nextSibling)  $this.SetFocusItem(focuseditem.nextSibling.dataset.feid, true);
										else if (focuseditem.previousSibling)  $this.SetFocusItem(focuseditem.previousSibling.dataset.feid, true);

										$this.ScrollToFocusedItem();
									}

									currfolder.RemoveEntry(x);
								}
							}
						}
						else
						{
							var entries = currfolder.GetEntries();
							var entries2 = [];
							for (var x = 0; x < entries.length; x++)
							{
								if (!(entries[x].id in selecteditemsmap2))  entries2.push(entries[x]);
							}

							// Adjust the focused item.
							if (focuseditem !== false && (focuseditem.dataset.feid in selecteditemsmap2))
							{
								var node = focuseditem.nextSibling;
								while (node && (node.dataset.feid in selecteditemsmap2))  node = node.nextSibling;

								if (!node)
								{
									node = focuseditem.previousSibling;
									while (node && (node.dataset.feid in selecteditemsmap2))  node = node.previousSibling;
								}

								if (node)
								{
									$this.SetFocusItem(node.dataset.feid, true);
									$this.ScrollToFocusedItem();
								}
							}

							currfolder.SetEntries(entries2);
						}

						$this.RefreshFolders();
					}
				}
				else
				{
					$this.SetNamedStatusBarText('message', EscapeHTML(FormatStr($this.Translate('Deleting items failed.' + (typeof success === 'string' ? '  {0}' : '')), success)), $this.settings.messagetimeout);

					currfolder.SetBusyRef(-1);

					if (currfolder === origfolder)  $this.RefreshFolders(true);
				}
			};

			$this.StartOperationIndicator();

			if (numselecteditems === 1)  $this.SetNamedStatusBarText('message', EscapeHTML($this.Translate('Deleting 1 item...')), $this.settings.messagetimeout);
			else  $this.SetNamedStatusBarText('message', EscapeHTML(FormatStr($this.Translate('Deleting {0} items...'), numselecteditems)), $this.settings.messagetimeout);

			DispatchEvent('delete', [deletecallback, currfolder, $this.GetSelectedItemIDs(), $this.GetSelectedFolderEntries(), recycle]);
		};

		// Checks whether or not Destroy was called.
		$this.IsDestroyed = function() {
			return destroyinprogress;
		};

		// Destroys the instance.
		$this.Destroy = function() {
			// Remove event listeners, timeouts, and intervals.  There are quite a few.
			destroyinprogress = true;

			// Force clear all busy queue callbacks across all mapped folders.
			for (var x in foldermap)
			{
				if (foldermap.hasOwnProperty(x))
				{
					foldermap[x].ClearBusyQueueCallbacks();

					DecrementMappedFolderRefCount(foldermap[x]);
				}
			}

			// Destroy tools and anything else that is listening for the destroy event.
			DispatchEvent('destroy');
			tools = [];

			// Reset a number of instance globals.
			triggers = {};
			historystack = [];
			currhistory = -1;

			selecteditemsmap = {};
			focuseditem = false;

			// Cancel the popup menu and/or rename text overlay.
			if (popupmenu)  popupmenu.Cancel();
			if (textareaoverlayinst)  textareaoverlayinst.Cancel();

			for (var x in elems.statusbartextsegmentmap)
			{
				if (elems.statusbartextsegmentmap.hasOwnProperty(x) && elems.statusbartextsegmentmap[x].timeout)
				{
					clearTimeout(elems.statusbartextsegmentmap[x].timeout);

					elems.statusbartextsegmentmap[x].timeout = null;
				}
			}

			window.removeEventListener('resize', statusbarresizewatch.Start, true);
			statusbarresizewatch.Destroy();
			statusbarresizewatch = null;

			if (internalcapturerefs)
			{
				capturingrefs -= internalcapturerefs;
				internalcapturerefs = 0;

				window.removeEventListener('popstate', CapturePopStateHandler, true);

				if (window.history.state && window.history.state._fileexplorer)  window.history.back();
			}

			elems.mainwrap.removeEventListener('mouseenter', CaptureMouseEnterHandler);
			elems.mainwrap.removeEventListener('mouseleave', CaptureMouseLeaveHandler);

			elems.mainwrap.removeEventListener('mousedown', MainWrapFocusMouseHandler);
			elems.mainwrap.removeEventListener('mouseup', MainWrapFocusMouseHandler);
			elems.mainwrap.removeEventListener('click', MainWrapFocusMouseHandler);

			window.removeEventListener('mousedown', InnerWrapBlurHandler, true);
			window.removeEventListener('blur', InnerWrapWindowBlurHandler, true);
			window.removeEventListener('focus', FocusKeyHandler, true);

			elems.bodytoolbar.removeEventListener('keydown', ToolbarKeyHandler);
			elems.bodytoolsscrollwrap.removeEventListener('focus', ToolbarToolFocusHandler, true);

			// Cancel all thumbnails.
			for (var x in queuedthumbs)
			{
				if (queuedthumbs.hasOwnProperty(x))  fe_thumbnailloader.RemoveFromQueue(x);
			}

			queuedthumbs = {};
			queuedthumbfailed = {};

			elems.itemsscrollwrap.removeEventListener('scroll', thumbnailscrollwatch.Start);
			window.removeEventListener('resize', thumbnailscrollwatch.Start, true);
			thumbnailscrollwatch.Destroy();
			thumbnailscrollwatch = null;

			folderitemcache = null;

			elems.pathsegmentsscrollwrap.removeEventListener('wheel', ConvertVertToHorzScroll);
			elems.navtools.removeEventListener('keydown', NavToolsKeyHandler);

			if (currfolder)
			{
				currfolder.removeEventListener('set_entries', SetFolderEntriesHandler);
				currfolder.removeEventListener('remove_entry', RemoveFolderEntryHandler);
			}

			selectanchorpos = null;
			prevselectrect = null;
			selectbox = null;
			lastmouseevent = null;

			if (autoscrolltimer)
			{
				clearInterval(autoscrolltimer);
				autoscrolltimer = null;
			}

			lastselecttouch = null;
			lastmousedownevent = null;

			// Clean up a ton of event handlers related to clipboard handling.  There are a couple of DOM changes too but it is not a big deal.
			ClipboardOverlayExitContextMenuHandler();

			// Cancel any rename start operation in progress.
			CancelRenameHandler();
			startrenamefolder = null;
			startrenameid = null;

			scrollnomoveinfo = null;

			movecopydata = false;
			elems.itemswrap.removeEventListener('dragstart', MoveCopyDragStartHandler);
			elems.itemswrap.removeEventListener('dragend', MoveCopyDragEndHandler);
			elems.innerwrap.removeEventListener('dragenter', MoveCopyDragEnterHandler);
			elems.innerwrap.removeEventListener('dragover', MoveCopyDragOverHandler);
			elems.innerwrap.removeEventListener('dragleave', MoveCopyDragLeaveHandler);
			elems.innerwrap.removeEventListener('drop', MoveCopyDropHandler);

			// Stop all progress trackers.
			if (progresstrackers.length)  ProgressCancelAllHandler();

			progresstrackers = [];
			if (progresstrackerinterval)
			{
				clearInterval(progresstrackerinterval);
				progresstrackerinterval = null;
			}

			PreFinishProgressDisplay();

			elems.statusbaractionprogresscancelwrap.removeEventListener('click', ProgressCancelAllHandler);
			elems.statusbaractionprogresscancelwrap.removeEventListener('keydown', ProgressCancelKeydownHandler);

			// Clear folder refresh interval used during uploads.
			if (uploadfolderinterval)
			{
				clearInterval(uploadfolderinterval);
				uploadfolderinterval = null;
			}

			// Remove a bunch more event handlers.
			window.removeEventListener('mouseup', ScrollNoMoveHandler, true);

			window.removeEventListener('mousemove', SelectBoxDragHandler, true);
			window.removeEventListener('mouseup', SelectBoxEndHandler, true);
			window.removeEventListener('blur', SelectBoxEndHandler, true);
			elems.itemsscrollwrap.removeEventListener('wheel', SelectBoxScrollWheelHandler);

			elems.itemsscrollwrapinner.removeEventListener('mousedown', StartSelectionHandler);
			elems.itemsscrollwrapinner.removeEventListener('touchstart', StartSelectionHandler);
			elems.itemsscrollwrapinner.removeEventListener('click', CheckboxSelectedFixHandler);

			elems.navtool_history.removeEventListener('mousedown', RecentLocationsHandler);
			elems.navtool_history.removeEventListener('keydown', RecentLocationsKeyHandler);

			elems.pathsegmentsscrollwrap.removeEventListener('mousedown', PathSegmentMouseFocusHandler);
			elems.pathsegmentsscrollwrap.removeEventListener('focus', PathSegmentFocusScrollHandler, true);
			elems.pathsegmentsscrollwrap.removeEventListener('click', PathSegmentClickHandler);
			elems.pathsegmentsscrollwrap.removeEventListener('keydown', PathSegmentKeyHandler);

			elems.itemsscrollwrap.removeEventListener('cut', ClipboardCutCopyHandler);
			elems.itemsscrollwrap.removeEventListener('copy', ClipboardCutCopyHandler);
			elems.itemsscrollwrap.removeEventListener('paste', ClipboardPasteHandler);

			elems.itemsclipboardoverlay.removeEventListener('cut', ClipboardCutCopyHandler);
			elems.itemsclipboardoverlay.removeEventListener('copy', ClipboardCutCopyHandler);
			elems.itemsclipboardoverlay.removeEventListener('paste', ClipboardPasteHandler);

			lasttypingstr = '';
			lastkey = '';

			elems.itemsscrollwrap.removeEventListener('keydown', ItemsKeyHandler);
			elems.itemsscrollwrap.removeEventListener('keypress', ItemsKeypressHandler);

			elems.innerwrap.removeEventListener('keydown', MainKeyHandler);

			elems.navtool_up.removeEventListener('mouseup', ClickNavigateUpHandler);
			elems.navtool_up.removeEventListener('keydown', NavigateUpKeyHandler);
			elems.navtool_back.removeEventListener('mouseup', ClickHistoryBackHandler);
			elems.navtool_back.removeEventListener('keydown', HistoryBackKeyHandler);
			elems.navtool_forward.removeEventListener('mouseup', ClickHistoryForwardHandler);
			elems.navtool_forward.removeEventListener('keydown', HistoryForwardKeyHandler);

			if (operationtimeout)
			{
				clearTimeout(operationtimeout);

				operationtimeout = null;
			}

			// Remove DOM elements.
			while (elems.pathsegmentswrap.firstChild)  elems.pathsegmentswrap.removeChild(elems.pathsegmentswrap.lastChild);

			while (elems.itemswrap.firstChild)
			{
				elems.itemswrap.removeChild(elems.itemswrap.lastChild);
			}

			for (var node in elems)
			{
				if (Array.isArray(elems[node]))
				{
					for (var x = 0; x < elems[node].length; x++)
					{
						if (elems[node][x].parentNode)  elems[node][x].parentNode.removeChild(elems[node][x]);
					}
				}
				else if (elems[node].parentNode)
				{
					elems[node].parentNode.removeChild(elems[node]);
				}
			}

			// Remaining cleanup.
			elems = null;

			$this.settings = Object.assign({}, defaults);

			currfolder = false;
			$this = null;
			parentelem = null;
			options = null;
		};


		// Create tool instances.  Needs to come after DOM-style and public functions to allow tools to register for various events.
		var tools = [], numtoolbuttons = 0, numtoolbuttongroups;

		var UpdateLastUsedToolButtonHandler = function(e) {
			if (!e.isTrusted)  return;

			if (!e.target.classList.contains('fe_fileexplorer_disabled'))
			{
				elems.bodytools.forEach(function(elem) {
					elem.tabIndex = (elem === e.target && !elem.classList.contains('fe_fileexplorer_disabled') ? 0 : -1);
				});
			}
		};

		$this.AddToolbarButton = function(classname, title) {
			var node = CreateNode('button', [classname, 'fe_fileexplorer_disabled'], { title: title, tabIndex: -1 });

			node.addEventListener('click', UpdateLastUsedToolButtonHandler);

			if (numtoolbuttons && !numtoolbuttongroups)  elems.bodytoolbar.appendChild(CreateNode('div', ['fe_fileexplorer_folder_tool_separator']));

			elems.bodytoolbar.appendChild(node);
			elems.bodytools.push(node);

			numtoolbuttons++;
			numtoolbuttongroups++;

			return node;
		};

		for (var x = 0; x < coretools.length; x++)
		{
			numtoolbuttongroups = 0;

			for (var x2 = 0; x2 < coretools[x].length; x2++)
			{
				tools.push(new coretools[x][x2]($this));
			}
		}

		if (numtoolbuttons)  elems.bodytoolsscrollwrap.classList.remove('fe_fileexplorer_hidden');

		// Set the initial path.
		$this.SetPath($this.settings.initpath);
	};


	// Export internal mini-classes for reusability purposes.
	window.FileExplorer.ImageLoader = ImageLoader;
	window.FileExplorer.PopupMenu = PopupMenu;
	window.FileExplorer.TextareaOverlay = TextareaOverlay;


	// Global function to register a tool.
	window.FileExplorer.RegisterTool = function(groupnum, tool) {
		while (groupnum >= coretools.length)  coretools.push([]);

		coretools[groupnum].push(tool);
	};


	// Core tools.
	var FileExplorerTool_NewFolder = function(fe) {
		if (!(this instanceof FileExplorerTool_NewFolder))  return new FileExplorerTool_NewFolder(fe);

		// Do not create the tool if the tool is not enabled.
		if (!fe.settings.onnewfolder && !fe.settings.tools.new_folder)  return;

		var enabled = false;

		var node = fe.AddToolbarButton('fe_fileexplorer_folder_tool_new_folder', fe.Translate('New Folder (Ctrl + Ins)'));

		if (fe.settings.onnewfolder)  fe.addToolEventListener('new_folder', fe.settings.onnewfolder);

		var CreateFolder = function() {
			if (!enabled)  return;

			var origfolder = fe.GetCurrentFolder();

			var calledback = false;
			var createdcallback = function(newentry) {
				if (calledback || fe.IsDestroyed())  return;

				calledback = true;

				fe.StopOperationIndicator();

				if (typeof newentry === 'object')
				{
					if (fe.IsMappedFolder(origfolder))
					{
						fe.SetNamedStatusBarText('message', '');

						origfolder.SetEntry(newentry);

						if (fe.GetCurrentFolder() === origfolder)
						{
							fe.SetFocusItem(newentry.id, true);
							fe.ScrollToFocusedItem();
							fe.SetSelectedItems([newentry.id]);
							fe.RenameSelectedItem();
						}
					}
				}
				else
				{
					fe.SetNamedStatusBarText('message', EscapeHTML(FormatStr(fe.Translate('Creating a new folder failed.' + (typeof newentry === 'string' ? '  {0}' : '')), newentry)), fe.settings.messagetimeout);
				}
			};

			fe.StartOperationIndicator();

			fe.SetNamedStatusBarText('message', EscapeHTML(fe.Translate('Creating a new folder...')), fe.settings.messagetimeout);

			fe.DispatchToolEvent('new_folder', [createdcallback, origfolder]);
		};

		var ClickHandler = function(e) {
			if (!e.isTrusted)  return;

			CreateFolder();
		};

		node.addEventListener('click', ClickHandler);

		var HotkeyHandler = function(e) {
			if (e.ctrlKey && !e.shiftKey && !e.altKey && e.keyCode == 45)
			{
				// Ctrl + Insert.
				e.preventDefault();

				CreateFolder();
			}
		};

		fe.addEventListener('keydown', HotkeyHandler);

		var UpdateToolHandler = function(currfolder, attrs) {
			var prevenabled = enabled;

			enabled = (!currfolder.waiting && (!('canmodify' in attrs) || attrs.canmodify));

			if (prevenabled !== enabled)
			{
				if (enabled)  node.classList.remove('fe_fileexplorer_disabled');
				else  node.classList.add('fe_fileexplorer_disabled');

				fe.ToolStateUpdated();
			}
		};

		fe.addEventListener('update_tool', UpdateToolHandler);

		var DestroyToolHandler = function() {
			node.removeEventListener('click', ClickHandler);
		};

		fe.addEventListener('destroy', DestroyToolHandler);
	};

	window.FileExplorer.RegisterTool(0, FileExplorerTool_NewFolder);


	var FileExplorerTool_NewFile = function(fe) {
		if (!(this instanceof FileExplorerTool_NewFile))  return new FileExplorerTool_NewFile(fe);

		// Do not create the tool if the tool is not enabled.
		if (!fe.settings.onnewfile && !fe.settings.tools.new_file)  return;

		var enabled = false;

		var node = fe.AddToolbarButton('fe_fileexplorer_folder_tool_new_file', fe.Translate('New File (Ins)'));

		if (fe.settings.onnewfile)  fe.addToolEventListener('new_file', fe.settings.onnewfile);

		var CreateFile = function() {
			if (!enabled)  return;

			var origfolder = fe.GetCurrentFolder();

			var calledback = false;
			var createdcallback = function(newentry) {
				if (calledback || fe.IsDestroyed())  return;

				calledback = true;

				fe.StopOperationIndicator();

				if (typeof newentry === 'object')
				{
					if (fe.IsMappedFolder(origfolder))
					{
						fe.SetNamedStatusBarText('message', '');

						origfolder.SetEntry(newentry);

						if (fe.GetCurrentFolder() === origfolder)
						{
							fe.SetFocusItem(newentry.id, true);
							fe.ScrollToFocusedItem();
							fe.SetSelectedItems([newentry.id]);
							fe.RenameSelectedItem();
						}
					}
				}
				else
				{
					fe.SetNamedStatusBarText('message', EscapeHTML(FormatStr(fe.Translate('Creating a new file failed.' + (typeof newentry === 'string' ? '  {0}' : '')), newentry)), fe.settings.messagetimeout);
				}
			};

			fe.StartOperationIndicator();

			fe.SetNamedStatusBarText('message', EscapeHTML(fe.Translate('Creating a new file...')), fe.settings.messagetimeout);

			fe.DispatchToolEvent('new_file', [createdcallback, origfolder]);
		};

		var ClickHandler = function(e) {
			if (!e.isTrusted)  return;

			CreateFile();
		};

		node.addEventListener('click', ClickHandler);

		var HotkeyHandler = function(e) {
			if (!e.ctrlKey && !e.shiftKey && !e.altKey && e.keyCode == 45)
			{
				// Insert.
				e.preventDefault();

				CreateFile();
			}
		};

		fe.addEventListener('keydown', HotkeyHandler);

		var UpdateToolHandler = function(currfolder, attrs) {
			var prevenabled = enabled;

			enabled = (!currfolder.waiting && (!('canmodify' in attrs) || attrs.canmodify));

			if (prevenabled !== enabled)
			{
				if (enabled)  node.classList.remove('fe_fileexplorer_disabled');
				else  node.classList.add('fe_fileexplorer_disabled');

				fe.ToolStateUpdated();
			}
		};

		fe.addEventListener('update_tool', UpdateToolHandler);

		var DestroyToolHandler = function() {
			node.removeEventListener('click', ClickHandler);
		};

		fe.addEventListener('destroy', DestroyToolHandler);
	};

	window.FileExplorer.RegisterTool(0, FileExplorerTool_NewFile);


	var FileExplorerTool_Upload = function(fe) {
		if (!(this instanceof FileExplorerTool_Upload))  return new FileExplorerTool_Upload(fe);

		// Do not create the tool if uploading is disabled.
		if (!fe.hasEventListener('init_upload') && !fe.settings.tools.upload)  return;

		var enabled = false;
		var inputfield = null;

		var node = fe.AddToolbarButton('fe_fileexplorer_folder_tool_upload', fe.Translate('Upload (Ctrl + U)'));

		var RemoveInputField = function() {
			if (inputfield)
			{
				inputfield.removeEventListener('change', UploadFiles);
				inputfield.parentNode.removeChild(inputfield);
				inputfield = null;
			}
		};

		var UploadFiles = function(e) {
			fe.ProcessFilesAndUpload('currfolder', null, inputfield);

			// Remove the field.
			RemoveInputField();
		};

		var CreateInputField = function() {
			RemoveInputField();

			inputfield = CreateNode('input', ['fe_fileexplorer_hidden'], { type: 'file', multiple: true });
			inputfield.addEventListener('change', UploadFiles);

			fe.GetElements().mainwrap.appendChild(inputfield);
		};

		var StartSelectFiles = function() {
			if (!enabled)  return;

			if (!inputfield)  CreateInputField();

			inputfield.click();
		};

		var ClickHandler = function(e) {
			if (!e.isTrusted)  return;

			StartSelectFiles();
		};

		node.addEventListener('click', ClickHandler);

		var HotkeyHandler = function(e) {
			if (e.ctrlKey && !e.shiftKey && !e.altKey && e.keyCode == 85)
			{
				// Ctrl + U.
				e.preventDefault();

				StartSelectFiles();
			}
		};

		fe.addEventListener('keydown', HotkeyHandler);

		var UpdateToolHandler = function(currfolder, attrs) {
			var prevenabled = enabled;

			enabled = (!currfolder.waiting && (!('canmodify' in attrs) || attrs.canmodify));

			if (prevenabled !== enabled)
			{
				if (enabled)  node.classList.remove('fe_fileexplorer_disabled');
				else  node.classList.add('fe_fileexplorer_disabled');

				fe.ToolStateUpdated();
			}
		};

		fe.addEventListener('update_tool', UpdateToolHandler);

		var DestroyToolHandler = function() {
			RemoveInputField();

			node.removeEventListener('click', ClickHandler);
		};

		fe.addEventListener('destroy', DestroyToolHandler);
	};

	window.FileExplorer.RegisterTool(0, FileExplorerTool_Upload);


	var FileExplorerTool_Download = function(fe) {
		if (!(this instanceof FileExplorerTool_Download))  return new FileExplorerTool_Download(fe);

		// Do not create the tool if downloading is disabled.
		if (!fe.settings.oninitdownload && !fe.settings.tools.download)  return;

		var enabled = false;

		var node = fe.AddToolbarButton('fe_fileexplorer_folder_tool_download', fe.Translate('Download'));

		if (fe.settings.oninitdownload)  fe.addToolEventListener('init_download', fe.settings.oninitdownload);
		if (fe.settings.ondownloadstarted)  fe.addToolEventListener('download_started', fe.settings.ondownloadstarted);
		if (fe.settings.ondownloaderror)  fe.addToolEventListener('download_error', fe.settings.ondownloaderror);

		var ClickHandler = function(e) {
			if (!e.isTrusted || !enabled)  return;

			var calledback = false;
			var downloadcallback = function(options) {
				if (calledback || fe.IsDestroyed())  return;

				calledback = true;

				if (typeof options === 'object')
				{
					// Create a form.
					var method = (options.method || 'POST');
					var formnode = CreateNode('form', ['fe_fileexplorer_hidden'], { action: options.url, method: method, enctype: 'multipart/form-data' });

					if (options.params)
					{
						if (options.params instanceof FormData)
						{
							for (var entry in options.params)
							{
								if (typeof entry[1] === 'string')  formnode.appendChild(CreateNode('input', [], { type: 'hidden', name: entry[0], value: entry[1] }));
							}
						}
						else if (Array.isArray(options.params))
						{
							for (var x = 0; x < options.params.length; x++)  formnode.appendChild(CreateNode('input', [], { type: 'hidden', name: options.params[x].name, value: options.params[x].value }));
						}
						else
						{
							for (var x in options.params)
							{
								if (options.params.hasOwnProperty(x) && typeof options.params[x] === 'string')  formnode.appendChild(CreateNode('input', [], { type: 'hidden', name: x, value: options.params[x] }));
							}
						}
					}

					// Create an iframe.
					if (!('iframe' in options) || options.iframe)
					{
						var iframenode = CreateNode('iframe', ['fe_fileexplorer_download_iframe_wrap']);

						var removeiframe = function() {
							if (iframenode)
							{
								document.body.removeChild(iframenode);

								iframenode = null;

								fe.DispatchToolEvent('download_started', options);
							}
						};

						// As soon as the response starts being delivered by the server, abort the request.
						var requestresponsehandler = function(e) {
							fe.StopOperationIndicator();

							// Remove the iframe after 5 seconds.  It is extremely likely that the other download has successfully started too.
							setTimeout(removeiframe, 5000);

							if (xhr)
							{
								var tempxhr = xhr;

								xhr = null;

								tempxhr.Destroy();
							}
						};

						// Prepare a second, independent request for the download.
						var xhr = new PrepareXHR(options);

						xhr.addEventListener('progress', requestresponsehandler);
						xhr.addEventListener('loadend', requestresponsehandler);
						xhr.addEventListener('timeout', requestresponsehandler);

						var iframeloadhandler = function(e) {
							if (formnode)
							{
								// First load.  Set the form in the iframe and submit it.
								// The iframe contents become immediately inaccessible so any security issues are mitigated.
								iframenode.contentWindow.document.body.appendChild(formnode);
								formnode.submit();

								formnode = null;

								// Start the second download.
								xhr.Send();
							}
							else if (iframenode)
							{
								// Second load.  Remove the iframe and cancel the XHR request.  The download also failed for some reason.
								fe.StopOperationIndicator();

								document.body.removeChild(iframenode);

								iframenode = null;

								if (xhr)
								{
									var tempxhr = xhr;

									xhr = null;

									tempxhr.Destroy();
								}

								fe.SetNamedStatusBarText('message', EscapeHTML(FormatStr(fe.Translate('Download failed to start'))), fe.settings.messagetimeout);

								fe.DispatchToolEvent('download_error', options);
							}
						};

						iframenode.addEventListener('load', iframeloadhandler);

						document.body.appendChild(iframenode);
					}
					else
					{
						// Create a new tab/window when submitting the form.  Most browsers will close the tab/window as soon as the download dialog shows.
						fe.StopOperationIndicator();

						formnode.target = '_blank';

						document.body.appendChild(formnode);
						formnode.submit();
						document.body.removeChild(formnode);
					}

					fe.SetNamedStatusBarText('message', EscapeHTML(FormatStr(fe.Translate('Starting download...'))), fe.settings.messagetimeout);
				}
				else
				{
					fe.StopOperationIndicator();

					fe.SetNamedStatusBarText('message', EscapeHTML(FormatStr(fe.Translate('Download initialization failed.' + (typeof options === 'string' ? '  {0}' : '')), options)), fe.settings.messagetimeout);
				}
			};

			fe.StartOperationIndicator();

			fe.SetNamedStatusBarText('message', EscapeHTML(fe.Translate('Initializing download...')), fe.settings.messagetimeout);

			fe.DispatchToolEvent('init_download', [downloadcallback, fe.GetCurrentFolder(), fe.GetSelectedItemIDs(), fe.GetSelectedFolderEntries()]);
		};

		node.addEventListener('click', ClickHandler);

		var UpdateToolHandler = function(currfolder, attrs) {
			var prevenabled = enabled;

			enabled = (!currfolder.waiting && fe.GetNumSelectedItems() > 0);

			if (prevenabled !== enabled)
			{
				if (enabled)  node.classList.remove('fe_fileexplorer_disabled');
				else  node.classList.add('fe_fileexplorer_disabled');

				fe.ToolStateUpdated();
			}
		};

		fe.addEventListener('update_tool', UpdateToolHandler);

		var DestroyToolHandler = function() {
			node.removeEventListener('click', ClickHandler);
		};

		fe.addEventListener('destroy', DestroyToolHandler);
	};

	window.FileExplorer.RegisterTool(0, FileExplorerTool_Download);


	var FileExplorerTool_Copy = function(fe) {
		if (!(this instanceof FileExplorerTool_Copy))  return new FileExplorerTool_Copy(fe);

		// Do not create the tool if copying is disabled.
		if (!fe.hasEventListener('copy') && !fe.settings.tools.copy)  return;

		var enabled = false;

		var node = fe.AddToolbarButton('fe_fileexplorer_folder_tool_copy', fe.Translate('Copy (' + (navigator.platform.indexOf('Mac') > -1 ? '\u2318' : 'Ctrl') + ' + C)'));

		var ClickHandler = function(e) {
			if (!e.isTrusted || !enabled)  return;

			var elems = fe.GetElements();

			elems.itemsclipboardoverlay.value = '';
			elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_hidden');
			elems.itemsclipboardoverlay.focus();

			document.execCommand('copy');
		};

		node.addEventListener('click', ClickHandler);

		var UpdateToolHandler = function(currfolder, attrs) {
			var prevenabled = enabled;

			enabled = (!currfolder.waiting && fe.GetNumSelectedItems() > 0);

			if (prevenabled !== enabled)
			{
				if (enabled)  node.classList.remove('fe_fileexplorer_disabled');
				else  node.classList.add('fe_fileexplorer_disabled');

				fe.ToolStateUpdated();
			}
		};

		fe.addEventListener('update_tool', UpdateToolHandler);

		var DestroyToolHandler = function() {
			node.removeEventListener('click', ClickHandler);
		};

		fe.addEventListener('destroy', DestroyToolHandler);
	};

	window.FileExplorer.RegisterTool(1, FileExplorerTool_Copy);


	var FileExplorerTool_Paste = function(fe) {
		if (!(this instanceof FileExplorerTool_Paste))  return new FileExplorerTool_Paste(fe);

		// Do not create the tool if copying and moving are disabled.
		if (!fe.hasEventListener('copy') && !fe.hasEventListener('move') && !fe.settings.tools.paste)  return;

		var enabled = false;

		var node = fe.AddToolbarButton('fe_fileexplorer_folder_tool_paste', fe.Translate('Paste (' + (navigator.platform.indexOf('Mac') > -1 ? '\u2318' : 'Ctrl') + ' + V)'));

		var ClickHandler = function(e) {
			if (!e.isTrusted || !enabled)  return;

			fe.ShowClipboardPasteBox();
		};

		var ToolKeyHandler = function(e) {
			if (!e.isTrusted || !enabled)  return;

			if (e.keyCode == 13 || e.keyCode == 32)
			{
				fe.ShowClipboardPasteBox();

				fe.GetElements().itemsclipboardoverlay.focus();
			}
		};

		node.addEventListener('mouseup', ClickHandler);
		node.addEventListener('keyup', ToolKeyHandler);

		var UpdateToolHandler = function(currfolder, attrs) {
			var prevenabled = enabled;

			enabled = (!currfolder.waiting && (!('canmodify' in attrs) || attrs.canmodify));

			if (prevenabled !== enabled)
			{
				if (enabled)  node.classList.remove('fe_fileexplorer_disabled');
				else  node.classList.add('fe_fileexplorer_disabled');

				fe.ToolStateUpdated();
			}
		};

		fe.addEventListener('update_tool', UpdateToolHandler);

		var DestroyToolHandler = function() {
			node.removeEventListener('mouseup', ClickHandler);
			node.removeEventListener('keyup', ToolKeyHandler);
		};

		fe.addEventListener('destroy', DestroyToolHandler);
	};

	window.FileExplorer.RegisterTool(1, FileExplorerTool_Paste);


	var FileExplorerTool_Cut = function(fe) {
		if (!(this instanceof FileExplorerTool_Cut))  return new FileExplorerTool_Cut(fe);

		// Do not create the tool if moving is disabled.
		if (!fe.hasEventListener('move') && !fe.settings.tools.cut)  return;

		var enabled = false;

		var node = fe.AddToolbarButton('fe_fileexplorer_folder_tool_cut', fe.Translate('Cut (' + (navigator.platform.indexOf('Mac') > -1 ? '\u2318' : 'Ctrl') + ' + X)'));

		var ClickHandler = function(e) {
			if (!e.isTrusted || !enabled)  return;

			var elems = fe.GetElements();

			elems.itemsclipboardoverlay.value = '';
			elems.itemsclipboardoverlaypastewrap.classList.remove('fe_fileexplorer_hidden');
			elems.itemsclipboardoverlay.focus();

			document.execCommand('cut');
		};

		node.addEventListener('click', ClickHandler);

		var UpdateToolHandler = function(currfolder, attrs) {
			var prevenabled = enabled;

			enabled = (!currfolder.waiting && (!('canmodify' in attrs) || attrs.canmodify) && fe.GetNumSelectedItems() > 0);

			if (prevenabled !== enabled)
			{
				if (enabled)  node.classList.remove('fe_fileexplorer_disabled');
				else  node.classList.add('fe_fileexplorer_disabled');

				fe.ToolStateUpdated();
			}
		};

		fe.addEventListener('update_tool', UpdateToolHandler);

		var DestroyToolHandler = function() {
			node.removeEventListener('click', ClickHandler);
		};

		fe.addEventListener('destroy', DestroyToolHandler);
	};

	window.FileExplorer.RegisterTool(1, FileExplorerTool_Cut);


	var FileExplorerTool_Delete = function(fe) {
		if (!(this instanceof FileExplorerTool_Delete))  return new FileExplorerTool_Delete(fe);

		// Do not create the tool if deleting is disabled.
		if (!fe.hasEventListener('delete') && !fe.settings.tools.delete)  return;

		var enabled = false;

		var node = fe.AddToolbarButton('fe_fileexplorer_folder_tool_delete', fe.Translate('Delete (Del)'));

		var ClickHandler = function(e) {
			if (e.isTrusted && enabled)  fe.DeleteSelectedItems(!e.shiftKey);
		};

		node.addEventListener('click', ClickHandler);

		var UpdateToolHandler = function(currfolder, attrs) {
			var prevenabled = enabled;

			enabled = (!currfolder.waiting && (!('canmodify' in attrs) || attrs.canmodify) && fe.GetNumSelectedItems());

			if (prevenabled !== enabled)
			{
				if (enabled)  node.classList.remove('fe_fileexplorer_disabled');
				else  node.classList.add('fe_fileexplorer_disabled');

				fe.ToolStateUpdated();
			}
		};

		fe.addEventListener('update_tool', UpdateToolHandler);

		var DestroyToolHandler = function() {
			node.removeEventListener('click', ClickHandler);
		};

		fe.addEventListener('destroy', DestroyToolHandler);
	};

	window.FileExplorer.RegisterTool(1, FileExplorerTool_Delete);


	var FileExplorerTool_ItemCheckboxes = function(fe) {
		if (!(this instanceof FileExplorerTool_ItemCheckboxes))  return new FileExplorerTool_ItemCheckboxes(fe);

		// Do not create the tool if the device's primary input is not coarse and the tool is not specifically enabled.
		if (!matchMedia('(pointer: coarse)').matches && !fe.settings.tools.item_checkboxes)  return;

		var node = fe.AddToolbarButton('fe_fileexplorer_folder_tool_item_checkboxes', fe.Translate('Item Checkboxes'));

		// Always enabled.
		node.classList.remove('fe_fileexplorer_disabled');

		var ClickHandler = function(e) {
			if (!e.isTrusted)  return;

			fe.GetElements().innerwrap.classList.toggle('fe_fileexplorer_show_item_checkboxes');
		};

		node.addEventListener('click', ClickHandler);

		var DestroyToolHandler = function() {
			node.removeEventListener('click', ClickHandler);
		};

		fe.addEventListener('destroy', DestroyToolHandler);
	};

	window.FileExplorer.RegisterTool(2, FileExplorerTool_ItemCheckboxes);
})();
