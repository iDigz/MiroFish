<template>
  <Teleport to="body">
    <div v-if="show" class="prompt-overlay" @click.self="$emit('close')">
      <div class="prompt-modal">
        <!-- Header -->
        <div class="modal-header">
          <h2 class="modal-title">{{ $t('settings.title') }}</h2>
          <button class="close-btn" @click="$emit('close')">{{ $t('settings.close') }} ×</button>
        </div>

        <!-- Body -->
        <div class="modal-body">
          <!-- Left sidebar with category tabs -->
          <div class="category-sidebar">
            <button
              v-for="cat in categories"
              :key="cat.id"
              class="category-tab"
              :class="{ active: activeCategory === cat.id }"
              @click="activeCategory = cat.id"
            >
              {{ $t('settings.category_' + cat.id) }}
            </button>
          </div>

          <!-- Right content area with textareas -->
          <div class="prompts-content">
            <div v-if="loading" class="loading-state">Loading...</div>
            <div v-else>
              <div
                v-for="key in activeCategoryKeys"
                :key="key"
                class="prompt-block"
              >
                <label class="prompt-label">{{ key }}</label>
                <textarea
                  v-model="prompts[activeCategory][key]"
                  class="prompt-textarea"
                  rows="8"
                ></textarea>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <div class="notification" v-if="notification">
            <span :class="notificationType">{{ notification }}</span>
          </div>
          <div class="footer-actions">
            <button class="btn-reset" @click="handleReset">{{ $t('settings.reset') }}</button>
            <button class="btn-save" @click="handleSave">{{ $t('settings.save') }}</button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { getPrompts, updatePrompts, resetPrompts } from '../api/prompts'

const { t } = useI18n()

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const categories = [
  { id: 'ontology', keys: ['system'] },
  { id: 'persona', keys: ['system', 'individual', 'group'] },
  { id: 'sim_config', keys: ['time_system', 'time_user', 'event_system', 'event_user', 'agent_system', 'agent_user'] },
  { id: 'report', keys: ['tool_insight_forge', 'tool_panorama_search', 'tool_quick_search', 'tool_interview_agents', 'plan_system', 'section_system', 'chat_system'] },
  { id: 'interview', keys: ['decompose_query', 'select_agents', 'generate_questions', 'generate_summary', 'prompt_prefix'] }
]

const activeCategory = ref('ontology')
const prompts = ref({})
const loading = ref(false)
const notification = ref('')
const notificationType = ref('success')

// Currently visible prompt keys based on selected category
const activeCategoryKeys = computed(() => {
  const cat = categories.find(c => c.id === activeCategory.value)
  return cat ? cat.keys : []
})

// Initialize empty prompt structure
const initEmptyPrompts = () => {
  const data = {}
  for (const cat of categories) {
    data[cat.id] = {}
    for (const key of cat.keys) {
      data[cat.id][key] = ''
    }
  }
  return data
}

// Load prompts from API
const loadPrompts = async () => {
  loading.value = true
  const res = await getPrompts()
  loading.value = false

  if (res.success === false) {
    showNotification(t('settings.error', { error: res.error }), 'error')
    prompts.value = initEmptyPrompts()
    return
  }

  // Merge API response into structured format
  const data = initEmptyPrompts()
  const responseData = res.data || res

  for (const cat of categories) {
    if (responseData[cat.id]) {
      for (const key of cat.keys) {
        if (responseData[cat.id][key] !== undefined) {
          data[cat.id][key] = responseData[cat.id][key]
        }
      }
    }
  }

  prompts.value = data
}

// Save prompts
const handleSave = async () => {
  const res = await updatePrompts(prompts.value)

  if (res.success === false) {
    showNotification(t('settings.error', { error: res.error }), 'error')
    return
  }

  showNotification(t('settings.saved'), 'success')
}

// Reset prompts to defaults
const handleReset = async () => {
  const res = await resetPrompts()

  if (res.success === false) {
    showNotification(t('settings.error', { error: res.error }), 'error')
    return
  }

  showNotification(t('settings.resetDone'), 'success')
  await loadPrompts()
}

// Show a brief notification
const showNotification = (message, type) => {
  notification.value = message
  notificationType.value = type
  setTimeout(() => {
    notification.value = ''
  }, 3000)
}

// Load prompts when modal becomes visible
watch(() => props.show, (newVal) => {
  if (newVal) {
    loadPrompts()
  }
})
</script>

<style scoped>
.prompt-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.prompt-modal {
  width: 90vw;
  height: 85vh;
  background: #fff;
  display: flex;
  flex-direction: column;
  font-family: 'JetBrains Mono', monospace;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #e5e5e5;
  background: #000;
  color: #fff;
}

.modal-title {
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 1px;
  margin: 0;
}

.close-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.6);
  padding: 4px 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  color: #fff;
  border-color: #FF4500;
}

.modal-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.category-sidebar {
  width: 200px;
  min-width: 200px;
  border-right: 1px solid #e5e5e5;
  display: flex;
  flex-direction: column;
  padding: 8px 0;
  background: #fafafa;
}

.category-tab {
  background: transparent;
  border: none;
  text-align: left;
  padding: 12px 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.category-tab:hover {
  color: #000;
  background: #f0f0f0;
}

.category-tab.active {
  color: #000;
  font-weight: 700;
  border-left-color: #FF4500;
  background: #fff;
}

.prompts-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.loading-state {
  color: #999;
  font-size: 0.85rem;
  padding: 40px;
  text-align: center;
}

.prompt-block {
  margin-bottom: 24px;
}

.prompt-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #FF4500;
  margin-bottom: 8px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.prompt-textarea {
  width: 100%;
  min-height: 200px;
  border: 1px solid #ddd;
  background: #fafafa;
  padding: 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.prompt-textarea:focus {
  border-color: #FF4500;
  background: #fff;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  border-top: 1px solid #e5e5e5;
  background: #fafafa;
}

.notification {
  font-size: 0.8rem;
}

.notification .success {
  color: #22c55e;
}

.notification .error {
  color: #ef4444;
}

.footer-actions {
  display: flex;
  gap: 12px;
  margin-left: auto;
}

.btn-reset {
  background: transparent;
  border: 1px solid #ccc;
  color: #666;
  padding: 8px 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reset:hover {
  border-color: #FF4500;
  color: #FF4500;
}

.btn-save {
  background: #000;
  border: 1px solid #000;
  color: #fff;
  padding: 8px 24px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save:hover {
  background: #FF4500;
  border-color: #FF4500;
}
</style>
