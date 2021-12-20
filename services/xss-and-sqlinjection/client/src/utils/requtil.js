function popup(msg) {
  alert(msg);
}

function req(url, obj, workWithJson) {
  let fullURL = url;
  let first = true;
  for (let key in obj) {
    fullURL += (first ? '?' : '&') + key + '=' + window.encodeURIComponent(obj[key]);
    first = false;
  }
  fetch(fullURL)
    .then(resp => {
      if (resp.status != 200) {
        throw Error(resp.statusText);
      }
      return resp;
    })
    .then(resp => {
      return resp.json();
    })
    .then(data => {
      if (data.Error) {
        throw Error('Server error');
      }
      return data;
    })
    .then(workWithJson)
    .catch(er => {
      console.log(er);
      popup('Ошибка сервера');
    });
}

function reqPost(url, data, workWithJson, doAfterError, doNotShowError) {
  let fullURL = url;
  fetch(fullURL, {
    method: 'POST',
    body: JSON.stringify(data),
  }).catch(er => {
      throw Error('Check connection');
    })
    .then(resp => {
      if (resp.status != 200) {
        throw Error(resp.statusText);
      }
      return resp;
    })
    .then(resp => {
      return resp.json();
    })
    .then(workWithJson)
    .catch(er => {
      console.log(er);
      popup('Ошибка сервера');
    });
}

export {
  req,
  reqPost,
};