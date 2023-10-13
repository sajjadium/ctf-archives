async function getCounters() {
    const response = await fetch('/api/counters');
    return response.json();
}

function url(strings, ...values) {
    return strings.reduce((result, string, i) => {
        const value = values[i - 1];
        if (typeof value === 'string') {
            return result + encodeURIComponent(value) + string;
        } else {
            return result + String(value) + string;
        }
    });
}

function escapeHtml(unsafe) {
    return unsafe.replace(/&/g, '&amp;')
                 .replace(/</g, '&lt;')
                 .replace(/>/g, '&gt;')
                 .replace(/"/g, '&quot;')
                 .replace(/'/g, '&apos;');
}

function html(strings, ...values) {
    return strings.reduce((result, string, i) => {
        const value = values[i - 1];
        if (typeof value === 'string') {
            return result + escapeHtml(value) + string;
        } else {
            return result + String(value) + string;
        }
    });
}

function parseElement(htmlString) {
    const doc = new DOMParser().parseFromString(htmlString, 'text/html');
    const elem = doc.body.firstElementChild;
    doc.body.removeChild(elem);
    return elem;
}

function elem(strings, ...values) {
    if (typeof strings === 'string') {
        return parseElement(strings);
    }
    return parseElement(html(strings, ...values));
}

async function createCounter(name, count) {
    const response = await fetch('/api/counters', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name,
            count,
        }),
    });
    return response.json();
}

async function renderCounters(counters) {
    let table = '<table><tr><th>Name</th><th>Count</th></tr>';
    for (const counter of counters) {
        table += '<tr>'
        table += html`<td>${counter.name}</td><td>${counter.count}</td>`;
        table += html`<td><button data-id="${counter.id}" data-action="decrement">-</button></td>`;
        table += html`<td><button data-id="${counter.id}" data-action="delete">Delete</button></td>`;
        table += '</tr>';
    }
    table += '</table>';
    const tableElem = elem(table);
    tableElem.querySelectorAll('button').forEach((button) => {
        button.onclick = async () => {
            const action = button.dataset.action;
            const id = button.dataset.id;
            if (action === 'decrement') {
                const response = await fetch(url`/api/counters/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ decrement: 1 }),
                });
                const counter = await response.json();
                button.parentElement.previousElementSibling.textContent = counter.count;
            } else if (action === 'delete') {
                const response = await fetch(url`/api/counters/${id}`, { method: 'DELETE' });
                if (response.ok) {
                    button.parentElement.parentElement.remove();
                }
            }
        };
    });
    document.body.appendChild(tableElem);
}

function randomString() {
    return Math.random().toString(36).slice(2);
}

window.onload = async () => {
    const counters = await getCounters();
    const button = elem`<button id="create-example">Add countdown</button>`;
    button.onclick = async () => {
        await createCounter(`example-${randomString()}`, 1337);
        location.reload();
    };
    document.body.appendChild(button);
    renderCounters(counters);
};
