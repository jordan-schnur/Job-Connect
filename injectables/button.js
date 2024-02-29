var newButton = document.createElement("button");
newButton.innerHTML = "Click Me";
newButton.id = "seleniumInjectedButton";
newButton.style = "position: fixed; top: 0; right: 0; z-index: 9999;background-color: blue; color: white;padding:10px;";

var hiddenInput = document.createElement("input");
hiddenInput.type = "hidden";
hiddenInput.id = "seleniumHiddenInput";

document.body.appendChild(newButton);
document.body.appendChild(hiddenInput);

document.getElementById("seleniumInjectedButton").addEventListener("click", function () {
    document.getElementById("seleniumHiddenInput").value = "clicked";
});