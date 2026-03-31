import { createI18n } from 'vue-i18n'
import en from './en.json'
import ru from './ru.json'
import zh from './zh.json'

const savedLocale = localStorage.getItem('mirofish-locale') || 'en'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: { en, ru, zh }
})

export default i18n
