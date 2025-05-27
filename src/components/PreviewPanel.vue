<template>
    <section class="preview-panel full-height">
        <h2>Preview: <span class="preview-title">{{ preview?.name || 'No file selected' }}</span></h2>
        <div class="preview-box">
            <div v-if="preview && preview.type === 'file'">
                <iframe :src="preview.url" class="preview-iframe" frameborder="0"></iframe>
            </div>
            <div v-else-if="preview && preview.content">
                {{ preview.content }}
            </div>
            <div v-else>
                <p>No preview available.</p>
            </div>
        </div>
    </section>
</template>


<script>
export default {
    name: 'PreviewPanel',
    props: {
        preview: Object
    }
}

</script>

<style scoped>
.preview-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.full-height {
    align-self: stretch;
}

.preview-title {
    word-break: break-word;
    overflow-wrap: break-word;
}

.preview-box {
    background: #f8f9fa;
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 6px;
    line-height: 1.5;
    display: flex;
    flex: 1;
    flex-direction: column;
    max-height: 900px;
    overflow-y: auto;
    overflow-x: auto;
    /* 👈 important for horizontal scroll */
    white-space: pre-wrap;
    word-break: break-word;
    width: 100%;
    /* 👈 force to not overflow parent */
    box-sizing: border-box;
}

.preview-iframe {
  flex: 1;
  width: 100%;
  height: 800px;
  border: none;
}
</style>