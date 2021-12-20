import '../../utils/requtil.js';
import { req } from '../../utils/requtil.js';

function bid(id) {
  return document.getElementById(id);
}

const keyEl = bid('key');
const btnGetFlagEl = bid('btn-get-flag');
const resultEl = bid('flag_value');

btnGetFlagEl.addEventListener('click', ev => {
  ev.preventDefault();
  const key = keyEl.value;
  const url = `/api/get_flag`;
  req(url, {
    key: key,
  }, data => {
    if (typeof data.Value === 'string') {
      resultEl.innerHTML = data.Value;
      //resultEl.textContent = data.Value; // Secure
    } else if (data.NoFlag) {
      resultEl.textContent = 'Такого флага, к сожалению, нет =(';
    }
  });
});