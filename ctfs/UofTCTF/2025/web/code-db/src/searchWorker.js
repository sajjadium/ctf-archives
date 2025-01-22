// searchWorker.js
import { parentPort, workerData } from 'worker_threads';
import fs from 'fs';

function handleRegexSearch(content, regex) {
  const matches = Array.from(content.matchAll(regex));
  return matches.map(match => ({
    start: match.index,
    end: match.index + match[0].length
  }));
}

function handleNormalSearch(content, searchTerm) {
  const matches = [];
  let idx = content.toLowerCase().indexOf(searchTerm);
  while (idx !== -1) {
    matches.push({
      start: idx,
      end: idx + searchTerm.length
    });
    idx = content.toLowerCase().indexOf(searchTerm, idx + searchTerm.length);
  }
  return matches;
}

function generatePreview(content, matchIndices, previewLength) {
  if (matchIndices.length === 0) return null;

  const firstMatch = matchIndices[0];
  const start = Math.max(firstMatch.start - previewLength, 0);
  const end = Math.min(firstMatch.end + previewLength, content.length);
  let preview = content.substring(start, end);

  const adjustedIndices = matchIndices
    .map(match => ({
      start: match.start - start,
      end: match.end - start
    }))
    .filter(match => match.start >= 0 && match.end <= preview.length)
    .sort((a, b) => b.start - a.start);

  adjustedIndices.forEach(match => {
    preview =
      preview.slice(0, match.start) +
      `<mark>${preview.slice(match.start, match.end)}</mark>` +
      preview.slice(match.end);
  });

  return (preview.includes("<mark></mark>")) ? null : preview;
}

const { filesIndex, language, searchRegex, searchTerm, PREVIEW_LENGTH } = workerData;

const results = Object.entries(filesIndex)
  .filter(([fileName, fileData]) => {
    if (language && language !== 'All') {
      return fileData.language === language;
    }
    return true;
  })
  .map(([fileName, fileData]) => {
    let content;
    try {
      content = fs.readFileSync(fileData.path, 'utf-8');
    } catch (e) {
      return null;
    }

    let matchIndices = [];
    if (searchRegex) {
      matchIndices = handleRegexSearch(content, searchRegex);
    } else if (searchTerm) {
      matchIndices = handleNormalSearch(content, searchTerm);
    }

    if (matchIndices.length === 0) return null;

    const preview = generatePreview(content, matchIndices, PREVIEW_LENGTH);
    return preview
      ? {
          fileName,
          preview,
          language: fileData.language,
          visible: fileData.visible
        }
      : null;
  })
  .filter(result => result !== null && result.visible);

parentPort.postMessage({ results });
