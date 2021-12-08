var loggedIn;

function onAddToCart(productId) {

    $.ajax({
        type: "POST",
        url: "/cart",
        data: JSON.stringify({'id': productId}),
        contentType: "application/json",
        dataType: "json",
        success: function(result) {
            console.log('success!');
        }
    });
}


'use strict';

window.addEventListener('load', function () {
  document.getElementById('logout-button').onclick = function () {
    firebase.auth().signOut();

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

  firebase.auth().onIdTokenChanged(function (user) {
    loggedIn = user;
    // Signed In
    if (user) {
      var products = document.getElementsByClassName("add-to-cart");
      for(var i=0; i < products.length; i++) {
        products[i].style.display = "block";
      }

      document.getElementById("logout-button").style.display="block";
      document.getElementById("login-button").style.display="none";
      document.getElementById("account-nav-item").style.display = "block";
      user.getIdToken().then(function (token) {
        document.cookie = "token=" + token;
      });
    }
    // Signed Out
    else {
      // Initialize the FirebaseUI Widget using Firebase.
      var ui = new firebaseui.auth.AuthUI(firebase.auth());
      // Show the Firebase login button.
      document.getElementById("logout-button").style.display="none";
      document.getElementById("account-nav-item").style.display = "none";
      ui.start('#firebaseui-auth-container', uiConfig);

      document.cookie = "token=";
    }
  }, function (error) {
    console.warn(error);
    alert('Unable to log in: ' + error)
  });
});
