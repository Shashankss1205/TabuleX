// navigator.mediaDevices.getUserMedia({ audio: true })
// 	.then(function (stream) {
// 		// Create a MediaRecorder instance to record the audio stream
// 		const mediaRecorder = new MediaRecorder(stream);
// 		const chunks = [];

// 		// When data is available, add it to the chunks array
// 		mediaRecorder.ondataavailable = function (e) {
// 			chunks.push(e.data);
// 		};

// 		// When recording stops, create a Blob and upload it
// 		mediaRecorder.onstop = function () {
// 			const blob = new Blob(chunks, { 'type': 'audio/mp3' });

// 			// Here you can send the blob to your API using fetch or any other method
// 			// For example:
// 			const formData = new FormData();
// 			formData.append('audio', blob);
// 			fetch('/audio', { method: 'POST', body: formData })
// 			  .then(response => {
// 			    // Handle response
// 				console.log(response)
// 			  })
// 			  .catch(error => {
// 			    // Handle error
// 			  });
// 		};

// 		// Start recording when the user clicks a button
// 		recordBtn = document.querySelector("#recordBtn")
// 		stopBtn = document.querySelector("#stopBtn")
// 		recordBtn.addEventListener('click', function () {
// 			mediaRecorder.start();
// 		});

// 		// Stop recording when the user clicks a button
// 		stopBtn.addEventListener('click', function () {
// 			mediaRecorder.stop();
// 		});
// 	})
// 	.catch(function (err) {
// 		console.log('The following error occurred: ' + err);
// 	});
// document.getElementById("changeCssButton").addEventListener("click", function () {
// 	var icon = document.getElementById("icon");
// 	var btn = document.getElementById("changeCssButton");
// 	if (icon.classList.contains("fa-moon")) {
// 		// If the icon is currently a sun, change it to a moon
// 		icon.classList.remove("fa-moon");
// 		icon.classList.add("fa-sun", "fa-inverse");
// 		btn.style.backgroundColor = "#1a1a1a";
// 	} else {
// 		// If the icon is currently a moon, change it to a sun
// 		icon.classList.remove("fa-sun", "fa-inverse");
// 		icon.classList.add("fa-moon");
// 		btn.style.backgroundColor = "white";
// 	}
// });
// JavaScript code to close the modal
document.addEventListener("DOMContentLoaded", function () {
	// Get the close button element
	var closeButton = document.querySelector('.modal .close');

	// Get the modal element
	var modal = document.getElementById('tableModal');

	// Add click event listener to the close button
	closeButton.addEventListener('click', function () {
		// Close the modal by removing the 'show' class
		modal.classList.remove('show');

		// Remove the modal-backdrop element
		var backdrop = document.querySelector('.modal-backdrop');
		backdrop.parentNode.removeChild(backdrop);

		// Set aria-hidden attribute to true
		modal.setAttribute('aria-hidden', 'true');
	});
});

