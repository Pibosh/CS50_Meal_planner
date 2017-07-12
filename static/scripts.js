
var constraints = {
  username: {
    presence: true,


  },
  password_1: {
    presence: true,
    length: {
      minimum: 6,
      message: "^User name must have at least 6 characters"
    }
  },
  password_2: {
    presence: true,
    equality: {
      attribute: "password_1"
      message: "^The passswords must be the same"
    }
  }
  email: {
    presence: true,
    email: true


  },
}

// execute when the DOM is fully loaded
$(function() {
  // declaring constraints for validate.js










}
