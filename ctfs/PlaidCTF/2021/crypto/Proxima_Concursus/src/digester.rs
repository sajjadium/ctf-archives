/// The main hashing algorithm
pub struct Digest {
    /// Internal state of the hash algorithm.
    state: (u64, u64),

    /// Total number of data bytes that have been inserted for
    /// hashing.
    bytes_inserted: usize,

    /// Number of bytes of `compression_queue` that are yet to be
    /// compressed into the state.
    uncompressed_len: usize,

    /// Bytes yet to be compressed into the state. Only the first
    /// `uncompressed_len` bytes are valid.
    compression_queue: [u8; Self::COMPRESSION_QUEUE_SIZE],
}

impl Digest {
    /// Number of bytes compressed in a single compression operation.
    const COMPRESSION_QUEUE_SIZE: usize = 8;

    /// Basic padding added to the end of the entire message.
    const BASIC_PADDING: [u8; Self::COMPRESSION_QUEUE_SIZE] = [0x80, 0, 0, 0, 0, 0, 0, 0];

    /// Initial state.
    ///
    /// Nothing-up-my-sleeve number: `floor(pi * 2^124)`.
    const INITIAL_STATE: (u64, u64) = (0x3243f6a8885a308d, 0x313198a2e0370734);

    /// Number of Feistel rounds in each compresison.
    const NUMBER_OF_FEISTEL_ROUNDS: usize = 5;

    /// Round keys for Feistel cipher.
    ///
    /// Nothing-up-my-sleeve numbers: `floor(sqrt(p) * 2^30)` for
    /// the first few primes `p`
    const KEYS: [u64; Self::NUMBER_OF_FEISTEL_ROUNDS] =
        [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xa953fd4e, 0xd443949f];

    /// Shift constants for internal Feistel round function.
    ///
    /// Nothing-up-my-sleeve numbers: `floor(sqrt(13) * 2^20)`
    const SHIFT_CONSTANTS: [u32; 6] = [0xe, 0x6, 0xc, 0x1, 0x5, 0xa];

    /// Create a new instance of the hasher.
    fn new() -> Self {
        Self {
            state: Self::INITIAL_STATE,
            bytes_inserted: 0,
            uncompressed_len: 0,
            compression_queue: [0u8; 8],
        }
    }

    /// Compress the current compression queue into the state if
    /// possible. Will not run if not enough of the queue is full yet.
    ///
    /// Ensures that the compression queue is not full when it
    /// finishes executing.
    fn compress_if_possible(&mut self) {
        // If there aren't enough bytes to fully compress, we
        // early-exit, since there weren't enough bytes to fill up the
        // compression queue.
        if self.uncompressed_len != self.compression_queue.len() {
            return;
        }

        // Compress the current compression queue
        let (mut l, mut r) = self.state;
        l ^= u64::from_le_bytes(self.compression_queue);
        for &k in &Self::KEYS {
            let mut x = k;
            let mut y = r.rotate_left(10);
            assert_eq!(Self::SHIFT_CONSTANTS.len(), 6);
            x ^= y.wrapping_add(x.wrapping_shl(Self::SHIFT_CONSTANTS[0]));
            y ^= y.wrapping_shl(Self::SHIFT_CONSTANTS[1]);
            x ^= y.wrapping_add(x.wrapping_shr(Self::SHIFT_CONSTANTS[2]));
            y ^= y.wrapping_shr(Self::SHIFT_CONSTANTS[3]);
            x ^= y.wrapping_add(x.wrapping_shl(Self::SHIFT_CONSTANTS[4]));
            y ^= y.wrapping_shl(Self::SHIFT_CONSTANTS[5]);
            let z = (x ^ y).rotate_left(1) ^ l;
            l = r;
            r = z;
        }
        self.state = (l, r);

        // The compression queue is now empty
        self.uncompressed_len = 0;
    }

    /// Adds a prefix of `data` into the queue, returning the un-added
    /// suffix.
    fn add_prefix_to_queue<'a>(&mut self, data: &'a [u8]) -> &'a [u8] {
        // Skim off the first few bytes
        let early_compressible = usize::min(
            self.compression_queue.len() - self.uncompressed_len,
            data.len(),
        );
        self.compression_queue[self.uncompressed_len..self.uncompressed_len + early_compressible]
            .copy_from_slice(&data[..early_compressible]);
        self.uncompressed_len += early_compressible;

        // Return the uncompressed data
        &data[early_compressible..]
    }

    /// Appends `data` to be hashed.
    fn append<T: AsRef<[u8]>>(&mut self, data: T) {
        let mut data: &[u8] = data.as_ref();
        self.bytes_inserted += data.len();
        while !data.is_empty() {
            data = self.add_prefix_to_queue(data);
            self.compress_if_possible();
        }
    }

    /// Perform final padding and compression.
    fn finalize(&mut self) {
        // Perform basic padding
        let padding_size =
            Self::COMPRESSION_QUEUE_SIZE - (self.bytes_inserted % Self::COMPRESSION_QUEUE_SIZE);
        let remaining = self.add_prefix_to_queue(&Self::BASIC_PADDING[..padding_size]);
        assert!(remaining.is_empty());
        self.compress_if_possible();

        // Perform length padding
        let length_padding = self.bytes_inserted.to_le_bytes();
        let remaining = self.add_prefix_to_queue(&length_padding);
        assert!(remaining.is_empty());
        self.compress_if_possible();

        // By now, everything should've been compressed away
        assert_eq!(self.uncompressed_len, 0);
    }

    /// Produces the a shortened hash of all the data that has been added.
    fn digest(mut self) -> u64 {
        // Perform final processing
        self.finalize();

        // Return middle 64 bits
        self.state.0.wrapping_shl(32) | self.state.1.wrapping_shr(32)
    }

    /// Produce a short hex-digest of `data`.
    pub fn hex_digest_of<T: AsRef<[u8]>>(data: T) -> String {
        let mut this = Self::new();
        this.append(data);
        format!("{:016x}", this.digest())
    }
}
