document.addEventListener('DOMContentLoaded', async () => {
  const enabledCheckbox = document.getElementById('enabled');
  const redirectUrlInput = document.getElementById('redirectUrl');
  const saveBtn = document.getElementById('saveBtn');
  const statusDiv = document.getElementById('status');

  // Load saved settings
  const settings = await browser.storage.local.get(['enabled', 'redirectUrl']);
  enabledCheckbox.checked = settings.enabled !== false;
  redirectUrlInput.value = settings.redirectUrl || 'https://your-url-here.com/?url=';

  // Save settings
  saveBtn.addEventListener('click', async () => {
    try {
      await browser.storage.local.set({
        enabled: enabledCheckbox.checked,
        redirectUrl: redirectUrlInput.value.trim()
      });
      showStatus('Settings saved successfully!', 'success');
    } catch (error) {
      showStatus('Failed to save settings: ' + error.message, 'error');
    }
  });

  function showStatus(message, type) {
    statusDiv.textContent = message;
    statusDiv.className = type;
    setTimeout(() => {
      statusDiv.style.display = 'none';
    }, 3000);
  }
});
