use std::io;

fn main() {
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");

    let mut floor = 0;
    let mut basement = 0;

    for (num, ch) in input.split("").enumerate() {
        floor += match ch {
            "(" => 1,
            ")" => -1,
            _ => 0,
        };
        if basement == 0 && floor == -1 {
            basement = num;
        }
    }

    println!("{}", floor);
    println!("{}", basement);
}
