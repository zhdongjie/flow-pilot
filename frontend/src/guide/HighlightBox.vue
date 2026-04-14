<template>
  <div v-if="rect" class="highlight-box" :style="style"></div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  rect: {
    type: Object,
    default: null,
  },
});

const style = computed(() => {
  if (!props.rect) {
    return {};
  }
  const padding = 6;
  return {
    top: `${props.rect.top - padding}px`,
    left: `${props.rect.left - padding}px`,
    width: `${props.rect.width + padding * 2}px`,
    height: `${props.rect.height + padding * 2}px`,
  };
});
</script>
