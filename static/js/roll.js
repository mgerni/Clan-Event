$(document).ready(function() {
    $(document).on('click', '.choice-menu', function() {
      tile_index = $(this).attr('id');

      req = $.ajax({
        url: '/event/roll/choice/',
        type: 'POST',
        data : {tile_index: tile_index, roll: roll}
      });

      var target = document.getElementById('choice')
      req.done(function(data){
        $(target).html(data)
      });
      
      document.getElementById("choice-modal").showModal();
    });
  });


  $(document).ready(function() {
    $(document).on('click', '.btn-close', () => {
      
     document.getElementById('choice-modal').close()
      
    });
  });

  $(document).ready(function() {
    $(document).on('click', '.confirm-tile', function() {
      $('form').submit(false);
      var roll = $(this).attr('roll');
      var tile_id = $(this).attr('tile_id');
      document.getElementById('choice-modal').close()
      req = $.ajax({
        url : '/event/roll/complete/',
        type : 'POST',
        data : {roll : roll, tile_id : tile_id}
      });

      req.done(function(data) {
        var target = document.getElementsByClassName('container');
        $(target).html(data);
      });

    });
  });

