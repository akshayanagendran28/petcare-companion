/**
 * Global Floating AI Chatbot Controller
 * Connects to Django Chatbot API with AJAX, history persistence, typing animations,
 * and robust markdown formatting.
 */

document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('chatbot-toggle-btn');
  const chatWindow = document.getElementById('chatbot-window');
  const closeBtn = document.getElementById('chatbot-close-btn');
  const clearBtn = document.getElementById('chatbot-clear-btn');
  const sendBtn = document.getElementById('chatbot-send-btn');
  const inputField = document.getElementById('chatbot-input');
  const messagesContainer = document.getElementById('chatbot-messages');

  if (!toggleBtn || !chatWindow) return;

  // Toggle Window Visibility
  toggleBtn.addEventListener('click', () => {
    const isHidden = chatWindow.style.display === 'none' || !chatWindow.style.display;
    chatWindow.style.display = isHidden ? 'flex' : 'none';
    if (isHidden) {
      inputField.focus();
      scrollToBottom();
      loadChatHistory();
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      chatWindow.style.display = 'none';
    });
  }

  // Enhanced Markdown Formatter
  function formatMarkdown(text) {
    if (!text) return '';
    let html = text
      .replace(/^### (.*$)/gim, '<strong class="d-block mt-2 mb-1 text-primary">$1</strong>')
      .replace(/^## (.*$)/gim, '<strong class="d-block mt-2 mb-1">$1</strong>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="btn btn-sm btn-primary-custom text-white fw-bold my-1 me-1 text-decoration-none shadow-sm d-inline-flex align-items-center gap-1"><i class="fa-solid fa-arrow-up-right-from-square me-1"></i> $1</a>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code class="bg-light px-1 rounded text-dark">$1</code>');

    const lines = html.split('\n');
    let inList = false;
    let inNumList = false;
    let formattedLines = [];

    lines.forEach(line => {
      const bulletMatch = line.match(/^(\s*)[-*]\s+(.*)/);
      const numMatch = line.match(/^(\s*)\d+\.\s+(.*)/);

      if (bulletMatch) {
        if (!inList) {
          if (inNumList) { formattedLines.push('</ol>'); inNumList = false; }
          formattedLines.push('<ul class="mb-1 ps-3">');
          inList = true;
        }
        formattedLines.push(`<li class="mb-1">${bulletMatch[2]}</li>`);
      } else if (numMatch) {
        if (!inNumList) {
          if (inList) { formattedLines.push('</ul>'); inList = false; }
          formattedLines.push('<ol class="mb-1 ps-3">');
          inNumList = true;
        }
        formattedLines.push(`<li class="mb-1">${numMatch[2]}</li>`);
      } else {
        if (inList) { formattedLines.push('</ul>'); inList = false; }
        if (inNumList) { formattedLines.push('</ol>'); inNumList = false; }
        formattedLines.push(line);
      }
    });

    if (inList) formattedLines.push('</ul>');
    if (inNumList) formattedLines.push('</ol>');

    return formattedLines.join('<br>').replace(/(<br>\s*){3,}/g, '<br><br>').replace(/<br>(<\/?(?:ul|ol|li|strong|a))/g, '$1').replace(/(<\/(?:ul|ol|strong|a)>)<br>/g, '$1');
  }

  function appendMessage(sender, text, isHtml = false, redirectUrl = null, destination = null) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble chat-bubble-${sender}`;
    let content = isHtml ? text : (sender === 'bot' ? formatMarkdown(text) : text.replace(/\n/g, '<br>'));
    if (redirectUrl) {
      content += `<div class="mt-2 pt-2 border-top border-light-subtle d-flex flex-wrap gap-2 align-items-center">
        <a href="${redirectUrl}" class="btn btn-primary-custom btn-sm fw-bold px-3 py-1 shadow-sm d-inline-flex align-items-center gap-1 text-white">
          <i class="fa-solid fa-compass"></i> Go to ${destination || 'Page'} Now <i class="fa-solid fa-arrow-right ms-1"></i>
        </a>
      </div>`;
    }
    bubble.innerHTML = content;
    messagesContainer.appendChild(bubble);
    scrollToBottom();
    return bubble;
  }

  function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Load History
  let historyLoaded = false;
  function loadChatHistory() {
    if (historyLoaded) return;
    fetch('/chatbot/api/history/')
      .then(res => res.json())
      .then(data => {
        if (data.history && data.history.length > 0) {
          messagesContainer.innerHTML = '';
          data.history.forEach(item => {
            appendMessage('user', item.query);
            appendMessage('bot', item.response);
          });
        }
        historyLoaded = true;
      })
      .catch(err => console.log('Chat history load notice:', err));
  }

  // Clear Chat
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (confirm('Clear chat history?')) {
        fetch('/chatbot/api/clear/', { method: 'POST' })
          .then(() => {
            messagesContainer.innerHTML = `
              <div class="chat-bubble chat-bubble-bot">
                🐾 Hello! I am your <strong>PawPal AI Assistant</strong>. How can I help you with your pet today?
              </div>
            `;
          });
      }
    });
  }

  // Send Message
  function sendMessage() {
    const text = inputField.value.trim();
    if (!text) return;

    appendMessage('user', text);
    inputField.value = '';
    inputField.focus();

    // Show Typing Indicator
    const typingElem = document.createElement('div');
    typingElem.className = 'chat-bubble chat-bubble-bot typing-indicator';
    typingElem.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    messagesContainer.appendChild(typingElem);
    scrollToBottom();

    fetch('/chatbot/api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {
      typingElem.remove();
      if (data.redirect_url) {
        appendMessage('bot', data.response || `🚀 Redirecting to ${data.destination || 'page'}...`, false, data.redirect_url, data.destination);
        window.location.href = data.redirect_url;
        return;
      }
      if (data.response) {
        appendMessage('bot', data.response);
      } else {
        appendMessage('bot', '⚠️ Sorry, I could not process your request at this moment.');
      }
    })
    .catch(() => {
      typingElem.remove();
      appendMessage('bot', '⚠️ Connection error with assistant.');
    });
  }

  if (sendBtn) {
    sendBtn.addEventListener('click', sendMessage);
  }

  if (inputField) {
    inputField.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
      }
    });
  }
});
