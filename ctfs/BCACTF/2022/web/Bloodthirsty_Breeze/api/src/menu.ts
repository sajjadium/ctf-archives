import { MenuItem } from "./MenuItem";

const menu: MenuItem[] = [
  {
    name: 'Web Eggs',
    description: 'A delicious breakfast made with fresh XSS',
    price: '$2.99',
    imageURL:
        'https://images.pexels.com/photos/6958019/pexels-photo-6958019.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
  },
  {
    name: 'Flag',
    description: 'Join us in co-opting Pride Month for a quick buck!',
    price: '$1,999.99',
    imageURL: 'https://nyc3.digitaloceanspaces.com/bcactf/bcactf/bloodthirsty-breeze/pride.png',
  },
  {
    name: 'Crypto-Locker',
    description: 'Sink your teeth into these delicious ransomwares!',
    price: '1 BTC',
    imageURL:
        'https://images.pexels.com/photos/735911/pexels-photo-735911.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
  },
];

export default menu;