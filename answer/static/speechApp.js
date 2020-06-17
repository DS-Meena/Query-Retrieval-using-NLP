//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

// Function call events
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

//Recording Functions
function startRecording() {
	console.log("recordButton clicked");

    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia()
	*/
	recordButton.disabled = true;
	stopButton.disabled = false;

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device
		*/
		audioContext = new AudioContext();


		/*  assign to gumStream for later use  */
		gumStream = stream;

		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;
	});
}

//STOP RECORDING FUNCTION
function stopRecording() {
	console.log("stopButton clicked");

	//disable the stop button, enable the record too allow for new recordings
	recordButton.disabled = false;
	stopButton.disabled = true;

	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {

    uploadtofolder(blob)
	var url = URL.createObjectURL(blob);

}

// Required for Django CSRF
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

function uploadtofolder(blob) {
        var csrftoken = getCookie('csrftoken');

        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'upload');

        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.setRequestHeader("MyCustomHeader", "Put anything you need in here, like an ID");

        xhr.onreadystatechange = function() {
             if (xhr.readyState == XMLHttpRequest.DONE) {
                  var data = xhr.responseText;
                  var jsonResponse = JSON.parse(data);

                  console.log(jsonResponse["ans"]);
                  document.getElementById("ans").innerHTML = jsonResponse["ans"];

                  if (jsonResponse["ques"] != "") {
                  document.getElementById("ques").innerHTML = "Did you said: " + jsonResponse["ques"] + "?";
             }
             }
        }

        //xhr.upload.onloadend = function() {
        //    alert('Upload complete');
        //};
        xhr.send(blob);
        console.log(blob);
}
