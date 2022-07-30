$(document).ready(function(){


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