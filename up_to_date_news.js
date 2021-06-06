// Needs :
// <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>

function news2html_js(news)
{
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = yyyy + '/' + mm + '/' + dd;

    var ret = "<p><ul>";

    var no_news = 1;
    for(var i = 0; i < news.length; i++) {
	if (news[i]["removal_date"] > today) {
	    var message_html = "no_message";
	    if (news[i]["date1"] != undefined) {
		if (news[i]["date1"] > today) {		
		    message_html = "<span class=\"news_message\">" + news[i]["initial_message"] + "</span>";
		} else {
		    if (news[i]["date2"] != undefined) {
			if (news[i]["date2"] > today) {		
			    message_html = "<span class=\"news_message\">" + news[i]["message_after_date1"] + "</span>";
			} else {
			    message_html = "<span class=\"news_message\">" + news[i]["message_after_date2"] + "</span>";
			}
		    } else {
			message_html = "<span class=\"news_message\">" + news[i]["message_after_date1"] + "</span>";
		    }		    
		}
	    } else {
		message_html = "<span class=\"news_message\">" + news[i]["initial_message"] + "</span>";
	    }
	    
	    ret += "<li>" + message_html + "</li>";
	    
	    no_news = 0;
	}
    }

    if (no_news == 1) {
	return "";
    } else {
	ret += "</ul></p>"
	ret = "<h3>News</h3>" + ret;

	return ret;
    }
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
