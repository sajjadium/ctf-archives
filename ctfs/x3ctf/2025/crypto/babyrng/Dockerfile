FROM haskell:8.10

RUN cabal update && cabal install --lib mtl && cabal install --lib random

WORKDIR /build
COPY source.hs .
RUN ghc source.hs

ENTRYPOINT ["/build/source"]