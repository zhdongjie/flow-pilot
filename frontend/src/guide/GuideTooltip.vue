<template>
  <div v-if="rect && message" class="tooltip" :style="style">
    <p class="tooltip-title">{{ message }}</p>
    <p v-if="reason" class="tooltip-reason">{{ reason }}</p>
    <button
      v-if="showNext"
      type="button"
      class="tooltip-action"
      @click="emit('next')"
    >
      我已填写，继续
    </button>
  </div>
</template>

<script setup>
import { computed } from "vue";

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

const style = computed(() => {
  if (!props.rect) {
    return {};
  }
  const margin = 12;
  const tooltipWidth = 280;
  const left = Math.min(props.rect.left, window.innerWidth - tooltipWidth - 16);
  const topBelow = props.rect.top + props.rect.height + margin;
  const topAbove = props.rect.top - margin - 80;
  const top = topBelow + 120 > window.innerHeight ? Math.max(topAbove, margin) : topBelow;

  return {
    top: `${top}px`,
    left: `${left}px`,
  };
});
</script>
