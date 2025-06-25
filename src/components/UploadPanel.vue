<template>
    <section class="upload-panel">
        <h2>File Upload Panel</h2>
        <div class="upload-box-wrapper">
            <label class="upload-box" @dragover.prevent @drop.prevent="handleDrop">
                <input type="file" ref="fileInput" multiple @change="handleFileUpload" hidden />
                <div @click="triggerFileUpload">📁 UPLOAD FILES (DRAG OR CLICK)</div>
            </label>
            <ul class="file-list" v-if="internalFiles.length > 0">
                <li v-for="(file, index) in internalFiles" :key="index" class="file-entry">
                    <div class="file-row">
                        <input type="checkbox" :checked="isSelected(file)" @change="toggleFileSelection(file)" />
                        <span class="file-name">{{ file.originalName }}</span>
                        <button class="preview-button" @click="previewFile(file)">PREVIEW</button>
                        <button class="delete-button" @click="removeFile(index)">✕</button>
                    </div>
                    <div class="file-divider"></div>
                </li>
            </ul>
        </div>
    </section>
</template>

<script>
export default {
    props: {
        uploadedFiles: {
            type: Array,
            required: true
        },
        selectedFiles: {
            type: Array,
            required: true
        }
    },
    emits: ['update:uploadedFiles', 'update:selectedFiles', 'preview-content', 'file-upload'],
    data() {
        return {
            internalFiles: [...this.uploadedFiles],
            internalSelectedFiles: [...this.selectedFiles]
        };
    },
    watch: {
        uploadedFiles(newFiles) {
            this.internalFiles = [...newFiles];
        },
        selectedFiles(newSelected) {
            this.internalSelectedFiles = [...newSelected];
        }
    },
    methods: {
        triggerFileUpload() {
            this.$refs.fileInput.click();
        },
        handleFileUpload(event) {
            const files = Array.from(event.target.files);
            this.$emit('file-upload', files);
        },
        handleDrop(event) {
            const dropped = Array.from(event.dataTransfer.files);
            this.$emit('file-upload', dropped);
        },
        removeFile(index) {
            const removed = this.internalFiles[index];
            this.internalFiles.splice(index, 1);
            this.internalSelectedFiles = this.internalSelectedFiles.filter(
                f => !(f.name === removed.name && f.size === removed.size)
            );

            this.$emit('update:uploadedFiles', [...this.internalFiles]);
            this.$emit('update:selectedFiles', [...this.internalSelectedFiles]);
        },
        previewFile(file) {
            const ext = file.name.split('.').pop().toLowerCase();

            if (['pdf'].includes(ext)) {
                this.$emit('preview-content', {
                    name: file.name,
                    originalName: file.originalName,
                    type: 'file',
                    url: `http://localhost:5000/uploads/${encodeURIComponent(file.name)}`
                });
            } else if (['docx', 'txt'].includes(ext)) {
                this.$emit('preview-content', {
                    name: file.name,
                    originalName: file.originalName,
                    type: 'doc-request'
                });
            } else {
                this.$emit('preview-content', {
                    name: file.name,
                    originalName: file.originalName,
                    content: 'Preview not supported for this file type.'
                });
            }
        },

        isSelected(file) {
            return this.internalSelectedFiles.some(
                f => f.name === file.name && f.size === file.size
            );
        },

        toggleFileSelection(file) {
            console.log(file.name)
            const exists = this.internalSelectedFiles.some(
                f => f.name === file.name && f.size === file.size
            );


            if (exists) {
                this.internalSelectedFiles = this.internalSelectedFiles.filter(
                    f => !(f.name === file.name && f.size === file.size)
                );
            } else {
                this.internalSelectedFiles.push(file);
            }

            this.$emit('update:selectedFiles', this.internalSelectedFiles);
            console.log(this.internalSelectedFiles)
        },
    }
};
</script>


<style scoped>
.upload-panel {
    width: 100%;
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
    margin-top: 0.5rem;
    border: 1px solid #007bff;
    border-radius: 12px;
    overflow: hidden;
    max-height: 200px;
    overflow-y: auto;
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
</style>