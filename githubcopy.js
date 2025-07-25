// ==UserScript==
// @name         School Copy and Paste Github
// @namespace    http://tampermonkey.net/
// @version      2024-06-14
// @description  try to take over the world!
// @author       You
// @match        https://github.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=github.com
// @grant        none
// ==/UserScript==


//create a button to do the copied text for
const newCopyBtn = document.createElement("button");
newCopyBtn.innerHTML = `
<svg aria-hidden="true" focusable="false" role="img" class="octicon octicon-copy" viewBox="0 0 16 16" width="16" height="16" fill="green" style="display:inline-block;user-select:none;vertical-align:text-bottom;overflow:visible">
    <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
</svg>`;
newCopyBtn.style.color = "green";
newCopyBtn.style.border = "none";
newCopyBtn.style.borderRadius = "4px";
newCopyBtn.className = "custom-copy-btn";
newCopyBtn.addEventListener("click", () => {
    const rawText = document.getElementById("read-only-cursor-text-area").value;
    navigator.clipboard.writeText(rawText);
    console.log("Copied text!"); 
});


function injectElement(){
    const mainElement = document.querySelector(".Box-sc-g0xbh4-0.iBylDf");
    if (mainElement){
        if (!document.querySelector(".custom-copy-btn")){
            mainElement.appendChild(newCopyBtn);
        }
    }else{
        console.warn("Not on a page script meant for injecting copy btn.");
    }
}


// Create a new MutationObserver instance
const observer = new MutationObserver((mutationsList, observer) => {
    // Call the function when mutations are observed
    injectElement();
});

// Configuration of the observer:
const config = {
    childList: true,
    subtree: true
};

// Start observing the <body> element
observer.observe(document.body, config);

