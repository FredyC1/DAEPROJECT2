const proxyConfig = {
    us: { host: '127.0.0.1', port: 8001 },
    de: { host: '127.0.0.1', port: 8002 },
    jp: { host: '127.0.0.1', port: 8003 }
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
      if (!proxy) return;
  
      const config = {
        mode: 'fixed_servers',
        rules: {
          singleProxy: {
            scheme: 'http',
            host: proxy.host,
            port: proxy.port
          },
          bypassList: ['<local>']
        }
      };
  
      chrome.proxy.settings.set(
        { value: config, scope: 'regular' },
        () => console.log(`Proxy set for ${location}`, proxy)
      );
    }
  
    if (message.action === 'clearProxy') {
      chrome.proxy.settings.clear({ scope: 'regular' }, () => {
        console.log('Proxy cleared');
      });
    }
  });
  