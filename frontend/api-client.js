/**
 * API Client for CareLoop Frontend
 * Provides fetch wrappers for all backend API endpoints
 */

// Configuration
const API_BASE = 'http://localhost:8000/api/v1';
const PATIENT_ID = 1; // Hardcoded for dev; replace with localStorage for production
const TIMEOUT = 10000; // 10 seconds

/**
 * Generic fetch wrapper with error handling and timeout
 */
async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT);
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data.data || data; // Extract data from APIResponse wrapper
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('API request timeout');
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * User API
 */
const userAPI = {
  // GET /users/me - Get current patient info
  getCurrentUser: async () => {
    return fetchAPI(`/users/me?patient_id=${PATIENT_ID}`);
  },
  
  // GET /users/relatives - Get list of relatives
  getRelatives: async () => {
    return fetchAPI(`/users/relatives?patient_id=${PATIENT_ID}`);
  },
  
  // PUT /users/relatives/{id}/notifications - Toggle notification for relative
  toggleNotification: async (relativeId, allowNotifications) => {
    return fetchAPI(`/users/relatives/${relativeId}/notifications`, {
      method: 'PUT',
      body: JSON.stringify({ allow_notifications: allowNotifications })
    });
  }
};

/**
 * Appointment API
 */
const appointmentAPI = {
  // GET /appointments/next - Get next scheduled appointment
  getNextAppointment: async () => {
    return fetchAPI(`/appointments/next?patient_id=${PATIENT_ID}`);
  },
  
  // GET /appointments/last-summary - Get latest clinical summary
  getLastSummary: async () => {
    return fetchAPI(`/appointments/last-summary?patient_id=${PATIENT_ID}`);
  },
  
  // PUT /appointments/{id}/confirm - Confirm appointment
  confirmAppointment: async (appointmentId) => {
    return fetchAPI(`/appointments/${appointmentId}/confirm`, {
      method: 'PUT',
      body: JSON.stringify({ patient_id: PATIENT_ID })
    });
  }
};

/**
 * Metrics API
 */
const metricsAPI = {
  // GET /metrics/latest - Get latest health metrics
  getLatestMetrics: async () => {
    return fetchAPI(`/metrics/latest?patient_id=${PATIENT_ID}`);
  },
  
  // GET /metrics/history - Get historical trend data
  getMetricsHistory: async (days = 90, maxSeries = 4, maxPoints = 8) => {
    const params = new URLSearchParams({
      patient_id: PATIENT_ID,
      days,
      max_series: maxSeries,
      max_points_per_series: maxPoints
    });
    return fetchAPI(`/metrics/history?${params}`);
  }
};

/**
 * AI API
 */
const aiAPI = {
  // GET /ai/suggestions - Get AI suggestion questions
  getSuggestions: async () => {
    return fetchAPI('/ai/suggestions');
  },
  
  // GET /ai/insights - Get AI insight for patient
  getInsights: async () => {
    return fetchAPI(`/ai/insights?patient_id=${PATIENT_ID}`);
  },
  
  // POST /ai/chat - Send chat message to AI
  sendChatMessage: async (message) => {
    return fetchAPI('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ message })
    });
  },
  
  // GET /ai/video-advice - Get personalized video advice
  getVideoAdvice: async () => {
    return fetchAPI(`/ai/video-advice?patient_id=${PATIENT_ID}`);
  }
};

/**
 * Export all API modules
 */
const API = {
  user: userAPI,
  appointment: appointmentAPI,
  metrics: metricsAPI,
  ai: aiAPI,
  
  // Utility to show loading spinner
  showLoading: () => {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) spinner.style.display = 'block';
  },
  
  // Utility to hide loading spinner
  hideLoading: () => {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) spinner.style.display = 'none';
  },
  
  // Utility to show error message
  showError: (message) => {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
      errorDiv.textContent = message;
      errorDiv.style.display = 'block';
      setTimeout(() => {
        errorDiv.style.display = 'none';
      }, 5000);
    } else {
      alert(`Error: ${message}`);
    }
  }
};

// Make API available globally
if (typeof window !== 'undefined') {
  window.API = API;
}
