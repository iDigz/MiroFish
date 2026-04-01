import service from './index'

/**
 * Get all current prompt settings
 */
export const getPrompts = async () => {
  try {
    return await service.get('/api/prompts')
  } catch (err) {
    return { success: false, error: err.message }
  }
}

/**
 * Update prompt settings
 * @param {Object} data - prompt data keyed by category
 */
export const updatePrompts = async (data) => {
  try {
    return await service.put('/api/prompts', data)
  } catch (err) {
    return { success: false, error: err.message }
  }
}

/**
 * Reset all prompts to default values
 */
export const resetPrompts = async () => {
  try {
    return await service.post('/api/prompts/reset')
  } catch (err) {
    return { success: false, error: err.message }
  }
}
