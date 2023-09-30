use std::{error::Error, io, time::Duration, fs::File};
use rand::seq::SliceRandom;

use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode, KeyEventKind},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
    tty::IsTty,
};
use ratatui::{prelude::*, widgets::*};
use chrono::{DateTime, Utc};

use chat_common::{Message, ChatMessage, Reaction, ReactionType, NUM_REACTIONS};
use std::sync::mpsc::{Receiver, Sender};
use std::collections::VecDeque;

const USERNAMES : [&str; 3] = [
    "hacker",
    "hax0r",
    "l33t",
];

const REACTIONS : [(&str, ReactionType); 5] = [
    ("+1", chat_common::ReactionType::Like),
    ("♡", chat_common::ReactionType::Love),
    ("LOL", chat_common::ReactionType::Haha),
    ("😲", chat_common::ReactionType::Wow),
    ("pepega", chat_common::ReactionType::Pepega),
];

const MAX_MESSAGES: usize = 50;

#[derive(Copy, Clone, PartialEq)]
enum InputMode {
    Normal,
    Editing,
    Reacting(usize), // selected react
}

/// App holds the state of the application
struct App {
    /// Current value of the input box
    input: String,
    /// Position of cursor in the editor area.
    cursor_position: usize,
    /// Current input mode
    input_mode: InputMode,
    /// History of recorded messages
    messages: VecDeque<Message>,
    /// Selected message
    selected_message: Option<usize>,
    /// Super messages
    is_super_message: bool,
    /// Send queue
    send_queue: Sender<Message>,
    /// Username
    username: String,
}

impl App {
    fn new_with_send_queue(send_queue: Sender<Message>) -> App {
        App {
            input: String::new(),
            input_mode: InputMode::Editing,
            messages: VecDeque::with_capacity(MAX_MESSAGES),
            cursor_position: 0,
            selected_message: None,
            is_super_message: false,
            username: USERNAMES.choose(&mut rand::thread_rng()).unwrap().to_string(),
            send_queue,
        }
    }
    fn move_cursor_left(&mut self) {
        let cursor_moved_left = self.cursor_position.saturating_sub(1);
        self.cursor_position = self.clamp_cursor(cursor_moved_left);
    }

    fn move_cursor_right(&mut self) {
        let cursor_moved_right = self.cursor_position.saturating_add(1);
        self.cursor_position = self.clamp_cursor(cursor_moved_right);
    }

    fn enter_char(&mut self, new_char: char) {
        self.input.insert(self.cursor_position, new_char);

        self.move_cursor_right();
    }

    fn delete_char(&mut self) {
        let is_not_cursor_leftmost = self.cursor_position != 0;
        if is_not_cursor_leftmost {
            // Method "remove" is not used on the saved text for deleting the selected char.
            // Reason: Using remove on String works on bytes instead of the chars.
            // Using remove would require special care because of char boundaries.

            let current_index = self.cursor_position;
            let from_left_to_current_index = current_index - 1;

            // Getting all characters before the selected character.
            let before_char_to_delete = self.input.chars().take(from_left_to_current_index);
            // Getting all characters after selected character.
            let after_char_to_delete = self.input.chars().skip(current_index);

            // Put all characters together except the selected one.
            // By leaving the selected one out, it is forgotten and therefore deleted.
            self.input = before_char_to_delete.chain(after_char_to_delete).collect();
            self.move_cursor_left();
        }
    }

    fn clamp_cursor(&self, new_cursor_pos: usize) -> usize {
        new_cursor_pos.clamp(0, self.input.len())
    }

    fn reset_cursor(&mut self) {
        self.cursor_position = 0;
    }

    fn submit_message(&mut self) {
        self.send_queue.send(Message::Chat(ChatMessage {
            id: rand::random(),
            author: self.username.clone(),
            content: self.input.clone(),
            is_super: self.is_super_message,
            timestamp: chrono::Utc::now().timestamp(),
        }));

        self.is_super_message = false;
        self.input.clear();
        self.reset_cursor();
    }

