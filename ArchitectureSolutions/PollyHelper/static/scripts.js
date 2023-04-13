var API_ENDPOINT = "https://3ojenshk9l.execute-api.eu-west-1.amazonaws.com/Prod/notes/"

document.getElementById("sayButton").onclick = function () {

	var inputData = {
		"voice": $('#voiceSelected option:selected').val(),
		"text": $('#noteText').val()
	};

	$.ajax({
		url: API_ENDPOINT,
		type: 'POST',
		data: JSON.stringify(inputData),
		contentType: 'application/json; charset=utf-8',
		success: function (response) {
			document.getElementById("noteIdreturned").textContent = "Post ID: " + response.noteId;
		},
		error: function () {
			alert("error");
		}
	});
}


document.getElementById("searchButton").onclick = function () {

	var noteId = $('#noteId').val();


	$.ajax({
		url: API_ENDPOINT + '?noteId=' + noteId,
		type: 'GET',
		success: function (response) {

			$('#notes tr').slice(1).remove();

			jQuery.each(response, function (i, data) {

				var player = "<audio controls><source src='" + data['url'] + "' type='audio/mpeg'></audio>"

				if (typeof data['url'] === "undefined") {
					var player = ""
				}

				$("#notes").append("<tr> \
								<td>" + data['id'] + "</td> \
								<td>" + data['voice'] + "</td> \
								<td>" + data['text'] + "</td> \
								<td>" + data['status'] + "</td> \
								<td>" + player + "</td> \
								</tr>");
			});
		},
		error: function () {
			alert("error");
		}
	});
}

document.getElementById("noteText").onkeyup = function () {
	var length = $(noteText).val().length;
	document.getElementById("charCounter").textContent = "Characters: " + length;
}
