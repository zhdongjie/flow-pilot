const buildWorkflow = () => ({
  id: "open_account",
  steps: [
    {
      step: 1,
      highlight: "ui.form_login",
      action: "填写登录信息",
      form: [
        { field: "phone", desc: "手机号" },
        { field: "code", desc: "验证码" },
      ],
    },
    {
      step: 2,
      highlight: "ui.btn_login",
      action: "点击【登录进入】",
    },
    {
      step: 3,
      highlight: "ui.menu_open_account",
      action: "点击【开户申请】",
    },
    {
      step: 4,
      highlight: "ui.form_open_account",
      action: "填写开户申请表单",
      form: [
        { field: "name", desc: "客户姓名" },
        { field: "idCard", desc: "身份证号" },
        { field: "phone", desc: "联系电话" },
        { field: "riskLevel", desc: "风险等级" },
        { field: "address", desc: "开户地址" },
        { field: "note", desc: "备注" },
      ],
    },
    {
      step: 5,
      highlight: "ui.btn_submit_application",
      action: "点击【提交申请】",
    },
  ],
});

const buildMapping = () => ({
  "ui.form_login": {
    selector: "[data-guide-id='ui.form_login']",
  },
  "ui.btn_login": {
    selector: "[data-guide-id='ui.btn_login']",
  },
  "ui.menu_open_account": {
    selector: "[data-guide-id='ui.menu_open_account']",
  },
  "ui.form_open_account": {
    selector: "[data-guide-id='ui.form_open_account']",
  },
  "ui.btn_submit_application": {
    selector: "[data-guide-id='ui.btn_submit_application']",
  },
});

const getCurrentPage = () => {
  if (document.querySelector(".login-page")) return "/home";
  if (document.querySelector(".menu-page")) return "/customer";
  if (document.querySelector(".form-page")) return "/customer/create";
  return "/";
};

export const initFlowPilot = () => {
  const FlowPilot = window.FlowPilot;
  if (!FlowPilot) {
    console.warn("[FlowPilot Demo] SDK 未加载，跳过初始化。");
    return;
  }
  FlowPilot.init({
    workflow: buildWorkflow(),
    mapping: buildMapping(),
    getCurrentPage,
  });
};
