function interceptToken() {
  return new Promise((resolve) => {
    const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;

    XMLHttpRequest.prototype.setRequestHeader = function (header, value) {
      if (header.toLowerCase() === "authorization" || value.length > 50) {
        resolve(value); // found the token
      }
      return originalSetRequestHeader.apply(this, arguments);
    };
  });
}

let cachedToken = null;
async function getDiscordToken(){
  //attach to all fetch/xml requests and intercept the Authorization header
  if (cachedToken) return cachedToken;
  const token = await interceptToken();
  cachedToken = token;
  return token; 
}

async function createMessagexhr(id, content){
  const xhr = new XMLHttpRequest();
  const uuid = crypto.randomUUID().replace(/-/g, ""); // Remove dashes
  const nonce = uuid.slice(0, 24); // Slice to 24 characters

  const url = `https://discord.com/api/v9/channels/${id}/messages`;
  const bodyObject = {
    "mobile_network_type": "unknown",
    "content": content,
    "nonce": nonce,
    "tts": false,
    "flags": 0
  };

  xhr.open("POST", url, true);
  xhr.setRequestHeader("Authorization", await getDiscordToken());
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.withCredentials = true;

  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (xhr.status >= 200 && xhr.status < 300) {
        console.log("Sent data to specified message link.", JSON.parse(xhr.responseText));
      } else {
        console.error(`Error: ${xhr.status} ${xhr.statusText}`);
      }
    }
  };

  xhr.send(JSON.stringify(bodyObject));
}
function getChannelIdFromUrl(url) {
  const parts = url.split("/");
  return parts[parts.length - 1]; // Get the last part
}

async function getIdsFromChannelFetch(id) {
  try {
    const url = `https://discord.com/api/v9/channels/${id}/messages?limit=100`;
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Authorization": await getDiscordToken(),
        "Content-Type": "application/json"
      },
      credentials: "include"
    });
    
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    const uniqueIds = new Map();
    data.map(element => uniqueIds.set(element.author.id))
    const ids = [...uniqueIds.keys()];
    console.log("Parsing data from response:", ids);
    return ids;
    
  } catch (error) {
    console.error("Error fetching channel data:", error);
    throw error; // Re-throw to let caller handle it
  }
}

const message = "hello! I hope ur doing well :)";
const ids = await getIdsFromChannelFetch(getChannelIdFromUrl(document.location.href));


async function createDmChannel(id){
  try {
    const url = `https://discord.com/api/v9/users/@me/channels`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": await getDiscordToken(),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({"recipients": [`${id}`]}),
      credentials: "include"
    });
    
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
    }
    const data = await response.json();
    console.log("Parsing data from response:", data);
    return data.id; //created id
  } catch (error) {
    console.error("Error fetching channel data:", error);
    throw error; // Re-throw to let caller handle it
  }
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendMessages(ids, message) {
  for (const id of ids) {
    const dmChannel = await createDmChannel(id);
    await createMessagexhr(dmChannel, message);
    await delay(100);
  }
}

sendMessages(ids, message);