    fn submit_react(&mut self) {
        if let InputMode::Reacting(r) = self.input_mode {
            self.send_queue.send(Message::React(Reaction {
                target_id: self.selected_message.unwrap(),
                author: self.username.clone(),
                reaction_type: REACTIONS[r].1,
                timestamp: chrono::Utc::now().timestamp(),
            }));
            self.input_mode = InputMode::Normal;
        }
    }
}

pub async fn tui_main() -> Result<(), Box<dyn Error>> {
    // setup terminal
    let mut stdout = io::stdout();
    let mut is_tty = stdout.is_tty();

    if is_tty {
        enable_raw_mode()?;
        execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
    }

    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    // setup client
    let server = std::env::args().nth(1).unwrap();
    let (recv_queue, send_queue) = chat_common::comms::start_client(server).await;

    // create app and run it
    let app = App::new_with_send_queue(send_queue);
    let res = run_app(&mut terminal, app, recv_queue, is_tty);

    // restore terminal
    if is_tty {
        disable_raw_mode()?;
        execute!(
            terminal.backend_mut(),
            LeaveAlternateScreen,
            DisableMouseCapture
        )?;
        terminal.show_cursor()?;
    }

    if let Err(err) = res {
        println!("{err:?}");
    }

    Ok(())
}

fn handle_updown_react<B: Backend>(terminal: &mut Terminal<B>, app: &mut App, event: event::KeyEvent) {
    app.input_mode = match (event.code, app.input_mode) {
        (KeyCode::Down, InputMode::Reacting(x)) if x < NUM_REACTIONS => { InputMode::Reacting(x + 1) }
        (KeyCode::Up, InputMode::Reacting(x)) if x > 0 => { InputMode::Reacting(x - 1) }
        _ => app.input_mode,
    }

}
fn handle_updown_editor<B: Backend>(terminal: &mut Terminal<B>, app: &mut App, event: event::KeyEvent) {
    match event.code {
        KeyCode::Down => {
            // Highlight the next message, or move to the input box if on the edge
            match app.selected_message {
                Some(x) if app.messages.len() > 0 && x < app.messages.len() - 1 => {
                    app.selected_message = Some(x + 1);
                    app.input_mode = InputMode::Normal;
                }
                None if app.messages.len() > 0 => {
                    app.selected_message = Some(0);
                    app.input_mode = InputMode::Normal;
                }
                _ => {
                    app.selected_message = None;
                    app.input_mode = InputMode::Editing;
                }
            }
        }
        KeyCode::Up => {
            // Highlight the previous message, or move to the input box if on the edge
            match app.selected_message {
                Some(x) if x > 0 => {
                    app.selected_message = Some(x - 1);
                    app.input_mode = InputMode::Normal;
                }
                None if app.messages.len() > 0 => {
                    app.selected_message = Some(app.messages.len() - 1);
                    app.input_mode = InputMode::Normal;
                }
                _ => {
                    app.selected_message = None;
                    app.input_mode = InputMode::Editing;
                }
            }
        }
        _ => {}
    }
}

