pub const INTRO: &str = "\n\
    You land your spaceship on one of the most brightly lit planets in the universe. \
    As you get out of your spaceship, in your earpiece, a cheerful robotic voice starts to speak.\n\
    \n\
    Welcome to Proxima Concursus!\
    \n";

pub const CHOICE: &str = "\
    What do you want to do?\n\
    \n\
    \t0) I'm here on a vacation to see the sights\n\
    \t1) Where's the signup for The Game?\n\
    \t2) I'm a scientist, here to use the particle collider\n\
    \t3) Wait, I wanted to go to Extremos Concursus...\n\
    ";

pub const GOODBYE: &str = "\
    Ah, that's on the other side of the universe. \
    You should've taken a left turn, not a right turn.\
    \n";

pub fn sleep() {
    std::thread::sleep(std::time::Duration::from_secs_f64(0.5));
}

pub fn print_messages_with_sleep(messages: &[&str]) {
    println!();
    for msg in messages {
        sleep();
        println!("{}", msg);
    }
}

pub fn exit_with<S: std::fmt::Display>(x: S) -> ! {
    print_messages_with_sleep(&[
        "A loud repeating sound plays...",
        "The sky grows bright",
        "In front of your eyes, the following message appears:",
        "",
        &format!("\t\t{}", x),
        "",
        "You suddenly wake up with a jolt.",
        "",
        "Your alarm is ringing, and you're late for your meeting.",
        "",
        "'That was a weird dream...' you think.",
        "",
    ]);
    std::process::exit(1)
}

pub fn desync() {
    print_messages_with_sleep(&[
        "Oh no!",
        "What did you do?!",
        "Looks like the whole universe is dissolving a..ww...aaa...yyy........",
        "...",
        ".",
        "...",
        "Wait, did you feel that too?",
        "Must've just been the wind.",
        "",
        "Where was I? Oh yes!",
        "",
    ]);
}

pub mod observe {
    pub const INTRO: &str = "Awesome! There's quite a lot to see here. For example, do you see that red machine there? \
                             We call it the Digester. \
                             You can send any signal into it and it digests it. \
                             Try it out! \
                             Send it an input.";
    pub const RESULT: &str = "Instantly, out popped out: ";
}

pub mod the_game {
    pub const INTRO: &str = "Great! \
                             We were just about to begin this year's tournament. You're right on time.\n\
                             This year's variant of The Game is to double-digest Connect 4. \
                             I assume you know how to play Connect 4.\n\
                             Our grid here is 10x8 in size.\n\
                             \n\
                             As a reminder, the objective is to play two games of Connect 4 which digest the same way.\
                             \n\
                             Good luck!\n";
}

pub mod particle_collider {
    pub const INTRO: &str = "Ooh! Wait, you must be Professor Falcon. We've been waiting for you. \
                             The particle collider we built is based off of one of your earlier designs.\n\
                             \n\
                             We have increased the power output in hopes of finding the elusive `inflaton` particle, \
                             but it has evaded detection. \
                             Maybe you can find what we couldn't? \
                             \n\n\
                             The theory predicts that the `inflaton` only appears in the presence of 3 other particles, \
                             and only when their relative velocities are just perfect. However, we haven't yet \
                             been able to figure out which particles, or how to properly get the velocities to align. \
                             \n\n\
                             Maybe you'll have better luck tuning the machine?\n";
    pub const EXPERIMENT_SETUP: &str = "\n\
                                        Interesting! \
                                        We hadn't tried that combination before. Let's give it a shot!";
}
