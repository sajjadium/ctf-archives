use poc_framework_osec::{
  solana_sdk::signature::{
    Keypair,
    Signer,
  },
  Environment,
};

use sol_ctf_framework::ChallengeBuilder;

use solana_program::system_program;

use std::{
  io::Write,
  error::Error,
  net::{
    TcpListener,
    TcpStream
  },
  env,
};

use threadpool::ThreadPool;

use solidarity::{
  initialize, propose, vote
};

fn main() -> Result<(), Box<dyn Error>> {
  let listener = TcpListener::bind("0.0.0.0:5000")?;
  let pool = ThreadPool::new(4);
  for stream in listener.incoming() {
    let stream = stream.unwrap();

    pool.execute(|| {
      handle_connection(stream).unwrap();
    });
  }
  Ok(())
}

fn handle_connection(mut socket: TcpStream) -> Result<(), Box<dyn Error>> {
  writeln!(socket, "solidarity")?;
  writeln!(socket, r#"                                            
                                 &@%                                            
                             #@@@@@@@@@*                                        
                         #@@@@@@@   %@@@@@@@@,                                  
                   .@@@@@@@@@@@@      .@@@@@@@@@@@*                             
                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                         
             #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&.@@@@@@@@@*                      
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.,@@@@@@@@@@@@,                   
         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&                 
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*,/&@               
       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      %(                
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&(*,#@@@@&@@@@%@&(                     
     @@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@   ,@@& @@*                               
    .@@@@@@@@@@@@@@@@@@@@@@@@.    @@,       %%/         *@@@@@@@@@(             
    /@@@@@@@@@@@@@@@@@@@@@@%     .@%                 @@@*      (@@@@@@(         
    (@@@@@@@@@@@@@@@@@@@@@#       @&               @/              &@@@@%       
    .@@@@@@@@@@@@@@@@@@@@@        @@             /@                  @@@@@      
     @@@@@@@@@@@@@@@@@@@@&         @@            @                   .@@@@&     
      @@@@@@@@@@@@@@@@@@@@          @@           @                    @@@@@     
      (@@@@@@@@@@@@@@@@@@@%           @@         /#                  @@@@@&     
       *@@@@@@@@@@@@@@@@@@@@            /@%        @               (@@@@@@      
         @@@@@@@@@@@@@@@@@@@@@              (@%      %@/        %@@@@@@@&       
          .@@@@@@@@@@@@@@@@@@@@@@/                 .,,//,%@@@@@@@@@@@@@         
             @@@@@@@@@@@@@@@@@@@@@@@@@@@@&&%%%&@@@@@@@@@@@@@@@@@@@@@/           
               *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,              
                   &@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&                   
                        %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,                        
                                  *#&@@@@@@&#*                                                                                    
"#)?;
  writeln!(socket, "save the otters with your vote! vote for proposals you care about :)")?;
  writeln!(socket, "proposal 1: the team buys an otter and takes care of it")?;
  writeln!(socket, "proposal 2: buy some fish to feed the otters")?;
  writeln!(socket, "proposal 3: donate to the International Otter Survival Fund")?;
  writeln!(socket, "proposal 4: we go on a field trip to build some cute shelters for otters")?;

  writeln!(socket, "\nnow, vote for your choice...\n")?;

  let mut builder = ChallengeBuilder::try_from(socket.try_clone().unwrap()).unwrap();

  // load programs
  let solve_pubkey = builder.input_program().unwrap();
  let program_pubkey = builder.chall_programs(&["./solidarity.so"])[0];

  // create admin
  let admin = Keypair::new();

  // create user
  let user = Keypair::new();

  // here you go!
  writeln!(socket, "\nsome information for you:")?;
  writeln!(socket, "program: {}", program_pubkey)?;
  writeln!(socket, "admin: {}", admin.pubkey())?;
  writeln!(socket, "user: {}", user.pubkey())?;

  // fund accounts
  builder
    .builder
    .add_account_with_lamports(admin.pubkey(), system_program::ID, 100_000);
  builder
    .builder
    .add_account_with_lamports(user.pubkey(), system_program::ID, 2_000);

  let mut challenge = builder.build();

  challenge.env.execute_as_transaction(
    &[
      // initialize the smart contract
      initialize(program_pubkey, admin.pubkey()),
      
      // create proposals
      propose(program_pubkey, admin.pubkey(), admin.pubkey(), 1),
      propose(program_pubkey, admin.pubkey(), admin.pubkey(), 2),
      propose(program_pubkey, admin.pubkey(), admin.pubkey(), 3),
      propose(program_pubkey, admin.pubkey(), admin.pubkey(), 4),

      // personally, i want to go on a field trip
      vote(program_pubkey, admin.pubkey(), 4, 99_000),
    ],
    &[&admin],
  );

  // run solve
  challenge.input_instruction(solve_pubkey, &[&user]).unwrap();

  // check solve
  let balance = challenge.env.get_account(user.pubkey()).unwrap().lamports;
  writeln!(socket, "lamports: {:?}", balance)?;

  if balance > 50_000 {
    writeln!(socket, "\nWow, you must hate otters or something...")?;
    writeln!(socket, "Flag: {}", env::var("FLAG").unwrap_or_else(|_| "corctf{test_flag}".to_string()))?;
  }

  Ok(())
}