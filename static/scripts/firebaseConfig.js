  const firebaseConfig = {
    apiKey: "AIzaSyAb7SXWBnjP1oAbHZOyaBoxC0YJf40nVok",
    authDomain: "ad-assignment-334817.firebaseapp.com",
    projectId: "ad-assignment-334817",
    storageBucket: "ad-assignment-334817.appspot.com",
    messagingSenderId: "517026741602",
    appId: "1:517026741602:web:9874ef1e41f5d8806c003b",
    measurementId: "${config.measurementId}"
  };
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
