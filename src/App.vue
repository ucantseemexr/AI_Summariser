<template>
  <div class="container">
    <NavbarComponent />
    <HeroComponent />

    <div class="section-box split-layout">
      <div class="left-column">
        <SettingsPanel :templateMode="templateMode" :selectedTemplateId="selectedTemplateId"
          :selectedTemplate="selectedTemplate" :availableTemplates="availableTemplates"
          :customTemplateName="customTemplateName" :customSections="customSections"
          @update:templateMode="templateMode = $event" @update:selectedTemplateId="selectedTemplateId = $event"
          @update:customTemplateName="customTemplateName = $event" @update:customSections="customSections = $event"
          @addSection="addSection" @removeSection="removeSection" @addSubsection="addSubsection"
          @removeSubsection="removeSubsection" @saveTemplate="saveTemplate" />

        <UploadPanel :uploaded-files="uploadedFiles" :selected-files="selectedFiles"
          @update:uploadedFiles="uploadedFiles = $event" @update:selectedFiles="selectedFiles = $event"
          @preview-content="handlePreview" @file-upload="handleFileUpload" />

      </div>

      <PreviewPanel :preview="previewFile" />
    </div>

    <div class="section-box">
      <OutputSection :summaryBySections="summaryBySections"
        :sectionOrder="templateMode === 'custom' ? customSections : selectedTemplate?.structure"
        @update:summary="summary = $event" @update-section-summary="updateSectionSummary"
        @generate-summary="generateSummary" @regenerate-section="handleSectionRegenerate" />
      <StreamOutputSection 
        :selectedFiles="selectedFiles" :sectionOrder="templateMode === 'custom' ? customSections : selectedTemplate?.structure" />
      </div>
  </div>
</template>

<script>
import NavbarComponent from './components/NavbarComponent.vue';
import HeroComponent from './components/HeroComponent.vue';
import SettingsPanel from './components/SettingsPanel.vue';
import UploadPanel from './components/UploadPanel.vue';
import PreviewPanel from './components/PreviewPanel.vue';
import StreamOutputSection from './components/StreamOutputSection.vue';
import OutputSection from './components/OutputSection.vue';

