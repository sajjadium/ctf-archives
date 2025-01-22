import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const FLAG = process.env.FLAG || "uoftctf{FAKEFLAGFAKEFLAG}"

function generateString(length) {
    const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    const charactersLength = characters.length;
    for ( let i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    return result;
}

const USERS = [
    {
        name: "White",
        password: generateString(Math.floor(Math.random()*10)+15),
    },
    {
        name: "Bob",
        password: generateString(Math.floor(Math.random()*10)+15),
    },
    {
        name: "Tommy",
        password: generateString(Math.floor(Math.random()*10)+15),
    },
    {
        name: "Sam",
        password: generateString(Math.floor(Math.random()*10)+15),
    },
];

const NUM_USERS = USERS.length; 

// all chatGPT generated cause im lazy
const POSTS = [
    {
      title: `Why Cybersecurity is Everyone's Responsibility`,
      body: `In today's digital age, cybersecurity isn't just an IT concern—it's everyone's responsibility. From clicking suspicious links to using weak passwords, small mistakes can lead to big vulnerabilities. Simple habits like enabling two-factor authentication, updating software, and being mindful of phishing emails can protect not just yourself but your entire organization. Cybersecurity starts with awareness—how are you contributing to a safer digital world?`,
      authorId: Math.floor(Math.random()*NUM_USERS)+1,
      published: true
    },
    {
        title: `Boosting Productivity with Time Blocking`,
        body: `Struggling to get things done? Time blocking might be your answer. By dividing your day into focused chunks of work, you can minimize distractions and maximize efficiency. Start by identifying your most important tasks, assign specific time slots, and stick to them. Bonus tip: leave buffer time for unexpected interruptions. Time blocking isn’t just about scheduling—it’s about creating space for what truly matters.`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: true
    },
    {
        title: `3 Easy Tips to Save Energy at Home`,
        body: `Reducing your energy footprint doesn’t have to be complicated. Start small:

Switch to LED bulbs—they last longer and use less power.
Unplug electronics when not in use—they still draw power even when off.
Use a programmable thermostat to optimize heating and cooling.
These simple changes save money and help the planet—win-win!`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: true
    },
    {
        title: `How to Start Your Fitness Journey Today`,
        body: `Getting fit can feel overwhelming, but it doesn’t have to be. Start small: commit to a 10-minute walk daily or try a beginner-friendly workout video. Focus on consistency over intensity. Remember, progress takes time, so celebrate small wins along the way. Your future self will thank you for taking that first step today!`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: true
    },
    {
        title: `The Magic of Morning Routines`,
        body: `What do successful people have in common? A solid morning routine. Whether it’s journaling, meditating, or a quick workout, starting your day intentionally sets the tone for productivity and positivity. Don’t overthink it—pick one activity that energizes you and stick with it. Mornings are your power hour; how will you use yours?`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: true
    },
    {
        title: `5 Quick Ways to Declutter Your Space`,
        body: `A cluttered space can lead to a cluttered mind. Here’s how to simplify:

Apply the “one in, one out” rule for new purchases.
Dedicate 10 minutes a day to tidying up.
Donate items you haven’t used in a year.
Invest in smart storage solutions.
Remember: less is more.
Decluttering isn’t just about cleaning—it’s about creating a space that inspires calm and focus.`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: true
    },
    {
        title: `Why Soft Skills Are the Secret to Career Growth`,
        body: `Technical skills may get your foot in the door, but soft skills will take you further. Communication, adaptability, and emotional intelligence are increasingly valued in today’s workplace. Why? Because they foster collaboration and help you navigate challenges effectively. Want to stand out in your career? Work on your soft skills—they’re just as crucial as hard ones.`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: true
    },
    {
        title: `3 Reasons You Should Start Journaling`,
        body: `Feeling overwhelmed? Journaling might be the outlet you need. It helps you:

Clarify your thoughts and emotions.
Track personal growth and progress.
Spark creativity by putting ideas to paper.
You don’t need fancy notebooks or hours of time—just a few minutes a day can make a big difference. Start writing and see where it takes you!`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: true
    },
    {
        title: `How to Beat Procrastination for Good`,
        body: `Procrastination affects us all, but overcoming it is possible. Start by breaking tasks into smaller, manageable chunks. Use techniques like the Pomodoro timer to stay focused, and reward yourself for completing milestones. Most importantly, don’t aim for perfection—progress is what counts. The best time to start? Right now.`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: true
    },
    {
        title: `The Future of Remote Work`,
        body: `The shift to remote work has changed the way we view the workplace. Flexibility and work-life balance are now top priorities for employees, while companies are investing in tools to keep teams connected. But with this freedom comes challenges—like maintaining productivity and avoiding burnout. The future of work is hybrid, but how can we make it truly sustainable for everyone?`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: true
    },
    {
        title: `The Flag`,
        body: `This is a secret blog I am still working on. The secret keyword for this blog is ${FLAG}`,
        authorId: Math.floor(Math.random()*NUM_USERS)+1,
        published: false
    }
];

(async () => {
    await prisma.user.createMany({data: USERS});
    await prisma.post.createMany({data: POSTS});
  })();