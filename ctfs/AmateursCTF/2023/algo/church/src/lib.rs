//! There once was a peaceful church consisting of `n` Warry Lu statues numbered `0, 1, ..., n - 1`.
//! The church's road network was very well developed, and there was a two-way road between each pair of (distinct) statues.
//!
//! However, recent regulations passed by the International Committee on Warry Lu Worshipping (ICWLW) demand all roads be one-way only
//! to avoid trampling situations on two-way roads. This caused quite some grief for the engineers of our church,
//! and they worked long days and nights to convert each two-way road to a one-way road.
//!
//! Byan is a traveling worshipper praying in the church.
//! Each day he starts at a statue in the church.
//! During the course of the day, he repeatedly prays to the omniscient Warry statue next to him and then
//! travels to another statue directly connected to his current statue via a road.
//! Being an efficient worshipper, he'll never visit the same statue twice over the course of a day.
//!
//! After the recent regulation changes, Byan has been running into planning issues.
//! Maximizing the amount of statues he visits each day was once an easy task, but he has been stumped by it after the recent regulation changes.
//! He now enlists in your help. He wants to know, for each statue, the longest pilgrimage he can take starting at that statue
//! (recall that such a pilgrimage cannot contain duplicate statues). In exchange, he promises you the elusive flag you seek,
//! through the help and guidance of the omniscient Warry.

/// dark secrets to be hidden from the public
///
/// the functions whose implementations are hidden:
///
#[cfg_attr(doctest, doc = " ````no_test")] // hack for syntax highlighting but no doctests (https://github.com/rust-lang/rust/issues/63193)
/// ```
/// /// Generates a valid [`Graph`] with 1412 nodes
/// pub fn gen_graph() -> Graph;
///
/// /// Requests help from the omniscient Warry to compute the optimal pilgrimages.
/// /// The `u`-th returned pilgrimage is the optimal one starting from statue `u`.
/// pub fn find_pilgrimages(g: &Graph) -> Vec<Vec<usize>>;
/// ```
pub mod ctf_private;

pub use ctf_private::{find_pilgrimages, gen_graph};

/// A graph of the church, after the regulation changes.
/// It is guaranteed that there is no road from a statue to itself, and that for all pairs of statues
/// `(u, v)` where `u ≠ v` there is either a road from `u` to `v` or from `v` to `u`.
#[derive(Clone)]
pub struct Graph(Vec<Vec<bool>>);

impl Graph {
    /// Constructs the graph, ensuring that it conforms to ICWLW standards
    pub fn new(graph: Vec<Vec<bool>>) -> Self {
        let n = graph.len();

        // the graph is an n by n array
        for v in &graph {
            assert_eq!(v.len(), n);
        }

        // no road from a statue to itself
        #[allow(clippy::needless_range_loop)]
        for i in 0..n {
            assert!(!graph[i][i]);
        }

        // exactly one road between two distinct statues
        for i in 0..n {
            for j in 0..i {
                assert!(graph[i][j] ^ graph[j][i]);
            }
        }

        Self(graph)
    }

    /// Number of cities in the church
    pub fn n(&self) -> usize {
        self.0.len()
    }

    /// Is there a one-way road taking the worshipper from statue `u` to statue `v` in the church?
    pub fn has_road(&self, u: usize, v: usize) -> bool {
        self.0[u][v]
    }

    /// Verifies that `p` is a valid pilgrimage
    pub fn assert_valid_pilgrimage(&self, p: &[usize]) {
        let n = self.n();

        // the statues worshipped exist
        for u in p {
            assert!((0..n).contains(u));
        }

        // no statue is worshipped twice
        {
            let mut vis = vec![false; n];
            for &u in p {
                assert!(!vis[u]);
                vis[u] = true;
            }
        }

        // there is a road between each adjacent pair of statues
        for w in p.windows(2) {
            assert!(self.has_road(w[0], w[1]));
        }
    }
}
