FROM mcr.microsoft.com/dotnet/framework/runtime:4.8-windowsservercore-ltsc2019 as builder
WORKDIR C:/build
COPY file.txt .
SHELL ["cmd", "/S", "/C"]
RUN curl -fSLo dotnet.exe "https://dotnetcli.azureedge.net/dotnet/Runtime/5.0.8/dotnet-runtime-5.0.8-win-x64.exe" \
    && dotnet.exe /quiet /norestart /wait

RUN curl -fSLo steamcmd.zip "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip" \
    && mkdir steamcmd  \
    && tar -xf steamcmd.zip --directory steamcmd \
    && cd steamcmd \
    && steamcmd.exe +login anonymous +force_install_dir ..\csgo-ds +app_update 740 +quit \
    || exit 0

RUN curl -fSLo depotdownloader.zip "https://github.com/SteamRE/DepotDownloader/releases/download/DepotDownloader_2.4.3/depotdownloader-2.4.3-hotfix1.zip" \
    && mkdir depotdownloader \
    && tar -xf depotdownloader.zip --directory depotdownloader \
    && cd depotdownloader \
    && DepotDownloader.exe -app 740 -depot 740 -filelist ../file.txt -manifest 9207149427838134249 \
    && for /f %f in ('dir depots\\740 /b') do copy depots\740\%f\bin\vscript.dll ..\csgo-ds\bin\vscript.dll

WORKDIR C:/build/csgo-ds
COPY exclusions.txt .
# uncomment line below to create minimal setup
# RUN powershell.exe -Command "Get-ChildItem -File -Path \".\" -Recurse | Resolve-Path -Relative | where {@(gc exclusions.txt) -notcontains $_} | Remove-Item"

FROM mcr.microsoft.com/windows/servercore:ltsc2019 as plugin-builder
WORKDIR C:/build
SHELL ["cmd", "/S", "/C"]
RUN mkdir csgo-ds\csgo\addons\sourcemod\extensions \
    && mkdir csgo-ds\csgo\addons\sourcemod\scripting \
    && mkdir csgo-ds\csgo\addons\sourcemod\plugins
RUN curl -fSLo metamod.zip "https://mms.alliedmods.net/mmsdrop/1.11/mmsource-1.11.0-git1145-windows.zip" \
    && tar -xf metamod.zip --directory .\csgo-ds\csgo
RUN curl -fSLo sourcemod.zip "https://sm.alliedmods.net/smdrop/1.10/sourcemod-1.10.0-git6510-windows.zip" \
    && tar -xf sourcemod.zip --directory .\csgo-ds\csgo

COPY sq.sp ./csgo-ds/csgo/addons/sourcemod/scripting
RUN cd .\csgo-ds\csgo\addons\sourcemod\scripting \
    && spcomp.exe sq.sp \
    && move sq.smx ..\plugins\sq.smx
RUN echo "" > csgo-ds\csgo\addons\sourcemod\extensions\sq.autoload

FROM mcr.microsoft.com/windows/servercore:ltsc2019 as ext-builder
WORKDIR C:/build
SHELL ["cmd", "/S", "/C"]
RUN curl -fSLo vs_buildtools.exe https://aka.ms/vs/16/release/vs_buildtools.exe
RUN vs_buildtools.exe --quiet --wait --norestart --nocache \
    --installPath C:\BuildTools \
    --add Microsoft.Component.MSBuild \
    --add Microsoft.VisualStudio.Component.Windows10SDK.18362 \
    --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64	\
  || IF "%ERRORLEVEL%"=="3010" EXIT 0

RUN curl -fSLo rustup-init.exe https://win.rustup.rs/x86_64
RUN start /w rustup-init.exe -y -v && echo "Error level is %ERRORLEVEL%"
RUN del rustup-init.exe

RUN setx /M PATH "C:\Users\ContainerAdministrator\.cargo\bin;%PATH%"
RUN rustup target add i686-pc-windows-msvc
ENV RUSTFLAGS="-C target-feature=+crt-static -C codegen-units=1"
COPY sq_ext .
RUN cargo build --all --all-targets --target=i686-pc-windows-msvc --release

FROM mcr.microsoft.com/windows/servercore:ltsc2019 as runner
COPY --from=builder C:/build/csgo-ds C:/csgo-ds
COPY --from=plugin-builder C:/build/csgo-ds C:/csgo-ds
COPY --from=ext-builder C:/build/target/i686-pc-windows-msvc/release/sq_ext.dll C:/csgo-ds/csgo/addons/sourcemod/extensions/sq.ext.dll
COPY run.ps1 .
COPY flag.bat .
RUN copy C:\Windows\System32\curl.exe .
WORKDIR C:/csgo-ds
CMD powershell -ExecutionPolicy Bypass -File C:\run.ps1