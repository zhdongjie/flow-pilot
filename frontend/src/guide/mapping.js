import mappingText from "./mapping.yaml?raw";

const parseMapping = (text) => {
  const mapping = {};
  let inMapping = false;
  let currentKey = "";
  let inFallback = false;
  let inPages = false;

  text.split(/\r?\n/).forEach((line) => {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      return;
    }
    if (trimmed === "mapping:") {
      inMapping = true;
      return;
    }
    if (!inMapping) {
      return;
    }
    const keyMatch = line.match(/^\s{2}([^:]+):\s*$/);
    if (keyMatch) {
      currentKey = keyMatch[1].trim();
      mapping[currentKey] = { selector: "", fallback: [], pages: [] };
      inFallback = false;
      inPages = false;
      return;
    }
    const selectorMatch = line.match(/^\s{4}selector:\s*(.+)$/);
    if (selectorMatch && currentKey) {
      let value = selectorMatch[1].trim();
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.slice(1, -1);
      }
      mapping[currentKey].selector = value;
      inFallback = false;
      inPages = false;
      return;
    }
    const fallbackMatch = line.match(/^\s{4}fallback:\s*$/);
    if (fallbackMatch && currentKey) {
      inFallback = true;
      inPages = false;
      return;
    }
    const pagesMatch = line.match(/^\s{4}pages:\s*$/);
    if (pagesMatch && currentKey) {
      inPages = true;
      inFallback = false;
      return;
    }
    const fallbackItemMatch = line.match(/^\s{6}-\s*(.+)$/);
    if (fallbackItemMatch && currentKey && inFallback) {
      let value = fallbackItemMatch[1].trim();
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.slice(1, -1);
      }
      mapping[currentKey].fallback.push(value);
    }
    if (fallbackItemMatch && currentKey && inPages) {
      let value = fallbackItemMatch[1].trim();
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.slice(1, -1);
      }
      mapping[currentKey].pages.push(value);
    }
  });

  return mapping;
};

const mapping = parseMapping(mappingText);

export const getSelectorsForHighlight = (key) => {
  if (!key) {
    return [];
  }
  const entry = mapping[key];
  const selectors = [];
  if (entry && entry.selector) {
    selectors.push(entry.selector);
  }
  if (entry && Array.isArray(entry.fallback)) {
    entry.fallback.forEach((item) => selectors.push(item));
  }
  const dataGuideSelector = `[data-guide-id="${key}"]`;
  if (!selectors.includes(dataGuideSelector)) {
    selectors.push(dataGuideSelector);
  }
  return selectors.filter(Boolean);
};

export const getPagesForHighlight = (key) => {
  const entry = mapping[key];
  if (!entry || !Array.isArray(entry.pages)) {
    return [];
  }
  return entry.pages;
};

const scoreElement = (element, priority) => {
  const rect = element.getBoundingClientRect();
  const width = Math.max(rect.width, 0);
  const height = Math.max(rect.height, 0);
  const area = width * height;
  const inViewport =
    rect.bottom > 0 &&
    rect.right > 0 &&
    rect.top < window.innerHeight &&
    rect.left < window.innerWidth;
  const visible = width > 0 && height > 0;
  const cx = rect.left + width / 2;
  const cy = rect.top + height / 2;
  const dx = Math.abs(cx - window.innerWidth / 2);
  const dy = Math.abs(cy - window.innerHeight / 2);
  const distance = Math.sqrt(dx * dx + dy * dy);

  let score = 0;
  score += (1000 - priority * 100);
  if (visible) {
    score += 300;
  }
  if (inViewport) {
    score += 200;
  }
  score += Math.min(area, 120000) / 120;
  score += Math.max(0, 500 - distance);
  return score;
};

export const findTargetForHighlight = (key) => {
  const selectors = getSelectorsForHighlight(key);
  const pages = getPagesForHighlight(key);
  let best = null;
  let bestScore = -Infinity;

  selectors.forEach((selector, index) => {
    document.querySelectorAll(selector).forEach((element) => {
      const score = scoreElement(element, index);
      if (score > bestScore) {
        bestScore = score;
        best = element;
      }
    });
  });

  return { element: best, selectors, pages };
};

export const auditMapping = () => {
  const report = [];
  Object.keys(mapping).forEach((key) => {
    const selectors = getSelectorsForHighlight(key);
    const pages = getPagesForHighlight(key);
    const found = selectors.some((selector) =>
      Boolean(document.querySelector(selector))
    );
    if (!found) {
      report.push({ key, selectors, pages });
    }
  });
  return report;
};
