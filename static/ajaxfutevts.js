//###########################################################################
//#
//#   File Name         Date          Owner            Description
//#   ----------       -------      ----------       ----------------
//#   ajaxfutevts.js  11/19/15  Archana Bahuguna  Ajax call to get fut events
//#
//###########################################################################

var xhr2=new XMLHttpRequest();

function get_futureeventdata(pagenum){
xhr2.open('GET', '/users/'+userid+'/pages/'+pagenum+'/futureevents', true);
xhr2.send(null);
}

$("futureevents").on("click", get_futureeventdata(1));

function handle_pagn_click_futureevent(event){
	var pagenum = $(this).data("pagenum");
	//console.log("Figured out page number for futureevents:"+pagenum);
	get_futureeventdata(pagenum);
}

function replacehtml_futureevents(){

	if (xhr2.status==200)
	{
		document.getElementById('futevents').innerHTML=xhr2.responseText;
		$("ul.pagination.fut a").on("click", handle_pagn_click_futureevent);
		$(window).scrollTop(0);
	}
}

xhr2.onload=replacehtml_futureevents;


