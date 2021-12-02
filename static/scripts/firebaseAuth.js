'use strict';

window.addEventListener('load', function () {
  document.getElementById('logout-button').onclick = function () {
    firebase.auth().signOut();
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
    // Signed In
    if (user) {
      document.getElementById("logout-button").style.display="block";
      document.getElementById("login-button").style.display="none";
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
      ui.start('#firebaseui-auth-container', uiConfig);

      document.cookie = "token=";
    }
  }, function (error) {
    console.log(error);
    alert('Unable to log in: ' + error)
  });
});
