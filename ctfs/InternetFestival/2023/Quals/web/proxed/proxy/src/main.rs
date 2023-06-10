mod http;
mod queue;
mod webapp;

use std::io::Write;
use std::net::{TcpListener, TcpStream};
use std::sync::Arc;
use std::thread;

fn main() {
    // Open socket
    let listener = TcpListener::bind("0.0.0.0:8000").unwrap();

    // Create requests queue
    let incoming_queue: Arc<queue::BlockingQueue<String>> = Arc::new(queue::BlockingQueue::new());
    let outgoing_queue: Arc<queue::BlockingQueue<String>> = Arc::new(queue::BlockingQueue::new());
    let stream_queue: Arc<queue::BlockingQueue<TcpStream>> = Arc::new(queue::BlockingQueue::new());

    // Spawn request handler thread
    let webapp_incoming_queue = incoming_queue.clone();
    let webapp_outgoing_queue = outgoing_queue.clone();
    thread::spawn(move || {
        webapp::start(webapp_incoming_queue, webapp_outgoing_queue);
    });

    /*
       Proxy listener
       - accept connection
       - get request
       - enqueue request
    */
    let listener_stream_queue = Arc::clone(&stream_queue);
    let listener_thread = thread::spawn(move || {
        for stream in listener.incoming() {
            // Get incoming connection
            let mut stream: TcpStream = match stream {
                Ok(x) => x,
                Err(_x) => break,
            };

            let listener_rt = Arc::clone(&incoming_queue);
            let listener_stream_queue = Arc::clone(&listener_stream_queue);

            thread::spawn(move || {
                println!("New connection from {}", stream.peer_addr().unwrap());
                // Parse request
                match http::get_request(&mut stream) {
                    Err(x) => {
                        eprintln!("Error in request decoding: {}", x);
                    }
                    Ok(req) => {
                        listener_rt.push(req.to_string());
                        listener_stream_queue.push(stream);
                    }
                }
            });
        }
    });

    /*
       Proxy responder
       - dequeue response
       - send response
    */
    let responder = thread::spawn(move || loop {
        let resp = outgoing_queue.pop();
        let mut stream = stream_queue.pop();
        match stream.write(resp.as_bytes()){
            Err(x)=>{
                eprintln!("Error in response send: {}", x)
            },
            _=>{}
        };
    });

    listener_thread.join().expect("Boh");
    responder.join().expect("Boh");
}
