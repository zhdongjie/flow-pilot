# FlowPilot

FlowPilot 是一个**外挂式引导层** Demo：用户只说一句话，系统就能高亮并引导完成银行开户流程。  
引导层运行在 Shadow DOM 中，**不污染业务系统样式**，仅通过 DOM 标记定位目标元素。

---

## 当前阶段

已进入 Phase 3（UI Mapping Registry）。  
流程与 UI 开始解耦，DOM 选择器由映射表维护。

---

## 关键能力

* 用户输入 → 意图识别 → YAML 流程 → 引导输出
* Shadow DOM 引导层（不污染业务样式）
* 高亮 + 气泡提示 + 自动推进
* 表单步骤统一“我已填写，继续”

---

## 技术栈

后端：Python 3.11.9 / FastAPI / Poetry  
前端：Vue 3 / Vite / Composition API

---

## 核心架构

```
用户输入 → 意图识别（规则） → 加载 YAML → Step Engine → 引导输出
```

---

## 项目结构

* `backend/app`：FastAPI 入口与业务接口  
* `backend/app/agent`：意图识别 / Step Engine / 输出格式  
* `backend/app/kb/tasks`：流程 YAML  
* `frontend/src/components/ChatPanel.vue`：业务系统 UI  
* `frontend/src/guide`：外挂引导层（Shadow DOM）  

---

## 运行方式

后端：
```bash
cd backend
poetry install
poetry run python app/main.py
```

前端：
```bash
cd frontend
npm install
npm run dev
```

打开：`http://localhost:5173`

---

## Guide Layer（外挂引导层）

引导层挂载在 `document.body` 的 Shadow DOM 中，不影响业务样式。  
业务系统只需要提供 `data-guide-id` 标记，DOM 选择器由映射表统一管理。

DOM 标记示例：
```html
<button data-guide-id="btn_login">登录进入</button>
<div data-guide-id="menu_open_account">开户申请</div>
```

---

## YAML 流程（Phase 2）

文件：`backend/app/kb/tasks/open_account.yaml`

示例结构：
```yaml
task:
  id: open_account
  name: 开户申请流程

steps:
  - step: 1
    page: /home
    action: 填写登录信息
    highlight: form_login
    desc: 输入手机号与验证码
    form:
      - field: phone
        desc: 手机号
      - field: code
        desc: 验证码
```

---

## UI Mapping Registry（Phase 3）

文件：`frontend/src/guide/mapping.yaml`

```yaml
mapping:
  ui.btn_login:
    selector: "[data-guide-id='ui.btn_login']"
    fallback:
      - "button.login-button"
    pages:
      - /home
  ui.menu_open_account:
    selector: "[data-guide-id='ui.menu_open_account']"
    fallback:
      - ".menu-item.open-account"
    pages:
      - /customer
```

说明：
* `highlight` 只输出业务语义（如 `ui.btn_login`）  
* 引导层通过 mapping 查找真实 DOM 选择器  
* selector 失效时会尝试 fallback，并在控制台提示  
* pages 可限制该 highlight 仅在指定页面生效  
* DEV 模式下会出现 Mapping 缺失提示面板  

---

## /chat 接口

请求：
```json
{
  "message": "我要开卡",
  "current_page": "/customer",
  "current_step": 3
}
```

响应：
```json
{
  "reply": "完整流程 + 下一步话术",
  "message": "点击【开户申请】",
  "highlight": "menu_open_account",
  "reason": "进入开户申请表单页面",
  "next_step": {
    "step": 3,
    "page": "/customer",
    "action": "点击【开户申请】",
    "highlight": "menu_open_account",
    "desc": "进入开户申请表单页面"
  }
}
```

说明：
* `message` 与 `highlight` 用于引导层高亮与提示
* `current_step` 用于自动推进（点击高亮后无需重复输入）

---

## 引导行为

* 点击高亮元素自动进入下一步  
* 表单步骤显示“我已填写，继续”按钮  
* 流程完成后返回“✅ 已完成”  

---

## Demo 成功标准

* 用户输入“我要开卡”
* 系统能定位第一步并高亮
* 点击高亮后自动进入下一步
* 引导层不影响业务系统样式
