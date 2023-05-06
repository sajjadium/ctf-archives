Vue.use(VueQuillEditor)
new Vue({
    el: '#app',
    delimiters: ['##', '##'],
    data: {
        quill_config: {
            modules: {
                toolbar: [
                  [{ header: [2, 3, false] }],
                  ['bold', 'italic', 'underline'],
                  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                  [{ 'script': 'sub'}, { 'script': 'super' }],
                  ['clean']
                ]
            },
            placeholder: 'Text...',
            theme: 'snow',
        },
        form: {
            url: '',
            post: {},
            cropper: false,
            isCropping: false,
            isImageLoaded: false
        },
        timing: {
            url: null,
            requesting: false
        },
        imageLock: 0
    },
    methods: {
        onFormURLUpdate() {
            this.timing.requesting = true;
            const url = this.form.url;
            if(this.timing.url) clearTimeout(this.timing.url)
            this.timing.url = setTimeout(_ => {
                this.fetchResource(url)
                this.timing.requesting = false;
            }, 2000);
        },
        fetchResource(url) {
            fetch("/api/get_resource", {
                method: 'POST',
                body: JSON.stringify({
                    url: url
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(content => {
                if(content.status === 500) {
                    alert("Could not fetch resource! Please enter a valid URL!")
                } else {
                    Promise.resolve(content.text()).then(data => {
                        const html = document.createElement("html");
                        html.innerHTML = data;
                        const scripts = html.querySelectorAll("script");
                        let schemes = [];
                        for(let i = 0; i < scripts.length; i++) {
                            const script = scripts[i];
                            try {
                                const json = JSON.parse(script.innerText)
                                if(Array.isArray(json)) {
                                    schemes.push(...json);
                                } else {
                                    schemes.push(json)
                                }
                            } catch(e) {}
                        }
                        console.log(schemes)
                        const news = schemes.filter(schema => schema["@type"] === "NewsArticle");
                        console.log(news)
                        if(news.length > 0)
                            this.validateSchema(news[0])
                    })
                }
            })
        },
        validateSchema(newsEntry) {
            let headline = newsEntry.headline;
            if(headline === undefined || headline === "") headline = newsEntry.name;

            let articleBody = newsEntry.articleBody;
            if(articleBody === undefined || articleBody === "") articleBody = newsEntry.description;

            const authors = newsEntry.author;
            const author = Array.isArray(authors) ? (authors.length > 0 ? authors[0].name : '') : authors.name;

            Vue.set(this.form.post, "Headline", headline);
            Vue.set(this.form.post, "Content", articleBody);
            Vue.set(this.form.post, "Author", author);
            this.getRandomImage();

        },
        startCrop() {
            Vue.set(this.form, "isCropping", true);
            if(this.form.cropper !== false) this.form.cropper.destroy();
            this.form.cropper = new Cropper(this.$refs.Image, {
                aspectRatio: 1,
                aspectRatio: this.aspect_ratio,
                zoomOnWheel: false,
                data:{ //define cropbox size
                    width: 240,
                    height:  90,
                  },
            });
        },
        stopCrop() {
            const data = this.form.cropper.getCroppedCanvas().toDataURL();
            this.form.cropper.destroy();
            this.form.cropper = false;
            Vue.set(this.form, "isCropping", false);
            this.$refs.CroppedCanvas.src = data;
        },
        getRandomImage() {
            this.imageLock = Math.floor(Math.random() * 100);
            const url = "https://loremflickr.com/320/240/?lock=" + this.imageLock;
            this.$refs.Image.src = url;
            this.$refs.CroppedCanvas.src = url;
        }
    },
    mounted() {
        this.$refs.file.addEventListener('change', evt => {
            const files = evt.target.files;
            if(files.length > 0) {
                const file = files[0];
                const reader = new FileReader();
                reader.onload = dataEvent => {
                    this.$refs.Image.src = dataEvent.target.result;
                    this.$refs.CroppedCanvas.src = dataEvent.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
        this.getRandomImage();
    }
  })