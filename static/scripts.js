$(document).ready(function() {
  $('#username').blur(function(){
    var username_input = $(this).val();
    if (username_input.length < 6){
      $('#username_check').text('Username must have at least 6 characters');
      $('#submit-button').prop('disabled', true);
    }else{
      $('#username_check').text('');
      $('#submit-button').prop('disabled', false);
      $('#username_check').text('Checking...');
      check_user();
    }
  });

  $('#password_1').blur(function(){
    var password_input = $(this).val();
    if (password_input.length < 6){
      $('#password_1_check').text('Password must have at least 6 characters');
      $('#submit-button').prop('disabled', true);
    }else{
      $('#password_1_check').text('');
      $('#submit-button').prop('disabled', false)
    }
  });

  $('#password_2').blur(function(){
    var password_input1 = $('#password_1').val();
    var password_input2 = $(this).val();
    if (password_input2.length == 0){
      $('#password_2_check').text('Must repeat password');
      $('#submit-button').prop('disabled', true);
    }else if (password_input1 != password_input2){
      $('#password_2_check').text('Passwords must be the same');
      $('#submit-button').prop('disabled', true);
    }else{
      $('#password_2_check').text('');
      $('#submit-button').prop('disabled', false);
    }
  });

  $('#email').keyup(function(){
    var email_input = $(this).val();
    var re = /^(([^<>()\[\]\\.,;:\s@']+(\.[^<>()\[\]\\.,;:\s@']+)*)|('.+'))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/igm;
    if (email_input.length == 0){
      $('#email_check').text('Must enter your email');
      $('#submit-button').prop('disabled', true);
    }else if(!re.test(email_input)){
      $('#email_check').text('Must enter valid email');
      $('#submit-button').prop('disabled', true);
    }else{
      $('#email_check').text('');
      $('#submit-button').prop('disabled', false);
      $('#email_check').text('Checking...');
      check_email()
    }
  });

  $('#login').blur(function(){
    var login = $(this).val();
    if (login.length == 0){
      $('#login_check').text('Please insert login');
      $('#submit-button').prop('disabled', true);
    }else{
      $('#login_check').text('');
      $('#login_check').prop('disabled', false);
    }
  });

  $('#password').blur(function(){
    var password = $(this).val();
    if (password.length == 0){
      $('#password_check').text('Please insert password');
      $('#submit-button').prop('disabled', true)
    }else{
      $('#password_check').text('');
      $('#submit-button').prop('disabled', false)
    }
  });

  $('#dishName').blur(function(){
    var dishName = $(this).val();
    if (dishName.length == 0){
      $('#dishNameCheck').text('Please insert dish name');
      $('#submit-button').prop('disabled', true)
    }else{
      $('#dishNameCheck').text('');
      $('#submit-button').prop('disabled', false)
    }
  });

  $('#recipeItems').blur(function(){
    var recipeItems = $(this).val();
    if (recipeItems.length == 0){
      $('#recipeItemsCheck').text('Please insert ingridients');
      $('#submit-button').prop('disabled', true)
    }else{
      $('#recipeItemsCheck').text('');
      $('#submit-button').prop('disabled', false)
    }
  });

  $('#recipeHowTo').blur(function(){
    var recipeHowTo = $(this).val();
    if (recipeHowTo.length == 0){
      $('#recipeHowToCheck').text('Please insert recipe');
      $('#submit-button').prop('disabled', true)
    }else{
      $('#recipeHowToCheck').text('');
      $('#submit-button').prop('disabled', false)
    }
  });

$('#searchRecipe').keyup(function(){
  var input = $(this).val();
  var filter = input.toUpperCase();
  console.log(filter);
  var table = $('#recipe_list');
  var tr = table.find("tr");
  var td;
  var i;
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
})

  $('#myModal').on('show.bs.modal', function(e) {
    //get data-id attribute of the clicked element
    var recipeName = $(e.relatedTarget).data('recipe-name');
    var recipeId = $(e.relatedTarget).data('recipe-id');
    console.log(recipeId);
    console.log(recipeName);
    $('#deleteBtn').attr("data-recipe-id", recipeId)
    $('#deleteBtn').attr("data-recipe-name", recipeName)
    //populate the textbox
    $("#recipe_name").text(recipeName);
  });

 $('#deleteBtn').click(function() {
    var id = $(this).data('recipe-id')
    var name = $(this).data('recipe-name')
    $.post('/delete',
    {
      recipe_id: id,
      recipe_name: name
    }, function(result) {
      if (result.result == "success"){
      location.reload();
      }else{
      alert("Something went wrong");
      location.reload();
      }
    })
  });

  function check_user(){
    var username_input = $('#username').val();
    $.post('/_checkUser', {username: username_input}, function(result){
        if(result.result == false){
          $('#username_check').text('Username already taken');
          $('#submit-button').prop('disabled', true);
        }else{
          $('#username_check').text('');
          $('#submit-button').prop('disabled', false);
        }
      })
  }
  function check_email(){
    var email_input = $('#email').val();
    $.post('/_checkEmail', {email: email_input}, function(result){
      if(result.result == false){
        $('#email_check').text('Email already registered');
        $('#submit-button').prop('disabled', true);
      }else{
        $('#email_check').text('');
        $('#submit-button').prop('disabled', false);
      }
    })
  }
})
