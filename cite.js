// ==UserScript==
// @name         Citation Gen 
// @namespace    http://tampermonkey.net/
// @version      2024-06-04
// @description  try to take over the world!
// @author       You
// @match        *://*/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        GM.xmlHttpRequest
// @grant        GM_notification
// ==/UserScript==

(async function() {
    'use strict';

    async function readClipboard() {
        try {
            // Check if the Clipboard API is supported
            if (navigator.clipboard) {
                // Read the clipboard text
                const text = await navigator.clipboard.readText();
                return text;
            } else {
                alert('Clipboard API not supported on this browser.');
                return null;
            }
        } catch (err) {
            console.error(err);
            return null;
        }
    }

    function findCitationOnWeb(url) {
        return new Promise((resolve, reject) => {
            try {
                GM.xmlHttpRequest({
                    method: "GET",
                    url: url,
                    onload: function(response) {
                        if (response.status === 200) {
                            resolve(response.responseText);
                        } else {
                            reject(`Request failed with status ${response.status}`);
                        }
                    },
                    onerror: function(err) {
                        reject(err);
                    }
                });
            } catch (error) {
                reject(error);
            }
        });
    }

    async function handleCitation() {
        const clipboardText = await readClipboard();
        if (clipboardText && (clipboardText.includes("http") || clipboardText.includes("www"))) {
            try {
                const response = await findCitationOnWeb(clipboardText);
                console.log("finished");
                console.log(response);
                GM_notification({ title: "Citation Found", text: "Citation text retrieved successfully.", timeout: 3000 });
            } catch (error) {
                console.error(error);
                GM_notification({ title: "Error", text: "Failed to retrieve citation text.", timeout: 3000 });
            }
        }
    }
    document.addEventListener("DOMContentLoaded", () => {
        document.addEventListener("keydown", async (event) => {
            if (event.altKey && event.key === 'l') {
                console.log("EE");
                await handleCitation();
            }
        });
    });
})();

