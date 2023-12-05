document.getElementById('submit_btn').disabled = true;
        document.querySelector("#id_current_password").addEventListener('keyup', function () {
            if (document.getElementById('id_current_password').value !=
            document.getElementById('id_new_password').value) {
            document.getElementById('submit_btn').disabled = false;
          } else {
            document.getElementById('submit_btn').disabled = true;
          }
        });
        document.querySelector("#id_new_password").addEventListener('keyup', function () {
            if (document.getElementById('id_current_password').value !=
            document.getElementById('id_new_password').value) {
            document.getElementById('submit_btn').disabled = false;
          } else {
            document.getElementById('submit_btn').disabled = true;
          }
        });
        var lowercase_pattern = new RegExp(
          "^(?=.*[a-z])"
        );
        var uppercase_pattern = new RegExp(
          "(?=.*[A-Z])"
        );
        var special_pattern = new RegExp(
          "(?=.*[-+_!@#$%^&*.,?]).+$"
        );
        var numeric_pattern = new RegExp(
          "(?=.*\\d)"
        );

        document.getElementById("submit_btn").addEventListener('click', function(event) {
            var pw = document.getElementById("id_new_password").value;
            //check empty password field
            if(pw == "") {
             document.getElementById("message").innerHTML = "**Fill the password please!";
             event.preventDefault();
            }

            //minimum password length validation
            if(pw.length < 7) {
             document.getElementById("message").innerHTML = "**Password length must be atleast 7 characters";
             event.preventDefault();
            }

            //maximum length of password validation
            if(pw.length > 15) {
             document.getElementById("message").innerHTML = "**Password length must not exceed 15 characters";
             event.preventDefault();
            }

            if (!lowercase_pattern.test(pw)) {
              document.getElementById("message").innerHTML = "**Password must contain 1 lowercase character";
              event.preventDefault();
            }

            if (!uppercase_pattern.test(pw)) {
              document.getElementById("message").innerHTML = "**Password must contain 1 uppercase character";
              event.preventDefault();
            }

            if (!numeric_pattern.test(pw)) {
              document.getElementById("message").innerHTML = "**Password must contain 1 numeric character";
              event.preventDefault();
            }

            if (!special_pattern.test(pw)) {
              document.getElementById("message").innerHTML = "**Password must contain 1 special character";
              event.preventDefault();
            }

        });