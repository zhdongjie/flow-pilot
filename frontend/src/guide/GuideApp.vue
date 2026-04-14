<template>
  <div class="guide-root">
    <GuideStep
      :rect="highlightRect"
      :message="highlightMessage"
      :reason="highlightReason"
      :show-next="showNextButton"
      @next="autoAdvance"
    />

    <button class="chat-fab" type="button" @click="toggleChat">在线客服</button>

    <p v-if="missingTargetKey" class="guide-warning">
      未找到目标元素：{{ missingTargetKey }}
    </p>

    <button
      v-if="mappingReport.length"
      class="mapping-pill"
      type="button"
      @click="showMappingPanel = !showMappingPanel"
    >
      Mapping 缺失 {{ mappingReport.length }}
    </button>

    <div v-if="showMappingPanel" class="mapping-panel">
      <p class="mapping-title">Mapping 校验报告</p>
      <ul class="mapping-list">
        <li v-for="item in mappingReport" :key="item.key">
          <strong>{{ item.key }}</strong>
          <div class="mapping-selectors">
            {{ item.selectors.join(" | ") }}
          </div>
          <div v-if="item.pages && item.pages.length" class="mapping-pages">
            pages: {{ item.pages.join(", ") }}
          </div>
        </li>
      </ul>
    </div>

    <div v-if="chatOpen" class="chat-window" role="dialog">
      <header class="chat-header">
        <div>
          <p class="chat-title">智能客服</p>
          <span class="chat-subtitle">流程引导助手</span>
        </div>
        <button class="icon" type="button" @click="toggleChat">×</button>
      </header>

      <div ref="chatBody" class="chat-body">
        <div
          v-for="item in messages"
          :key="item.id"
          :class="['chat-bubble', item.role]"
        >
          <span class="role">{{ item.role === 'assistant' ? '客服' : '我' }}</span>
          <pre>{{ item.text }}</pre>
        </div>
        <div v-if="chatLoading" class="chat-bubble assistant">
          <span class="role">客服</span>
          <p>正在解析意图...</p>
        </div>
      </div>

      <form class="chat-input" @submit.prevent="sendMessage">
        <input
          v-model="chatInput"
          type="text"
          placeholder="例如：我要开卡"
          autocomplete="off"
        />
        <button type="submit" :disabled="chatLoading">发送</button>
      </form>

      <p v-if="chatError" class="chat-error">{{ chatError }}</p>
    </div>
  </div>
</template>

<script setup>
import { nextTick, onMounted, onUnmounted, ref, watch } from "vue";
import { sendChat } from "../api/chat";
import GuideStep from "./GuideStep.vue";
import { auditMapping, findTargetForHighlight } from "./mapping";

const chatOpen = ref(false);
const chatInput = ref("");
const chatLoading = ref(false);
const chatError = ref("");
const chatBody = ref(null);
const messages = ref([]);
const highlightKey = ref("");
const highlightMessage = ref("");
const highlightReason = ref("");
const highlightRect = ref(null);
const highlightPage = ref("");
const lastIntent = ref("");
const currentStep = ref(null);
const showNextButton = ref(false);
const lastScrollToken = ref("");
const missingTargetKey = ref("");
const mappingReport = ref([]);
const showMappingPanel = ref(false);
const missingTargetKey = ref("");

let messageId = 1;
let domObserver = null;

const getCurrentPage = () => window.location.pathname || "";

const updateHighlightRect = () => {
  if (!highlightKey.value) {
    highlightRect.value = null;
    return;
  }
  const page = getCurrentPage();
  const { element: target, selectors, pages } = findTargetForHighlight(
    highlightKey.value
  );
  if (pages.length && page && !pages.includes(page)) {
    highlightRect.value = null;
    return;
  }
  if (!target) {
    highlightRect.value = null;
    if (highlightKey.value && missingTargetKey.value !== highlightKey.value) {
      missingTargetKey.value = highlightKey.value;
      console.warn(
        `[FlowPilot] 未找到目标元素: ${highlightKey.value}`,
        selectors
      );
    }
    return;
  }
  if (missingTargetKey.value) {
    missingTargetKey.value = "";
  }
  if (missingTargetKey.value === highlightKey.value) {
    missingTargetKey.value = "";
  }
  const rect = target.getBoundingClientRect();
  const margin = 24;
  const inView =
    rect.top >= margin &&
    rect.left >= margin &&
    rect.bottom <= window.innerHeight - margin &&
    rect.right <= window.innerWidth - margin;
  const scrollToken = `${highlightKey.value}:${highlightPage.value || page}`;
  if (!inView && lastScrollToken.value !== scrollToken) {
    lastScrollToken.value = scrollToken;
    target.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  highlightRect.value = {
    top: rect.top,
    left: rect.left,
    width: rect.width,
    height: rect.height,
  };
};

const scheduleHighlightRetry = () => {
  const delays = [120, 280, 520, 820];
  delays.forEach((delay) => {
    setTimeout(() => {
      if (highlightKey.value) {
        updateHighlightRect();
      }
    }, delay);
  });
};

const startDomObserver = () => {
  if (domObserver) {
    return;
  }
  domObserver = new MutationObserver(() => {
    if (highlightKey.value) {
      updateHighlightRect();
    }
  });
  domObserver.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
  });
};

