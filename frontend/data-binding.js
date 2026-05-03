/**
 * Data Binding Helpers for CareLoop Frontend
 * Provides functions to update DOM elements with API data
 */

const DataBinding = {
  
  /**
   * Date & Time Utilities
   */
  formatDate: (isoString) => {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    return `${day}/${month}`;
  },
  
  formatTime: (timeString) => {
    if (!timeString) return 'N/A';
    return timeString.substring(0, 5); // HH:MM
  },
  
  formatRelativeTime: (isoString) => {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'Vừa xong';
    if (diffMins < 60) return `${diffMins} phút trước`;
    if (diffHours < 24) return `${diffHours} giờ trước`;
    return `${diffDays} ngày trước`;
  },
  
  /**
   * Dashboard Page Binding
   */
  
  // Bind patient name to greeting
  bindGreeting: (name) => {
    const greeting = document.querySelector('.greeting-heading');
    if (greeting) greeting.textContent = `Chào bác ${name}!`;
  },
  
  // Bind health metrics to cards
  bindHealthMetrics: (metricsData) => {
    if (!metricsData) return;
    
    // Blood Glucose
    if (metricsData.blood_glucose) {
      const glucoseValue = document.querySelector('.health-cards-grid .glucose .metric-value');
      const glucoseStatus = document.querySelector('.health-cards-grid .glucose .status-text');
      const glucoseCard = document.querySelector('.health-cards-grid .glucose');
      
      if (glucoseValue) glucoseValue.textContent = metricsData.blood_glucose.value;
      if (glucoseStatus) {
        glucoseStatus.textContent = DataBinding.statusToText(metricsData.blood_glucose.status);
      }
      if (glucoseCard) {
        glucoseCard.className = `health-card glucose ${DataBinding.statusToClass(metricsData.blood_glucose.status)}`;
      }
    }
    
    // Blood Pressure
    if (metricsData.blood_pressure) {
      const bpValue = document.querySelector('.health-cards-grid .health-card:not(.glucose) .metric-value');
      const bpStatus = document.querySelector('.health-cards-grid .health-card:not(.glucose) .status-text-gray');
      const bpCard = document.querySelector('.health-cards-grid .health-card:not(.glucose)');
      
      if (bpValue) bpValue.textContent = metricsData.blood_pressure.value;
      if (bpStatus) {
        bpStatus.textContent = DataBinding.statusToText(metricsData.blood_pressure.status);
      }
      if (bpCard) {
        bpCard.className = `health-card ${DataBinding.statusToClass(metricsData.blood_pressure.status)}`;
      }
    }
  },
  
  // Bind next appointment to card
  bindNextAppointment: (appointmentData) => {
    if (!appointmentData) return;
    
    const title = document.querySelector('.appointment-title');
    const date = document.querySelector('.datetime-container .datetime-value');
    const time = document.querySelectorAll('.datetime-container .datetime-value')[1];
    const status = document.querySelector('.status-badge-text');
    const location = document.querySelector('.location-text');
    
    if (title) title.textContent = appointmentData.title || 'N/A';
    if (date) date.textContent = DataBinding.formatDate(appointmentData.date);
    if (time) time.textContent = DataBinding.formatTime(appointmentData.time);
    if (status) status.textContent = DataBinding.appointmentStatusText(appointmentData.status);
    if (location) location.textContent = appointmentData.location || 'TBD';
  },
  
  /**
   * Appointments Page Binding
   */
  
  // Bind clinical summary
  bindClinicalSummary: (summaryData) => {
    if (!summaryData) return;
    
    // Title with date
    const titleSection = document.querySelector('.section-title');
    if (titleSection) {
      const date = DataBinding.formatDate(summaryData.date);
      titleSection.innerHTML = `Tóm tắt sau thăm khám<br>(${date})`;
    }
    
    // Summary title
    const summaryTitle = document.querySelector('.summary-title');
    if (summaryTitle) summaryTitle.textContent = summaryData.clinical_summary || 'N/A';
    
    // Metrics list
    const metricsList = document.querySelector('.summary-list');
    if (metricsList && summaryData.metrics) {
      metricsList.innerHTML = summaryData.metrics
        .map(m => `<li>${m}</li>`)
        .join('');
    }
    
    // Doctor notes
    const doctorNotes = document.querySelector('.summary-details > p');
    if (doctorNotes) doctorNotes.textContent = summaryData.doctor_notes || 'Không có ghi chú';
    
    // Warning (if exists)
    const warningBox = document.querySelector('.summary-warning');
    if (summaryData.warning) {
      if (warningBox) {
        warningBox.style.display = 'flex';
        const warningText = warningBox.querySelector('.warning-text');
        if (warningText) warningText.textContent = summaryData.warning;
      }
    } else {
      if (warningBox) warningBox.style.display = 'none';
    }
    
    // Next steps
    const nextSteps = document.querySelector('.next-steps-content');
    const nextDate = document.querySelector('.next-steps-date');
    if (nextSteps) nextSteps.textContent = summaryData.next_steps || 'Tiếp tục theo dõi';
    if (nextDate) nextDate.textContent = DataBinding.formatDate(summaryData.next_appointment_date);
  },
  
  // Bind metrics history chart
  bindMetricsChart: (historyData) => {
    if (!historyData || historyData.length === 0) return;
    
    const firstSeries = historyData[0];
    const points = firstSeries.points || [];
    
    // Update chart title and value
    const chartTitle = document.querySelector('.chart-title');
    const chartValue = document.querySelector('.chart-main-value');
    const chartUnit = document.querySelector('.chart-unit');
    
    if (chartTitle) chartTitle.textContent = `Xu hướng ${firstSeries.name}`;
    if (points.length > 0) {
      const latestPoint = points[points.length - 1];
      if (chartValue) chartValue.textContent = latestPoint.value;
      if (chartUnit) chartUnit.textContent = firstSeries.unit;
    }
    
    // Render chart bars
    const chartBars = document.querySelector('.chart-bars');
    if (chartBars && points.length > 0) {
      chartBars.innerHTML = points.map((point, index) => `
        <div class="chart-bar-container">
          <div class="chart-bar ${index === points.length - 1 ? 'chart-bar-3' : index === 0 ? 'chart-bar-1' : 'chart-bar-2'}">
            <div class="bar-value ${index === points.length - 1 ? 'bar-value-highlight' : ''}">
              ${point.value}
            </div>
          </div>
          <div class="bar-label ${index === points.length - 1 ? 'bar-label-highlight' : ''}">
            ${index === points.length - 1 ? 'HIỆN TẠI' : `LẦN ${index + 1}`}
          </div>
        </div>
      `).join('');
    }
  },
  
  /**
   * Chatbot Page Binding
   */
  
  // Bind AI suggestions
  bindSuggestions: (suggestionsArray) => {
    if (!suggestionsArray || suggestionsArray.length === 0) return;
    
    const suggestionsList = document.querySelector('.suggestions-list');
    if (suggestionsList) {
      suggestionsList.innerHTML = suggestionsArray
        .map(suggestion => `
          <button class="suggestion-button" onclick="askQuestion('${suggestion}')">
            ${suggestion}
          </button>
        `)
        .join('');
    }
  },
  
  // Add message to chat
  addChatMessage: (text, isAI = true) => {
    const mainContent = document.querySelector('.main-content');
    if (!mainContent) return;
    
    const messageContainer = document.createElement('div');
    messageContainer.className = 'message-container';
    
    if (isAI) {
      messageContainer.innerHTML = `
        <div class="message-avatar">
          <img src="https://www.figma.com/api/mcp/asset/69238e48-18a5-4956-8077-65ff7ca7a8b7" alt="AI">
        </div>
        <div class="message-bubble">
          <p class="message-text">${text}</p>
        </div>
      `;
    } else {
      messageContainer.innerHTML = `
        <div class="message-bubble user-message">
          <p class="message-text">${text}</p>
        </div>
      `;
    }
    
    mainContent.appendChild(messageContainer);
    mainContent.scrollTop = mainContent.scrollHeight;
  },
  
  /**
   * Settings Page Binding
   */
  
  // Bind relatives list
  bindRelativesList: (relativesArray) => {
    if (!relativesArray || relativesArray.length === 0) return;
    
    const cardsGrid = document.querySelector('.cards-grid');
    if (!cardsGrid) return;
    
    // Keep the "Add Relative" and "Privacy" cards, replace only relative cards
    const addCard = cardsGrid.querySelector('.add-relative-card');
    const privacyCard = cardsGrid.querySelector('.privacy-card');
    
    // Remove existing relative cards
    document.querySelectorAll('.relative-card').forEach(card => card.remove());
    
    // Add new relative cards
    relativesArray.forEach(relative => {
      const card = document.createElement('div');
      card.className = 'relative-card';
      card.innerHTML = `
        <div class="relative-header">
          <div class="relative-info">
            <div class="relative-icon-box">
              <div class="relative-icon">
                <img src="https://www.figma.com/api/mcp/asset/0b5a8f8a-f07f-4248-9fca-a9fa43b571cd" alt="Relative">
              </div>
            </div>
            <div class="relative-details">
              <div class="relative-name">${relative.name} (${relative.relationship})</div>
              <div class="relative-phone">${relative.phone}</div>
            </div>
          </div>
          <div class="connection-badge">
            <div class="badge-icon">
              <img src="https://www.figma.com/api/mcp/asset/99414d00-0012-4eae-aad6-dc9165fa7a38" alt="Connected">
            </div>
            <span class="badge-text">Đã kết nối</span>
          </div>
        </div>
        <div class="notification-setting">
          <div class="notification-info">
            <div class="notification-icon">
              <img src="https://www.figma.com/api/mcp/asset/cc6a7925-20cf-43f4-b42f-675ee31d6f76" alt="Notification">
            </div>
            <div class="notification-text">Cho phép thông báo lịch tái khám</div>
          </div>
          <div class="toggle-switch ${!relative.allow_notifications ? 'off' : ''}" 
               onclick="toggleRelativeNotification(${relative.id}, this)">
            <div class="toggle-slider"></div>
          </div>
        </div>
      `;
      
      cardsGrid.insertBefore(card, addCard);
    });
  },
  
  /**
   * Utility Functions
   */
  
  statusToText: (status) => {
    const statusMap = {
      'GOOD': 'Tốt',
      'STABLE': 'Ổn định',
      'HIGH': 'Cao'
    };
    return statusMap[status] || status;
  },
  
  statusToClass: (status) => {
    const classMap = {
      'GOOD': 'good',
      'STABLE': 'stable',
      'HIGH': 'high'
    };
    return classMap[status] || '';
  },
  
  appointmentStatusText: (status) => {
    const statusMap = {
      'Scheduled': 'CẦN XÁC NHẬN',
      'Confirmed': 'ĐÃ XÁC NHẬN',
      'Cancelled': 'ĐÃ HỦY'
    };
    return statusMap[status] || status;
  }
};

// Make DataBinding available globally
if (typeof window !== 'undefined') {
  window.DataBinding = DataBinding;
}
