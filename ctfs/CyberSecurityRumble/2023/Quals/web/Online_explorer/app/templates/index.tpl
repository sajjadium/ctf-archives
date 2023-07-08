<!DOCTYPE html>
<html>

<head>
</head>

<body>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='file-explorer.css') }}">
    <script type="text/javascript" src="{{ url_for('static', filename='file-explorer.js') }}"></script>
    <div id="filemanager" style="height: 95vh"></div>
    <script type="text/javascript">
        (function () {
            var elem = document.getElementById('filemanager')

            var options = {
                initpath: [
                    ['', "{{ session['token'] }} (/)", { canmodify: false }]
                ],

                onrefresh: function (folder, required) {
                    if (!required) return;

                    fetch("/api" + folder.GetPathIDs().join("/")).then(
                        (resp) => resp.json()
                    ).then(
                        (items) => {
                            var convertedItems = []
                            for (const item of items.items) {
                                var convertedItem = { "name": item.name, "id": item.name, "hash": item.name }
                                if (item.type == "file") {
                                    convertedItem.type = "file"
                                    convertedItems.push(convertedItem)
                                }
                                else if (item.type == "directory" || item.type == "symlink") {
                                    convertedItem.type = "folder"
                                    convertedItems.push(convertedItem)
                                }
                            }
                            folder.SetEntries(convertedItems)
                        }
                    )
                },

                onopenfile: function (folder, entry) {
                    fetch("/api" + folder.GetPathIDs().join("/") + "/" + entry.name).then(
                        (resp) => resp.json()
                    ).then(
                        (output) => {
                            if ("output" in output) {
                                alert("Output: " + output.output)
                            }
                            else if ("content" in output) {
                                alert("Content: " + output.content)
                            }
                            else if ("error" in output) {
                                alert("Error: " + output.error)
                            }
                        }
                    )
                }
            }

            var fe = new window.FileExplorer(elem, options)
        })()
    </script>
</body>

</html>