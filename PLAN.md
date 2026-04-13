# 🧠 FlowPilot - MVP PLAN (FULL VERSION)

---

## 🎯 Project Goal

Build a **minimal working demo** of an AI system that:

> Accepts user input → Understands intent → Guides user step-by-step through a system operation

---

## 🧪 Demo Scope (STRICT)

Only implement:

### ✅ MUST HAVE

* Open Account (开户流程)

### ⚠️ OPTIONAL

* Transfer (转账流程)

---

## ❌ Out of Scope (DO NOT BUILD)

* No generic workflow engine
* No AI reasoning system
* No RAG / knowledge base
* No OpenAPI integration
* No automation / execution engine

---

## ⚙️ Tech Stack (MANDATORY)

### Backend

* Python == 3.11.9
* Poetry (dependency management)
* FastAPI

### Frontend

* Vue 3
* Vite
* Composition API

---

## 🏗️ System Architecture (FIXED)

User Input
→ Intent Detection (rule-based)
→ Load YAML Task
→ Step Engine (based on state)
→ Response Generator

---

## 📦 Project Structure

```
project/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── agent/
│   │   │   ├── intent.py
│   │   │   ├── engine.py
│   │   │   ├── state.py
│   │   │   └── responder.py
│   │   ├── kb/
│   │   │   └── tasks/
│   │   │       └── open_account.yaml
│   │   └── schemas/
│   │       └── task_schema.py
│   │
│   ├── pyproject.toml
│   └── poetry.lock
│
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── components/
│   │   │   └── ChatPanel.vue
│   │   └── api/
│   │       └── chat.ts
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── PLAN.md
└── .cursorrules
```

---

## 📚 Data Design (YAML Workflow)

### File: `open_account.yaml`

```yaml
task:
  id: open_account
  name: 开户流程

steps:
  - step: 1
    page: /home
    action: 进入客户管理

  - step: 2
    page: /customer
    action: 点击开户按钮

  - step: 3
    page: /customer/create
    form:
      - field: name
        desc: 客户姓名
      - field: riskLevel
        desc: 风险等级

  - step: 4
    action: 点击提交
```

---

## 🧠 Module Design

---

### 1️⃣ intent.py

Purpose:

* Detect user intent

Rules:

* MUST be rule-based
* NO AI usage

Example:

```python
def detect_intent(text: str) -> str:
    if "开卡" in text or "开户" in text:
        return "open_account"
    return "unknown"
```

---

### 2️⃣ state.py

Purpose:

* Represent current UI state

Example:

```python
def get_state():
    return {
        "current_page": "/customer"
    }
```

---

### 3️⃣ engine.py

Purpose:

* Determine next step

Logic:

* Compare current_page with steps
* Return next actionable step

---

### 4️⃣ responder.py

Purpose:

* Format output for user

Rules:

* Must be actionable
* Must be step-by-step

Example Output:

👉 当前页面：客户管理

建议下一步：
点击【开户】

原因：
这是开户流程的下一步

---

## 🚀 Backend API (FastAPI)

### Endpoint

POST `/chat`

---

### Request

```json
{
  "message": "我要开卡",
  "state": {
    "current_page": "/customer"
  }
}
```

---

### Response

```json
{
  "reply": "text guidance",
  "next_step": {
    "step": 2,
    "action": "点击开户按钮"
  }
}
```

---

## 💻 CLI Mode (FIRST IMPLEMENTATION)

Before frontend:

```bash
python main.py
```

Example:

```
输入：我要开卡
输出：下一步操作
```

---

## 🎨 Frontend Design (Vue3)

### Component: ChatPanel.vue

Must include:

* Input box
* Submit button
* Response display
* Current step display

---

### API Call

`POST /chat`

---

## 🔄 Development Steps (STRICT ORDER)

---

### Step 1

* Create Poetry project
* Setup FastAPI

---

### Step 2

* Implement intent detection

---

### Step 3

* Create YAML workflow

---

### Step 4

* Implement step engine

---

### Step 5

* Implement CLI demo

---

### Step 6

* Add FastAPI endpoint

---

### Step 7

* Build Vue3 UI

---

## 🧪 Testing Requirements

* Test intent detection
* Test step engine
* Ensure correct step output

---

## ✅ Success Criteria

The demo is successful if:

1. User enters: “我要开卡”
2. System detects intent correctly
3. System returns correct next step
4. Output is actionable
5. Feels like human guidance

---

## 🚫 Anti-Scope Rules

DO NOT:

* Build reusable framework
* Add abstraction layers
* Introduce AI/LLM
* Optimize for scalability
* Implement future features

---

## 🔥 Final Principle

> Build the simplest system that works.

---

## 🧭 Completion Definition

Project is DONE when:

* CLI works
* API works
* UI works
* Workflow is correct

---

## 🧨 Absolute Rule

If a feature is not required for MVP:

👉 DO NOT BUILD IT
