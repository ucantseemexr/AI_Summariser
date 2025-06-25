<!-- src/components/OutputSection.vue -->
<template>
  <section class="output-section">
    <div class="overlay-wrapper">

      <!-- overlay when generating -->
      <div v-if="isGenerating" class="overlay">
        <div class="overlay-text">Generating summary...<br>Please wait.</div>
      </div>

      <div :class="{ 'blurred': isGenerating }">
        <button class="generate-button" @click="triggerSummaryGeneration" :disabled="isGenerating || adjustingSection">
          GENERATE SUMMARY
        </button>


        <div v-if="Object.keys(summaryBySections).length > 0" class="summary-card-wrapper">
          <div v-for="section in sectionOrder" :key="section.title" class="summary-card-wrapper">
            <div :class="['summary-card', { 'section-blurred': adjustingSection === section.title }]">
              <div class="section-header">{{ section.title }}</div>

              <div v-if="pendingAdjustments[section.title]">
                <div class="summary-comparison">
                  <div class="summary-original">
                    <strong>Original:</strong>
                    <div class="summary-text">{{ summaryBySections[section.title] }}</div>
                    <button @click="keepVersion(section.title, 'original')">Keep Original</button>
                  </div>
                  <div class="summary-updated">
                    <strong>Updated:</strong>
                    <div class="summary-text">{{ pendingAdjustments[section.title] }}</div>
                    <button @click="keepVersion(section.title, 'updated')">Keep Updated</button>
                  </div>
                </div>
              </div>
              <div v-else>
                <div class="summary-text">{{ summaryBySections[section.title] || "No summary generated yet." }}</div>
              </div>

              <div v-if="editingSection === section.title">
                <textarea v-model="adjustments[section.title]" class="adjustment-input"
                  placeholder="Enter adjustment instruction for this section..." />
                <button @click="submitAdjustment(section.title)" :disabled="adjustingSection">Submit</button>
                <button @click="cancelEdit(section.title)" :disabled="adjustingSection">Cancel</button>
              </div>
              <div v-else>
                <button @click="startEdit(section.title)"
                  :disabled="!summaryBySections[section.title] || adjustingSection">Regenerate
                  Section</button>
              </div>
            </div>

            <div v-if="adjustingSection === section.title" class="section-overlay">
              <div class="section-overlay-text">Adjusting summary...<br>Please wait.</div>
            </div>
          </div>


        </div>

        <div v-else class="summary-box">No summary generated yet.</div>
      </div>
      <div class="output-actions">
        <button @click="$emit('copy-summary')" :disabled="!hasSummary || adjustingSection || isGenerating">
          Copy
        </button>
        <button @click="$emit('download-summary')" :disabled="!hasSummary || adjustingSection || isGenerating">
          Download
        </button>
      </div>
    </div>


  </section>
</template>

<script>
export default {
  name: 'OutputSection',
  props: {
    summaryBySections: {
      type: Object,
      required: true
    },
    sectionOrder: {
      type: Array,
      required: true
    },
  },
  data() {
    return {
      adjustments: {},
      editingSection: null,
      pendingAdjustments: {},  // holds updated summaries not yet accepted
      isGenerating: false,
      adjustingSection: null,
    };
  },
  computed: {
    hasSummary() {
      return Object.keys(this.summaryBySections).length > 0;
    }
  },
  methods: {
    startEdit(section) {
      this.adjustments = {}
      this.editingSection = section;
      console.log(this.editingSection)
      console.log(this.adjustments[section])
    },
    cancelEdit(section) {
      this.editingSection = null;
      this.adjustments[section] = "";
    },
    submitAdjustment(section) {
      console.log(this.editingSection)
      console.log(this.adjustments[section])
      this.adjustingSection = section;
      const instruction = this.adjustments[section] || '';
      this.$emit('regenerate-section', {
        section,
        instruction,
        callback: (revised) => {
          this.pendingAdjustments[section] = revised;
          this.editingSection = null;
          this.adjustments[section] = '';
          this.adjustingSection = null;
        }
      });
    },
    keepVersion(section, version) {
      if (version === 'updated') {
        this.$emit('update-section-summary', {
          section,
          summary: this.pendingAdjustments[section]
        });
      }
      delete this.pendingAdjustments[section];
    },
    triggerSummaryGeneration() {
      this.isGenerating = true;
      this.$emit('generate-summary', () => {
        this.isGenerating = false;
      });
    }
  }
};
</script>

<style scoped>
.output-section {
  margin-top: 2rem;
}

.overlay-wrapper {
  position: relative;
}

/* overlay with centered message */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.overlay-text {
  font-size: 1.25rem;
  font-weight: bold;
  color: #333;
}

.generate-button {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.75rem;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 6px rgba(0, 123, 255, 0.4);
}

/* blur effect */
.blurred {
  filter: blur(2px);
  pointer-events: none;
  user-select: none;
  opacity: 0.5;
}

.summary-card-wrapper {
  position: relative;
}

.summary-card {
  border: 1px solid #ccc;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  background-color: #fdfdfd;
}

.section-blurred {
  position: relative;
  filter: blur(2px);
  opacity: 0.5;
  pointer-events: none;
  user-select: none;
}

.section-overlay {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  text-align: center;
}

.section-overlay-text {
  font-size: 1rem;
  font-weight: bold;
  color: #333;
  line-height: 1.5;
  text-align: center;
  pointer-events: none;
}

.section-header {
  margin-top: 0;
  font-size: 1.1rem;
  color: #333;
  font-weight: bold;
}

.summary-comparison {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
}

.summary-original,
.summary-updated {
  flex: 1;
  border: 1px solid #ccc;
  padding: 1rem;
  border-radius: 6px;
  background: #f9f9f9;
}

.summary-original {
  background-color: #f2f2f2;
}

.summary-updated {
  background-color: #e6f7ff;
}

.summary-text {
  white-space: pre-wrap;
  margin-bottom: 0.5rem;
}

.adjustment-input {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #bbb;
  margin-bottom: 0.5rem;
}

.summary-box {
  padding: 1rem;
  background: #f9f9f9;
  border: 1px dashed #aaa;
  text-align: center;
  color: #555;
}

.output-actions button {
  margin-right: 0.75rem;
  padding: 0.5rem 1rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 0.5rem;
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