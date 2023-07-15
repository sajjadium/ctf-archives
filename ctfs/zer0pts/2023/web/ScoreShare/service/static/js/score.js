async function loadScore(sid) {
    let promise = await fetch(`/api/score/${sid}`);
    return await promise.text();
}

window.onload = async() => {
    let config = await defaultConfig();
    let abc = await loadScore(document.getElementById('sid').value);
    document.getElementById('abc').value = abc;

    let synth = { el: '#audio' };
    if (typeof config !== 'undefined') {
        for (let i = 0; i < config.synth_options.length; i++) {
            let option = config.synth_options[i];
            if (typeof option.value === 'object') {
                if (synth[option.name] === undefined)
                    synth[option.name] = {};
                let param = synth[option.name];
                Object.getOwnPropertyNames(option.value).forEach(key => {
                    param[key] = option.value[key];
                });
            } else {
                synth[option.name] = option.value;
            }
        }
    }

    new ABCJS.Editor('abc', { paper_id: 'paper', synth });
};
