var msg = new SpeechSynthesisUtterance();
msg.volume = 1; // 0 to 1
msg.lang = 'en-US';

msg.text = "Hello Sir!";
window.speechSynthesis.speak(msg);

var connection = new ReconnectingWebSocket('ws://localhost:8080');

connection.onopen = function () {
	// connection is opened and ready to use
	msg.text = "Connection established";
	window.speechSynthesis.speak(msg);
	init();
};

connection.onerror = function (error) {
	// an error occurred when sending/receiving data
	console.log(error);
};

connection.onmessage = function (message) {
	// try to decode json (I assume that each message from server is json)
	try {
		var json = JSON.parse(message.data);
	} catch (e) {
		console.log('This doesn\'t look like a valid JSON: ', message.data);
		return;
	}
	console.log(json.type);
	if(json.type == "chat"){
		// handle incoming message
		var con = "";
		con += "<div class='debMes'>";
		con += "<span class='debMesUser'>"+json.user+"</span>: <span class='debMesTitle'>"+json.title+"</span><br>";
		con += "<span class='debMesDate'>"+json.date+"</span><br>";
		con += "<span class='debMesContent'>"+json.content+"</span></div>";
		$('#debateCon').append(con);
		var objDiv = document.getElementById('debateCon');
		objDiv.scrollTop = objDiv.scrollHeight;
	}else if(json.type == "push"){
		$("#notificationBar").append("<div class='notification'>"+json.text+"</div>");
		$("#notificationBar").css("display", "block");
		window.setTimeout(function(){$("#notificationBar").html(""); $("#notificationBar").css("display", "none");}, 7000);
	}else if(json.type == "login"){
		
	}else if(json.type == "topics"){
		for(var c in json.content){
			var cont = json.content[c];
			var con = "";
			con += "<div class='topic'>";
			con += "<h4 class='topTitle'><a href='topic.html?id="+cont.id+"' class='topTitle'>"+cont.title+"</a></h4>";
			con += "<span class='topDate'>"+cont.date+"</span><br>";
			con += "<span class='topContent'>"+cont.content+"</span></div>";
			$('#news .content').append(con);
		}
	}
};

$("#debIn").on("keydown", function (e) {
	if(e.which == 13) {
		var input = $('#debIn').val();
		console.log(input);
		window.setTimeout(function(){document.getElementById("debIn").value = "";}, 1);
		var obj = {
			type: "chat",
			content: input
		}
		connection.send(JSON.stringify(obj));
	}
});

function send(obj){
	connection.send(JSON.stringify(obj));
}

function getPage(page){
	$.ajax({
	  url: "getPages.php",
	  data: {page: page}
	})
	.done(function( html ) {
		$( "#container" ).append( html );
	  });
}
