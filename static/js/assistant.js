/* ===== AI Assistant - Interaction Logic ===== */

(() => {
  // Feature flag from Django template
  const enabled = window.ASSISTANT_ENABLED || false;

  // DOM Elements
  const trigger = document.getElementById('assistant-btn');
  const modal = document.getElementById('assistant-modal');
  const closeBtn = document.getElementById('assistant-close');
  const body = document.getElementById('assistant-body');
  const input = document.getElementById('assistant-input');
  const sendBtn = document.getElementById('assistant-send');
  const typingIndicator = document.getElementById('assistant-typing');

  // Conversation history
  const history = [];

  // Hide trigger if assistant is disabled
  if (!enabled) {
    trigger.style.display = 'none';
    return;
  }

  /* ===== Modal Toggle ===== */
  function openModal() {
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    input.focus();
    // Prevent body scroll on mobile
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
    // Restore body scroll
    document.body.style.overflow = '';
  }

  // Event listeners for open/close
  trigger.addEventListener('click', openModal);
  closeBtn.addEventListener('click', closeModal);

  // Close on backdrop click
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });

  /* ===== HTML Sanitization ===== */
  function sanitizeHTML(html) {
    // Create a temporary div to parse HTML
    const temp = document.createElement('div');
    temp.innerHTML = html;

    // Remove dangerous tags
    const dangerousTags = ['script', 'iframe', 'object', 'embed', 'style'];
    dangerousTags.forEach(tag => {
      const elements = temp.getElementsByTagName(tag);
      while (elements.length > 0) {
        elements[0].remove();
      }
    });

    // Remove dangerous attributes
    const allElements = temp.getElementsByTagName('*');
    for (let i = 0; i < allElements.length; i++) {
      const element = allElements[i];
      const attrs = element.attributes;
      for (let j = attrs.length - 1; j >= 0; j--) {
        const attrName = attrs[j].name.toLowerCase();
        if (attrName.startsWith('on') || attrName === 'style') {
          element.removeAttribute(attrs[j].name);
        }
      }
    }

    // Only allow internal links (starting with /)
    const links = temp.getElementsByTagName('a');
    for (let i = 0; i < links.length; i++) {
      const href = links[i].getAttribute('href');
      if (href && !href.startsWith('/')) {
        links[i].removeAttribute('href');
      }
    }

    return temp.innerHTML;
  }

  /* ===== Message Rendering ===== */
  function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `assistant-message assistant-message--${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'assistant-avatar';
    avatar.innerHTML = role === 'ai'
      ? '<i class="bi bi-chat-text"></i>'
      : '<i class="bi bi-person-fill"></i>';

    const bubble = document.createElement('div');
    bubble.className = 'assistant-bubble';

    // Sanitize AI messages that may contain HTML
    if (role === 'ai') {
      bubble.innerHTML = sanitizeHTML(content);
    } else {
      // User messages are plain text
      bubble.textContent = content;
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    body.appendChild(messageDiv);

    // Scroll to bottom smoothly
    body.scrollTo({
      top: body.scrollHeight,
      behavior: 'smooth'
    });
  }

  /* ===== Typing Indicator ===== */
  function showTyping() {
    typingIndicator.style.display = 'flex';
    body.scrollTo({
      top: body.scrollHeight,
      behavior: 'smooth'
    });
  }

  function hideTyping() {
    typingIndicator.style.display = 'none';
  }

  /* ===== Send Message ===== */
  async function sendMessage() {
    const text = input.value.trim();

    if (!text) return;

    // Clear input and disable send button
    input.value = '';
    sendBtn.disabled = true;

    // Add user message to UI
    addMessage('user', text);

    // Append system prompt guidance for internal links
    const enhancedMessage = text + '\n\n[System: You may include internal links using normal HTML anchor tags. Only link to URLs starting with \'/\'. Allowed tags: <a>, <p>, <ul>, <li>, <strong>, <em>]';

    // Add to history (with enhanced message)
    history.push({ role: 'user', content: enhancedMessage });

    // Show typing indicator
    showTyping();

    try {
      // Call backend API
      const response = await fetch('/api/assist/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: enhancedMessage,
          history: history
        })
      });

      const data = await response.json();
      const reply = data.reply || 'Sorry—please try again or use the contact form.';

      // Hide typing indicator
      hideTyping();

      // Add assistant message to UI
      addMessage('ai', reply);

      // Add to history
      history.push({ role: 'assistant', content: reply });

    } catch (error) {
      console.error('Assistant error:', error);

      // Hide typing indicator
      hideTyping();

      // Show error message
      addMessage('ai', 'Sorry—something went wrong. Please try again or use the contact form.');
    } finally {
      // Re-enable send button
      sendBtn.disabled = false;
      input.focus();
    }
  }

  /* ===== Event Listeners ===== */
  sendBtn.addEventListener('click', sendMessage);

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Prevent enter from submitting if in a form context
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
    }
  });

  /* ===== Suggested Questions ===== */
  const suggestionBtns = document.querySelectorAll('.assistant-suggestion-btn');

  suggestionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const question = btn.getAttribute('data-question');
      if (question) {
        // Fill input and send
        input.value = question;
        sendMessage();

        // Hide suggestions after first use (optional)
        const suggestionsContainer = document.getElementById('assistant-suggestions');
        if (suggestionsContainer) {
          suggestionsContainer.style.display = 'none';
        }
      }
    });
  });
})();
