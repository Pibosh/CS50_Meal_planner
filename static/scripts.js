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
  })
  $('#password_1').blur(function(){
    var password_input = $(this).val();
    if (password_input.length < 6){
      $('#password_1_check').text('Password must have at least 6 characters');
      $('#submit-button').prop('disabled', true);
    }else{
      $('#password_1_check').text('');
      $('#submit-button').prop('disabled', false)
    }
  })
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
  })
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
  })
  $('#login').blur(function(){
    var login = $(this).val();
    if (login.length == 0){
      $('#login_check').text('Please insert login');
      $('#submit-button').prop('disabled', true);
    }else{
      $('#login_check').text('');
      $('#login_check').prop('disabled', false);
    }
  })
  $('#password').keyup(function(){
    var password = $(this).val();
    if (password.length == 0){
      $('#password_check').text('Please insert password');
      $('#submit-button').prop('disabled', true)
    }else{
      $('#password_check').text('');
      $('#submit-button').prop('disabled', false)
    }
  })

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
