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

document.addEventListener("DOMContentLoaded", function () {
    var isToggled = false; // Variable to track the state

    var changeCssButton = document.getElementById("changeCssButton");
    var icon = document.getElementById("icon");
    var bodyElement = document.querySelector('body');
    var chatElement = document.querySelector('.card');
    var sidenavElement = document.querySelector('.sidenav');
    var faqs = document.querySelector('.faq-section');
	var graphPlotterButton = document.querySelector('a[href="/graphy"]');
    var chatBotButton = document.querySelector('a[href="/"]');
    var modal = document.querySelector('.modal-content');
    var faqItems = document.querySelectorAll('.list-group-item');

    changeCssButton.addEventListener("click", function () {
        isToggled = !isToggled;

        if (isToggled) {
            // Enable dark mode
            bodyElement.style.backgroundColor = "070F2B";
            bodyElement.style.color = "#f7f8fc";
            if (modal) modal.style.backgroundColor = "070F2B";
            if (chatElement) chatElement.style.backgroundColor = "070F2B";
            if (chatElement) chatElement.style.color = "#f7f8fc";
            if (sidenavElement) sidenavElement.style.backgroundColor = "070F2B";
            if (sidenavElement) sidenavElement.style.color = "white";
            if (faqs) faqs.style.backgroundColor = "535C91";
            changeCssButton.style.color = "white";
			graphPlotterButton.style.color = "#FF9EAA"; // Adjust as needed
            chatBotButton.style.color = "#FF9EAA"; // Adjust as needed

			faqItems.forEach(function (item) {
                item.style.backgroundColor = "#292B4A";
                item.style.color = "white";
            });

            // Change icon to sun
            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");
        } else {
            // Disable dark mode
            bodyElement.style.backgroundColor = "";
            bodyElement.style.color = "";
            if (modal) modal.style.backgroundColor = "";
            if (chatElement) chatElement.style.backgroundColor = "";
            if (chatElement) chatElement.style.color = "";
            if (sidenavElement) sidenavElement.style.backgroundColor = "";
            if (sidenavElement) sidenavElement.style.color = "";
            if (faqs) faqs.style.backgroundColor = "";
            changeCssButton.style.color = "black";
			graphPlotterButton.style.color = ""; // Reset to default
            chatBotButton.style.color = ""; // Reset to default

			faqItems.forEach(function (item) {
                item.style.backgroundColor = "";
                item.style.color = "";
            });

            // Change icon to moon
            icon.classList.remove("fa-sun");
            icon.classList.add("fa-moon");
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const recordBtn = document.getElementById('recordBtn');
    const stopBtn = document.getElementById('stopBtn');
    const textInput = document.getElementById('text');

    let recognition;
    let isRecording = false;

    // Check for browser support
    if (!('webkitSpeechRecognition' in window)) {
        alert('Your browser does not support speech recognition. Try using Chrome.');
    } else {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = function () {
            isRecording = true;
            recordBtn.style.display = 'none';
            stopBtn.style.display = 'inline';
        };

        recognition.onresult = function (event) {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            textInput.value = finalTranscript + interimTranscript;
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error', event);
        };

        recognition.onend = function () {
            isRecording = false;
            recordBtn.style.display = 'inline';
            stopBtn.style.display = 'none';
        };
    }

    recordBtn.addEventListener('click', function () {
        if (isRecording) {
            recognition.stop();
            return;
        }
        recognition.start();
    });

    stopBtn.addEventListener('click', function () {
        if (isRecording) {
            recognition.stop();
        }
    });
});

// ***************************************QUESTIONS HINT SECTION****************************************
function copyToClipboard(text) {
	const regex = /^\d+/;
    if (regex.test(text)) {
        text = text.substring(3);
    }
	navigator.clipboard.writeText(text).then(function() {
		alert('Copied to clipboard: ' + text);
	}, function(err) {
		console.error('Could not copy text: ', err);
	});
}

$(document).ready(function () {
	$("#messageArea").on("submit", function (event) {
		const date = new Date();
		const hour = date.getHours();
		const minute = date.getMinutes();
		const str_time = hour + ":" + minute;
		var rawText = $("#text").val();

		var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + 
		'<span class="msg_time_send">' + str_time + 
		'</span></div><div class="img_cont_msg"><img src="../static/user_img.png" class="rounded-circle user_img_msg"></div></div>';

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

// ***************************************SELECT TABLE****************************************
$(document).ready(function () {
    $('#select_table').click(function () {
        $.ajax({
            type: 'GET',
            url: '/listTable',
            contentType: 'application/json',
            success: function (response) {
                let data = response;
                console.log(data);
                populateselectModal(data);
            }
        });
    });
});

function populateselectModal(data) {
    let modalBody = $('#table_modal_body');
    modalBody.empty(); // Clear previous items

    data.forEach(itemArray => {
        if (itemArray.length > 0) {
            let item = itemArray[0]; // Assuming each array contains a single item
            console.log(item);
            
            // Create a div for each item
            let itemDiv = $('<div class="mb-2">');
            
            // Create a link with a download icon (using Font Awesome as an example)
            let downloadIcon = $('<i class="fas fa-download mr-2"></i>');
            let itemName = $('<span>').text(item);
            let downloadLink = $('<div class="btn btn-outline-primary btn-sm">')
                                .append(downloadIcon)
                                .append(itemName);
            
			downloadLink.click(function(event) {
				event.preventDefault();
				let tableName = item;
				selectTableFunction(tableName);
			});
            // Append download link to item div
            itemDiv.append(downloadLink);
            
            // Append item div to modal body
            modalBody.append(itemDiv);
        }
    });
}

function selectTableFunction(tableName) {
    // Make AJAX call to Python backend endpoint
    $.ajax({
        type: 'POST',
        url: '/selectTable', // Replace with your backend endpoint URL
        contentType: 'application/json',
        data: JSON.stringify({ tableName: tableName }),
        success: function(response) {
            console.log('Selected successfully.');
            // Handle success response if needed
        },
        error: function(xhr, status, error) {
            console.error('Error calling Python function:', error);
            // Handle error response if needed
        }
    });
}


// ***************************************DOWNLOAD TABLE****************************************
$(document).ready(function () {
    $('#list_table').click(function () {
        $.ajax({
            type: 'GET',
            url: '/listTable',
            contentType: 'application/json',
            success: function (response) {
                let data = response;
                console.log(data);
                populateDownloadModal(data);
            }
        });
    });
});

function populateDownloadModal(data) {
	let modalBody = $('#Dtable_modal_body');
	modalBody.empty(); // Clear previous items
	
	// Iterate over each table item in data
	data.forEach(itemArray => {
		if (itemArray.length > 0) {
			let item = itemArray[0]; // Assuming each array contains a single item (table name)
			
			// Create a div for each item
			let itemDiv = $('<div class="mb-2">');
			
			// Create a link with a download icon (using Font Awesome as an example)
			let downloadIcon = $('<i class="fas fa-download mr-2"></i>');
			let itemName = $('<span>').text(item);
			let downloadLink = $('<a class="btn btn-outline-primary btn-sm">').append(downloadIcon).append(itemName);
			
			downloadLink.click(function(event) {
				event.preventDefault();
				let tableName = item;
				selectTableFunction(tableName);
			});
			
			// Append download link to item div
			itemDiv.append(downloadLink);
			
			// Append item div to modal body
			modalBody.append(itemDiv);
		}
	});
}


// ***************************************GRAPH IMAGE COMPONENT****************************************

function updateGraphImage() {
	var imgElement = document.getElementById('graphImage');
	// console.log(imgElement)
	var currentSrc = imgElement.src;

	// Append a timestamp query parameter to ensure cache busting
	var newSrc = currentSrc.split('?')[0] + '?timestamp=' + new Date().getTime();

	// Update the image src
	imgElement.src = newSrc;
  }

function pollForChanges() {
setInterval(function () {
	updateGraphImage();
	// console.log(i++)
}, 5000); // 5000 milliseconds = 5 seconds
}

$(document).ready(function () {
	$("#graphinput").on("submit", function (event) {
	  event.preventDefault();

	  var rawText = $("#text").val();

	  // Clear the input field
	  $("#text").val("");
	  pollForChanges();
	  // Send the input text to the API
	  $.ajax({
		data: {
		  msg: rawText,
		},
		type: "POST",
		url: "/graphy",
	  }).done(function (response) {
		// Handle the response from the API if needed
		console.log(response);
	  });
	});
  });
