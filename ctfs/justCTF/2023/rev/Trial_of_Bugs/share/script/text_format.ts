const REGEX = /\{[a-zA-Z0-9_.]+}/g;

export function applyFormat(text: string, context: any) {
    let resultText = '';
    let i = 0;
    let match;
    while ((match = REGEX.exec(text))) {
        let expr = text.substring(match.index! + 1, match.index! + match[0].length - 1);
        resultText += text.substring(i, match.index!);
        i = match.index! + match[0].length;

        resultText += expr.split('.').reduce((x: any, y) => x[y], context);
    }
    resultText += text.substring(i);
    return resultText;
}
