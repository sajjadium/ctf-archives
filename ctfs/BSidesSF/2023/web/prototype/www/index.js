class RegistrationRequest{

	constructor(source){
		merge(this, source);
		this.requestsElement = document.getElementById("requests");
		this.clicked = false;
		var newElementOuter = document.createElement("div")
		newElementOuter.className="center";
		
		var newElementInner = document.createElement("div")
		newElementInner.setAttribute("role", "page");
		newElementInner.setAttribute("aria-checked", "true");
		newElementInner.setAttribute("data-augmented-ui", "");

		this.button = document.createElement("button");
		this.button.setAttribute("role", "button");
		this.button.setAttribute("data-augmented-ui","");
		this.button.textContent = "show"

		newElementInner.appendChild(document.createTextNode(this.name));
		newElementInner.appendChild(document.createElement("br"));
		newElementInner.appendChild(this.button);
		newElementOuter.appendChild(newElementInner);

		this.requestsElement.appendChild(newElementOuter);

		var temp = this;
		this.button.addEventListener("click", function(){temp.click()}, true);
		this.outerDiv = newElementOuter;
	}

	click(){
		if(!this.clicked){
			this.display = document.createElement("div")
			this.display.setAttribute("role", "page");
			this.display.setAttribute("aria-checked", "true");
			this.display.setAttribute("data-augmented-ui", "");

			this.display.appendChild(document.createTextNode("Registration Period: "+this.rperiod+" years"))
			this.display.appendChild(document.createElement("br"))
			this.display.appendChild(document.createTextNode("a Registration Type: "+this.rtype));
			this.display.appendChild(document.createElement("br"))
			this.display.appendChild(document.createTextNode("Year: "+this.year));
			this.display.appendChild(document.createElement("br"))
			this.display.appendChild(document.createTextNode("Make: "+this.make));
			this.display.appendChild(document.createElement("br"))
			this.display.appendChild(document.createTextNode("Model: "+this.model));
			this.display.appendChild(document.createElement("br"))
			this.display.appendChild(document.createTextNode("Color: "+this.color));
			this.display.appendChild(document.createElement("br"))
			this.display.appendChild(document.createTextNode("Street Address: "+this.address.streetAddress));
			this.display.appendChild(document.createElement("br"))
			this.display.appendChild(document.createTextNode("State/Province: "+this.address.province));
			this.display.appendChild(document.createElement("br"))
			this.display.appendChild(document.createTextNode("Country: "+this.address.country));
			this.display.appendChild(document.createElement("br"))
			if(this.planet)
				this.display.innerHTML += "Planet: "+this.address.planet+"<br>";

			this.outerDiv.appendChild(this.display);
			this.button.textContent = "hide";
		}
		else{
			this.display.remove()
			this.button.innerHTML = "show"
		}

		this.clicked = !this.clicked;
	}
}

function merge(target, source){
	for(let attr in source){
		if(source[attr] && typeof source[attr] === 'object'){
			if(!target[attr])
				target[attr] = {};
			this.merge(target[attr], source[attr]);
		}
		else if(source[attr]){
			target[attr] = source[attr];
		}
	}
}

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function(){
	if (xhttp.readyState == XMLHttpRequest.DONE){
		requests = JSON.parse(xhttp.response);
		var first = new RegistrationRequest(requests[0]);
		for(var i = 1; i<requests.length; i++){
			new RegistrationRequest(requests[i]);
		}
		first.click();
	}
}
xhttp.open("GET", "/requests", true);
xhttp.send();
