//###########################################################################
//#
//#   File Name         Date          Owner            Description
//#   ----------       -------      ----------       ----------------
//#   countonclick.js  11/19/15  Archana Bahuguna  Display count on click
//#
//###########################################################################

var count=0;

function displayCount()
{
	count++;
	window.alert(count)
}

var el=document.getElementById('feature-1');
el.onclick=displayCount;