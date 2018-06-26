function get_results() {
	var python = require("python-shell");
	var path = require("path");

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["loadresult"]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("results").value = message;
	});
}

function get_userid() {
	var python = require("python-shell");
	var path = require("path");

	var username = document.getElementById("username").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getuserid", username]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("userid").value = message;
		document.getElementById("userid2").value = message;
		document.getElementById("status").value = message;
	});
}
function get_username() {
	var python = require("python-shell");
	var path = require("path");

	var userid = document.getElementById("userid").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getusername", userid]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("username").value = message;
		document.getElementById("status").value = message;
	});
}
function get_profilepic() {
	var python = require("python-shell");
	var path = require("path");

	var userid = document.getElementById("userid").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getprofilepic", userid, "False"]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
function get_newpost() {
	var python = require("python-shell");
	var path = require("path");

	var userid = document.getElementById("userid").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getnewpost", userid, "False"]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
function get_mediacount() {
	var python = require("python-shell");
	var path = require("path");

	var userid = document.getElementById("userid").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getmediacount", userid]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
function get_stories() {
	var python = require("python-shell");
	var path = require("path");

	var userid = document.getElementById("userid").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getstories", userid, "False"]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
function get_pstatus() {
	var python = require("python-shell");
	var path = require("path");

	var userid = document.getElementById("userid").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getprivacysetting", userid]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
function dl_profilepicture() {
	var python = require("python-shell");
	var path = require("path");

	var userid = document.getElementById("userid2").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getprofilepic", userid, "True"]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
function dl_newpost() {
	var python = require("python-shell");
	var path = require("path");

	var userid = document.getElementById("userid2").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getnewpost", userid, "True"]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
function dl_stories() {
	var python = require("python-shell");
	var path = require("path");

	var userid = document.getElementById("userid2").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getstories", userid, "True"]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
function dl_media() {
	var python = require("python-shell");
	var path = require("path");

	var postid = document.getElementById("postid").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["getmedia", postid, "True"]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
function start_instabot() {
	var python = require("python-shell");
	var path = require("path");

	var channel = document.getElementById("channel").value;
	var apitoken = document.getElementById("apitoken").value;
	var rtime = document.getElementById("runtime").value;
	var stime = document.getElementById("storytime").value;
	var userids = document.getElementById("userids").value;
	var debugging_mode = String(document.getElementById("debugg").checked);

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["instabot", channel, apitoken, rtime, stime, debugging_mode, userids]
	}

	document.getElementById("status").value = "Running...";

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = "Finished!";
	});
}
function instaview() {
	var python = require("python-shell");
	var path = require("path");

	var a_path = document.getElementById("absolutepath").value;

	var options = {
		scriptPath : path.join(__dirname, '/bin/python/'),
		args : ["instaview", a_path]
	}

	var pyscript = new python('requesthandler.py', options);

	pyscript.on('message', function(message) {
		document.getElementById("status").value = message;
	});
}
