var loggedIn;

function onAddToCart(productId) {
    if(loggedIn) {
      console.log("Added product " + productId);
      var qtyStr = document.getElementById('shopping-cart-quantity-text').textContent;
      var qty = parseInt(qtyStr) || 0;
      qty += 1;
      document.getElementById('shopping-cart-quantity-text').textContent = qty.toString();
    }
    else {

    }

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

  firebase.auth().onAuthStateChanged(function (user) {
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
        console.log(user.uid);
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
    console.log(error);
    alert('Unable to log in: ' + error)
  });
});
