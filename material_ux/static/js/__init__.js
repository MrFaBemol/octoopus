$(document).ready(function(){

    // Set the right label as active
    let double_label_switches = $("div.mux.form-check.double-label");
    double_label_switches.each(function(){ setActiveLabel(this); });
    double_label_switches.change(function(){ setActiveLabel(this); });

    // Set an empty placeholder on mux input (needed for css classes)
    $("div.mux.form-group input[type=text].form-control").each(function(){
        $(this).attr("placeholder", " ");
    });

});


// Double label switch always have a span.active
function setActiveLabel(checkNode){
    let checkbox = $(checkNode).find("input:checkbox");
    let spanNodes = $(checkNode).find("span");
    if (spanNodes.length !== 2){return;}
    if (checkbox[0].checked){
        $(spanNodes[1]).addClass("active");
        $(spanNodes[0]).removeClass("active");
    } else {
        $(spanNodes[0]).addClass("active");
        $(spanNodes[1]).removeClass("active");
    }
}
