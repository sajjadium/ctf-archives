library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity SuperABS is
    port (
        brake : in STD_LOGIC_VECTOR(7 downto 0); -- Brake
        data: inout STD_LOGIC; -- 2-Wire connection to humidity sensor
        busy: inout STD_LOGIC; -- 2-Wire connection to humidity sensor
        clk : in STD_LOGIC; -- Clock
        handbrake : in STD_LOGIC; -- Handbrake
        left_rear_brake : out STD_LOGIC_VECTOR(7 downto 0); -- Percent of brake applied to left rear wheel
        right_rear_brake : out STD_LOGIC_VECTOR(7 downto 0); -- Percent of brake applied to right rear wheel
        left_front_brake : out STD_LOGIC_VECTOR(7 downto 0); -- Percent of brake applied to left front wheel
        right_front_brake : out STD_LOGIC_VECTOR(7 downto 0); -- Percent of brake applied to right front wheel
    );
end entity SuperABS;

architecture Behavioural of SuperABS is
type SensorStatus is (NONE, INITIALIZING, INITIALIZED);
signal sensor_current_status : SensorStatus := NONE;
signal init_status : integer := 0;
signal config_status : integer := 0;
signal busy_value : STD_LOGIC := '0';
signal data_value : STD_LOGIC := '0';
signal data_to_send : STD_LOGIC_VECTOR(15 downto 0) := (others => '0');
signal data_to_send_index : integer := 0;
signal read_status : integer := 0;
signal high_data : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');
signal low_data : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');
signal read_index : integer := 0;
signal humidity_value : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');
signal brake_value : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');

begin
    -- Trigger for handbrake and brake value change
    process(handbrake, brake)
    begin
        if handbrake = '1' then
            left_rear_brake <= (others => '1');
            right_rear_brake <= (others => '1');
            left_front_brake <= (others => '1');
            right_front_brake <= (others => '1');
        else -- if handbrake is not pulled use normal brake value
            brake_value <= brake * humidity_value;
            left_rear_brake <= brake_value;
            right_rear_brake <= brake_value;
            left_front_brake <= brake_value;
            right_front_brake <= brake_value;
        end if;
    end process;

    -- Clock for synchronous communication with humidity sensor
    process(clk)
    begin
        if rising_edge(clk) then
            if sensor_current_status = NONE then -- if the sensor is not initialized
                -- procedure for initializing the sensor
                case init_status is
                    when 0 =>
                        busy_value <= '0';
                        data_value <= '1';
                    when 1 =>
                        busy_value <= '1';
                        data_value <= '1';
                    when 2 =>
                        busy_value <= '0';
                        data_value <= '1';
                    when 3 =>
                        busy_value <= '1';
                        data_value <= '0';
                        sensor_current_status <= INITIALIZING;
                end case;
                init_status <= init_status + 1;
                busy <= busy_value;
                data <= data_value;
            elsif sensor_current_status = INITIALIZING then -- filling the sensor registers
                if data_to_send = (others => '0') then -- before writing something, wait for the buffer to be empty
                    case config_status is
                        when 0 =>
                            high_data <= B"10101101"; -- SET SRC REG
                            low_data <= B"00000011"; -- PARAM
                        when 1 =>
                            high_data <= B"10111111"; -- SET DST REG
                            low_data <= B"00000001"; -- POWER SAVE
                        when 2 =>
                            high_data <= B"10001101"; -- SET PARAM REG
                            low_data <= X"69"; -- ALWAYS_ACTIVE
                        when 3 =>
                            high_data <= B"01001111"; -- MOVE
                            low_data <= B"00000000"; -- NO PARAM
                        when 4 =>
                            high_data <= B"10101001"; -- SET SRC REG
                            low_data <= B"00000011"; -- PARAM
                        when 5 =>
                            high_data <= B"10111111"; -- SET DST REG
                            low_data <= B"1001100";  -- MODE
                        when 6 =>
                            high_data <= B"10000001"; -- SET PARAM REG
                            low_data <= X"20"; -- 16bit size
                        when 7 =>
                            high_data <= B"01001111"; -- MOVE
                            low_data <= B"00000000"; -- NO PARAM
                        when 8 => -- End initialization
                            sensor_current_status <= INITIALIZED;
                            high_data <= (others => '0');
                            low_data <= (others => '0');
                    end case;
                    config_status <= config_status + 1;
                    data_to_send <= high_data & low_data;
                end if;
            elsif sensor_current_status = INITIALIZED then -- Send continuosly GET VALUE command and wait for response
                if read_status = 0 then -- phase 1: send command
                    high_data <= B"01101000"; -- GET VALUE
                    low_data <= B"00000000"; -- NO PARAM
                    data_to_send <= high_data & low_data;
                    read_status = 1; -- pass to phase 2 (waiting for response)
                end if;
            end if;
        end if;
        if not (sensor_current_status = NONE) then -- sending 
            busy_value <= clk;
            busy <= busy_value;
            if rising_edge(clk) then
                if not (data_to_send = (others => '0')) then
                    if data_to_send_index = 16 then
                        data_to_send_index <= 0;
                        data_to_send <= (others => '0');
                        data_value = '0';
                        data <= data_value;
                    end if;
                    data_value <= data_to_send(data_to_send_index);
                    data <= data_value;
                    data_to_send_index <= data_to_send_index + 1;
                end if;
            end if;
        end if;
        if sensor_current_status = INITIALIZED then
            if read_status = 1 then -- Check if read-phase-2 is active
                if busy = '1' then -- Check if busy value is high
                    if read_index = 16 then -- wait for the end of the transmission (16 bits)
                        read_index <= 0;
                        read_status <= 0;
                    elsif < 8 then -- read only the first byte
                        humidity_value(7 - read_index) <= data;
                    end if;
                    read_index <= read_index + 1; -- increment bit counter
                end if;
            end if;
        end if;
    end process;
end architecture Behavioural;
