%Build script to beep-boop (UMDCTF2023, author: Assgent)

%{
A flag was encoded into a sound file using the script below. 
Analyze the script and reverse-engineer the flag!
%}

close
clear all

flag = fileread("flag.txt");

Fs = 8192;
sound = string_to_sound(flag, Fs, 1, 0.5);

sound_normalized = sound / (max(abs(sound)));
audiowrite("sound.wav", sound_normalized, Fs);

function freq = get_frequency_1(char)
    freq = char * 13;
end

function freq = get_frequency_2(char)
    freq = (char - 50) * 11;
end


% Fs is the samples/sec.
% T is the duration of each key. (in seconds)
% Tpause is the pause between keys. (in seconds)
function x = string_to_sound(keys,Fs,T,Tpause)
    t = (0:fix(T*Fs)).'/Fs ;
    zp = zeros(fix(Tpause*Fs/2),1) ;
    x = [];
    for r = 1:length(keys(:))
        char = keys(r);
        x = [x ; zp ; cos(2*pi*get_frequency_1(char)*t) + cos(2*pi*get_frequency_2(char)*t) ; zp];
    end
end