fn run_app<B: Backend>(terminal: &mut Terminal<B>, mut app: App, mut queue: Receiver<Message>, is_tty: bool) -> io::Result<()> {
    app.send_queue.send(Message::Join(app.username.clone())).unwrap();
    loop {
        terminal.draw(|f| ui(f, &app))?;

        for m in queue.try_iter() {
            match m {
                Message::Chat(_) | Message::Join(_) | Message::React(_) | Message::FriendRequest(_, _) => {
                    if app.messages.len() + 1 > MAX_MESSAGES {
                        app.messages.pop_front();
                    }
                    match m {
                        Message::Join(ref name) if *name != app.username => {
                            app.send_queue.send(Message::FriendRequest(app.username.clone(), name.clone())).unwrap();
                        }
                        _ => {}
                    }
                    app.messages.push_back(m);
                }
                Message::Ping(data, needs_response) => {
                    if needs_response {
                        app.send_queue.send(Message::Ping(data, false)).unwrap();
                    }
                }
                _ => {}
            }

        }

        if !is_tty {
            std::thread::sleep(Duration::from_millis(250));
            continue;
        }

        if !event::poll(Duration::from_millis(250))? { continue; }
        if let Event::Key(key) = event::read()? {
            // Handle up/down
            match app.input_mode {
                InputMode::Normal | InputMode::Editing => handle_updown_editor(terminal, &mut app, key),
                InputMode::Reacting(_) => handle_updown_react(terminal, &mut app, key),
            }

            // Handle other keys
            match app.input_mode {
                InputMode::Normal => match key.code {
                    KeyCode::Char('r') if app.selected_message.is_some() => {
                        app.input_mode = InputMode::Reacting(0);
                    }
                    KeyCode::Char('q') => {
                        return Ok(());
                    }
                    _ => {}
                },
                InputMode::Editing if key.kind == KeyEventKind::Press => match key.code {
                    KeyCode::Enter => app.submit_message(),
                    KeyCode::Char(to_insert) => {
                        app.enter_char(to_insert);
                    }
                    KeyCode::Backspace => {
                        app.delete_char();
                    }
                    KeyCode::Left => {
                        app.move_cursor_left();
                    }
                    KeyCode::Right => {
                        app.move_cursor_right();
                    }
                    KeyCode::Esc => {
                        app.input_mode = InputMode::Normal;
                    }
                    KeyCode::Tab => {
                        app.is_super_message = !app.is_super_message;
                    }
                    _ => {}
                },
                InputMode::Reacting(_) if key.kind == KeyEventKind::Press => match key.code {
                    KeyCode::Enter => app.submit_react(),
                    KeyCode::Esc => {
                        app.input_mode = InputMode::Normal;
                    }
                    _ => {}
                },
                _ => {}
            }
        }
    }
}

