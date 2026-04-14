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
            <div class="panel wide" data-guide-id="ui.form_login">
              <h2>安全登录</h2>
              <p>请输入您的登录信息，进入客户服务中心。</p>
              <form class="form-grid dense" @submit.prevent>
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
              </form>
              <div class="form-actions">
                <button
                  class="primary"
                  type="button"
                  data-guide-id="ui.btn_login"
                  :disabled="loginLoading"
                  @click="handleLogin"
                >
                  {{ loginLoading ? "登录中..." : "登录进入" }}
                </button>
              </div>
              <p v-if="loginMessage" class="inline-status">{{ loginMessage }}</p>
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
                  data-guide-id="ui.menu_overview"
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
                  data-guide-id="ui.menu_open_account"
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
                  data-guide-id="ui.menu_profile"
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
                  data-guide-id="ui.menu_funds"
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
            <div class="panel wide" data-guide-id="ui.form_open_account">
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
                  data-guide-id="ui.btn_submit_application"
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

</template>

<script setup>
import { ref } from "vue";
import { login, submitOpenAccount } from "../api/bank";

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
  activeMenu.value = "";
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

  const FlowPilot = window.FlowPilot;
  if (FlowPilot && typeof FlowPilot.next === "function") {
    FlowPilot.next();
    FlowPilot.next();
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

  const FlowPilot = window.FlowPilot;
  if (FlowPilot && typeof FlowPilot.next === "function") {
    FlowPilot.next();
    FlowPilot.next();
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
