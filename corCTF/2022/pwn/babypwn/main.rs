use libc;
use libc_stdhandle;

fn main() {
    unsafe {
        libc::setvbuf(libc_stdhandle::stdout(), &mut 0, libc::_IONBF, 0);

        libc::printf("Hello, world!\n\0".as_ptr() as *const libc::c_char);
        libc::printf("What is your name?\n\0".as_ptr() as *const libc::c_char);

        let text = [0 as libc::c_char; 64].as_mut_ptr();
        libc::fgets(text, 64, libc_stdhandle::stdin());
        libc::printf("Hi, \0".as_ptr() as *const libc::c_char);
        libc::printf(text);

        libc::printf("What's your favorite :msfrog: emote?\n\0".as_ptr() as *const libc::c_char);
        libc::fgets(text, 128, libc_stdhandle::stdin());
        
        libc::printf(format!("{}\n\0", r#"
          .......           ...----.
        .-+++++++&&&+++--.--++++&&&&&&++.
       +++++++++++++&&&&&&&&&&&&&&++-+++&+
      +---+&&&&&&&@&+&&&&&&&&&&&++-+&&&+&+-
     -+-+&&+-..--.-&++&&&&&&&&&++-+&&-. ....
    -+--+&+       .&&+&&&&&&&&&+--+&+... ..
   -++-.+&&&+----+&&-+&&&&&&&&&+--+&&&&&&+.
 .+++++---+&&&&&&&+-+&&&&&&&&&&&+---++++--
.++++++++---------+&&&&&&&&&&&&@&&++--+++&+
-+++&&&&&&&++++&&&&&&&&+++&&&+-+&&&&&&&&&&+-
.++&&++&&&&&&&&&&&&&&&&&++&&&&++&&&&&&&&+++-
 -++&+&+++++&&&&&&&&&&&&&&&&&&&&&&&&+++++&&
  -+&&&@&&&++++++++++&&&&&&&&&&&++++++&@@&
   -+&&&@@@@@&&&+++++++++++++++++&&&@@@@+
    .+&&&@@@@@@@@@@@&&&&&&&@@@@@@@@@@@&-
      .+&&@@@@@@@@@@@@@@@@@@@@@@@@@@@+
        .+&&&@@@@@@@@@@@@@@@@@@@@@&+.
          .-&&&&@@@@@@@@@@@@@@@&&-
             .-+&&&&&&&&&&&&&+-.
                 ..--++++--."#).as_ptr() as *const libc::c_char);
    }
}