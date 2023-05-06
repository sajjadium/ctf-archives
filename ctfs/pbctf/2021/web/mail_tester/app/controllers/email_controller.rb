class EmailController < ApplicationController
  def index; end

  def create
    if email_params[:to] && email_params[:message]
      send_mail
      flash[:notice] = 'Email has been sent'
    else
      flash[:notice] = 'Must supply and address and a message'
    end

    redirect_to email_url
  end

  def email_params
    params.permit(:to, :message)
  end

  private

  def send_mail
    IO.popen("/usr/sbin/sendmail -B 7BIT -i -f app@localhost -- #{quoted_to}", 'w+', err: :out) do |io|
      io.puts email_params[:message]
      io.flush
    end
  end

  def quoted_to
    %("#{email_params[:to].shellescape}")
  end
end
