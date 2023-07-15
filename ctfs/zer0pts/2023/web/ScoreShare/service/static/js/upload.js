window.onload = async() => {
    let config = await defaultConfig();
    document.getElementById('title').value = config?.template?.title || '';
    document.getElementById('abc').value = config?.template?.abc || '';
    document.getElementById('link').value = config?.template?.link || '';
};
