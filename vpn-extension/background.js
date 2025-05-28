const proxyConfig = {
  us: { host: '127.0.0.1', port: 8001 },               // Placeholder for US
  de: { host: '127.0.0.1', port: 8002 },               // Placeholder for DE
  jp: { host: '34.85.121.188', port: 8080 }            // ✅ Real Japan proxy
};

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'updateBadge') {
    const text = message.status === 'connected' ? 'ON' : '';
    const color = message.status === 'connected' ? '#4caf50' : '#808080';
    chrome.action.setBadgeText({ text });
    chrome.action.setBadgeBackgroundColor({ color });
  }

  if (message.action === 'setProxy') {
    const { location } = message;
    const proxy = proxyConfig[location];
    if (!proxy) {
      console.warn('No proxy config for location:', location);
      return;
    }

    const config = {
      mode: 'fixed_servers',
      rules: {
        singleProxy: {
          scheme: 'http', // Use HTTP even for HTTPS proxy targets
          host: proxy.host,
          port: proxy.port
        },
        bypassList: ['<local>']
      }
    };

    chrome.proxy.settings.set(
      { value: config, scope: 'regular' },
      () => {
        if (chrome.runtime.lastError) {
          console.error('Proxy set failed:', chrome.runtime.lastError.message);
        } else {
          console.log(`Proxy set for ${location}:`, proxy);
        }
      }
    );
  }

  if (message.action === 'clearProxy') {
    chrome.proxy.settings.clear({ scope: 'regular' }, () => {
      if (chrome.runtime.lastError) {
        console.error('Proxy clear failed:', chrome.runtime.lastError.message);
      } else {
        console.log('Proxy cleared');
      }
    });
  }
});
