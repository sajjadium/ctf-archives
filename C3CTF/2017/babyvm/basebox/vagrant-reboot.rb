# Adapted from https://www.exratione.com/2014/06/how-to-reboot-a-vagrant-guest-vm-during-provisioning/
#
require 'vagrant'
 
class RebootPlugin < Vagrant.plugin('2')
  name 'Reboot Plugin'
 
  # This plugin provides a provisioner called unix_reboot.
  provisioner 'unix_reboot' do
    # Create a provisioner.
    class RebootProvisioner < Vagrant.plugin('2', :provisioner)
      # Initialization, define internal state. Nothing needed.
      def initialize(machine, config)
        super(machine, config)
      end
 
      # Configuration changes to be done. Nothing needed here either.
      def configure(root_config)
        super(root_config)
      end
 
      # Run the provisioning.
      def provision
        command = 'reboot'
        @machine.ui.info("Issuing command: #{command}")
        @machine.communicate.sudo(command) do |type, data|
          if type == :stderr
            @machine.ui.error(data);
          end
        end
 
        begin
          sleep 5
        end until @machine.communicate.ready?
      end
 
      # Nothing needs to be done on cleanup.
      def cleanup
        super
      end
    end
    RebootProvisioner
  end
end
