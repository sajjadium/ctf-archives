<form action="/api" method="POST" enctype="multipart/form-data">
	<input type="file" name="file" required accept=".png, .jpg, .jpeg, .jfif" />
	<button type="submit">Upload</button>
</form>

Welcome to the license plate app! upload a picture of a license plate to find the user! Below is an
example plate. All plates uploaded must only contain the text of the plate, and nothing else.
Otherwise, it doesn't work. Click below to download the example plate.<br/>
<a href="/plate.jpg" download><img src="/plate.jpg" alt="example plate"/></a>
