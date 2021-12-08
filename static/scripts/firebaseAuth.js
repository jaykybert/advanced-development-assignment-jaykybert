
'use strict';

window.addEventListener('load', function () {
  document.getElementById('logout-button').onclick = function () {
    firebase.auth().signOut();

    // Remove 'Add to Cart' buttons.
    var products = document.getElementsByClassName("add-to-cart");
    for(var i=0; i < products.length; i++) {
      products[i].style.display = "none";
    }

    document.getElementById('login-button').style.display="block";

  };

  // FirebaseUI config.
  var uiConfig = {
    signInSuccessUrl: '/account',
    signInOptions: [
      firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      firebase.auth.EmailAuthProvider.PROVIDER_ID,
    ]
  };

  firebase.auth().onAuthStateChanged(function (user) {

    // Signed In
    if (user) {
      var products = document.getElementsByClassName("add-to-cart");
      for(var i=0; i < products.length; i++) {
        products[i].style.display = "block";
      }

      document.getElementById("logout-button").style.display="block";
      document.getElementById("login-button").style.display="none";
      document.getElementById("account-nav-item").style.display = "block";
      document.getElementById("shopping-cart").style.display = "block";

      // Update back-end session.
        $.ajax({
        type: "POST",
        url: "/login",
        data: JSON.stringify({ "uid": user.uid,
                                    "name": user.displayName,
                                    "email": user.email}),
        contentType: "application/json",
        dataType: "json",
        success: function(result) {
            console.log('success!');
        }
    });


    }
    // Signed Out
    else {
      // Initialize the FirebaseUI Widget using Firebase.
      var ui = new firebaseui.auth.AuthUI(firebase.auth());
      // Show the Firebase login button.
      document.getElementById("logout-button").style.display="none";
      document.getElementById("account-nav-item").style.display = "none";
      document.getElementById("shopping-cart").style.display = "none";
      ui.start('#firebaseui-auth-container', uiConfig);

                // Update back-end session.
    $.ajax({
        type: "POST",
        url: "/logout",
        data: JSON.stringify({ "logged-out": true}),
        contentType: "application/json",
        dataType: "json",
        success: function(result) {
            console.log('success!');
        }
    });




    }
  }, function (error) {
    console.warn(error);
    alert('Unable to log in: ' + error)
  });
});
