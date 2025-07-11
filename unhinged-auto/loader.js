// ==UserScript==
// @name         Account Loader All
// @namespace    http://tampermonkey.net/
// @version      2024-01-30
// @description  try to take over the world!
// @author       You
// @match        https://www.unhinged.ai/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=unhinged.ai
// @resource     userText file:///Users/maheralmoussaly/Desktop/unhinged-auto/users.txt
// @grant        GM_getResourceText
// ==/UserScript==

function login(hamButton, email, password){
  hamButton.click()
  setTimeout(() => {
    try {
      const checkLog = document.querySelector("[name='Log In']");
      if (checkLog){
        setTimeout(() => {
          const formUrl = "https://api.unhinged.ai/auth/email/login";
          fetch(formUrl, {"headers": {
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJBTk9OWU1PVVMiLCJ0b2tlblR5cGUiOiJhbm9ueW1vdXNfYXV0aCIsImlhdCI6MTcwNTU5MjAyMn0.r8uGEniU92Eow8kMVzH-K-iMt7ooC1rMrNiZ518aA0A",
            "accept": "*/*",
            "content-type": "application/json"
          },
            "body": `{"email": "${email}","password": "${password}"}`,
            "method": "POST",
            "mode": "cors",
            "credentials": "include"
          })
          .then((response) => {
            console.log(response);
            return response;
          })
          .then((response) => {
            console.log(response);
            hamButton.click();
          })
        }, 1000);
      }else{
        document.querySelector("[name='Log Out']").click();
        login(hamButton, email, password);
      }
    } catch (error) {
      console.error("Errno", error);
    }
      
  }, 1000);
 }

function createButton(textContent){
  const myButton = document.createElement("button");
  const bottomBar = document.querySelector(".bottom-bar");
  myButton.textContent = textContent;
  bottomBar.appendChild(myButton);
  return myButton;
}

(function() {
  'use strict';

  // Your code here...
  console.log("loading plugin");
  //add current file reading url
  let userString = GM_getResourceText("userText");
  userString = userString.split("\n").join(",");
  userString = "[" + userString.replaceAll(new RegExp("'", 'g'), "\"").slice(0, -1) + "]";
  userString = JSON.parse(userString);
  console.log(userString);
  const switchBtn = createButton("Switch Account");
  switchBtn.addEventListener("click", () => {
    let userInput = prompt("Select Index of desired Element: ");
    userInput = parseInt(userInput);
    if (!isNaN(userInput)){
      const hamburgerButton = document.querySelector("button");
      const selectedEmail = userString[userInput].email; 
      const selectedPassword = userString[userInput].password;
      if (selectedEmail && selectedPassword){
        login(hamburgerButton, selectedEmail, selectedPassword); 
      }
    }else{
      console.error("Hey, you can't use a non number for input!");
    }
  });
   
})();
