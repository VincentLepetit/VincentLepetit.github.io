// Needs :
// <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
// <script src="BibTex.js"></script>

var expanded_venues = [
    "3DV",   "International Conference on 3D Vision",
    "ACCV",  "Proceedings of the Asian Conference on Computer Vision (<b>ACCV</b>)",
    "arXiv", "arXiv",
    "ARXIV", "arXiv",
    "BMVC",  "Proceedings of the British  Machine Vision Conference (<b>BMVC</b>)",
    "CVIU",  "Computer Vision and Image Understanding (<b>CVIU</b>)",
    "CVPR",  "Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (<b>CVPR</b>)",
    "ECCV",  "Proceedings of the European Conference on Computer Vision (<b>ECCV</b>)",
    "ICCV",  "Proceedings of the International Conference on Computer Vision (<b>ICCV</b>)",
    "ICCV Workshop", "do not expand",
    "ICCVW", "Workshop at the International Conference on Computer Vision (<b>ICCV Workshop</b>)",
    "IJCV",  "International Journal of Computer Vision (<b>IJCV</b>)",
    "ISMAR", "Proceedings of the International Symposium on Mixed and Augmented Reality (<b>ISMAR</b>)",
    "MICCAI", "Proceedings of the Conference on  Medical Image Computing and Computer Assisted Intervention (<b>MICCAI</b>)",
    "NIPS",  "Advances in Neural Information Processing Systems (<b>NIPS</b>)",
    "PAMI",  "IEEE Transactions on Pattern Analysis and Machine Intelligence (<b>PAMI</b>)",
    "VR",    "Proceedings of the IEEE Virtual Reality Conference (<b>VR</b>)",
    "WACV",  "IEEE Winter Conference on Applications of Computer Vision (<b>WACV</b>)"
];

function uniformize_venue(venue) {
    v = expanded_venues;
    for(i = 0; i < v.length; i+=2) {
	if (venue == v[i]) {
	    return v[i+1];
	}
    }

    return venue;
}

function extract(entry, field)
{
    if (array_key_exists(field, entry)) {
	field_text = entry[field];
	field_text.replace(/\s+/, ' ');
	return trim(field_text);
    } else {
	return "";
    }
}

function entry2html(entry)
{
    ret = "";

    var weblink = extract(entry, 'weblink');
    if (weblink == "") {
	weblink = extract(entry, 'pdf');
    }
    if (weblink != "") {
	if (!weblink.includes("http")) {
		weblink = "https://vincentlepetit.github.io/publications/../files/" + weblink;
	}
    }
	
    ////////////////////////////////////////////////////////////////////////////////

    var title = "";
    if (entry['entryType'] == 'inbook') {
	title = extract(entry, 'chapter');
    } else {
	title = extract(entry, 'title');
    }
    var title_html = "";
    if (weblink != "") {
	title_html = "<a class=\"title\" href=\"" + weblink + "\">" + trim(title) + "</a>";
    } else {
	title_html = "<span class=\"title\">" + trim(title) + "</span>";
    }

    ////////////////////////////////////////////////////////////////////////////////

    var authors_html = ""
    if (array_key_exists('author', entry)) {
    	var N = entry['author'].length;
    	if (N == 1) {
    	    authors_html = bibtex_entries._formatAuthor(entry['author'][0]);
    	}
    	if (N == 2) {
    	    authors_html = bibtex_entries._formatAuthor(entry['author'][0]);
    	    authors_html += " and ";
    	    authors_html += bibtex_entries._formatAuthor(entry['author'][1]);
    	}
    	if (N >= 3) {
    	    for (var i = 0; i < N-1; i++) {
    		authors_html += bibtex_entries._formatAuthor(entry['author'][i]);
    		authors_html += ", "
    	    }
    	    authors_html += "and ";
    	    authors_html += bibtex_entries._formatAuthor(entry['author'][N-1]);
    	}
	authors_html = "<span class=\"authors\">" + authors_html + "</span>";
    }

    ////////////////////////////////////////////////////////////////////////////////

    var venue_html = "";

    if (entry['entryType'] == 'inproceedings') {
	var booktitle = extract(entry, 'booktitle')
	venue_html = "In <i>" + uniformize_venue(booktitle) + "</i>";
    } else if (entry['entryType'] == 'article') {
	var journal = extract(entry, 'journal')
	venue_html = uniformize_venue(journal);
    }

    ////////////////////////////////////////////////////////////////////////////////

    var year = extract(entry, 'year')
    var year_html = "<span class=\"year\">" + year + "</span>";

    ////////////////////////////////////////////////////////////////////////////////

    var note = extract(entry, 'note');
    var note_html = "";
    if (note != "") {
	note_html = "<span class=\"note\">" + note + "</span>";
    }

    ////////////////////////////////////////////////////////////////////////////////

    var project_html = "";
    var project = extract(entry, 'project');
    if (project != '') {
	project_html += "<p><a href = \"" + project + "\">Project page</a></p>"
    }
    
    ////////////////////////////////////////////////////////////////////////////////
    
    if (entry['entryType'] == 'inproceedings') {
	return title_html + ". " + authors_html + ". " + venue_html + ", " + year_html + ". " + note_html + project_html;
    } else if (entry['entryType'] == 'article') {
	return title_html + ". " + authors_html + ". " + venue_html + ", " + year_html + ". " + note_html + project_html;
    } else if (entry['entryType'] == 'inbook') {
	var booktitle = extract(entry, 'title');
	var booktitle_html = "Chapter in <span class=\"in\">" + booktitle + "</span>";
	var ret = title_html + ". " + authors_html + ". " + booktitle_html;
	var publisher = extract(entry, 'publisher');
	if (publisher != "") {
	    var publisher_html = "<span class=\"publisher\">" + publisher + "</span>";
	    ret += ". " + publisher_html;
	}
	ret += ", " + year_html + ". " + note_html + project_html;
	return ret;
    } else if (entry['entryType'] == 'techreport') {
	var ret = title_html + ". " + authors_html + ". ";
	ret += "<span class=\"in\">Technical Report</span>";
	var institution = extract(entry, 'institution');
	if (institution != "") {
	    ret += ", <span class=\"institution\">" + institution + "</span>";
	}
	var number = extract(entry, 'number');
	if (number != "") {
	    ret += ", <span class=\"number\">" + number + "</span>";
	}
	ret += ", " + year_html + ". " + note_html + project_html;
	return ret;
    } else if (entry['entryType'] == 'hdr') {
	return title_html + ". " + authors_html + ". " + venue_html + ", " + year_html + ". " + note_html + project_html;
    }

    ////////////////////////////////////////////////////////////////////////////////
        
    return "entry type not implemented for " + title;
}

