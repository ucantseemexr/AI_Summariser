<template>
    <div class="container">
      <!-- Navbar -->
      <nav class="navbar">
        <div class="logo">AI Summariser</div>
        <ul class="nav-links">
          <li><a href="#">Home</a></li>
          <li><a href="#">Templates</a></li>
          <li><a href="#">API</a></li>
          <li><a href="#">About</a></li>
          <li><a href="#">Login/Signup</a></li>
        </ul>
      </nav>
  
      <!-- Hero Section -->
      <header class="hero">
        <h1>Summarise Smarter. On Your Terms.</h1>
        <p>Upload multiple documents, preview content, and summarise with your own custom templates.</p>
      </header>
  
      <!-- Upload + Settings with Shared Preview Panel -->
      <div class="section-box split-layout">
        <div class="left-column">
  
          <section class="settings-section">
            <h2>Summary Settings Panel</h2>
            <div class="template-options">
              <h3>Choose Template:</h3>
  
              <label>
                <input type="radio" value="use" v-model="templateMode" />
                Use Template:
                <select v-model="selectedTemplate" :disabled="templateMode !== 'use'">
                  <option disabled value="">-- Select Template --</option>
                  <option v-for="template in availableTemplates" :key="template.id" :value="template.id">
                    {{ template.name }}
                  </option>
                </select>
              </label>
              <label>
                <input type="radio" value="custom" v-model="templateMode" />
                Create Custom Template
              </label>
  
              <div v-if="templateMode === 'custom'" class="custom-template-box">
                <h4>Custom Template Builder</h4>
                <div class="template-name">Template Name: <input v-model="customTemplateName" placeholder="Template Name">
                </div>
                <draggable v-model="customSections" group="sections" handle=".drag-handle" item-key="index">
                  <template #item="{ element, index }">
                    <div class="section-block">
                      <div class="section-input-block">
                        <input v-model="element.title" placeholder="Section Title" />
                        <div class="drag-handle">⇅</div>
                      </div>
                      <draggable v-model="element.subsections" handle=".sub-drag-handle" item-key="subIndex">
                        <template #item="{ index: subIndex }">
                          <li class="subsection-row">
                            <input v-model="element.subsections[subIndex]" placeholder="Subsection content" />
                            <button @click="removeSubsection(index, subIndex)">✕</button>
                            <div class="sub-drag-handle">⇅</div>
                          </li>
                        </template>
                      </draggable>
                      <button @click="addSubsection(index)">+ Add Subsection</button>
                      <button @click="removeSection(index)" class="danger">Remove Section</button>
                      <hr />
                    </div>
                  </template>
                </draggable>
                <button @click="addSection">+ Add Section</button>
                <button @click="saveTemplate">💾 Save Template</button>
  
              </div>
            </div>
          </section>
  
          <section class="upload-panel">
            <h2>File Upload Panel</h2>
            <div class="upload-box-wrapper">
              <label class="upload-box" @dragover.prevent @drop.prevent="handleDrop">
                <input type="file" ref="fileInput" multiple @change="handleFileUpload" hidden />
                <div @click="triggerFileUpload">📁 UPLOAD FILES (DRAG OR CLICK)</div>
              </label>
              <ul class="file-list" v-if="uploadedFiles.length > 0">
                <li v-for="(file, index) in uploadedFiles" :key="index" class="file-entry">
                  <div class="file-row">
                    <input type="checkbox" checked />
                    <span class="file-name">{{ file.name }}</span>
                    <button class="preview-button">PREVIEW</button>
                    <button class="delete-button" @click="removeFile(index)">✕</button>
                  </div>
                  <div class="file-divider"></div>
                </li>
              </ul>
            </div>
          </section>
        </div>
  
        <section class="preview-panel full-height">
          <h2>Preview: proposal.docx</h2>
          <div class="preview-box">
            <p>This proposal outlines our strategy for success in the upcoming year.</p>
            <p>1. <strong>Introduction</strong>: Overview of company goals and objectives</p>
            <p>2. <strong>Market Analysis</strong>: Assessment of current market trends.</p>
            <p>3. <strong>Implementation</strong>: Steps to achieve our targets.</p>
          </div>
        </section>
      </div>
  
      <!-- Output Section -->
      <div class="section-box">
        <section class="output-section">
          <button class="generate-button" @click="generateSummary">GENERATE SUMMARY</button>
          <div class="summary-box">{{ summary }}</div>
          <div class="output-actions">
            <button @click="copySummary">Copy</button>
            <button @click="downloadSummary">Download</button>
          </div>
        </section>
      </div>
    </div>
  </template>
  
  <script>
  import draggable from 'vuedraggable/src/vuedraggable';
  
  export default {
    components: { draggable },
    data() {
      return {
        uploadedFiles: [],
        selectedTemplate: null,
        summary: '',
        templateMode: 'choose',
        availableTemplates: [],
        customTemplateName: '',
        customSections: [],
        savedTemplates: []
      };
    },
    mounted() {
      this.fetchTemplates();
    },
    methods: {
      triggerFileUpload() {
        this.$refs.fileInput.click();
      },
      handleFileUpload(event) {
        this.uploadedFiles.push(...Array.from(event.target.files));
      },
      handleDrop(event) {
        const droppedFiles = Array.from(event.dataTransfer.files);
        this.uploadedFiles.push(...droppedFiles);
      },
      removeFile(index) {
        this.uploadedFiles.splice(index, 1);
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
          style: "paragraph", // or "bullet", you can make this dynamic
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
          await this.fetchTemplates(); // call the existing method
        } catch (err) {
          console.error('Error saving template:', err);
          alert('Failed to save template');
        }
      },
  
      async fetchTemplates() {
        try {
          const response = await fetch('http://localhost:5000/api/templates');
          const data = await response.json();
          this.availableTemplates = data;
          console.log("Loaded templates:", data);
        } catch (err) {
          console.error("Failed to fetch templates:", err);
        }
      },
  
      generateSummary() {
        if (this.templateMode === 'custom') {
          this.summary = this.customSections.map(section => {
            const subs = section.subsections.map(s => - ${s}).join('\n');
            return ${section.title}:\n${subs};
          }).join('\n\n');
        } else if (this.templateMode === 'use') {
          const matchedTemplate = this.availableTemplates.find(t => t.id === parseInt(this.selectedTemplate));
          if (matchedTemplate) {
            this.summary = matchedTemplate.sections.map(section => {
              const subs = section.subsections.map(s => - ${s}).join('\n');
              return ${section.title}:\n${subs};
            }).join('\n\n');
          } else if (this.selectedTemplate === 'executive') {
            this.summary = \n- Boost social media engagement\n- Launch new ad campaigns\n- Expect 20% increase in leads;
          } else {
            this.summary = 'This is a paragraph-style summary based on the uploaded content.';
          }
        }
      },
      copySummary() {
        navigator.clipboard.writeText(this.summary).then(() => alert('Copied!'));
      },
      downloadSummary() {
        const blob = new Blob([this.summary], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'summary.txt';
        link.click();
      }
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
  
  .cta-button {
    margin-top: 1rem;
    padding: 0.6rem 1.5rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 123, 255, 0.4);
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
  
  .preview-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .full-height {
    align-self: stretch;
  }
  
  .upload-panel,
  .settings-section {
    width: 100%;
  }
  
  .section-input-block {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  }
  
  .template-name {
    font-size: 15px;
    font-weight: bold;
  }
  
  .drag-handle {
    cursor: move;
    padding: 0.5rem;
    font-weight: bold;
    display: flex;
    flex: 1;
  }
  
  .subsection-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.5rem;
    padding-left: 2rem;
    /* 👈 Indentation to visually nest */
    border-left: 2px solid #e0e0e0;
    /* Optional: add a vertical line */
  }
  
  
  .sub-drag-handle {
    cursor: move;
    font-weight: bold;
    user-select: none;
    display: flex;
    flex: 1;
  }
  
  
  .upload-box-wrapper {
    border: 2px dashed #007bff;
    padding: 1rem;
    border-radius: 12px;
    background: #f0f8ff;
    margin-right: 1rem;
  }
  
  .upload-box {
    padding: 1.5rem;
    text-align: center;
    cursor: pointer;
    font-weight: bold;
  }
  
  .file-list {
    list-style: none;
    padding: 0;
    margin-top: 1rem;
    border: 1px solid #007bff;
    border-radius: 12px;
    overflow: hidden;
  }
  
  .file-entry {
    padding: 0.75rem 1rem;
    background-color: #f8faff;
  }
  
  .file-row {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .file-name {
    flex-grow: 1;
    font-weight: 500;
  }
  
  .file-divider {
    border-top: 1px solid #007bff;
    margin-top: 0.75rem;
  }
  
  .preview-button {
    background: #e0e0e0;
    border: none;
    padding: 0.25rem 0.75rem;
    cursor: pointer;
    border-radius: 4px;
    font-size: 12px;
  }
  
  .delete-button {
    background: #ff4d4f;
    color: white;
    border: none;
    padding: 0.25rem 0.5rem;
    cursor: pointer;
    border-radius: 4px;
  }
  
  
  .preview-box {
    background: #f8f9fa;
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 6px;
    line-height: 1.5;
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .template-options label {
    display: block;
    margin-bottom: 0.75rem;
    font-weight: 500;
  }
  
  .builder-button {
    background: #6c757d;
    color: white;
    border: none;
    padding: 0.4rem 0.75rem;
    cursor: pointer;
    border-radius: 6px;
    margin-top: 0.5rem;
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
  
  .custom-template-box {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .custom-template-box textarea {
    padding: 0.5rem;
    font-family: monospace;
    border: 1px solid #ccc;
    border-radius: 6px;
    resize: vertical;
  }
  
  .placeholder-guide {
    font-size: 0.875rem;
    color: #555;
  }
  </style>