<template>
  <div v-if="rect">
    <div
      v-for="(piece, idx) in maskPieces"
      :key="idx"
      class="mask-piece"
      :style="pieceStyle(piece)"
    ></div>
    <HighlightBox :rect="rect" />
    <GuideTooltip
      :rect="rect"
      :message="message"
      :reason="reason"
      :show-next="showNext"
      @next="emit('next')"
    />
  </div>
</template>

<script setup>
import { computed } from "vue";
import HighlightBox from "./HighlightBox.vue";
import GuideTooltip from "./GuideTooltip.vue";

const emit = defineEmits(["next"]);

const props = defineProps({
  rect: {
    type: Object,
    default: null,
  },
  message: {
    type: String,
    default: "",
  },
  reason: {
    type: String,
    default: "",
  },
  showNext: {
    type: Boolean,
    default: false,
  },
});

const maskPieces = computed(() => {
  if (!props.rect) {
    return [];
  }
  const pad = 10;
  const top = Math.max(props.rect.top - pad, 0);
  const left = Math.max(props.rect.left - pad, 0);
  const right = Math.min(
    props.rect.left + props.rect.width + pad,
    window.innerWidth
  );
  const bottom = Math.min(
    props.rect.top + props.rect.height + pad,
    window.innerHeight
  );
  const pieces = [];
  if (top > 0) {
    pieces.push({ top: 0, left: 0, width: window.innerWidth, height: top });
  }
  if (bottom < window.innerHeight) {
    pieces.push({
      top: bottom,
      left: 0,
      width: window.innerWidth,
      height: window.innerHeight - bottom,
    });
  }
  const middleHeight = Math.max(bottom - top, 0);
  if (left > 0 && middleHeight > 0) {
    pieces.push({ top, left: 0, width: left, height: middleHeight });
  }
  if (right < window.innerWidth && middleHeight > 0) {
    pieces.push({
      top,
      left: right,
      width: window.innerWidth - right,
      height: middleHeight,
    });
  }
  return pieces;
});

const pieceStyle = (piece) => ({
  top: `${piece.top}px`,
  left: `${piece.left}px`,
  width: `${piece.width}px`,
  height: `${piece.height}px`,
});
</script>
