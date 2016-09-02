//###########################################################################
//#
//#   File Name         Date          Owner            Description
//#   ----------       -------      ----------       ----------------
//#   ajaxupevts.js  11/19/15  Archana Bahuguna  Ajax call to get updtd events
//#
//###########################################################################


var xhr1=new XMLHttpRequest();

function get_updatedeventdata(pagenum){
xhr1.open('GET', '/users/'+userid+'/pages/'+pagenum+'/updatedevents', true);
xhr1.send(null);
}

//$("updatedevents").on("click", get_updatedeventdata(1) ); => $("updatedevents").on("click", null);

$("updatedevents").on("click", function () { get_updatedeventdata(1) } );

function handle_pagn_click_updatedevent(event){
	var pagenum = $(this).data("pagenum");
	//console.log("Figured out page number for updatedevents:"+pagenum);
	get_updatedeventdata(pagenum);
}

function replacehtml_updatedevents(){
	if (xhr1.status==200)
	{
		document.getElementById('upevents').innerHTML=xhr1.responseText;
		$("ul.pagination.up a").on("click", handle_pagn_click_updatedevent);
		$(window).scrollTop(0);
	}
}
//when the function name was replacehtml_upevents it was not able to find 
// element id 'upevents' It said null returned. It worked with 2 solns-
// (i)I changed upevents name to upevents1 here and in html
//(ii) I changed name of this function to replacehtml_updatedevents while
//retaining upevents for element id
xhr1.onload=replacehtml_updatedevents;
