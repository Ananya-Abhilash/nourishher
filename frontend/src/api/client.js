import axios from 'axios'

const client = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api' })
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('nourishher_token')
  if (token) config.headers.Authorization = `Token ${token}`
  return config
})
export const apiError = (error) => {
  const data = error.response?.data
  if (typeof data?.detail === 'string') return data.detail
  if (data && typeof data === 'object') {
    const flatten = (value) => Array.isArray(value) ? value.flatMap(flatten) : typeof value === 'object' && value ? Object.values(value).flatMap(flatten) : String(value)
    return flatten(data).join(' ')
  }
  return 'Something went wrong. Please try again.'
}
export default client
