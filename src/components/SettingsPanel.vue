<template>
    <section class="settings-section">
        <h2>Summary Settings Panel</h2>
        <div class="template-options">
            <h3>Choose Template:</h3>

            <label>
                <input type="radio" value="use" :checked="templateMode === 'use'"
                    @change="$emit('update:templateMode', 'use')" />
                Use Template:
                <select :value="selectedTemplateId" @change="$emit('update:selectedTemplateId', Number($event.target.value))"
                    :disabled="templateMode !== 'use'">
                    <option disabled value="">-- Select Template --</option>
                    <option v-for="template in availableTemplates" :key="template.id" :value="template.id">
                        {{ template.name }}
                    </option>
                </select>
            </label>

            <label>
                <input type="radio" value="custom" :checked="templateMode === 'custom'"
                    @change="$emit('update:templateMode', 'custom')" />
                Create Custom Template
            </label>

            <div v-if="templateMode === 'custom'" class="custom-template-box">
                <h4>Custom Template Builder</h4>
                <div class="template-name">
                    Template Name:
                    <input :value="customTemplateName" @input="$emit('update:customTemplateName', $event.target.value)"
                        placeholder="Template Name" />
                </div>
                <div class = "section-blocks">
                    <draggable :model-value="customSections" @update:modelValue="$emit('update:customSections', $event)"
                        group="sections" handle=".drag-handle" item-key="index">
                        <template #item="{ element, index }">
                            <div class="section-block">
                                <div class="section-input-block">
                                    <input v-model="element.title" placeholder="Section Title" />
                                    <div class="drag-handle">⇅</div>
                                </div>
                                <draggable v-model="element.subsections" handle=".sub-drag-handle" item-key="subIndex">
                                    <template #item="{ index: subIndex }">
                                        <li class="subsection-row">
                                            <input v-model="element.subsections[subIndex]"
                                                placeholder="Subsection content" />
                                            <button @click="$emit('removeSubsection', index, subIndex)">✕</button>
                                            <div class="sub-drag-handle">⇅</div>
                                        </li>
                                    </template>
                                </draggable>
                                <button @click="$emit('addSubsection', index)">+ Add Subsection</button>
                                <button @click="$emit('removeSection', index)">
                                    Remove Section
                                </button>
                                <hr />
                            </div>
                        </template>
                    </draggable>
                </div>

                <button @click="$emit('addSection')">+ Add Section</button>
                <button @click="$emit('saveTemplate')">💾 Save Template</button>
            </div>
        </div>
    </section>
</template>

<script>
import draggable from 'vuedraggable/src/vuedraggable';

export default {
    name: 'SettingsPanel',
    components: { draggable },
    props: {
        templateMode: String,
        selectedTemplate: Object,
        selectedTemplateId: Number,
        availableTemplates: Array,
        customTemplateName: String,
        customSections: Array,
    },
};
</script>

<style scoped>
.settings-section {
    width: 100%;
}

.template-options label {
    display: block;
    margin-bottom: 0.75rem;
    font-weight: 500;
}

.template-name {
    font-size: 15px;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.custom-template-box {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.section-blocks {
    max-height: 200px;
    overflow-y: auto;
}

.section-block {
    border: 1px solid #e0e0e0;
    padding: 0.5rem;
    border-radius: 6px;
    background-color: #fafafa;
    margin-bottom: 0.5rem;
}

.section-input-block {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.5rem;
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
    border-left: 2px solid #e0e0e0;
}

.sub-drag-handle {
    cursor: move;
    font-weight: bold;
    user-select: none;
    display: flex;
    flex: 1;
}

.danger {
    background: #ff4d4f;
    color: white;
    border: none;
    padding: 0.4rem 0.75rem;
    cursor: pointer;
    border-radius: 6px;
    margin-top: 0.5rem;
}
</style>