const stopDomObserver = () => {
  if (!domObserver) {
    return;
  }
  domObserver.disconnect();
  domObserver = null;
};


const clearHighlight = () => {
  highlightKey.value = "";
  highlightMessage.value = "";
  highlightReason.value = "";
  highlightPage.value = "";
  currentStep.value = null;
  showNextButton.value = false;
  lastScrollToken.value = "";
  highlightRect.value = null;
  missingTargetKey.value = "";
  stopDomObserver();
};

const handleDocumentClick = (event) => {
  if (!highlightKey.value || !lastIntent.value || chatLoading.value) {
    return;
  }
  if (highlightKey.value.startsWith("ui.form_")) {
    return;
  }
  const target = event.target;
  if (!(target instanceof Element)) {
    return;
  }
  const matched = target.closest(
    `[data-guide-id="${highlightKey.value}"]`
  );
  if (!matched) {
    return;
  }
  autoAdvance();
};

const toggleChat = () => {
  chatOpen.value = !chatOpen.value;
  if (chatOpen.value) {
    nextTick(() => {
      if (chatBody.value) {
        chatBody.value.scrollTop = chatBody.value.scrollHeight;
      }
    });
  }
};

const pushMessage = (role, text) => {
  messages.value.push({ id: messageId++, role, text });
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight;
    }
  });
};

const applyResponse = (data) => {
  highlightKey.value = data.highlight || "";
  highlightMessage.value = data.message || "";
  highlightReason.value = data.reason || "";
  highlightPage.value = data.next_step?.page || "";
  currentStep.value = data.next_step?.step ?? null;
  showNextButton.value = highlightKey.value.startsWith("ui.form_");
  if (!data.next_step) {
    clearHighlight();
  } else {
    updateHighlightRect();
    scheduleHighlightRetry();
    startDomObserver();
  }
};

const requestStep = async (text, step, addUserMessage) => {
  if (chatLoading.value) {
    return;
  }
  chatError.value = "";
  if (addUserMessage) {
    pushMessage("user", text);
  }

  chatLoading.value = true;
  try {
    const data = await sendChat(text, getCurrentPage(), step);
    applyResponse(data);
    let replyText = data.reply || "已收到，请继续。";
    if (!data.next_step) {
      replyText = `${replyText}\n\n✅ 已完成`;
    }
    pushMessage("assistant", replyText);
  } catch (err) {
    chatError.value = "请求失败，请确认后端服务已启动。";
    clearHighlight();
    pushMessage("assistant", "我暂时无法连接系统，请稍后再试。");
  } finally {
    chatLoading.value = false;
  }
};

const sendMessage = async () => {
  const text = chatInput.value.trim();
  if (!text || chatLoading.value) {
    return;
  }
  chatInput.value = "";
  lastIntent.value = text;
  await requestStep(text, null, true);
};

const autoAdvance = async () => {
  if (!lastIntent.value || currentStep.value == null) {
    return;
  }
  await requestStep(lastIntent.value, currentStep.value, false);
};

watch(highlightKey, () => {
  lastScrollToken.value = "";
  updateHighlightRect();
});

onMounted(() => {
  window.addEventListener("resize", updateHighlightRect);
  window.addEventListener("scroll", updateHighlightRect, true);
  document.addEventListener("click", handleDocumentClick, true);
  if (import.meta && import.meta.env && import.meta.env.DEV) {
    setTimeout(() => {
      const report = auditMapping();
      mappingReport.value = report;
      if (report.length) {
        console.warn("[FlowPilot] Mapping 校验未通过：", report);
      }
    }, 400);
  }
});

onUnmounted(() => {
  window.removeEventListener("resize", updateHighlightRect);
  window.removeEventListener("scroll", updateHighlightRect, true);
  document.removeEventListener("click", handleDocumentClick, true);
  stopDomObserver();
});
</script>
