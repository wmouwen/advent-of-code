use std::cmp;
use std::io;
use std::str::FromStr;

fn main() {
    let mut surface = 0;
    let mut ribbon = 0;

    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        let it = line
            .unwrap();
        let mut it = it
            .trim()
            .split("x")
            .map(|s| i32::from_str(s).expect("failed to parse number"));

        let (x, y, z): (i32, i32, i32) = (it.next().unwrap(), it.next().unwrap(), it.next().unwrap());
        let (a, b, c) = (x * y, x * z, y * z);

        surface += 2 * (a + b + c) + cmp::min(a, cmp::min(b, c));
        ribbon += (x * y * z) + 2 * (x + y + z - cmp::max(x, cmp::max(y, z)));
    }

    println!("{}", surface);
    println!("{}", ribbon);
}

use std::io::BufRead;
