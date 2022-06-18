function move() {
	var apperer = document.getElementById('move');
	var text = document.getElementById('texter');
	apperer.innerHTML = "I<b> Can't</b> see U 🙈 "
	text.innerHTML = " "
}

function remove() {
	var apperer = document.getElementById('move');
	var text = document.getElementById('texter');
	apperer.innerHTML = ""
	text.innerHTML = 'Hi , I am Brijesh'
}

async function  repository_fill  (){
	const response = await fetch("https://api.github.com/users/brijeshkrishna/repos");
	const myJson = await response.json();
	console.log(myJson);
	
	var table_row = document.getElementById("table-repos_list");
	

	for (var i = 0; i < myJson.length; i++) {
		var tbody = document.createElement("a");
		tbody.setAttribute('href', 'https://github.com/Brijeshkrishna/'+myJson[i]['name']);
		tbody.setAttribute('target', '_blank');

		tbody.innerHTML = '<img class="repo_img" src="https://github-readme-stats.vercel.app/api/pin/?username=brijeshkrishna&repo=' + myJson[i]['name'] + '&theme=aura" alt="'+ myJson[i]['name']+ '">';
		table_row.appendChild(tbody);

	}


	
}
setTimeout( repository_fill(), 100);
