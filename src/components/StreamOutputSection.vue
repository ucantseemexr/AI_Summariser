<template>
    <section class="output-section">
        <div class="overlay-wrapper">

            <div v-if="isGenerating" class="overlay">
                <div class="overlay-text">Streaming summary...<br>Please wait.</div>
            </div>

            <div :class="{ 'blurred': isGenerating }">
                <button class="generate-button" @click="startStreamingSummary" :disabled="isGenerating">
                    STREAM SUMMARY
                </button>

                <div v-if="sectionOrder?.length > 0 && streamedSummaries[sectionOrder[0].title]?.length > 0" class="summary-card-wrapper">
                    <template v-for="section in sectionOrder" :key="section.title">
                        <div v-if="streamedSummaries[section.title]?.length > 0" class="summary-card">
                            <div class="section-header">{{ section.title }}</div>
                            <div class="summary-text">
                                <pre
                                    style="white-space: pre-wrap;">{{ streamedSummaries[section.title]?.join('') }}</pre>
                            </div>
                        </div>
                    </template>
                </div>

                <div v-else class="summary-box">No summary generated yet.</div>
            </div>

            <div class="output-actions">
                <button @click="copyStreamedText" :disabled="isGenerating || !hasStreamed">
                    Copy
                </button>
                <button @click="$emit('download-streamed', downloadText)" :disabled="isGenerating || !hasStreamed">
                    Download
                </button>
            </div>

        </div>
    </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
    sectionOrder: {
        type: Array,
        required: true
    },
    selectedFiles: {
        type: Array,
        required: true
    }
})

const isGenerating = ref(false)
const streamedSummaries = ref({})

const hasStreamed = computed(() => {
    return Object.values(streamedSummaries.value).some(arr => arr.length > 0)
})

const downloadText = computed(() => {
    return props.sectionOrder.map(section => {
        const lines = streamedSummaries.value[section.title] || []
        return `${section.title}\n${lines.join(' ')}`
    }).join('\n\n')
})

function copyStreamedText() {
    navigator.clipboard.writeText(downloadText.value)
}

async function startStreamingSummary() {
    isGenerating.value = true
    streamedSummaries.value = {}

    for (const section of props.sectionOrder) {
        streamedSummaries.value[section.title] = []
        await streamSection(section)
    }


}

async function streamSection(section) {
    const CombinedfileContent = [];
    for (const file of props.selectedFiles) {

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
        sections: [section]
    };

    const response = await fetch('http://localhost:5000/stream-summary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload )
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    //let buffer = ''

    // eslint-disable-next-line no-constant-condition
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        //buffer += chunk;
        console.log(chunk)

        // Push the whole new chunk to preserve formatting (e.g. \n, markdown)
        streamedSummaries.value[section.title].push(chunk);
        isGenerating.value = false
    }

}
</script>

<style scoped>
.output-section {
    margin-top: 2rem;
}

.overlay-wrapper {
    position: relative;
}

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

.section-header {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.summary-text p {
    margin-bottom: 0.75rem;
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
