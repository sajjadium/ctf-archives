How to send requests to nmanager website for debugging purpose:
	Add "127.0.0.1 nmanager" to your hosts list and then Bind port 80 of namanger container to your localhost.
	Then you should be able to get http://nmanager/ with your browser
Or you can just remove host header check from patch file