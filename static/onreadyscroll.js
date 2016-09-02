//###########################################################################
//#
//#   File Name         Date          Owner            Description
//#   ----------       -------      ----------       ----------------
//#   onreadyscroll.js  11/19/15  Archana Bahuguna  Display count on click
//#
//###########################################################################

function whenclicked(event) {
        location.hash = this.getAttribute("href")+'#';
        event.preventDefault();
    }
function showtab() {
    if(location.hash) {
        console.log(location.hash);
        var actualname=location.hash.substring(0,location.hash.length-"#".length);
        console.log("actual hash is "+actualname);
        var subtab=$('a[href=' + actualname + ']');
        console.log(subtab.attr("href"));
        var parents=subtab.parents("div.tab-pane");
        var parentnames=parents.map(function() {
    return this.id;
  })
  .get()
  .join( ", " );
        $('a[href=#'+parentnames+']').tab('show');
        console.log(parentnames);
        subtab.tab('show');
    }
}

function documentready() {
    showtab();
    $(document.body).on("click", "a[data-toggle]", whenclicked);
    get_updatedeventdata(1);
    get_futureeventdata(1);
}

function function2() {
    var anchor = location.hash || $("a[data-toggle=tab]").first().attr("href");
    $('a[href=' + anchor + ']').tab('show');
}
$(document).ready(documentready);
$(window).on('popstate', function2);
