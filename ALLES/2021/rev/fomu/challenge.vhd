library ieee;
context ieee.ieee_std_context;


use work.components.all;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;

entity Fomu_Blink is
  port (
    clki: in std_logic;

    rgb0: out std_logic;
    rgb1: out std_logic;
    rgb2: out std_logic;

    user_1: in std_logic;
    user_2: out std_logic;
    user_3: out std_logic;
    user_4: in std_logic;

    -- USB Pins (which should be statically driven if not being used)
    usb_dp: out std_logic;
    usb_dn: out std_logic;
    usb_dp_pu: out std_logic
  );
end;



architecture arch of Fomu_Blink is

  signal clk: std_logic;
  signal fast_counter: std_logic_vector(17 downto 0);
  signal counter1_debouncer: unsigned(3 downto 0) := (others=>'0');
  signal counter4_debouncer: unsigned(3 downto 0) := (others=>'0');

  signal msb_fast_counter: std_logic;
  signal switch: std_logic := '1';
  signal red: std_logic;
  signal green: std_logic;
  signal blue: std_logic;
  signal user_1_a:std_logic;
  signal user_4_a:std_logic;
  signal user_1_s: std_logic;
  signal user_4_s: std_logic;
  type debounce_state is (out0, out1);
  signal user_1_state: debounce_state;
  signal user_4_state: debounce_state;
  signal user_1_debounced: std_logic := ('0');
  signal user_4_debounced: std_logic := ('0');
  signal user_1_rising_edge: std_logic := ('0');
 signal user_4_rising_edge: std_logic := ('0');



 signal led_io: std_logic_vector(2 downto 0) := (others=>'0');
 signal led_flag: std_logic_vector(2 downto 0) := (others=>'0');

 type led_mux_state is (inpMode, flagMode);
 signal led_mux : led_mux_state := inpMode;

 signal rhold : unsigned(4 downto 0) := (others => '0');
  signal shift_counter: unsigned(21 downto 0) := (others=>'0');
  type r_active_state is (rOn, rOff);
  signal r_active : r_active_state := rOff;
  signal readIn : std_logic := ('0');


  signal flag1Ref : std_logic_vector(20 downto 0) := "111101110101110000011";
  signal flag2Ref : std_logic_vector(31 downto 0) := "11111111111111111111111111111110";

  signal flag1Shift : std_logic_vector(40 downto 0) := (others => '1');
  signal flag2Shift : std_logic_vector(40 downto 0) := (others => '1');




  signal flag1Solved : std_logic := '0';
  signal flag1 : std_logic_vector(127 downto 0) := 
  "01100100011100100110010100101110011011000110100100101111111100001001111110011000100011101111000010011111100011111011001100000000";

  signal flag2 : std_logic_vector(143 downto 0) := 
  "011110010011001001110101001011100110001001100101001011110110010001010001011101110011010001110111001110010101011101100111010110000110001101010001";
  
  signal flag2Solved : std_logic := '0';

  signal test1:std_logic_vector(15 downto 0) := (others => '1');

  signal flOut : std_logic_vector(15 downto 0) := (others => '1');

  signal im : std_logic_vector(15 downto 0) := (others => '0');
  signal once : std_logic_vector(3 downto 0) := "1111";
  signal SA : std_logic_vector(15 downto 0) := (others => '0');
  signal SB : std_logic_vector(15 downto 0) := "1101100110011001";
  signal SC : std_logic_vector(15 downto 0) := (others=>'0');
 signal SD : std_logic_vector(15 downto 0) := (others => '0');
 signal dout : std_logic_vector(31 downto 0) := (others => '1');

begin

