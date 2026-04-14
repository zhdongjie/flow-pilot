import { createApp } from "vue";
import GuideApp from "./GuideApp.vue";
import { guideStyles } from "./styles";

export function mountGuideLayer() {
  if (document.getElementById("flowpilot-guide-layer")) {
    return;
  }

  const host = document.createElement("div");
  host.id = "flowpilot-guide-layer";
  document.body.appendChild(host);

  const shadow = host.attachShadow({ mode: "open" });

  const style = document.createElement("style");
  style.textContent = guideStyles;
  shadow.appendChild(style);

  const container = document.createElement("div");
  shadow.appendChild(container);

  createApp(GuideApp).mount(container);
}
