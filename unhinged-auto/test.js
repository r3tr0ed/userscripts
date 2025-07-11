function createCustomHookEvent(type, targetElement){
  let usrevent = new CustomEvent(type);
  Object.defineProperty(usrevent, 'target', {writable: false, value: targetElement});
  Object.defineProperty(usrevent, 'nativeEvent', {writable: false, value: new InputEvent({bubbles: true, data: "x", inputType: "insertText", returnValue: true, target: targetElement})});
  Object.defineProperty(usrevent, 'isTrusted', {writable: false, value: true});
  return usrevent;
}

//get react methods
function getreactMethod(element){
    let id = null;
    for(let i = 0, keys = Object.keys(element); i < keys.length; i++)
    {
      if ((id = keys[i].match(/^__react[^$]*(\$.+)$/)))
      {
        id = id[1];
        return id;
      }
    }
}

//define 2 different events for each
const emailSelector = document.getElementById("email");
const customEmailEvent = createCustomHookEvent("change", emailSelector);
let reactNumEmail = getreactMethod(emailSelector);
let reactEmailProps = emailSelector[`__reactProps${reactNumEmail}`];

const passwordselector = document.getElementById("password");
const customPasswordEvent  = createCustomHookEvent("change", passwordselector);
let reactNumPass = getreactMethod(passwordselector);
let reactPasswordProps = passwordselector[`__reactProps${reactNumEmail}`];

console.log(reactEmailProps, reactPasswordProps);
//change the values of the elements
emailSelector.value = "topicsgpt@gmail.com";
passwordselector.value = "nonetypeValue";
reactEmailProps.value = "topicsgpt@gmail.com";
reactPasswordProps.value = "nonetypeValue";


reactEmailProps.onChange(customEmailEvent);
reactPasswordProps.onChange(customPasswordEvent);

