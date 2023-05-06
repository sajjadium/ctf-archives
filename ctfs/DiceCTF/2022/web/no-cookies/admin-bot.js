import flag from './flag.txt';

function sleep(time) {
  return new Promise((resolve) => {
    setTimeout(resolve, time);
  });
}

export default {
  id: 'no-cookies',
  name: 'no-cookies',
  urlRegex:
    /^https:\/\/no-cookies-[a-f0-9]{16}\.mc\.ax\/view\?id=[a-f0-9]{32}$/,
  timeout: 10000,
  extraFields: [
    {
      name: 'instance',
      displayName: 'Instance ID',
      placeholder: 'no-cookies-{THIS}.mc.ax',
      regex: '^[0-9a-f]{16}$',
    },
  ],
  handler: async (url, ctx, { instance }) => {
    const page = await ctx.newPage();

    const doLogin = async (username, password) => {
      return new Promise((resolve) => {
        page.once('dialog', (first) => {
          page.once('dialog', (second) => {
            second.accept(password);
          });
          first.accept(username);
          resolve();
        });
      });
    };

    // make an account
    const username = Array(32)
      .fill('')
      .map(() => Math.floor(Math.random() * 16).toString(16))
      .join('');
    const password = flag;

    const firstLogin = doLogin(username, password);

    try {
      page.goto(`https://no-cookies-${instance}.mc.ax/register`);
    } catch {}

    await firstLogin;

    await sleep(3000);

    // visit the note and log in
    const secondLogin = doLogin(username, password);

    try {
      page.goto(url);
    } catch {}

    await secondLogin;

    await sleep(3000);
  },
};
