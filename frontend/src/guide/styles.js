export const guideStyles = `
:host {
  all: initial;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  font-family: "Manrope", "Noto Sans SC", "PingFang SC", sans-serif;
}

.guide-root {
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none;
}

.mask-piece {
  position: fixed;
  background: rgba(12, 18, 28, 0.45);
  backdrop-filter: blur(1px);
  pointer-events: none;
  z-index: 1;
}

.highlight-box {
  position: fixed;
  border: 2px solid #f1b256;
  border-radius: 12px;
  box-shadow: 0 0 0 6px rgba(241, 178, 86, 0.22);
  pointer-events: none;
  transition: all 0.2s ease;
  animation: pulse 1.6s ease-in-out infinite;
  z-index: 2;
}

.tooltip {
  position: fixed;
  background: #0f1b2b;
  color: #f7f9fc;
  padding: 12px 14px;
  border-radius: 12px;
  max-width: 280px;
  font-size: 12px;
  line-height: 1.5;
  pointer-events: auto;
  box-shadow: 0 12px 26px rgba(8, 16, 28, 0.35);
  z-index: 3;
}

.tooltip-title {
  font-weight: 600;
  margin: 0 0 6px;
  font-size: 13px;
}

.tooltip-reason {
  margin: 0;
  opacity: 0.8;
}

.tooltip-action {
  margin-top: 10px;
  border: none;
  background: #f1b256;
  color: #1b1f23;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
}

.chat-fab {
  position: fixed;
  right: 24px;
  bottom: 24px;
  pointer-events: auto;
  border: none;
  background: linear-gradient(135deg, #0c5b4c, #083f34);
  color: #fff;
  border-radius: 999px;
  padding: 12px 18px;
  font-size: 14px;
  cursor: pointer;
  box-shadow: 0 14px 30px rgba(9, 40, 33, 0.3);
  z-index: 4;
}

.chat-window {
  position: fixed;
  right: 24px;
  bottom: 80px;
  width: min(380px, 100%);
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 18px 40px rgba(12, 24, 40, 0.2);
  display: grid;
  gap: 12px;
  padding: 16px;
  pointer-events: auto;
  z-index: 4;
}

.guide-warning {
  position: fixed;
  right: 24px;
  bottom: 150px;
  background: #ffe6dc;
  color: #8b2f1b;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 12px;
  pointer-events: none;
  z-index: 4;
}

.mapping-pill {
  position: fixed;
  right: 24px;
  bottom: 190px;
  background: #1e293b;
  color: #fff;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 12px;
  border: none;
  cursor: pointer;
  pointer-events: auto;
  z-index: 4;
}

.mapping-panel {
  position: fixed;
  right: 24px;
  bottom: 240px;
  width: 320px;
  max-height: 240px;
  overflow: auto;
  background: #ffffff;
  border-radius: 14px;
  box-shadow: 0 18px 40px rgba(12, 24, 40, 0.2);
  padding: 12px;
  font-size: 12px;
  color: #1b1f23;
  z-index: 4;
}

.mapping-title {
  margin: 0 0 8px;
  font-weight: 600;
}

.mapping-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
}

.mapping-selectors,
.mapping-pages {
  color: #5b6574;
  word-break: break-all;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chat-title {
  margin: 0;
  font-weight: 600;
  font-size: 14px;
  color: #101318;
}

.chat-subtitle {
  font-size: 12px;
  color: #5b6574;
}

.icon {
  border: none;
  background: #f1f3f7;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  cursor: pointer;
}

.chat-body {
  background: #f6f7fb;
  border-radius: 16px;
  padding: 12px;
  height: 280px;
  overflow-y: auto;
  display: grid;
  gap: 12px;
}

.chat-bubble {
  background: #fff;
  padding: 10px 12px;
  border-radius: 14px;
  display: grid;
  gap: 6px;
  font-size: 12px;
  color: #101318;
  border: 1px solid #e6eaf0;
  white-space: pre-wrap;
}

.chat-bubble pre {
  margin: 0;
  font-family: inherit;
  white-space: pre-wrap;
}

.chat-bubble.user {
  background: #102f4f;
  color: #fff;
  border-color: transparent;
  justify-self: end;
}

.chat-bubble .role {
  font-size: 11px;
  opacity: 0.7;
}

.chat-input {
  display: flex;
  gap: 8px;
}

.chat-input input {
  flex: 1;
  border-radius: 12px;
  border: 1px solid #dfe4ee;
  padding: 10px 12px;
  font-size: 13px;
}

.chat-input button {
  border: none;
  background: #0c5b4c;
  color: #fff;
  border-radius: 12px;
  padding: 10px 16px;
  cursor: pointer;
}

.chat-footnote {
  margin: 0;
  font-size: 12px;
  color: #5b6574;
}

.chat-error {
  margin: 0;
  font-size: 12px;
  color: #b23a2a;
}

@media (max-width: 640px) {
  .chat-window {
    right: 12px;
    left: 12px;
    width: auto;
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 6px rgba(241, 178, 86, 0.22);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(241, 178, 86, 0.35);
  }
  100% {
    box-shadow: 0 0 0 6px rgba(241, 178, 86, 0.22);
  }
}
`;
