// Needs :
// <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>

function process_news(news)
{
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = yyyy + '/' + mm + '/' + dd;

    var ret = [];

    var no_news = 1;
    for(var i = 0; i < news.length; i++) {
	if (news[i]["removal_date"] > today) {
	    var date_val = "";
	    var message_val = "";



	    var beg = "<span class=\"news_message\"> <b>" + news[i]["posting_date"] + "</b>: ";
	    if (news[i]["date1"] != undefined) {
		if (news[i]["date1"] > today) {
		    date_val = news[i]["posting_date"];
		    message_val = news[i]["initial_message"];
		} else {
		    if (news[i]["date2"] != undefined) {
			if (news[i]["date2"] > today) {
			    date_val = news[i]["date1"];
			    message_val = "message_after_date1"
			} else {
			    date_val = news[i]["date1"];
			    message_val = news[i]["message_after_date2"];
			}
		    } else {
			date_val = news[i]["date1"];
			message_val = "message_after_date1"
		    }		    
		}
	    } else {
		date_val = news[i]["posting_date"];
		message_val = news[i]["initial_message"];
	    }

	    entry = {date: date_val, message: message_val};
	    ret.push(entry)
	    
	    no_news = 0;
	}
    }

    ret.sort(function (e1, e2) {
	return e1.date > e2.date;
    });
    
    return ret;
}

function news2html_js(news)
{
    news = process_news(news);

    var ret = "<h3>News</h3> <ul>";

    var no_news = 1;
    for(var i = 0; i < news.length; i++) {
	ret += "<p> <span class=\"news_message\"> <b>" + news[i].date + "</b>: ";
	ret += news[i].message + "</span> </p>";
	no_news = 0;
    }

    if (no_news == 1) {
	ret = "";
    }

    return ret;
}

function up_to_date_news(news_json_filename, news_id)
{
    jQuery.getJSON(news_json_filename, function(news) {
	document.getElementById(news_id).innerHTML = news2html_js(news);
    })
	.fail(function() {
	    document.getElementById(news_id).innerHTML = "syntax error in JSON file";
	});
}
