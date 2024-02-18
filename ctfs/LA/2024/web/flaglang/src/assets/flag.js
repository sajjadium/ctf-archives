const $ = (...args) => document.querySelectorAll(...args);
const H = (...args) => document.createElement(...args);

// add each country to each select menu
$('select').forEach(select => {
  for (const country of countries) {
    const option = H('option');
    option.value = country;
    option.textContent = country;
    select.appendChild(option);
  }
});

// set value of my country select to what cookies say
const myName = $('.your-flag .name')[0].textContent;
$('.your-flag select')[0].value = myName;
$('.your-flag select')[0].addEventListener('change', (e) => {
  const newName = e.target.value;
  location.href = '/switch?to=' + encodeURIComponent(newName);
});

// set my flag
const myISO = $('.iso')[0].textContent;
const flagSrc = iso => `https://flagpedia.net/data/flags/w1160/${iso.toLowerCase()}.webp`;
$('.your-flag img')[0].src = flagSrc(myISO);

// set value of country we are viewing
$('.other-flag select')[0].addEventListener('change', async (e) => {
  const newCountry = e.target.value;
  const resp = await fetch('/view?country=' + encodeURIComponent(newCountry))
    .then(r => r.json());
  if ('err' in resp) {
    $('.error')[0].style.display = 'block';
    $('.error')[0].textContent = resp.err;
  }
  else {
    $('.error')[0].style.display = 'none';
    $('.other-flag span')[0].textContent = resp.msg;
    $('.other-flag img')[0].src = flagSrc(resp.iso);
  }
});

$('.other-flag select')[0].value = myName;
$('.other-flag img')[0].src = flagSrc(myISO);
