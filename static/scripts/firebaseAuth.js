'use strict';


window.addEventListener('load', function () {

  // Redirect on logout, hide add to basket buttons, display login button.
  document.getElementById('logout-button').onclick = function () {
    firebase.auth().signOut();

    window.location.href='products';

    // Remove 'Add to Cart' buttons.
    var products = document.getElementsByClassName("add-to-cart");
    for(var i=0; i < products.length; i++) {
      products[i].style.display = "none";
    }
    document.getElementById('login-button').style.display="block";
  };

  // FirebaseUI config.
  var uiConfig = {
    signInSuccessUrl: '/products',
    signInOptions: [
      firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      firebase.auth.EmailAuthProvider.PROVIDER_ID,
    ]
  };

  firebase.auth().onAuthStateChanged(function (user) {

    // User logged in.
    if (user) {

      // Display 'Add to Cart' buttons.
      var products = document.getElementsByClassName("add-to-cart");
      for(var i=0; i < products.length; i++) {
        products[i].style.display = "block";
      }

      // Update DOM elements.
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
          dataType: "json"
      });
    }

    // User logged out.
    else {

      var ui = new firebaseui.auth.AuthUI(firebase.auth());

      // Update DOM elements
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
      });
    }
  },

  // Authentication Error
  function (error) {
    console.warn(error);
    alert('Unable to log in: ' + error)
  });
});
