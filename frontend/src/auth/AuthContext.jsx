import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
} from 'react'
import api from '../api/client.js'

const AuthContext = createContext(null)
const STORAGE_KEY = 'phishing_admin_token'

/** Decode a JWT payload (display + expiry only; the backend verifies signature). */
function decodeJwt(token) {
  try {
    const base64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    const json = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(json)
  } catch {
    return null
  }
}

function isExpired(payload) {
  return payload?.exp ? payload.exp * 1000 < Date.now() : true
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null)
  const [user, setUser] = useState(null)

  // Restore a still-valid token from a previous session.
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      const payload = decodeJwt(stored)
      if (payload && !isExpired(payload)) {
        setToken(stored)
        setUser(payload)
      } else {
        localStorage.removeItem(STORAGE_KEY)
      }
    }
  }, [])

  const login = useCallback(async (username, password) => {
    const { data } = await api.post('/api/login', { username, password })
    const t = data.access_token
    localStorage.setItem(STORAGE_KEY, t)
    setToken(t)
    setUser(decodeJwt(t))
    return data
  }, [])

  const logout = useCallback(() => {
    setToken(null)
    setUser(null)
    localStorage.removeItem(STORAGE_KEY)
  }, [])

  const value = {
    token,
    user,
    login,
    logout,
    isAuthenticated: Boolean(token && user && !isExpired(user)),
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  return useContext(AuthContext)
}
