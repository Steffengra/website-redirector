// Listen for web requests
browser.webRequest.onBeforeRequest.addListener(
  async (details) => {
    const settings = await browser.storage.local.get(['enabled', 'redirectUrl']);
    
    if (!settings.enabled) {
      return { cancel: false };
    }

    // Check if the URL is an Instagram URL
    if (details.url.startsWith("https://www.instagram.com/") || details.url.startsWith("http://www.instagram.com/")) {
      const encodedUrl = encodeURIComponent(details.url)
        .replace(/%3A/g, ':')
        .replace(/%2F/g, '/');
      const redirectUrl = `${settings.redirectUrl}${encodedUrl}`;
      return { redirectUrl };
    }
    return { cancel: false };
  },
  { urls: ["*://*.instagram.com/*"] },
  ["blocking"]
);