export default {
  components: {
    NavbarComponent,
    HeroComponent,
    SettingsPanel,
    UploadPanel,
    PreviewPanel,
    StreamOutputSection,
    OutputSection
  },
  data() {
    return {
      uploadedFiles: [],
      selectedFiles: [],
      previewFile: null,
      selectedTemplateId: null,
      selectedTemplate: null,
      templateMode: 'choose',
      customTemplateName: '',
      customSections: [],
      availableTemplates: [],
      summary: '',
      summaryBySections: {},
    };
  },
  mounted() {
    this.fetchTemplates();
  },
  watch: {
    selectedTemplateId(newId) {
      this.selectedTemplate = this.availableTemplates.find(t => t.id === newId) || null;
    }
  },
  methods: {
    async fetchTemplates() {
      try {
        const response = await fetch('http://localhost:5000/api/templates');
        const data = await response.json();
        this.availableTemplates = data;
        this.selectedTemplateId = null;
        console.log("Loaded templates:", data);
      } catch (err) {
        console.error("Failed to fetch templates:", err);
      }
    },

    addSection() {
      this.customSections.push({ title: '', subsections: [] });
    },

    removeSection(index) {
      this.customSections.splice(index, 1);
    },

    addSubsection(sectionIndex) {
      this.customSections[sectionIndex].subsections.push('');
    },

    removeSubsection(sectionIndex, subIndex) {
      this.customSections[sectionIndex].subsections.splice(subIndex, 1);
    },

    async saveTemplate() {
      if (!this.customTemplateName.trim()) {
        alert('Please enter a template name before saving.');
        return;
      }

      const payload = {
        templateName: this.customTemplateName,
        style: "paragraph", // You can update this dynamically in the future if needed
        sections: this.customSections
      };

      try {
        const response = await fetch('http://localhost:5000/api/templates', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await response.json();
        alert(data.message);
        await this.fetchTemplates(); // Refresh templates after saving
      } catch (err) {
        console.error('Error saving template:', err);
        alert('Failed to save template');
      }
    },

    handlePreview(fileMeta) {
      if (fileMeta.content) {
        this.previewFile = fileMeta;
        return;
      }

      const ext = fileMeta.name.split('.').pop().toLowerCase();

      if (ext === 'pdf') {
        this.previewFile = {
          name: fileMeta.originalName,
          type: 'file',
          url: `http://localhost:5000/uploads/${encodeURIComponent(fileMeta.name)}`,
        };
      } else if (ext === 'docx' || ext === 'txt') {
        fetch(`http://localhost:5000/api/preview/${encodeURIComponent(fileMeta.name)}`)
          .then((res) => res.json())
          .then((data) => {
            this.previewFile = {
              name: fileMeta.originalName,
              content: data.content,
            };
          })
          .catch(() => {
            this.previewFile = {
              name: fileMeta.name,
              content: 'Failed to preview file.',
            };
          });
      } else {
        this.previewFile = {
          name: fileMeta.name,
          content: 'Unsupported file type for preview.',
        };
      }
    },


    async handleFileUpload(files) {
      for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);

        try {
          const res = await fetch('http://localhost:5000/api/upload', {
            method: 'POST',
            body: formData
          });

          if (!res.ok) {
            const errorMsg = await res.text(); // Try to capture backend error response
            throw new Error(`Upload failed: ${res.status} ${res.statusText} - ${errorMsg}`);
          }

          const result = await res.json();
          console.log('File uploaded to server:', result);

          const newFile = {
            originalName: file.name,
            name: result.filename
          };

          this.uploadedFiles = [...this.uploadedFiles, newFile];
          this.selectedFiles = [...this.selectedFiles, newFile]; // Automatically select uploaded files
        } catch (err) {
          console.error('File upload failed:', err.message || err);
          alert(`Error uploading "${file.name}": ${err.message}`);
        }
      }
    },

    async generateSummary(done) {
      console.log(this.selectedTemplate)
      console.log(this.selectedFiles)

      const CombinedfileContent = [];
      for (const file of this.selectedFiles) {

        try {
          const res = await fetch(`http://localhost:5000/api/preview/${encodeURIComponent(file.name)}`);
          const data = await res.json();
          if (data.content) {
            CombinedfileContent.push(...data.content);
          }
        } catch (err) {
          console.error(`Error reading file ${file.name}:`, err);
        }
      }
      console.log(CombinedfileContent)
      const payload = {
        text: CombinedfileContent,
        sections: this.templateMode === 'custom' ? this.customSections : this.selectedTemplate.structure
      };

      try {
        const res = await fetch('http://localhost:5000/api/summarise_FAISS', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const result = await res.json();
        this.summaryBySections = result
      } catch (err) {
        console.error('Failed to generate summary:', err);
        alert('Failed to generate summary.');
      } finally {
        done(); // inform OutputSection that it's done
      }
    },


    async handleSectionRegenerate({ section, instruction, callback }) {
      const CombinedfileContent = [];

      for (const file of this.selectedFiles) {
        try {
          const res = await fetch(`http://localhost:5000/api/preview/${encodeURIComponent(file.name)}`);
          const data = await res.json();
          if (data.content) {
            CombinedfileContent.push(...data.content);
          }
        } catch (err) {
          console.error(`Failed to read ${file.name}:`, err);
        }
      }
      const payload = {
        text: CombinedfileContent,
        sections: [
          {
            title: section,
            instruction: instruction,
            subsections: this.selectedTemplate.structure.find(t => t['title'] === section)['subsections'],
          }
        ],
        originalSummaries: {
          [section]: this.summaryBySections[section]
        },
      };

      try {
        const res = await fetch('http://localhost:5000/api/adjust_summary', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (callback) {
          callback(data.revised_summary.trim());
        }
      } catch (err) {
        console.error(`Failed to regenerate summary for ${section}:`, err);
        alert(`Error updating section: ${section}`);
      }
    },

    updateSectionSummary({ section, summary }) {
      this.summaryBySections[section] = summary

    },

  }
};
</script>


<style scoped>
.container {
  font-family: 'Segoe UI', sans-serif;
  color: #1a1a1a;
  background-color: #fff;
  padding: 1.5rem;
  max-width: 1200px;
  margin: auto;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.75rem;
  margin-bottom: 1.5rem;
}

.logo {
  font-weight: bold;
  font-size: 1.25rem;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 1.25rem;
}

.nav-links a {
  text-decoration: none;
  color: #007bff;
}

.hero {
  text-align: center;
  margin-bottom: 2rem;
}

.section-box {
  border: 1px solid #ccc;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  background: #fefefe;
}

.split-layout {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  flex-direction: row;
}

.left-column {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
