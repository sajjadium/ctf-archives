// submit flag
function submitFlag() {
  const formId = event.target.closest('form').id;
  const formData = Object.fromEntries(new FormData(document.getElementById(formId)).entries());
  const data = Object.entries(formData)[0];
  const id = data[0]
  const flag = data[1]

  const jdata = { 
  	_id: id,
  	challenge_flag: flag
  };

  fetch("/submit_flag", {
	  method: "POST",
	  body: JSON.stringify(jdata),
	  headers: {
	    "Content-Type": "application/json"
	  }
	})
	.then(response => response.text())
	.then(text => {
    alert(text);
  })
  .catch(error => console.error(error));
}