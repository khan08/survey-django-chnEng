$(document).ready(function(){
    $('.radio-form > div > label > input').each(function() {
    $(this).parent().before(this);
});
});