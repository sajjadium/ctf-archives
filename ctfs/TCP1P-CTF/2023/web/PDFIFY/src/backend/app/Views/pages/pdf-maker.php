<!-- Include stylesheet -->

<!-- Create the editor container -->
<link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
<div class="container p-4">
    <div class="row">
        <div class="col-sm">
            <div class="grid gap-3">
                <div class="p-1 g-col-6" id="editor" style="height: 65vh;">
                </div>
                <div class="p-1 g-col-6">
                    <button type="submit" class="btn btn-primary w-100 text-white" onclick="getOutputFromHtml()">
                        Generate PDF
                    </button>
                </div>
            </div>
        </div>
        <div class="col-sm border border-primary" id="pdfout">
        </div>
    </div>
</div>



<!-- Include the Quill library -->
<script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>

<!-- Initialize Quill editor -->
<script>
    var options = {
        debug: 'info',
        placeholder: 'Compose an epic pdf...',
        theme: 'snow'
    };
    var quill = new Quill('#editor', options);

    function getOutputFromHtml() {
        const pdf_value = quill.root.innerHTML
        $("#pdfout").empty().append(`
        <div class="d-flex align-items-center justify-content-center" style="height: 100vh;">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        `)
        $.post("/pdf-maker", {
            body: pdf_value,
            option: "getOutputFromHtml",
        }).done((res) => {
            const b64_pdf = res['pdf'];
            const iframe = document.createElement('iframe');
            iframe.src = `data:application/pdf;base64,${b64_pdf}`;
            iframe.width = "100%"
            iframe.height = "100%"
            $("#pdfout").empty().append(iframe);
        }).fail((res) => {
            $("#pdfout").empty().append();
            alert(JSON.parse(res.responseText).message)
        })
    }
</script>
