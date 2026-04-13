# 🧠 FlowPilot - V1.5 PLAN (UI-Aware Guided Flow)

---

## 🎯 Goal

Build a system that:

> Understands user intent + detects current UI state + guides user step-by-step with UI highlights

---

## 🔥 Core Experience

User says:

👉 我要开户

System does:

1. Detect intent → open_account
2. Check current page
3. Decide:

   * continue flow OR
   * guide to correct entry point
4. Highlight UI element
5. Show instruction

---

## 🧠 Core Capability (NEW)

### 1️⃣ Route Awareness

System must:

* Read `current_page`
* Match with workflow steps

---

### 2️⃣ Path Recovery (CRITICAL)

Logic:

```
IF current_page in workflow:
    continue to next step
ELSE:
    find closest valid step
    guide user to it
```

---

### 3️⃣ UI Highlighting

Each step must support:

* highlight target (button / menu)
* instruction text

---

## 📚 YAML Upgrade (IMPORTANT)

```yaml
task:
  id: open_account

steps:
  - step: 1
    page: /home
    action: 进入客户管理
    highlight: menu_customer
    desc: 点击客户管理进入客户模块

  - step: 2
    page: /customer
    action: 点击开户按钮
    highlight: btn_open_account
    desc: 点击开户创建新账户

  - step: 3
    page: /customer/create
    form:
      - field: name
        desc: 客户姓名
      - field: riskLevel
        desc: 风险等级
```

---

## 🧠 Engine Logic (UPGRADE)

### Input

```json
{
  "message": "我要开户",
  "current_page": "/unknown"
}
```

---

### Output Decision

1. detect intent
2. load workflow
3. find current step

---

### Step Matching Logic

```python
if current_page in step_pages:
    return next_step
else:
    return first_reachable_step
```

---

## 🖥️ Frontend Requirement (NEW)

Frontend must support:

* receive `highlight` field
* visually highlight UI element
* show instruction popup

---

## 🔄 Response Format (UPDATED)

```json
{
  "message": "点击【客户管理】",
  "highlight": "menu_customer",
  "reason": "这是开户流程入口"
}
```

---

## 🧪 Demo Scenario

Case 1:

User at `/home`
→ highlight 客户管理

Case 2:

User at `/customer`
→ highlight 开户按钮

Case 3:

User at wrong page
→ guide to nearest step

---

## 🚫 Still NOT Allowed

* No OpenAPI
* No AI reasoning
* No dynamic planning

---

## ✅ Success Criteria

* System adapts to current page
* System highlights correct UI
* System does NOT restart blindly
* Feels like real training assistant

---

## 🔥 Key Upgrade

From:

👉 Static step output

To:

👉 Context-aware UI guidance