function bibtex2html_BibTex(bibtex_entries)
{
    var year = Number(extract(bibtex_entries.data[0], 'year'))
    var min_year = year;
    var max_year = year;
    for (var i=0; i<bibtex_entries.data.length; i++){
	year = Number(extract(bibtex_entries.data[i], 'year'))
	if (year > max_year) { max_year = year; }
	if (year < min_year) { min_year = year; }
    }

    var ret = "";

    const uaDataIsMobile = window.navigator.userAgentData?.mobile;
    if (uaDataIsMobile) {
	    ret = "MOBILE";
    } else {
   	    ret = "NOT MOBILE";
    }
	
    for (var current_year = max_year; current_year >= min_year; current_year--) {
	ret += "<h2>\n" + current_year.toString() + "</h2>\n";

	ret += "<table id=\"publis\">\n";

	for (var i=0; i<bibtex_entries.data.length; i++){
	    var entry = bibtex_entries.data[i];
	    var year = Number(extract(entry, 'year'));
	    if (year == current_year) {
		var img = extract(entry, 'img');
		var weblink = extract(entry, 'weblink');
		if (weblink == "") {
		  weblink = extract(entry, 'pdf');
		}
		entry_html = entry2html(entry);
		var anchor_html = "<a id=\"" + entry['cite'] + "\"></a>";		
		ret += anchor_html;

		ret += "<tr>\n";
		if (img != '') {
		    ret += "<td>";
		    if (weblink != '') {
			ret += "<a href = \"" + weblink + "\">";
		    }
		    ret += "<img alt = \"<missing>\" width = 300 src = \"https://vincentlepetit.github.io/" + img + "\" class = \"thumbnail\" ></img>";
		    if (weblink != '') {
			ret += "</a>";
		    }
		    ret += "</td><td>";
		    ret += entry_html;
		    ret += "</td></tr>\n";
		} else {
		    ret += "<td colspan=\"2\">";
		    ret += entry_html;
		    ret += "</td>";
		}
		ret += "</tr>\n";
	    }
	}
	ret += "</table>\n";
    }

    return ret;
}

function bibtex2html_bibfile(bibfile_name, list_of_publications_id)
{
    jQuery.get(bibfile_name, function(textString) {
	bibtex_entries = new BibTex();
	bibtex_entries.content = textString;
	bibtex_entries.parse();
	document.getElementById(list_of_publications_id).innerHTML = bibtex2html_BibTex(bibtex_entries);
    });
}
