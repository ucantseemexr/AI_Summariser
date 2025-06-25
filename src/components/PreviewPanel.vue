<template>
    <section class="preview-panel full-height">
        <h2>Preview: <span class="preview-title">{{ preview?.name || 'No file selected' }}</span></h2>
        <div class="preview-box">
            <div v-if="preview && preview.type === 'file'">
                <iframe :src="preview.url" class="preview-iframe" frameborder="0"></iframe>
            </div>
            <div v-else-if="preview && preview.content">
                <div v-for="(block, index) in preview.content" :key="index" class="block-item">
                    <p v-if="block.type === 'paragraph'">{{ block.text }}</p>

                    <table v-else-if="block.type === 'table'" class="preview-table">
                        <thead>
                            <tr>
                                <th v-for="(cell, i) in block.rows[0]" :key="i">{{ cell }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(row, rowIndex) in block.rows.slice(1)" :key="rowIndex">
                                <td v-for="(cell, i) in row" :key="i">{{ cell }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
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

.block-item {
  margin-bottom: 1rem;
}

.preview-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}

.preview-table th,
.preview-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
  background-color: #fff;
}

.preview-table th {
  background-color: #e9ecef;
  font-weight: bold;
}
</style>