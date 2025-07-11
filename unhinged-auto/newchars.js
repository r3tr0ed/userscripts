const counter = 10;
// main tag ID is NSFW tag
const tagId = "6531c7a6fe4908d7ec875ca6";

const authToken = document.cookie.split('; ').find(cookie => cookie.startsWith('authToken=')).split('=')[1];

let allObjects = [];
// Array to store all fetch promises
const fetchPromises = [];

for (let index = 0; index < counter; index++) {
  const skipAmount = index * 20;
  console.log("Skip", skipAmount);
  const fetchPromise = fetch(`https://api.unhinged.ai/feed/tag?tagId=${tagId}&skip=${skipAmount}`, {
    "headers": {
      "Authorization": `Bearer ${authToken}`,
      "Content-type": "application/json"
    },
    "body": null,
    "method": "GET",
    "mode": "cors",
    "credentials": "include"
  })
  .then((response) => {return response.json();})
  .then((res) => {
    console.log(res);
    res.newCharacters.forEach((element) => {allObjects.push(element)});
    res.featuredCharacters.forEach((element) => {allObjects.push(element)});
    res.topCharacters.forEach((element) => {allObjects.push(element)});
  })
  .then(() => {
    console.log(`Finished Batch ${index}`, allObjects);
  })
  .catch((err) => {
    console.error("Error when fetching:", err);
  });
  fetchPromises.push(fetchPromise);
}

Promise.all(fetchPromises)
.then(() => {
  allObjects = allObjects.filter((value, index, self) =>
    index === self.findIndex((t) => (
      t._id === value._id || t.name === value.name
    ))
  )

  console.log("Done", allObjects);
})
