const buildWorkflow = () => ({
  id: "open_account",
  steps: [
    {
      step: 1,
      page: "/home",
      type: "form",
      highlight: "ui.form_login",
      action: "Fill in login form fields",
      behavior: {
        type: "form",
        completion: {
          type: "state",
          validator: (event) =>
            event?.source === "form" &&
            Boolean(event?.formData?.phone?.toString().trim()) &&
            Boolean(event?.formData?.code?.toString().trim()),
        },
      },
    },
    {
      step: 2,
      page: "/home",
      type: "form",
      highlight: "ui.btn_login",
      action: "Submit login",
      behavior: {
        type: "form",
        completion: {
          type: "event",
          validator: (event) =>
            event?.source === "fetch" &&
            event?.ok === true &&
            typeof event?.url === "string" &&
            event.url.includes("/auth/login") &&
            event?.status === 200,
        },
      },
    },
    {
      step: 3,
      page: "/home",
      type: "route",
      highlight: "ui.btn_login",
      action: "Navigate to customer center",
      behavior: {
        type: "route",
        completion: {
          type: "event",
          validator: (event) =>
            event?.source === "route" && event?.pathname === "/customer",
        },
      },
    },
    {
      step: 4,
      page: "/customer",
      type: "click",
      highlight: "ui.menu_open_account",
      action: "Click Open Account",
    },
    {
      step: 5,
      page: "/customer",
      type: "route",
      highlight: "ui.menu_open_account",
      action: "Navigate to account form page",
      behavior: {
        type: "route",
        completion: {
          type: "event",
          validator: (event) =>
            event?.source === "route" && event?.pathname === "/customer/create",
        },
      },
    },
    {
      step: 6,
      page: "/customer/create",
      type: "form",
      highlight: "ui.form_open_account",
      action: "Fill in account opening form fields",
      behavior: {
        type: "form",
        completion: {
          type: "state",
          validator: (event) => {
            if (event?.source !== "form") {
              return false;
            }
            const data = event?.formData || {};
            return (
              Boolean(data.name?.toString().trim()) &&
              Boolean(data.idCard?.toString().trim())
            );
          },
        },
      },
    },
    {
      step: 7,
      page: "/customer/create",
      type: "form",
      highlight: "ui.btn_submit_application",
      action: "Submit and wait for successful API response",
      behavior: {
        type: "form",
        completion: {
          type: "event",
          validator: (event) =>
            event?.source === "fetch" &&
            event?.ok === true &&
            typeof event?.url === "string" &&
            event.url.includes("/account/open") &&
            event?.status === 200,
        },
      },
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
  if (typeof window === "undefined") {
    return "/home";
  }
  return window.location.pathname || "/home";
};

export const initFlowPilot = () => {
  const FlowPilot = window.FlowPilot;
  if (!FlowPilot) {
    console.warn("[FlowPilot Demo] SDK not loaded, skip init.");
    return;
  }

  FlowPilot.init({
    workflow: buildWorkflow(),
    mapping: buildMapping(),
    getCurrentPage,
    autoStart: false,
  });
};
