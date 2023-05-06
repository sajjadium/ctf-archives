const Discord = require('discord.js');
const client = new Discord.Client();

const { submitForm, downloadFile } = require('./util.js');

const transition = new Map();
transition.set('start', {
  message: null,
  handle: () => ['username', []],
});

transition.set('username', {
  message: 'Please enter a username for your account.',
  handle: (message, data) => {
    const content = message.content;
    if (content.length < 4) {
      message.channel.send('Username too short!');
      return ['username', data];
    }
    // I forgot about regex, which is ironic given that
    // this is some sort of state machine
    const allowed = new Set(
      'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
    );
    for (const character of content) {
      if (!allowed.has(character)) {
        message.channel.send(
          'Username can only contain alphanumeric characters'
        );
        return ['username', data];
      }
    }
    return ['password', [...data, [{ name: 'username' }, content]]];
  },
});

transition.set('password', {
  message: 'Please enter a password for your account.',
  handle: (message, data) => [
    'bio',
    [...data, [{ name: 'password' }, message.content]],
  ],
});

transition.set('bio', {
  message: 'Please write a bio for your account.',
  handle: (message, data) => {
    const content = message.content;
    if (content.length > 200) {
      message.channel.send('Bio too long!');
      return ['bio', data];
    }
    return ['picture', [...data, [{ name: 'bio' }, content]]];
  },
});

transition.set('picture', {
  message: 'Please upload a picture or send an image URL. (png, <100kb)',
  handle: async (message, data) => {
    const attachment = message.attachments.first();
    if (attachment) {
      const picture = await downloadFile(attachment.url);
      return [
        'end',
        [...data, [{ name: 'picture', filename: 'picture.png' }, picture]],
      ];
    }
    try {
      const { protocol, hostname, pathname, search } = new URL(message.content);
      return [
        'end',
        [
          ...data,
          [
            { name: 'picture' },
            JSON.stringify({
              protocol,
              host: hostname,
              path: pathname,
              search,
            }),
          ],
        ],
      ];
    } catch {
      message.channel.send('Invalid URL.');
      return ['picture', data];
    }
  },
});

// uid -> [ state, data ]
const states = new Map();

client.on('message', async (message) => {
  const channel = message.channel;
  if (channel.type !== 'dm') return;
  const id = message.author.id;
  const content = message.content;
  if (!states.has(id)) {
    if (content === 'Create Account') states.set(id, ['start', {}]);
    else return;
  }

  // handle current state and move to next
  const [state, data] = states.get(id);
  const { handle } = transition.get(state);
  const [nextState, newData] = await handle(message, data);

  if (nextState === 'end') {
    try {
      submitForm(newData);
      states.delete(id);
      channel.send(
        'Request sent. If account is not created, make sure that username ' +
          'is not already taken and profile picture has proper size and format.'
      );
    } catch {
      channel.send('Account creation failed.');
    }
    return;
  }

  states.set(id, [nextState, newData]);

  channel.send(transition.get(nextState).message);
});

client.login(process.env.TOKEN);
