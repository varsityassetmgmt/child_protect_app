chrome.tabs.onUpdated.addListener(async function(tabId, changeInfo, tab) {
    if (tab.url) {
        let url = new URL(tab.url).hostname;

        let response = await fetch("http://localhost:8000/check-url/?url=" + url);
        let data = await response.json();

        if (data.blocked) {
            chrome.tabs.update(tabId, {
                url: "https://www.google.com"
            });
        }
    }
});