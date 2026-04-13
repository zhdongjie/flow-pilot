from __future__ import annotations

from typing import Any
import uuid

from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn

from app.agent.engine import get_next_step, load_task
from app.agent.intent import detect_intent
from app.agent.responder import format_reply
from app.agent.state import get_current_page


app = FastAPI()


class StatePayload(BaseModel):
    current_page: str | None = Field(
        default=None, description="当前页面路径，例如 /customer"
    )


class ChatRequest(BaseModel):
    message: str = Field(..., description="用户输入的意图文本，例如 我要开户")
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
    form: list[FormFieldPayload] | None = Field(
        default=None, description="需要填写的表单字段"
    )


class ChatResponse(BaseModel):
    reply: str = Field(..., description="可直接展示的引导话术")
    intro: str = Field(..., description="引导简介，用于页面提示")
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
        return {"current_page": current_page}

    return {}


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


def _build_intro(step: dict[str, Any] | None, state: dict[str, Any] | None) -> str:
    page = state.get("current_page") if state else None
    page_label = page or "未知页面"
    if step is None:
        return "未找到可执行步骤，请确认流程配置。"
    action = step.get("action") or "继续执行下一步操作"
    step_page = step.get("page")
    if step_page and step_page != page_label:
        return f"当前页面：{page_label}，建议前往 {step_page} 并执行：{action}。"
    return f"当前页面：{page_label}，建议执行：{action}。"


@app.post("/chat", response_model=ChatResponse, summary="开户引导对话接口")
def chat(payload: ChatRequest) -> ChatResponse:
    message = payload.message.strip()
    if not message:
        return ChatResponse(
            reply="未输入内容。",
            intro="请输入意图，例如：我要开户。",
            next_step=None,
        )

    state = _normalize_state(_dump_state(payload.state))
    intent = detect_intent(message)
    if intent == "unknown":
        return ChatResponse(
            reply="未识别意图。",
            intro="可以尝试输入：我要开户。",
            next_step=None,
        )

    try:
        task = load_task(intent)
    except FileNotFoundError:
        return ChatResponse(
            reply="未找到对应流程。",
            intro="请确认流程文件是否存在。",
            next_step=None,
        )

    step = get_next_step(task, state)
    reply = format_reply(task, step, state)
    intro = _build_intro(step, state)

    return ChatResponse(
        reply=reply,
        intro=intro,
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
