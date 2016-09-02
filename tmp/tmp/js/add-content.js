console.log("Hello- starting..............");

function validate() {
    console.log("Hello- entering validate fn:..............");
    var name = document.getElementById("name").value;
    var a = document.getElementById("a").value;
    var b = document.getElementById("b").value;
    var c = document.getElementById("c").value;
    $.ajax({
        type: "POST",
        url: "http://192.168.33.10:5005/jsurl",
            contentType: "application/json",
            dataType: 'json',
               data:JSON.stringify({
               jsonname:name,
               jsona:a,
               jsonb:b,
               jsonc:c
       }),
       success: function() {
         alert('success');
       }
    });
        console.log(name,a,b,c)

    }
