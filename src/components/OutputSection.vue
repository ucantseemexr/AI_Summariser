<!-- src/components/OutputSection.vue -->
<template>
  <section class="output-section">
    <button class="generate-button" @click="$emit('generate-summary')">GENERATE SUMMARY</button>
    <div class="summary-box">{{ summary }}</div>
    <div class="output-actions">
      <button @click="$emit('copy-summary')" :disabled="summary === ''">Copy</button>
      <button @click="$emit('download-summary')" :disabled="summary === ''">Download</button>
    </div>
  </section>
</template>

<script>
export default {
  name: 'OutputSection',
  props: {
    summary: {
      type: String,
      required: true
    }
  }
};
</script>

<style scoped>
.output-section {
  margin-top: 2rem;
}

.generate-button {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.75rem;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 1rem;
  box-shadow: 0 2px 6px rgba(0, 123, 255, 0.4);
}

.summary-box {
  border: 1px solid #ccc;
  padding: 1rem;
  margin-bottom: 1rem;
  min-height: 120px;
  background: #fff;
  border-radius: 6px;
}

.output-actions button {
  margin-right: 0.75rem;
  padding: 0.5rem 1rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover:enabled {
  background-color: #007bff;
}

button:disabled {
  background-color: #cccccc;
  color: #666666;
  cursor: not-allowed;
}
</style>