-- oh mac16 oh mac16 oracle... what is your secret?
mac16: SB_MAC16
generic map (A_REG => 1, B_REG=>1, C_REG => 1, D_REG=>1, BOTOUTPUT_SELECT=>0, BOTADDSUB_UPPERINPUT => 1, BOTADDSUB_CARRYSELECT => 1, BOTADDSUB_LOWERINPUT => 2, TOPADDSUB_UPPERINPUT => 1, TOPADDSUB_CARRYSELECT => 2, TOPOUTPUT_SELECT => 0, TOPADDSUB_LOWERINPUT => 2) 
port map(clk=>clk, A=>SA, B=>SB, C=>SC, D=>SD, O=>dout, CI => '0', OLOADBOT => '0', OHOLDBOT=>'1', ORSTBOT=>'1', OLOADTOP => '0', ORSTTOP=>'1', OHOLDTOP=>'1', ADDSUBTOP=>'1');



  -- Assign USB pins to "0" so as to disconnect Fomu from
  -- the host system.  Otherwise it would try to talk to
  -- us over USB, which wouldn't work since we have no stack.
  usb_dp    <= '0';
  usb_dn    <= '0';
  usb_dp_pu <= '0';
  user_2 <= '0';
  user_3 <= '0';

im(1 downto 0) <= "00";
  im(15 downto 2) <= (others => '0');



  -- Connect to system clock (with buffering)
  clk_gb: SB_GB
  port map (
    USER_SIGNAL_TO_GLOBAL_BUFFER => clki,
    GLOBAL_BUFFER_OUTPUT => clk
  );

  process(clk)
  begin
	  if (rising_edge(clk)) then
		  SA <= flag1(SA'left downto 0);
		  SB <= flag1(flag1'left downto flag1'left-15);
		  SC <= flag1(68 downto (68-15));
		  SD <= flag1(86 downto (86-15));

		flag2Ref(31 downto 0) <= not dout(31 downto 0);
	  end if;
  end process;

  -- Use counter logic to divide system clock.  The clock is 48 MHz,
  -- so we divide it down by 2^22.
  process(clk)
  begin
    if rising_edge(clk) then
      shift_counter <= shift_counter + 1;
      fast_counter <= std_logic_vector(unsigned(fast_counter) + 1);
      msb_fast_counter <= fast_counter(fast_counter'left);
    end if;
  end process;
  

  -- Instantiate iCE40 LED driver hard logic, connecting up
  -- counter state and LEDs.
  --
  -- Note that it's possible to drive the LEDs directly,
  -- however that is not current-limited and results in
  -- overvolting the red LED.
  --
  -- See also:
  -- https://www.latticesemi.com/-/media/LatticeSemi/Documents/ApplicationNotes/IK/ICE40LEDDriverUsageGuide.ashx?document_id=50668
  rgba_driver: SB_RGBA_DRV
  generic map (
    CURRENT_MODE => "0b1",      -- half current
    RGB0_CURRENT => "0b000011", -- 4 mA
    RGB1_CURRENT => "0b000011", -- 4 mA
    RGB2_CURRENT => "0b000011"  -- 4 mA
  )
  port map (
    CURREN   => '1',
    RGBLEDEN => switch,
    RGB0PWM  => green, -- Green
    RGB1PWM  => red, -- Red
    RGB2PWM  => blue, -- Blue
    RGB0     => rgb0,
    RGB1     => rgb1,
    RGB2     => rgb2
  );

  user_input : process(clk)
  begin
    if rising_edge(clk) then
      user_1_a <= user_1;
      user_4_a <= user_4;
      user_1_s <= user_1_a;
      user_4_s <= user_4_a;
    end if;
  end process ;

  debouncer : process( clk )
  begin
    if rising_edge(clk) then
      user_1_rising_edge <= '0';
      user_4_rising_edge <= '0';
      counter1_debouncer <= counter1_debouncer;
      counter4_debouncer <= counter4_debouncer;

      user_1_debounced <= user_1_debounced;
      user_1_state <= user_1_state;

      led_io(1) <= not user_1_debounced;
      led_io(2) <= not user_4_debounced;
      if msb_fast_counter = '0' and fast_counter(fast_counter'left) = '1' then
        if user_1_s = '1' then
          if counter1_debouncer < 15 then
            counter1_debouncer <= counter1_debouncer + 1;
          end if;
        else
          if counter1_debouncer > 0 then
            counter1_debouncer <= counter1_debouncer - 1;
          end if;
        end if;

	if user_4_s = '1' then
          if counter4_debouncer < 15 then
            counter4_debouncer <= counter4_debouncer + 1;
          end if;
        else
          if counter4_debouncer > 0 then
            counter4_debouncer <= counter4_debouncer - 1;
          end if;
        end if;

      end if;

      case user_1_state is
        when out0 =>
          if counter1_debouncer = 15 then
            user_1_debounced <= '1';
            user_1_rising_edge <= '1';
            user_1_state <= out1;
          end if;
        when out1 =>
          if counter1_debouncer = 0 then
            user_1_debounced <= '0';
            user_1_state <= out0;
          end if;
        when others =>
          user_1_debounced <= '0';
          user_1_state <= out0;
      end case ;

     case user_4_state is
        when out0 =>
	  if counter4_debouncer = 15 then
            user_4_debounced <= '1';
            user_4_rising_edge <= '1';
            user_4_state <= out1;
          end if;
        when out1 =>
	  if counter4_debouncer = 0 then
            user_4_debounced <= '0';
            user_4_state <= out0;
          end if;
        when others =>
          user_4_debounced <= '0';
          user_4_state <= out0;
      end case ;

    end if;
  end process ;

  process(clk)
  begin
	  if rising_edge(clk) then
		  readIn <= '0';
if shift_counter = 0 then
	case r_active is
		when rOn =>
			led_io(0) <= '1';
			led_flag(0) <= '1';
			rhold <= (others => '0');
			r_active <= rOff;
		when rOff =>
			led_io(0) <= '0';
			led_flag(0) <= '0';
			rhold <= rhold + 1;
			if (rhold + 1) = 0 then
				r_active <= rOn;
				readIn <= '1';
			end if;
		when Others =>
			led_io(0) <= '1';
			led_flag(0) <= '0';
			rhold <= (others => '0');
	end case;

	end if;
	end if;

  end process;

  process (clk)
  begin
	  if rising_edge(clk) then
			flag1Solved <= flag1Solved;
			flag2Solved <= flag2Solved;

		  if readIn = '1' then
			flag1Shift(flag1Shift'left downto 3) <= flag1Shift(flag1Shift'left-3 downto 0);
			flag1Shift(0) <= user_1_debounced;
			flag1Shift(1) <= user_4_debounced;
			flag1Shift(2) <= user_1_debounced xor user_4_debounced;
			flag2Shift(flag2Shift'left downto 2) <= flag2Shift(flag2Shift'left-2 downto 0);
			flag2Shift(0) <= user_1_debounced;
			flag2Shift(1) <= user_4_debounced;
		else
			if (flag1Shift(flag1Ref'left downto 0) = flag1Ref) then
				flag1Solved <= '1';
			else
				if (flag2Shift(flag2Ref'left downto 0) = flag2Ref) then
					flag2Solved <= '1';
				end if;
			end if;

		  end if;
	  end if;
  end process;

  process (clk)
  begin

	  if rising_edge(clk) then
		if (readIn = '1') then
			if (once = "1111") then
				once <= "0000";
			else
				if (flag1Solved = '1') then
					flag1(flag1'left downto 2) <= flag1(flag1'left-2 downto 0);
					led_flag(2) <= flag1(flag1'left);
					led_flag(1) <= flag1(flag1'left-1);
					flag1(0) <= flag1(flag1'left-1);
					flag1(1) <= flag1(flag1'left);
				else
					if (flag2Solved = '1') then
						flag2(flag2'left downto 2) <= flag2(flag2'left-2 downto 0);
						led_flag(2) <= flag2(flag2'left);
						led_flag(1) <= flag2(flag2'left-1);
						flag2(0) <= flag2(flag2'left-1);
						flag2(1) <= flag2(flag2'left);
					end if;
				end if;
			end if;
		end if;
	end if;
  end process;
  
-- led output mux
  process(clk)
  begin
	  if rising_edge(clk) then
	 switch <= '1';
	led_mux <= inpMode;

 case led_mux is
	 when inpMode =>
		  red <= led_io(0);
		  green <= led_io(1);
		  blue <= led_io(2);
	 	  if (flag1Solved = '1') or (flag2Solved = '1') then
		 	led_mux <= flagMode;
		else
			led_mux <= inpMode;
		end if;

	  when flagMode =>
		  red <= led_flag(0);
		  green <= led_flag(1);
		  blue <= led_flag(2);
		 led_mux <= flagMode;


	  when others =>
		  red <= '0';
		  green <= '0';
		  blue <= '0';
 end case;
          end if;
  end process;

end;
