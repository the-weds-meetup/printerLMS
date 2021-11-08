import axios from 'axios';

/**
 * Preloads each refresh with user credentials to prevent constant
 * refretch from the server
 * @returns Promise<void>
 */
export async function checkSessionToken() {
  // if credentials not found, redirect to login screen
  // if expired, redirect to login screen
  if (
    !window.localStorage.getItem('session_token') ||
    !window.localStorage.getItem('token_expiry') ||
    Date.now() >= parseInt(window.localStorage.getItem('token_expiry'))
  ) {
    window.localStorage.clear();
    window.sessionStorage.clear();
    window.location.replace('/login');
  }

  // check if learner credentials do not exist, fetch and cache
  if (
    !window.sessionStorage.getItem('learner_email') ||
    !window.sessionStorage.getItem('learner_fullname') ||
    !window.sessionStorage.getItem('learner_isAdmin')
  ) {
    await axios
      .post(process.env.VUE_APP_BACKEND + '/api/learner', {
        token: window.localStorage.getItem('session_token'),
      })
      .then((response) => {
        const learner = response.data.result.records[0];
        window.sessionStorage.setItem('learner_fullname', learner.full_name);
        window.sessionStorage.setItem('learner_email', learner.email);
        window.sessionStorage.setItem('learner_isAdmin', learner.is_admin);
      })
      .catch((error) => {
        console.error(error.response.data.result.message);
      });
  }
}

export async function cleanupSession() {
  await axios
    .post(process.env.VUE_APP_BACKEND + '/api/auth/logout', {
      token: window.localStorage.getItem('session_token'),
    })
    .catch((error) => {
      console.error(error.response.data.result.message);
    })
    .then(() => {
      // remove everything
      window.localStorage.clear();
      window.sessionStorage.clear();
      // navigate to login after 3 secs
      setTimeout(function () {
        window.location.replace('/login');
      }, 3000);
    });
}
