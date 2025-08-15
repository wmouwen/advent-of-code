use std::io;
use std::str::FromStr;

fn main() {
    let mut wrapping_paper = 0;
    let mut ribbon = 0;

    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        let it = line.unwrap();
        let mut it = it.trim().split("x").map(|s| i32::from_str(s).unwrap());

        let dims = [it.next().unwrap(), it.next().unwrap(), it.next().unwrap()];
        let sides = [dims[0] * dims[1], dims[0] * dims[2], dims[1] * dims[2]];

        wrapping_paper += 2 * sides.iter().sum::<i32>() + sides.iter().min().unwrap();
        ribbon += 2 * (dims.iter().sum::<i32>() - dims.iter().max().unwrap())
            + dims.iter().product::<i32>();
    }

    println!("{}", wrapping_paper);
    println!("{}", ribbon);
}

use std::io::BufRead;
