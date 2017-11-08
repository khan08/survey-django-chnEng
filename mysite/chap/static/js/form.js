$(document).ready(function(){
    $('.radio-inline > input').each(function() {
    $(this).parent().before(this);
    });

    $('.checkbox-inline > input').each(function() {
    $(this).parent().attr('for',$(this).attr("id"))
    $(this).parent().before(this);
    });
});