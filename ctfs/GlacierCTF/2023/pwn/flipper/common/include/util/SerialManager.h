#pragma once

#include "types.h"
#include "chardev.h"

#define MAX_PORTS  16

class ArchSerialInfo;

class SerialPort : public CharacterDevice
{
  public:
    typedef enum _br
    {
      BR_9600, BR_14400, BR_19200, BR_38400, BR_55600, BR_115200
    } BAUD_RATE_E;

    typedef enum _par
    {
      ODD_PARITY, EVEN_PARITY, NO_PARITY
    } PARITY_E;

    typedef enum _db
    {
      DATA_7, DATA_8
    } DATA_BITS_E;

    typedef enum _sb
    {
      STOP_ONE, STOP_TWO, STOP_ONEANDHALF
    } STOP_BITS_E;

    typedef enum _sres
    {
      SR_OK, SR_ERROR // you might want to add elements for common errors that can appear
    } SRESULT;

    SerialPort(char*, ArchSerialInfo port_info);

    ~SerialPort();

    /**
     * Opens a serial port for reading or writing
     * @param baud_rate Speed @see BAUD_RATE_E
     * @param data_bits Data bits @see DATA_BITS_E
     * @param stop_bits Stop bits @see STOP_BITS_E
     * @param parity Parity @see PARITY_E
     * @return Result @see SERIAL_ERROR_E
     */
    SRESULT setup_port(BAUD_RATE_E baud_rate, DATA_BITS_E data_bits, STOP_BITS_E stop_bits, PARITY_E parity);

    /**
     * Writes size bytes to serial port
     * @param offset Not used with serial ports
     * @param size Number of bytes to be written
     * @param buffer The data to be written
     * @return Number of bytes actualy written or -1 in case of an error
     */
    virtual int32 writeData(uint32 offset, uint32 size, const char*buffer);

    void irq_handler();

    /**
     * Returns the Architecture specific data for this serial port.
     * The basic task of any operating system is to hide this ugly data.
     * This function is mainly called from SerialManager and I do not think
     * that it is needed anywhere else. Perhaps it could be protected and
     * SerialManager declared as a friend class.
     * @return @see ArchSerialInfo
     */
    ArchSerialInfo get_info()
    {
      return port_info_;
    }
    ;

  private:
    void write_UART(uint32 reg, uint8 what);
    uint8 read_UART(uint32 reg);

    size_t WriteLock;
    size_t SerialLock;

  private:
    ArchSerialInfo port_info_;

};

class SerialManager
{
  public:
    static SerialManager *instance_;

    static SerialManager * getInstance()
    {
      if (!instance_)
        instance_ = new SerialManager();

      return instance_;
    }
    ;

    SerialManager();
    ~SerialManager();

    SerialPort * serial_ports[ MAX_PORTS];

    uint32 do_detection(uint32 is_paging_set_up);
    uint32 get_num_ports();
    uint32 get_port_number(const uint8* friendly_name);
    void service_irq(uint32 irq_num);

  private:
    uint32 num_ports;
};

