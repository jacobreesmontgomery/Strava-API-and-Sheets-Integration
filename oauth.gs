var CLIENT_ID = '83199';
var CLIENT_SECRET = '4d662f26d0a43fb69c2ab52e7838cc7c31736879';

// configure the service
function getStravaService() {
  return OAuth2.createService('Strava')
    .setAuthorizationBaseUrl('https://www.strava.com/oauth/authorize')
    .setTokenUrl('https://www.strava.com/oauth/token')
    .setClientId(CLIENT_ID)
    .setClientSecret(CLIENT_SECRET)
    .setCallbackFunction('authCallback')
    .setPropertyStore(PropertiesService.getUserProperties())
    .setScope('activity:read_all');
}

// handle the callback
function authCallback(request) {
  var stravaService = getStravaService();
  var isAuthorized = stravaService.handleCallback(request);
  if (isAuthorized) {
    return HtmlService.createHtmlOutput('Success! You can close this tab.');
  } else {
    return HtmlService.createHtmlOutput('Denied. You can close this tab');
  }
}

// configure the webhook
function getWebhookSubscription() {
  var callbackUrl = 'script.google.com';
  var postLink = `https://www.strava.com/api/v3/push_subscriptions?client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&callback_url=${callbackUrl}&verify_token=STRAVA`;
  console.log(postLink);

  // this will have to be investigated further. for now, might just skip past this and work on getting cool views on athlete data
}




