chrome.tabs.onUpdated.addListener(async function(tabId, changeInfo, tab) {

    if (changeInfo.status !== 'complete' || !tab.url) return;

    // ❗ Avoid loop
    if (tab.url.includes("blocked.html")) return;

    // 🔥 Allow Chrome internal pages
    if (tab.url.startsWith("chrome://")) return;

    let url;
    try {
        url = new URL(tab.url).hostname;
    } catch (e) {
        return;
    }

    // 🔥 Allow backend
    if (url.includes("127.0.0.1") || url.includes("localhost")) return;

    // 🔥 Allow Google
    if (url.includes("google.com")) return;

    try {
        let response = await fetch("http://127.0.0.1:8000/check-url/?url=" + url, {
            credentials: "include"
        });

        let data = await response.json();

        // ✅ IMPORTANT: If allowed → do nothing
        if (!data.blocked) return;

        // 🔥 Redirect with reason
        chrome.tabs.update(tabId, {
            url: chrome.runtime.getURL(
                "blocked.html?site=" + url + "&reason=" + encodeURIComponent(data.reason || "Restricted")
            )
        });

    } catch (e) {
        console.log("Error:", e);
    }
});



// chrome.tabs.onUpdated.addListener(async function(tabId, changeInfo, tab) {

//     if (changeInfo.status !== 'complete' || !tab.url) return;

//     try {
//         let url = new URL(tab.url).hostname;

//         // Allow backend
//         if (url.includes("127.0.0.1") || url.includes("localhost")) return;

//         let response = await fetch("http://127.0.0.1:8000/check-url/?url=" + url, {
//             credentials: "include"
//         });

//         let data = await response.json();

//         if (data.blocked) {
//             chrome.tabs.update(tabId, {
//                 url: "https://www.google.com"
//             });
//         }

//     } catch (e) {
//         console.log(e);
//     }
// });