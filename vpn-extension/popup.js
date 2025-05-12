document.addEventListener('DOMContentLoaded', () => {
    const locationSelect = document.getElementById('location');
    const connectBtn = document.getElementById('connectBtn');
    const resetBtn = document.getElementById('resetBtn');
    const statusText = document.getElementById('status');
    const loader = document.getElementById('loader');
  
    // Load saved state
    chrome.storage.local.get(['vpnStatus', 'selectedLocation'], (data) => {
      if (data.selectedLocation) locationSelect.value = data.selectedLocation;
      const connected = data.vpnStatus === 'connected';
      updateUI(connected);
    });
  
    // Connect / Disconnect
    connectBtn.addEventListener('click', () => {
      connectBtn.disabled = true;
      loader.style.display = 'block';
  
      const selectedLocation = locationSelect.value;
      chrome.storage.local.set({ selectedLocation });
  
      chrome.storage.local.get(['vpnStatus'], (data) => {
        const isConnected = data.vpnStatus === 'connected';
        const newStatus = isConnected ? 'disconnected' : 'connected';
  
        setTimeout(() => {
          chrome.storage.local.set({ vpnStatus: newStatus }, () => {
            chrome.runtime.sendMessage({
              action: 'updateBadge',
              status: newStatus
            });
  
            chrome.runtime.sendMessage({
              action: isConnected ? 'clearProxy' : 'setProxy',
              location: selectedLocation
            });
  
            updateUI(newStatus === 'connected');
            loader.style.display = 'none';
            connectBtn.disabled = false;
          });
        }, 1000);
      });
    });
  
    // Reset VPN
    resetBtn.addEventListener('click', () => {
      chrome.runtime.sendMessage({ action: 'clearProxy' }, () => {
        chrome.storage.local.set({ vpnStatus: 'disconnected' }, () => {
          chrome.runtime.sendMessage({ action: 'updateBadge', status: 'disconnected' });
          updateUI(false);
          alert('VPN has been reset.');
        });
      });
    });
  
    function updateUI(connected) {
      statusText.textContent = `Status: ${connected ? 'Connected' : 'Disconnected'}`;
      connectBtn.textContent = connected ? 'Disconnect' : 'Connect';
    }
  });
  