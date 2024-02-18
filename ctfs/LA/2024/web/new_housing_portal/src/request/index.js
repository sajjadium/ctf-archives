const $ = q => document.querySelector(q);
const $all = q => document.querySelectorAll(q);

(async () => {
  const { invitations } = await fetch('/invitation').then(r => r.json());
  $('.invitations').innerHTML = invitations.map((inv) => `
    <div class="invitation">
      <div class="col">
        <div class="from">From: ${inv.from}</div>
        <div class="secret">Deepest Darkest Secret: ${inv.deepestDarkestSecret}</div>
      </div>
      <div class="col">
        <button>Accept</button>
      </div>
    </div>
  `).join('\n');

  $all('button').forEach((button) => {
    button.addEventListener('click', () => {
      alert('Sorry! The System is under load, cannot accept invite!');
    })
  });
})();
