
$(document).ready(function() {
    $(document).on('click', '.teamButton', function(){
      $('#taskTable').fadeOut(1000);
      $(".teams").fadeIn(3000);
    });
  });

  $(document).ready(function() {
    $(document).on('click', '.taskButton', function(){
      $(".teams").fadeOut(1000);
      $('#taskTable').fadeIn(3000);
    });
  });