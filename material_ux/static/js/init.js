$(document).ready(function(){

    $('div.form-check.double-label').each(function(){ setActiveLabel(this); });
    $("div.form-check.double-label").change(function(){ setActiveLabel(this); });


    $('.material-card > .mc-btn-action').click(function () {
        let card = $(this).parent('.material-card');
        let icon = $(this).children('i');
        let removedClass = '';
        let addedClass = '';
        icon.addClass('fa-spin-fast');

        if (card.hasClass('mc-active')) {
            removedClass = 'fa-arrow-left';
            addedClass = 'fa-bars';
        } else {
            addedClass = 'fa-arrow-left';
            removedClass = 'fa-bars';
        }
        card.toggleClass('mc-active');
        window.setTimeout(function() {
            icon.removeClass(removedClass).removeClass('fa-spin-fast').addClass(addedClass);
        }, 300);
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