fn ui<B: Backend>(f: &mut Frame<B>, app: &App) {
    let full_layout = Layout::default()
        .direction(Direction::Horizontal)
        .constraints(match app.input_mode {
            InputMode::Reacting(_) => Vec::from([
                Constraint::Min(0),
                Constraint::Length(20),
            ]),
            _ => Vec::from([
                Constraint::Min(0),
            ]),
        })
        .split(f.size());
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints(
            [
                Constraint::Length(1),
                Constraint::Min(0),
                Constraint::Length(3),
            ]
            .as_ref(),
        )
        .split(full_layout[0]);

    let (msg, style) = match app.input_mode {
        InputMode::Normal => (
            vec![
                "Press ".into(),
                "q".bold(),
                " to exit, ".into(),
                "r".bold(),
                " to react.".bold(),
            ],
            Style::default().add_modifier(Modifier::RAPID_BLINK),
        ),
        InputMode::Reacting(_) => (
            vec![
                "Press ".into(),
                "Enter".bold(),
                " to react, ".into(),
                "ESC".bold(),
                " to cancel, ".into(),
            ],
            Style::default().add_modifier(Modifier::RAPID_BLINK),
        ),
        InputMode::Editing => (
            vec![
                "Press ".into(),
                "Esc".bold(),
                " to stop editing, ".into(),
                "TAB".bold(),
                " to make this message 'super', ".into(),
                "Enter".bold(),
                " to send the message".into(),
            ],
            Style::default(),
        ),
    };
    let mut text = Text::from(Line::from(msg));
    text.patch_style(style);
    let help_message = Paragraph::new(text);
    f.render_widget(help_message, chunks[0]);

    let input = Paragraph::new(app.input.as_str())
        .style(match app.input_mode {
            InputMode::Normal | InputMode::Reacting(_) => Style::default(),
            InputMode::Editing if app.is_super_message => Style::default().fg(Color::Green),
            InputMode::Editing => Style::default().fg(Color::Yellow),
        })
        .block({
            let s = if app.is_super_message { " (SUPER)" } else { "" };
            Block::default().borders(Borders::ALL).title(format!("Send Message{}", s))
        });
    f.render_widget(input, chunks[2]);
    match app.input_mode {
        InputMode::Normal | InputMode::Reacting(_) =>
            // Hide the cursor.
            {}

        InputMode::Editing => {
            // Make the cursor visible and ask ratatui to put it at the specified coordinates after
            // rendering
            f.set_cursor(
                // Draw the cursor at the current position in the input field.
                // This position is can be controlled via the left and right arrow key
                chunks[2].x + app.cursor_position as u16 + 1,
                // Move one line down, from the border to the input line
                chunks[2].y + 1,
            )
        }
    }

    let messages: Vec<ListItem> = app
        .messages
        .iter()
        .enumerate()
        .filter_map(|(i, m)| {
            let mut content = match m {
                Message::Chat(m) => {
                    // display time and author
                    let local_date = DateTime::<Utc>::from_timestamp(m.timestamp, 0)?.with_timezone(&chrono::Local);
                    let mut content = Line::from(Span::raw(format!("[{}] ", local_date.format("%H:%M:%S"))));
                    content.patch_style(Style::default().fg(Color::White));

                    let mut content2 = Span::raw(format!("{}: ", m.author));
                    content2.patch_style(Style::default().fg(Color::Magenta));

                    let mut body = Span::raw(m.content.clone());
                    if m.is_super {
                        body.patch_style(Style::default().fg(Color::Green));
                    }
                    content.spans.append(&mut [content2, body].to_vec());
                    content
                }
                Message::Join(m) => {
                    let mut content = Line::from(Span::raw(format!("{} joined", m)));
                    content.patch_style(Style::default().fg(Color::Green));
                    content
                }
                Message::FriendRequest(from, to) => {
                    if to == &app.username {
                        let mut content = Line::from(Span::raw(format!("{} requested to be your friend!", from)));
                        content.patch_style(Style::default().fg(Color::Green));
                        content
                    } else {
                        return None;
                    }
                }
                Message::React(m) => {
                    let local_date = DateTime::<Utc>::from_timestamp(m.timestamp, 0)?.with_timezone(&chrono::Local);

                    let mut date_content = Line::from(Span::raw(format!("[{}] ", local_date.format("%H:%M:%S"))));
                    date_content.patch_style(Style::default().fg(Color::White));

                    let mut content = Span::raw(format!("{} reacted with {}", m.author, REACTIONS.iter().find(|(_, x)| *x == m.reaction_type).unwrap().0));
                    content.patch_style(Style::default().fg(Color::Blue));

                    date_content.spans.append(&mut [content].to_vec());
                    date_content
                }
                _ => return None,
            };
            if Some(i) == app.selected_message {
                Some(match app.input_mode {
                    InputMode::Normal | InputMode::Editing => {
                        ListItem::new(content).style(Style::default().fg(Color::Black).bg(Color::White))
                    }
                    InputMode::Reacting(_) => {
                        content.patch_style(Style::default().fg(Color::Yellow));
                        ListItem::new(content)
                    }
                })
            } else {
                Some(ListItem::new(content))
            }
        })
        .collect();
    let messages =
        List::new(messages).block(Block::default().borders(Borders::ALL).title("Chat"));
    f.render_widget(messages, chunks[1]);

    match app.input_mode {
        InputMode::Reacting(x) => {
            let reactions: Vec<ListItem> = REACTIONS.iter().enumerate().map(|(i, (s, _))| {
                    let content = Line::from(Span::raw(format!("{}", s)));
                    if i == x {
                        ListItem::new(content).style(Style::default().fg(Color::Black).bg(Color::White))
                    } else {
                        ListItem::new(content)
                    }
                })
                .collect();
            let reactions =
                List::new(reactions).block(Block::default().borders(Borders::ALL).title("Reactions"));
            f.render_widget(reactions, full_layout[1]);
        }
        _ => {}
    }
}