document.querySelector('.add_image').addEventListener('click', function () {
	document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function () {
	var file = this.files[0];
	if (file) {
		var formData = new FormData();
		formData.append('file', file);

		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/addimg', true);
		xhr.onload = function () {
			if (xhr.status === 200) {
				// Request was successful
				console.log('File uploaded successfully');
				alert('File uploaded successfully');
			} else {
				// Error handling
				console.error('Error uploading file:', xhr.statusText);
				alert('Error uploading file: ' + xhr.statusText);
			}
		};
		xhr.send(formData);
	} else {
		console.log('No file selected');
	}
});
document.querySelector('.add_table').addEventListener('click', function () {
	document.getElementById('fileInput2').click();
});

document.getElementById('fileInput2').addEventListener('change', function () {
	var file = this.files[0];
	if (file) {
		var formData = new FormData();
		formData.append('file', file);

		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/addtable', true);
		xhr.onload = function () {
			if (xhr.status === 200) {
				// Request was successful
				console.log('File uploaded successfully');
				alert('File uploaded successfully');
			} else {
				// Error handling
				console.error('Error uploading file:', xhr.statusText);
				alert('Error uploading file: ' + xhr.statusText);
			}
		};
		xhr.send(formData);
	} else {
		console.log('No file selected');
	}
});

var isToggled = false; // Variable to track the state

document.getElementById("changeCssButton").addEventListener("click", function () {
	// Select the elements with the classes to be changed
	var bodyElement = document.querySelector('body');
	var chatElement = document.querySelector('.card');
	var sidenavElement = document.querySelector('.sidenav');
	var showElement = document.querySelector('#show_table');
	var modal = document.querySelector('.modal-content');
	var btn = document.getElementById("changeCssButton");
	// Toggle between two states
	if (!isToggled) {
		// Apply changes for the first state
		bodyElement.style.backgroundColor = "#1a1a1a"; // Change background color
		bodyElement.style.color = "#f7f8fc";
		modal.style.backgroundColor = "#1a1a1a";
		chatElement.style.backgroundColor = "#1a1a1a"; // Change text color
		sidenavElement.style.backgroundColor = "#1a1a1a"; // Change background color
		sidenavElement.style.color = "white"; // Change text color
		showElement.style.color = "white";
		isToggled = true; // Update the state
		btn.style.color = "white"
	} else {
		// Revert changes for the second state
		bodyElement.style.backgroundColor = ""; // Revert background color
		bodyElement.style.color = "";
		modal.style.backgroundColor = "";
		chatElement.style.color = ""; // Revert text color
		chatElement.style.backgroundColor = "";
		showElement.style.color = "black";
		sidenavElement.style.backgroundColor = ""; // Revert background color
		sidenavElement.style.color = ""; // Revert text color
		isToggled = false; // Update the state
		btn.style.color = "black"
	}
});


$(document).ready(function () {
	$("#messageArea").on("submit", function (event) {
		const date = new Date();
		const hour = date.getHours();
		const minute = date.getMinutes();
		const str_time = hour + ":" + minute;
		var rawText = $("#text").val();

		var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';

		$("#text").val("");
		$("#messageFormeight").append(userHtml);

		$.ajax({
			data: {
				msg: rawText,
			},
			type: "POST",
			url: "/get",
		}).done(function (responses) {
			console.log(responses)
			var botHtml = '<div class="d-flex justify-content-start mb-4">';
			botHtml += '<div class="img_cont_msg"><img src="../static/Wrapper@3x.png" class="rounded-circle user_img_msg"></div>';
			botHtml += '<div class="msg_cotainer">';
			if (responses[0].length > 0) {
				botHtml += '<ul>';
				responses[0].forEach(function (response) {
					botHtml += '<li>' + response + '</li>';
				});
				botHtml += '</ul>';
			}
			else {
				botHtml += '<p>No single responses yet.</p>';
			}
			botHtml += '<span class="msg_time">' + str_time + '</span>';
			botHtml += '</div></div>';

			$("#messageFormeight").append($.parseHTML(botHtml));
		});
		event.preventDefault();
	});
});
$(document).ready(function () {
	$('#show_table').click(function () {
		$.ajax({
			type: 'POST',
			url: '/show',
			contentType: 'application/json',
			success: function (response) {
				let data = response.output_value;

				const container = document.getElementById('output');
				container.innerHTML = '';
				// Loop through the data and create tables
				for (const [tableName, rows] of Object.entries(data)) {
					// Create a container for each table and title
					const tableContainer = document.createElement('div');

					const table = document.createElement('table');
					const headerRow = table.insertRow();

					// Create table rows
					for (const row of rows) {
						const newRow = table.insertRow();
						for (const cellData of row) {
							const cell = newRow.insertCell();
							cell.textContent = cellData;
						}
					}

					// Set table title
					const title = document.createElement('h2');
					title.textContent = tableName;

					// Append the title and table to the container for this table
					tableContainer.appendChild(title);
					tableContainer.appendChild(table);

					// Append the container for this table to the main container
					container.appendChild(tableContainer);
				}
			}
		});
	});
});

