<template>
  <div class="bank-shell">
    <header class="bank-header">
      <div class="brand">
        <div class="brand-mark">FP</div>
        <div>
          <p class="brand-name">FlowPilot Bank</p>
          <p class="brand-tag">客户服务系统 · 银行开户模拟</p>
        </div>
      </div>
      <div class="header-actions">
        <span class="status-pill">系统在线</span>
        <button class="ghost" type="button" @click="resetDemo">重置演示</button>
      </div>
    </header>

    <div class="bank-body">
      <section class="bank-main">
        <div class="page-screen">
          <Transition name="page" mode="out-in">
            <section v-if="activePage === 'login'" key="login" class="page login-page">
            <div class="panel">
              <h2>安全登录</h2>
              <p>请输入您的登录信息，进入客户服务中心。</p>
              <div class="form-grid">
                <label>
                  手机号
                  <input
                    v-model="loginPhone"
                    type="text"
                    placeholder="11 位手机号"
                  />
                </label>
                <label>
                  验证码
                  <input
                    v-model="loginCode"
                    type="text"
                    placeholder="短信验证码"
                  />
                </label>
              </div>
              <div class="action-row">
                <button
                  class="primary"
                  type="button"
                  :disabled="loginLoading"
                  @click="handleLogin"
                >
                  {{ loginLoading ? "登录中..." : "登录进入" }}
                </button>
                <p v-if="loginMessage" class="inline-status">{{ loginMessage }}</p>
              </div>
            </div>
            <div class="info-panel">
              <h3>登录提示</h3>
              <ul>
                <li>请使用本人实名手机号</li>
                <li>验证码有效期 5 分钟</li>
                <li>若未收到验证码请稍后重试</li>
              </ul>
            </div>
            </section>
            <section v-else-if="activePage === 'menu'" key="menu" class="page menu-page">
            <div class="panel wide">
              <h2>客户服务中心</h2>
              <p>选择业务办理入口，进入对应流程。</p>
              <div class="menu-grid">
                <div
                  class="menu-item"
                  :class="{ active: activeMenu === 'overview' }"
                  role="button"
                  tabindex="0"
                  @click="selectMenu('overview')"
                >
                  <p>账户概览</p>
                  <span>查看账户状态</span>
                </div>
                <div
                  class="menu-item"
                  :class="{ active: activeMenu === 'open' }"
                  role="button"
                  tabindex="0"
                  @click="selectMenu('open')"
                >
                  <p>开户申请</p>
                  <span>开立新账户</span>
                </div>
                <div
                  class="menu-item"
                  :class="{ active: activeMenu === 'profile' }"
                  role="button"
                  tabindex="0"
                  @click="selectMenu('profile')"
                >
                  <p>资料管理</p>
                  <span>更新个人信息</span>
                </div>
                <div
                  class="menu-item"
                  :class="{ active: activeMenu === 'funds' }"
                  role="button"
                  tabindex="0"
                  @click="selectMenu('funds')"
                >
                  <p>资金服务</p>
                  <span>转账与充值</span>
                </div>
              </div>
            </div>
            <div class="info-panel">
              <h3>业务提示</h3>
              <p>开户申请需要填写客户姓名、风险等级等信息。</p>
            </div>
            </section>
            <section v-else key="form" class="page form-page">
            <div class="panel wide">
              <h2>开户申请表单</h2>
              <p>请完整填写开户信息，提交后进入审核流程。</p>
              <form class="form-grid dense" @submit.prevent>
                <label>
                  客户姓名
                  <input v-model="formName" type="text" placeholder="例如：张三" />
                </label>
                <label>
                  身份证号
                  <input
                    v-model="formIdCard"
                    type="text"
                    placeholder="18 位身份证号"
                  />
                </label>
                <label>
                  联系电话
                  <input
                    v-model="formPhone"
                    type="text"
                    placeholder="预留手机号"
                  />
                </label>
                <label>
                  风险等级
                  <select v-model="formRisk">
                    <option value="">请选择风险等级</option>
                    <option value="低风险">低风险</option>
                    <option value="中风险">中风险</option>
                    <option value="高风险">高风险</option>
                  </select>
                </label>
                <label class="full">
                  开户地址
                  <input
                    v-model="formAddress"
                    type="text"
                    placeholder="开户地址信息"
                  />
                </label>
                <label class="full">
                  备注
                  <textarea
                    v-model="formNote"
                    rows="3"
                    placeholder="补充说明"
                  ></textarea>
                </label>
              </form>
              <div class="form-actions">
                <button class="ghost" type="button" @click="goToMenu">
                  返回用户中心
                </button>
                <button
                  class="primary"
                  type="button"
                  :disabled="formLoading"
                  @click="handleSubmit"
                >
                  {{ formLoading ? "提交中..." : "提交申请" }}
                </button>
              </div>
              <p v-if="formMessage" class="inline-status">{{ formMessage }}</p>
            </div>
            <div class="info-panel">
              <h3>审核说明</h3>
              <p>提交后预计 1 个工作日内完成审核。</p>
            </div>
            </section>
          </Transition>
        </div>
      </section>
    </div>
  </div>

  <button class="chat-fab" type="button" @click="toggleChat">
    在线客服
  </button>

  <Transition name="chat">
    <div v-if="chatOpen" class="chat-window floating" role="dialog">
      <header class="chat-header">
        <div>
          <p class="chat-title">智能客服</p>
          <span class="chat-subtitle">开户引导助手</span>
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
          <p>{{ item.text }}</p>
        </div>
        <div v-if="chatLoading" class="chat-bubble assistant">
          <span class="role">客服</span>
          <p>正在为你解析意图...</p>
        </div>
      </div>

      <form class="chat-input" @submit.prevent="sendMessage">
        <input
          v-model="chatInput"
          type="text"
          placeholder="例如：我要开户"
          autocomplete="off"
        />
        <button type="submit" :disabled="chatLoading">发送</button>
      </form>

      <p v-if="messages.length" class="chat-footnote">
        当前页面：{{ currentPageLabel }}
      </p>
      <p v-if="chatError" class="chat-error">{{ chatError }}</p>
    </div>
  </Transition>
