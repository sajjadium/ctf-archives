'use strict';

let lights = false;

const fetchAttribute = () => {
  fetch('/enabledAttributes')
    .then(async (res) => {
      const enabledAttributes = await res.json();

      if (enabledAttributes?.lights?.on) {
        lights = true;
        root.render(genContainer());
      } else {
        lights = false;
        root.render(genContainer());
      }
    })
    .catch(() => {
      console.log('Error fetching server data');
    });
};

fetchAttribute();

const genLoginLink = () => {
  return React.createElement(
    'a',
    { href: '/login.html', className: 'login-link' },
    'Login',
  );
};

const genSignupLink = () => {
  return React.createElement(
    'a',
    { href: '/signup.html', className: 'signup-link' },
    'Signup',
  );
};

const genLogoutLink = () => {
  return React.createElement(
    'a',
    { href: '/logout.html', className: 'logout-link' },
    'Logout',
  );
};

const genLights = () => {
  return React.createElement(
    'svg',
    {
      xmlns: 'http://www.w3.org/2000/svg',
      className: 'icon icon-tabler icon-tabler-traffic-lights',
      width: '240',
      height: '240',
      viewBox: '0 0 24 24',
      strokeWidth: '2',
      stroke: 'currentColor',
      fill: 'none',
      strokeLinecap: 'round',
      strokeLinejoin: 'round',
    },
    React.createElement('path', {
      stroke: 'none',
      d: 'M0 0h24v24H0z',
      fill: 'none',
      strokeWidth: '2',
    }),
    React.createElement('path', {
      d: 'M7 2m0 5a5 5 0 0 1 5 -5h0a5 5 0 0 1 5 5v10a5 5 0 0 1 -5 5h0a5 5 0 0 1 -5 -5z',
    }),
    React.createElement('path', {
      d: 'M12 7m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0',
      stroke: lights ? 'red' : 'black',
    }),
    React.createElement('path', {
      d: 'M12 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0',
      stroke: lights ? 'orange' : 'black',
    }),
    React.createElement('path', {
      d: 'M12 17m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0',
      stroke: lights ? 'green' : 'black',
    }),
  );
};

const genOnButton = () => {
  return React.createElement(
    'button',
    {
      className: 'onBtn',
      onClick: async () => {
        await fetch(
          `/enableAttribute?` +
            new URLSearchParams({
              attribute: 'lights',
              value: 'on',
            }),
        );

        fetchAttribute();
      },
    },
    'Turn On',
  );
};

const genOffButton = () => {
  return React.createElement(
    'button',
    {
      className: 'offBtn',
      onClick: async () => {
        await fetch(
          `/disableAttribute?` +
            new URLSearchParams({
              attribute: 'lights',
              value: 'on',
            }),
        );

        fetchAttribute();
      },
    },
    'Turn Off',
  );
};

const genContainer = () => {
  const isAuthorized = !!localStorage.getItem('authorization');
  console.log('isAuthorized: ', isAuthorized);
  return React.createElement(
    'div',
    {
      className: 'container',
    },
    React.createElement(
      'nav',
      {},
      !isAuthorized && genLoginLink(),
      !isAuthorized && genSignupLink(),
      isAuthorized && genLogoutLink(),
    ),
    isAuthorized &&
      React.createElement(
        'div',
        {
          className: 'centered',
        },
        genOnButton(),
        genLights(),
        genOffButton(),
      ),
  );
};

const domContainer = document.querySelector('#app');
const root = ReactDOM.createRoot(domContainer);

root.render(genContainer());
