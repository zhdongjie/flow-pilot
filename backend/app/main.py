from __future__ import annotations

from typing import Any
import uuid

from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn

from app.agent.engine import get_next_step, load_task
from app.agent.intent import detect_intent
from app.agent.responder import build_action_text, format_reply
from app.agent.state import get_current_page


app = FastAPI()


class StatePayload(BaseModel):
    current_page: str | None = Field(
        default=None, description="当前页面路径，例如 /customer"
    )
    auth: str | None = Field(default=None, description="认证状态，例如 authenticated")


class ChatRequest(BaseModel):
    message: str = Field(..., description="用户输入的意图文本，例如 我要开户")
    current_page: str | None = Field(
        default=None, description="当前页面路径（可选）"
    )
    current_step: int | None = Field(
        default=None, description="当前已完成的步骤编号（可选）"
    )
    state: StatePayload | None = Field(
        default=None, description="页面状态信息（可选）"
    )


class FormFieldPayload(BaseModel):
    field: str | None = Field(default=None, description="字段标识")
    desc: str | None = Field(default=None, description="字段说明")


class StepPayload(BaseModel):
    step: int | None = Field(default=None, description="步骤编号")
    page: str | None = Field(default=None, description="目标页面路径")
    action: str | None = Field(default=None, description="建议动作")
    highlight: str | None = Field(default=None, description="高亮目标标识")
    desc: str | None = Field(default=None, description="步骤说明")
    form: list[FormFieldPayload] | None = Field(
        default=None, description="需要填写的表单字段"
    )


class ChatResponse(BaseModel):
    reply: str = Field(..., description="完整流程 + 下一步引导话术")
    message: str = Field(..., description="简短指令文案")
    highlight: str | None = Field(
        default=None, description="需要高亮的 UI 元素标识"
    )
    reason: str = Field(..., description="给出该步骤的原因说明")
    next_step: StepPayload | None = Field(
        default=None, description="下一步结构化信息"
    )


class LoginRequest(BaseModel):
    phone: str = Field(..., description="登录手机号")
    code: str = Field(..., description="短信验证码")


class UserPayload(BaseModel):
    name: str = Field(..., description="用户名称")
    phone: str = Field(..., description="手机号")


class LoginResponse(BaseModel):
    status: str = Field(..., description="处理状态")
    intro: str = Field(..., description="引导介绍")
    user: UserPayload = Field(..., description="登录用户信息")


class OpenAccountRequest(BaseModel):
    name: str = Field(..., description="客户姓名")
    id_card: str = Field(..., description="身份证号")
    phone: str = Field(..., description="联系电话")
    risk_level: str = Field(..., description="风险等级")
    address: str = Field(..., description="开户地址")
    note: str | None = Field(default=None, description="备注")


class OpenAccountResponse(BaseModel):
    status: str = Field(..., description="处理状态")
    intro: str = Field(..., description="引导介绍")
    application_id: str = Field(..., description="申请编号")


def _normalize_state(state: Any) -> dict[str, Any]:
    if not isinstance(state, dict):
        return {}

    current_page = get_current_page(state)
    if current_page:
        normalized: dict[str, Any] = {"current_page": current_page}
    else:
        normalized = {}

    auth = state.get("auth")
    if isinstance(auth, str) and auth.strip():
        normalized["auth"] = auth

    return normalized


def _dump_state(state: StatePayload | None) -> dict[str, Any]:
    if state is None:
        return {}
    if hasattr(state, "model_dump"):
        return state.model_dump()
    return state.dict()


def _build_step_payload(step: dict[str, Any] | None) -> StepPayload | None:
    if step is None:
        return None
    if hasattr(StepPayload, "model_validate"):
        return StepPayload.model_validate(step)
    return StepPayload.parse_obj(step)  # type: ignore[attr-defined]



@app.post("/chat", response_model=ChatResponse, summary="开户引导对话接口")
def chat(payload: ChatRequest) -> ChatResponse:
    message = payload.message.strip()
    if not message:
        return ChatResponse(
            reply="未输入内容。",
            message="请输入意图，例如：我要开卡。",
            highlight=None,
            reason="未收到有效输入。",
            next_step=None,
        )

    state_payload = _dump_state(payload.state)
    if payload.current_page:
        state_payload["current_page"] = payload.current_page
    state = _normalize_state(state_payload)
    intent = detect_intent(message)
    if intent == "unknown":
        return ChatResponse(
            reply="未识别意图。",
            message="可以尝试输入：我要开卡。",
            highlight=None,
            reason="当前仅支持开户流程。",
            next_step=None,
        )

    try:
        task = load_task(intent)
    except FileNotFoundError:
        return ChatResponse(
            reply="未找到对应流程。",
            message="流程未配置，请检查流程文件。",
            highlight=None,
            reason="缺少对应的流程定义。",
            next_step=None,
        )

    step = get_next_step(task, state, payload.current_step)
    reply = format_reply(task, step, state)

    if step is None:
        return ChatResponse(
            reply=reply,
            message="流程已完成。",
            highlight=None,
            reason="已完成全部步骤。",
            next_step=None,
        )

    action_text = ""
    if isinstance(step.get("action"), str) and step.get("action").strip():
        action_text = step.get("action").strip()
    else:
        action_text = build_action_text(step)
    message_text = action_text if action_text else "请继续完成流程。"
    reason_text = (
        step.get("desc")
        if isinstance(step.get("desc"), str) and step.get("desc").strip()
        else "这是开户流程的下一步。"
    )
    highlight_key = None
    highlight_value = step.get("highlight")
    if isinstance(highlight_value, str) and highlight_value.strip():
        highlight_key = highlight_value

    return ChatResponse(
        reply=reply,
        message=message_text,
        highlight=highlight_key,
        reason=reason_text,
        next_step=_build_step_payload(step),
    )


@app.post("/auth/login", response_model=LoginResponse, summary="登录接口（模拟）")
def login(payload: LoginRequest) -> LoginResponse:
    user = UserPayload(name="客户", phone=payload.phone)
    intro = "登录成功，已进入客户服务中心。"
    return LoginResponse(status="ok", intro=intro, user=user)


@app.post(
    "/account/open", response_model=OpenAccountResponse, summary="开户申请接口（模拟）"
)
def open_account(payload: OpenAccountRequest) -> OpenAccountResponse:
    application_id = f"AP-{uuid.uuid4().hex[:8].upper()}"
    intro = f"已收到开户申请，编号 {application_id}，预计 1 个工作日内审核。"
    return OpenAccountResponse(
        status="submitted", intro=intro, application_id=application_id
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
