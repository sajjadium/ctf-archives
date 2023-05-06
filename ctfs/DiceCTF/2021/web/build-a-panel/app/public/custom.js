const mergableTypes = ['boolean', 'string', 'number', 'bigint', 'symbol', 'undefined'];

const safeDeepMerge = (target, source) => {
    for (const key in source) {
        if(!mergableTypes.includes(typeof source[key]) && !mergableTypes.includes(typeof target[key])){
            if(key !== '__proto__'){
                safeDeepMerge(target[key], source[key]);
            }
        }else{
            target[key] = source[key];
        }
    }
}

const displayWidgets = async () => {
    const userWidgets = await (await fetch('/panel/widgets', {method: 'post', credentials: 'same-origin'})).json();
    let toDisplayWidgets = {'welcome back to build a panel!': {'type': 'welcome'}};

    safeDeepMerge(toDisplayWidgets, userWidgets);

    const timeData = await (await fetch('/status/time')).json();
    const weatherData = await (await fetch('/status/weather')).json();
    const welcomeData = await (await fetch('/status/welcome')).json();

    const widgetData = {'time': timeData['data'], 'weather': weatherData['data'], 'welcome': welcomeData['data']};

    const widgetPanel = document.getElementById('widget-panel');
    for(let name of Object.keys(toDisplayWidgets)){
        const widgetType = toDisplayWidgets[name]['type'];

        const panel = document.createElement('div');
        panel.className = 'panel panel-default';

        const panelTitle = document.createElement('h5');
        panelTitle.className = 'panel-heading';
        panelTitle.textContent = name;

        const panelData = document.createElement('p');
        panelData.className = 'panel-body';
        if(widgetData[widgetType]){
            panelData.textContent = widgetData[widgetType];
        }else{
            panelData.textContent = 'The widget type does not exist, make sure you spelled it right.';
        }

        panel.appendChild(panelTitle);
        panel.appendChild(panelData);

        widgetPanel.appendChild(panel);
    }
};

window.onload = (_event) => {
    displayWidgets();
};