import '../../utils/requtil.js';
import { req } from '../../utils/requtil.js';

function bid(id) {
  return document.getElementById(id);
}

const keyEl = bid('key');
const valueEl = bid('value');
const btnAddFlagEl = bid('btn-add-flag');

btnAddFlagEl.addEventListener('click', ev => {
  ev.preventDefault();
  const key = keyEl.value;
  const value = valueEl.value;
  const url = `/api/add_flag`;
  req(url, {
    key: key,
    value: value,
  }, data => {
    if (data.Success) {
      alert('Флаг успешно добавлен!');
    } else {
      alert('Флаг не удалось добавить =(');
    }
  });
});