</template>

<script setup>
import { computed, nextTick, ref } from "vue";
import { sendChat } from "../api/chat";
import { login, submitOpenAccount } from "../api/bank";

const pages = [
  { key: "login", label: "登录页", pageId: "/home" },
  { key: "menu", label: "用户中心", pageId: "/customer" },
  { key: "form", label: "开户申请", pageId: "/customer/create" },
];

const activePage = ref("login");
const activeMenu = ref("");
const loginPhone = ref("");
const loginCode = ref("");
const loginLoading = ref(false);
const loginMessage = ref("");

const formName = ref("");
const formIdCard = ref("");
const formPhone = ref("");
const formRisk = ref("");
const formAddress = ref("");
const formNote = ref("");
const formLoading = ref(false);
const formMessage = ref("");

const chatOpen = ref(false);
const chatInput = ref("");
const chatLoading = ref(false);
const chatError = ref("");
const chatBody = ref(null);

let messageId = 1;
const messages = ref([]);

const currentPage = computed(() => pages.find((page) => page.key === activePage.value));

const currentPageLabel = computed(() => currentPage.value?.label || "未知页面");

const currentPagePath = computed(() => currentPage.value?.pageId || "-");

const goToMenu = () => {
  activePage.value = "menu";
  activeMenu.value = "";
};

const goToForm = () => {
  activePage.value = "form";
};

const resetDemo = () => {
  activePage.value = "login";
  loginPhone.value = "";
  loginCode.value = "";
  loginMessage.value = "";
  formName.value = "";
  formIdCard.value = "";
  formPhone.value = "";
  formRisk.value = "";
  formAddress.value = "";
  formNote.value = "";
  formMessage.value = "";
  chatError.value = "";
  messages.value = [];
  activeMenu.value = "";
};

const toggleChat = () => {
  chatOpen.value = !chatOpen.value;
  chatError.value = "";
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

const sendMessage = async () => {
  const text = chatInput.value.trim();
  if (!text || chatLoading.value) {
    return;
  }
  chatError.value = "";
  chatInput.value = "";
  pushMessage("user", text);

  chatLoading.value = true;
  try {
    const data = await sendChat(text, currentPagePath.value);
    pushMessage("assistant", data.reply || "已收到，请继续。");
  } catch (err) {
    chatError.value = "请求失败，请确认后端服务已启动。";
    pushMessage("assistant", "我暂时无法连接系统，请稍后再试。");
  } finally {
    chatLoading.value = false;
  }
};

const selectMenu = (key) => {
  activeMenu.value = key;
  if (key === "open") {
    goToForm();
  }
};

const handleLogin = async () => {
  if (loginLoading.value) {
    return;
  }
  loginMessage.value = "";
  const phone = loginPhone.value.trim();
  const code = loginCode.value.trim();
  if (!phone || !code) {
    loginMessage.value = "请输入手机号和验证码。";
    return;
  }
  loginLoading.value = true;
  try {
    const data = await login(phone, code);
    loginMessage.value = data.intro || "登录成功。";
    activePage.value = "menu";
  } catch (err) {
    loginMessage.value = "登录失败，请稍后再试。";
  } finally {
    loginLoading.value = false;
  }
};

const handleSubmit = async () => {
  if (formLoading.value) {
    return;
  }
  formMessage.value = "";
  if (!formName.value.trim() || !formIdCard.value.trim()) {
    formMessage.value = "请至少填写姓名和身份证号。";
    return;
  }
  formLoading.value = true;
  try {
    const data = await submitOpenAccount({
      name: formName.value.trim(),
      id_card: formIdCard.value.trim(),
      phone: formPhone.value.trim(),
      risk_level: formRisk.value || "未选择",
      address: formAddress.value.trim(),
      note: formNote.value.trim(),
    });
    formMessage.value = data.intro || "申请已提交。";
  } catch (err) {
    formMessage.value = "提交失败，请稍后再试。";
  } finally {
    formLoading.value = false;
  }
};
</script>
