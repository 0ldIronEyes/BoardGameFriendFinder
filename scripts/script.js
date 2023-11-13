//storing input and listbox
const input = document.querySelector('#searchinput');
const suggestions = document.querySelector('.suggestions ul');





//Add eventlistener to input from user, if input text is empty, clear the list, if not populate results
input.addEventListener('input',async function inputFind() {
	const inputText = input.value;
	if (inputText !== "")
	{
		const searchResults = await search(inputText);
		//showSuggestions(searchResults);
	}
	else
	{
		suggestions.innerHTML = "";
	}
});



//takes user's input as parameter, then returns an array (results) that contains items from fruit array that contain user's input.
async function search(str) {
	response = await axios.get(`https://boardgamegeek.com//xmlapi2/search?query=${str}&type=boardgame`)
	var xmlText = response.data;      
    var parser = new DOMParser();
    var xmlDoc = parser.parseFromString(xmlText, "text/xml");
	var nameElements = xmlDoc.querySelectorAll('name[type="primary"]');

	var result = [];
	for (var i = 0; i < nameElements.length; i++) {
   		var nameElement = nameElements[i];
    	var value = nameElement.getAttribute("value");
    	if (value.toLowerCase().includes(str.toLowerCase())) {
        	result.push(value);
    	}
	}
	if (result)
	{
		showSuggestions(result);
	}
	
	//return results;
}


//populates the list of suggestions by creating list items under the suggestions ul. 
function showSuggestions(results) {
	console.log(results);
	suggestions.innerHTML = "";
    results.map(res => {
	const li=document.createElement('li');
	//const button = document.createElement('button');
	
	//button.href = `/users/add_games/${res}`;
    //button.innerText = `${res}`;
	li.innerText = `${res}`;
	//li.appendChild(button);
    suggestions.appendChild(li);
   })

}

//activated by clicking on a list item, sets the input value to be the text in the list item that was clicked on, then clears the suggestions list.
function useSuggestion(ev) {
	if (ev.target.tagName === 'LI') {
		suggestions.innerHTML = "";
		input.value = ev.target.innerText;
	  }
}




suggestions.addEventListener('click', useSuggestion);


